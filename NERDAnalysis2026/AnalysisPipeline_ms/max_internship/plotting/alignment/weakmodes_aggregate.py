#!/usr/bin/env python3
"""Aggregate of the ScoutingOffline/{DiMuon,DiMuonJpsi}/DiMuonAlignmentMonitor folders over the selected runs,
for the HLT / Prompt / NGT reprocessings, in the style of the IP analysis (../../IPAnalysis/analysis).

Input : <dqmdir>/scouting/{HLT,Prompt,NGT}/DQM_scouting_R<run>.root (default: plotting/), runs of results/runs_used.txt
TH1          summed over runs
TProfile(2D) entries-weighted average over runs (sums of w*y, w*y^2 and w are added, then the mean is taken)
TH2 mass vs x  summed over runs, then one mass fit per x bin, giving the peak and the width vs x:
    Z     : Breit-Wigner (Gamma_Z fixed) x double-sided Crystal Ball + exponential
    J/psi : double-sided Crystal Ball + exponential
    The tails are fitted on the sum of the condition sets, then fixed in the fit of each one, so that the condition
    sets are compared with the same shape: per folder (sum of all x bins) for the Z, where the mass window leaves too
    few bins to constrain them slice by slice; per x bin for the J/psi, whose resolution changes by a factor 3 with
    eta (per folder for slices below MIN_SLICE_TAILS candidates). "Width" is the Gaussian core sigma. Bins at the edge of a mass window imposed upstream (Z: 80-100 GeV) are left out of the fit.

Writes: plots/<folder>/<set>/{hists,profiles,mass_fits,maps}/*.{png,pdf}, set = with_prompt (w.r.t. Prompt),
        without_prompt (HLT and NGT, w.r.t. HLT); plots/<folder>/fit_qa/<hist>_<variant>.png (the fit of every slice);
        results/<folder>_{hists,profiles}.csv, results/<folder>_mass_fits.csv
Usage : weakmodes_aggregate.py [--label Preliminary] [-j 8]
"""
import argparse
import csv
import os
import re
import sys
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
IP = os.path.join(HERE, "..")  # directory holding scouting/{HLT,Prompt,NGT}
sys.path.insert(0, HERE)

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import uproot  # noqa: E402

import fit_dilepton as FD  # noqa: E402
import plot_profile_averages as PA  # noqa: E402
import plot_trends as PT  # noqa: E402

BASE = "ScoutingOffline"
SUB = "DiMuonAlignmentMonitor"
FOLDERS = {
    "DiMuon": dict(kind="Z", ref=91.1876, sel=r"Z$\rightarrow\mu\mu$ events", slice_tails=False,
                   model=r"Fit: BW $\otimes$ double-sided CB + exp.", floor_peak=0.05, floor_mass=0.05),
    "DiMuonJpsi": dict(kind="Jpsi", ref=3.0969, sel=r"J/$\psi\rightarrow\mu\mu$ events", slice_tails=True,
                       model="Fit: double-sided CB + exp.", floor_peak=0.5, floor_mass=0.002),
}
SETS = {
    "with_prompt": dict(variants=("HLT", "NGT", "Prompt"), ref="Prompt"),
    "without_prompt": dict(variants=("HLT", "NGT"), ref="HLT"),
}
# mass_fits folders with the year and 3 significant digits in the luminosity label: "11.9 fb^-1, 2026 (13.6 TeV)"
MASS_FIT_YEAR = {("DiMuon", "without_prompt"): "2026"}
MIN_FIT = 300  # candidates in a slice to attempt a fit
MIN_SLICE_TAILS = 30000  # candidates (sum of the condition sets) to fit the tails of a slice


def clean(t):
    """DQM titles written with <...>: '<x [u]>' -> mean of x in [u], '<x>' -> mean of x, as ROOT TLatex."""
    t = re.sub(r"<([^<>]*?) \[([^\]]*)\]>", r"#LT\1#GT [\2]", t)
    return re.sub(r"<([^<>]*)>", r"#LT\1#GT", t)


def flat2d(a, nx, ny):
    """ROOT global-bin array -> [ix, iy], flow bins included."""
    return np.asarray(a, dtype=float).reshape(nx + 2, ny + 2, order="F")


