"""Fit Z-to-ee HLT DQM histograms from DQM_DEST_BASE in pipeline.cfg.

Conditions (folders, colours, markers), the ratio reference and the CMS
label come from the plotting config.  Use --pipeline-cfg for another
pipeline config, or --local for the condition folders in the current
directory.  Plots are saved in PLOTS_DEST from pipeline.cfg (default
DQM_DEST_BASE/plots) or --output-dir, fit sanity checks in its
fit_sanity_checks/ subfolder.
"""

from dqm_runs import DQMRunSelection, add_run_arguments
from luminosity import cms_lumi_label
from plotting_functions import (DCB_PAR_NAMES, ZEE_DQM_PREFIX,
                                ZEE_FIT_RANGE, ZEE_HIST_NAME, ZEE_HIST_SUBPATH,
                                add_common_arguments, cms_text, condition_styles, dcb_background, dcb_func,
                                dcb_signal, extract_run_number, fit_dcb,
                                hlt_input_dir, load_config, lumi_csv_path,
                                make_output_dir)

import argparse
import os

import ROOT
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot

# Set CMS style
plt.style.use(hep.style.CMS)

HIST_PATH = f"{ZEE_DQM_PREFIX}/{ZEE_HIST_SUBPATH}"
FIT_RANGE = ZEE_FIT_RANGE


