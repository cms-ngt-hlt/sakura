import ROOT
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot

# Set CMS style
plt.style.use(hep.style.CMS)

def extract_run_number(filename):
    match = re.search(r'_R(\d+)\.root', filename)
    return int(match.group(1)) if match else None

def dcb_func(x, p):
    xx = x[0]
    mean, sigma = p[3], p[4]
    aL, nL, aH, nH = abs(p[5]), p[6], abs(p[7]), p[8]
    t = (xx - mean) / sigma
    bkg = p[0] * np.exp(p[1] * xx)
    if t > -aL and t < aH:
        return p[2] * np.exp(-0.5 * t**2) + bkg
    elif t <= -aL:
        A = (nL / aL)**nL * np.exp(-0.5 * aL**2)
        B = nL / aL - aL
        return p[2] * A * (B - t)**(-nL) + bkg
    else:
        A = (nH / aH)**nH * np.exp(-0.5 * aH**2)
        B = nH / aH - aH
        return p[2] * A * (B + t)**(-nH) + bkg

def get_fit_results(base_path, folder_name, label):
    folder_path = os.path.join(base_path, folder_name)
    files = [f for f in os.listdir(folder_path) if f.endswith(".root")]
    combined_hist = None
    
    for item in files:
        run_num = extract_run_number(item)
        if not run_num: continue
        f = ROOT.TFile.Open(os.path.join(folder_path, item))
        h = f.Get(f"DQMData/Run {run_num}/HLT/Run summary/ObjectMonitor/MainShifter/di-Electron_Mass")
        if not h: 
            f.Close(); continue
        if combined_hist is None:
            combined_hist = h.Clone(f"h_fit_{label}")
            combined_hist.SetDirectory(0)
        else:
            combined_hist.Add(h)
        f.Close()
    
    fit_min, fit_max = 60, 120
    fit_func = ROOT.TF1(f"f_{label}", dcb_func, fit_min, fit_max, 9)
    peak_val = combined_hist.GetMaximum()
    peak_x = combined_hist.GetXaxis().GetBinCenter(combined_hist.GetMaximumBin())
    
    # Standardized initial parameters for all sources
    fit_func.SetParameters(peak_val*0.05, -0.04, peak_val, peak_x, 3.0, 1.5, 5.0, 1.5, 5.0)
    
    # Relaxed limits to allow the optimizer more room
    fit_func.SetParLimits(0, 0, peak_val)
    fit_func.SetParLimits(1, -0.8, 0.0)
    fit_func.SetParLimits(2, peak_val*0.01, peak_val*5.0)
    # Dynamic limits for Mean (p[3]) around the detected peak
    fit_func.SetParLimits(3, peak_x - 5.0, peak_x + 5.0)
    fit_func.SetParLimits(4, 0.5, 8.0)
    fit_func.SetParLimits(5, 0.1, 10.0); fit_func.SetParLimits(6, 1.01, 100.0)
    fit_func.SetParLimits(7, 0.1, 10.0); fit_func.SetParLimits(8, 1.01, 100.0)
    
    combined_hist.Fit(fit_func, "SRLIMQ", "", fit_min, fit_max)
    
    # --- Sanity Check Plot ---
    os.makedirs(os.path.join(base_path, "fit_sanity_checks"), exist_ok=True)
    fig_s, (ax_s, ax_p) = plt.subplots(
        2, 1, 
        figsize=(10, 10), 
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )
    hep.cms.label(ax=ax_s, data=True, text="Sanity Check", year=2025, label=label)
    
    # Plot data
    hep.histplot(combined_hist, ax=ax_s, label=f"{label} Data", color='black', histtype='errorbar', marker='o')
    
    # Plot fit components
    x_plot = np.linspace(fit_min, fit_max, 500)
    params = [fit_func.GetParameter(i) for i in range(9)]
    y_plot_total = [dcb_func([x], params) for x in x_plot]
    
    # Helper to calculate individual components
    def bkg_val(x, p): return p[0] * np.exp(p[1] * x)
    def sig_val(x, p):
        mean, sigma = p[3], p[4]
        aL, nL, aH, nH = abs(p[5]), p[6], abs(p[7]), p[8]
        t = (x - mean) / sigma
        if t > -aL and t < aH: return p[2] * np.exp(-0.5 * t**2)
        elif t <= -aL:
            A = (nL / aL)**nL * np.exp(-0.5 * aL**2)
            B = nL / aL - aL
            return p[2] * A * (B - t)**(-nL)
        else:
            A = (nH / aH)**nH * np.exp(-0.5 * aH**2)
            B = nH / aH - aH
            return p[2] * A * (B + t)**(-nH)

    y_plot_bkg = [bkg_val(x, params) for x in x_plot]
    y_plot_sig = [sig_val(x, params) for x in x_plot]

    ax_s.plot(x_plot, y_plot_total, color='red', label='Total Fit (DCB + Exp)', linewidth=3)
    ax_s.plot(x_plot, y_plot_sig, color='blue', linestyle='--', label='Signal (DCB)', linewidth=2)
    ax_s.plot(x_plot, y_plot_bkg, color='green', linestyle=':', label='Background (Exp)', linewidth=2)
    
    # --- Pull Plot Calculation ---
    pull_x = []
    pull_y = []
    for i in range(1, combined_hist.GetNbinsX() + 1):
        x = combined_hist.GetBinCenter(i)
        if x < fit_min or x > fit_max: continue
        val = combined_hist.GetBinContent(i)
        err = combined_hist.GetBinError(i)
        f_val = fit_func.Eval(x)
        if err > 0:
            pull_x.append(x)
            pull_y.append((val - f_val) / err)
    
    ax_p.errorbar(pull_x, pull_y, yerr=1, fmt='o', color='black', markersize=4, capsize=0)
    ax_p.axhline(0, color='red', linestyle='-')
    ax_p.axhline(1, color='gray', linestyle='--', alpha=0.5)
    ax_p.axhline(-1, color='gray', linestyle='--', alpha=0.5)
    ax_p.axhline(2, color='gray', linestyle=':', alpha=0.3)
    ax_p.axhline(-2, color='gray', linestyle=':', alpha=0.3)
    ax_p.set_ylabel("Pull", fontsize=15)
    
    # Free range: autoscale with a bit of padding
    if pull_y:
        max_pull = max(abs(min(pull_y)), abs(max(pull_y)))
        ax_p.set_ylim(-max_pull * 1.2, max_pull * 1.2)
    
    ax_p.grid(True, alpha=0.3)

    # Extract results
    mean = fit_func.GetParameter(3); mean_err = fit_func.GetParError(3)
    sigma = fit_func.GetParameter(4); sigma_err = fit_func.GetParError(4)
    chi2 = fit_func.GetChisquare()
    ndf = fit_func.GetNDF()
    
    res = (sigma/mean)*100
    res_err = res * np.sqrt((sigma_err/sigma)**2 + (mean_err/mean)**2)

    # Build parameter text box
    par_names = ["Bkg C0", "Bkg C1", "Sig Norm", "Mean", "Sigma", "aL", "nL", "aH", "nH"]
    chi2_val = chi2 / ndf if ndf > 0 else 0
    stats_text = rf"$\chi^2/ndf = {chi2:.1f}/{ndf} = {chi2_val:.2f}$" + "\n"
    stats_text += rf"Res ($\sigma/\mu$): {res:.2f} $\pm$ {res_err:.2f}%" + "\n"
    stats_text += "-"*20 + "\n"
    for i in range(9):
        val = fit_func.GetParameter(i)
        err = fit_func.GetParError(i)
        stats_text += rf"{par_names[i]}: {val:.3f} $\pm$ {err:.3f}" + "\n"
    
    ax_s.text(0.05, 0.95, stats_text, transform=ax_s.transAxes, fontsize=9,
              verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    ax_p.set_xlabel("$m_{ee}$ [GeV]", fontsize=15)
    ax_s.set_ylabel("Events", fontsize=15)
    ax_s.legend(loc='upper right')
    ax_s.set_xlim(fit_min, fit_max)
    
    sanity_path = os.path.join(base_path, "fit_sanity_checks", f"{label}_Fit_Sanity.png")
    fig_s.savefig(sanity_path, bbox_inches='tight')
    plt.close(fig_s)
    
    res = (sigma/mean)*100
    res_err = res * np.sqrt((sigma_err/sigma)**2 + (mean_err/mean)**2)
    
    return mean, mean_err, res, res_err, chi2/ndf

def main():
    ROOT.gROOT.SetBatch(True)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    sources = {
        'HLT':    {'folder': 'HLT',    'color': '#5790fc', 'marker': 'o'},
        'NGT':    {'folder': 'NGT',    'color': '#f89c20', 'marker': 'D'},
        'Prompt': {'folder': 'Prompt', 'color': 'black',   'marker': 'v'}
    }
    
    global_histos = {src: None for src in sources}
    common_bins = None
    fit_params = {}

    print("Loading data and fitting...")
    for label, info in sources.items():
        folder_path = os.path.join(base_dir, info['folder'])
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".root")])
        
        for item in files:
            run_num = extract_run_number(item)
            if not run_num: continue
            with uproot.open(os.path.join(folder_path, item)) as f:
                keys = [k for k in f.keys() if "di-Electron_Mass" in k]
                if not keys: continue
                h = f[keys[0]]
                if common_bins is None: common_bins = h.axis().edges()
                counts = h.values()
                if global_histos[label] is None: global_histos[label] = np.zeros_like(counts)
                global_histos[label] += counts
        
        mu, mu_err, res, res_err, chi2_ndf = get_fit_results(base_dir, info['folder'], label)
        fit_params[label] = (mu, mu_err, res, res_err)
        print(f"Finished {label} - chi2/ndf: {chi2_ndf:.2f}")

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, 
        figsize=(10, 10), 
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )

    # --- Top Plot: Distributions ---
    hep.cms.label(ax=ax_main, data=True, text="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=22)

    prompt_counts = global_histos.get('Prompt')

    for label, info in sources.items():
        counts = global_histos[label]
        if counts is None: continue
        
        mu, mu_err, res, res_err = fit_params[label]
        res_label = f"{label} Conditions\n" + rf"$\sigma/\mu = {res:.2f} \pm {res_err:.2f}\%$"

        # 1. Plot the histogram step line
        hep.histplot(
            counts,
            bins=common_bins,
            color=info['color'],
            yerr=False,
            histtype='step',
            linewidth=2,
            ax=ax_main
        )

        # 2. Plot the markers and error bars
        hep.histplot(
            counts,
            bins=common_bins,
            label=res_label,
            color=info['color'],
            marker=info['marker'],
            markersize=10,        # Explicitly set to match original visual weight
            yerr=True,
            histtype='errorbar',
            linewidth=0,          
            ax=ax_main
        )

    ax_main.set_ylabel("Number of Dielectron Candidates", fontsize=20)
    ax_main.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax_main.yaxis.get_offset_text().set_ha('left')
    ax_main.yaxis.get_offset_text().set_x(-0.07) 
    
    ax_main.legend(fontsize=18, loc='upper right')
    ax_main.set_xlim(60, 120)
    ax_main.grid(True, alpha=0.3)

    # --- Bottom Plot: Ratios (X / Prompt) ---
    if prompt_counts is not None:
        valid_mask = prompt_counts > 0
        bin_centers = (common_bins[:-1] + common_bins[1:]) / 2

        # --- Gray band: statistical uncertainty of the Prompt reference ---
        ref_rel_err = np.divide(np.sqrt(prompt_counts), prompt_counts,
                                out=np.zeros_like(prompt_counts),
                                where=prompt_counts > 0)
        ax_ratio.fill_between(bin_centers,
                              1 - ref_rel_err,
                              1 + ref_rel_err,
                              step='mid',
                              alpha=0.3,
                              color='gray',
                              label='Stat. unc. (Prompt)')

        for label, info in sources.items():
            counts = global_histos[label]
            if counts is None: continue

            ratio = np.divide(counts, prompt_counts, out=np.full_like(counts, np.nan), where=prompt_counts!=0)

            # Propagated uncertainty: sigma_R = R * sqrt(1/N + 1/D)
            # Only add for non-reference items (NGT, HLT)
            is_reference = (label == 'Prompt')
            err_ratio = ratio * np.sqrt(
                np.divide(1, counts,        out=np.zeros_like(counts), where=counts > 0) +
                np.divide(1, prompt_counts, out=np.zeros_like(prompt_counts), where=prompt_counts > 0)
            )

            hep.histplot(                
                ratio,
                bins=common_bins,
                color=info['color'],
                yerr=err_ratio if not is_reference else False,
                histtype='errorbar',
                marker='_',
                markersize=12,
                linewidth=0, 
                markeredgewidth=2,
                ax=ax_ratio
            )

    ax_ratio.axhline(1.0, color='gray', linestyle='--', alpha=0.5)
    ax_ratio.set_ylabel("Ratio w.r.t. Prompt", fontsize=20)
    ax_ratio.set_xlabel("$m_{ee} [GeV]$ ", fontsize=20)
    ax_ratio.set_ylim(0.0, 2.0)
    ax_ratio.grid(True, alpha=0.3)
    ax_ratio.legend(fontsize=14, loc='best')

    ax_ratio.grid(True, alpha=0.3)
    
    plt.savefig("Zee_Comparison_Final.png", bbox_inches='tight')
    print("Saved Zee_Comparison_Final.png")


if __name__ == "__main__":
    main()