def read_2d(fn, run, folder):
    """TH2: {name: (xedges, yedges, counts, titles)}; TProfile2D: {name: (xedges, yedges, sum_wy, sum_wy2, n, titles)}."""
    d = uproot.open(fn)[f"DQMData/Run {run}/HLT/Run summary/{BASE}/{folder}/{SUB}"]
    th2, tp2 = {}, {}
    for key, cls in d.classnames().items():
        name = key.split(";")[0]
        if cls not in ("TH2F", "TH2D", "TProfile2D"):
            continue
        o = d[key]
        xe, ye = o.axes[0].edges(), o.axes[1].edges()
        tit = tuple(o.member(a).member("fTitle") for a in ("fXaxis", "fYaxis", "fZaxis"))
        if cls == "TProfile2D":
            n = flat2d(o.member("fBinEntries"), len(xe) - 1, len(ye) - 1)
            tp2[name] = (xe, ye, o.values(flow=True) * n, flat2d(o.member("fSumw2"), len(xe) - 1, len(ye) - 1), n, tit)
        else:
            th2[name] = (xe, ye, o.values(flow=True).astype(float), tit)
    return th2, tp2


def read_one(args):
    v, run, folder, dqm = args
    fn = f"{dqm}/scouting/{v}/DQM_scouting_R{run:09d}.root"
    _, _, prof, hist = PA.read_file((fn, BASE, f"{folder}/{SUB}"))
    th2, tp2 = read_2d(fn, run, folder)
    return v, folder, prof, hist, th2, tp2


def add_nd(acc, per_run, nsum):
    """Sum the arrays at positions 2..1+nsum of every (xedges, yedges, arrays..., titles) entry."""
    for name, t in per_run.items():
        if name not in acc:
            acc[name] = list(t[:2]) + [x.copy() for x in t[2:2 + nsum]] + list(t[2 + nsum:])
        else:
            for i in range(2, 2 + nsum):
                acc[name][i] = acc[name][i] + t[i]


def fit_window(tot):
    """[i0, i1) of the mass bins to fit: bins around an upstream window (empty edges) and the ones it cuts are left out."""
    nz = np.flatnonzero(tot > 0.01 * tot.max())
    return (0, tot.size) if nz[0] == 0 and nz[-1] == tot.size - 1 else (nz[0] + 1, nz[-1])


def fit_slice(job):
    key, vals, edges, kind, ref, tail = job
    try:
        return key, FD.fit(vals, edges, kind, ref, tail, two_sided=True)
    except (ValueError, FloatingPointError, np.linalg.LinAlgError):
        return key, None


def fit_mass(folder, th2, jobs_n):
    """{name: {variant: {slice index: fit}}}, xedges, mass edges of the fit, counts of the fit window, tail parameters."""
    info = FOLDERS[folder]
    any_name = sorted(th2)[0]
    projection = sum(th2[any_name][v][2][1:-1, 1:-1].sum(axis=0) for v in PA.VARIANTS)
    i0, i1 = fit_window(projection)
    medges = th2[any_name][PA.VARIANTS[0]][1][i0:i1 + 1]
    tail = FD.fit(projection[i0:i1], medges, info["kind"], info["ref"], two_sided=True)["tail_params"]
    print(f"{folder}: fit window {medges[0]:.4g}-{medges[-1]:.4g} GeV, {i1 - i0} bins; tails " +
          ", ".join(f"{x:.2f}" for x in tail))
    windowed = {(name, v): per_v[v][2][1:-1, 1:-1][:, i0:i1] for name, per_v in th2.items() for v in PA.VARIANTS}
    tail_jobs = []
    if info["slice_tails"]:
        for name in th2:
            total = sum(windowed[(name, v)] for v in PA.VARIANTS)
            for i in np.flatnonzero(total.sum(axis=1) >= MIN_SLICE_TAILS):
                tail_jobs.append(((name, int(i)), total[i], medges, info["kind"], info["ref"], None))
    jobs, fits = [], {}
    with Pool(jobs_n) as pool:
        slice_tail = {k: ft["tail_params"] for k, ft in pool.imap_unordered(fit_slice, tail_jobs, chunksize=2)
                      if ft is not None}
        for (name, v), counts in windowed.items():
            for i in np.flatnonzero(counts.sum(axis=1) >= MIN_FIT):
                jobs.append(((name, v, int(i)), counts[i], medges, info["kind"], info["ref"],
                             slice_tail.get((name, int(i)), tail)))
        for key, ft in pool.imap_unordered(fit_slice, jobs, chunksize=4):
            fits[key] = ft
    return fits, medges, windowed


