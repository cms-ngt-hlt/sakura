#!/usr/bin/env python3
"""
Figures for the NGT-demonstrator upload-latency analysis.

Reads analysis/out/perrun_all.csv and uploads_<wf>.csv (from analyze_uploads.py)
and writes PNG (300 dpi) + PDF into analysis/figs/.

Two analyses are drawn throughout: the FIRST upload of a run and the LAST upload
of a run, each referenced to the run start and to the run end.
"""

import os

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")
os.makedirs(FIGS, exist_ok=True)

WFS = ["BeamSpot", "EcalPedestals", "SiStripQuality", "SiStripDetVOff",
       "EcalLaserAPDPNRatios", "SiPixelAliHLTHGCombined"]
# tags filled by the NGT demonstrator; "NGT" = their union
DEMO = ["BeamSpot", "EcalPedestals", "SiStripQuality", "SiStripDetVOff"]
LABEL = {
    "BeamSpot": "Beam spot (NGT, per lumisection)",
    "EcalPedestals": "ECAL pedestals (NGT)",
    "SiStripQuality": "Strip tracker bad components (NGT)",
    "SiStripDetVOff": "Strip tracker HV/LV-off modules (NGT, per lumisection)",
    "EcalLaserAPDPNRatios": "ECAL laser corrections (prompt O2O, per lumisection)",
    "SiPixelAliHLTHGCombined": "Pixel alignment for HLT, high granularity (PCL)",
    "NGT": "NGT conditions, combined",
}
C = {
    "BeamSpot": "#d64545",
    "EcalPedestals": "#2b6cb0",
    "SiStripQuality": "#2f9e44",
    "SiStripDetVOff": "#8e44ad",
    "EcalLaserAPDPNRatios": "#17a2b8",
    "SiPixelAliHLTHGCombined": "#7f8c8d",
    "NGT": "#1a1a1a",
    "run": "#c9d2dc",
    "band": "#e9edf2",
    "first": "#0f9b9b",
    "last": "#f0a13c",
}
BUDGETS = [("Tiny", 1), ("Small", 3), ("Medium", 6), ("Large", 12)]
REF_TXT = {"start": "Time after start of run", "end": "Time after end of run"}
UPL_TXT = {"first": "first upload of the run", "last": "last upload of the run"}


def cms_style():
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "font.size": 13, "font.family": "sans-serif", "savefig.dpi": 300,
        "axes.labelsize": 14, "axes.titlesize": 14, "xtick.labelsize": 12,
        "ytick.labelsize": 12, "legend.fontsize": 11, "axes.axisbelow": True,
        "grid.alpha": 0.35,
    })


def cms_tag(ax, x=0.0, y=1.01, extra="NGT", inside=False):
    va = "top" if inside else "bottom"
    ax.text(x, y, "CMS", transform=ax.transAxes, fontsize=16, fontweight="bold",
            va=va, ha="left")
    ax_w_in = ax.get_window_extent().width / ax.figure.dpi
    ax.text(x + 0.62 / ax_w_in, y, extra, transform=ax.transAxes, fontsize=13,
            style="italic", va=va, ha="left")


def right_tag(ax, txt, y=1.01):
    ax.text(1.0, y, txt, transform=ax.transAxes, fontsize=12, va="bottom", ha="right")


def budget_lines(ax, top=True):
    for name, b in BUDGETS:
        ax.axvline(b, color="#9aa3ad", ls="--", lw=1.0, zorder=1)
    if top:
        sec = ax.secondary_xaxis("top")
        sec.set_xticks([b for _, b in BUDGETS], [f"{n}\n{b} h" for n, b in BUDGETS])
        sec.tick_params(axis="x", labelsize=10, colors="#5a6472", length=0)
        for s in sec.spines.values():
            s.set_visible(False)


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(FIGS, f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)
    print("wrote", os.path.join(FIGS, name + ".png"))


def load():
    pr = pd.read_csv(os.path.join(OUT, "perrun_all.csv"), parse_dates=["start", "end", "first", "last"])
    ups = {wf: pd.read_csv(os.path.join(OUT, f"uploads_{wf}.csv"), parse_dates=["inserted", "start", "end"])
           for wf in WFS}
    for wf in WFS:
        ups[wf] = ups[wf][~ups[wf]["dropped"]]
    return pr, ups


def sel(pr, wf):
    """Rows of one workflow, or of the demonstrator union for 'NGT'."""
    return pr[pr["workflow"].isin(DEMO)] if wf == "NGT" else pr[pr["workflow"] == wf]


