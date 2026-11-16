#!/usr/bin/env python3
"""CMS-style trend plots of the scouting PV-track impact-parameter profiles, HLT / Prompt / NGT conditions overlaid.

Needs results/ip_summary.csv and results/quality.csv (extract_ip.py).
Runs with tracking problems are removed from all three series (so the comparison is on the same runs):
  * EXCLUDE-TRACKING in the online NGTDemonstrator scan (--exclusion, run_exclusion.csv)
  * any condition set whose mean number of layers per track differs by > LAYER_DIFF from the median of the
    three (strip modules masked by that condition set), or is below LAYER_MIN (strips off)
  * fewer than MIN_EVENTS events, or a condition set missing
Run start times come from the online scan (--metrics, metrics.csv); runs without one are placed by
interpolating in run number. On the luminosity axis each run sits at the middle of its slice of recorded
luminosity (brilcalc file --lumifile, lumi_data.csv), accumulated over the selected runs only, from 0.

Usage: plot_trends.py [-i results] [-o plots] [--label Preliminary] [--xaxis time|run|lumi|both|all]
                      [--lumi X|auto]   (auto: recorded luminosity of the selected runs, from --lumifile)
Writes plots/<xaxis>/<profile>_{average,spread}.{png,pdf}, plots/<xaxis>/dxyVsPhi_pt*_{dx,dy}.{png,pdf},
plots/overview_<xaxis>.png and results/excluded_runs.csv, results/runs_used.txt
"""
import argparse
import csv
import os
from datetime import datetime, timezone

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(HERE, "data")  # run_exclusion.csv, metrics.csv of the online NGTDemonstrator DQM scan
VARIANTS = ("HLT", "Prompt", "NGT")
STYLE = {  # CMS-recommended (Petroff) colours
    "HLT": dict(color="#5790fc", marker="s", ms=6, label="HLT conditions"),
    "Prompt": dict(color="#f89c20", marker="^", ms=7, label="Prompt conditions"),
    "NGT": dict(color="#e42536", marker="o", ms=6, label="NGT conditions"),
}
LAYER_DIFF = 0.3
LAYER_MIN = 6.0
MIN_EVENTS = 5000
VAR_TEX = {"dxy": r"d_{xy}", "dz": r"d_{z}"}
X_TEX = {"Eta": r"\eta", "Phi": r"\phi"}


def selection(q, exclusion):
    """Return (runs used, list of excluded (run, reason))."""
    bad = {}
    sample = set(q.run)
    if os.path.exists(exclusion):
        for r in csv.DictReader(open(exclusion)):
            if r["recommendation"] == "EXCLUDE-TRACKING" and int(r["run"]) in sample:
                bad.setdefault(int(r["run"]), f"online scan: {r['issue']}")
    used = []
    for run, g in q.groupby("run"):
        g = g.set_index("variant")
        if run in bad:
            continue
        if set(g.index) != set(VARIANTS) or g.events.isna().any():
            bad[run] = "condition set missing"
            continue
        if g.events.min() < MIN_EVENTS:
            bad[run] = f"low statistics ({int(g.events.min())} events)"
            continue
        lay = g.layers
        dev = (lay - lay.median()).abs()
        if lay.min() < LAYER_MIN or dev.max() > LAYER_DIFF:
            v = dev.idxmax()
            bad[run] = f"{v} conditions: {lay[v]:.2f} layers/track vs {lay.median():.2f} (strip modules masked)"
            continue
        used.append(run)
    return used, sorted(bad.items())


def run_times(runs, metrics):
    m = pd.read_csv(metrics).set_index("run")["run_start"] if os.path.exists(metrics) else pd.Series(dtype=float)
    known = m[(m > 0) & m.notna()]
    t, est = {}, {}
    for r in runs:
        ok = r in known.index
        t[r] = known[r] if ok else np.interp(r, known.index.values, known.values)
        est[r] = not ok
    return {r: datetime.fromtimestamp(v, timezone.utc) for r, v in t.items()}, est


