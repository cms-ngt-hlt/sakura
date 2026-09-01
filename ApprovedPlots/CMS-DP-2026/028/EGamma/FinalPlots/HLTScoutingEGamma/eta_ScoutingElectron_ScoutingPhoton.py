import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob
import os
import mplhep as hep
from matplotlib.lines import Line2D

# Set CMS style
plt.style.use(hep.style.CMS)


files_config = [
    {"label": "Prompt Conditions", "path": "Prompt", "color": "black",  "style": "-"},
    {"label": "HLT Conditions",    "path": "HLT",    "color": "#5790fc", "style": "--"},
    {"label": "NGT Conditions",    "path": "NGT",    "color": "#f89c20", "style": ":"}
]

# Specific histograms for Eta
target_histograms = [
    {"category": "Electron", "hist_name": "eta_ele", "label": "Electrons"},
    {"category": "Photon",   "hist_name": "eta_pho", "label": "Photons"}
]

output_pdf = "Comparison_Eta_Plots.pdf"


def get_base_dir(file_handle, category):
    if "DQMData" not in file_handle: return None
    dqm_keys = file_handle["DQMData"].keys(cycle=False)
    run_folder = next((k for k in dqm_keys if "Run " in k), None)
    
    if run_folder:
        full_path = f"DQMData/{run_folder}/HLT/Run summary/ScoutingOnline/Miscellaneous/{category}"
        if full_path in file_handle:
            return file_handle[full_path]
    return None

def fetch_and_sum(dir_list, key):
    sum_values = None
    edges = None
    found_any = False

    for d in dir_list:
        if d is None: continue
        try:
            if key in d:
                obj = d[key]
                data = obj.to_numpy()
                if not found_any:
                    sum_values = np.array(data[0], dtype=float)
                    edges = data[1]
                    found_any = True
                else:
                    if data[0].shape == sum_values.shape:
                        sum_values += data[0]
        except Exception:
            continue
    return (sum_values, edges) if found_any else None

def plot_comparison(hist_info, hist_data_list, pdf_pages):
    valid_items = [h for h in hist_data_list if h['data'] is not None]
    if not valid_items: return

    hist_name = hist_info['hist_name']
    label_type = hist_info['label']

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, 
        figsize=(10, 10), 
        sharex=True, 
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )
    
    # CMS Label
    hep.cms.label(ax=ax_main, data=True, label="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=22)
    
    max_y = 0
    ref_values = None
    ref_edges = None
    if hist_data_list[0]['data'] is not None:
        ref_values = hist_data_list[0]['data'][0]
        ref_edges = hist_data_list[0]['data'][1]

    if ref_values is not None:
        # --- Gray band: statistical uncertainty of the Prompt reference ---
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

    for item in hist_data_list:
        if item['data'] is None: continue
        values, edges = item['data']
        if np.sum(values) == 0: continue 

        current_max = np.max(values)
        if current_max > max_y: max_y = current_max

        hep.histplot(values, bins=edges, ax=ax_main, 
                     label=item['label'], color=item['color'], 
                     linestyle=item['style'], linewidth=2, yerr=True)

        if ref_values is not None and len(values) == len(ref_values):
            ratio = np.divide(values, ref_values, out=np.full_like(values, np.nan), where=ref_values!=0)
            
            # Propagated uncertainty: sigma_R = R * sqrt(1/N + 1/D)
            err_ratio = ratio * np.sqrt(
                np.divide(1, values,     out=np.zeros_like(values),     where=values     > 0) +
                np.divide(1, ref_values, out=np.zeros_like(ref_values), where=ref_values > 0)
            )
            
            is_reference = (item['label'] == hist_data_list[0]['label'])
            ms = 600 / len(edges) if len(edges) > 0 else 4

            hep.histplot(ratio, bins=edges, ax=ax_ratio,
                         color=item['color'], linestyle='none',
                         histtype='errorbar', marker='_', markersize=ms, markeredgewidth=2, 
                         yerr=err_ratio if not is_reference else False)

    # Specific formatting for Electron vs Photon Eta
    ax_main.set_ylabel(f"Number of {label_type}", fontsize=20)
    
    if hist_name == "eta_ele":
        ax_main.set_ylim(0, 17000)
        ax_ratio.set_ylim(0.75, 1.15)
        leg_loc = 'best'
    elif hist_name == "eta_pho":
        ax_main.set_ylim(0, 10500)
        ax_ratio.set_ylim(0.55, 1.55)
        leg_loc = 'upper right'
    else:
        leg_loc = 'best'

    # Legend with header
    header = Line2D([], [], color='none', label=r'$\bf{HLT\ Scouting}$')
    handles, labels = ax_main.get_legend_handles_labels()
    ax_main.legend(
        handles=[header] + handles,
        labels=[r'$\bf{HLT\ Scouting}$'] + labels,
        fontsize=18,
        loc=leg_loc,
    )

    ax_main.set_xlim(edges[0], edges[-1])
    ax_main.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax_main.yaxis.get_offset_text().set_fontsize(18)
    ax_main.yaxis.get_offset_text().set_x(-0.06)

    ax_main.grid(True, linestyle='--', alpha=0.3)
    ax_ratio.grid(True, linestyle='--', alpha=0.3)
    
    ax_ratio.set_ylabel("Ratio w.r.t. Prompt", fontsize=20)
    ax_ratio.axhline(1.0, color='gray', linestyle='--', linewidth=1)
    ax_ratio.legend(fontsize=14, loc=leg_loc)
    ax_ratio.set_xlabel(r"$\eta$", fontsize=20)
    
    # Save outputs
    pdf_pages.savefig(fig, bbox_inches='tight')
    fig.savefig(f"Comparison_{hist_name}.png", bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    with PdfPages(output_pdf) as pdf:
        for hist_info in target_histograms:
            print(f"Processing {hist_info['hist_name']}...")
            hist_list = []
            all_file_handles = []
            for cfg in files_config:
                files = glob.glob(os.path.join(cfg['path'], "*.root"))
                tag_dirs = []
                for fname in files:
                    try:
                        f = uproot.open(fname)
                        all_file_handles.append(f)
                        tag_dirs.append(get_base_dir(f, hist_info['category']))
                    except: tag_dirs.append(None)
                hist_list.append({**cfg, "data": fetch_and_sum(tag_dirs, hist_info['hist_name'])})
            
            plot_comparison(hist_info, hist_list, pdf)
            for f in all_file_handles: f.close()
            
    print(f"SUCCESS: Analysis Complete. Output: {output_pdf}")