def fit_results(name, per_v, fits, kind, windowed):
    """{variant: (peak dict, width dict)} in the format of plot_profile_averages.plot."""
    unit, k, _ = FD.unit_of(kind)
    xe = per_v[PA.VARIANTS[0]][0]
    nb = len(xe) - 1
    xt = clean(per_v[PA.VARIANTS[0]][3][0])
    out, bad = {}, 0
    for v in PA.VARIANTS:
        arr = {q: np.full(nb, np.nan) for q in ("peak", "peak_err", "sigma", "sigma_err")}
        n = np.zeros(nb)
        for i in range(nb):
            ft = fits.get((name, v, i))
            if ft is None:
                bad += int(windowed[(name, v)][i].sum() >= MIN_FIT)
                continue
            if not (np.isfinite(ft["peak_err"]) and np.isfinite(ft["sigma_err"])):
                bad += 1
                continue
            for q in arr:
                arr[q][i] = k * ft[q]
            n[i] = ft["entries"]
        out[v] = (dict(edges=xe, mean=arr["peak"], err=arr["peak_err"], entries=n,
                       titles=(xt, f"m_{{#mu#mu}} peak position [{unit}]")),
                  dict(edges=xe, mean=arr["sigma"], err=arr["sigma_err"], entries=n,
                       titles=(xt, f"m_{{#mu#mu}} resolution #sigma [{unit}]")))
    return out, bad


def qa_grid(name, v, xe, medges, counts, fits, kind, title, path):
    """Every slice with its fit, to check the fits by eye."""
    nb = len(xe) - 1
    ncol, nrow = 6, int(np.ceil(nb / 6))
    fig, axs = plt.subplots(nrow, ncol, figsize=(4 * ncol, 3 * nrow), squeeze=False)
    c = 0.5 * (medges[1:] + medges[:-1])
    for i, ax in enumerate(axs.flat):
        ax.tick_params(labelsize=9, length=3)
        if i >= nb:
            ax.axis("off")
            continue
        y = counts[i]
        ax.errorbar(c, y, yerr=np.sqrt(y), fmt="o", ms=2, color="black", elinewidth=0.7)
        txt = f"[{xe[i]:.2f}, {xe[i + 1]:.2f}]"
        ft = fits.get((name, v, i))
        if ft is not None:
            ax.stairs(FD.expected(ft["params"], medges, ft["tail"], kind), medges, color="#f89c20", lw=1.2)
            txt += f"\nm={ft['peak']:.4g} s={ft['sigma']:.3g}\nchi2/ndf={ft['chi2'] / max(ft['ndf'], 1):.1f}"
        ax.text(0.03, 0.96, txt, transform=ax.transAxes, fontsize=9, va="top")
        ax.set_ylim(0, max(y.max() * 1.5, 1))
    fig.suptitle(f"{title}, {v} conditions", fontsize=16)
    fig.tight_layout()
    fig.savefig(path, dpi=70)
    plt.close(fig)


def map_plot(z, xe, ye, label, lumi, sel, xt, yt, zt, path, cmap="viridis", symmetric=False, cmin=None):
    """Colour map in a square frame, with the colour scale to its right."""
    fig, ax = plt.subplots(figsize=(10, 10))
    PT.cms_label(ax, label, lumi)
    for t in ax._cms_texts[:2]:  # the label sits on the map
        t.set_bbox(dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))
    ax.set_position([0.19, 0.14, 0.66, 0.66])
    cax = fig.add_axes([0.87, 0.14, 0.03, 0.66])
    z = np.ma.masked_invalid(z)
    norm = None
    if symmetric:
        m = np.max(np.abs(z)) if z.count() else 1.0
        norm = matplotlib.colors.Normalize(-m, m)
    pm = ax.pcolormesh(xe, ye, z.T, cmap=cmap, norm=norm, vmin=cmin if norm is None else None)
    cb = fig.colorbar(pm, cax=cax)
    cb.set_label(zt, fontsize=PT.RATIO_FS)
    cb.ax.tick_params(labelsize=18)
    ax.set_xlabel(xt, fontsize=PT.AXIS_FS)
    ax.set_ylabel(yt, fontsize=PT.AXIS_FS)
    ax.tick_params(axis="both", which="major", labelsize=22)
    ax.text(0.03, PT.below_label(ax), sel, transform=ax.transAxes, fontsize=15, va="top",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))
    PT.save_square(fig, path)
    plt.close(fig)


