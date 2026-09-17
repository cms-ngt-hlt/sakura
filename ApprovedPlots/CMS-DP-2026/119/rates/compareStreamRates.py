#!/usr/bin/env python3
"""
Compares HLT vs NGT Demonstrator stream rates and bandwidths across every categorisation and split.

Reuses TSG STEAM's rate plotting style and classification rules: https://github.com/cms-steam/RateDPS

Inputs from OMS (HLT) and F3Mon (NGT) in JSON format:
RateDPS/OMS_query/get_stream_info.py is used to dump OMS information into a JSON. F3Mon JSON output should be prepared in the same type of format.

HLT_JSON_PATH: full per-LS records from OMS, one entry per stream per LS with all fields (rate, size, bandwidth, start_time, pileup, deadtime, delivered_lumi_per_lumisection, hlt_rate_Status_OnGPU, ...).

NGT_JSON_PATH: F3Mon-derived per-LS records for the NGT Demonstrator, with only {LS, rate, size, bandwidth}. Missing metadata (e.g. luminosity, PU, etc.) is assumed identical between the two instances and taken from OMS. Rate and bandwidth are scaled by NGT_PRESCALE (110) before any aggregation.

Outputs in form of stream rates and bandwidths (per run, per split, per quantity the split supports).
"""

import os
import re
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional

import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import mplhep as hep
from matplotlib.ticker import MultipleLocator, FuncFormatter

# -----------------------------------------------------------------------------
# Configuration (mirrors 2025_NGT.ipynb)
# -----------------------------------------------------------------------------

RUN = "398802"

HLT_JSON_PATH = "data/run_398802.json"
NGT_JSON_PATH  = "data/streamRates_F3Mon_ngtdemonstrator_398802_F3MonToOMS.json"

FILL_FIG  = "run398802"
FILL_TEXT = "Fill 11237, November 2025"
DEFAULT_OUTDIR = "/eos/user/m/mzarucki/www/2026/NGT/SAKURA/NERD/rates/comparisons"
os.makedirs(DEFAULT_OUTDIR + "/" + FILL_FIG, exist_ok=True)

QUANTITY_SUBDIR = {"rate": "rates", "bandwidth": "bandwidths"}


def output_dir(quantity):
    """Output directory for a given quantity -- rate plots go under 'rates/',
    bandwidth plots go under 'bandwidth/', both created on first use."""
    d = f"{DEFAULT_OUTDIR}/{FILL_FIG}/{QUANTITY_SUBDIR[quantity]}"
    os.makedirs(d, exist_ok=True)
    return d

SMOOTH_WINDOW = 5
YEAR       = 2025
LUMI_LABEL = 0.43  # 428.56 pb^-1 = 0.42856 fb^-1

CMS_ENERGY = 13.6

FIGSIZE = (16, 10)

# 398802
PRESCALE_LSES = []
IGNORE_LSES   = []
LS_CUT        = 1

HLT_LABEL = "HLT"
NGT_LABEL  = "NGT Demonstrator"
NGT_PRESCALE = 110
NGT_DASH = (0, (1, 2.2))

RATIO_YLIM = {
    "rate":      (0.8, 1.3),
    "bandwidth": (0.8, 1.3),
}
LS_DURATION = 23.31

METADATA_FIELDS = (
    "start_time", "delivered_lumi_per_lumisection", "pileup",
    "deadtime", "hlt_rate_Status_OnGPU", "run_number", "lumisection_number", "time",
)

QUANTITY_INFO = {
    "rate":      dict(ylabel_unit="kHz",  ylabel_word="Rate"),
    "bandwidth": dict(ylabel_unit="GB/s", ylabel_word="Bandwidth"),
}

# -----------------------------------------------------------------------------
# Helpers 
# -----------------------------------------------------------------------------

def moving_average(data, window_size=SMOOTH_WINDOW):
    arr = np.array(data, dtype=float)
    if len(arr) < window_size:
        return np.array([])
    csum = np.cumsum(np.insert(arr, 0, 0.0))
    return (csum[window_size:] - csum[:-window_size]) / float(window_size)


def hhmm_fmt(x, pos=None):
    h = int(x)
    m = int(round((x - h) * 60))
    return f"{h:02d}:{m:02d}"


def safe_name(name):
    """Make a category name filesystem-safe (e.g. a name containing '/')."""
    return re.sub(r"[^\w\-]+", "_", name)


def short_category_label(name):
    """Drop the redundant 'Parking' prefix from parking sub-category names
    (e.g. ParkingSingleMuon -> SingleMuon) for compact display -- the plain
    'Parking' category itself (from the top-level category split) is left
    untouched since stripping it would leave an empty string. SingleMuon/
    DoubleMuon are further split onto two lines (still too long to fit
    otherwise, even after dropping the prefix)."""
    if name.startswith("Parking") and name != "Parking":
        short = name[len("Parking"):]
        if short in ("SingleMuon", "DoubleMuon"):
            short = short.replace("Muon", "\nMuon")
        return short
    return name


def lighten(color, amount=0.55):
    """Mix a color with white to get a visually distinct lighter tint of the
    same hue -- HLT/NGT get genuinely different colors (not just different
    linestyles), while curves from the same category stay in the same hue
    family."""
    c = np.array(mcolors.to_rgb(color))
    white = np.array([1.0, 1.0, 1.0])
    return tuple(c + (white - c) * amount)


# -----------------------------------------------------------------------------
# Classification 
# -----------------------------------------------------------------------------

