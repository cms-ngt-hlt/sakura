import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import os

from scripts import LCTS

plt.style.use(hep.style.CMS)

def get_run_lumi_data(lumi_data_path='lumi.csv', start_run=None):
    """
    Reads lumi CSV and returns a DataFrame with run as index and
    'lumi_center' for the x-axis position.
    - 'lumi_center' is (lumi at start of run) + 0.5 * (lumi for this run)
    - 'start_run' defines the zero-point for the cumulative x-axis.
    - All units are converted to fb^-1.
    """
    
    df_lumi = pd.read_csv(lumi_data_path, comment='#', header=None, dtype=str)
    
    COLUMN_NAMES = [
        'run:fill', 'time', 'nls', 'ncms', 
        'delivered(/ub)', 'recorded(/ub)'
    ]
    
    df_lumi.columns = COLUMN_NAMES[:df_lumi.shape[1]]
    df_lumi['run'] = df_lumi['run:fill'].apply(lambda x: int(x.split(':')[0]))
    
    lumi_column = 'delivered(/ub)'
    df_lumi[lumi_column] = pd.to_numeric(df_lumi[lumi_column], errors='coerce')
    
    run_lumi_sorted = df_lumi.groupby('run')[lumi_column].sum().sort_index()
    cumulative_lumi_at_end = run_lumi_sorted.cumsum()
    cumulative_lumi_at_start = cumulative_lumi_at_end.shift(1).fillna(0)
    
    if start_run is not None:
        if start_run in cumulative_lumi_at_start.index:
            offset = cumulative_lumi_at_start[start_run] 
            cumulative_lumi_at_start = cumulative_lumi_at_start - offset
        else:
            print(f"⚠️ Warning: start_run {start_run} not found in luminosity data")
    
    lumi_half_width = 0.5 * run_lumi_sorted
    lumi_center = cumulative_lumi_at_start + lumi_half_width
    
    CONV_FACTOR = 1e-9  # (1 ub^-1 = 1e-9 fb^-1)
    
    lumi_df = pd.DataFrame({
        'lumi_center': lumi_center * CONV_FACTOR,
    })
    
    print("Luminosity data (center) processed in fb^-1.")
    return lumi_df



def get_fill_boundary_lines(lumi_data_path='lumi.csv', start_run=None, plotted_runs_set=None):
    """
    Calculates the cumulative luminosity at the end of each *plotted* fill.
    Returns a list of luminosity values (in fb^-1) for drawing vlines.
    """

    df_lumi = pd.read_csv(lumi_data_path, comment='#', header=None, dtype=str)
    COLUMN_NAMES = [
        'run:fill', 'time', 'nls', 'ncms', 
        'delivered(/ub)', 'recorded(/ub)'
    ]
    df_lumi.columns = COLUMN_NAMES[:df_lumi.shape[1]]
    df_lumi['run'] = df_lumi['run:fill'].apply(lambda x: int(x.split(':')[0]))
    df_lumi['fill'] = df_lumi['run:fill'].apply(lambda x: int(x.split(':')[1]))
    lumi_column = 'delivered(/ub)'
    df_lumi[lumi_column] = pd.to_numeric(df_lumi[lumi_column], errors='coerce')
    df_lumi = df_lumi.sort_values('run')
    run_to_fill = df_lumi.groupby('run')['fill'].first()
    
    local_plotted_fills_set = set()
    if plotted_runs_set:
        for run in plotted_runs_set:
            if run in run_to_fill:
                local_plotted_fills_set.add(run_to_fill[run])
        print(f"Identified {len(local_plotted_fills_set)} fills with data: {sorted(list(local_plotted_fills_set))}")
    else:
        local_plotted_fills_set = set(run_to_fill.unique())
        print("Warning: No plotted_runs_set provided, will draw all fills from CSV.")
    
    run_lumi = df_lumi.groupby('run')[lumi_column].sum().sort_index()
    cumulative_lumi = run_lumi.cumsum()
    
    cumulative_lumi_at_start = cumulative_lumi.shift(1).fillna(0)
    offset = 0.0
    if start_run is not None:
        if start_run in cumulative_lumi_at_start.index:
            offset = cumulative_lumi_at_start[start_run] 
            cumulative_lumi = cumulative_lumi - offset
        else:
            print(f"⚠️ Warning: start_run {start_run} not found in luminosity data")
    
    fill_changes = run_to_fill != run_to_fill.shift(1)
    fill_starts = run_to_fill[fill_changes].index.tolist()
    
    fill_boundaries_lumi = []
    
    for i, start_run_of_fill in enumerate(fill_starts):
        fill_num = run_to_fill[start_run_of_fill]
        if fill_num not in local_plotted_fills_set:
            continue

        prev_fill_start_run = None
        for j in range(i - 1, -1, -1):
            if run_to_fill[fill_starts[j]] in local_plotted_fills_set:
                prev_fill_start_run = fill_starts[j]
                break
        
        if prev_fill_start_run is None:
            continue 

        prev_fill_num = run_to_fill[prev_fill_start_run]
        prev_fill_runs = run_to_fill[run_to_fill == prev_fill_num].index
        prev_fill_end_run = prev_fill_runs.max()
        boundary_lumi = cumulative_lumi[prev_fill_end_run]
        fill_boundaries_lumi.append(boundary_lumi)
    
    CONV_FACTOR = 1e-9
    fill_boundaries_lumi_fb = [l * CONV_FACTOR for l in fill_boundaries_lumi]
    
    return fill_boundaries_lumi_fb