def profile2d_mean(t, min_entries=20):
    xe, ye, wy, _, n, tit = t
    with np.errstate(divide="ignore", invalid="ignore"):
        mean = np.where(n >= min_entries, wy / n, np.nan)
    return xe, ye, mean[1:-1, 1:-1], tit


def draw_mass_fits(folder, tag, fitres, label, lumi, outdir):
    """Fitted peak and width vs the muon variable, for one folder and set."""
    info, s = FOLDERS[folder], SETS[tag]
    variants, ref = s["variants"], s["ref"]
    pick = lambda per_v: {v: per_v[v] for v in variants}
    sel = info["sel"]
    PT.LABEL_YEAR = MASS_FIT_YEAR.get((folder, tag))
    if PT.LABEL_YEAR:
        lumi = f"{float(lumi):.3g}"
    for name, res in fitres.items():
        msel = sel + "\n" + info["model"]
        PA.plot(f"{name}_peak", pick({v: res[v][0] for v in PA.VARIANTS}), "profile", 1, label, lumi,
                f"{outdir}/mass_fits/{name}_peak", variants=variants, refv=ref, sel=msel, force_diff=True,
                diff_floor=info["floor_peak"])
        PA.plot(f"{name}_width", pick({v: res[v][1] for v in PA.VARIANTS}), "profile", 1, label, lumi,
                f"{outdir}/mass_fits/{name}_width", variants=variants, refv=ref, sel=msel)
    PT.LABEL_YEAR = None


