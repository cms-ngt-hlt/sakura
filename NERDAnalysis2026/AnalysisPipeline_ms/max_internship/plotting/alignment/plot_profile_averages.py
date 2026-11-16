#!/usr/bin/env python3
"""Scouting tracking DQM histograms summed over runs, HLT / Prompt / NGT conditions overlaid.

Input : DQMOutput/scouting/{HLT,Prompt,NGT}/DQM_scouting_R<run>.root
        (HLT/Run summary/<folder>/<subdir>/..., every 1D TProfile and TH1, in all subfolders)
Output: plots/scouting_tracks/<subfolder>/<name>.{png,pdf}
            profiles: entries-weighted average, bottom panel difference (ratio for profiles of positive
                      quantities, e.g. the *Err* ones) w.r.t. Prompt
            1D      : sum over runs (same events for the three condition sets), bottom panel ratio
                      w.r.t. Prompt; --norm normalises each to unit area
        results/<outdir name>_profiles.csv, results/<outdir name>_hists.csv   one row per (variant, name, bin)

The profiles are combined bin by bin as ROOT's TProfile::Add does, i.e. each bin is the mean of the per-run
bin contents weighted by their number of entries:
  <y>_bin = sum_runs(sum w y) / sum_runs(sum w),   error = RMS / sqrt(N_eff)   (ROOT default error option)
Runs: those in results/runs_used.txt (plot_trends.py selection) present for all three condition sets;
--all-runs takes every run present for all three. Profile bins with < --min-entries entries are not drawn.
TProfile2D and TH2 are not plotted.

--folder selects the DQM folder under "HLT/Run summary" (default ScoutingOnline); if a file does not have
it, ScoutingOffline is used instead and a notice is printed.
The TracksPV profiles alone (previous default): --subdir Tracks/TracksPV -o plots/profile_averages

Usage: plot_profile_averages.py [-d ../DQMOutput] [-o plots/scouting_tracks] [-r results]
                                [--folder ScoutingOnline] [--subdir Tracks] [--all-runs] [--min-entries 100]
                                [--norm] [--label Preliminary] [--lumi X] [--only TracksPV/dxyVsEta_pt1 ...]
"""
import argparse
import csv
import glob
import os
import re
from multiprocessing import Pool

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import uproot  # noqa: E402

import plot_trends as PT  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
VARIANTS = ("HLT", "Prompt", "NGT")
FALLBACK = "ScoutingOffline"
# same look as plot_trends.py (styled_plot)
STYLE = {
    "HLT": dict(color="#5790fc", marker="o"),
    "NGT": dict(color="#f89c20", marker="D"),
    "Prompt": dict(color="black", marker="v"),
}
ORDER = ("HLT", "NGT", "Prompt")
REF = "Prompt"
LEGEND_ORDER = ("Prompt", "HLT", "NGT")
TEXT = "HLT Scouting"
MATHTEXT = matplotlib.mathtext.MathTextParser("path")


def run_of(fn):
    return int(re.search(r"_R0*(\d+)\.root$", fn).group(1))


def root2tex(s):
    """ROOT TLatex axis title -> matplotlib mathtext (good enough for the DQM titles)."""
    s = s.replace("#LT", r"\langle ").replace("#GT", r"\rangle ").replace("#mum", r"\mu\mathrm{m}")
    s = re.sub(r"#([A-Za-z]+)", r"\\\1", s)
    s = s.replace(r"\Lumi", "Lumi")
    # spaces inside sub/superscripts become math spaces, so the chunk below stays in one piece
    s = re.sub(r"([_^]\{)([^{}]*)\}", lambda m: m.group(1) + m.group(2).replace(" ", r"\;") + "}", s)
    # put every chunk with TeX in $...$
    t = re.sub(r"([^\s\[\]()]*(?:\\|_\{|\^\{)[^\s\[\]()]*)", r"$\1$", s)
    try:
        MATHTEXT.parse(t)
        return t
    except ValueError:  # give up on TeX, plain text
        return re.sub(r"[\\{}$]", "", s).replace("_", "").replace("^", "")


def titles(o):
    return o.member("fXaxis").member("fTitle"), o.member("fYaxis").member("fTitle")


def labels(o):
    lab = o.member("fXaxis").member("fLabels")
    if lab is None or not len(lab):
        return None
    out = [""] * (len(o.member("fXaxis").edges()) - 1)
    for s in lab:
        i = s.member("@fUniqueID")
        if i and 1 <= i <= len(out):
            out[i - 1] = str(s)
    return out


