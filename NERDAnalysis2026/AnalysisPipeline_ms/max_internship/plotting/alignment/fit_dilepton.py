#!/usr/bin/env python3
"""Scouting di-muon Z and J/psi peak position and resolution vs time / run, from the DiLepton DQM folder.

Channels: muons_zMass, muonsNoVtx_zMass (70-110 GeV), muons_jpsiMass, muonsNoVtx_jpsiMass (2.6-3.5 GeV);
"muons" are the scouting muons with a vertex, "muonsNoVtx" the ones without vertex constraint.

Sources (--source):
  nerd   : DQMOutput/scouting/{HLT,Prompt,NGT}/DQM_scouting_R*.root, HLT/Run summary/ScoutingOffline/DiLepton;
           the same events reprocessed with three sets of conditions; runs of results/runs_used.txt
  online : ~/Downloads/NGTDemonstratorDQM/dqm_files/*NGTDemonstrator.root, NGT/Run summary/ScoutingOnline/DiLepton;
           NGT conditions only; runs without EXCLUDE-TRACKING in the online scan, and with pixel hits on tracks

Models (binned Poisson likelihood over the histogram window, numpy only):
  Z     : Breit-Wigner (Gamma_Z = 2.4952 GeV fixed) x double-sided Crystal Ball, + exponential
  J/psi : Crystal Ball (low-mass tail; double-sided if a channel has >= 20000 candidates in total) + exponential;
          Gaussian core if a channel has < 1000 candidates in total
  The tail parameters are fitted once per channel on the sum of all runs and condition sets, then fixed.
  "peak" = BW mass (Z) / CB mean (J/psi); "resolution" = Gaussian core sigma.
Runs with fewer than MIN_POINT candidates are merged with their neighbours (same blocks for all condition sets;
runs with < 5 % of MIN_POINT are left out);
a channel with fewer than 2 x MIN_POINT candidates in total only gets the summed fit.

Usage : fit_dilepton.py --source nerd|online [--label Preliminary]
Writes: <out>/<channel>/{vs_time,vs_run,vs_lumi}/<channel>_{peak,resolution}.{png,pdf} (vs_lumi: nerd only);
        <out>/without_prompt/<channel>/...: the same without the Prompt curve (nerd only);
        <out>/without_prompt_iovs/<channel>/vs_*/...: those trends with the HLT alignment updates as dashed lines, <out>/<channel>/summed_fit.{png,pdf},
        <out>/dilepton_fits.csv, <out>/summary.txt
        (<out> = plots/scouting_dilepton for nerd, ~/Downloads/NGTDemonstratorDQM/results/dilepton for online)
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
from fit_zmumu import dscb, hessian, nelder_mead  # noqa: E402

GZ = 2.4952
CHANNELS = {
    "muons_zMass": dict(kind="Z", tex=r"Z$\rightarrow\mu\mu$, scouting muons (vertex)", ref=91.1876, min_point=800),
    "muonsNoVtx_zMass": dict(kind="Z", tex=r"Z$\rightarrow\mu\mu$, scouting muons (no vertex)", ref=91.1876,
                             min_point=800),
    "muons_jpsiMass": dict(kind="Jpsi", tex=r"J/$\psi\rightarrow\mu\mu$, scouting muons (vertex)", ref=3.0969,
                           min_point=150),
    "muonsNoVtx_jpsiMass": dict(kind="Jpsi", tex=r"J/$\psi\rightarrow\mu\mu$, scouting muons (no vertex)",
                                ref=3.0969, min_point=300),
}
GAUSS_TAIL = (20.0, 20.0, 20.0, 20.0)
NO_PROMPT = ("HLT", "NGT")  # plots without the Prompt curve, w.r.t. HLT (same fits)
SCAN = os.environ.get("NGT_ONLINE_SCAN", os.path.expanduser("~/Downloads/NGTDemonstratorDQM"))  # --source online only


# ---------------------------------------------------------------- input
def _read(args):
    variant, fn, base = args
    run = int(re.search(r"_R0*(\d+)", os.path.basename(fn)).group(1))
    out = {}
    try:
        f = uproot.open(fn)
        d = f[f"DQMData/Run {run}/{base}"]
    except Exception:
        return out
    for ch in CHANNELS:
        if ch in d.keys(cycle=False):
            v, e = d[ch].to_numpy(flow=False)
            out[(run, variant, ch)] = (v.astype(float), e)
    return out


def load(source, dqmdir):
    if source == "nerd":
        jobs = [(v, fn, "HLT/Run summary/ScoutingOffline/DiLepton") for v in PT.VARIANTS
                for fn in sorted(glob.glob(f"{dqmdir}/scouting/{v}/DQM_scouting_R*.root"))]
    else:
        jobs = [("NGT", fn, "NGT/Run summary/ScoutingOnline/DiLepton")
                for fn in sorted(glob.glob(f"{SCAN}/dqm_files/*NGTDemonstrator.root"))]
    hists = {}
    with Pool(8) as pool:
        for h in pool.imap_unordered(_read, jobs):
            hists.update(h)
    return hists


def crop_to_filled(hists, runs, variants, ch):
    """Histograms filled only inside a mass window (empty bins at the edges, e.g. 80-100 GeV of 70-110 GeV
    in newer monitor configurations): crop every run and condition set of the channel to the filled bins,
    dropping the first and last one, which the window cuts through. No-op if the edges are filled."""
    tot = np.sum([hists[(r, v, ch)][0] for r in runs for v in variants], axis=0)
    nz = np.flatnonzero(tot > 0.01 * tot.max())
    if nz.size == 0 or (nz[0] == 0 and nz[-1] == tot.size - 1):
        return
    i0, i1 = nz[0] + 1, nz[-1]  # [i0, i1) excludes the partially filled edge bins
    for key in [k for k in hists if k[2] == ch]:
        vals, edges = hists[key]
        hists[key] = (vals[i0:i1], edges[i0:i1 + 1])
    e = hists[(runs[0], variants[0], ch)][1]
    print(f"{ch}: filled only in {e[0]:.4g}-{e[-1]:.4g}, fit window cropped to it")


def select_runs(source, indir, hists):
    if source == "nerd":
        return [int(l.split()[0]) for l in open(f"{indir}/runs_used.txt") if l.strip()]
    bad = set()
    with open(f"{SCAN}/results/run_exclusion.csv") as f:
        for r in csv.DictReader(f):
            if r["recommendation"] == "EXCLUDE-TRACKING":
                bad.add(int(r["run"]))
    # runs whose tracks have no pixel hits (below the scan's statistics cut, so not in run_exclusion.csv)
    with open(f"{SCAN}/results/metrics.csv") as f:
        for r in csv.DictReader(f):
            try:
                if float(r["pix_mean"]) < 0.5:
                    bad.add(int(r["run"]))
            except (KeyError, ValueError):
                pass
    return sorted({r for r, _, _ in hists} - bad)


# ---------------------------------------------------------------- model
def signal_bins(edges, m0, sigma, tail, width):
    """Bin integrals of [BW(m0, width) x] DSCB(m0, sigma, tail), normalised over the window."""
    w = edges[1] - edges[0]
    step = min(w / 10, sigma / 10)
    span = 12 * sigma + (10 * width if width else 0)
    lo, hi = edges[0] - span, edges[-1] + span
    npt = int(round((hi - lo) / step))
    x = lo + step * (np.arange(npt) + 0.5)
    if width:
        bw = 1 / ((x - m0) ** 2 + width ** 2 / 4)
        half = int(round(min(span, 8 * sigma + 20 * w) / step))
        k = np.arange(-half, half + 1) * step
        g = dscb(k / sigma, *tail)
        pdf = np.convolve(bw, g / g.sum(), mode="same")
    else:
        pdf = dscb((x - m0) / sigma, *tail)
    cdf = np.concatenate([[0], np.cumsum(pdf)])
    xc = lo + step * np.arange(npt + 1)
    b = np.diff(np.interp(edges, xc, cdf))
    return b / b.sum()


def expo_bins(edges, lam):
    t = (edges - edges[0]) / (edges[-1] - edges[0])  # lambda per unit window
    c = -np.exp(-lam * t) / lam if abs(lam) > 1e-6 else t
    b = np.diff(c)
    return b / b.sum()


def tail_of(p, tail, kind):
    """Fixed tail, or free tails from p[5:]: four parameters = double-sided CB, two = low-mass tail only."""
    if tail is not None:
        return tail
    if len(p) >= 9:
        return (np.exp(p[5]), 1 + np.exp(p[6]), np.exp(p[7]), 1 + np.exp(p[8]))
    return (np.exp(p[5]), 1 + np.exp(p[6]), 20.0, 20.0)


def expected(p, edges, tail, kind):
    width = GZ if kind == "Z" else 0.0
    return (np.exp(p[0]) * signal_bins(edges, p[1], np.exp(p[2]), tail_of(p, tail, kind), width)
            + np.exp(p[3]) * expo_bins(edges, p[4]))


def fit(vals, edges, kind, ref, tail=None, two_sided=None):
    """tail=None: fit the tails (double-sided CB if two_sided, default for Z; else low-mass tail only)."""
    if two_sided is None:
        two_sided = kind == "Z"
    y = vals
    f = lambda p: np.sum((mu := np.maximum(expected(p, edges, tail, kind), 1e-9)) - y * np.log(mu))
    tot = y.sum()
    side = max(0.5 * (y[:5].mean() + y[-5:].mean()) * len(y), 1.0)
    s0 = 1.5 if kind == "Z" else 0.03
    p0 = [np.log(max(tot - side, 5)), ref - (0.3 if kind == "Z" else 0.0), np.log(s0), np.log(side), 0.5]
    step = [0.2, 0.3 * s0, 0.2, 0.5, 0.3]
    if tail is None:
        p0 += [np.log(1.2), np.log(2.0)] + ([np.log(1.5), np.log(3.0)] if two_sided else [])
        step += [0.3, 0.3] + ([0.3, 0.3] if two_sided else [])
    p, _ = nelder_mead(f, p0, step)
    for _ in range(2):
        p, _ = nelder_mead(f, p, [s / 4 for s in step])
    n = len(p)
    err = np.full(n, np.nan)
    for h in (1e-3, 3e-3, 1e-2):  # retry with a larger step if the Hessian is not positive definite
        try:
            cov = np.linalg.inv(hessian(f, p, [h] * n))
        except np.linalg.LinAlgError:
            continue
        if np.all(np.diag(cov) > 0):
            err = np.sqrt(np.diag(cov))
            break
        p, _ = nelder_mead(f, p, [s / 10 for s in step])  # not at the minimum yet: polish and retry
    mu = expected(p, edges, tail, kind)
    ok = mu > 0
    chi2 = np.sum((y[ok] - mu[ok]) ** 2 / np.maximum(mu[ok], 1))
    sig = np.exp(p[2])
    return dict(peak=p[1], peak_err=err[1], sigma=sig, sigma_err=sig * err[2], entries=tot, chi2=chi2,
                ndf=int((y > 0).sum()) - n, params=p, tail=tail, tail_params=tail_of(p, tail, kind))


# ---------------------------------------------------------------- run blocks
def blocks(runs, counts, min_point):
    """Group consecutive runs so that every block has >= min_point candidates in every condition set."""
    out, cur = [], []
    floor = max(1.0, 0.05 * min_point)  # runs with (almost) no candidates are left out instead of merged
    for r in runs:
        if min(counts[(r, v)] for v in counts["variants"]) < floor:
            continue
        cur.append(r)
        if min(counts[(r, v)] for v in counts["variants"]) and \
                all(sum(counts[(x, v)] for x in cur) >= min_point for v in counts["variants"]):
            out.append(cur)
            cur = []
    if cur:
        if out:
            out[-1] += cur
        else:
            out.append(cur)
    return out


# ---------------------------------------------------------------- plots
def summed_plot(hs, fits, ch, variants, label, path, nruns):
    info = CHANNELS[ch]
    fig, ax = PT.cms_axes(label)
    for v in variants:
        vals, edges = hs[v]
        ft = fits[v]
        st = PT.STYLE[v]
        c = 0.5 * (edges[1:] + edges[:-1])
        unit = "GeV" if info["kind"] == "Z" else "MeV"
        k = 1 if unit == "GeV" else 1000
        ax.errorbar(c, vals, yerr=np.sqrt(vals), fmt=st["marker"], ms=st["ms"] - 2, color=st["color"],
                    label=f"{st['label']}: m = {k * ft['peak']:.{3 if k == 1 else 1}f} ± "
                          f"{k * ft['peak_err']:.{3 if k == 1 else 1}f}, σ = {k * ft['sigma']:.{3 if k == 1 else 1}f} ± "
                          f"{k * ft['sigma_err']:.{3 if k == 1 else 1}f} {unit}")
        ax.stairs(expected(ft["params"], edges, ft["tail"], info["kind"]), edges, color=st["color"], lw=1.5)
    ax.set_xlabel(r"$m_{\mu\mu}$ [GeV]")
    w = edges[1] - edges[0]
    ax.set_ylabel(f"Candidates / {w * (1 if info['kind'] == 'Z' else 1000):.{2 if info['kind'] == 'Z' else 1}f} "
                  f"{'GeV' if info['kind'] == 'Z' else 'MeV'}")
    ax.set_xlim(edges[0], edges[-1])
    lo, hi = ax.get_ylim()
    ax.set_ylim(0, hi * 1.5)
    ax.legend(loc="upper right", fontsize=12, frameon=False)
    PT.text(ax, info["tex"] + f"\nsum of {nruns} runs")
    fig.savefig(path + ".png", dpi=200, bbox_inches="tight")
    fig.savefig(path + ".pdf", bbox_inches="tight")
    plt.close(fig)


def trend_plot(points, ch, variants, xaxis, label, path_base, grouped):
    info = CHANNELS[ch]
    k = 1.0 if info["kind"] == "Z" else 1000.0
    unit = "GeV" if info["kind"] == "Z" else "MeV"
    for key, err, ylab, ref in (("peak", "peak_err", rf"$m_{{\mu\mu}}$ peak position [{unit}]", info["ref"]),
                                ("sigma", "sigma_err", rf"$m_{{\mu\mu}}$ resolution $\sigma$ [{unit}]", None)):
        fig, ax = PT.cms_axes(label)
        data = {}
        for v in variants:
            pts = points[v]
            data[v] = (np.array([p["x"] for p in pts]), np.array([k * p[key] for p in pts]),
                       np.array([k * p[err] for p in pts]))
        PT.draw(ax, {v: data[v] for v in variants}) if len(variants) > 1 else _draw_single(ax, data[variants[0]],
                                                                                              variants[0])
        if grouped:  # horizontal bars spanning the runs of each block
            for v in variants:
                for p in points[v]:
                    ax.plot([p["x0"], p["x1"]], [k * p[key]] * 2, color=PT.STYLE[v]["color"], lw=1, alpha=0.6)
        if ref:
            ax.axhline(k * ref, color="gray", lw=1, ls="--", zorder=1)
            ax.text(0.99, k * ref, r"PDG ", transform=ax.get_yaxis_transform(), ha="right", va="bottom",
                    fontsize=14, color="gray")
        ax.set_ylabel(ylab)
        txt = info["tex"] + ("\nruns grouped to ≥ %d candidates" % info["min_point"] if grouped else "")
        PT.text(ax, txt)
        PT.finish(fig, ax, xaxis, f"{path_base}_{'peak' if key == 'peak' else 'resolution'}")


def unit_of(kind):
    """(unit, scale from GeV, decimals) for the mass axis and the fit results."""
    return ("GeV", 1.0, 3) if kind == "Z" else ("MeV", 1000.0, 2)


def styled_summed_plot(hs, fits, ch, variants, label, lumi, path, ref=PT.REF):
    """Summed fit in the style of the other plots: fit on top, data / reference below, square frame."""
    info = CHANNELS[ch]
    unit, k, nd = unit_of(info["kind"])
    fig, ax, axr = PT.styled_axes(label, lumi)
    edges = hs[variants[0]][1]
    c, w = 0.5 * (edges[1:] + edges[:-1]), edges[1] - edges[0]
    for v in variants:
        vals, ft, st = hs[v][0], fits[v], PT.STYLE_IP[v]
        ax.errorbar(c, vals, yerr=np.sqrt(vals), fmt=st["marker"], ms=6, color=st["color"], elinewidth=1.2,
                    capsize=0, linewidth=0, zorder=3 if v == ref else 2,
                    label=f"{v} Conditions\n$m$ = {k * ft['peak']:.{nd}f} ± {k * ft['peak_err']:.{nd}f}, "
                          f"$\\sigma$ = {k * ft['sigma']:.{nd}f} ± {k * ft['sigma_err']:.{nd}f} {unit}")
        ax.stairs(expected(ft["params"], edges, ft["tail"], info["kind"]), edges, color=st["color"], lw=1.5)
    ax.set_xlim(edges[0], edges[-1])
    ax.set_ylim(0, ax.get_ylim()[1] * 1.6)
    ax.set_ylabel(f"Candidates / {k * w:.{2 if unit == 'GeV' else 1}f} {unit}", fontsize=PT.AXIS_FS)
    handles, names = ax.get_legend_handles_labels()
    order = [i for v in PT.LEGEND_ORDER_IP for i, nm in enumerate(names) if nm.startswith(f"{v} Conditions")]
    leg = ax.legend([handles[i] for i in order], [names[i] for i in order], title=PT.LEGEND_TITLE, fontsize=14,
                    loc="upper right", frameon=False, title_fontproperties={"weight": "bold", "size": 17})
    txt = ax.text(0.03, PT.below_label(ax), info["tex"], transform=ax.transAxes, fontsize=15, va="top")
    fig.canvas.draw()  # text running into the (wide) legend goes below it, with the data kept underneath
    to_ax = ax.transAxes.inverted()
    lb, tb = leg.get_window_extent().transformed(to_ax), txt.get_window_extent().transformed(to_ax)
    if tb.x1 > lb.x0 and tb.y0 < lb.y1:
        txt.set_y(lb.y0 - 0.02)
        peak = max(np.max(hs[v][0] + np.sqrt(hs[v][0])) for v in variants)
        ax.set_ylim(0, max(ax.get_ylim()[1], peak / (lb.y0 - 0.04 - tb.height)))
    # data / reference, with the reference statistical uncertainty as a band
    nref = hs[ref][0]
    rel = np.divide(np.sqrt(nref), nref, out=np.zeros_like(nref, dtype=float), where=nref > 0)
    axr.stairs(1 + rel, edges, baseline=1 - rel, fill=True, color="gray", alpha=0.3, label=f"Stat. unc. ({ref})")
    axr.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
    for v in variants:
        if v == ref:
            continue
        vals = hs[v][0]
        r = np.divide(vals, nref, out=np.full_like(vals, np.nan, dtype=float), where=nref > 0)
        er = r * np.sqrt(np.divide(1, vals, out=np.zeros_like(r), where=vals > 0)
                         + np.divide(1, nref, out=np.zeros_like(r), where=nref > 0))
        axr.errorbar(c, r, xerr=w / 2, yerr=er, fmt="o", ms=3, color=PT.STYLE_IP[v]["color"], elinewidth=1.2,
                     capsize=0, linewidth=0)
    good = nref > 0.05 * nref.max()  # range from the populated bins
    span = np.nanmax(np.abs(np.concatenate([np.divide(hs[v][0][good], nref[good]) - 1 for v in variants])))
    span = min(max(1.3 * span, 0.02), 0.5)
    axr.set_ylim(1 - span, 1 + span)
    axr.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4, prune="both"))
    axr.set_ylabel(f"Ratio w.r.t. {ref}", fontsize=PT.RATIO_FS)
    axr.set_xlabel(r"$m_{\mu\mu}$ [GeV]", fontsize=PT.AXIS_FS)
    axr.legend(fontsize=13, loc="best", frameon=False)
    PT.save_square(fig, path)
    plt.close(fig)


def styled_trend_plot(points, ch, variants, xaxis, label, lumi, path_base, grouped, ref=PT.REF, vlines=None):
    """Peak and resolution vs time / run / luminosity, in the style of the IP trends (w.r.t. ref)."""
    info = CHANNELS[ch]
    unit, k, _ = unit_of(info["kind"])
    for key, err, ylab, mode, name in (
            ("peak", "peak_err", rf"$m_{{\mu\mu}}$ peak position [{unit}]", "diff", "peak"),
            ("sigma", "sigma_err", rf"$m_{{\mu\mu}}$ resolution $\sigma$ [{unit}]", "ratio", "resolution")):
        data = {}
        for v in variants:
            pts = points[v]
            x = np.array([p["x"] for p in pts])
            row = [x, np.array([k * p[key] for p in pts]), np.array([k * p[err] for p in pts])]
            if grouped and xaxis != "time":  # horizontal bars spanning the runs of each block
                row.append(np.array([[p["x"] - p["x0"] for p in pts], [p["x1"] - p["x"] for p in pts]]))
            data[v] = tuple(row)
        PT.styled_plot(data, mode, ylab, info["tex"], xaxis, label, lumi, f"{path_base}_{name}", unit=unit,
                       variants=variants, ref=ref, vlines=vlines)


def iov_positions(xaxis, runs, lumis, times):
    """[(x, iov)] of the HLT alignment updates inside the run range, on the given x axis."""
    if xaxis == "lumi":
        return PT.iov_lines(runs, lumis)
    out = []
    for iov in PT.HLT_ALIGNMENT_IOVS:
        after = [r for r in sorted(runs) if r >= iov]
        if after and min(runs) < iov:
            out.append((iov if xaxis == "run" else times[after[0]], iov))
    return out


def _draw_single(ax, d, v):
    x, y, e = d
    st = PT.STYLE[v]
    ax.errorbar(x, y, yerr=e, fmt=st["marker"], ms=st["ms"] - 1, color=st["color"], mec="black", mew=0.4,
                elinewidth=0.8, capsize=0, label="NGT demonstrator (online)")


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=("nerd", "online"), default="nerd")
    ap.add_argument("-d", "--dqmdir", default=os.path.join(PT.HERE, ".."))
    ap.add_argument("-i", "--indir", default=os.path.join(PT.HERE, "results"))
    ap.add_argument("-o", "--outdir", default=None)
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("--lumifile", default=os.path.join(PT.HERE, "..", "lumi_data.csv"),
                    help="brilcalc csv: luminosity axis and CMS label (nerd source)")
    a = ap.parse_args()
    hep.style.use("CMS")
    out = a.outdir or (os.path.join(PT.HERE, "plots", "scouting_dilepton") if a.source == "nerd"
                       else f"{SCAN}/results/dilepton")
    os.makedirs(out, exist_ok=True)
    variants = list(PT.VARIANTS) if a.source == "nerd" else ["NGT"]

    hists = load(a.source, a.dqmdir)
    runs = select_runs(a.source, a.indir, hists)
    runs = [r for r in runs if all((r, v, ch) in hists for v in variants for ch in CHANNELS)]
    times, _ = PT.run_times(runs, f"{SCAN}/results/metrics.csv")
    styled = a.source == "nerd"  # HLT / Prompt / NGT comparison: same look as the other plots, plus vs lumi
    lumis = PT.run_lumis(a.lumifile) if styled and os.path.exists(a.lumifile) else {}
    lumi_label = f"{sum(lumis[r][1] for r in runs if r in lumis):.2f}" if lumis else None
    lumi_x = PT.lumi_axis(runs, lumis) if lumis else {}
    rows, summary = [], []
    for ch, info in CHANNELS.items():
        kind = info["kind"]
        crop_to_filled(hists, runs, variants, ch)
        edges = hists[(runs[0], variants[0], ch)][1]
        summed = {v: (np.sum([hists[(r, v, ch)][0] for r in runs], axis=0), edges) for v in variants}
        total = min(s[0].sum() for s in summed.values())
        # common tail parameters (Gaussian core only for very small channels)
        if kind == "Jpsi" and total < 1000:
            tail = GAUSS_TAIL
        else:
            tail = fit(sum(s[0] for s in summed.values()), edges, kind, info["ref"],
                       two_sided=(kind == "Z" or total >= 20000))["tail_params"]
        sfits = {v: fit(summed[v][0], edges, kind, info["ref"], tail) for v in variants}
        os.makedirs(f"{out}/{ch}", exist_ok=True)
        if styled:
            styled_summed_plot(summed, sfits, ch, variants, a.label, lumi_label, f"{out}/{ch}/summed_fit")
            os.makedirs(f"{out}/without_prompt/{ch}", exist_ok=True)
            styled_summed_plot(summed, sfits, ch, NO_PROMPT, a.label, lumi_label,
                               f"{out}/without_prompt/{ch}/summed_fit", ref="HLT")
        else:
            summed_plot(summed, sfits, ch, variants, a.label, f"{out}/{ch}/summed_fit", len(runs))
        line = f"{ch:20s} {int(total):>9d} cand."
        for v in variants:
            ft = sfits[v]
            line += f" | {v}: m={ft['peak']:.4f}±{ft['peak_err']:.4f} s={ft['sigma']:.4f}±{ft['sigma_err']:.4f}"
        summary.append(line)
        print(line)
        if total < 2 * info["min_point"]:
            summary.append(f"{'':20s} too few candidates for a trend: summed fit only")
            continue
        counts = {(r, v): hists[(r, v, ch)][0].sum() for r in runs for v in variants}
        counts["variants"] = variants
        blks = blocks(runs, counts, info["min_point"])
        grouped = any(len(b) > 1 for b in blks)
        points = {v: [] for v in variants}
        for b in blks:
            for v in variants:
                vals = np.sum([hists[(r, v, ch)][0] for r in b], axis=0)
                ft = fit(vals, edges, kind, info["ref"], tail)
                w = np.array([hists[(r, v, ch)][0].sum() for r in b])
                points[v].append(dict(runs=b, **{kk: ft[kk] for kk in ("peak", "peak_err", "sigma", "sigma_err",
                                                                         "entries", "chi2", "ndf")}))
                rows.append(dict(channel=ch, variant=v, first_run=b[0], last_run=b[-1], nruns=len(b),
                                 entries=int(ft["entries"]), peak_GeV=f"{ft['peak']:.5f}",
                                 peak_err_GeV=f"{ft['peak_err']:.5f}", sigma_GeV=f"{ft['sigma']:.5f}",
                                 sigma_err_GeV=f"{ft['sigma_err']:.5f}", chi2=f"{ft['chi2']:.1f}", ndf=ft["ndf"]))
        for xaxis in ("time", "run") + (("lumi",) if lumi_x else ()):
            for v in variants:
                for p in points[v]:
                    b = p["runs"]
                    if xaxis == "time":
                        ts = np.array([times[r].timestamp() for r in b])
                        w = np.array([max(counts[(r, v)], 1) for r in b])
                        from datetime import datetime, timezone
                        conv = lambda t: datetime.fromtimestamp(t, timezone.utc)
                        p["x"], p["x0"], p["x1"] = conv((ts * w).sum() / w.sum()), conv(ts.min()), conv(ts.max())
                    elif xaxis == "lumi":  # candidate-weighted centre; bars over the luminosity of the block
                        w = np.array([max(counts[(r, v)], 1) for r in b])
                        mid = np.array([lumi_x[r] for r in b])
                        p["x"] = (mid * w).sum() / w.sum()
                        p["x0"], p["x1"] = mid[0] - 0.5 * lumis[b[0]][1], mid[-1] + 0.5 * lumis[b[-1]][1]
                    else:
                        w = np.array([max(counts[(r, v)], 1) for r in b])
                        p["x"], p["x0"], p["x1"] = (np.array(b) * w).sum() / w.sum(), b[0], b[-1]
            os.makedirs(f"{out}/{ch}/vs_{xaxis}", exist_ok=True)
            if styled:
                styled_trend_plot(points, ch, variants, xaxis, a.label, lumi_label, f"{out}/{ch}/vs_{xaxis}/{ch}",
                                  grouped)
                os.makedirs(f"{out}/without_prompt/{ch}/vs_{xaxis}", exist_ok=True)
                styled_trend_plot(points, ch, NO_PROMPT, xaxis, a.label, lumi_label,
                                  f"{out}/without_prompt/{ch}/vs_{xaxis}/{ch}", grouped, ref="HLT")
                # the same with the HLT alignment updates, and the year and 3 significant digits in the label
                os.makedirs(f"{out}/without_prompt_iovs/{ch}/vs_{xaxis}", exist_ok=True)
                PT.LABEL_YEAR = "2026"
                styled_trend_plot(points, ch, NO_PROMPT, xaxis, a.label, f"{float(lumi_label):.3g}" if lumi_label else None,
                                  f"{out}/without_prompt_iovs/{ch}/vs_{xaxis}/{ch}", grouped, ref="HLT",
                                  vlines=iov_positions(xaxis, runs, lumis, times))
                PT.LABEL_YEAR = None
            else:
                trend_plot(points, ch, variants, xaxis, a.label, f"{out}/{ch}/vs_{xaxis}/{ch}", grouped)
        summary.append(f"{'':20s} {len(blks)} points" + (" (runs grouped)" if grouped else ""))
    if rows:
        with open(f"{out}/dilepton_fits.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    with open(f"{out}/summary.txt", "w") as f:
        f.write(f"source={a.source}, {len(runs)} runs\n" + "\n".join(summary) + "\n")
    print(f"{len(runs)} runs -> {out}")


if __name__ == "__main__":
    main()