# ---------------------------------------------------------------- figure 1
def fig_timeline(pr, ups, wf):
    """Every run as a row: grey bar = run, dots = uploads, first/last marked."""
    d = pr[pr["workflow"] == wf].sort_values("run").reset_index(drop=True)
    u = ups[wf]
    n = len(d)
    if n > 150:
        print(f"skip fig1_timeline_{wf}: {n} runs is too many for one row per run")
        return
    fig, ax = plt.subplots(figsize=(12.5, max(3.6, 0.27 * n + 2.2)))
    for i, r in d.iterrows():
        ax.barh(i, r["duration_h"], left=0, height=0.72, color=C["run"], zorder=1)
        t = u[u["run"] == r["run"]]["from_start_h"].values
        ax.plot(t, np.full_like(t, i), ".", ms=5, color="#5a6472", alpha=0.75, zorder=3)
        ax.plot([r["first_from_start_h"]], [i], marker="o", ms=7.5, color=C["first"], zorder=4)
        ax.plot([r["last_from_start_h"]], [i], marker="s", ms=6.5, color=C["last"], zorder=4)
    ax.set_yticks(range(n), [f"{r}" for r in d["run"]])
    ax.tick_params(axis="y", labelsize=9 if n > 30 else 10)
    ax.set_ylim(-0.8, n - 0.2)
    ax.invert_yaxis()
    ax.set_xlabel("Time after start of run [hours]")
    ax.set_ylabel("Run")
    xmax = max(d["last_from_start_h"].max(), d["duration_h"].max()) * 1.05
    ax.set_xlim(-0.3, xmax)
    ax.axvline(0, color="#333", lw=1.0)
    handles = [
        Patch(facecolor=C["run"], label="run (start $\\rightarrow$ end)"),
        Line2D([], [], marker=".", ls="", color="#5a6472", ms=8, label="upload"),
        Line2D([], [], marker="o", ls="", color=C["first"], ms=8, label="first upload"),
        Line2D([], [], marker="s", ls="", color=C["last"], ms=7, label="last upload"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.06 if n > 30 else -0.16),
              ncol=4, frameon=False)
    cms_tag(ax)
    right_tag(ax, f"{LABEL[wf]}: {n} runs, {int(d['n_uploads'].sum())} uploads")
    fig.tight_layout()
    save(fig, f"fig1_timeline_{wf}")


# ---------------------------------------------------------------- figure 2
def fig_cdf(pr, which):
    """Cumulative fraction of runs with the FIRST (or LAST) upload done vs time."""
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.6))
    for ax, ref in zip(axes, ("start", "end")):
        col = f"{which}_from_{ref}_h"
        lo = -16 if ref == "end" else 0
        hi = 24
        if ref == "end":
            ax.axvspan(lo, 0, color="#dff3ea", alpha=0.6, zorder=0)
            ax.text(lo + 0.4, 0.97, "delivered while the run\nwas still ongoing", fontsize=10,
                    va="top", color="#2f6b4e")
        for wf in WFS + ["NGT"]:
            v = sel(pr, wf)[col]
            s = np.sort(v.values)
            f = np.arange(1, len(s) + 1) / len(s)
            s = np.concatenate([[lo], s, [hi]])
            f = np.concatenate([[0], f, [1]])
            ax.step(s, f, where="post", lw=2.4 if wf == "NGT" else 1.7,
                    color=C[wf], ls="-" if wf in DEMO else (":" if wf != "NGT" else "--"),
                    label=f"{LABEL[wf]}  (median {np.median(v):.1f} h, n={len(v)})")
        budget_lines(ax)
        ax.axhline(0.5, color="#888", lw=0.8, ls=":")
        ax.set_xlim(lo, hi)
        ax.set_ylim(0, 1.0)
        ax.set_xlabel(REF_TXT[ref] + " [hours]")
        ax.set_ylabel(f"Fraction of runs with {UPL_TXT[which]}")
        ax.legend(loc="lower right", frameon=True, framealpha=0.95, fontsize=8.5)
        cms_tag(ax, x=0.012, y=0.985, inside=True) if ref == "start" else None
    right_tag(axes[1], f"{UPL_TXT[which].capitalize()}", y=1.10)
    fig.tight_layout()
    save(fig, f"fig2_cdf_{which}")


# ------------------------------------------- CMS-public square canvases
CMS_RLABEL = "2026 (13.6 TeV)"


def cms_square_frame(ax, lo, hi, ytop):
    """Fraction axis 0..1 with head room up to ytop for legend and labels."""
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, ytop)
    ax.grid(False)
    for sp in ax.spines.values():
        sp.set_color("black")
    ax.tick_params(which="both", colors="black")
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.yaxis.set_minor_locator(matplotlib.ticker.FixedLocator(np.arange(0, 1.01, 0.05)))
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(2 if hi - lo <= 20 else 5))


def cms_public_label(ax):
    import mplhep as hep
    hep.cms.label("Preliminary", data=True, rlabel=CMS_RLABEL, loc=0, ax=ax)


