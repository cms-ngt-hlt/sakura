#!/usr/bin/env python3
"""Selected plots, with and without the Prompt conditions, in the style of the other scripts.

  profile_dxyVsPt_pt1            <d_xy>(p_T > 1 GeV) vs p_T, entries-weighted average over runs (plot_profile_averages.py)
  dxyVsEta_pt1_average, _pt10    <d_xy> vs integrated luminosity, |eta| < 2.5 (plot_trends.py)
  dzVsEta_pt1_spread, _pt10      RMS of d_z(eta) vs integrated luminosity (plot_trends.py)
  dxyVsEta_pt1_spread, _pt10     RMS of d_xy(eta) vs integrated luminosity (plot_trends.py)
  dxyVsPhi_pt1_spread, _pt10     RMS of d_xy(phi) vs integrated luminosity (plot_trends.py)
  aggregate_CosPhi3D, _CosPhi    Z -> mu mu vertex pointing-angle distribution (cosphi_aggregate.py)
  dimu_CosPhi3D, dimu_CosPhi     <cos phi> vs integrated luminosity (alignment_trends.py)

with_prompt/   : HLT, NGT, Prompt; bottom panels w.r.t. Prompt (as in the other scripts)
without_prompt/: HLT and NGT only, same colours and markers; bottom panels NGT w.r.t. HLT
*_vs0/          : as above, no comparison panel (a difference w.r.t. 0 is the value itself); the cos phi
                  distributions keep only the unbalance U(x) = N(x) - N(-x) below the distribution
*_absratio/     : bottom panels |value| / |HLT| on a log scale (< 1: closer to the ideal value 0 than HLT);
                  the cos phi distributions are as in *_vs0
*_absdiff/      : bottom panels |value| - |HLT| (< 0: closer to the ideal value 0 than HLT); cos phi distributions
                  as in *_vs0
without_prompt_single/: HLT and NGT, a single square panel, y axis symmetric around 0; the cos phi
                  distributions without the unbalance panel
without_prompt_single_no_outliers/: as without_prompt_single, the year and 3 significant digits in the luminosity label, and the runs whose
                  error is above 3x the median error not drawn in the trends
without_prompt_single_iovs_no_outliers/: without_prompt_single_iovs with the label and the run removal of
                  without_prompt_single_no_outliers
without_prompt_single_iovs/: the trends vs luminosity of without_prompt_single, with dashed lines at the
                  HLT alignment updates (plot_trends.HLT_ALIGNMENT_IOVS); the RMS axes follow the bulk of
                  the points, not the few with large errors

Needs results/runs_used.txt, ip_summary.csv (extract_ip.py, plot_trends.py), alignment_trends.csv (alignment_trends.py).
Usage : make_selected_plots.py [-o plots/selected] [--label Preliminary]
"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import plot_trends as PT  # noqa: E402
import plot_profile_averages as PA  # noqa: E402
import cosphi_aggregate as CA  # noqa: E402
import alignment_trends as AT  # noqa: E402
import cosphi_asymmetry_trend as CAT  # noqa: E402

SETS = {
    "with_prompt": dict(variants=("HLT", "NGT", "Prompt"), ref="Prompt"),
    "without_prompt": dict(variants=("HLT", "NGT"), ref="HLT"),
    "with_prompt_vs0": dict(variants=("HLT", "NGT", "Prompt"), ref=None),
    "without_prompt_vs0": dict(variants=("HLT", "NGT"), ref=None, lumi_3sig=True, year="2026"),
    "with_prompt_absratio": dict(variants=("HLT", "NGT", "Prompt"), ref="HLT", absratio=True),
    "without_prompt_absratio": dict(variants=("HLT", "NGT"), ref="HLT", absratio=True),
    "with_prompt_absdiff": dict(variants=("HLT", "NGT", "Prompt"), ref="HLT", absdiff=True),
    "without_prompt_absdiff": dict(variants=("HLT", "NGT"), ref="HLT", absdiff=True),
    "without_prompt_single": dict(variants=("HLT", "NGT"), ref=None, center0=True, unbalance=False, square=True),
    "without_prompt_single_iovs": dict(variants=("HLT", "NGT"), ref=None, center0=True, unbalance=False, square=True,
                                       vlines=True, lumi_only=True, robust_rms=True),
    "without_prompt_single_iovs_no_outliers": dict(variants=("HLT", "NGT"), ref=None, center0=True, unbalance=False,
                                                   square=True, vlines=True, lumi_only=True, year="2026",
                                                   drop_err=3.0, lumi_3sig=True),
    "without_prompt_single_no_outliers": dict(variants=("HLT", "NGT"), ref=None, center0=True, unbalance=False,
                                              square=True, year="2026", drop_err=3.0, lumi_3sig=True),
}
TREND_IP = [("dxyVsEta_pt1", "average"), ("dxyVsEta_pt10", "average"),
            ("dzVsEta_pt1", "spread"), ("dzVsEta_pt10", "spread"),
            ("dxyVsEta_pt1", "spread"), ("dxyVsEta_pt10", "spread"),
            ("dxyVsPhi_pt1", "spread"), ("dxyVsPhi_pt10", "spread")]
TREND_DIMU = ("dimu_CosPhi3D", "dimu_CosPhi")


def ip_trend(p, runs, xs, prof, col):
    """(data, mode, y label, selection text, zero line) as in plot_trends.make_plots."""
    var, rest = prof.split("Vs")
    x, pt = rest.split("_pt")
    sel = rf"Scouting tracks from the PV, $p_{{T}} > {pt}$ GeV" + (r", $|\eta| < 2.5$" if x == "Eta" else "")
    if col == "average":
        return (PT.series(p, runs, xs, prof, "average", "average_err"), "diff",
                rf"$\langle {PT.VAR_TEX[var]} \rangle$ [$\mu$m]", sel, True)
    return (PT.series(p, runs, xs, prof, "spread", "spread_err"), "ratio",
            rf"RMS of ${PT.VAR_TEX[var]}({PT.X_TEX[x]})$ [$\mu$m]",
            sel + f"\nspread of ${PT.VAR_TEX[var]}$ vs ${PT.X_TEX[x]}$ (statistical part removed)", False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-d", "--dqmdir", default=os.path.join(PT.HERE, ".."))
    ap.add_argument("-i", "--indir", default=os.path.join(PT.HERE, "results"))
    ap.add_argument("-o", "--outdir", default=os.path.join(PT.HERE, "plots", "selected"))
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("--lumifile", default=os.path.join(PT.HERE, "..", "lumi_data.csv"))
    ap.add_argument("--sets", nargs="+", choices=list(SETS), default=list(SETS))
    a = ap.parse_args()
    hep.style.use("CMS")

    runs = [int(l.split()[0]) for l in open(f"{a.indir}/runs_used.txt") if l.strip()]
    lumis = PT.run_lumis(a.lumifile)
    intlumi = sum(lumis[r][1] for r in runs if r in lumis)
    lumi = f"{intlumi:.2f}"
    xs = PT.lumi_axis(runs, lumis)
    print(f"{len(runs)} runs, {lumi} fb^-1")

    # inputs
    p = pd.read_csv(f"{a.indir}/ip_summary.csv")
    al = pd.read_csv(f"{a.indir}/alignment_trends.csv")
    by = {(r.run, r.variant): r for r in al.itertuples()}
    out = [PA.read_file((f"{a.dqmdir}/scouting/{v}/DQM_scouting_R{r:09d}.root", PA.FALLBACK, "Tracks/TracksPV"))
           for v in PA.VARIANTS for r in runs]
    profs = {v: PA.merge_profiles([o[2] for o in out[i * len(runs):(i + 1) * len(runs)]])
             for i, v in enumerate(PA.VARIANTS)}
    cosphi = {name: CA.load(a.dqmdir, runs, name) for name in ("CosPhi3D", "CosPhi")}
    _, _, nn = CAT.run_asymmetry(a.dqmdir, runs, "CosPhi3D")["NGT"]
    npairs = dict(zip(runs, nn))  # Z -> mu mu pairs per run (NGT; the same events in all condition sets)

    for tag in a.sets:
        s = SETS[tag]
        outd = os.path.join(a.outdir, tag)
        os.makedirs(outd, exist_ok=True)
        variants, ref = s["variants"], s["ref"]
        absratio, absdiff = s.get("absratio", False), s.get("absdiff", False)
        center0, unbalance = s.get("center0", False), s.get("unbalance", True)
        square = s.get("square", False)
        vl = PT.iov_lines(runs, lumis) if s.get("vlines") else None
        PT.LABEL_YEAR, drop = s.get("year"), s.get("drop_err")
        lumi = f"{intlumi:.3g}" if s.get("lumi_3sig") else f"{intlumi:.2f}"
        lumi_only = s.get("lumi_only", False)
        # profile vs pT
        if not lumi_only:
            PA.plot("dxyVsPt_pt1", {v: profs[v]["dxyVsPt_pt1"] for v in PA.VARIANTS}, "profile", 100, a.label, lumi,
                    f"{outd}/profile_dxyVsPt_pt1", variants=variants, refv=ref, absratio=absratio,
                    absdiff=absdiff, center0=center0, ylabel=r"$\langle d_{xy} \rangle$ [$\mu$m]",
                    xlabel=r"Track $p_{T}$ [GeV]", sel=r"Scouting tracks from the PV, $p_{T} > 1$ GeV")
        # IP trends vs luminosity
        for prof, col in TREND_IP:
            data, mode, ylab, sel, zero = ip_trend(p, runs, xs, prof, col)
            PT.styled_plot(data, mode, ylab, sel, "lumi", a.label, lumi, f"{outd}/{prof}_{col}", zero_line=zero,
                           variants=variants, ref=ref, absratio=absratio, absdiff=absdiff,
                           center0=center0 and col != "spread", square=square,  # RMS is positive: not centred,
                           ymin0=col == "spread", vlines=vl, drop_err=drop,  # and from 0
                           robust_y=s.get("robust_rms", False) and col == "spread")
        # pointing angle trends vs luminosity
        for group, key, err, mode, ylab, sel, unit, zero in AT.PLOTS:
            if key not in TREND_DIMU:
                continue
            common = [r for r in runs if all(np.isfinite(getattr(by[(r, v)], key)) for v in PT.VARIANTS)
                      and npairs[r] >= CAT.MIN_PAIRS]  # <cos phi> of a run with a handful of pairs: not drawn
            data = {v: (np.array([xs[r] for r in common]), np.array([getattr(by[(r, v)], key) for r in common]),
                        np.array([getattr(by[(r, v)], err) for r in common])) for v in PT.VARIANTS}
            PT.styled_plot(data, mode, ylab, sel, "lumi", a.label, lumi, f"{outd}/{key}", zero_line=zero,
                           unit=unit if unit is not None else "", min_span=(0.002 if unit == "" else None),
                           variants=variants, ref=ref, absratio=absratio, absdiff=absdiff, center0=center0,
                           vlines=vl, drop_err=drop)
        # pointing angle distributions
        for name, (hists, edges) in cosphi.items() if not lumi_only else ():
            CA.plot(name, hists, edges, len(runs), a.label, lumi, f"{outd}/aggregate_{name}",
                    variants=variants, refv=None if absratio or absdiff else ref, unbalance=unbalance)
        print(f"-> {outd}")


if __name__ == "__main__":
    main()
