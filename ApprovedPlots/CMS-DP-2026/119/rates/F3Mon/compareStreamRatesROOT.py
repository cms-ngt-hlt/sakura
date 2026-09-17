#!/usr/bin/env python3
"""
Comparison plot of per-stream rate vs lumisection for Physics streams, one plot per stream, between two DAQ configurations. 

Usage:
    python3 compareStreamRatesROOT.py --run 398802 --ref cdaq2025 --comp ngtdemonstrator
    python3 compareStreamRatesROOT.py --run 398802 --ref cdaq2025 --comp hltteststand

Valid sources: cdaq2025 | ngtdemonstrator | hltteststand

Expects JSON files at:
    run<RUN>/streamRates_F3Mon_<SOURCE>_<RUN>.json

Saves PDF, PNG, and ROOT output to:
    /eos/user/m/mzarucki/www/2026/NGT/SAKURA/NERD/rates/F3Mon/run<RUN>/
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import ROOT

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_SOURCES = ("cdaq2025", "ngtdemonstrator", "hltteststand")

SOURCE_LABELS = {
    "cdaq2025":        "HLT Farm",
    "ngtdemonstrator": "NGT Demonstrator (x110)",
    "hltteststand":    "HLT Test Stand",
}

PRESCALE_FACTORS = {
    "ngtdemonstrator": 110,
    "hltteststand":    110,
}

DEFAULT_OUTDIR_TMPL = "/eos/user/m/mzarucki/www/2026/NGT/SAKURA/NERD/rates/F3Mon/run{run}"

REF_COLOR  = ROOT.kBlack
COMP_COLOR = 9

LS_DURATION = 23.31  # seconds per LS

# Display-only unit conversion
RATE_DISPLAY_SCALE = 1e-3
RATE_AXIS_LABEL = "Rate [kHz]"

# Smoothing
SMOOTH_WINDOW = 5

# CMS label info
YEAR       = 2025
LUMI_LABEL = 0.43  # 428.56 pb^-1 = 0.42856 fb^-1
CMS_ENERGY = 13.6

# ---------------------------------------------------------------------------
# TDR style
# ---------------------------------------------------------------------------

def set_tdr_style():
    s = ROOT.TStyle("tdrStyle", "Style for P-TDR")
    s.SetCanvasBorderMode(0)
    s.SetCanvasColor(ROOT.kWhite)
    s.SetCanvasDefH(600)
    s.SetCanvasDefW(600)
    s.SetCanvasDefX(0)
    s.SetCanvasDefY(0)
    s.SetPadBorderMode(0)
    s.SetPadColor(ROOT.kWhite)
    s.SetPadGridX(False)
    s.SetPadGridY(False)
    s.SetGridColor(0)
    s.SetGridStyle(3)
    s.SetGridWidth(1)
    s.SetFrameBorderMode(0)
    s.SetFrameBorderSize(1)
    s.SetFrameFillColor(0)
    s.SetFrameFillStyle(0)
    s.SetFrameLineColor(1)
    s.SetFrameLineStyle(1)
    s.SetFrameLineWidth(1)
    s.SetHistLineColor(1)
    s.SetHistLineStyle(0)
    s.SetHistLineWidth(1)
    s.SetEndErrorSize(2)
    s.SetMarkerStyle(20)
    s.SetOptFit(1)
    s.SetFitFormat("5.4g")
    s.SetFuncColor(2)
    s.SetFuncStyle(1)
    s.SetFuncWidth(1)
    s.SetOptDate(0)
    s.SetOptFile(0)
    s.SetOptStat(0)
    s.SetStatColor(ROOT.kWhite)
    s.SetStatFont(42)
    s.SetStatFontSize(0.025)
    s.SetStatTextColor(1)
    s.SetStatFormat("6.4g")
    s.SetStatBorderSize(1)
    s.SetStatH(0.1)
    s.SetStatW(0.15)
    s.SetOptTitle(0)
    s.SetTitleFont(42)
    s.SetTitleColor(1)
    s.SetTitleTextColor(1)
    s.SetTitleFillColor(10)
    s.SetTitleFontSize(0.05)
    s.SetPadTopMargin(0.05)
    s.SetPadBottomMargin(0.13)
    s.SetPadLeftMargin(0.16)
    s.SetPadRightMargin(0.02)
    s.SetTitleColor(1, "XYZ")
    s.SetTitleFont(42, "XYZ")
    s.SetTitleSize(0.06, "XYZ")
    s.SetTitleXOffset(0.9)
    s.SetTitleYOffset(1.25)
    s.SetLabelColor(1, "XYZ")
    s.SetLabelFont(42, "XYZ")
    s.SetLabelOffset(0.007, "XYZ")
    s.SetLabelSize(0.05, "XYZ")
    s.SetAxisColor(1, "XYZ")
    s.SetStripDecimals(True)
    s.SetTickLength(0.03, "XYZ")
    s.SetNdivisions(510, "XYZ")
    s.SetPadTickX(1)
    s.SetPadTickY(1)
    s.SetOptLogx(0)
    s.SetOptLogy(0)
    s.SetOptLogz(0)
    s.SetPaperSize(20., 20.)
    s.SetHatchesLineWidth(5)
    s.SetHatchesSpacing(0.05)
    s.SetLegendBorderSize(0)
    s.SetLegendFont(42)
    s.SetLegendFillColor(0)
    s.cd()
    ROOT.gROOT.ForceStyle()
    return s


def draw_cms_label(run, extra="Preliminary", year=YEAR, lumi=LUMI_LABEL, energy=CMS_ENERGY):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(11)
    latex.SetTextFont(61)
    latex.SetTextSize(0.055)
    latex.DrawLatex(0.16, 0.915, "CMS")
    if extra:
        latex.SetTextFont(52)
        latex.SetTextSize(0.042)
        latex.DrawLatex(0.255, 0.916, extra)
    latex.SetTextFont(42)
    latex.SetTextSize(0.042)
    latex.SetTextAlign(31)
    info_label = (
        f"{lumi:.1f} fb^{{-1}} ({year}, {energy:.1f} TeV), Run {run}"
    )
    latex.DrawLatex(0.96, 0.915, info_label)


# ---------------------------------------------------------------------------
# Smoothing helpers
# ---------------------------------------------------------------------------

def moving_average(data, window_size=SMOOTH_WINDOW):
    arr = np.array(data, dtype=float)
    if len(arr) < window_size:
        return np.array([])
    csum = np.cumsum(np.insert(arr, 0, 0.0))
    return (csum[window_size:] - csum[:-window_size]) / float(window_size)


def smooth_ls_data(ls_data, window_size=SMOOTH_WINDOW):
    """
    Apply the SMOOTH_WINDOW-wide moving average to a stream's per-LS data.

    ls_data: { ls -> (rate_scaled, rate_raw, duration) }

    rate_scaled and rate_raw are each smoothed independently over LS
    """
    if not ls_data:
        return {}

    pts           = sorted(ls_data.items())
    ls_arr        = [p[0]    for p in pts]
    scaled        = [p[1][0] for p in pts]
    raw           = [p[1][1] for p in pts]
    base_duration = pts[0][1][2]  # constant single-LS duration

    effective_duration = base_duration * window_size

    ls_sm     = moving_average(ls_arr, window_size)
    scaled_sm = moving_average(scaled, window_size)
    raw_sm    = moving_average(raw, window_size)

    if len(ls_sm) == 0:
        return {}

    smoothed = {}
    for ls_val, rate_sc, rate_rw in zip(ls_sm, scaled_sm, raw_sm):
        ls_key = int(round(ls_val))
        smoothed[ls_key] = (rate_sc, rate_rw, effective_duration)
    return smoothed


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def resolve_path(run, source):
    p = Path(f"run{run}") / f"streamRates_F3Mon_{source}_{run}.json"
    if not p.exists():
        sys.exit(f"ERROR: File not found: {p}")
    return p


def base_stream_name(name):
    stripped = re.sub(r"\d+$", "", name)
    return stripped if stripped else name


def load_physics_data(path, prescale=1.0):
    """
    Returns:
        { base_stream_name -> { ls -> (rate_scaled, rate_raw, duration) } }

    rate_raw    = measured rate [Hz] (used for error computation: N = rate_raw * T)
    rate_scaled = rate_raw * prescale (used as bin content for plotting)
    duration    = LS_DURATION [s]

    Physics* streams only; split-stream digit suffixes are merged by summing.
    """
    with open(path) as f:
        doc = json.load(f)

    raw_rates = defaultdict(lambda: defaultdict(float))

    for entry in doc["data"]:
        attr = entry["attributes"]
        if not attr["stream_name"].startswith("Physics"):
            continue
        base = base_stream_name(attr["stream_name"])
        ls   = attr["lumisection_number"]
        raw_rates[base][ls] += attr["rate"]

    result = {}
    for name, ls_map in raw_rates.items():
        result[name] = {
            ls: (float(r) * prescale, float(r), LS_DURATION)
            for ls, r in ls_map.items()
        }
    return result


# ---------------------------------------------------------------------------
# Histogram helpers
# ---------------------------------------------------------------------------

def make_hist(ls_data, color, name, marker=2, scale=1.0):
    """
    ls_data: { ls -> (rate_scaled [Hz], rate_raw [Hz], duration [s]) }

    Bin content = rate_scaled.
    Bin error   = prescale * sqrt(N_raw) / T   where N_raw = rate_raw * T.
    This correctly inflates errors for prescaled sources.

    `scale` is a display-only unit conversion (e.g. Hz -> kHz) applied to
    both content and error after the physics calculation above.
    """
    ROOT.TH1.AddDirectory(False)
    pts    = sorted(ls_data.items())
    ls_arr = [ls for ls, _ in pts]
    n      = len(pts)
    h = ROOT.TH1F(name, "", n, ls_arr[0] - 0.5, ls_arr[-1] + 0.5)
    h.Sumw2()
    for ls, (rate_scaled, rate_raw, dur) in pts:
        b        = h.FindBin(ls)
        n_raw    = rate_raw * dur
        prescale = (rate_scaled / rate_raw) if rate_raw > 0 else 1.0
        content  = rate_scaled * scale
        error    = (prescale * (n_raw ** 0.5) / dur if n_raw > 0 else 0.0) * scale
        h.SetBinContent(b, content)
        h.SetBinError(b, error)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(marker)
    h.SetMarkerSize(0.9)
    h.SetLineWidth(1)
    for i, ls in enumerate(ls_arr):
        h.GetXaxis().SetBinLabel(i + 1, str(ls))
    return h


def make_band_graph(h, color, alpha=0.35, name=None):
    """
    Convert a TH1 that already has correctly-computed bin content/error
    (e.g. from make_hist or make_ratio_hist) into a TGraphErrors and style
    it for drawing as a continuous, filled error *band* rather than a
    per-bin error bar/crossbar.

    Once bins are packed densely (as with SMOOTH_WINDOW smoothing over many
    LS), individual crossbars start to overlap and become unreadable; a
    band traces out the same +/-1 sigma statistical envelope but reads as
    one continuous shape, the way "Brazil plot" limit bands are drawn.

    Draw the returned graph with option "3" for the filled band, and again
    with option "L SAME" (same graph) to overlay a solid central-value line.
    """
    n = h.GetNbinsX()
    g = ROOT.TGraphErrors(n)
    if name:
        g.SetName(name)
    for i in range(1, n + 1):
        x  = h.GetBinCenter(i)
        y  = h.GetBinContent(i)
        ey = h.GetBinError(i)
        g.SetPoint(i - 1, x, y)
        g.SetPointError(i - 1, 0.0, ey)
    g.SetFillColorAlpha(color, alpha)
    g.SetFillStyle(1001)
    g.SetLineColor(color)
    g.SetLineWidth(2)
    g.SetMarkerSize(0)
    return g


def make_ratio_hist(ref_data, comp_data, color, name, marker=2):
    """
    ref_data / comp_data: { ls -> (rate_scaled, rate_raw, duration) }

    Builds h_ref and h_comp with correct prescale-aware errors,
    then divides with TH1::Divide(..., "B") for proper propagation.
    """
    ROOT.TH1.AddDirectory(False)
    common = sorted(set(ref_data) & set(comp_data))
    if not common:
        return None

    n  = len(common)
    lo = common[0]  - 0.5
    hi = common[-1] + 0.5

    h_ref  = ROOT.TH1F(name + "_ref",  "", n, lo, hi)
    h_comp = ROOT.TH1F(name + "_comp", "", n, lo, hi)
    h_ref.Sumw2()
    h_comp.Sumw2()

    for ls in common:
        r_sc, r_raw, t_r = ref_data[ls]
        c_sc, c_raw, t_c = comp_data[ls]
        ps_r = (r_sc / r_raw) if r_raw > 0 else 1.0
        ps_c = (c_sc / c_raw) if c_raw > 0 else 1.0
        b = h_ref.FindBin(ls)
        h_ref.SetBinContent(b, r_sc)
        h_ref.SetBinError(b, ps_r * (r_raw * t_r) ** 0.5 / t_r if r_raw > 0 else 0.0)
        h_comp.SetBinContent(b, c_sc)
        h_comp.SetBinError(b, ps_c * (c_raw * t_c) ** 0.5 / t_c if c_raw > 0 else 0.0)

    h_ratio = h_comp.Clone(name)
    h_ratio.Divide(h_comp, h_ref, 1, 1, "B")
    h_ratio.SetLineColor(color)
    h_ratio.SetMarkerColor(color)
    h_ratio.SetMarkerStyle(marker)
    h_ratio.SetMarkerSize(0.9)
    h_ratio.SetLineWidth(1)
    for i, ls in enumerate(common):
        h_ratio.GetXaxis().SetBinLabel(i + 1, str(ls))
    return h_ratio


# ---------------------------------------------------------------------------
# Per-stream plot
# ---------------------------------------------------------------------------

def make_stream_plot(stream, ref_ls, comp_ls, run,
                     ref_label, comp_label, outdir, stem_prefix):
    """
    ref_ls / comp_ls: { ls -> (rate_scaled, rate_raw, duration) }
    """

    # y range
    ref_rates  = [v[0] for v in ref_ls.values()]  if ref_ls  else []
    comp_rates = [v[0] for v in comp_ls.values()] if comp_ls else []
    all_rates  = ref_rates + comp_rates
    y_max      = float(max(all_rates)) * RATE_DISPLAY_SCALE if all_rates else 1.0

    # x range
    all_ls = sorted(set(ref_ls or {}) | set(comp_ls or {}))
    if not all_ls:
        return
    ls_min, ls_max = all_ls[0], all_ls[-1]
    x_lo = float(ls_min - 1)
    x_hi = float(ls_max + 1)

    # histograms
    hname   = stream.replace(" ", "_")
    h_ref   = make_hist(ref_ls,  REF_COLOR,  f"h_ref_{hname}",  marker=2, scale=RATE_DISPLAY_SCALE) if ref_ls  else None
    h_comp  = make_hist(comp_ls, COMP_COLOR, f"h_comp_{hname}", marker=2, scale=RATE_DISPLAY_SCALE) if comp_ls else None
    h_ratio = make_ratio_hist(ref_ls, comp_ls, COMP_COLOR, f"h_ratio_{hname}", marker=2) \
              if ref_ls and comp_ls else None

    # error bands
    g_ref   = make_band_graph(h_ref,   REF_COLOR,  name=f"g_ref_{hname}")   if h_ref   else None
    g_comp  = make_band_graph(h_comp,  COMP_COLOR, name=f"g_comp_{hname}")  if h_comp  else None
    g_ratio = make_band_graph(h_ratio, COMP_COLOR, name=f"g_ratio_{hname}") if h_ratio else None

    # canvas
    cname = f"c_{stream}"
    c = ROOT.TCanvas(cname, stream, 800, 800)

    split  = 0.30
    gap_hi = 0.03
    gap_lo = 0.05

    pad_up = ROOT.TPad(f"up_{stream}", "", 0, split, 1, 1)
    pad_up.SetTopMargin(0.10)
    pad_up.SetBottomMargin(gap_hi)
    pad_up.SetLeftMargin(0.16)
    pad_up.SetRightMargin(0.04)
    pad_up.SetFillStyle(4000)
    pad_up.Draw()

    pad_dn = ROOT.TPad(f"dn_{stream}", "", 0, 0, 1, split)
    pad_dn.SetTopMargin(gap_lo)
    pad_dn.SetBottomMargin(0.35)
    pad_dn.SetLeftMargin(0.16)
    pad_dn.SetRightMargin(0.04)
    pad_dn.SetFillStyle(4000)
    pad_dn.Draw()

    # upper pad
    pad_up.cd()

    frame_up = pad_up.DrawFrame(x_lo, 0, x_hi, y_max * 1.65)
    frame_up.GetYaxis().SetTitle(RATE_AXIS_LABEL)
    frame_up.GetYaxis().SetTitleSize(0.07)
    frame_up.GetYaxis().SetTitleOffset(1)
    frame_up.GetYaxis().SetLabelSize(0.06)
    frame_up.GetXaxis().SetLabelSize(0)
    frame_up.GetXaxis().SetTickLength(0.04)

    if g_ref:
        g_ref.Draw("3 SAME")   # filled +/-1 sigma band
        g_ref.Draw("LX SAME")   # central-value line on top
    if g_comp:
        g_comp.Draw("3 SAME")
        g_comp.Draw("LX SAME")

    display_stream = re.sub(r"^Physics", "", re.sub(r"Stream$", "", stream))
    leg = ROOT.TLegend(0.42, 0.62, 0.94, 0.88)
    leg.SetTextSize(0.053)
    leg.SetHeader(display_stream, "C")
    if g_ref:
        leg.AddEntry(g_ref,  ref_label,  "lf")
    if g_comp:
        leg.AddEntry(g_comp, comp_label, "lf")
    leg.Draw()

    draw_cms_label(run)
    pad_up.RedrawAxis()

    # lower pad
    pad_dn.cd()

    scale = (1.0 - split) / split

    frame_dn = pad_dn.DrawFrame(x_lo, 0.8, x_hi, 1.3)
    frame_dn.GetYaxis().SetTitle("NGT/HLT")
    frame_dn.GetYaxis().CenterTitle(True)
    frame_dn.GetYaxis().SetNdivisions(504)
    frame_dn.GetYaxis().SetTitleSize(0.07 * scale)
    frame_dn.GetYaxis().SetTitleOffset(1.0 / scale)
    frame_dn.GetYaxis().SetLabelSize(0.06 * scale)
    frame_dn.GetXaxis().SetTitle("LS")
    frame_dn.GetXaxis().SetTitleSize(0.07 * scale)
    frame_dn.GetXaxis().SetTitleOffset(0.95)
    frame_dn.GetXaxis().SetLabelSize(0.06 * scale)
    frame_dn.GetXaxis().SetTickLength(0.04 * scale)

    ref_line = ROOT.TLine(x_lo, 1, x_hi, 1)
    ref_line.SetLineColor(ROOT.kBlack)
    ref_line.SetLineStyle(2)
    ref_line.SetLineWidth(1)
    ref_line.Draw("SAME")

    if g_ratio:
        g_ratio.Draw("3 SAME")
        g_ratio.Draw("L SAME")

    pad_dn.RedrawAxis()

    # save
    c.cd()
    stem = outdir / f"{stem_prefix}_{stream}"
    for ext in ("pdf", "png", "root"):
        c.SaveAs(f"{stem}.{ext}")
    print(f"  Saved: {stem}.[pdf/png/root]")
    c.Close()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="CMS stream-rate comparison plots (Physics streams, one per stream)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Valid sources: {' | '.join(VALID_SOURCES)}",
    )
    parser.add_argument("--run",    required=True, help="Run number (e.g. 398802)")
    parser.add_argument("--ref",    required=True, choices=VALID_SOURCES)
    parser.add_argument("--comp",   required=True, choices=VALID_SOURCES)
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    if args.ref == args.comp:
        sys.exit("ERROR: --ref and --comp must be different sources.")

    outdir = Path(args.outdir) if args.outdir else \
             Path(DEFAULT_OUTDIR_TMPL.format(run=args.run))
    outdir.mkdir(parents=True, exist_ok=True)

    ref_path  = resolve_path(args.run, args.ref)
    comp_path = resolve_path(args.run, args.comp)
    print(f"Reference : {ref_path}")
    print(f"Comparison: {comp_path}")

    ref_ps  = PRESCALE_FACTORS.get(args.ref,  1)
    comp_ps = PRESCALE_FACTORS.get(args.comp, 1)
    if ref_ps  != 1: print(f"Applying prescale x{ref_ps}  to {args.ref}")
    if comp_ps != 1: print(f"Applying prescale x{comp_ps} to {args.comp}")

    ref_data_raw  = load_physics_data(ref_path,  prescale=ref_ps)
    comp_data_raw = load_physics_data(comp_path, prescale=comp_ps)

    # Apply the same SMOOTH_WINDOW moving-average smoothing
    print(f"Applying moving-average smoothing (window={SMOOTH_WINDOW} LS)")
    ref_data  = {s: smooth_ls_data(d) for s, d in ref_data_raw.items()}
    comp_data = {s: smooth_ls_data(d) for s, d in comp_data_raw.items()}

    all_streams = sorted(set(ref_data) | set(comp_data))
    if not all_streams:
        sys.exit("ERROR: No Physics streams found - check the input files.")

    print(f"\nFound {len(all_streams)} Physics stream(s):")
    for s in all_streams:
        print(f"  {s}")
    print()

    ROOT.gROOT.SetBatch(True)
    style = set_tdr_style()

    ref_label   = SOURCE_LABELS[args.ref]
    comp_label  = SOURCE_LABELS[args.comp]
    stem_prefix = f"run{args.run}_{args.comp}_vs_{args.ref}"

    for stream in all_streams:
        make_stream_plot(
            stream      = stream,
            ref_ls      = ref_data .get(stream, {}),
            comp_ls     = comp_data.get(stream, {}),
            run         = args.run,
            ref_label   = ref_label,
            comp_label  = comp_label,
            outdir      = outdir,
            stem_prefix = stem_prefix,
        )

    print(f"\nDone. {len(all_streams)} plot(s) written to: {outdir}")


if __name__ == "__main__":
    main()