def fig_cdf_public(pr, which):
    """fig 2 for public use: one square canvas per reference (run start / run end),
    beam spot left out (10 runs only), no budget lines."""
    import mplhep as hep
    wfs = [wf for wf in WFS if wf != "BeamSpot"]
    demo = [wf for wf in DEMO if wf != "BeamSpot"]
    ytop = 1.62
    for ref in ("start", "end"):
        col = f"{which}_from_{ref}_h"
        lo = -16 if ref == "end" else 0
        hi = 24
        with plt.style.context(hep.style.CMS):
            fig, ax = plt.subplots(figsize=(10, 10))
            if ref == "end":
                ax.axvspan(lo, 0, ymax=1.0 / ytop, color="#dff3ea", alpha=0.6, zorder=0, lw=0)
                ax.axvline(0, ymax=1.0 / ytop, color="#333", lw=1.5)
                ax.text(-0.3, 1.03, r"$\leftarrow$ during the run", ha="right", va="bottom",
                        fontsize=16, color="#2f6b4e")
                ax.text(0.3, 1.03, r"after the run $\rightarrow$", ha="left", va="bottom",
                        fontsize=16, color="#333")
            for wf in wfs + ["NGT"]:
                v = (pr[pr["workflow"].isin(demo)] if wf == "NGT" else pr[pr["workflow"] == wf])[col]
                s = np.sort(v.values)
                f = np.arange(1, len(s) + 1) / len(s)
                s = np.concatenate([[lo], s, [hi]])
                f = np.concatenate([[0], f, [1]])
                lab = LABEL[wf]
                ax.step(s, f, where="post", lw=3.2 if wf == "NGT" else 2.2, color=C[wf],
                        ls="-" if wf in demo else (":" if wf != "NGT" else "--"),
                        label=f"{lab}: {np.median(v):+.1f} h" if ref == "end" else
                              f"{lab}: {np.median(v):.1f} h")
            ax.axhline(1.0, color="#333", lw=1.0)
            cms_square_frame(ax, lo, hi, ytop)
            ax.set_xlabel(f"{REF_TXT[ref]} [h]")
            ax.set_ylabel(f"Fraction of runs with {UPL_TXT[which]}")
            ax.legend(loc="upper left", fontsize=15, frameon=False, handlelength=2.6,
                      title=f"{UPL_TXT[which].capitalize()} (median after run {ref})",
                      title_fontsize=15, alignment="left")
            cms_public_label(ax)
            save(fig, f"fig2_cdf_{which}_{ref}")