def classify_stream(name):
    """Standard/Parking/Scouting/Calibration/Monitoring/Express split (extends
    cells 4/5's grouping by splitting the DQM-prefixed streams out into their own
    "Monitoring" category, separate from "Calibration" -- DQM streams like
    DQMOnlineScouting are not proportionally prescaled the same way as
    calibration data streams, so blending them together made the combined
    category's NGT/HLT ratio misleading)."""
    if name.startswith("Physics"):   return "Standard"
    if name.startswith("Parking"):   return "Parking"
    if name.startswith("Scouting"):  return "Scouting"
    if name.startswith("Express"):   return "Express"
    if name.startswith("DQM") and name != "DQMHistograms":
        return "Monitoring"
    if name.startswith(("ALCA", "Calibration")) or name.startswith("NanoDST"):
        return "Calibration"
    return None


def classify_main_only(name):
    """Same classification as classify_stream, but excludes Monitoring/Calibration/
    Express -- for a 'main categories only' view (Standard/Parking/Scouting),
    leaving out the smaller monitoring/calibration streams (including the DQM
    artifact, now labeled "Monitoring")."""
    cat = classify_stream(name)
    return cat if cat in ("Standard", "Parking", "Scouting") else None


def classify_no_monitoring_express(name):
    """Same classification as classify_stream, but excludes only Monitoring and
    Express (keeps Standard/Parking/Scouting/Calibration) -- isolates the DQM
    artifact (labeled "Monitoring") and the small Express category while still
    showing Calibration."""
    cat = classify_stream(name)
    return cat if cat not in ("Monitoring", "Express") else None


def group_of(stream):
    """Muon/EGamma/JetMET/Others dataset split (cells 6/7). First-match
    precedence: Muon > EGamma > JetMET > Others (same practical result as the
    notebook's independent membership tests, for standard CMS stream names)."""
    if "Muon" in stream:   return "Muon"
    if "EGamma" in stream: return "EGamma"
    if "JetMET" in stream: return "JetMET"
    return "Others"


def is_comparable_stream(stream):
    """Same filter as the notebook's rates_datasets / bandwidth_datasets cells."""
    return stream.startswith("Physics") and "HLTPhysics" not in stream and "ZeroBias" not in stream


def classify_dataset(name):
    return group_of(name) if is_comparable_stream(name) else None


def canonical_name(name):
    """Merge ParkingSingleMuonX -> ParkingSingleMuon etc (cell 8)."""
    for base in ("ParkingSingleMuon", "ParkingDoubleMuon", "ParkingVBF"):
        if name.startswith(base):
            return base
    return name


PARKING_ORDERED = ("ParkingLLP", "ParkingHH", "ParkingVBF", "ParkingDoubleMuon", "ParkingSingleMuon")


def classify_parking(name):
    if not name.startswith("Parking"):
        return None
    c = canonical_name(name)
    return c if c in PARKING_ORDERED else None  # NOTE: silently dropping e.g. ParkingAnomalyDetection


# -----------------------------------------------------------------------------
# Splitting
# -----------------------------------------------------------------------------

@dataclass
class Split:
    name: str                              # short id, e.g. "category"
    categories: List[str]                  # ordered category/group names
    colors: Dict[str, str]                 # category -> base color
    classify: Callable[[str], Optional[str]]
    quantities: List[str]                  # which of "rate"/"bandwidth" apply
    fname: Dict[str, str]                  # quantity -> output filename stem
    stream_word: str = "HLT Stream"        # for y-axis labels (comparison plots only)
    ylabel_text: Dict[str, str] = field(default_factory=dict)  # quantity -> exact Part-A ylabel
    legend_style: str = "dataset"          # "category" | "dataset" | "parking" -- which notebook cell's legend layout to replicate
    y_headroom: float = 1.8                # y-axis headroom multiplier above the stacked max
    label_fontsize: int = 18               # x/y axis label fontsize
    tick_labelsize: int = 14               # tick label fontsize
    fill_text_y: float = 0.65              # axes-fraction y-position of the FILL_TEXT annotation
    x_end_factor: float = 0.995            # Part-A x-axis end multiplier (time_sm[-1] * this), per notebook cell


