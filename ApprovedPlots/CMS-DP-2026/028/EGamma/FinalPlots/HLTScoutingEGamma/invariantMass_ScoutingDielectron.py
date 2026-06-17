import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import sys
import glob
import os
import mplhep as hep
from matplotlib.lines import Line2D

plt.style.use(hep.style.CMS)
plt.rcParams.update({'font.size': 20})


files_config = [
    {"label": "Prompt Conditions", "path": "Prompt", "color": "black",  "style": "-"},
    {"label": "HLT Conditions",    "path": "HLT",    "color": "#5790fc", "style": "--"},
    {"label": "NGT Conditions",    "path": "NGT",    "color": "#f89c20", "style": ":"}
]


partial_path_suffix = "HLT/Run summary/ScoutingOnline/DiLepton"


def get_base_dir(file_handle):
    """
    Finds the run-dependent path inside a ROOT file.
    Example: DQMData/Run 398827/HLT/Run summary/ScoutingOnline/DiLepton
    """
    if "DQMData" not in file_handle:
        return None
    dqm_keys = file_handle["DQMData"].keys(cycle=False)

    run_folder = next((k for k in dqm_keys if "Run " in k), None)

    if run_folder:
        full_path = f"DQMData/{run_folder}/{partial_path_suffix}"
        if full_path in file_handle:
            return file_handle[full_path]
    return None


def fetch_and_sum(dir_list, key):
    """
    Aggregates 1D histograms from multiple files for a specific key.
    Returns: (values, edges) or None if nothing found.
    """
    sum_values = None
    edges      = None
    found_any  = False

    for d in dir_list:
        if d is None:
            continue
        try:
            if key in d:
                obj        = d[key]
                data       = obj.to_numpy()
                if len(data) != 2:   # skip anything that isn't 1D
                    continue
                vals, edg  = data[0], data[1]
                if not found_any:
                    sum_values = np.array(vals, dtype=float)
                    edges      = edg
                    found_any  = True
                else:
                    if vals.shape == sum_values.shape:
                        sum_values += vals
        except Exception:
            continue

    if not found_any:
        return None

    return (sum_values, edges)


def rebin_hist(agg_data):
    """
    Reduces the number of bins by half by merging adjacent bins.
    """
    if agg_data is None:
        return None

    values, edges = agg_data

    # Merge every 2 bins
    if len(values) % 2 != 0:
        values = values[:-1]
        edges  = edges[:-1]

    new_values = values.reshape(-1, 2).sum(axis=1)
    new_edges  = edges[::2]
    return (new_values, new_edges)


def plot_comparison(plot_name, hist_data_list, pdf_pages):
    """
    Generates the comparison plot with:
      - Main panel: all three distributions with statistical error bars
      - Ratio panel: HLT/Prompt and NGT/Prompt with propagated error bars,
                     plus a gray band showing the statistical uncertainty of
                     the Prompt reference.
    """
    valid_items = [h for h in hist_data_list if h['data'] is not None]
    if not valid_items:
        return

    clean_title = plot_name.split("/")[-1]

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1,
        figsize=(10, 10),
        sharex=True,
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )

    hep.cms.label(ax=ax_main, data=True, label="Preliminary", year=2025,
                  lumi=2.09, com=13.6, fontsize=22)

    max_y      = 0
    ref_values = None
    ref_edges  = None

    # Extract reference (Prompt) data
    if hist_data_list[0]['data'] is not None:
        ref_values, ref_edges = hist_data_list[0]['data']

        # Gray band: statistical uncertainty of the Prompt reference
        ref_rel_err = np.divide(np.sqrt(ref_values), ref_values,
                                out=np.zeros_like(ref_values),
                                where=ref_values > 0)

        bin_centers = 0.5 * (ref_edges[:-1] + ref_edges[1:])
        ax_ratio.fill_between(bin_centers,
                              1 - ref_rel_err,
                              1 + ref_rel_err,
                              step='mid',
                              alpha=0.3,
                              color='gray',
                              label='Stat. unc. (Prompt)')

    # Main panel + ratio panel per sample
    for item in hist_data_list:
        if item['data'] is None:
            continue

        values, edges = item['data']
        if np.sum(values) == 0:
            continue

        current_max = np.max(values)
        if current_max > max_y:
            max_y = current_max

        # Main plot with statistical error bars (sqrt(N))
        hep.histplot(values, bins=edges, ax=ax_main,
                     label=item['label'], color=item['color'],
                     linestyle=item['style'], linewidth=2, yerr=True)

        # Ratio plot
        if ref_values is not None and len(values) == len(ref_values):
            ratio = np.divide(values, ref_values,
                              out=np.full_like(values, np.nan),
                              where=ref_values != 0)

            # Propagated uncertainty: sigma_R = R * sqrt(1/N + 1/D)
            err_ratio = ratio * np.sqrt(
                np.divide(1, values,     out=np.zeros_like(values),     where=values     > 0) +
                np.divide(1, ref_values, out=np.zeros_like(ref_values), where=ref_values > 0)
            )

            is_reference = (item['label'] == hist_data_list[0]['label'])

            # Adaptive marker size: 600 / num_bins
            ms = 600 / len(edges) if len(edges) > 0 else 8

            hep.histplot(ratio, bins=edges, ax=ax_ratio,
                         color=item['color'], linestyle='none',
                         histtype='errorbar', marker='_',
                         markersize=ms, markeredgewidth=2,
                         yerr=err_ratio if not is_reference else False)

    ax_main.set_ylabel("Number of Dielectron Candidates", fontsize=20)

    header = Line2D([], [], color='none', label=r'$\bf{HLT\ Scouting}$')
    handles, labels = ax_main.get_legend_handles_labels()
    ax_main.legend(
        handles=[header] + handles,
        labels=[r'$\bf{HLT\ Scouting}$'] + labels,
        fontsize=18,
        loc='best'
    )

    if max_y > 100:
        ax_main.set_yscale('log')
    else:
        ax_main.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax_main.yaxis.get_offset_text().set_fontsize(18)
        ax_main.yaxis.get_offset_text().set_x(-0.06)
    ax_main.grid(True, linestyle='--', alpha=0.3)

    ax_ratio.axhline(1.0, color='gray', linestyle='--', linewidth=1)
    ax_ratio.set_ylabel("Ratio w.r.t. Prompt", fontsize=20)
    ax_ratio.set_ylim(0.0, 2.0)
    ax_ratio.grid(True, linestyle='--', alpha=0.3)
    ax_ratio.legend(fontsize=14, loc='best')

    ax_ratio.set_xlabel(r"$m_{ee}$ [GeV]", fontsize=20)
    if ref_edges is not None:
        ax_main.set_xlim(ref_edges[0], ref_edges[-1])

    pdf_pages.savefig(fig, bbox_inches='tight')
    fig.savefig(f"{clean_title}_rebin_err.png", bbox_inches='tight')
    fig.savefig(f"{clean_title}_rebin_err.pdf", bbox_inches='tight')
    plt.close(fig)