def read_file(args):
    """Raw sums of every 1D TProfile / TH1 below <folder>/<subdir> of one file, keyed by relative path:
    profiles {name: (edges, sum_wy, sum_wy2, sum_w, sum_w2, titles)}, hists {name: (edges, sumw, sumw2, titles, labels)}."""
    fn, folder, subdir = args
    run = run_of(fn)
    f = uproot.open(fn)
    used = folder
    try:
        d = f[f"DQMData/Run {run}/HLT/Run summary/{folder}/{subdir}"]
    except KeyError:
        used = FALLBACK
        d = f[f"DQMData/Run {run}/HLT/Run summary/{FALLBACK}/{subdir}"]
    prof, hist = {}, {}
    for key, cls in d.classnames(recursive=True).items():
        name = key.split(";")[0]
        if cls == "TProfile":
            o = d[key]
            n = np.asarray(o.member("fBinEntries"), dtype=float)
            wy = o.values(flow=True) * n
            wy2 = np.asarray(o.member("fSumw2"), dtype=float)
            bw2 = np.asarray(o.member("fBinSumw2"), dtype=float)
            if bw2.size != n.size:  # unweighted fill: sum w^2 = sum w
                bw2 = n.copy()
            prof[name] = (o.axis().edges(), wy, wy2, n, bw2, titles(o))
        elif cls.startswith("TH1"):
            o = d[key]
            hist[name] = (o.axis().edges(), o.values(flow=True).astype(float), o.variances(flow=True).astype(float),
                          titles(o), labels(o))
    return run, used, prof, hist


def accumulate(per_run, nsum):
    """Sum the first nsum arrays (after the edges) of every entry over runs."""
    acc = {}
    for objs in per_run:
        for name, t in objs.items():
            if name not in acc:
                acc[name] = [t[0]] + [x.copy() for x in t[1:1 + nsum]] + list(t[1 + nsum:])
                continue
            a = acc[name]
            if len(a[1]) != len(t[1]):
                raise RuntimeError(f"{name}: binning changes between runs")
            for i in range(1, 1 + nsum):
                a[i] += t[i]
    return acc


def merge_profiles(per_run):
    """{name: dict(edges, mean, err, entries, titles)} of the run-merged profiles."""
    res = {}
    for name, (edges, wy, wy2, n, bw2, tit) in accumulate(per_run, 4).items():
        sl = slice(1, -1)  # drop under/overflow
        wy, wy2, n, bw2 = wy[sl], wy2[sl], n[sl], bw2[sl]
        with np.errstate(divide="ignore", invalid="ignore"):
            mean = np.where(n > 0, wy / n, np.nan)
            rms = np.sqrt(np.maximum(wy2 / n - mean ** 2, 0))
            neff = np.where(bw2 > 0, n ** 2 / bw2, 0)
            err = np.where(neff > 0, rms / np.sqrt(neff), np.nan)
        res[name] = dict(edges=edges, mean=mean, err=err, entries=n, titles=tit)
    return res


def merge_hists(per_run):
    """{name: dict(edges, mean (= counts), err, entries, titles, labels)} of the run-summed histograms."""
    res = {}
    for name, (edges, w, w2, tit, lab) in accumulate(per_run, 2).items():
        w, w2 = w[1:-1], w2[1:-1]
        res[name] = dict(edges=edges, mean=w, err=np.sqrt(w2), entries=w, titles=tit, labels=lab)
    return res


def logx(name, xt, edges):
    """Logarithmic x axis for pT axes spanning more than 1.5 decades."""
    return edges[0] > 0 and edges[-1] / edges[0] >= 30 and bool(re.search(r"Pt|pt|p_\{T\}", name + xt))


def axes(label, lumi):
    fig, (ax, axr) = plt.subplots(2, 1, figsize=(10, 10), sharex=True,
                                  gridspec_kw={"height_ratios": [3, 1], "hspace": 0.05})
    PT.cms_label(ax, label, lumi)
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
    PT.save_square(fig, path)


def drop_bottom(fig, ax, axr):
    """Remove the bottom panel and let the main one fill its space, with the x axis it had."""
    top, bot = ax.get_position(), axr.get_position()
    xlabel = axr.get_xlabel()
    fig.delaxes(axr)
    ax.set_position([top.x0, bot.y0, top.width, top.y1 - bot.y0])
    ax.tick_params(axis="x", which="both", labelbottom=True)
    ax.set_xlabel(xlabel, fontsize=PT.AXIS_FS)