SPLITS = [
    Split(
        name="category",
        categories=["Standard", "Parking", "Scouting", "Calibration", "Monitoring", "Express"],
        colors=dict(zip(
            ["Standard", "Parking", "Scouting", "Calibration", "Monitoring", "Express"],
            ["#3f90da", "#ffa90e", "#bd1f01", "#94a4a2", "#a96b59", "#832db6"],
        )),
        classify=classify_stream,
        quantities=["rate", "bandwidth"],
        fname={"rate": "rates", "bandwidth": "bandwidths"},
        stream_word="HLT Stream",
        ylabel_text={"rate": "HLT Stream Rate [kHz]", "bandwidth": "HLT Stream Bandwidth [GB/s]"},
        legend_style="category",
        y_headroom=1.6,
        label_fontsize=23,
        tick_labelsize=18,
        fill_text_y=0.622,
        x_end_factor=0.99,
    ),
    Split(
        name="dataset",
        categories=["Muon", "EGamma", "JetMET", "Others"],
        colors={"Others": "#999999", "Muon": "#0072B2", "EGamma": "#E69F00", "JetMET": "#009E73"},
        classify=classify_dataset,
        quantities=["rate", "bandwidth"],
        fname={"rate": "rates_datasets", "bandwidth": "bandwidths_datasets"},
        stream_word="HLT Stream",
        ylabel_text={"rate": "HLT Stream Rate [kHz]", "bandwidth": "HLT Stream Bandwidth [GB/s]"},
        legend_style="dataset",
        y_headroom=1.8,
        label_fontsize=23,
        tick_labelsize=18,
        fill_text_y=0.674,
    ),
    Split(
        name="parking",
        categories=list(PARKING_ORDERED),
        colors={
            "ParkingSingleMuon": "#377eb8",
            "ParkingDoubleMuon": "#4daf4a",
            "ParkingHH":         "#984ea3",
            "ParkingLLP":        "#ff7f00",
            "ParkingVBF":        "#e41a1c",
        },
        classify=classify_parking,
        quantities=["rate", "bandwidth"],
        fname={"rate": "rates_parking", "bandwidth": "bandwidths_parking"},
        stream_word="Parking Stream",
        ylabel_text={"rate": "Parking Stream Rate [kHz]", "bandwidth": "Parking Stream Bandwidth [GB/s]"},
        legend_style="parking",
        y_headroom=1.8,
        label_fontsize=25,
        tick_labelsize=19,
        fill_text_y=0.621,
    ),
    Split(
        name="category_main",
        categories=["Standard", "Parking", "Scouting"],
        colors={"Standard": "#3f90da", "Parking": "#ffa90e", "Scouting": "#bd1f01"},
        classify=classify_main_only,
        quantities=["rate", "bandwidth"],
        fname={"rate": "rates_main", "bandwidth": "bandwidths_main"},
        stream_word="HLT Stream",
        ylabel_text={"rate": "HLT Stream Rate [kHz]", "bandwidth": "HLT Stream Bandwidth [GB/s]"},
        legend_style="category",
        y_headroom=1.6,
        label_fontsize=23,
        tick_labelsize=18,
        fill_text_y=0.674,
        x_end_factor=0.99,
    ),
    Split(
        name="category_no_monitoring_express",
        categories=["Standard", "Parking", "Scouting", "Calibration"],
        colors={"Standard": "#3f90da", "Parking": "#ffa90e", "Scouting": "#bd1f01", "Calibration": "#94a4a2"},
        classify=classify_no_monitoring_express,
        quantities=["rate", "bandwidth"],
        fname={"rate": "rates_no_monitoring_express", "bandwidth": "bandwidths_no_monitoring_express"},
        stream_word="HLT Stream",
        ylabel_text={"rate": "HLT Stream Rate [kHz]", "bandwidth": "HLT Stream Bandwidth [GB/s]"},
        legend_style="category",
        y_headroom=1.6,
        label_fontsize=23,
        tick_labelsize=18,
        fill_text_y=0.674,
        x_end_factor=0.99,
    ),
]


# -----------------------------------------------------------------------------
# Load HLT (full) and NGT (partial) JSON
# -----------------------------------------------------------------------------

def load_run(path, run):
    with open(path) as fp:
        all_data = json.load(fp)
    run_data = all_data.get(run, {})
    if not run_data:
        raise RuntimeError(f"Run {run} not found in {path}")
    return run_data


def extract_meta_by_ls(run_data, ls_cut=LS_CUT):
    """{ ls -> metadata dict }, from the first entry seen for that LS across
    any stream (metadata is identical across streams for a given LS).
    Excludes the instance-specific fields (rate/size/bandwidth)."""
    meta_by_ls = {}
    for entries in run_data.values():
        for e in entries:
            ls = e["LS"]
            if ls <= ls_cut or ls in IGNORE_LSES:
                continue
            if ls not in meta_by_ls:
                meta_by_ls[ls] = {k: e[k] for k in METADATA_FIELDS if k in e}
    return meta_by_ls


def enrich_with_hlt_metadata(run_data, hlt_meta_by_ls):
    """Fill in missing per-LS metadata using the HLT's per-LS metadata,
    without touching rate/size/bandwidth (genuinely instance-specific)."""
    enriched = {}
    for stream, entries in run_data.items():
        new_entries = []
        for e in entries:
            e = dict(e)  # don't mutate the original
            meta = hlt_meta_by_ls.get(e["LS"])
            if meta:
                for k, v in meta.items():
                    e.setdefault(k, v)
            new_entries.append(e)
        enriched[stream] = new_entries
    return enriched


# -----------------------------------------------------------------------------
# Generic per-instance aggregation for a given split
# -----------------------------------------------------------------------------

def aggregate_instance(run_data, t0, classify, categories, prescale=1.0):
    """
    Returns a dict with:
        time_arr   : hours since t0
        rates      : {category -> [rate_kHz]}       (prescale-applied, for display)
        bws        : {category -> [bandwidth_GBs]}  (prescale-applied, for display)
        raw_rates  : {category -> [rate_Hz]}        (NOT prescaled, statistics only)
        lumi_arr   : delivered_lumi_per_lumisection
        l1_arr     : pre-deadtime L1 rate [kHz]
    all aligned to the same sorted-LS grid.
    """
    ls_time         = {}
    deliv_lumi      = {}
    l1rate_raw      = {}
    pre_deadtime_l1 = {}
    rate_by_cat     = {c: {} for c in categories}
    bw_by_cat       = {c: {} for c in categories}
    raw_rate_by_cat = {c: {} for c in categories}

    for stream, entries in run_data.items():
        cat = classify(stream)
        if cat is None:
            continue
        for e in entries:
            ls = e["LS"]
            if ls <= LS_CUT or ls in IGNORE_LSES:
                continue
            ts_str = e.get("start_time")
            if ts_str is None:
                continue

            if ls not in ls_time:
                ls_time[ls]    = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
                deliv_lumi[ls] = e.get("delivered_lumi_per_lumisection", 0.0)

            rate_by_cat[cat].setdefault(ls, 0.0)
            rate_by_cat[cat][ls] += (e["rate"] * prescale) / 1000.0
            bw_by_cat[cat].setdefault(ls, 0.0)
            bw_by_cat[cat][ls] += (e.get("bandwidth", 0.0) * prescale) / 1e9
            raw_rate_by_cat[cat].setdefault(ls, 0.0)
            raw_rate_by_cat[cat][ls] += e["rate"]

            if ls not in l1rate_raw and "hlt_rate_Status_OnGPU" in e:
                l1rate_raw[ls] = e["hlt_rate_Status_OnGPU"] / 1000.0
            if "deadtime" in e and ls in l1rate_raw:
                dt = e["deadtime"]
                pre_deadtime_l1[ls] = l1rate_raw[ls] / (1 - dt) if dt < 1 else l1rate_raw[ls]

    ls_sorted = sorted(ls_time)
    time_arr  = [(ls_time[ls] - t0).total_seconds() / 3600.0 for ls in ls_sorted]
    lumi_arr  = [deliv_lumi.get(ls, 0.0) for ls in ls_sorted]
    l1_arr    = [pre_deadtime_l1.get(ls, 0.0) for ls in ls_sorted]

    rates     = {c: [rate_by_cat[c].get(ls, 0.0)     for ls in ls_sorted] for c in categories}
    bws       = {c: [bw_by_cat[c].get(ls, 0.0)       for ls in ls_sorted] for c in categories}
    raw_rates = {c: [raw_rate_by_cat[c].get(ls, 0.0) for ls in ls_sorted] for c in categories}

    return dict(ls_sorted=ls_sorted, time_arr=time_arr, rates=rates, bws=bws,
                raw_rates=raw_rates, lumi_arr=lumi_arr, l1_arr=l1_arr)


