#!/usr/bin/env python3
"""Aggregate Z -> mu mu vertex pointing distribution, cos(phi_3D) and cos(phi_xy), summed over the selected runs,
for the HLT / Prompt / NGT reprocessings, highlighting the unbalance.

phi is the angle between the PV -> di-muon-vertex displacement and the di-muon momentum
(DiMuonVertexMonitor). For prompt Z decays the vertex displacement is pure resolution, so the distribution is
symmetric in cos(phi); a systematic displacement of the reconstructed vertex along the di-muon direction (e.g.
from a beam-spot or weak-mode bias) makes it asymmetric.

Unbalance, as in DiMuonVertexMonitor::CosPhi3DUnbalance (that histogram is filled with weights +1 / -1, so its
contents sum to zero; rebuilt here from CosPhi3D, bin by bin identical to it):
  U(x) = N(cos phi = x) - N(cos phi = -x),  sigma_U = sqrt(N(x) + N(-x))
Integrated asymmetry: A = (N(cos > 0) - N(cos < 0)) / N,  sigma_A = sqrt((1 - A^2) / N)

Panels: distributions (step + markers), unbalance U(x) normalised to the total (per mille per bin), ratio w.r.t. Prompt.
Usage : cosphi_aggregate.py [--label Preliminary] [--lumi X] [--lumifile lumi_data.csv]
Writes: plots/alignment/dimuon_vertex/aggregate_{CosPhi3D,CosPhi}.{png,pdf}
"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import uproot  # noqa: E402

import plot_trends as PT  # noqa: E402

HIST = "HLT/Run summary/ScoutingOffline/DiMuon/DiMuonVertexMonitor"
XLAB = {"CosPhi3D": r"$\cos\phi_{3D}$", "CosPhi": r"$\cos\phi_{xy}$"}


def load(dqmdir, runs, name):
    out, edges = {}, None
    for v in PT.ORDER_IP:
        tot = None
        for r in runs:
            h = uproot.open(f"{dqmdir}/scouting/{v}/DQM_scouting_R{r:09d}.root")[f"DQMData/Run {r}/{HIST}/{name}"]
            vals, edges = h.to_numpy(flow=False)
            tot = vals.astype(float) if tot is None else tot + vals
        out[v] = tot
    return out, edges


def asymmetry(n, centres):
    pos, neg = n[centres > 0].sum(), n[centres < 0].sum()
    N = pos + neg
    A = (pos - neg) / N
    return A, np.sqrt((1 - A ** 2) / N), N


def plot(name, hists, edges, nruns, label, lumi, path, intlumi=None, variants=PT.ORDER_IP, refv=PT.REF,
         unbalance=True):
    c = 0.5 * (edges[1:] + edges[:-1])
    if refv is None and not unbalance:  # distribution only
        fig, ax = plt.subplots(figsize=(10, 10))
        axu = None
    elif refv is None:  # no ratio panel: the unbalance U(x) is the comparison w.r.t. 0
        fig, (ax, axu) = plt.subplots(2, 1, figsize=(10, 10), sharex=True,
                                      gridspec_kw={"height_ratios": [3, 1.4], "hspace": 0.05})
    else:
        fig, (ax, axu, axr) = plt.subplots(3, 1, figsize=(10, 10), sharex=True,
                                           gridspec_kw={"height_ratios": [3, 1.4, 1], "hspace": 0.05})
    if lumi is None and intlumi is not None:
        lumi = f"{intlumi:.2f}"
    PT.cms_label(ax, label, lumi)

    # ---- distributions
    for v in variants:
        st = PT.STYLE_IP[v]
        n = hists[v]
        A, dA, N = asymmetry(n, c)
        hep.histplot(n, bins=edges, color=st["color"], yerr=False, histtype="step", linewidth=2, ax=ax)
        hep.histplot(n, bins=edges, color=st["color"], marker=st["marker"], markersize=8, yerr=True,
                     histtype="errorbar", linewidth=0, ax=ax,
                     label=f"{v} Conditions\n" + rf"$A = ({100 * A:.2f} \pm {100 * dA:.2f})\%$")
    ax.axvline(0, color="gray", linestyle="--", alpha=0.5)
    ax.set_ylabel(r"Number of $\mu\mu$ pairs [$10^{3}$]", fontsize=PT.AXIS_FS)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y / 1e3:g}"))
    lo, hi = ax.get_ylim()
    ax.set_ylim(0, hi * 1.65)
    leg = ax.legend(fontsize=15, loc="upper right", title="HLT Scouting", title_fontsize=17)
    leg.get_title().set_fontweight("bold")
    ax.text(0.03, PT.below_label(ax), r"Z$\rightarrow\mu\mu$ events" + "\n"
            + r"$A = (N_{\cos>0} - N_{\cos<0})\,/\,N$" + ("\n" + r"$U(x) = N(x) - N(-x)$" if unbalance else ""),
            transform=ax.transAxes, fontsize=19, va="top")

    if axu is None:
        ax.set_xlabel(XLAB[name], fontsize=PT.AXIS_FS)
        ax.set_xlim(edges[0], edges[-1])
        ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))  # -1, -0.5, ... not -1.00
        PT.save_square(fig, path)
        plt.close(fig)
        return

    # ---- unbalance U(x) = N(x) - N(-x), per mille of the total
    for v in variants:
        st = PT.STYLE_IP[v]
        n = hists[v]
        N = n.sum()
        U = n - n[::-1]
        dU = np.sqrt(n + n[::-1])
        axu.errorbar(c, 1e3 * U / N, yerr=1e3 * dU / N, fmt=st["marker"], ms=6, color=st["color"],
                     elinewidth=1.2, capsize=0, linewidth=0)
        axu.stairs(1e3 * U / N, edges, color=st["color"], linewidth=1.2, alpha=0.7)
    axu.axhline(0, color="gray", linestyle="--", alpha=0.5)
    axu.axvline(0, color="gray", linestyle="--", alpha=0.5)
    axu.set_ylabel(r"$U(x)/N$ [‰]", fontsize=PT.RATIO_FS)
    lim = np.nanmax(np.abs(axu.get_ylim()))
    axu.set_ylim(-lim, lim)
    axu.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4, prune="both"))  # no clash at the panel edges
    if refv is None:
        axu.set_xlabel(XLAB[name], fontsize=PT.AXIS_FS)
        axu.set_xlim(edges[0], edges[-1])
        axu.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))  # -1, -0.5, ... not -1.00
        PT.save_square(fig, path)
        plt.close(fig)
        return

    # ---- ratio w.r.t. Prompt
    ref = hists[refv]
    rel = np.divide(np.sqrt(ref), ref, out=np.zeros_like(ref), where=ref > 0)
    axr.fill_between(c, 1 - rel, 1 + rel, step="mid", alpha=0.3, color="gray", label=f"Stat. unc. ({refv})")
    for v in variants:
        if v == refv:
            continue
        n = hists[v]
        r = np.divide(n, ref, out=np.full_like(n, np.nan), where=ref > 0)
        er = r * np.sqrt(np.divide(1, n, out=np.zeros_like(n), where=n > 0)
                         + np.divide(1, ref, out=np.zeros_like(ref), where=ref > 0))
        hep.histplot(r, bins=edges, color=PT.STYLE_IP[v]["color"], yerr=er, histtype="errorbar", marker="_",
                     markersize=12, linewidth=0, markeredgewidth=2, ax=axr)
    axr.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
    axr.set_ylabel(f"Ratio w.r.t. {refv}", fontsize=PT.RATIO_FS)
    axr.set_xlabel(XLAB[name], fontsize=PT.AXIS_FS)
    axr.set_xlim(edges[0], edges[-1])
    axr.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))  # -1, -0.5, ... not -1.00
    dev = np.nanmax(np.abs(np.concatenate([hists[v] / np.where(ref > 0, ref, np.nan) - 1
                                           for v in variants if v != refv])))
    span = max(0.05, 1.3 * dev)
    axr.set_ylim(1 - span, 1 + span)
    axr.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=4, prune="both"))  # no clash at the panel edges
    axr.legend(fontsize=13, loc="best")
    PT.save_square(fig, path)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dqmdir", default=os.path.join(PT.HERE, ".."))
    ap.add_argument("-i", "--indir", default=os.path.join(PT.HERE, "results"))
    ap.add_argument("-o", "--outdir", default=os.path.join(PT.HERE, "plots", "alignment", "dimuon_vertex"))
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("--lumi", default=None)
    ap.add_argument("--lumifile", default=os.path.join(PT.HERE, "..", "lumi_data.csv"), help="brilcalc csv, luminosity per run")
    a = ap.parse_args()
    plt.style.use(hep.style.CMS)
    runs = [int(l.split()[0]) for l in open(f"{a.indir}/runs_used.txt") if l.strip()]
    os.makedirs(a.outdir, exist_ok=True)
    lumis = PT.run_lumis(a.lumifile) if os.path.exists(a.lumifile) else {}
    missing = [r for r in runs if r not in lumis]
    if missing:
        print(f"WARNING: no luminosity for runs {missing}")
    intlumi = sum(lumis[r][1] for r in runs if r in lumis) if lumis else None
    if intlumi is not None:
        print(f"recorded luminosity of the {len(runs)} runs: {intlumi:.3f} fb^-1")
    for name in ("CosPhi3D", "CosPhi"):
        hists, edges = load(a.dqmdir, runs, name)
        c = 0.5 * (edges[1:] + edges[:-1])
        assert np.allclose(c, -c[::-1]), "binning must be symmetric around 0"
        plot(name, hists, edges, len(runs), a.label, a.lumi, f"{a.outdir}/aggregate_{name}",
             intlumi)
        print(name + ":")
        for v in PT.ORDER_IP:
            A, dA, N = asymmetry(hists[v], c)
            print(f"  {v:7s} N={int(N):8d}  A = ({100 * A:+.3f} +- {100 * dA:.3f}) %   <cos> = "
                  f"{(hists[v] * c).sum() / hists[v].sum():+.4f}")
    print(f"-> {a.outdir}/aggregate_*.png")


if __name__ == "__main__":
    main()