def traverse_and_compare(structure_keys, open_configs, current_path, pdf_pages):
    """
    Recursive function to walk through the ROOT directories.
    """
    subfolders = []
    plots      = []

    master_dir_list = open_configs[0]['dirs']
    master_example  = next((d for d in master_dir_list if d is not None), None)
    if master_example is None:
        return

    # Sort keys into folders vs histograms
    for key in structure_keys:
        if "/" in key:
            continue
        try:
            obj = master_example[key]
            if hasattr(obj, "keys"):
                subfolders.append(key)
            elif hasattr(obj, "to_numpy"):
                plots.append(key)
        except Exception:
            continue

    if plots:
        print(f"   [Plotting] Found {len(plots)} histograms in {current_path.split('/')[-1]}")

    for plot_key in plots:
        hist_list = []
        for cfg in open_configs:
            agg_data = fetch_and_sum(cfg['dirs'], plot_key)
            agg_data = rebin_hist(agg_data)
            hist_list.append({
                "label": cfg['label'],
                "color": cfg['color'],
                "style": cfg['style'],
                "data":  agg_data
            })
        plot_comparison(f"{current_path}/{plot_key}", hist_list, pdf_pages)

    for folder_key in subfolders:
        new_configs = []
        for cfg in open_configs:
            new_dir_list = []
            for d in cfg['dirs']:
                sub_d = d[folder_key] if (d and folder_key in d) else None
                new_dir_list.append(sub_d)
            new_configs.append({
                "label": cfg['label'],
                "color": cfg['color'],
                "style": cfg['style'],
                "dirs":  new_dir_list
            })

        next_master_list = new_configs[0]['dirs']
        next_example     = next((d for d in next_master_list if d is not None), None)
        if next_example:
            next_keys = next_example.keys(cycle=False)
            print(f" > Entering subfolder: {folder_key}")
            traverse_and_compare(next_keys, new_configs,
                                 f"{current_path}/{folder_key}", pdf_pages)


if __name__ == "__main__":
    try:
        active_configs   = []
        all_file_handles = []

        print(f"--- Starting Analysis (Rebinned with Errors) ---")
        print(f"Target Path: {partial_path_suffix}")

        for cfg in files_config:
            dir_path = cfg['path']
            files    = glob.glob(os.path.join(dir_path, "*.root"))

            if not files:
                print(f"WARNING: No .root files found in {dir_path}")
                continue

            print(f"Tag '{cfg['label']}': Found {len(files)} files in {dir_path}")

            tag_dirs = []
            for fname in files:
                try:
                    f    = uproot.open(fname)
                    base = get_base_dir(f)
                    all_file_handles.append(f)
                    tag_dirs.append(base)
                except Exception as e:
                    print(f"Error reading {fname}: {e}")
                    tag_dirs.append(None)

            active_configs.append({
                "label": cfg['label'],
                "color": cfg['color'],
                "style": cfg['style'],
                "dirs":  tag_dirs
            })

        if not active_configs or not active_configs[0]['dirs']:
            print("ERROR: Reference tag has no valid files or path is incorrect.")
            sys.exit(1)

        master_roots = active_configs[0]['dirs']
        master_root  = next((d for d in master_roots if d is not None), None)

        if not master_root:
            print(f"ERROR: Could not find '{partial_path_suffix}' in the reference files.")
            sys.exit(1)

        master_keys  = master_root.keys(cycle=False)
        pdf_filename = "Comparison_DiLepton_rebin_err.pdf"

        print(f"\n--- Generating Rebinned Plots with Error Bands into {pdf_filename} ---")

        with PdfPages(pdf_filename) as pdf:
            traverse_and_compare(master_keys, active_configs, "DiLepton", pdf)

        print(f"\nSUCCESS: Analysis Complete. Saved to {pdf_filename}")

    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()