def smoothed_category_series(agg, quantity, category):
    """
    Moving-average-smoothed (time, value, error) for one category/quantity, truncated to the common smoothed length.
    """
    values   = agg["rates"][category] if quantity == "rate" else agg["bws"][category]
    raw_rate = agg["raw_rates"][category]  # Hz, unprescaled -- for statistics only

    time_sm     = moving_average(agg["time_arr"])
    val_sm      = moving_average(values)
    raw_rate_sm = moving_average(raw_rate)

    L = min(len(time_sm), len(val_sm), len(raw_rate_sm))
    time_sm, val_sm, raw_rate_sm = time_sm[:L], val_sm[:L], raw_rate_sm[:L]

    n_eff = raw_rate_sm * (SMOOTH_WINDOW * LS_DURATION)
    with np.errstate(divide="ignore", invalid="ignore"):
        err_sm = np.where(n_eff > 0, val_sm / np.sqrt(n_eff), 0.0)

    return time_sm, val_sm, err_sm


def aligned_series(hlt_agg, ngt_agg, category, quantity):
    """(time, hlt_values, hlt_errors, ngt_values, ngt_errors) on their common smoothed time grid for one category/quantity, or None if there is not enough overlap."""
    t_hlt, v_hlt, e_hlt = smoothed_category_series(hlt_agg, quantity, category)
    t_ngt,  v_ngt,  e_ngt  = smoothed_category_series(ngt_agg,  quantity, category)

    common_t = sorted(set(np.round(t_hlt, 4)) & set(np.round(t_ngt, 4)))
    if len(common_t) < 2:
        return None

    hlt_val_map = {round(t, 4): v for t, v in zip(t_hlt, v_hlt)}
    hlt_err_map = {round(t, 4): e for t, e in zip(t_hlt, e_hlt)}
    ngt_val_map  = {round(t, 4): v for t, v in zip(t_ngt,  v_ngt)}
    ngt_err_map  = {round(t, 4): e for t, e in zip(t_ngt,  e_ngt)}

    time_c = np.array(common_t)
    hlt_c = np.array([hlt_val_map[t] for t in common_t])
    hlt_e = np.array([hlt_err_map[t] for t in common_t])
    ngt_c  = np.array([ngt_val_map[t]  for t in common_t])
    ngt_e  = np.array([ngt_err_map[t]  for t in common_t])
    return time_c, hlt_c, hlt_e, ngt_c, ngt_e