def run_lumis(path):
    """brilcalc csv (run:fill,time,nls,ncms,delivered(/pb),recorded(/pb)) -> {run: (cumulative start, recorded)}
    in fb^-1, cumulative over all runs of the file in run order."""
    rec = {}
    with open(path) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            cols = line.strip().split(",")
            rec[int(cols[0].split(":")[0])] = float(cols[5]) / 1000.
    out, cum = {}, 0.
    for r in sorted(rec):
        out[r] = (cum, rec[r])
        cum += rec[r]
    return out


def lumi_axis(runs, lumis):
    """x position of each run: middle of its slice of recorded luminosity, accumulated over the selected
    runs only (in run order), so that the axis goes from 0 to their total. NaN if unknown."""
    out, cum = {}, 0.
    for r in sorted(runs):
        if r not in lumis:
            out[r] = np.nan
            continue
        out[r] = cum + 0.5 * lumis[r][1]
        cum += lumis[r][1]
    return out


LUMI_LABEL = r"Cumulative integrated luminosity [fb$^{-1}$]"
# first runs of the 2026 IOVs of the TrackerAlignmentRcd tag used at HLT
HLT_ALIGNMENT_IOVS = (400847, 401674, 402250, 403333, 403732, 404612)


def iov_lines(runs, lumis, iovs=HLT_ALIGNMENT_IOVS):
    """[(x, iov)] on the luminosity axis of lumi_axis(runs, lumis): each IOV inside the run range is placed
    at the start of the first selected run it covers (= the end of the last selected run before it)."""
    xs, out = lumi_axis(runs, lumis), []
    for iov in iovs:
        after = [r for r in sorted(runs) if r >= iov and np.isfinite(xs[r])]
        if after and min(runs) < iov:
            out.append((xs[after[0]] - 0.5 * lumis[after[0]][1], iov))
    return out


def cms_axes(label):
    fig, ax = plt.subplots(figsize=(12, 7))
    cms_label(ax, label)
    return fig, ax


def finish(fig, ax, xaxis, path):
    if xaxis == "time":
        lo, hi = ax.get_xlim()
        weeks = 1 if hi - lo < 45 else 2 if hi - lo < 130 else 4  # keep the date labels readable
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=weeks))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.set_xlabel("Date (2026)")
    elif xaxis == "lumi":
        ax.set_xlim(0, 1.03 * ax.get_xlim()[1])
        ax.set_xlabel(LUMI_LABEL)
    else:
        ax.set_xlabel("Run number")
        ax.ticklabel_format(axis="x", style="plain", useOffset=False)
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.35 * (hi - lo))  # room for label, legend and selection text
    ax.legend(loc="upper right", ncol=3, fontsize=16, frameon=False, handletextpad=0.3, columnspacing=1.0)
    fig.savefig(path + ".png", dpi=200, bbox_inches="tight")
    fig.savefig(path + ".pdf", bbox_inches="tight")
    plt.close(fig)


def series(p, runs, xs, profile, col, err=None):
    out = {}
    for v in VARIANTS:
        s = p[(p.variant == v) & (p.profile == profile) & p.run.isin(runs)].set_index("run").reindex(runs)
        out[v] = (np.array([xs[r] for r in runs]), s[col].values, None if err is None else s[err].values)
    return out


def draw(ax, data):
    for v in VARIANTS:
        x, y, e = data[v]
        st = STYLE[v]
        ax.errorbar(x, y, yerr=e, fmt=st["marker"], ms=st["ms"], color=st["color"], mfc=st["color"],
                    mec="black" if v == "NGT" else st["color"], mew=0.5, elinewidth=1, capsize=0,
                    alpha=0.9, label=st["label"], zorder=3 if v == "NGT" else 2)


def text(ax, s):
    ax.text(0.02, 0.80, s, transform=ax.transAxes, fontsize=16, va="top")


