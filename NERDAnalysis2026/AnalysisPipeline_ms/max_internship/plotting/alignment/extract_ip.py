#!/usr/bin/env python3
"""Summaries of the scouting PV-track impact-parameter profiles for the HLT / Prompt / NGT reprocessings.

Input : DQMOutput/scouting/{HLT,Prompt,NGT}/DQM_scouting_R<run>.root
        (HLT/Run summary/ScoutingOffline/Tracks/TracksPV/{dxy,dz}Vs{Eta,Phi}_pt{1,10})
Output: results/ip_summary.csv  one row per (run, variant, profile)
        results/quality.csv     one row per (run, variant): events, tracks, layers / off-layers per track

Per profile:
  average  = entries-weighted mean of the bin contents (um), with statistical error
  spread   = RMS of the bin contents with the statistical part removed, sqrt(RMS^2 - <err^2>) (um),
             with its error propagated from the bin errors
  sin_dx, sin_dy (dxy vs phi only) = fit dxy(phi) = a - dx sin(phi) + dy cos(phi) (um): transverse offset of
             the track origin from the reference point (the scouting PV)
Bins with < MIN_BIN entries, and eta bins outside |eta| < ETA_MAX, are not used.
(The DQMOutput/hlt files do not contain these profiles.)

Usage: extract_ip.py [-d ../DQMOutput] [-o results]
"""
import argparse
import csv
import glob
import os
import re
from multiprocessing import Pool

import numpy as np
import uproot

VARIANTS = ("HLT", "Prompt", "NGT")
PROFILES = [f"{v}Vs{x}_pt{p}" for v in ("dxy", "dz") for x in ("Eta", "Phi") for p in (1, 10)]
BASE = "HLT/Run summary/ScoutingOffline/Tracks"
MIN_BIN = 100
ETA_MAX = 2.5


def entries(o):
    return np.asarray(o.member("fBinEntries"), dtype=float)[1:-1]


def summarise(o, name):
    v, n, e = o.values(flow=False), entries(o), o.errors(flow=False)
    edges = o.axis().edges()
    c = 0.5 * (edges[1:] + edges[:-1])
    use = n >= MIN_BIN
    if "Eta" in name:
        use &= np.abs(c) < ETA_MAX
    out = dict(entries=n.sum(), nbins=int(use.sum()))
    if use.sum() < 3:
        return out
    w = n[use]
    raw = np.std(v[use])
    spread = np.sqrt(max(0.0, raw ** 2 - np.mean(e[use] ** 2)))
    # error on the spread from the bin errors: dS/dv_i = (v_i - <v>) / (N S)
    d = v[use] - v[use].mean()
    spread_err = np.sqrt((d ** 2 * e[use] ** 2).sum()) / (use.sum() * spread) if spread > 0 else np.nan
    out.update(average=(w * v[use]).sum() / w.sum(), average_err=np.sqrt((w ** 2 * e[use] ** 2).sum()) / w.sum(),
               spread=spread, spread_err=spread_err, spread_raw=raw, vmin=v[use].min(), vmax=v[use].max())
    if "Phi" in name and use.sum() >= 6:
        A = np.vstack([np.ones(use.sum()), -np.sin(c[use]), np.cos(c[use])]).T
        W = 1 / np.maximum(e[use], 1e-6) ** 2
        cov = np.linalg.inv(A.T @ (A * W[:, None]))
        p = cov @ (A.T @ (W * v[use]))
        out.update(sin_a=p[0], sin_dx=p[1], sin_dy=p[2], sin_dx_err=np.sqrt(cov[1, 1]), sin_dy_err=np.sqrt(cov[2, 2]))
    return out


def h1_mean(o):
    v, e = o.to_numpy(flow=False)
    return (v * 0.5 * (e[1:] + e[:-1])).sum() / v.sum() if v.sum() > 0 else np.nan, v.sum()


def process(args):
    variant, fn = args
    run = int(re.search(r"_R0*(\d+)\.root$", fn).group(1))
    f = uproot.open(fn)
    top = f"DQMData/Run {run}/{BASE}"
    prof = []
    for name in PROFILES:
        try:
            o = f[f"{top}/TracksPV/{name}"]
        except KeyError:
            continue
        prof.append(dict(run=run, variant=variant, profile=name, **summarise(o, name)))
    q = dict(run=run, variant=variant)
    for key, h in (("layers", "HitProperties/NumberOfLayersPerTrack_ScoutingTk"),
                   ("off_layers", "HitProperties/NumberOfOffLayersPerTrack_ScoutingTk"),
                   ("missing_layers", "HitProperties/NumberOfMissingLayersPerTrack_ScoutingTk"),
                   ("valid_hits", "HitProperties/NumberOfValidRecHitsPerTrack_ScoutingTk"),
                   ("tracks_per_event", "GeneralProperties/NumberOfTracks_ScoutingTk")):
        try:
            q[key], n = h1_mean(f[f"{top}/{h}"])
            if key == "tracks_per_event":
                q["events"] = n
        except KeyError:
            q[key] = np.nan
    try:  # pixel layers per track from the (eta, phi) profile
        o = f[f"{top}/HitProperties/NumberOfPixelLayersVsPhiVsEtaPerTrack_ScoutingTk"]
        nx, ny = o.member("fXaxis").member("fNbins"), o.member("fYaxis").member("fNbins")
        n = np.asarray(o.member("fBinEntries"), dtype=float).reshape(ny + 2, nx + 2).T[1:-1, 1:-1]
        q["pixel_layers"] = (o.values(flow=False) * n).sum() / n.sum()
    except KeyError:
        q["pixel_layers"] = np.nan
    return prof, q


def write(path, rows):
    cols = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("-d", "--dqmdir", default=os.path.join(here, ".."))
    ap.add_argument("-o", "--outdir", default=os.path.join(here, "results"))
    ap.add_argument("-j", "--jobs", type=int, default=8)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    jobs = [(v, fn) for v in VARIANTS for fn in sorted(glob.glob(f"{a.dqmdir}/scouting/{v}/DQM_scouting_R*.root"))]
    prof, qual = [], []
    with Pool(a.jobs) as pool:
        for p, q in pool.imap_unordered(process, jobs):
            prof += p
            qual.append(q)
    key = lambda r: (r["run"], VARIANTS.index(r["variant"]), r.get("profile", ""))
    write(f"{a.outdir}/ip_summary.csv", sorted(prof, key=key))
    write(f"{a.outdir}/quality.csv", sorted(qual, key=key))
    print(f"{len(jobs)} files -> {a.outdir}/ip_summary.csv ({len(prof)} rows), quality.csv ({len(qual)} rows)")


if __name__ == "__main__":
    main()