def ratio_and_error(hlt_c, hlt_e, ngt_c, ngt_e):
    """
    NGT/HLT ratio and its propagated statistical error
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(hlt_c > 0, ngt_c / hlt_c, np.nan)
        rel_hlt = np.where(hlt_c > 0, hlt_e / hlt_c, 0.0)
        rel_ngt  = np.where(ngt_c  > 0, ngt_e  / ngt_c,  0.0)
        ratio_err = ratio * np.sqrt(rel_hlt**2 + rel_ngt**2)
    return ratio, ratio_err


def align_twin_label(twin_ax, fig, top_margin=0.97, gap_px=12):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bbox = twin_ax.get_window_extent(renderer=renderer)
    tick_bboxes = [t.get_window_extent(renderer=renderer) for t in twin_ax.get_yticklabels() if t.get_text()]
    tick_right = max((b.x1 for b in tick_bboxes), default=ax_bbox.x1)
    label_bbox = twin_ax.yaxis.label.get_window_extent(renderer=renderer)
    height_axfrac = label_bbox.height / ax_bbox.height

    target_x0 = tick_right + gap_px
    x_axfrac = (target_x0 - ax_bbox.x0) / ax_bbox.width
    y_axfrac = top_margin - height_axfrac
    twin_ax.yaxis.set_label_coords(x_axfrac, y_axfrac)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    new_label_bbox = twin_ax.yaxis.label.get_window_extent(renderer=renderer)
    correction_px = target_x0 - new_label_bbox.x0
    twin_ax.yaxis.set_label_coords(x_axfrac + correction_px / ax_bbox.width, y_axfrac)


def add_lumi_l1t_reference(ax, agg, fig, show_labels=True, linewidth=1.5, alpha=0.85):
    lumi_sm = moving_average(agg["lumi_arr"])
    l1_sm   = moving_average(agg["l1_arr"])
    time_sm = moving_average(agg["time_arr"])
    L = min(len(lumi_sm), len(l1_sm), len(time_sm))
    lumi_sm, l1_sm, time_sm = lumi_sm[:L], l1_sm[:L], time_sm[:L]

    ax_lumi = ax.twinx()
    lum_handle, = ax_lumi.plot(time_sm, np.array(lumi_sm) * 100 / LS_DURATION, color="tab:red",
                                linestyle="--", linewidth=linewidth, alpha=alpha,
                                label="Delivered Luminosity")
    ax_lumi.set_ylim(0, 2.3)
    if show_labels:
        ax_lumi.set_ylabel("Inst. Luminosity [$10^{34}$ cm$^{-2}$s$^{-1}$]", color="tab:red",
                           fontsize=15, rotation=270, labelpad=12)
        ax_lumi.tick_params(labelcolor="tab:red", labelsize=14)
        align_twin_label(ax_lumi, fig)
    else:
        ax_lumi.set_yticks([])

    ax_l1t = ax.twinx()
    ax_l1t.spines["right"].set_position(("outward", 78 if show_labels else 0))
    l1_handle, = ax_l1t.plot(time_sm, l1_sm, color="tab:blue", linestyle="--", linewidth=linewidth,
                              alpha=alpha, label="Pre-Deadtime L1T Rate")
    ax_l1t.set_ylim(0, 110)
    if show_labels:
        ax_l1t.set_ylabel("L1T Rate [kHz]", color="tab:blue", fontsize=15, rotation=270, labelpad=12)
        ax_l1t.tick_params(labelcolor="tab:blue", labelsize=14)
        align_twin_label(ax_l1t, fig)
    else:
        ax_l1t.set_yticks([])

    return lum_handle, l1_handle


def center_ylabel_on_value(ax, value, fig):
    ymin, ymax = ax.get_ylim()
    target_frac = (value - ymin) / (ymax - ymin)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    label_bbox = ax.yaxis.label.get_window_extent(renderer=renderer)
    ax_bbox = ax.get_window_extent(renderer=renderer)
    x_axfrac = (label_bbox.x0 - ax_bbox.x0) / ax_bbox.width
    label_height_axfrac = label_bbox.height / ax_bbox.height
    anchor_frac = target_frac + label_height_axfrac / 2
    ax.yaxis.set_label_coords(x_axfrac, anchor_frac)


def cms_label(ax, fontsize=24):
    hep.cms.label(data=True, text="Preliminary", year=YEAR, lumi=LUMI_LABEL,
                  loc=0, ax=ax, com=CMS_ENERGY, fontsize=fontsize, pad=0.3)


# -----------------------------------------------------------------------------
# Standard per-instance stacked plot
# -----------------------------------------------------------------------------

def compute_stack_max(agg, quantity, split):
    values = {c: moving_average(agg["rates"][c] if quantity == "rate" else agg["bws"][c]) for c in split.categories}
    lens = [len(v) for v in values.values()]
    if not lens or min(lens) == 0:
        return None
    L = min(lens)
    cumul = np.zeros(L)
    for c in split.categories:
        cumul += values[c][:L]
    return float(cumul.max()) if L > 0 else None


def plot_stacked(agg, system_label, quantity, split, ylim_max=None, display_label=None):
    display_label = display_label if display_label is not None else system_label
    qinfo = QUANTITY_INFO[quantity]
    time_sm  = moving_average(agg["time_arr"])
    cats_sm  = {c: moving_average(agg["rates"][c] if quantity == "rate" else agg["bws"][c]) for c in split.categories}
    lumi_sm  = moving_average(agg["lumi_arr"])
    l1_sm    = moving_average(agg["l1_arr"])

    L = min(len(time_sm), len(lumi_sm), len(l1_sm), *(len(cats_sm[c]) for c in split.categories))
    if L == 0:
        print(f"  [skip] {split.name}/{system_label}/{quantity}: not enough LS to smooth")
        return
    time_sm = time_sm[:L]
    lumi_sm = lumi_sm[:L]
    l1_sm   = l1_sm[:L]
    for c in split.categories:
        cats_sm[c] = cats_sm[c][:L]

    plt.style.use(hep.style.CMS)
    fig, ax1 = plt.subplots(figsize=FIGSIZE)
    fig.subplots_adjust(left=0.30, right=0.78, top=0.88)  # exact notebook margins

    cumul, handles, labels = np.zeros(L), [], []
    for cat in split.categories:
        y = cats_sm[cat]
        h = ax1.fill_between(time_sm, cumul, cumul + y, step="mid", alpha=0.8,
                              color=split.colors[cat], label=cat)
        handles.append(h)
        labels.append(cat)
        cumul += y

    prescale_handle = None
    for ls in PRESCALE_LSES:
        if ls in agg["ls_sorted"]:
            i = agg["ls_sorted"].index(ls)
            j = max(0, i - (SMOOTH_WINDOW - 1))
            x = time_sm[j] if j < len(time_sm) else time_sm[-1]
            if prescale_handle is None:
                prescale_handle = ax1.axvline(x, color="black", linestyle="--", linewidth=2, label="Prescale Change")
            else:
                ax1.axvline(x, color="black", linestyle="--", linewidth=2)

    fs, ts = split.label_fontsize, split.tick_labelsize
    ax1.set_xlabel("Time [hh:mm]", fontsize=fs)
    ax1.set_ylabel(split.ylabel_text[quantity], fontsize=fs)
    ax1.set_xlim(0, time_sm[-1] * split.x_end_factor)
    y_top = ylim_max if ylim_max is not None else cumul.max() * split.y_headroom
    ax1.set_ylim(0, y_top)
    ax1.tick_params(labelsize=ts)
    ax1.xaxis.set_major_locator(MultipleLocator(1))
    ax1.xaxis.set_major_formatter(FuncFormatter(hhmm_fmt))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

    ax2 = ax1.twinx()
    lum_handle, = ax2.plot(time_sm, np.array(lumi_sm) * 100 / LS_DURATION, color="tab:red",
                           linestyle="--", linewidth=3, label="Delivered Luminosity")
    ax2.set_ylabel("Inst. Luminosity [$10^{34}$ cm$^{-2}$s$^{-1}$]", color="tab:red",
                   fontsize=fs, rotation=270, labelpad=12)
    ax2.tick_params(labelcolor="tab:red", labelsize=ts)
    ax2.set_ylim(0, 2.3)

    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("outward", 100))
    l1_handle, = ax3.plot(time_sm, l1_sm, color="tab:blue", linestyle="--", linewidth=3,
                          label="Pre-Deadtime L1T Rate")
    ax3.set_ylabel("L1T Rate [kHz]", color="tab:blue", fontsize=fs, rotation=270, labelpad=12)
    ax3.tick_params(labelcolor="tab:blue", labelsize=ts)
    ax3.set_ylim(0, 110)
    plt.tight_layout()
    fig.subplots_adjust(top=0.92)
    align_twin_label(ax2, fig)
    align_twin_label(ax3, fig)

    extra = [lum_handle, l1_handle] + ([prescale_handle] if prescale_handle else [])
    extra_names = ["Delivered Luminosity", "Pre-Deadtime L1T Rate"] + (["Prescale Change"] if prescale_handle else [])

    leg_y = 0.87

    leg_extra = ax1.legend(extra, extra_names, loc="upper left", bbox_to_anchor=(0.02, leg_y),
                           fontsize=20, frameon=False)
    ax1.add_artist(leg_extra)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bbox = ax1.get_window_extent(renderer=renderer)
    extra_bbox = leg_extra.get_window_extent(renderer=renderer)
    extra_right_axfrac = (extra_bbox.x1 - ax_bbox.x0) / ax_bbox.width

    main_kwargs = dict(loc="upper left", bbox_to_anchor=(extra_right_axfrac + 0.02, leg_y),
                       fontsize=20, frameon=False, ncol=2)
    leg_main = ax1.legend(handles, labels, **main_kwargs)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bbox   = ax1.get_window_extent(renderer=renderer)
    extra_bbox = leg_extra.get_window_extent(renderer=renderer)
    main_bbox  = leg_main.get_window_extent(renderer=renderer)
    combined_left  = min(extra_bbox.x0, main_bbox.x0)
    combined_right = max(extra_bbox.x1, main_bbox.x1)
    center_axfrac = ((combined_left + combined_right) / 2 - ax_bbox.x0) / ax_bbox.width

    ax1.text(center_axfrac, split.fill_text_y, f"{FILL_TEXT} ({display_label})", transform=ax1.transAxes,
              fontsize=21, verticalalignment="top", horizontalalignment="center")

    cms_label(ax1, fontsize=29)

    out_stem = f"{output_dir(quantity)}/{FILL_FIG}_{split.fname[quantity]}_{system_label}"
    for ext in ("png", "jpg", "pdf"):
        fig.savefig(f"{out_stem}.{ext}", dpi=1200)
    print(f"  Saved: {out_stem}.[png/jpg/pdf]")
    plt.close(fig)


# -----------------------------------------------------------------------------
# HLT vs NGT comparisons (merged)
# -----------------------------------------------------------------------------

def plot_comparison_merged(hlt_agg, ngt_agg, quantity, split):
    qinfo = QUANTITY_INFO[quantity]
    ngt_tints = {c: lighten(col) for c, col in split.colors.items()}

    series_by_cat = {}
    y_max = 0.0
    x_min, x_max = None, None
    for cat in split.categories:
        series = aligned_series(hlt_agg, ngt_agg, cat, quantity)
        if series is None:
            print(f"  [skip] {split.name}/{cat}/{quantity}: not enough overlapping time points")
            continue
        series_by_cat[cat] = series
        time_c, hlt_c, hlt_e, ngt_c, ngt_e = series
        y_max = max(y_max, (hlt_c + hlt_e).max(), (ngt_c + ngt_e).max())
        x_min = time_c[0]  if x_min is None else min(x_min, time_c[0])
        x_max = time_c[-1] if x_max is None else max(x_max, time_c[-1])

    if not series_by_cat:
        print(f"  [skip] {split.name}/{quantity}: no category had enough overlapping time points")
        return

    cats_with_data = list(series_by_cat.keys())
    n = len(cats_with_data)

    TOP_HEIGHT_IN, MINI_HEIGHT_IN = 8.0, 0.85
    fig_height_in = TOP_HEIGHT_IN + n * MINI_HEIGHT_IN

    plt.style.use(hep.style.CMS)
    fig, axes = plt.subplots(
        n + 1, 1, figsize=(FIGSIZE[0], fig_height_in), sharex=True,
        gridspec_kw={"height_ratios": [TOP_HEIGHT_IN] + [MINI_HEIGHT_IN] * n, "hspace": 0.12},
    )
    ax_top = axes[0]
    ratio_axes = axes[1:]

    handles, labels = [], []
    for cat in cats_with_data:
        time_c, hlt_c, hlt_e, ngt_c, ngt_e = series_by_cat[cat]
        ax_top.fill_between(time_c, hlt_c - hlt_e, hlt_c + hlt_e, step="mid",
                             color=split.colors[cat], alpha=0.25, linewidth=0)
        ax_top.fill_between(time_c, ngt_c - ngt_e, ngt_c + ngt_e, step="mid",
                             color=ngt_tints[cat], alpha=0.35, linewidth=0)
        h_hlt, = ax_top.step(time_c, hlt_c, where="mid", color=split.colors[cat],
                              linewidth=2.5, linestyle="-")
        h_ngt,  = ax_top.step(time_c, ngt_c,  where="mid", color=ngt_tints[cat],
                              linewidth=2.5, linestyle=NGT_DASH, dash_capstyle="round")
        handles += [h_hlt, h_ngt]
        labels  += [f"{cat} ({HLT_LABEL})", f"{cat} (NGT x{NGT_PRESCALE})"]

    ax_top.set_ylabel(f"{split.stream_word} {qinfo['ylabel_word']} [{qinfo['ylabel_unit']}]", fontsize=23)
    ax_top.set_ylim(0, y_max * 2.2)
    ax_top.tick_params(labelsize=18)

    lum_handle, l1_handle = add_lumi_l1t_reference(ax_top, hlt_agg, fig, show_labels=True)

    leg_extra = ax_top.legend([lum_handle, l1_handle], ["Delivered Luminosity", "Pre-Deadtime L1T Rate"],
                              loc="upper left", bbox_to_anchor=(0.02, 0.84), fontsize=17, frameon=False)
    ax_top.add_artist(leg_extra)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    ax_bbox = ax_top.get_window_extent(renderer=renderer)
    extra_bbox = leg_extra.get_window_extent(renderer=renderer)
    extra_right_axfrac = (extra_bbox.x1 - ax_bbox.x0) / ax_bbox.width

    ax_top.legend(handles, labels, loc="upper left",
                  bbox_to_anchor=(extra_right_axfrac + 0.02, 0.84), fontsize=17, frameon=False, ncol=2)

    cms_label(ax_top, fontsize=26)
    ax_top.text(0.02, 0.90, FILL_TEXT, transform=ax_top.transAxes,
                fontsize=18, verticalalignment="top")

    for cat, ax_r in zip(cats_with_data, ratio_axes):
        time_c, hlt_c, hlt_e, ngt_c, ngt_e = series_by_cat[cat]
        ratio, ratio_err = ratio_and_error(hlt_c, hlt_e, ngt_c, ngt_e)
        ax_r.fill_between(time_c, ratio - ratio_err, ratio + ratio_err, step="mid",
                           color=split.colors[cat], alpha=0.25, linewidth=0)
        ax_r.step(time_c, ratio, where="mid", color=split.colors[cat], linewidth=2.0,
                  linestyle=NGT_DASH, dash_capstyle="round")
        ax_r.axhline(1.0, color="black", linestyle="--", linewidth=1.0)
        ax_r.set_xlim(x_min, x_max)
        ax_r.set_ylim(*RATIO_YLIM[quantity])
        ax_r.yaxis.set_major_locator(MultipleLocator(0.2))
        ax_r.tick_params(labelsize=13)
        ax_r.text(1.004, 0.5, short_category_label(cat), transform=ax_r.transAxes, fontsize=12,
                   color=split.colors[cat], rotation=270, multialignment="center",
                   verticalalignment="center", horizontalalignment="left")

    ratio_axes[-1].set_xlabel("Time [hh:mm]", fontsize=22)
    ratio_axes[-1].xaxis.set_major_locator(MultipleLocator(1))
    ratio_axes[-1].xaxis.set_major_formatter(FuncFormatter(hhmm_fmt))
    plt.setp(ratio_axes[-1].get_xticklabels(), rotation=45, ha="right")

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig_w, fig_h = fig.get_size_inches() * fig.dpi
    top_box    = ratio_axes[0].get_window_extent(renderer=renderer)
    bottom_box = ratio_axes[-1].get_window_extent(renderer=renderer)
    label_x = min(ax.yaxis.label.get_window_extent(renderer=renderer).x0 for ax in ratio_axes) / fig_w - 0.01
    label_y = (top_box.y1 + bottom_box.y0) / 2 / fig_h
    fig.text(label_x, label_y, "NGT / HLT", rotation=90, fontsize=20,
             ha="center", va="center")

    out_stem = f"{output_dir(quantity)}/{FILL_FIG}_{split.fname[quantity]}_HLT_vs_NGT"
    for ext in ("png", "jpg", "pdf"):
        fig.savefig(f"{out_stem}.{ext}", dpi=300, bbox_inches="tight")
    print(f"  Saved: {out_stem}.[png/jpg/pdf]")
    plt.close(fig)


# -----------------------------------------------------------------------------
# HLT vs NGT comparisons (separate)
# -----------------------------------------------------------------------------

def plot_comparison_separate(hlt_agg, ngt_agg, quantity, split):
    qinfo = QUANTITY_INFO[quantity]

    for cat in split.categories:
        series = aligned_series(hlt_agg, ngt_agg, cat, quantity)
        if series is None:
            print(f"  [skip] {split.name}/{cat}/{quantity}: not enough overlapping time points")
            continue
        time_c, hlt_c, hlt_e, ngt_c, ngt_e = series
        color = split.colors[cat]
        ngt_color = lighten(color)

        plt.style.use(hep.style.CMS)
        fig, (ax_top, ax_bot) = plt.subplots(
            2, 1, figsize=FIGSIZE, sharex=True,
            gridspec_kw={"height_ratios": [3, 1], "hspace": 0.06},
        )

        ax_top.fill_between(time_c, hlt_c - hlt_e, hlt_c + hlt_e, step="mid",
                             color=color, alpha=0.25, linewidth=0)
        ax_top.fill_between(time_c, ngt_c - ngt_e, ngt_c + ngt_e, step="mid",
                             color=ngt_color, alpha=0.35, linewidth=0)
        ax_top.step(time_c, hlt_c, where="mid", color=color, linewidth=2.5,
                    linestyle="-", label=HLT_LABEL)
        ax_top.step(time_c, ngt_c,  where="mid", color=color, linewidth=2.5,
                    linestyle=NGT_DASH, dash_capstyle="round", label=f"{NGT_LABEL} (x{NGT_PRESCALE})")
        ax_top.set_ylabel(f"{split.stream_word} {qinfo['ylabel_word']} [{qinfo['ylabel_unit']}]", fontsize=23)
        y_hi = (hlt_c + hlt_e).max()
        y_hi = max(y_hi, (ngt_c + ngt_e).max())
        ax_top.set_ylim(0, y_hi * 1.35 if y_hi > 0 else 1.0)
        ax_top.tick_params(labelsize=18)

        hn_handles, hn_labels = ax_top.get_legend_handles_labels()
        lum_handle, l1_handle = add_lumi_l1t_reference(ax_top, hlt_agg, fig, show_labels=True)
        ax_top.legend(hn_handles + [lum_handle, l1_handle],
                      hn_labels + ["Delivered Luminosity", "Pre-Deadtime L1T Rate"],
                      loc="upper left", bbox_to_anchor=(0.02, 0.84), fontsize=22,
                      title=cat, title_fontsize=23, frameon=False)

        cms_label(ax_top, fontsize=26)
        ax_top.text(0.02, 0.90, FILL_TEXT, transform=ax_top.transAxes,
                    fontsize=18, verticalalignment="top")

        ratio, ratio_err = ratio_and_error(hlt_c, hlt_e, ngt_c, ngt_e)
        ax_bot.fill_between(time_c, ratio - ratio_err, ratio + ratio_err, step="mid",
                             color=color, alpha=0.25, linewidth=0)
        ax_bot.step(time_c, ratio, where="mid", color=color, linewidth=2.0,
                    linestyle=NGT_DASH, dash_capstyle="round")
        ax_bot.axhline(1.0, color="black", linestyle="--", linewidth=1.5)
        ax_bot.set_xlim(time_c[0], time_c[-1])
        ax_bot.set_ylim(*RATIO_YLIM[quantity])
        ax_bot.yaxis.set_major_locator(MultipleLocator(0.2))
        ax_bot.set_ylabel("NGT / HLT", fontsize=20)
        ax_bot.set_xlabel("Time [hh:mm]", fontsize=22)
        ax_bot.tick_params(labelsize=16)
        ax_bot.xaxis.set_major_locator(MultipleLocator(1))
        ax_bot.xaxis.set_major_formatter(FuncFormatter(hhmm_fmt))
        plt.setp(ax_bot.get_xticklabels(), rotation=45, ha="right")
        center_ylabel_on_value(ax_bot, 1.0, fig)

        out_stem = f"{output_dir(quantity)}/{FILL_FIG}_{split.fname[quantity]}_{safe_name(cat)}_HLT_vs_NGT"
        for ext in ("png", "jpg", "pdf"):
            fig.savefig(f"{out_stem}.{ext}", dpi=300, bbox_inches="tight")
        print(f"  Saved: {out_stem}.[png/jpg/pdf]")
        plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    print(f"HLT JSON: {HLT_JSON_PATH}")
    print(f"NGT JSON: {NGT_JSON_PATH}")

    hlt_run = load_run(HLT_JSON_PATH, RUN)
    ngt_run  = load_run(NGT_JSON_PATH,  RUN)

    hlt_meta_by_ls = extract_meta_by_ls(hlt_run)
    if not hlt_meta_by_ls:
        raise RuntimeError("No usable LS found in HLT JSON after LS_CUT.")
    t0 = min(datetime.strptime(m["start_time"], "%Y-%m-%dT%H:%M:%SZ")
              for m in hlt_meta_by_ls.values())

    print(f"Borrowing metadata ({', '.join(METADATA_FIELDS)}) from HLT onto NGT entries")
    ngt_run_enriched = enrich_with_hlt_metadata(ngt_run, hlt_meta_by_ls)

    print(f"Applying NGT Demonstrator prescale factor: x{NGT_PRESCALE}")

    for split in SPLITS:
        print(f"\n===== Split: {split.name} ({', '.join(split.categories)}) =====")
        hlt_agg = aggregate_instance(hlt_run, t0, split.classify, split.categories, prescale=1.0)
        ngt_agg = aggregate_instance(ngt_run_enriched, t0, split.classify, split.categories, prescale=NGT_PRESCALE)

        for quantity in split.quantities:
            print(f"\n=== Standard per-instance plots: {quantity}, {split.name}")
            hlt_max = compute_stack_max(hlt_agg, quantity, split)
            ngt_max  = compute_stack_max(ngt_agg,  quantity, split)
            shared_max = max(v for v in (hlt_max, ngt_max) if v is not None) if (hlt_max or ngt_max) else None
            shared_ylim = shared_max * split.y_headroom if shared_max is not None else None

            plot_stacked(hlt_agg, "HLT", quantity, split, ylim_max=shared_ylim)
            plot_stacked(ngt_agg,  "NGT", quantity, split, ylim_max=shared_ylim, display_label=f"NGT x{NGT_PRESCALE}")

            print(f"=== HLT-vs-NGT comparison (merged): {quantity}, {split.name}")
            plot_comparison_merged(hlt_agg, ngt_agg, quantity, split)

            print(f"=== HLT-vs-NGT comparison (separate): {quantity}, {split.name}")
            plot_comparison_separate(hlt_agg, ngt_agg, quantity, split)

    print(f"\nPlots written to: {DEFAULT_OUTDIR}/{FILL_FIG}")


if __name__ == "__main__":
    main()