def plot(name, data, kind, min_entries, label, lumi, path, norm=False, variants=ORDER, refv=REF, absratio=False,
         absdiff=False, center0=False, ylabel=None, xlabel=None, sel=None, force_diff=False,
         diff_floor=0.5):
    """kind = 'profile' (difference or ratio panel) or 'hist' (ratio panel);
    force_diff: difference panel also for a profile of positive values (e.g. a mass);
    diff_floor: minimum half-range of a difference panel."""
    is_err = kind == "profile" and "Err" in name
    mode = "ratio" if kind == "hist" or is_err else "diff"
    zero = refv is None  # bottom panel: every variant w.r.t. 0
    refv = variants[0] if zero else refv
    ref = data[refv]
    xt, yt = ref["titles"]
    edges = ref["edges"]
    c = 0.5 * (edges[1:] + edges[:-1])
    hw = 0.5 * np.diff(edges)
    lab = ref.get("labels")

    if kind == "hist":
        data = {v: dict(d) for v, d in data.items()}
        if norm:
            for d in data.values():
                s = d["mean"].sum()
                if s > 0:
                    d["mean"], d["err"] = d["mean"] / s, d["err"] / s
            yt = "Fraction of " + (yt.lower() if yt else "entries")
        keep = {v: d["entries"] > 0 for v, d in data.items()}
        yt = yt or "Entries"
    else:
        keep = {v: d["entries"] >= min_entries for v, d in data.items()}
    if not any(k.any() for k in keep.values()):
        return False
    # profiles of positive quantities (errors, resolutions, hit counts) are compared as ratios,
    # the ones crossing zero (dxy, dz, ...) as differences
    positive = kind == "profile" and keep[refv].any() and all(np.all(d["mean"][keep[v]] > 0)
                                                              for v, d in data.items() if keep[v].any())
    if positive and not force_diff:
        mode = "ratio"
    if zero:
        mode = "diff"
    if lab is not None:  # alphanumeric axis: only the filled bins, one unit each
        used = np.flatnonzero(np.any([d["entries"] > 0 for d in data.values()], axis=0))
        c, hw, edges = np.arange(len(used), dtype=float), np.full(len(used), 0.5), np.arange(len(used) + 1) - 0.5
        data = {v: {k: (x[used] if isinstance(x, np.ndarray) and x.shape == d["mean"].shape else x)
                    for k, x in d.items()} for v, d in data.items()}
        keep = {v: k[used] for v, k in keep.items()}
        ref = data[refv]

    fig, ax, axr = axes(label, lumi)
    for v in variants:
        d, st, ok = data[v], STYLE[v], keep[v]
        ax.errorbar(c[ok], d["mean"][ok], xerr=hw[ok], yerr=d["err"][ok], fmt=st["marker"], ms=8 if len(c) <= 60 else 5,
                    color=st["color"], elinewidth=1.5, capsize=0, linewidth=0,
                    label=f"{v} Conditions", zorder=3 if v == refv else 2)
    if kind == "profile" and not is_err and not positive:
        ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_ylabel(ylabel or root2tex(yt), fontsize=PT.AXIS_FS)
    pos = np.concatenate([d["mean"][keep[v]] for v, d in data.items()])
    pos = pos[pos > 0]
    if kind == "hist" and pos.size and pos.max() / pos.min() > 100:
        ax.set_yscale("log")
        lo, hi = pos.min() * 0.5, pos.max()
        ax.set_ylim(lo, hi * (hi / lo) ** 0.6)  # room for CMS label, legend and text
    else:
        lo, hi = ax.get_ylim()
        ax.set_ylim(0 if kind == "hist" else lo, hi + 0.55 * (hi - lo))
    # legend as in the dilepton plots: bold title, reference first, no frame
    handles, names = ax.get_legend_handles_labels()
    order = [names.index(f"{v} Conditions") for v in LEGEND_ORDER if v in variants]
    ax.legend([handles[i] for i in order], [names[i] for i in order], title=TEXT,
              title_fontproperties={"weight": "bold", "size": 18}, fontsize=18, loc="upper right", frameon=False)
    if sel:
        ax.text(0.03, PT.below_label(ax), sel, transform=ax.transAxes, fontsize=15, va="top")

    ok_r = keep[refv]
    yr, er = ref["mean"], np.nan_to_num(ref["err"])
    if zero:
        ok_r, yr, er = np.ones_like(ok_r), np.zeros_like(yr), np.zeros_like(er)
        axr.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
        unit = re.search(r"\(([^)]*)\)\s*$|\[([^\]]*)\]\s*$", yt)
        unit = root2tex(next(g for g in unit.groups() if g)) if unit else ""
        axr.set_ylabel(r"$\Delta$ w.r.t. 0" + (f" [{unit}]" if unit else ""), fontsize=PT.RATIO_FS)
    elif absratio:  # distance from the ideal value 0, relative to the reference
        axr.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(f"|value| / |{refv}|", fontsize=PT.RATIO_FS)
    elif absdiff:  # distance from the ideal value 0, minus the reference one
        mode = "diff"
        axr.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
        unit = re.search(r"\(([^)]*)\)\s*$|\[([^\]]*)\]\s*$", yt)
        unit = root2tex(next(g for g in unit.groups() if g)) if unit else ""
        axr.set_ylabel(f"|value| − |{refv}|" + (f" [{unit}]" if unit else ""), fontsize=PT.RATIO_FS)
    elif mode == "ratio":
        rel = np.divide(er, yr, out=np.zeros_like(yr), where=yr > 0)
        axr.bar(c[ok_r], 2 * rel[ok_r], bottom=1 - rel[ok_r], width=2 * hw[ok_r], color="gray", alpha=0.3,
                label=f"Stat. unc. ({refv})")
        axr.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
        axr.set_ylabel(f"Ratio w.r.t. {refv}", fontsize=PT.AXIS_FS)
    else:
        axr.bar(c[ok_r], 2 * er[ok_r], bottom=-er[ok_r], width=2 * hw[ok_r], color="gray", alpha=0.3,
                label=f"Stat. unc. ({refv})")
        axr.axhline(0.0, color="gray", linestyle="--", alpha=0.5)
        unit = re.search(r"\(([^)]*)\)\s*$|\[([^\]]*)\]\s*$", yt)
        unit = root2tex(next(g for g in unit.groups() if g)) if unit else ""
        axr.set_ylabel(r"$\Delta$ w.r.t. " + refv + (f" [{unit}]" if unit else ""), fontsize=PT.RATIO_FS)
    vals = []
    for v in variants:
        if v == refv and not zero:
            continue
        d = data[v]
        y, e = d["mean"], np.nan_to_num(d["err"])
        ok = ok_r & keep[v]
        if absratio:
            r, re_ = abs_ratio(y, e, yr, er)
        elif absdiff:
            r, re_ = np.abs(y) - np.abs(yr), np.sqrt(e ** 2 + er ** 2)
        elif mode == "ratio":
            r = np.divide(y, yr, out=np.full_like(y, np.nan), where=yr > 0)
            re_ = np.abs(r) * np.sqrt(np.divide(e, y, out=np.zeros_like(y), where=y != 0) ** 2
                              + np.divide(er, yr, out=np.zeros_like(yr), where=yr > 0) ** 2)
        else:
            r, re_ = y - yr, np.sqrt(e ** 2 + er ** 2)
        axr.errorbar(c[ok], r[ok], xerr=hw[ok], yerr=re_[ok], fmt="o", ms=5 if len(c) <= 60 else 3,
                     color=STYLE[v]["color"], elinewidth=1.5, capsize=0, linewidth=0,
                     label=f"|{v}| / |{refv}|" if absratio else f"|{v}| − |{refv}|" if absdiff else None)
        # range from the well-measured points only, so a few empty-ish tail bins do not flatten the panel
        good = ok & (re_ < 0.5 * (1 if mode == "ratio" else max(np.nanmax(np.abs(r[ok])), 1e-9)) if ok.any() else ok)
        vals.append(r[good] if good.any() else r[ok])
    allv = np.concatenate(vals) if vals else np.array([])
    allv = allv[np.isfinite(allv)]
    c0 = 1.0 if mode == "ratio" else 0.0
    span = max(np.max(np.abs(allv - c0)) * 1.3 if allv.size else 0, 0.05 if mode == "ratio" else diff_floor)
    if mode == "ratio":
        span = min(span, 1.0)
    axr.set_ylim(c0 - span, c0 + span)
    if absratio:
        abs_ratio_range(axr, vals)
    if not zero:
        axr.legend(fontsize=14, loc="best")
    axr.set_xlabel(xlabel or root2tex(xt), fontsize=PT.AXIS_FS)
    if lab is not None:
        axr.set_xticks(c, [lab[i] for i in used], rotation=60, ha="right", fontsize=12)
        axr.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    else:
        # zoom on the filled part of the axis
        filled = np.flatnonzero(np.any([keep[v] for v in variants], axis=0))
        x0, x1 = edges[filled[0]], edges[filled[-1] + 1]
        axr.set_xlim(x0, x1)
        if logx(name, xt, edges[filled[0]:filled[-1] + 2]):
            axr.set_xscale("log")
            axr.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
            axr.xaxis.set_minor_locator(matplotlib.ticker.LogLocator(subs=(1, 2, 3, 4, 5, 6, 7, 8, 9)))
            axr.xaxis.set_minor_formatter(matplotlib.ticker.FuncFormatter(
                lambda x, _: f"{x:g}" if round(x / 10 ** np.floor(np.log10(x) + 1e-9)) in (2, 5) else ""))
    if zero:  # a difference w.r.t. 0 is the value itself: no bottom panel
        drop_bottom(fig, ax, axr)
    if center0:  # y axis symmetric around 0
        lo, hi = ax.get_ylim()
        m = max(abs(lo), abs(hi))
        ax.set_ylim(-m, m)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if center0:
        save_square(fig, path)
    else:
        save_square(fig, path)
    plt.close(fig)
    return True


