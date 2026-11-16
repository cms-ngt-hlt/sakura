#!/usr/bin/env python3
"""Z -> mu mu peak position and resolution vs time / run for the HLT, Prompt and NGT reprocessings.

Input : DQMOutput/hlt/{HLT,Prompt,NGT}/DQM_hlt_R<run>.root,
        HLT/Run summary/ObjectMonitor/MainShifter/diMuon_Mass (HLT di-muons of
        HLT_Mu17_TrkIsoVVL_(Tk)Mu8_TrkIsoVVL_DZ, 60-160 GeV, 2 GeV bins)
Model : Breit-Wigner (Gamma_Z = 2.4952 GeV, fixed) convolved with a double-sided Crystal Ball (Gaussian core
        sigma = resolution; power-law tails for FSR and for the barrel/endcap resolution mixture), plus an
        exponential background; binned Poisson likelihood fit in [FIT_LO, FIT_HI]. The four tail parameters are
        fitted once on the sum of all selected runs and all three condition sets, and fixed in every other fit. numpy only (Nelder-Mead minimiser, uncertainties
        from the numerical Hessian).
Runs  : by default the runs of results/runs_used.txt (tracking problems removed, see plot_trends.py);
        --all-runs uses every run with >= MIN_ENTRIES di-muons in a condition set.

Usage : fit_zmumu.py [-d ../DQMOutput] [--label Preliminary] [--all-runs]
Writes: results/zmumu_fits.csv, plots/zmumu[_allruns]/{vs_time,vs_run}/zmumu_{mass,resolution}.{png,pdf},
        plots/zmumu[_allruns]/fits_<variant>.png (fit check per run), plots/zmumu[_allruns]/combined_fit.{png,pdf}
"""
import argparse
import csv
import glob
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import mplhep as hep  # noqa: E402
import numpy as np  # noqa: E402
import uproot  # noqa: E402

import plot_trends as PT  # noqa: E402  (styles, CMS axes, run times)

HIST = "HLT/Run summary/ObjectMonitor/MainShifter/diMuon_Mass"
MZ_PDG, GZ = 91.1876, 2.4952
FIT_LO, FIT_HI = 70.0, 110.0
MIN_ENTRIES = 2000
FINE = 0.05  # GeV, grid for the numerical convolution
N_MAX = 50.0  # cap on the Crystal Ball tail exponents (beyond this the tail is Gaussian-like)


def load(dqmdir):
    out = {}
    for v in PT.VARIANTS:
        for fn in sorted(glob.glob(f"{dqmdir}/hlt/{v}/DQM_hlt_R*.root")):
            run = int(re.search(r"_R0*(\d+)\.root$", fn).group(1))
            try:
                h = uproot.open(fn)[f"DQMData/Run {run}/{HIST}"]
            except KeyError:
                continue
            vals, edges = h.to_numpy(flow=False)
            out[(run, v)] = (vals.astype(float), edges)
    return out


# ---------------------------------------------------------------- model + fit
def dscb(t, aL, nL, aR, nR):
    """Double-sided Crystal Ball in t = x / sigma: Gaussian core, power-law tails beyond -aL and +aR."""
    out = np.exp(-0.5 * t ** 2)
    for side, a, n in ((t < -aL, aL, nL), (t > aR, aR, nR)):
        A = (n / a) ** n * np.exp(-0.5 * a ** 2)
        B = n / a - a
        out[side] = A * (B + np.abs(t[side])) ** (-n)
    return out


def signal_bins(edges, m0, sigma, tail):
    """Bin integrals (normalised to 1 over the fit range) of BW(m0, GZ) x DSCB(sigma, tail)."""
    lo, hi = edges[0] - 30, edges[-1] + 30  # margin > kernel half-width
    npt = int(round((hi - lo) / FINE))
    x = lo + FINE * (np.arange(npt) + 0.5)
    bw = 1 / ((x - m0) ** 2 + GZ ** 2 / 4)
    half = int(round(min(25.0, 8 * sigma + 20) / FINE))
    k = np.arange(-half, half + 1) * FINE
    g = dscb(k / sigma, *tail)
    pdf = np.convolve(bw, g / g.sum(), mode="same")
    cdf = np.concatenate([[0], np.cumsum(pdf) * FINE])
    xc = lo + FINE * np.arange(npt + 1)
    c = np.interp(edges, xc, cdf)
    b = np.diff(c)
    return b / b.sum()