# ---------------------------------------------------------------- IP trend plots (Zee-comparison style)
# Same look as the Z->ee comparison script: 10x10 figure, main panel + comparison panel (3:1),
# HLT blue circles / NGT orange diamonds / Prompt black triangles, Prompt as reference with a grey
# statistical band. Spreads are compared as ratios to Prompt; averages and offsets (which cross zero)
# as differences to Prompt.
STYLE_IP = {
    "HLT": dict(color="#5790fc", marker="o"),
    "NGT": dict(color="#f89c20", marker="D"),
    "Prompt": dict(color="black", marker="v"),
}
ORDER_IP = ("HLT", "NGT", "Prompt")
LEGEND_ORDER_IP = ("Prompt", "HLT", "NGT")
LEGEND_TITLE = "HLT Scouting"
REF = "Prompt"


AXIS_FS, RATIO_FS, TICK_FS = 26, 20, 24  # axis titles, bottom-panel y titles, tick labels


def square_frame(fig, left=1.9, right=0.6, bottom=1.4):
    """Place the panels (one, or stacked with a shared x axis) so that together they fill a square frame;
    margins in inches, room for the axis titles, the lumi label goes above."""
    fw, fh = fig.get_size_inches()
    side = fw - left - right
    fig.subplots_adjust(left=left / fw, right=1 - right / fw, bottom=bottom / fh, top=(bottom + side) / fh)


LABEL_YEAR = None  # e.g. "2026": shown in the luminosity label, "1.76 fb^-1, 2026 (13.6 TeV)"


def cms_label(ax, label, lumi=None, fontsize=22):
    """CMS figure guidelines: "CMS" in-frame upper left, "Preliminary" below it,
    luminosity and energy out of frame upper right in the compact form "1.76 fb^-1 (13.6 TeV)"."""
    rlabel = (f"{lumi} fb$^{{-1}}$" + ("," if LABEL_YEAR else "") + " " if lumi else "") + (
        f"{LABEL_YEAR} " if LABEL_YEAR else "") + "(13.6 TeV)"
    square_frame(ax.figure)
    for a in ax.figure.axes:  # every panel of the figure, created before the label
        a.tick_params(axis="both", which="major", labelsize=TICK_FS)
    ax._cms_texts = [t for t in hep.cms.label(ax=ax, data=True, text=label, rlabel=rlabel, fontsize=fontsize,
                                              loc=2) if t is not None]


def below_label(ax, pad=0.035):
    """Axes y just below the in-frame CMS / Preliminary label, to anchor (va="top") the selection text."""
    ax.figure.canvas.draw()
    to_ax = ax.transAxes.inverted()
    inframe = [t.get_window_extent().transformed(to_ax) for t in getattr(ax, "_cms_texts", [])]
    inframe = [b for b in inframe if b.y1 <= 1.0]
    return min(b.y0 for b in inframe) - pad if inframe else 0.80


def styled_axes(label, lumi):
    fig, (ax, axr) = plt.subplots(2, 1, figsize=(10, 10), sharex=True,
                                  gridspec_kw={"height_ratios": [3, 1], "hspace": 0.05})
    cms_label(ax, label, lumi)
    return fig, ax, axr


def abs_ratio(y, e, yr, er):
    """|y| / |y_ref| and its uncertainty, for quantities whose ideal value is 0."""
    r = np.divide(np.abs(y), np.abs(yr), out=np.full_like(y, np.nan, dtype=float), where=yr != 0)
    re_ = r * np.sqrt(np.divide(e, y, out=np.zeros_like(y, dtype=float), where=y != 0) ** 2
                      + np.divide(er, yr, out=np.zeros_like(yr, dtype=float), where=yr != 0) ** 2)
    return r, re_


def abs_ratio_range(axr, vals):
    """Log axis symmetric around 1, from the values, between x2 and x20."""
    v = np.concatenate([np.asarray(x, float) for x in vals]) if vals else np.array([])
    v = v[np.isfinite(v) & (v > 0)]
    m = np.max(np.abs(np.log10(v))) + 0.15 if v.size else 0.0
    m = min(max(m, np.log10(2)), np.log10(20))
    axr.set_yscale("log")
    axr.set_ylim(10 ** -m, 10 ** m)
    axr.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
    axr.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())