def calculate_ratio_with_error(mu, mu_err, sigma, sigma_err):
    """
    Calculates the ratio R = sigma / mu and its error.
    """
    mu = np.array(mu)
    mu_err = np.array(mu_err)
    sigma = np.array(sigma)
    sigma_err = np.array(sigma_err)
    ratio = np.where(mu != 0, sigma / mu, np.nan)
    rel_err_mu = np.where(mu != 0, mu_err / mu, np.nan)
    rel_err_sigma = np.where(sigma != 0, sigma_err / sigma, np.nan)

    ratio_err = ratio * np.sqrt(
        np.square(rel_err_mu) + np.square(rel_err_sigma)
    )

    return ratio, ratio_err


def plot_stability_comparison():
    """
    Generates the 2-panel stability plot for mu and sigma/mu.
    """
    print("Loading data for stability plot (this may take a moment)...")
    
    off = LCTS('HLTTag')
    prompt = LCTS('Prompt')
    lcped = LCTS('HLT-LCPed')
    print("Data loading complete.")

    all_plotted_runs = set(off.rnms) | set(prompt.rnms) | set(lcped.rnms)
    print(f"Found {len(all_plotted_runs)} total runs with data.")

    START_RUN = 386478  # First run in data (adjust as needed)
    
    lumi_df = get_run_lumi_data(start_run=START_RUN)
    
    fill_boundaries = get_fill_boundary_lines(
        start_run=START_RUN, 
        plotted_runs_set=all_plotted_runs
    )
    print(f"Found {len(fill_boundaries)} fill boundaries to draw.")
    
    if lumi_df.empty:
        print("🛑 No luminosity data found, cannot generate plot.")
        return

    x_off = lumi_df.reindex(off.rnms)['lumi_center'].values
    x_prompt = lumi_df.reindex(prompt.rnms)['lumi_center'].values
    x_lcped = lumi_df.reindex(lcped.rnms)['lumi_center'].values

    ratio_off, err_ratio_off = calculate_ratio_with_error(
        off.fit_mus, off.fit_mu_errors, off.fit_sigmas, off.fit_sigma_errors
    )
    ratio_prompt, err_ratio_prompt = calculate_ratio_with_error(
        prompt.fit_mus, prompt.fit_mu_errors, prompt.fit_sigmas, prompt.fit_sigma_errors
    )
    ratio_lcped, err_ratio_lcped = calculate_ratio_with_error(
        lcped.fit_mus, lcped.fit_mu_errors, lcped.fit_sigmas, lcped.fit_sigma_errors
    )

    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(12, 12),
        sharex=True,
        gridspec_kw={'height_ratios': [2, 1]}, 
    )
    hep.cms.label("Preliminary", data=True, year="Sep 30 - Oct 23, 2024", com=13.6, ax=ax1, loc=0)

    for i, boundary_lumi in enumerate(fill_boundaries):
        label = 'Fill Boundary' if i == 0 else None
        ax1.axvline(boundary_lumi, color='grey', linestyle='--', linewidth=1, label=label)
        ax2.axvline(boundary_lumi, color='grey', linestyle='--', linewidth=1)
    
    ax1.errorbar(
        x_off, off.fit_mus, yerr=off.fit_mu_errors,
        fmt='o', color='#5790fc', ecolor='#5790fc',
        elinewidth=1.5, capsize=6, label=r'HLT conditions',
    )
    ax1.errorbar(
        x_prompt, prompt.fit_mus, yerr=prompt.fit_mu_errors,
        fmt='v', color='#f89c20', ecolor='#f89c20',
        elinewidth=1.5, capsize=4, label=r'Prompt conditions',
    )
    ax1.errorbar(
        x_lcped, lcped.fit_mus, yerr=lcped.fit_mu_errors,
        fmt='D', color='#e42536', ecolor='#e42536',
        elinewidth=1.5, capsize=4, label=r'HLT+Prompt LC and Prompt Ped',
    )
    ax1.set_ylabel(r'$\mu$ [GeV]')
    
    ax2.errorbar(
        x_off, ratio_off, yerr=err_ratio_off,
        fmt='o', color='#5790fc', ecolor='#5790fc',
        elinewidth=1.5, capsize=6, label=r'HLT',
    )
    ax2.errorbar(
        x_prompt, ratio_prompt, yerr=err_ratio_prompt,
        fmt='v', color='#f89c20', ecolor='#f89c20',
        elinewidth=1.5, capsize=4, label=r'Prompt',
    )
    ax2.errorbar(
        x_lcped, ratio_lcped, yerr=err_ratio_lcped,
        fmt='D', color='#e42536', ecolor='#e42536',
        elinewidth=1.5, capsize=4, label=r'HLT+Prompt LC and Prompt Ped',
    )
    
    ax2.set_xlabel(r'Delivered Integrated Luminosity [$fb^{-1}$]', weight='bold')
    ax2.set_ylabel(r'$\sigma / \mu$') 
    
    leg = ax1.legend(
        loc='lower right', 
        fontsize='small',
        frameon=True,
        facecolor='white',
        edgecolor='black'
    )

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig("stability_comparison_sigma_over_mu.pdf", dpi=300)
    print("✅ Stability plot saved as stability_comparison_sigma_over_mu.pdf")
    plt.show()


if __name__ == "__main__":
    print("--- Generating Stability Comparison Plot (mu and sigma/mu) ---")
    plot_stability_comparison()
    print("\n--- All plots generated. ---")