def get_fit_results(base_path, folder_name, label, output_dir,
                    run_selection=None, run=None, *, lumi_csv, year, com):
    folder_path = os.path.join(base_path, folder_name)
    file_runs = (run_selection.file_runs(label) if run_selection else
                 ((os.path.join(folder_path, f), extract_run_number(f))
                  for f in os.listdir(folder_path) if f.endswith(".root")))
    suffix = "" if run is None else f"_Run{run}"
    combined_hist = None
    contributing_runs = set()

    for path, run_num in file_runs:
        if not run_num: continue
        f = ROOT.TFile.Open(path)
        h = f.Get(f"DQMData/Run {run_num}/{HIST_PATH}")
        if not h:
            f.Close(); continue
        if combined_hist is None:
            combined_hist = h.Clone(f"h_fit_{label}{suffix}")
            combined_hist.SetDirectory(0)
        else:
            combined_hist.Add(h)
        contributing_runs.add(run_num)
        f.Close()

    if combined_hist is None:
        print(f"Warning: no histogram for {label}{suffix}; skipping")
        return None

    fit_min, fit_max = FIT_RANGE
    fit_func = fit_dcb(combined_hist, f"f_{label}{suffix}", FIT_RANGE)

    # --- Sanity Check Plot ---
    sanity_dir = os.path.join(output_dir, "fit_sanity_checks")
    os.makedirs(sanity_dir, exist_ok=True)
    fig_s, (ax_s, ax_p) = plt.subplots(
        2, 1,
        figsize=(10, 10),
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )
    cms_lumi_label(ax_s, {label: contributing_runs}, lumi_csv, data=True,
                   text=f"Sanity Check | {label}" + ("" if run is None else f" | Run {run}"),
                   year=year, com=com)

    # Plot data
    hep.histplot(combined_hist, ax=ax_s, label=f"{label} Data", color='black', histtype='errorbar', marker='o')

    # Plot fit components
    x_plot = np.linspace(fit_min, fit_max, 500)
    params = [fit_func.GetParameter(i) for i in range(9)]
    y_plot_total = [dcb_func([x], params) for x in x_plot]
    y_plot_bkg = [dcb_background(x, params) for x in x_plot]
    y_plot_sig = [dcb_signal(x, params) for x in x_plot]

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
    chi2_ndf = chi2 / ndf if ndf > 0 else 0

    res = (sigma/mean)*100
    res_err = res * np.sqrt((sigma_err/sigma)**2 + (mean_err/mean)**2)

    # Build parameter text box
    stats_text = rf"$\chi^2/ndf = {chi2:.1f}/{ndf} = {chi2_ndf:.2f}$" + "\n"
    stats_text += rf"Res ($\sigma/\mu$): {res:.2f} $\pm$ {res_err:.2f}%" + "\n"
    stats_text += "-"*20 + "\n"
    for i, name in enumerate(DCB_PAR_NAMES):
        stats_text += rf"{name}: {params[i]:.3f} $\pm$ {fit_func.GetParError(i):.3f}" + "\n"

    ax_s.text(0.05, 0.95, stats_text, transform=ax_s.transAxes, fontsize=9,
              verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax_p.set_xlabel("$m_{ee}$ [GeV]", fontsize=15)
    ax_s.set_ylabel("Events", fontsize=15)
    ax_s.legend(loc='upper right')
    ax_s.set_xlim(fit_min, fit_max)

    sanity_path = os.path.join(sanity_dir, f"{label}{suffix}_Fit_Sanity.png")
    fig_s.savefig(sanity_path, bbox_inches='tight')
    plt.close(fig_s)

    return mean, mean_err, res, res_err, chi2_ndf


def plot_comparison(base_dir, config, output_dir, run_selection=None, run=None,
                    *, lumi_csv):
    year = config["cms_label"]["year"]
    com = config["cms_label"]["com"]
    reference = config["reference"]
    sources = condition_styles(config)

    global_histos = {src: None for src in sources}
    contributing_runs = {label: set() for label in sources}
    common_bins = None
    fit_params = {}

    print("Loading data and fitting...")
    for label, info in sources.items():
        folder_path = os.path.join(base_dir, info['folder'])
        file_runs = (run_selection.file_runs(label) if run_selection else
                     ((os.path.join(folder_path, f), extract_run_number(f))
                      for f in sorted(os.listdir(folder_path)) if f.endswith(".root")))

        for path, run_num in file_runs:
            if not run_num: continue
            with uproot.open(path) as f:
                if run_selection:
                    hist_path = f"DQMData/Run {run_num}/{HIST_PATH}"
                    keys = [hist_path] if hist_path in f else []
                else:
                    keys = [k for k in f.keys() if ZEE_HIST_NAME in k]
                if not keys: continue
                h = f[keys[0]]
                if common_bins is None: common_bins = h.axis().edges()
                counts = h.values()
                if global_histos[label] is None: global_histos[label] = np.zeros_like(counts)
                global_histos[label] += counts
                contributing_runs[label].add(run_num)

        result = get_fit_results(base_dir, info['folder'], label, output_dir,
                                 run_selection=run_selection, run=run,
                                 lumi_csv=lumi_csv, year=year, com=com)
        if result is None:
            global_histos[label] = None
            contributing_runs[label].clear()
            continue
        mu, mu_err, res, res_err, chi2_ndf = result
        fit_params[label] = (mu, mu_err, res, res_err)
        print(f"Finished {label} - chi2/ndf: {chi2_ndf:.2f}")

    if not fit_params:
        print("Warning: no condition could be fitted; nothing to plot")
        return

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1,
        figsize=(10, 10),
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )

    # --- Top Plot: Distributions ---
    cms_lumi_label(ax_main, {label: runs for label, runs in contributing_runs.items()
                            if runs}, lumi_csv, data=True, text=cms_text(config),
                   year=year, com=com, fontsize=22)

    if run is not None:
        ax_main.text(0.02, 0.04, f"Run {run}", transform=ax_main.transAxes)

    ref_counts = global_histos.get(reference)

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
    ax_main.set_xlim(*FIT_RANGE)
    ax_main.grid(True, alpha=0.3)

    # --- Bottom Plot: Ratios (X / reference) ---
    if ref_counts is not None:
        bin_centers = (common_bins[:-1] + common_bins[1:]) / 2

        # --- Gray band: statistical uncertainty of the reference ---
        ref_rel_err = np.divide(np.sqrt(ref_counts), ref_counts,
                                out=np.zeros_like(ref_counts),
                                where=ref_counts > 0)
        ax_ratio.fill_between(bin_centers,
                              1 - ref_rel_err,
                              1 + ref_rel_err,
                              step='mid',
                              alpha=0.3,
                              color='gray',
                              label=f'Stat. unc. ({reference})')

        for label, info in sources.items():
            counts = global_histos[label]
            if counts is None: continue

            ratio = np.divide(counts, ref_counts, out=np.full_like(counts, np.nan), where=ref_counts!=0)

            # Propagated uncertainty: sigma_R = R * sqrt(1/N + 1/D)
            # Only shown for non-reference conditions (the reference has the band)
            is_reference = (label == reference)
            err_ratio = ratio * np.sqrt(
                np.divide(1, counts,     out=np.zeros_like(counts), where=counts > 0) +
                np.divide(1, ref_counts, out=np.zeros_like(ref_counts), where=ref_counts > 0)
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
        ax_ratio.legend(fontsize=14, loc='best')

    ax_ratio.axhline(1.0, color='gray', linestyle='--', alpha=0.5)
    ax_ratio.set_ylabel(f"Ratio w.r.t. {reference}", fontsize=20)
    ax_ratio.set_xlabel("$m_{ee}$ [GeV]", fontsize=20)
    ax_ratio.set_ylim(0.0, 2.0)
    ax_ratio.grid(True, alpha=0.3)

    suffix = "" if run is None else f"_Run{run}"
    output = os.path.join(output_dir, f"Zee_Comparison_Final{suffix}.png")
    plt.savefig(output, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_common_arguments(parser)
    add_run_arguments(parser)
    args = parser.parse_args()
    ROOT.gROOT.SetBatch(True)
    try:
        config = load_config(args.config)
        sources = condition_styles(config)
        folders = [info['folder'] for info in sources.values()]
        output_dir = make_output_dir(args.pipeline_cfg, args.local, args.output_dir)
        base_dir = hlt_input_dir(args.pipeline_cfg, folders, local=args.local)
        selecting = args.per_run is not False or args.runs or args.exclude_runs
        for folder in folders:
            if not (base_dir / folder).is_dir() and not selecting:
                raise ValueError(
                    f"DQM input directory not found: {base_dir / folder}. "
                    "Check DQM_DEST_BASE in pipeline.cfg (or the current directory "
                    "with --local).")
        lumi_csv = lumi_csv_path(config, args.lumi_csv)

        selection = None
        if selecting:
            selection = DQMRunSelection(
                {label: str(base_dir / info['folder']) for label, info in sources.items()},
                ZEE_DQM_PREFIX, args.per_run, args.runs, args.exclude_runs)
            runs = selection.runs()
            print("Selected runs: " + ", ".join(map(str, runs)))
        if selection and selection.per_run:
            for run in runs:
                selection.active_run = run
                plot_comparison(base_dir, config, output_dir, selection, run,
                                lumi_csv=lumi_csv)
        else:
            plot_comparison(base_dir, config, output_dir, selection,
                            lumi_csv=lumi_csv)
    except (ValueError, KeyError, OSError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