# ---------------------------------------------------------------- figure 3
def fig_summary(pr):
    """Median + 16-84% band for first/last upload, from run start / run end."""
    rows = [(wf, which) for wf in WFS + ["NGT"] for which in ("first", "last")]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 0.55 * len(rows) + 1.8), sharey=True)
    for ax, ref in zip(axes, ("start", "end")):
        lo = -14 if ref == "end" else 0
        hi = 26
        if ref == "end":
            ax.axvspan(lo, 0, color="#dff3ea", alpha=0.6, zorder=0)
        for i, (wf, which) in enumerate(rows):
            v = sel(pr, wf)[f"{which}_from_{ref}_h"]
            p16, med, p84 = np.percentile(v, [16, 50, 84])
            col = C[which]
            ax.hlines(i, p16, p84, color=col, lw=6.0, alpha=0.35, zorder=2)
            ax.plot([v.mean()], [i], marker="|", ms=14, mew=2.0, color="#444", zorder=4)
            ax.plot([med], [i], marker="o" if which == "first" else "s", ms=8.5, color=col,
                    mec="#222", zorder=5)
            ax.text(min(p84, hi - 4) + 0.5, i, f"{med:+.1f} h", va="center", fontsize=10,
                    color="#333", bbox=dict(facecolor="white", edgecolor="none", pad=1.0), zorder=6)
        for k in range(1, len(WFS) + 1):
            ax.axhline(2 * k - 0.5, color="#ccc", lw=0.8 if k != len(DEMO) else 1.6)
        budget_lines(ax)
        ax.axvline(0, color="#333", lw=1.0)
        ax.set_xlim(lo, hi)
        ax.set_ylim(-0.7, len(rows) - 0.3)
        ax.set_xlabel(REF_TXT[ref] + " [hours]")
        ax.grid(axis="y", visible=False)
    axes[0].set_yticks(range(len(rows)),
                       [f"{LABEL[wf]}\n{which} upload" for wf, which in rows])
    axes[0].tick_params(axis="y", labelsize=10)
    axes[0].invert_yaxis()
    handles = [
        Line2D([], [], marker="o", ls="", color=C["first"], mec="#222", ms=8, label="first upload: median"),
        Line2D([], [], marker="s", ls="", color=C["last"], mec="#222", ms=8, label="last upload: median"),
        Patch(facecolor="#888", alpha=0.35, label="16$-$84% of runs"),
        Line2D([], [], marker="|", ls="", color="#444", ms=12, mew=2, label="mean"),
        Patch(facecolor="#dff3ea", label="before the run ended"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False, fontsize=10.5,
               bbox_to_anchor=(0.5, -0.03))
    cms_tag(axes[0], x=0.012, y=0.985, inside=True)
    axes[1].set_title("one entry per run", loc="right", fontsize=12, pad=30)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    save(fig, "fig3_summary_first_vs_last")


# ---------------------------------------------------------------- figure 4
def fig_hist(pr):
    """2x2: first/last upload x from start/end, per-workflow histograms.

    Normalised per workflow (fraction of its runs per hour): the tags have from
    10 to 1700 runs, so stacked counts would only show the largest one.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14.0, 8.6))
    for r, which in enumerate(("first", "last")):
        for c, ref in enumerate(("start", "end")):
            ax = axes[r, c]
            col = f"{which}_from_{ref}_h"
            lo = -16 if ref == "end" else 0
            bins = np.arange(lo, 24.01, 1.0)
            if ref == "end":
                ax.axvspan(lo, 0, color="#dff3ea", alpha=0.6, zorder=0)
            for wf in WFS:
                v = pr[pr["workflow"] == wf][col]
                ax.hist(v.clip(lo, 23.99), bins=bins, histtype="step", lw=1.8 if wf in DEMO else 1.3,
                        ls="-" if wf in DEMO else ":", color=C[wf], density=True,
                        label=f"{LABEL[wf]} (median {v.median():+.1f} h, n={len(v)})")
            med = sel(pr, "NGT")[col].median()
            ax.axvline(med, color="#1a1a1a", lw=1.6, ls="--", label=f"NGT combined: median {med:+.1f} h")
            ax.set_xlim(lo, 24)
            ax.set_xlabel(f"{UPL_TXT[which].capitalize()}: {REF_TXT[ref].lower()} [hours]")
            ax.set_ylabel("Fraction of the tag's runs / 1 h")
            ax.legend(loc="upper right", frameon=True, fontsize=8)
            for _, b in BUDGETS:
                ax.axvline(b, color="#9aa3ad", ls=":", lw=0.9, zorder=1)
    cms_tag(axes[0, 0])
    right_tag(axes[0, 1], "entries clipped to the axis range")
    fig.tight_layout()
    save(fig, "fig4_histograms")


# ---------------------------------------------------------------- figure 5
def fig_cadence(pr, ups):
    """How the uploads are spread inside a run: count vs duration, cadence, span."""
    fig, axes = plt.subplots(1, 3, figsize=(16.5, 6.4))
    # draw the big prompt/PCL samples first so the demonstrator points stay on top
    order = [wf for wf in WFS if wf not in DEMO] + DEMO

    ax = axes[0]
    for wf in order:
        d = pr[pr["workflow"] == wf]
        ax.scatter(d["duration_h"], d["n_uploads"], s=30 if wf in DEMO else 16, color=C[wf],
                   alpha=0.85 if wf in DEMO else 0.4, lw=0,
                   label=f"{LABEL[wf]} (median {d['n_uploads'].median():.0f}/run)", zorder=3)
    ax.set_yscale("log")
    ax.set_xlabel("Run duration [hours]")
    ax.set_ylabel("Uploads per run")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), fontsize=8.5, frameon=False, ncol=1)
    cms_tag(ax)

    ax = axes[1]
    bins = np.arange(0, 125, 5)
    for wf in order:
        v = pr[(pr["workflow"] == wf)]["cadence_median_min"].dropna().clip(0, 124)
        ax.hist(v, bins=bins, histtype="step", lw=1.8 if wf in DEMO else 1.3,
                ls="-" if wf in DEMO else ":", color=C[wf], density=True,
                label=f"{LABEL[wf]} (median {v.median():.0f} min, n={len(v)})")
    ax.set_xlabel("Median gap between consecutive uploads within a run [min]")
    ax.set_ylabel("Fraction of the tag's runs / 5 min")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), fontsize=8.5, frameon=False, ncol=1)
    ax.set_title("runs with $\\geq$ 2 uploads", loc="right", fontsize=11, pad=8)

    ax = axes[2]
    for wf in order:
        d = pr[pr["workflow"] == wf]
        ax.scatter(d["duration_h"], d["span_h"], s=30 if wf in DEMO else 16, color=C[wf],
                   alpha=0.85 if wf in DEMO else 0.4, lw=0, zorder=3,
                   label=f"{LABEL[wf]} (median span {d['span_h'].median():.1f} h)")
    lim = max(pr["duration_h"].max(), 17)
    ax.plot([0, lim], [0, lim], color="#888", ls=":", lw=1.0, label="span = run duration")
    ax.set_xlabel("Run duration [hours]")
    ax.set_ylabel("First $\\rightarrow$ last upload [hours]")
    ax.set_ylim(-0.5, min(pr["span_h"].max() * 1.05, 40))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), fontsize=8.5, frameon=False, ncol=1)
    ax.set_title("one entry per run", loc="right", fontsize=11, pad=8)
    fig.tight_layout()
    save(fig, "fig5_cadence")


# ---------------------------------------------------------------- figure 6
def fig_first_vs_duration(pr):
    """Does the first upload wait for the end of the run?  Latency vs duration."""
    fig, axes = plt.subplots(1, 2, figsize=(14.0, 5.8))
    order = [wf for wf in WFS if wf not in DEMO] + DEMO
    for ax, which in zip(axes, ("first", "last")):
        for wf in order:
            d = pr[pr["workflow"] == wf]
            ax.scatter(d["duration_h"], d[f"{which}_from_start_h"], s=34 if wf in DEMO else 16,
                       color=C[wf], alpha=0.85 if wf in DEMO else 0.4, lw=0,
                       label=LABEL[wf], zorder=3)
        lim = pr["duration_h"].max() * 1.05
        ax.plot([0, lim], [0, lim], color="#555", ls="--", lw=1.2, label="upload at run end")
        ax.fill_between([0, lim], [0, 0], [0, lim], color="#dff3ea", alpha=0.6, zorder=0)
        ax.text(lim * 0.97, lim * 0.10, "during the run", ha="right", fontsize=10, color="#2f6b4e")
        if which == "last":
            ax.axhline(8.1, color="#d64545", lw=1.2, ls=":", zorder=2)
            ax.text(lim * 0.97, 8.5, "uploads stop 8.1 h after run start", ha="right",
                    fontsize=10, color="#d64545")
        ax.set_xlim(0, lim)
        ax.set_ylim(0, min(pr[f"{which}_from_start_h"].max() * 1.05, 30))
        ax.set_xlabel("Run duration [hours]")
        ax.set_ylabel(f"{UPL_TXT[which].capitalize()}: time after start of run [hours]")
        ax.legend(loc="upper left", fontsize=8.5, frameon=True, framealpha=0.95)
    cms_tag(axes[0])
    right_tag(axes[1], "entries above 30 h clipped")
    fig.tight_layout()
    save(fig, "fig6_latency_vs_duration")


# ---------------------------------------------------------------- figure 7
def fig_decomposition(pr, ref):
    """Same layout as fig1_decomposition of the PCL analysis.

    Stacked MEANS (only means are additive): reference -> first upload, then
    first -> last upload, so the bar ends at the mean of the last upload.
    Overlaid: median of the first (o) and of the last (diamond) upload, each
    with its 16-84% band.
    """
    rows = []
    for wf in WFS + ["NGT"]:
        d = sel(pr, wf)
        f, l = d[f"first_from_{ref}_h"], d[f"last_from_{ref}_h"]
        rows.append((LABEL[wf], f.mean(), l.mean(), f.median(), *np.percentile(f, [16, 84]),
                     l.median(), *np.percentile(l, [16, 84]), len(d)))
    lab, fmean, lmean, fmed, f16, f84, lmed, l16, l84, n = map(np.array, zip(*rows))
    y = np.arange(len(lab))

    fig, ax = plt.subplots(figsize=(12.6, 0.78 * len(lab) + 2.0))
    lo = min(-12.0, f16.min() - 1) if ref == "end" else 0.0
    hi = max(l84.max(), lmean.max()) * 1.36
    if ref == "end":
        ax.axvspan(lo, 0, color="#dff3ea", alpha=0.6, zorder=0)
        ax.text(lo + 0.3, len(lab) - 0.55, "before the run ended", fontsize=10, color="#2f6b4e")
    ax.barh(y, fmean, color=C["first"], height=0.62, label=f"{'run ' + ref} $\\rightarrow$ first upload (mean)")
    ax.barh(y, lmean - fmean, left=fmean, color=C["last"], height=0.62,
            label="first $\\rightarrow$ last upload (mean)")
    ax.errorbar(fmed, y + 0.12, xerr=[fmed - f16, f84 - fmed], fmt="o", ms=6, color="#0b4f4f",
                lw=1.4, capsize=3, zorder=5, label="first upload: median with 16$-$84% band")
    ax.errorbar(lmed, y - 0.12, xerr=[lmed - l16, l84 - lmed], fmt="D", ms=6, color=C["NGT"],
                lw=1.4, capsize=3, zorder=5, label="last upload: median with 16$-$84% band")
    for i in range(len(lab)):
        ax.text(max(l84[i], lmean[i]) + 0.4, i,
                f"first {fmed[i]:+.1f} h, last {lmed[i]:+.1f} h  (n={n[i]})",
                va="center", fontsize=10, color="#444")
    ax.axvline(0, color="#333", lw=1.0)
    ax.axhline(len(DEMO) - 0.5, color="#999", lw=1.2)
    ax.set_yticks(y, lab)
    ax.tick_params(axis="y", labelsize=11)
    ax.set_xlabel(REF_TXT[ref] + " [hours]")
    ax.set_xlim(lo, hi)
    ax.set_ylim(-0.7, len(lab) - 0.3)
    ax.invert_yaxis()
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, frameon=False, fontsize=10.5)
    cms_tag(ax)
    right_tag(ax, "one entry per run, medians and means over runs")
    fig.tight_layout()
    save(fig, "fig7_decomposition" + ("" if ref == "end" else "_from_start"))


# ---------------------------------------------------------------- figure 8
def load_perls(wf):
    path = os.path.join(OUT, f"perls_{wf}.csv")
    if not os.path.exists(path):
        return None
    f = pd.read_csv(path)
    for c in ("start", "end", "ls_time", "inserted"):
        f[c] = pd.to_datetime(f[c], format="ISO8601")
    return f


def fig_perls_latency(wf):
    """By-LS tags: latency of every lumisection's condition (first upload per LS)."""
    f = load_perls(wf)
    if f is None:
        return
    runs = sorted(f["run"].unique())
    per_run_colours = len(runs) <= 12
    cmap = plt.get_cmap("tab10")
    col = {r: cmap(i % 10) for i, r in enumerate(runs)}
    ymax = min(f["latency_h"].max() * 1.08, 30.0)
    n_clip = int((f["latency_h"] > ymax).sum())

    fig, axes = plt.subplots(1, 2, figsize=(15.5, 5.8), gridspec_kw={"width_ratios": [1.7, 1]})

    # (a) every LS: latency vs the wall-clock time the LS was acquired
    ax = axes[0]
    for _, b in BUDGETS:
        ax.axhline(b, color="#9aa3ad", ls="--", lw=0.9, zorder=1)
    for name, b in BUDGETS:
        ax.text(f["ls_time"].min() - pd.Timedelta(hours=6), b, f" {name}", fontsize=9,
                color="#5a6472", va="bottom")
    if per_run_colours:
        for r in runs:
            d = f[f["run"] == r]
            ax.scatter(d["ls_time"], d["latency_h"].clip(upper=ymax), s=42, color=col[r],
                       edgecolor="#222", lw=0.4, label=f"{r}  ({len(d)} LS)", zorder=3)
        ax.legend(title="run", ncol=2, fontsize=9, title_fontsize=9.5, loc="upper right", frameon=True)
    else:
        ax.scatter(f["ls_time"], f["latency_h"].clip(upper=ymax), s=14, color=C[wf], alpha=0.45,
                   lw=0, zorder=3)
    med = f["latency_h"].median()
    ax.axhline(med, color="#1a1a1a", lw=1.4, ls=":", zorder=2)
    ax.text(f["ls_time"].max() + pd.Timedelta(hours=6), med, f"median {med:.1f} h", fontsize=10,
            va="bottom", ha="right")
    ax.set_xlabel("Time the lumisection was acquired (UTC)")
    ax.set_ylabel("LS acquired $\\rightarrow$ condition uploaded [hours]")
    ax.set_ylim(0, ymax)
    fig.autofmt_xdate(rotation=0, ha="center")
    cms_tag(ax)
    ax.set_title(f"{LABEL[wf]}, first upload per (run, LS)"
                 + (f", {n_clip} entries clipped" if n_clip else ""),
                 loc="right", fontsize=11, pad=26)

    # (b) the distribution
    ax = axes[1]
    bins = np.arange(0, ymax + 1.0, 1.0 if ymax > 12 else 0.5)
    ax.hist(f["latency_h"].clip(upper=ymax - 1e-6), bins=bins, color=C[wf], alpha=0.8, edgecolor="white")
    ax.axvline(med, color="#1a1a1a", lw=1.4, ls=":", label=f"median {med:.1f} h")
    ax.axvline(f["latency_h"].mean(), color="#1a1a1a", lw=1.4, ls="--",
               label=f"mean {f['latency_h'].mean():.1f} h")
    p16, p84 = np.percentile(f["latency_h"], [16, 84])
    ax.axvspan(p16, p84, color="#e9edf2", zorder=0, label=f"16$-$84%: {p16:.1f}$-${p84:.1f} h")
    for _, b in BUDGETS:
        ax.axvline(b, color="#9aa3ad", ls="--", lw=0.9, zorder=1)
    ax.set_xlabel("LS acquired $\\rightarrow$ condition uploaded [hours]")
    ax.set_ylabel(f"Lumisections / {'1 h' if ymax > 12 else '30 min'}")
    ax.legend(loc="upper right", frameon=True, fontsize=10)
    right_tag(ax, f"{len(f)} lumisections, {len(runs)} runs")
    fig.tight_layout()
    save(fig, f"fig8_perls_latency_{wf}")


# ---------------------------------------------------------------- figure 9
def fig_perls_timeline(wf):
    """By-LS tags with few runs: per run, each LS drawn from acquisition to upload."""
    f = load_perls(wf)
    if f is None:
        return
    runs = sorted(f["run"].unique())
    if len(runs) > 40:
        print(f"skip fig9_perls_timeline_{wf}: {len(runs)} runs")
        return
    fig, ax = plt.subplots(figsize=(13.0, 6.2))
    for i, r in enumerate(runs):
        d = f[f["run"] == r].sort_values("lumi")
        dur = d["duration_h"].iloc[0]
        ax.barh(i, dur, left=0, height=0.78, color=C["run"], zorder=1)
        k = len(d)
        # spread the LS of one run over the height of its bar, in LS order
        yy = i + np.linspace(-0.3, 0.3, k) if k > 1 else np.array([i])
        for y0, (_, row) in zip(yy, d.iterrows()):
            ax.plot([row["ls_from_start_h"], row["upload_from_start_h"]], [y0, y0],
                    color="#5a6472", lw=0.9, alpha=0.7, zorder=2)
        ax.scatter(d["ls_from_start_h"], yy, marker="|", s=90, color="#0f9b9b", lw=1.6, zorder=3)
        ax.scatter(d["upload_from_start_h"], yy, s=22, color=C[wf], edgecolor="#222",
                   lw=0.3, zorder=4)
        ax.text(max(d["upload_from_start_h"].max(), dur) + 0.3, i,
                f"{k} LS, median {d['latency_h'].median():.1f} h", va="center", fontsize=9.5,
                color="#444")
    ax.set_yticks(range(len(runs)), [str(r) for r in runs])
    ax.invert_yaxis()
    ax.set_ylabel("Run")
    ax.set_xlabel("Time after start of run [hours]")
    ax.set_xlim(-0.3, f["upload_from_start_h"].max() * 1.22)
    ax.axvline(0, color="#333", lw=1.0)
    handles = [
        Patch(facecolor=C["run"], label="run (start $\\rightarrow$ end)"),
        Line2D([], [], marker="|", ls="", color="#0f9b9b", ms=11, mew=1.6, label="lumisection acquired"),
        Line2D([], [], marker="o", ls="", color=C[wf], mec="#222", ms=6, label="its first upload"),
        Line2D([], [], color="#5a6472", lw=1, label="latency"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False)
    cms_tag(ax)
    right_tag(ax, f"{LABEL[wf]}: one line per (run, LS), rows sorted by LS")
    fig.tight_layout()
    save(fig, f"fig9_perls_timeline_{wf}")


# ---------------------------------------------------------------- figure 10
TIMEOUT_H = 8.0


def fig_margin_to_timeout(pr):
    """Margin to the NGT timeout of 8 h.  The first upload of a run is
    measured against 8 h after the run START, the last upload against 8 h after
    the run END:  margin = 8 h - (upload - reference).
    Drawn as the fraction of runs with at least x hours of margin: the value at
    x = 0 is the fraction that made the deadline.  Beam spot excluded."""
    import mplhep as hep
    wfs = [wf for wf in WFS if wf != "BeamSpot"]
    demo = [wf for wf in DEMO if wf != "BeamSpot"]
    ref_of = {"first": "start", "last": "end"}
    lo = -10.0
    ytop = 1.62                                   # head room for the legend, above all curves
    rows = []
    for which in ("first", "last"):
        ref = ref_of[which]
        # a last upload made before the run ended has more than 8 h of margin
        hi = max(8.0, np.ceil(TIMEOUT_H - pr[~pr["workflow"].eq("BeamSpot")][f"{which}_from_{ref}_h"].min()))
        with plt.style.context(hep.style.CMS):
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.axvspan(lo, 0, ymax=1.0 / ytop, color="#fbe3e3", alpha=0.7, zorder=0, lw=0)
            ax.axvspan(0, hi, ymax=1.0 / ytop, color="#dff3ea", alpha=0.6, zorder=0, lw=0)
            for wf in wfs + ["NGT"]:
                d = pr[pr["workflow"].isin(demo)] if wf == "NGT" else pr[pr["workflow"] == wf]
                m = TIMEOUT_H - d[f"{which}_from_{ref}_h"].values
                s = np.sort(m)[::-1]                      # fraction with margin >= x
                f = np.arange(1, len(s) + 1) / len(s)
                xs = np.concatenate([[hi], s, [lo]])
                ys = np.concatenate([[0], f, [f[-1]]])
                ok = float((m >= 0).mean())
                lab = LABEL[wf]
                ax.step(xs, ys, where="pre", lw=3.2 if wf == "NGT" else 2.2, color=C[wf],
                        ls="-" if wf in demo else (":" if wf != "NGT" else "--"),
                        label=f"{lab}: {np.median(m):+.1f} h, {ok*100:.0f}%")
                rows.append(dict(workflow=wf, upload=which, deadline=f"run {ref} + 8 h", n=len(m),
                                 margin_median_h=np.median(m),
                                 margin_mean_h=m.mean(), margin_p16_h=np.percentile(m, 16),
                                 margin_p84_h=np.percentile(m, 84), frac_in_time=ok,
                                 frac_margin_ge_1h=float((m >= 1).mean()),
                                 frac_margin_ge_3h=float((m >= 3).mean())))
            ax.axvline(0, ymax=1.0 / ytop, color="#333", lw=1.5)
            ax.axhline(1.0, color="#333", lw=1.0)
            cms_square_frame(ax, lo, hi, ytop)
            ax.set_xlabel(f"Margin of {UPL_TXT[which]} to 8 h timeout [h]")
            ax.set_ylabel("Fraction of runs with at least this margin")
            ax.legend(loc="upper left", fontsize=15, frameon=False, handlelength=2.6,
                      title=f"Deadline: run {ref} + 8 h  (median margin, in time)",
                      title_fontsize=15, alignment="left")
            # region labels sit in the band between the legend and the curves
            ax.text(-0.3, 1.03, r"$\leftarrow$ rejected", ha="right", va="bottom", fontsize=16,
                    color="#8b2e2e")
            ax.text(0.3, 1.03, r"accepted $\rightarrow$", ha="left", va="bottom", fontsize=16,
                    color="#2f6b4e")
            cms_public_label(ax)
            save(fig, f"fig10_margin_to_timeout_{ref}")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "margin_to_timeout.csv"), index=False)
    print("wrote", os.path.join(OUT, "margin_to_timeout.csv"))