def write_csv(path, data, names, ycol):
    with open(path, "w", newline="") as fo:
        w = csv.writer(fo)
        w.writerow(["variant", "name", "bin", "x_low", "x_high", ycol, "err", "entries"])
        for v in VARIANTS:
            for name in names:
                d = data[v][name]
                for i in range(len(d["mean"])):
                    w.writerow([v, name, i + 1, f"{d['edges'][i]:.6g}", f"{d['edges'][i + 1]:.6g}",
                                f"{d['mean'][i]:.6g}", f"{d['err'][i]:.6g}", f"{d['entries'][i]:.0f}"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-d", "--dqm", default=os.path.join(HERE, ".."))
    ap.add_argument("-o", "--outdir", default=os.path.join(HERE, "plots", "scouting_tracks"))
    ap.add_argument("-r", "--results", default=os.path.join(HERE, "results"))
    ap.add_argument("--folder", default="ScoutingOnline", help='folder under "HLT/Run summary"')
    ap.add_argument("--subdir", default="Tracks", help="directory below --folder, read recursively")
    ap.add_argument("--all-runs", action="store_true", help="ignore results/runs_used.txt")
    ap.add_argument("--min-entries", type=float, default=100, help="minimum entries of a drawn profile bin")
    ap.add_argument("--norm", action="store_true", help="normalise the 1D histograms to unit area")
    ap.add_argument("--only", "--profiles", nargs="*", dest="only",
                    help="only these names (path relative to --subdir, or bare name)")
    ap.add_argument("--label", default="Preliminary", help='CMS label text, e.g. "Preliminary", "Internal", ""')
    ap.add_argument("--lumi", default="1.76",
                    help="integrated luminosity in fb^-1 for the CMS label (recorded, selected runs); '' for none")
    ap.add_argument("-j", "--jobs", type=int, default=8)
    a = ap.parse_args()

    files = {v: {run_of(fn): fn for fn in glob.glob(f"{a.dqm}/scouting/{v}/DQM_scouting_R*.root")} for v in VARIANTS}
    runs = set.intersection(*(set(f) for f in files.values()))
    runlist = os.path.join(a.results, "runs_used.txt")
    if not a.all_runs and os.path.exists(runlist):
        runs &= {int(l.split()[0]) for l in open(runlist) if l.strip()}
    runs = sorted(runs)
    if not runs:
        raise SystemExit("no runs common to all condition sets")
    print(f"{len(runs)} runs ({runs[0]}-{runs[-1]})")

    profs, hists, folders = {}, {}, set()
    with Pool(a.jobs) as pool:
        for v in VARIANTS:
            out = pool.map(read_file, [(files[v][r], a.folder, a.subdir) for r in runs])
            folders |= {o[1] for o in out}
            profs[v] = merge_profiles([o[2] for o in out])
            hists[v] = merge_hists([o[3] for o in out])
    if folders != {a.folder}:
        print(f"NOTE: {a.folder}/{a.subdir} missing in (some) files, used {FALLBACK}/{a.subdir} there")

    def select(data):
        names = sorted(set.intersection(*(set(d) for d in data.values())))
        if a.only:
            names = [n for n in names if n in a.only or n.rsplit("/", 1)[-1] in a.only]
        return names

    hep.style.use("CMS")
    os.makedirs(a.results, exist_ok=True)
    stem = os.path.basename(os.path.normpath(a.outdir))
    for kind, data in (("profile", profs), ("hist", hists)):
        names = select(data)
        done = sum(plot(n, {v: data[v][n] for v in VARIANTS}, kind, a.min_entries, a.label, a.lumi,
                        os.path.join(a.outdir, n), norm=a.norm) for n in names)
        csvpath = os.path.join(a.results, f"{stem}_{kind}s.csv")
        write_csv(csvpath, data, names, "mean" if kind == "profile" else "content")
        print(f"{done}/{len(names)} {kind}s plotted -> {a.outdir}/, {csvpath}")


if __name__ == "__main__":
    main()