def expo_bins(edges, lam):
    c = -np.exp(-lam * (edges - FIT_LO)) / lam if abs(lam) > 1e-6 else edges
    b = np.diff(c)
    return b / b.sum()


def tail_of(p, tail):
    """(aL, nL, aR, nR): fixed, or from p[5:9] = (log aL, log(nL-1), log aR, log(nR-1))."""
    if tail is not None:
        return tail
    return (np.exp(p[5]), min(1 + np.exp(p[6]), N_MAX), np.exp(p[7]), min(1 + np.exp(p[8]), N_MAX))


def expected(p, edges, tail):
    """p = (log Nsig, m0, log sigma, log Nbkg, lambda[, tail parameters]); tail = fixed tuple or None."""
    ns, m0, ls, nb, lam = np.exp(p[0]), p[1], p[2], np.exp(p[3]), p[4]
    return ns * signal_bins(edges, m0, np.exp(ls), tail_of(p, tail)) + nb * expo_bins(edges, lam)


def nll(p, y, edges, tail):
    mu = np.maximum(expected(p, edges, tail), 1e-9)
    return np.sum(mu - y * np.log(mu))


def nelder_mead(f, x0, step, tol=1e-7, maxit=4000):
    n = len(x0)
    pts = [np.array(x0, float)] + [np.array(x0, float) + np.eye(n)[i] * step[i] for i in range(n)]
    vals = [f(p) for p in pts]
    for _ in range(maxit):
        order = np.argsort(vals)
        pts, vals = [pts[i] for i in order], [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) < tol * (abs(vals[0]) + 1e-9):
            break
        cen = np.mean(pts[:-1], axis=0)
        xr = cen + (cen - pts[-1])
        fr = f(xr)
        if fr < vals[0]:
            xe = cen + 2 * (cen - pts[-1])
            fe = f(xe)
            pts[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            pts[-1], vals[-1] = xr, fr
        else:
            xc = cen + 0.5 * (pts[-1] - cen)
            fc = f(xc)
            if fc < vals[-1]:
                pts[-1], vals[-1] = xc, fc
            else:
                pts = [pts[0] + 0.5 * (q - pts[0]) for q in pts]
                vals = [f(q) for q in pts]
    i = int(np.argmin(vals))
    return pts[i], vals[i]


def hessian(f, p, h):
    n = len(p)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            ei, ej = np.eye(n)[i] * h[i], np.eye(n)[j] * h[j]
            H[i, j] = H[j, i] = (f(p + ei + ej) - f(p + ei - ej) - f(p - ei + ej) + f(p - ei - ej)) / (4 * h[i] * h[j])
    return H


def fit(vals, edges, tail=None):
    """Fit one histogram. tail=None: alpha and n free; otherwise (alpha, n) fixed."""
    c = 0.5 * (edges[1:] + edges[:-1])
    sel = (c > FIT_LO) & (c < FIT_HI)
    y, e = vals[sel], np.concatenate([edges[:-1][sel], [edges[1:][sel][-1]]])
    tot = y.sum()
    side = max(y[-3:].mean() * len(y), 1.0)
    p0 = [np.log(max(tot - side, 10)), MZ_PDG - 0.3, np.log(1.5), np.log(side), 0.05]
    step = [0.2, 0.5, 0.2, 0.5, 0.02]
    if tail is None:
        p0 += [np.log(1.0), np.log(2.0), np.log(1.5), np.log(3.0)]
        step += [0.3, 0.3, 0.3, 0.3]
    f = lambda p: nll(p, y, e, tail)
    p, best = nelder_mead(f, p0, step)
    for _ in range(2):  # restarts
        p, best = nelder_mead(f, p, [s / 4 for s in step])
    if tail is None:  # uncertainties with the tail parameters fixed at their best values
        fixed = tail_of(p, None)
        f5 = lambda q: nll(q, y, e, fixed)
        p5 = p[:5]
    else:
        f5, p5 = f, p
    npar = len(p5)
    try:
        H = hessian(f5, p5, [1e-3] * npar)
        cov = np.linalg.inv(H)
        err = np.sqrt(np.diag(cov)) if np.all(np.diag(cov) > 0) else np.full(npar, np.nan)
    except np.linalg.LinAlgError:
        err = np.full(npar, np.nan)
    mu = expected(p, e, tail)
    chi2 = np.sum((y - mu) ** 2 / np.maximum(mu, 1))
    sigma = np.exp(p[2])
    out = dict(mass=p[1], mass_err=err[1], sigma=sigma, sigma_err=sigma * err[2], nsig=np.exp(p[0]),
               nbkg=np.exp(p[3]), lam=p[4], chi2=chi2, ndf=int(sel.sum()) - len(p), entries=vals.sum(),
               params=p, fit_edges=e, fit_y=y, tail=tail)
    out["tail_params"] = tail_of(p, tail)
    return out


# ---------------------------------------------------------------- plots
def trend(fits, runs, xs, xaxis, label, outdir):
    os.makedirs(outdir, exist_ok=True)
    for key, err, ylab, ref in (("mass", "mass_err", r"$m_{\mu\mu}$ peak position [GeV]", MZ_PDG),
                                ("sigma", "sigma_err", r"$m_{\mu\mu}$ resolution $\sigma$ [GeV]", None)):
        fig, ax = PT.cms_axes(label)
        data = {}
        for v in PT.VARIANTS:
            rr = [r for r in runs if (r, v) in fits]
            data[v] = (np.array([xs[r] for r in rr]), np.array([fits[(r, v)][key] for r in rr]),
                       np.array([fits[(r, v)][err] for r in rr]))
        PT.draw(ax, data)
        if ref:
            ax.axhline(ref, color="gray", lw=1, ls="--", zorder=1)
            ax.text(0.99, ref, r"$m_{Z}^{PDG}$ ", transform=ax.get_yaxis_transform(), ha="right", va="bottom",
                    fontsize=14, color="gray")
        ax.set_ylabel(ylab)
        PT.text(ax, r"Z$\rightarrow\mu\mu$, HLT di-muons (Mu17_Mu8 DZ paths)" + "\n"
                + rf"BW($\Gamma_Z$ fixed) $\otimes$ double-sided CB + exp., {FIT_LO:.0f}$-${FIT_HI:.0f} GeV")
        PT.finish(fig, ax, xaxis, f"{outdir}/zmumu_{'mass' if key == 'mass' else 'resolution'}")


def fit_grid(hists, fits, runs, variant, path):
    rr = [r for r in runs if (r, variant) in fits]
    nc = 6
    nr = int(np.ceil(len(rr) / nc))
    fig, axs = plt.subplots(nr, nc, figsize=(3.2 * nc, 2.6 * nr), squeeze=False)
    for ax in axs.flat:
        ax.axis("off")
    for ax, r in zip(axs.flat, rr):
        ft = fits[(r, variant)]
        e, y = ft["fit_edges"], ft["fit_y"]
        c = 0.5 * (e[1:] + e[:-1])
        ax.axis("on")
        ax.errorbar(c, y, yerr=np.sqrt(y), fmt="k.", ms=3)
        ax.step(e, np.append(expected(ft["params"], e, ft["tail"]), np.nan), where="post", color="tab:red", lw=1)
        ax.set_title(f"{r}: m={ft['mass']:.2f}, σ={ft['sigma']:.2f}, χ²/n={ft['chi2']:.0f}/{ft['ndf']}", fontsize=8)
        ax.tick_params(labelsize=7)
    fig.suptitle(f"{variant} conditions: di-muon mass fits", fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=80)
    plt.close(fig)


def combined(hists, runs, label, outdir):
    """Fit of the di-muon mass summed over the selected runs, one curve per condition set.
    The tail shape is fitted once on the sum of all three condition sets and then fixed everywhere,
    so that the core sigma is comparable between condition sets (sigma and tails are correlated)."""
    fig, ax = PT.cms_axes(label)
    summed = {v: np.sum([hists[(r, v)][0] for r in runs if (r, v) in hists], axis=0) for v in PT.VARIANTS}
    edges = next(hists[(r, v)][1] for r in runs for v in PT.VARIANTS if (r, v) in hists)
    common = fit(sum(summed.values()), edges)["tail_params"]
    res = {}
    for v in PT.VARIANTS:
        vals = summed[v]
        ft = fit(vals, edges, tail=common)
        res[v] = ft
        st = PT.STYLE[v]
        c = 0.5 * (edges[1:] + edges[:-1])
        ax.errorbar(c, vals, yerr=np.sqrt(vals), fmt=st["marker"], ms=st["ms"] - 1, color=st["color"],
                    label=f"{st['label']}: m = {ft['mass']:.3f} ± {ft['mass_err']:.3f}, "
                          f"σ = {ft['sigma']:.3f} ± {ft['sigma_err']:.3f} GeV")
        e = ft["fit_edges"]
        ax.stairs(expected(ft["params"], e, ft["tail"]), e, color=st["color"], lw=1.5)
    ax.set_xlabel(r"$m_{\mu\mu}$ [GeV]")
    ax.set_ylabel("Di-muon candidates / 2 GeV")
    ax.set_xlim(60, 130)
    lo, hi = ax.get_ylim()
    ax.set_ylim(0, hi * 1.45)
    ax.legend(loc="upper right", fontsize=13, frameon=False)
    PT.text(ax, f"{len(runs)} runs")
    fig.savefig(f"{outdir}/combined_fit.png", dpi=200, bbox_inches="tight")
    fig.savefig(f"{outdir}/combined_fit.pdf", bbox_inches="tight")
    plt.close(fig)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dqmdir", default=os.path.join(PT.HERE, ".."))
    ap.add_argument("-i", "--indir", default=os.path.join(PT.HERE, "results"))
    ap.add_argument("-o", "--outdir", default=os.path.join(PT.HERE, "plots"))
    ap.add_argument("--metrics", default=f"{PT.SCAN}/metrics.csv")
    ap.add_argument("--label", default="Preliminary")
    ap.add_argument("--all-runs", action="store_true", help="no tracking-based run selection")
    a = ap.parse_args()
    hep.style.use("CMS")

    hists = load(a.dqmdir)
    enough = {k for k, (vals, _) in hists.items() if vals.sum() >= MIN_ENTRIES}
    if a.all_runs:
        runs = sorted({r for r, _ in enough})
        tag = "zmumu_allruns"
    else:
        sel = [int(l.split()[0]) for l in open(f"{a.indir}/runs_used.txt") if l.strip()]
        runs = [r for r in sel if all((r, v) in enough for v in PT.VARIANTS)]
        tag = "zmumu"
    out = f"{a.outdir}/{tag}"
    os.makedirs(out, exist_ok=True)
    res = combined(hists, runs, a.label, out)  # also fixes the (common) tail parameters
    fits = {}
    for (r, v) in sorted(enough):
        if r in runs:
            fits[(r, v)] = fit(*hists[(r, v)], tail=res[v]["tail_params"])

    with open(f"{a.indir}/{tag}_fits.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["run", "variant", "entries", "mass_GeV", "mass_err_GeV", "sigma_GeV", "sigma_err_GeV",
                    "nsig", "nbkg", "chi2", "ndf"])
        for (r, v), ft in sorted(fits.items()):
            if r in runs:
                w.writerow([r, v, int(ft["entries"]), f"{ft['mass']:.4f}", f"{ft['mass_err']:.4f}",
                            f"{ft['sigma']:.4f}", f"{ft['sigma_err']:.4f}", f"{ft['nsig']:.0f}", f"{ft['nbkg']:.0f}",
                            f"{ft['chi2']:.1f}", ft["ndf"]])
    times, _ = PT.run_times(runs, a.metrics)
    for xaxis in ("time", "run"):
        xs = times if xaxis == "time" else {r: r for r in runs}
        trend(fits, runs, xs, xaxis, a.label, f"{out}/vs_{xaxis}")
    for v in PT.VARIANTS:
        fit_grid(hists, fits, runs, v, f"{out}/fits_{v}.png")
    print(f"{len(runs)} runs ({'all' if a.all_runs else 'tracking selection'}) -> {out}")
    for v, ft in res.items():
        print(f"  {v:7s} combined: m = {ft['mass']:.3f} +- {ft['mass_err']:.3f} GeV, "
              f"sigma = {ft['sigma']:.3f} +- {ft['sigma_err']:.3f} GeV, "
              f"tails (aL, nL, aR, nR) = {tuple(round(float(t), 2) for t in ft['tail_params'])}, "
              f"chi2/ndf = {ft['chi2']:.1f}/{ft['ndf']}")


if __name__ == "__main__":
    main()