def save_square(fig, path):
    """Save cropped to the content with the same small pad on all four sides (the frame stays square,
    the canvas follows the width of the axis titles)."""
    for ext in ("png", "pdf"):
        fig.savefig(f"{path}.{ext}", bbox_inches="tight", pad_inches=0.3)


def drop_bottom(fig, ax, axr):
    """Remove the bottom panel and let the main one fill its space, with the x axis it had."""
    top, bot = ax.get_position(), axr.get_position()
    xlabel = axr.get_xlabel()
    fig.delaxes(axr)
    ax.set_position([top.x0, bot.y0, top.width, top.y1 - bot.y0])
    ax.tick_params(axis="x", which="both", labelbottom=True)
    ax.set_xlabel(xlabel, fontsize=AXIS_FS)


def _xnum(x):
    """x values as numbers (matplotlib dates for datetimes), for bar widths."""
    x = np.asarray(x)
    return mdates.date2num(list(x)) if x.size and hasattr(x[0], "tzinfo") else x.astype(float)


def styled_plot(data, mode, ylab, sel, xaxis, label, lumi, path, zero_line=False, unit=r"$\mu$m", min_span=None,
                variants=ORDER_IP, ref=REF, absratio=False, absdiff=False,
                center0=False, square=False, ymin0=False, vlines=None, robust_y=False, drop_err=None):
    """data[v] = (x, y, yerr[, xerr]) (xerr: horizontal bars, e.g. the span of grouped runs);
    mode = 'ratio' or 'diff' for the bottom panel (w.r.t. Prompt);
    unit = unit of the difference panel; min_span = minimum half-range of the bottom panel;
    vlines = [(x, run)]: dashed vertical lines (e.g. HLT alignment updates, iov_lines), labelled with the run;
    robust_y: y range from the points with an error <= 3x the median one, so that a few poorly measured
    points do not flatten the bulk (their error bars are then cut at the frame);
    drop_err: a run is not drawn if, in any drawn variant, its error is above drop_err x the median error."""
    if drop_err:
        es = np.array([np.asarray(data[v][2], float) for v in variants])
        keep = np.all(~(es > drop_err * np.nanmedian(es)), axis=0)
        data = {v: tuple(np.asarray(a)[keep] for a in data[v][:3]) for v in data}
        print(f"  {os.path.basename(path)}: {np.sum(~keep)} of {keep.size} points with a large error not drawn")
    fig, ax, axr = styled_axes(label, lumi)
    for v in variants:
        x, y, e = data[v][:3]
        st = STYLE_IP[v]
        ax.errorbar(x, y, yerr=e, xerr=data[v][3] if len(data[v]) > 3 else None, fmt=st["marker"], ms=10,
                    color=st["color"], ecolor=st["color"],
                    elinewidth=1.5, capsize=0, linewidth=0, label=f"{v} Conditions",
                    zorder=3 if v == ref else 2)
    if zero_line:
        ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_ylabel(ylab, fontsize=AXIS_FS)
    if robust_y:
        ys, es = (np.concatenate([np.asarray(data[v][i], float) for v in variants]) for i in (1, 2))
        ok = np.isfinite(ys) & np.isfinite(es)
        ok &= es <= 3 * np.median(es[ok])
        lo_, hi_ = np.min((ys - es)[ok]), np.max((ys + es)[ok])
        pad = 0.05 * (hi_ - lo_)
        ax.set_ylim(lo_ - pad, hi_ + pad)
    if ymin0:  # positive-definite quantity (an RMS): y axis from 0
        ax.set_ylim(0, ax.get_ylim()[1])
    lo, hi = ax.get_ylim()
    ax.set_ylim(lo, hi + 0.55 * (hi - lo))  # room for CMS label, legend and selection text
    # legend as in the dilepton plots: bold title, reference first, no frame
    handles, names = ax.get_legend_handles_labels()
    order = [names.index(f"{v} Conditions") for v in LEGEND_ORDER_IP if v in variants]
    leg = ax.legend([handles[i] for i in order], [names[i] for i in order], title=LEGEND_TITLE,
                    title_fontproperties={"weight": "bold", "size": 18}, fontsize=18, loc="upper right",
                    frameon=False)
    txt = ax.text(0.03, below_label(ax), sel, transform=ax.transAxes, fontsize=15, va="top")
    # a long selection text that runs into the legend goes below it, with more headroom above the data
    fig.canvas.draw()
    to_ax = ax.transAxes.inverted()
    lb = leg.get_window_extent().transformed(to_ax)
    tb = txt.get_window_extent().transformed(to_ax)
    if tb.x1 > lb.x0 and tb.y0 < lb.y1 and tb.y1 > lb.y0:
        txt.set_y(lb.y0 - 0.02)
        bottom = lb.y0 - 0.02 - tb.height
        top = lo + (hi - lo) / (bottom - 0.03)  # data (up to the old hi) below the text
        ax.set_ylim(lo, max(top, ax.get_ylim()[1]))

    # ---- comparison panel w.r.t. Prompt (ref=None: every variant w.r.t. 0) ----
    xr, yr, er = data[ref if ref is not None else variants[0]][:3]
    er = np.zeros_like(yr) if er is None else np.nan_to_num(er)
    xn = _xnum(xr)
    x_lo = 0.0 if xaxis == "lumi" else np.nanmin(xn)  # luminosity axis starts at 0
    width = 0.012 * (np.nanmax(xn) - x_lo) if len(xn) > 1 else 1.0
    if ref is None:
        mode, yr, er = "diff", np.zeros_like(yr), np.zeros_like(er)
        axr.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(r"$\Delta$ w.r.t. 0" + (f" [{unit}]" if unit else ""), fontsize=RATIO_FS)
    elif absratio:  # distance from the ideal value 0, relative to the reference
        axr.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(f"|value| / |{ref}|", fontsize=RATIO_FS)
    elif absdiff:  # distance from the ideal value 0, minus the reference one
        mode = "diff"
        axr.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(f"|value| − |{ref}|" + (f" [{unit}]" if unit else ""), fontsize=RATIO_FS)
    elif mode == "ratio":
        rel = np.divide(er, yr, out=np.zeros_like(yr), where=yr > 0)
        axr.bar(xn, 2 * rel, bottom=1 - rel, width=width, color="gray", alpha=0.3, label=f"Stat. unc. ({ref})")
        axr.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(f"Ratio w.r.t. {ref}", fontsize=AXIS_FS)
    else:
        axr.bar(xn, 2 * er, bottom=-er, width=width, color="gray", alpha=0.3, label=f"Stat. unc. ({ref})")
        axr.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(r"$\Delta$ w.r.t. " + ref + (f" [{unit}]" if unit else ""), fontsize=RATIO_FS)
    vals = []
    for v in variants:
        if v == ref:
            continue
        x, y, e = data[v][:3]
        e = np.zeros_like(y) if e is None else np.nan_to_num(e)
        if absratio:
            r, re_ = abs_ratio(y, e, yr, er)
        elif absdiff:
            r, re_ = np.abs(y) - np.abs(yr), np.sqrt(e ** 2 + er ** 2)
        elif mode == "ratio":
            r = np.divide(y, yr, out=np.full_like(y, np.nan), where=yr > 0)
            # sigma_R = R * sqrt((e/y)^2 + (e_ref/y_ref)^2)
            re_ = np.abs(r) * np.sqrt(np.divide(e, y, out=np.zeros_like(y), where=y != 0) ** 2
                              + np.divide(er, yr, out=np.zeros_like(yr), where=yr > 0) ** 2)
        else:
            r, re_ = y - yr, np.sqrt(e ** 2 + er ** 2)
        axr.errorbar(_xnum(x), r, yerr=re_, fmt="_", ms=12, mew=2, color=STYLE_IP[v]["color"], elinewidth=1.5,
                     capsize=0, linewidth=0,
                     label=f"|{v}| / |{ref}|" if absratio else f"|{v}| − |{ref}|" if absdiff else None)
        vals.append(r)
    # symmetric range around the reference, with some padding
    allv = np.concatenate([np.asarray(v, float) for v in vals]) if vals else np.array([])
    allv = allv[np.isfinite(allv)]
    c0 = 1.0 if mode == "ratio" else 0.0
    floor = min_span if min_span is not None else (0.2 if mode == "ratio" else 0.5)
    span = max(np.max(np.abs(allv - c0)) * 1.3 if allv.size else 0, floor)
    axr.set_ylim(c0 - span, c0 + span)
    if absratio:
        abs_ratio_range(axr, vals)
    if ref is not None:
        axr.legend(fontsize=14, loc="best")
    if xaxis == "time":
        lo, hi = axr.get_xlim()
        weeks = 1 if hi - lo < 45 else 2 if hi - lo < 130 else 4
        axr.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=weeks))
        axr.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        axr.set_xlabel("Date (2026)", fontsize=AXIS_FS)
    elif xaxis == "lumi":
        axr.set_xlim(0, 1.03 * np.nanmax(xn))
        axr.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=6))
        axr.set_xlabel(LUMI_LABEL, fontsize=AXIS_FS)
    else:
        axr.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=5, integer=True))
        axr.ticklabel_format(axis="x", style="plain", useOffset=False)
        axr.set_xlabel("Run number", fontsize=AXIS_FS)
    if ref is None:  # a difference w.r.t. 0 is the value itself: no bottom panel
        drop_bottom(fig, ax, axr)
    if center0:  # y axis symmetric around 0
        lo, hi = ax.get_ylim()
        m = max(abs(lo), abs(hi))
        ax.set_ylim(-m, m)
    if vlines:  # in the main panel the lines stop below the legend and the selection text
        fig.canvas.draw()
        to_ax = ax.transAxes.inverted()
        ytop = min(b.get_window_extent().transformed(to_ax).y0 for b in (leg, txt)) - 0.02
    for x, run in vlines or ():
        for a in fig.axes:
            a.axvline(x, ymax=ytop if a is ax else 1, color="dimgray", linestyle="--", linewidth=1.5, zorder=1)
        ax.text(x, 0.03, f"HLT alignment {run} ", transform=ax.get_xaxis_transform(), rotation=90, ha="right",
                va="bottom", fontsize=13, color="dimgray")
    if center0 or square:
        save_square(fig, path)
    else:
        save_square(fig, path)
    plt.close(fig)


