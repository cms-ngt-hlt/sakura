#!/usr/bin/env python3
"""Per-run asymmetry of the Z -> mu mu vertex pointing distribution vs cumulative integrated luminosity.

  A = (N(cos phi > 0) - N(cos phi < 0)) / N,  sigma_A = sqrt((1 - A^2) / N)

from the CosPhi3D / CosPhi histograms of DiMuonVertexMonitor, run by run, for the HLT / Prompt / NGT
reprocessings (the same quantity quoted in the legend of aggregate_CosPhi*.png, there over all runs).

Writes, in the style of the other trend plots:
  plots/alignment/dimuon_vertex/vs_lumi/dimu_CosPhi{3D,}_asym   all conditions, bottom panel w.r.t. Prompt
  plots/selected/<set>/dimu_CosPhi{3D,}_asym                    one per set of make_selected_plots.SETS
Usage : cosphi_asymmetry_trend.py [--label Preliminary]
"""
import argparse
import os

import matplotlib

matplotlib.use("Agg")
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import uproot  # noqa: E402

import plot_trends as PT  # noqa: E402
import cosphi_aggregate as CA  # noqa: E402
import make_selected_plots as MS  # noqa: E402

MIN_PAIRS = 1000
TEX = {"CosPhi3D": r"\cos\phi_{3D}", "CosPhi": r"\cos\phi_{xy}"}


def run_asymmetry(dqmdir, runs, name):
    """{variant: (A, sigma_A, N) arrays over runs}, in percent."""
    out = {}
    for v in PT.ORDER_IP:
        A, dA, N = [], [], []
        for r in runs:
            h = uproot.open(f"{dqmdir}/scouting/{v}/DQM_scouting_R{r:09d}.root")[f"DQMData/Run {r}/{CA.HIST}/{name}"]
            n, edges = h.to_numpy(flow=False)
            a, da, nn = CA.asymmetry(n.astype(float), 0.5 * (edges[1:] + edges[:-1])) if n.sum() >= MIN_PAIRS else (
                np.nan, np.nan, 0)  # too few pairs: A meaningless (sigma_A > 3%), run not drawn
            A.append(100 * a)
            dA.append(100 * da)
            N.append(nn)
        out[v] = tuple(np.array(x, float) for x in (A, dA, N))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-d", "--dqmdir", default=os.path.join(PT.HERE, ".."))
    ap.add_argument("-i", "--indir", default=os.path.join(PT.HERE, "results"))
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("--lumifile", default=os.path.join(PT.HERE, "..", "lumi_data.csv"))
    a = ap.parse_args()
    hep.style.use("CMS")

    runs = [int(l.split()[0]) for l in open(f"{a.indir}/runs_used.txt") if l.strip()]
    lumis = PT.run_lumis(a.lumifile)
    lumi = f"{sum(lumis[r][1] for r in runs if r in lumis):.2f}"
    xs = PT.lumi_axis(runs, lumis)
    x = np.array([xs[r] for r in runs])

    for name in ("CosPhi3D", "CosPhi"):
        asym = run_asymmetry(a.dqmdir, runs, name)
        for v, (A, dA, N) in asym.items():
            tot = np.nansum(A / 100 * N) / N.sum()
            print(f"{name:9s} {v:7s} per-run A: median {np.nanmedian(A):+.2f}%, N-weighted {100 * tot:+.2f}%")
        data = {v: (x, A, dA) for v, (A, dA, _) in asym.items()}
        ylab = rf"Asymmetry of ${TEX[name]}$ [%]"
        sel = (r"Z$\rightarrow\mu\mu$ events" + "\n"
               + rf"$A = (N_{{{TEX[name]} > 0}} - N_{{{TEX[name]} < 0}})\,/\,N$")
        outd = os.path.join(PT.HERE, "plots", "alignment", "dimuon_vertex", "vs_lumi")
        os.makedirs(outd, exist_ok=True)
        PT.styled_plot(data, "diff", ylab, sel, "lumi", a.label, lumi, f"{outd}/dimu_{name}_asym", zero_line=True,
                       unit="%", min_span=1.0)
        for tag, s in MS.SETS.items():
            outd = os.path.join(PT.HERE, "plots", "selected", tag)
            PT.LABEL_YEAR = s.get("year")
            os.makedirs(outd, exist_ok=True)
            PT.styled_plot(data, "diff", ylab, sel, "lumi", a.label, f"{float(lumi):.3g}" if s.get("lumi_3sig") else lumi,
                           f"{outd}/dimu_{name}_asym", zero_line=True,
                           unit="%", min_span=1.0, variants=s["variants"], ref=s["ref"],
                           absratio=s.get("absratio", False), absdiff=s.get("absdiff", False),
                           center0=s.get("center0", False), square=s.get("square", False),
                           vlines=PT.iov_lines(runs, lumis) if s.get("vlines") else None,
                           drop_err=s.get("drop_err"))
    print("-> plots/alignment/dimuon_vertex/vs_lumi, plots/selected/*")


if __name__ == "__main__":
    main()