def draw_set(folder, tag, profs, hists, th2, tp2, fitres, label, lumi, outdir):
    info, s = FOLDERS[folder], SETS[tag]
    variants, ref = s["variants"], s["ref"]
    pick = lambda per_v: {v: per_v[v] for v in variants}
    sel = info["sel"]
    for name in sorted(hists[variants[0]]):
        PA.plot(name, pick({v: hists[v][name] for v in PA.VARIANTS}), "hist", 1, label, lumi,
                f"{outdir}/hists/{name}", variants=variants, refv=ref, sel=sel)
    for name in sorted(profs[variants[0]]):
        PA.plot(name, pick({v: profs[v][name] for v in PA.VARIANTS}), "profile", 20, label, lumi,
                f"{outdir}/profiles/{name}", variants=variants, refv=ref, sel=sel, force_diff=True,
                diff_floor=info["floor_mass"] if "Mass" in name else 0.5)
    draw_mass_fits(folder, tag, fitres, label, lumi, outdir)
    os.makedirs(f"{outdir}/maps", exist_ok=True)
    tex = PA.root2tex
    for name, per_v in th2.items():
        for v in variants:
            xe, ye, counts, tit = per_v[v]
            map_plot(counts[1:-1, 1:-1], xe, ye, label, lumi, sel + f"\n{v} Conditions", tex(clean(tit[0])),
                     tex(clean(tit[1])), "Candidates", f"{outdir}/maps/{name}_{v}", cmap="Blues", cmin=0)
    for name, per_v in tp2.items():
        means = {v: profile2d_mean(per_v[v]) for v in variants}
        xe, ye, _, tit = means[variants[0]]
        xt, yt, zt = (tex(clean(x)) for x in tit)
        for v in variants:
            map_plot(means[v][2], xe, ye, label, lumi, sel + f"\n{v} Conditions", xt, yt, zt,
                     f"{outdir}/maps/{name}_{v}", symmetric="Delta" in name, cmap="RdBu_r" if "Delta" in name else "viridis")
            if v != ref:
                map_plot(means[v][2] - means[ref][2], xe, ye, label, lumi, sel + f"\n{v} $-$ {ref} Conditions", xt, yt,
                         r"$\Delta$ " + zt, f"{outdir}/maps/{name}_{v}_minus_{ref}", cmap="RdBu_r", symmetric=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-d", "--dqmdir", default=IP)
    ap.add_argument("--runs", default=os.path.join(HERE, "results", "runs_used.txt"))
    ap.add_argument("--lumifile", default=os.path.join(HERE, "..", "lumi_data.csv"))
    ap.add_argument("-o", "--outdir", default=os.path.join(HERE, "plots", "weakmodes"))
    ap.add_argument("-r", "--results", default=os.path.join(HERE, "results"))
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("-j", "--jobs", type=int, default=8)
    ap.add_argument("--mass-fits-only", metavar="FOLDER/SET", default=None,
                    help="only redo the fits of FOLDER and redraw its SET/mass_fits; csv files and other plots untouched")
    a = ap.parse_args()
    hep.style.use("CMS")
    os.makedirs(a.results, exist_ok=True)
    only_folder, only_set = a.mass_fits_only.split("/") if a.mass_fits_only else (None, None)
    folders = [only_folder] if only_folder else list(FOLDERS)
    runs = [int(l.split()[0]) for l in open(a.runs) if l.strip()]
    lumis = PT.run_lumis(a.lumifile)
    lumi = f"{sum(lumis[r][1] for r in runs if r in lumis):.2f}"
    print(f"{len(runs)} runs, {lumi} fb^-1")

    jobs = [(v, r, folder, a.dqmdir) for folder in folders for v in PA.VARIANTS for r in runs]
    per = {(f, v): dict(prof=[], hist=[], th2={}, tp2={}) for f in folders for v in PA.VARIANTS}
    with Pool(a.jobs) as pool:
        for v, folder, prof, hist, th2, tp2 in pool.imap_unordered(read_one, jobs, chunksize=4):
            p = per[(folder, v)]
            p["prof"].append(prof)
            p["hist"].append(hist)
            add_nd(p["th2"], th2, 1)
            add_nd(p["tp2"], tp2, 3)

    for folder in folders:
        info = FOLDERS[folder]
        profs, hists = {}, {}
        for v in PA.VARIANTS:
            profs[v], hists[v] = PA.merge_profiles(per[(folder, v)]["prof"]), PA.merge_hists(per[(folder, v)]["hist"])
            for d in list(profs[v].values()) + list(hists[v].values()):
                d["titles"] = tuple(clean(t) for t in d["titles"])
        th2 = {n: {v: per[(folder, v)]["th2"][n] for v in PA.VARIANTS} for n in per[(folder, PA.VARIANTS[0])]["th2"]}
        tp2 = {n: {v: per[(folder, v)]["tp2"][n] for v in PA.VARIANTS} for n in per[(folder, PA.VARIANTS[0])]["tp2"]}

        fits, medges, windowed = fit_mass(folder, th2, a.jobs)
        fitres, rows = {}, []
        for name, per_v in th2.items():
            res, bad = fit_results(name, per_v, fits, info["kind"], windowed)
            fitres[name] = {v: res[v] for v in PA.VARIANTS}
            if bad:
                print(f"  {name}: {bad} slices without a usable fit")
        if only_set:
            draw_mass_fits(folder, only_set, fitres, a.label, lumi, f"{a.outdir}/{folder}/{only_set}")
            print(f"-> {a.outdir}/{folder}/{only_set}/mass_fits")
            continue
        for name, per_v in th2.items():
            xe = per_v[PA.VARIANTS[0]][0]
            os.makedirs(f"{a.outdir}/{folder}/fit_qa", exist_ok=True)
            for v in PA.VARIANTS:
                tit = f"{folder} {name}"
                qa_grid(name, v, xe, medges, windowed[(name, v)], fits, info["kind"], tit,
                        f"{a.outdir}/{folder}/fit_qa/{name}_{v}.png")
                for i in range(len(xe) - 1):
                    ft = fits.get((name, v, i))
                    if ft is not None:
                        rows.append(dict(histogram=name, variant=v, x_low=f"{xe[i]:.4f}", x_high=f"{xe[i + 1]:.4f}",
                                         entries=int(ft["entries"]), peak_GeV=f"{ft['peak']:.5f}",
                                         peak_err_GeV=f"{ft['peak_err']:.5f}", sigma_GeV=f"{ft['sigma']:.5f}",
                                         sigma_err_GeV=f"{ft['sigma_err']:.5f}", chi2=f"{ft['chi2']:.1f}", ndf=ft["ndf"]))
        with open(f"{a.results}/{folder}_mass_fits.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        PA.write_csv(f"{a.results}/{folder}_profiles.csv", profs, sorted(profs["NGT"]), "mean")
        PA.write_csv(f"{a.results}/{folder}_hists.csv", hists, sorted(hists["NGT"]), "counts")
        chi = np.array([float(r["chi2"]) / max(r["ndf"], 1) for r in rows])
        print(f"  {len(rows)} slice fits, chi2/ndf median {np.median(chi):.2f}, 95% below {np.quantile(chi, 0.95):.2f}")
        for tag in SETS:
            draw_set(folder, tag, profs, hists, th2, tp2, fitres, a.label, lumi, f"{a.outdir}/{folder}/{tag}")
        print(f"-> {a.outdir}/{folder}")


if __name__ == "__main__":
    main()