def make_plots(p, runs, xs, xaxis, label, outdir, lumi=None):
    os.makedirs(outdir, exist_ok=True)
    for prof in sorted(p.profile.unique()):
        var, rest = prof.split("Vs")
        x, pt = rest.split("_pt")
        sel = rf"Scouting tracks from the PV, $p_{{T}} > {pt}$ GeV" + (r", $|\eta| < 2.5$" if x == "Eta" else "")
        styled_plot(series(p, runs, xs, prof, "average", "average_err"), "diff",
                    rf"$\langle {VAR_TEX[var]} \rangle$ [$\mu$m]", sel, xaxis, label, lumi,
                    f"{outdir}/{prof}_average", zero_line=True)
        styled_plot(series(p, runs, xs, prof, "spread", "spread_err"), "ratio",
                    rf"RMS of ${VAR_TEX[var]}({X_TEX[x]})$ [$\mu$m]",
                    sel + f"\nspread of ${VAR_TEX[var]}$ vs ${X_TEX[x]}$ (statistical part removed)",
                    xaxis, label, lumi, f"{outdir}/{prof}_spread", ymin0=True)
        if var == "dxy" and x == "Phi":
            for k, lab in (("dx", r"\Delta x"), ("dy", r"\Delta y")):
                styled_plot(series(p, runs, xs, prof, f"sin_{k}", f"sin_{k}_err"), "diff",
                            rf"${lab}$ of track origin w.r.t. PV [$\mu$m]",
                            sel + "\n" + r"fit $d_{xy}(\phi) = a - \Delta x \sin\phi + \Delta y \cos\phi$",
                            xaxis, label, lumi, f"{outdir}/{prof}_{k}", zero_line=True)


