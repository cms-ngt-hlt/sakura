"""
zee_stability_per_fill.py

Per-fill DSCB fit stability analyser.

For every fill found in the HLT / NGT / Prompt folders (by grouping runs):
  1. Aggregates di-electron mass histograms for all runs in the fill.
  2. Fits a Double-sided Crystal-Ball + exponential background.
  3. Saves a sanity-check plot for the aggregated fill.
  4. Collects the fitted μ and σ/μ per fill and plots them vs integrated
     luminosity, centering the points at the midpoint of each fill's lumi range.

Usage
-----
  python zee_stability_per_fill.py
"""

import ROOT
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

plt.style.use(hep.style.CMS)

# ─────────────────────────────────────────────────────────────────────────────
# DCB + exponential background
# ─────────────────────────────────────────────────────────────────────────────

def dcb_func(x, p):
    xx = x[0]
    mean, sigma     = p[3], p[4]
    aL, nL, aH, nH = abs(p[5]), p[6], abs(p[7]), p[8]
    t = (xx - mean) / sigma
    bkg = p[0] * np.exp(p[1] * xx)

    if -aL < t < aH:
        return p[2] * np.exp(-0.5 * t**2) + bkg
    elif t <= -aL:
        A = (nL / aL)**nL * np.exp(-0.5 * aL**2)
        B = nL / aL - aL
        return p[2] * A * (B - t)**(-nL) + bkg
    else:
        A = (nH / aH)**nH * np.exp(-0.5 * aH**2)
        B = nH / aH - aH
        return p[2] * A * (B + t)**(-nH) + bkg


def bkg_only(x, p):
    return p[0] * np.exp(p[1] * x)


def sig_only(x, p):
    mean, sigma     = p[3], p[4]
    aL, nL, aH, nH = abs(p[5]), p[6], abs(p[7]), p[8]
    t = (x - mean) / sigma

    if -aL < t < aH:
        return p[2] * np.exp(-0.5 * t**2)
    elif t <= -aL:
        A = (nL / aL)**nL * np.exp(-0.5 * aL**2)
        B = nL / aL - aL
        return p[2] * A * (B - t)**(-nL)
    else:
        A = (nH / aH)**nH * np.exp(-0.5 * aH**2)
        B = nH / aH - aH
        return p[2] * A * (B + t)**(-nH)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_lumi_info(lumi_csv):
    """Parse brilcalc-style CSV → {run: fill}, {run: recorded_lumi_pb}."""
    run_fill, run_lumi = {}, {}
    if not os.path.exists(lumi_csv):
        print(f"Warning: {lumi_csv} not found – fill/lumi info will be missing.")
        return run_fill, run_lumi

    with open(lumi_csv) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split(',')
            if ':' not in parts[0]:
                continue
            rf   = parts[0].split(':')
            run  = int(rf[0])
            fill = int(rf[1])
            lumi = float(parts[5])   # recorded (/pb)
            run_fill[run] = fill
            run_lumi[run] = lumi

    return run_fill, run_lumi


def extract_run_number(filename):
    match = re.search(r'_R(\d+)\.root', filename)
    return int(match.group(1)) if match else None


# ─────────────────────────────────────────────────────────────────────────────
# Per-fill fit + sanity-check plot
# ─────────────────────────────────────────────────────────────────────────────

