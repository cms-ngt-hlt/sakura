#!/usr/bin/env python3
"""Trends of alignment-sensitive quantities for the HLT / Prompt / NGT reprocessings (scouting DQM files).

Input: DQMOutput/scouting/{HLT,Prompt,NGT}/DQM_scouting_R<run>.root, HLT/Run summary/ScoutingOffline/...;
runs of results/runs_used.txt (tracking problems removed, see plot_trends.py).

1. Z -> mu mu di-muon vertex (DiMuon/DiMuonVertexMonitor): means of cos(phi) / cos(phi_3D) (angle between the
   PV -> di-muon-vertex displacement and the di-muon momentum, ~0 for prompt Z), of the transverse / 3D
   PV-vertex distance and its significance, and of the vertex probability. The distance histograms stop at
   300 um, so those are truncated means.
2. Impact parameters w.r.t. the beam spot (Tracks/TracksBS): sinusoid fit of <d_xy(BS)>(phi) -> (dx, dy) offset of
   the track origin from the beam spot; average and spread of d_xy(BS) vs eta. (d_z(BS) is zero by construction
   in these files, every track is in the central bin, so it is not used.)
3. Z -> mu mu peak and resolution in the barrel and in the endcaps (DiLepton/muons_{barrel,endcap}Mass), and the
   endcap - barrel peak difference (weak modes bias the momentum scale differently with eta). Same fit as
   fit_dilepton.py: BW x double-sided CB + exponential in 70-110 GeV, tails fixed per region.
4. Impact-parameter uncertainties (Tracks/TracksPV/{dxy,dz}ErrVsEta_pt{1,10}): entries-weighted mean for
   |eta| < 2.5; they follow the alignment position errors.

Plots in the same style as plot_trends.py (Prompt as reference: ratio for positive quantities,
difference for quantities that cross zero).
Usage : alignment_trends.py [--label Preliminary] [--lumi X]
Writes: plots/alignment/<group>/{vs_time,vs_run,vs_lumi}/<quantity>.{png,pdf}, results/alignment_trends.csv
"""
import argparse
import csv
import os
import re
from multiprocessing import Pool

import matplotlib

matplotlib.use("Agg")
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import uproot  # noqa: E402

import plot_trends as PT  # noqa: E402
from extract_ip import summarise  # noqa: E402
import fit_dilepton as FD  # noqa: E402

BASE = "HLT/Run summary/ScoutingOffline"
DIMU = ["CosPhi", "CosPhi3D", "VtxDistXY", "VtxDist3D", "VtxDistXYSig", "VtxDist3DSig", "VtxProb"]
BSPROF = {"dxyBS_eta": ("p_dxyBS_vs_eta", 1.0, "Eta")}  # d_z(BS) is ~0 by construction in these files: not used
ERRPROF = [f"{v}ErrVsEta_pt{p}" for v in ("dxy", "dz") for p in (1, 10)]
ZWIN = (70.0, 110.0)


def h_mean(h):
    v, e = h.to_numpy(flow=False)
    c = 0.5 * (e[1:] + e[:-1])
    n = v.sum()
    if n <= 0:
        return np.nan, np.nan
    m = (v * c).sum() / n
    rms = np.sqrt((v * (c - m) ** 2).sum() / n)
    return m, rms / np.sqrt(n)


class Scaled:
    """Wrap a TProfile so that summarise() sees values and errors in other units."""

    def __init__(self, o, k):
        self.o, self.k = o, k

    def values(self, flow=False):
        return self.o.values(flow=flow) * self.k

    def errors(self, flow=False, **kw):
        return self.o.errors(flow=flow, **kw) * self.k

    def member(self, name):
        return self.o.member(name)

    def axis(self):
        return self.o.axis()