# ---------------------------------------------------------------- figure 11
LS_SECONDS = 2**18 * 88.924e-6


def fig_laser_upload_delay():
    """ECAL laser: delay of EVERY upload to the lumisection its IOV starts at,
    LS time = run start + LS x 23.31 s.  Unlike fig 8 this keeps the re-uploads
    (same since inserted again at a later cron tick)."""
    wf = "EcalLaserAPDPNRatios"
    u = pd.read_csv(os.path.join(OUT, f"uploads_{wf}.csv"))
    for c in ("inserted", "start", "end"):
        u[c] = pd.to_datetime(u[c], format="ISO8601")
    u = u[~u["dropped"]].copy()
    u["ls_time"] = u["start"] + pd.to_timedelta(u["lumi"] * LS_SECONDS, unit="s")
    u["delay_h"] = (u["inserted"] - u["ls_time"]).dt.total_seconds() / 3600.0
    u["ls_h"] = u["lumi"] * LS_SECONDS / 3600.0
    u = u.sort_values("inserted")
    # an identical payload hash inserted again for the same since is a repeat
    # of the O2O, not a new condition: keep only its first insertion
    n_before = len(u)
    u = u.drop_duplicates(["run", "lumi", "payload"], keep="first")
    n_repeat = n_before - len(u)
    u["rank"] = u.groupby(["run", "lumi"]).cumcount()
    first, again = u[u["rank"] == 0], u[u["rank"] > 0]
    ymax = 12.0
    n_clip = int((u["delay_h"] > ymax).sum())
    med, p16, p84 = np.percentile(u["delay_h"], [50, 16, 84])

    fig, axes = plt.subplots(1, 3, figsize=(18.5, 5.8), gridspec_kw={"width_ratios": [1.8, 1, 1]})

    # (a) every upload vs the wall-clock time of its lumisection
    ax = axes[0]
    for _, b in BUDGETS[:3]:
        ax.axhline(b, color="#9aa3ad", ls="--", lw=0.9, zorder=1)
    for name, b in BUDGETS[:3]:
        ax.text(u["ls_time"].min() + pd.Timedelta(days=28), b, f" {name}", fontsize=9,
                color="#5a6472", va="bottom")
    ax.scatter(first["ls_time"], first["delay_h"].clip(upper=ymax), s=12, color=C[wf], alpha=0.45,
               lw=0, label=f"first upload of the LS  (n={len(first)})", zorder=3)
    if len(again):
        ax.scatter(again["ls_time"], again["delay_h"].clip(upper=ymax), s=30, marker="x",
                   color="#d64545", lw=1.2,
                   label=f"same since, different payload  (n={len(again)})", zorder=4)
    ax.axhline(med, color="#1a1a1a", lw=1.4, ls=":", zorder=2)
    ax.text(u["ls_time"].max() + pd.Timedelta(hours=6), med, f"median {med:.2f} h", fontsize=10,
            va="bottom", ha="right")
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Time the lumisection was acquired (UTC)")
    ax.set_ylabel("Upload $-$ lumisection covered [hours]")
    ax.legend(loc="upper right", fontsize=9.5, frameon=True, framealpha=0.95)
    ax.set_title(f"{n_repeat} repeated-hash uploads removed; {n_clip} entries above {ymax:.0f} h clipped",
                 loc="right", fontsize=11, pad=26)
    fig.autofmt_xdate(rotation=0, ha="center")
    cms_tag(ax, extra="ECAL laser corrections, prompt O2O")

    # (b) fine histogram of the delay: the 30-min cron shows as the width
    ax = axes[1]
    hmax = 12.0
    bins = np.arange(0, hmax + 1e-6, 5 / 60)
    ax.hist(u["delay_h"], bins=bins, color=C[wf], alpha=0.8, edgecolor="none",
            label=f"uploads (n={len(u)})")
    ax.axvspan(p16, p84, color="#e9edf2", zorder=0, label=f"16$-$84%: {p16:.2f}$-${p84:.2f} h")
    ax.axvline(med, color="#1a1a1a", lw=1.4, ls=":", label=f"median {med:.2f} h")
    ax.axvline(u["delay_h"].mean(), color="#1a1a1a", lw=1.4, ls="--",
               label=f"mean {u['delay_h'].mean():.2f} h")
    for _, b in BUDGETS:
        ax.axvline(b, color="#9aa3ad", ls="--", lw=0.9, zorder=1)
    ax.set_xlim(0, hmax)
    ax.set_xlabel("Upload $-$ lumisection covered [hours]")
    ax.set_ylabel("Uploads / 5 min")
    ax.legend(loc="upper right", fontsize=9, frameon=True)
    ax.set_title(f"{100 * (u['delay_h'] >= hmax).mean():.1f}% of uploads above {hmax:.0f} h not shown",
                 loc="right", fontsize=11, pad=8)

    # (c) does the delay depend on where in the run the LS is?
    ax = axes[2]
    core = u[u["delay_h"] < ymax]
    ax.scatter(core["ls_h"], core["delay_h"], s=9, color=C[wf], alpha=0.3, lw=0, zorder=2)
    edges = np.array([0, 0.25, 0.5, 1, 2, 3, 4, 6, 8, 12, 16, 24])
    mids, meds, lo, hi = [], [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s = core[(core["ls_h"] >= a) & (core["ls_h"] < b)]["delay_h"]
        if len(s) >= 10:
            mids.append(0.5 * (a + b)); meds.append(s.median())
            lo.append(np.percentile(s, 16)); hi.append(np.percentile(s, 84))
    ax.errorbar(mids, meds, yerr=[np.array(meds) - lo, np.array(hi) - np.array(meds)], fmt="o-",
                color="#1a1a1a", ms=5, lw=1.3, capsize=3, zorder=4,
                label="median with 16$-$84% band per bin")
    ax.set_xscale("log")
    ax.set_xlim(0.005, 24)
    ax.set_xticks([LS_SECONDS / 3600 * k for k in (1, 10, 100, 1000)],
                  ["LS 1\n23 s", "LS 10\n4 min", "LS 100\n39 min", "LS 1000\n6.5 h"])
    ax.set_ylim(0, ymax)
    ax.set_xlabel("Covered lumisection (position in the run)")
    ax.set_ylabel("Upload $-$ lumisection covered [hours]")
    ax.legend(loc="upper left", fontsize=9.5, frameon=True)
    ax.set_title("uploads below 12 h", loc="right", fontsize=11, pad=8)
    fig.tight_layout()
    save(fig, "fig11_ecallaser_upload_delay")


def main():
    cms_style()
    pr, ups = load()
    fig_laser_upload_delay()
    fig_margin_to_timeout(pr)
    for wf in WFS:
        fig_perls_latency(wf)
        fig_perls_timeline(wf)
    fig_decomposition(pr, "end")
    fig_decomposition(pr, "start")
    for wf in WFS:
        fig_timeline(pr, ups, wf)
    fig_cdf(pr, "first")
    fig_cdf(pr, "last")
    fig_cdf_public(pr, "first")
    fig_cdf_public(pr, "last")
    fig_summary(pr)
    fig_hist(pr)
    fig_cadence(pr, ups)
    fig_first_vs_duration(pr)


if __name__ == "__main__":
    main()