def overview(p, runs, xs, xaxis, path):
    profs = [f"{v}Vs{x}_pt{pt}" for v in ("dxy", "dz") for x in ("Eta", "Phi") for pt in (1, 10)]
    fig, axs = plt.subplots(8, 2, figsize=(18, 30), sharex=True)
    for row, prof in zip(axs, profs):
        for ax, col, err in ((row[0], "average", "average_err"), (row[1], "spread", None)):
            draw(ax, series(p, runs, xs, prof, col, err))
            ax.set_title(f"{prof}: {col} [μm]", fontsize=14, loc="left")
    axs[0, 0].legend(fontsize=11)
    if xaxis == "time":
        for ax in axs[-1]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    elif xaxis == "lumi":
        for ax in axs[-1]:
            ax.set_xlim(0, 1.03 * np.nanmax([xs[r] for r in runs]))
    fig.tight_layout()
    fig.savefig(path, dpi=80)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--indir", default=os.path.join(HERE, "results"))
    ap.add_argument("-o", "--outdir", default=os.path.join(HERE, "plots"))
    ap.add_argument("--exclusion", default=f"{SCAN}/run_exclusion.csv")
    ap.add_argument("--metrics", default=f"{SCAN}/metrics.csv")
    ap.add_argument("--label", default="Preliminary", help='CMS label text, e.g. "Preliminary", "Internal", ""')
    ap.add_argument("--xaxis", default="all", choices=("time", "run", "lumi", "both", "all"),
                    help="both = time and run; all = time, run and luminosity")
    ap.add_argument("--lumi", default=None,
                    help="integrated luminosity in fb^-1 for the CMS label, or 'auto' (selected runs, from --lumifile)")
    ap.add_argument("--lumifile", default=os.path.join(HERE, "..", "lumi_data.csv"), help="brilcalc csv with the luminosity per run")
    a = ap.parse_args()
    hep.style.use("CMS")

    p = pd.read_csv(f"{a.indir}/ip_summary.csv")
    q = pd.read_csv(f"{a.indir}/quality.csv")
    runs, excluded = selection(q, a.exclusion)
    times, est = run_times(runs, a.metrics)
    with open(f"{a.indir}/excluded_runs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "reason"])
        w.writerows(excluded)
    with open(f"{a.indir}/runs_used.txt", "w") as f:
        f.write("\n".join(f"{r}{'  # start time interpolated' if est[r] else ''}" for r in runs) + "\n")

    xaxes = {"both": ("time", "run"), "all": ("time", "run", "lumi")}.get(a.xaxis, (a.xaxis,))
    lumis = run_lumis(a.lumifile) if os.path.exists(a.lumifile) else {}
    if "lumi" in xaxes and not lumis:
        print(f"no luminosity file {a.lumifile}: skipping the luminosity axis")
        xaxes = tuple(x for x in xaxes if x != "lumi")
    missing = [r for r in runs if r not in lumis]
    if lumis and missing:
        print(f"runs without luminosity (left out of the luminosity axis): {missing}")
    label_lumi = a.lumi
    if a.lumi == "auto":
        label_lumi = f"{sum(lumis[r][1] for r in runs if r in lumis):.2f}" if lumis else None
        print(f"CMS label luminosity: {label_lumi} fb^-1 (recorded, selected runs)")

    for xaxis in xaxes:
        xs = times if xaxis == "time" else lumi_axis(runs, lumis) if xaxis == "lumi" else {r: r for r in runs}
        make_plots(p, runs, xs, xaxis, a.label, f"{a.outdir}/vs_{xaxis}", lumi=label_lumi)
        overview(p, runs, xs, xaxis, f"{a.outdir}/overview_vs_{xaxis}.png")
    print(f"{len(runs)} runs used, {len(excluded)} excluded ({sum(est.values())} with interpolated start time)")
    for r, why in excluded:
        print(f"  {r}: {why}")
    print(f"-> {a.outdir}")


if __name__ == "__main__":
    main()