def sinus(o, k=1.0):
    v, e = o.values() * k, o.errors() * k
    n = np.asarray(o.member("fBinEntries"), dtype=float)[1:-1]
    edges = o.axis().edges()
    c = 0.5 * (edges[1:] + edges[:-1])
    u = n >= 100
    if u.sum() < 6:
        return {}
    A = np.vstack([np.ones(u.sum()), -np.sin(c[u]), np.cos(c[u])]).T
    W = 1 / np.maximum(e[u], 1e-6) ** 2
    cov = np.linalg.inv(A.T @ (A * W[:, None]))
    p = cov @ (A.T @ (W * v[u]))
    return dict(dx=p[1], dx_err=np.sqrt(cov[1, 1]), dy=p[2], dy_err=np.sqrt(cov[2, 2]))


def process(args):
    variant, run, fn = args
    f = uproot.open(fn)
    top = f"DQMData/Run {run}/{BASE}"
    out = dict(run=run, variant=variant)
    for h in DIMU:
        out[f"dimu_{h}"], out[f"dimu_{h}_err"] = h_mean(f[f"{top}/DiMuon/DiMuonVertexMonitor/{h}"])
    s = sinus(f[f"{top}/Tracks/TracksBS/p_dxyBS_vs_phi"])
    for k, v in s.items():
        out[f"bs_{k}"] = v
    for key, (h, k, x) in BSPROF.items():
        r = summarise(Scaled(f[f"{top}/Tracks/TracksBS/{h}"], k), f"{key}Vs{x}")
        for q in ("average", "average_err", "spread", "spread_err"):
            out[f"{key}_{q}"] = r.get(q, np.nan)
    for h in ERRPROF:
        r = summarise(f[f"{top}/Tracks/TracksPV/{h}"], h)
        out[f"{h}_average"], out[f"{h}_average_err"] = r.get("average", np.nan), r.get("average_err", np.nan)
    hists = {}
    for reg in ("barrel", "endcap"):
        v, e = f[f"{top}/DiLepton/muons_{reg}Mass"].to_numpy(flow=False)
        sel = (e[:-1] >= ZWIN[0] - 1e-6) & (e[1:] <= ZWIN[1] + 1e-6)
        hists[reg] = (v[sel].astype(float), np.append(e[:-1][sel], e[1:][sel][-1]))
    return out, hists


def zfits(rows, hists, runs):
    """Fit the barrel / endcap Z peaks; tail shape per region from the sum of all runs and condition sets."""
    for reg in ("barrel", "endcap"):
        edges = next(iter(hists.values()))[reg][1]
        tot = sum(hists[k][reg][0] for k in hists if k[0] in runs)
        tail = FD.fit(tot, edges, "Z", 91.1876)["tail_params"]
        for r in rows:
            k = (r["run"], r["variant"])
            vals = hists[k][reg][0]
            if vals.sum() < 500:
                continue
            ft = FD.fit(vals, edges, "Z", 91.1876, tail)
            r[f"z_{reg}_peak"], r[f"z_{reg}_peak_err"] = ft["peak"], ft["peak_err"]
            r[f"z_{reg}_sigma"], r[f"z_{reg}_sigma_err"] = ft["sigma"], ft["sigma_err"]
        print(f"  Z {reg}: tails {tuple(round(float(t), 2) for t in tail)}")
    for r in rows:
        if "z_barrel_peak" in r and "z_endcap_peak" in r:
            r["z_ec_minus_b"] = r["z_endcap_peak"] - r["z_barrel_peak"]
            r["z_ec_minus_b_err"] = np.hypot(r["z_endcap_peak_err"], r["z_barrel_peak_err"])