def fit_fill(root_hist, label, fill_id, sanity_dir):
    """
    Fit root_hist with DCB + exp background.
    """
    fit_min, fit_max = 60, 120

    peak_val = root_hist.GetMaximum()
    peak_x   = root_hist.GetXaxis().GetBinCenter(root_hist.GetMaximumBin())

    if peak_val <= 0 or root_hist.GetEntries() < 10:
        print(f"  [{label} Fill {fill_id}] Too few entries, skipping.")
        return None

    fname    = f"f_{label}_Fill{fill_id}"
    fit_func = ROOT.TF1(fname, dcb_func, fit_min, fit_max, 9)

    fit_func.SetParameters(
        peak_val * 0.05,          # p0  bkg constant
        -0.04,                    # p1  bkg slope
        peak_val,                 # p2  signal norm
        peak_x,                   # p3  mean
        3.0,                      # p4  sigma
        1.5,                      # p5  aL
        5.0,                      # p6  nL
        1.5,                      # p7  aH
        5.0,                      # p8  nH
    )
    fit_func.SetParLimits(0, 0,              peak_val)
    fit_func.SetParLimits(1, -0.8,           0.0)
    fit_func.SetParLimits(2, peak_val*0.01,  peak_val*5.0)
    fit_func.SetParLimits(3, peak_x - 5.0,  peak_x + 5.0)
    fit_func.SetParLimits(4, 0.5,   8.0)
    fit_func.SetParLimits(5, 0.1,  10.0);  fit_func.SetParLimits(6, 1.01, 100.0)
    fit_func.SetParLimits(7, 0.1,  10.0);  fit_func.SetParLimits(8, 1.01, 100.0)

    root_hist.Fit(fit_func, "SRLIMQ", "", fit_min, fit_max)

    mean      = fit_func.GetParameter(3);  mean_err  = fit_func.GetParError(3)
    sigma     = fit_func.GetParameter(4);  sigma_err = fit_func.GetParError(4)
    chi2      = fit_func.GetChisquare()
    ndf       = fit_func.GetNDF()
    chi2_ndf  = chi2 / ndf if ndf > 0 else 0.0

    if not (80 < mean < 95):
        print(f"  [{label} Fill {fill_id}] Unphysical mean={mean:.2f}, skipping.")
        return None

    res     = (sigma / mean) * 100.0
    res_err = res * np.sqrt((sigma_err / sigma)**2 + (mean_err / mean)**2)
    params  = [fit_func.GetParameter(i) for i in range(9)]

    # ── Sanity-check plot ──────────────────────────────────────────────────
    x_plot  = np.linspace(fit_min, fit_max, 500)
    y_total = [dcb_func([x], params) for x in x_plot]
    y_bkg   = [bkg_only(x,   params) for x in x_plot]
    y_sig   = [sig_only(x,   params) for x in x_plot]

    pull_x, pull_y = [], []
    for i in range(1, root_hist.GetNbinsX() + 1):
        xc  = root_hist.GetBinCenter(i)
        if not (fit_min <= xc <= fit_max):
            continue
        val = root_hist.GetBinContent(i)
        err = root_hist.GetBinError(i)
        fv  = fit_func.Eval(xc)
        if err > 0:
            pull_x.append(xc)
            pull_y.append((val - fv) / err)

    fig_s, (ax_s, ax_p) = plt.subplots(
        2, 1, figsize=(10, 12), sharex=True,
        gridspec_kw={'height_ratios': [3, 2], 'hspace': 0.05}
    )
    hep.cms.label(ax=ax_s, data=True,
                  label=f"Sanity Check | {label} | Fill {fill_id}",
                  year=2025, fontsize=16)

    hep.histplot(root_hist, ax=ax_s,
                 label=f"{label} Fill {fill_id}",
                 color='black', histtype='errorbar', marker='o')

    ax_s.plot(x_plot, y_total, color='red',   lw=3,         label='Total Fit (DCB + Exp)')
    ax_s.plot(x_plot, y_sig,   color='blue',  lw=2, ls='--', label='Signal (DCB)')
    ax_s.plot(x_plot, y_bkg,   color='green', lw=2, ls=':',  label='Background (Exp)')

    par_names = ["Bkg C0","Bkg C1","Sig Norm","Mean","Sigma","aL","nL","aH","nH"]
    stats  = rf"$\chi^2/\mathrm{{ndf}} = {chi2:.1f}/{ndf} = {chi2_ndf:.2f}$" + "\n"
    stats += rf"Res $(\sigma/\mu)$: ${res:.2f} \pm {res_err:.2f}\%$" + "\n"
    stats += "─" * 22 + "\n"
    for i in range(9):
        stats += rf"{par_names[i]}: {params[i]:.3f} $\pm$ {fit_func.GetParError(i):.3f}" + "\n"

    ax_s.text(0.04, 0.96, stats, transform=ax_s.transAxes, fontsize=8,
              va='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))
    ax_s.set_ylabel("Events", fontsize=15)
    ax_s.set_xlim(fit_min, fit_max)
    ax_s.legend(loc='upper right', fontsize=12)
    ax_s.grid(True, alpha=0.3)

    ax_p.errorbar(pull_x, pull_y, yerr=1, fmt='o',
                  color='black', markersize=4, capsize=0)
    ax_p.axhline( 0, color='red',  ls='-')
    ax_p.axhline( 1, color='gray', ls='--', alpha=0.5)
    ax_p.axhline(-1, color='gray', ls='--', alpha=0.5)
    ax_p.axhline( 2, color='gray', ls=':',  alpha=0.3)
    ax_p.axhline(-2, color='gray', ls=':',  alpha=0.3)
    ax_p.set_ylabel("Pull", fontsize=15)
    ax_p.set_xlabel(r"$m_{ee}$ [GeV]", fontsize=15)
    if pull_y:
        mp = max(abs(min(pull_y)), abs(max(pull_y)))
        ax_p.set_ylim(-mp * 1.3, mp * 1.3)
    ax_p.grid(True, alpha=0.3)

    out_png = os.path.join(sanity_dir, f"{label}_Fill{fill_id}_Fit_Sanity.png")
    fig_s.savefig(out_png, bbox_inches='tight')
    plt.close(fig_s)

    return mean, mean_err, res, res_err, chi2_ndf


# ─────────────────────────────────────────────────────────────────────────────
# Analyser
# ─────────────────────────────────────────────────────────────────────────────

class PerFillFitAnalyzer:

    SOURCES = {
        'HLT':    {'folder': 'HLT',    'color': '#5790fc', 'marker': 'o'},
        'NGT':    {'folder': 'NGT',    'color': '#f89c20', 'marker': 'D'},
        'Prompt': {'folder': 'Prompt', 'color': 'black',   'marker': 'v'},
    }

    def __init__(self, base_path, lumi_csv):
        self.base_path  = base_path
        self.run_fill, self.run_lumi = load_lumi_info(lumi_csv)
        self.sanity_dir = os.path.join(base_path, "fit_sanity_checks_per_fill")
        os.makedirs(self.sanity_dir, exist_ok=True)

        # Group runs by fill
        self.fill_to_runs = {}
        for run, fill in self.run_fill.items():
            if fill not in self.fill_to_runs:
                self.fill_to_runs[fill] = []
            self.fill_to_runs[fill].append(run)

        # Calculate lumi ranges for fills
        # We need a consistent run order to define "start" and "end" of each fill in cumulative lumi
        self.all_runs = sorted(self.run_lumi.keys())
        self.run_to_cum_end = {}
        curr = 0.0
        for r in self.all_runs:
            curr += self.run_lumi[r]
            self.run_to_cum_end[r] = curr
        
        self.fill_info = {} # fill -> {'x': midpoint_fb, 'start': start_fb, 'end': end_fb, 'lumi': total_pb}
        for fill, runs in self.fill_to_runs.items():
            starts = [self.run_to_cum_end[r] - self.run_lumi[r] for r in runs if r in self.run_to_cum_end]
            ends   = [self.run_to_cum_end[r] for r in runs if r in self.run_to_cum_end]
            if not starts: continue
            
            f_start = min(starts)
            f_end   = max(ends)
            self.fill_info[fill] = {
                'x':     (f_start + f_end) / 2.0 / 1000.0, # midpoint in fb-1
                'start': f_start / 1000.0,
                'end':   f_end / 1000.0,
                'lumi':  sum(self.run_lumi[r] for r in runs if r in self.run_lumi)
            }

        # fit_results[fill][source] = (mean, mean_err, res, res_err, chi2_ndf)
        self.fit_results = {}
        self._run_all_fits()

    def _open_histogram(self, fpath, run_num):
        rf = ROOT.TFile.Open(fpath)
        if not rf or rf.IsZombie():
            return None

        dqm_path = (f"DQMData/Run {run_num}/HLT/Run summary/"
                    f"ObjectMonitor/MainShifter/di-Electron_Mass")
        h = rf.Get(dqm_path)

        if not h:
            for key in rf.GetListOfKeys():
                if "di-Electron_Mass" in key.GetName():
                    h = key.ReadObj()
                    break

        if not h:
            rf.Close()
            return None

        h_clone = h.Clone(f"htmp_{run_num}_{id(fpath)}")
        h_clone.SetDirectory(0)
        rf.Close()
        return h_clone

    def _run_all_fits(self):
        ROOT.gROOT.SetBatch(True)

        for label, info in self.SOURCES.items():
            folder = os.path.join(self.base_path, info['folder'])
            if not os.path.exists(folder):
                print(f"Warning: {folder} not found, skipping {label}.")
                continue

            files = sorted(
                f for f in os.listdir(folder)
                if f.endswith('.root') and not f.endswith('.origin')
            )
            run_to_file = {extract_run_number(f): f for f in files}
            
            print(f"\n=== Fitting {label} per fill ===")

            for fill in sorted(self.fill_to_runs.keys()):
                runs_in_fill = self.fill_to_runs[fill]
                h_sum = None
                
                for run_num in runs_in_fill:
                    if run_num in run_to_file:
                        fpath = os.path.join(folder, run_to_file[run_num])
                        h = self._open_histogram(fpath, run_num)
                        if h:
                            if h_sum is None:
                                h_sum = h.Clone(f"h_sum_{label}_Fill{fill}")
                                h_sum.SetDirectory(0)
                            else:
                                h_sum.Add(h)

                if h_sum is None:
                    continue

                print(f"  Fitting Fill {fill} ({len(runs_in_fill)} runs)...")
                result = fit_fill(h_sum, label, fill, self.sanity_dir)

                if fill not in self.fit_results:
                    self.fit_results[fill] = {src: None for src in self.SOURCES}
                self.fit_results[fill][label] = result

                if result:
                    mu, mu_e, res, res_e, c2 = result
                    print(f"    Fill {fill}  μ={mu:.3f}±{mu_e:.3f} GeV  "
                          f"σ/μ={res:.2f}±{res_e:.2f}%  χ²/ndf={c2:.2f}")

    def plot_stability_vs_lumi(self, output_file="Zee_Stability_Lumi_PerFillFit.png"):
        fills_to_plot = sorted(f for f in self.fit_results if f in self.fill_info)
        if not fills_to_plot:
            print("No fills with results and lumi info.")
            return

        LUMI_THRESHOLD = 1.0 # pb

        fig, (ax_top, ax_bot) = plt.subplots(
            2, 1, figsize=(10, 12), sharex=True,
            gridspec_kw={'height_ratios': [3, 2], 'hspace': 0.05}
        )
        hep.cms.label(ax=ax_top, data=True, text="Preliminary",
                      year=2025, lumi=2.09, com=13.6, fontsize=22)

        for label, info in self.SOURCES.items():
            x_pts, mu_pts, mu_err_pts, res_pts, res_err_pts = [], [], [], [], []

            for fill in fills_to_plot:
                res = self.fit_results[fill].get(label)
                if res is not None:
                    x_pts.append(self.fill_info[fill]['x'])
                    mu_pts.append(res[0]); mu_err_pts.append(res[1])
                    res_pts.append(res[2]); res_err_pts.append(res[3])

            common_kw = dict(
                fmt=info['marker'], color=info['color'],
                capsize=3, markersize=10, linewidth=0, markeredgewidth=1.5,
                label=f"{label} Conditions",
            )
            ax_top.errorbar(x_pts, mu_pts,  yerr=mu_err_pts,  **common_kw)
            ax_bot.errorbar(x_pts, res_pts, yerr=res_err_pts, **common_kw)

        # Add padding to y-axes
        ax_top.margins(y=0.25)
        ax_bot.margins(y=0.15)

        # Boundaries
        fig.canvas.draw()
        ylim_top = ax_top.get_ylim()
        y_text  = ylim_top[0] + 0.04 * (ylim_top[1] - ylim_top[0])

        all_sorted_fills = sorted(self.fill_info.keys(), key=lambda f: self.fill_info[f]['start'])
        for i, fill in enumerate(all_sorted_fills):
            finfo = self.fill_info[fill]
            if i < len(all_sorted_fills) - 1:
                nxt = all_sorted_fills[i+1]
                if finfo['lumi'] > LUMI_THRESHOLD or self.fill_info[nxt]['lumi'] > LUMI_THRESHOLD:
                    for ax in (ax_top, ax_bot):
                        ax.axvline(finfo['end'], color='grey', ls='--', alpha=0.6, lw=1.5)

            if finfo['lumi'] > LUMI_THRESHOLD:
                ax_top.text(finfo['x'], y_text, f"Fill {fill}",
                            ha='center', va='bottom', color='grey',
                            fontsize=13, fontweight='bold')

        ax_top.set_ylabel(r"Fitted Mean Mass $\mu$ [GeV]", fontsize=20)
        ax_top.legend(fontsize=17, loc='upper right')
        ax_top.grid(True, alpha=0.3)
        ax_bot.set_ylabel(r"Fitted Resolution $\sigma/\mu$ [%]", fontsize=20)
        ax_bot.set_xlabel(r"Integrated Luminosity [fb$^{-1}$]", fontsize=20)
        ax_bot.grid(True, alpha=0.3)

        # Ensure x-axis starts at 0 and covers the full range
        if all_sorted_fills:
            max_x = max(f['end'] for f in self.fill_info.values())
            ax_bot.set_xlim(0, max_x * 1.05) # 5% padding

        out = os.path.join(self.base_path, output_file)
        plt.savefig(out, bbox_inches='tight')
        plt.close()
        print(f"\nSaved → {out}")

    def summary_table(self):
        print(f"\n{'Fill':>10}  {'Source':>8}  "
              f"{'μ [GeV]':>12}  {'σ/μ [%]':>12}  {'χ²/ndf':>8}")
        print("─" * 60)
        for fill in sorted(self.fit_results):
            for label in self.SOURCES:
                result = self.fit_results[fill].get(label)
                if result:
                    mu, mu_e, res, res_e, c2 = result
                    print(f"{fill:>10}  {label:>8}  "
                          f"{mu:7.3f}±{mu_e:.3f}  {res:6.3f}±{res_e:.3f}  {c2:8.2f}")


if __name__ == "__main__":
    BASE_DIR = "."
    LUMI_CSV = "lumi_data.csv"

    analyzer = PerFillFitAnalyzer(BASE_DIR, LUMI_CSV)
    analyzer.summary_table()
    analyzer.plot_stability_vs_lumi()