# (group, key, error key, mode, y label, selection text, unit of the difference panel, zero line)
UM = r"$\mu$m"
PLOTS = [
    ("dimuon_vertex", "dimu_CosPhi3D", "dimu_CosPhi3D_err", "diff", r"$\langle\cos\phi_{3D}\rangle$",
     r"Z$\rightarrow\mu\mu$ events", "", True),
    ("dimuon_vertex", "dimu_CosPhi", "dimu_CosPhi_err", "diff", r"$\langle\cos\phi_{xy}\rangle$",
     r"Z$\rightarrow\mu\mu$ events", "", True),
    ("dimuon_vertex", "dimu_VtxDistXY", "dimu_VtxDistXY_err", "ratio", rf"$\langle d_{{xy}}$(PV, $\mu\mu$ vtx)$\rangle$ [{UM}]",
     r"Z$\rightarrow\mu\mu$ vertex, transverse distance to the PV (< 300 $\mu$m)", None, False),
    ("dimuon_vertex", "dimu_VtxDist3D", "dimu_VtxDist3D_err", "ratio", rf"$\langle d_{{3D}}$(PV, $\mu\mu$ vtx)$\rangle$ [{UM}]",
     r"Z$\rightarrow\mu\mu$ vertex, 3D distance to the PV (< 300 $\mu$m)", None, False),
    ("dimuon_vertex", "dimu_VtxDistXYSig", "dimu_VtxDistXYSig_err", "ratio", r"$\langle d_{xy}/\sigma\rangle$",
     r"Z$\rightarrow\mu\mu$ vertex, transverse distance significance", None, False),
    ("dimuon_vertex", "dimu_VtxDist3DSig", "dimu_VtxDist3DSig_err", "ratio", r"$\langle d_{3D}/\sigma\rangle$",
     r"Z$\rightarrow\mu\mu$ vertex, 3D distance significance", None, False),
    ("dimuon_vertex", "dimu_VtxProb", "dimu_VtxProb_err", "ratio", r"$\langle$vertex prob.$\rangle$",
     r"Z$\rightarrow\mu\mu$ vertex fit probability", None, False),
    ("ip_beamspot", "bs_dx", "bs_dx_err", "diff", rf"$\Delta x$ of track origin w.r.t. BS [{UM}]",
     r"Scouting tracks, fit $d_{xy}^{BS}(\phi) = a - \Delta x\sin\phi + \Delta y\cos\phi$", UM, True),
    ("ip_beamspot", "bs_dy", "bs_dy_err", "diff", rf"$\Delta y$ of track origin w.r.t. BS [{UM}]",
     r"Scouting tracks, fit $d_{xy}^{BS}(\phi) = a - \Delta x\sin\phi + \Delta y\cos\phi$", UM, True),
    ("ip_beamspot", "dxyBS_eta_average", "dxyBS_eta_average_err", "diff", rf"$\langle d_{{xy}}^{{BS}}\rangle$ [{UM}]",
     r"Scouting tracks, $d_{xy}$ w.r.t. beam spot, $|\eta| < 2.5$", UM, True),
    ("ip_beamspot", "dxyBS_eta_spread", "dxyBS_eta_spread_err", "ratio", rf"RMS of $d_{{xy}}^{{BS}}(\eta)$ [{UM}]",
     r"Scouting tracks, spread of $d_{xy}^{BS}$ vs $\eta$, $|\eta| < 2.5$", None, False),
    ("zmass_regions", "z_barrel_peak", "z_barrel_peak_err", "diff", r"$m_{\mu\mu}$ peak, barrel [GeV]",
     r"Z$\rightarrow\mu\mu$, scouting muons, barrel", "GeV", False),
    ("zmass_regions", "z_endcap_peak", "z_endcap_peak_err", "diff", r"$m_{\mu\mu}$ peak, endcap [GeV]",
     r"Z$\rightarrow\mu\mu$, scouting muons, endcap", "GeV", False),
    ("zmass_regions", "z_ec_minus_b", "z_ec_minus_b_err", "diff", r"$m_{\mu\mu}^{endcap} - m_{\mu\mu}^{barrel}$ [GeV]",
     r"Z$\rightarrow\mu\mu$ peak, endcap $-$ barrel", "GeV", True),
    ("zmass_regions", "z_barrel_sigma", "z_barrel_sigma_err", "ratio", r"$m_{\mu\mu}$ resolution $\sigma$, barrel [GeV]",
     r"Z$\rightarrow\mu\mu$, scouting muons, barrel", None, False),
    ("zmass_regions", "z_endcap_sigma", "z_endcap_sigma_err", "ratio", r"$m_{\mu\mu}$ resolution $\sigma$, endcap [GeV]",
     r"Z$\rightarrow\mu\mu$, scouting muons, endcap", None, False),
] + [("ip_errors", f"{h}_average", f"{h}_average_err", "ratio",
      rf"$\langle\sigma({PT.VAR_TEX[h[:h.index('Err')]]})\rangle$ [{UM}]",
      rf"Scouting tracks from the PV, $p_T > {h.split('_pt')[1]}$ GeV, $|\eta| < 2.5$", None, False)
     for h in ERRPROF]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dqmdir", default=os.path.join(PT.HERE, ".."))
    ap.add_argument("-i", "--indir", default=os.path.join(PT.HERE, "results"))
    ap.add_argument("-o", "--outdir", default=os.path.join(PT.HERE, "plots", "alignment"))
    ap.add_argument("--metrics", default=f"{PT.SCAN}/metrics.csv")
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("--lumi", default=None, help="fb^-1 for the CMS label, or 'auto' (selected runs, from --lumifile)")
    ap.add_argument("--lumifile", default=os.path.join(PT.HERE, "..", "lumi_data.csv"), help="brilcalc csv, luminosity per run")
    a = ap.parse_args()
    hep.style.use("CMS")

    runs = [int(l.split()[0]) for l in open(f"{a.indir}/runs_used.txt") if l.strip()]
    jobs = [(v, r, f"{a.dqmdir}/scouting/{v}/DQM_scouting_R{r:09d}.root") for v in PT.VARIANTS for r in runs]
    rows, hists = [], {}
    with Pool(8) as pool:
        for out, h in pool.imap_unordered(process, jobs):
            rows.append(out)
            hists[(out["run"], out["variant"])] = h
    rows.sort(key=lambda r: (r["run"], PT.VARIANTS.index(r["variant"])))
    zfits(rows, hists, runs)

    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(f"{a.indir}/alignment_trends.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    times, _ = PT.run_times(runs, a.metrics)
    by = {(r["run"], r["variant"]): r for r in rows}
    lumis = PT.run_lumis(a.lumifile) if os.path.exists(a.lumifile) else {}
    xaxes = ("time", "run", "lumi") if lumis else ("time", "run")
    if a.lumi == "auto":
        a.lumi = f"{sum(lumis[r][1] for r in runs if r in lumis):.2f}" if lumis else None
    for xaxis in xaxes:
        xs = times if xaxis == "time" else PT.lumi_axis(runs, lumis) if xaxis == "lumi" else {r: r for r in runs}
        for group, key, err, mode, ylab, sel, unit, zero in PLOTS:
            common = [r for r in runs if all(np.isfinite(by[(r, v)].get(key, np.nan)) for v in PT.VARIANTS)]
            if not common:
                continue
            data = {v: (np.array([xs[r] for r in common]), np.array([by[(r, v)][key] for r in common]),
                        np.array([by[(r, v)].get(err, np.nan) for r in common])) for v in PT.VARIANTS}
            outd = f"{a.outdir}/{group}/vs_{xaxis}"
            os.makedirs(outd, exist_ok=True)
            PT.styled_plot(data, mode, ylab, sel, xaxis, a.label, a.lumi, f"{outd}/{key}", zero_line=zero,
                           unit=unit if unit is not None else "", min_span=(0.002 if unit == "" else None))
    # medians per condition set, for the README
    print(f"{len(runs)} runs; medians (HLT / Prompt / NGT):")
    for _, key, _, _, _, _, _, _ in PLOTS:
        med = [np.nanmedian([by[(r, v)].get(key, np.nan) for r in runs]) for v in PT.VARIANTS]
        print(f"  {key:28s} " + " / ".join(f"{m:.4g}" for m in med))
    print(f"-> {a.outdir}, {a.indir}/alignment_trends.csv")


if __name__ == "__main__":
    main()
