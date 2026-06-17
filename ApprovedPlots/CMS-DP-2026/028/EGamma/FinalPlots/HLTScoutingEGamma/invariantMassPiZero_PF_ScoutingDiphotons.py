import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import sys
import glob
import os
import mplhep as hep

# Set CMS style
plt.style.use(hep.style.CMS)

# ==========================================
# --- USER CONFIGURATION ---
# ==========================================

files_config = [
    {"label": "Prompt Conditions", "path": "Prompt", "color": "black",  "style": "-"},
    {"label": "HLT Conditions", "path": "HLT", "color": "#5790fc",  "style": "--"},
    {"label": "NGT Conditions", "path": "NGT", "color": "#f89c20",    "style": ":"}
]

# Specific histogram we want to plot
# Format: (Folder within ScoutingOnline, Histogram Name)
target_histograms = [
    ("PiZero", "h_mass_Scouting")
]

output_pdf = "Comparison_PiZero_Mass.pdf"
# rlabel_text = "Oct 29 - Nov 4, 2025 (13.6 TeV)"

# Total recorded lumi: 2094.86 /pb = 2.09 /fb
#rlabel_text = r"2.09 fb$^{-1}$ (13.6 TeV)"
# ==========================================
# --- LOGIC START ---
# ==========================================

def get_base_dir(file_handle, category):
    """
    Finds the run-dependent path inside a ROOT file.
    """
    if "DQMData" not in file_handle: return None
    dqm_keys = file_handle["DQMData"].keys(cycle=False)
    
    # Find the run folder (e.g., "Run 398827")
    run_folder = next((k for k in dqm_keys if "Run " in k), None)
    
    if run_folder:
        full_path = f"DQMData/{run_folder}/HLT/Run summary/ScoutingOnline/{category}"
        # Verify path exists
        if full_path in file_handle:
            return file_handle[full_path]
    return None

def fetch_and_sum(dir_list, key):
    """
    Aggregates histograms from multiple files for a specific key.
    """
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

    if not found_any:
        return None
        
    return (sum_values, edges)

def plot_comparison(plot_name, hist_data_list, pdf_pages):
    """
    Generates the plot.
    """
    valid_items = [h for h in hist_data_list if h['data'] is not None]
    if not valid_items: 
        print(f"      [Warning] No valid data for {plot_name}")
        return

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, 
        figsize=(10, 10), 
        sharex=True, 
        gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
    )
    
    # CMS Label with fixed fontsize 22
    #hep.cms.label(ax=ax_main, data=True, label="Preliminary", year=2025, rlabel=rlabel_text, fontsize=22)
    # CMS Label with fixed fontsize 22
    hep.cms.label(ax=ax_main, data=True, label="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=22)
    max_y = 0
    ref_values = None
    
    # Get Reference Data (Prompt Conditions)
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

        # Main Plot
        hep.histplot(values, bins=edges, ax=ax_main, 
                     label=item['label'], color=item['color'], 
                     linestyle=item['style'], linewidth=2, yerr=True)

        # Ratio Plot
        if ref_values is not None and len(values) == len(ref_values):
            ratio = np.divide(values, ref_values, out=np.full_like(values, np.nan), where=ref_values!=0)
            
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
                         histtype='errorbar', marker='_', markersize=ms, markeredgewidth=2,
                         yerr=err_ratio if not is_reference else False)

    # Add vertical line for Pi0 mass expectation (134.9766 MeV)
    ax_main.axvline(0.1349766, color='grey', linestyle='--', linewidth=1.5, alpha=0.8, label=r"$\pi^0$ Mass")

    # Formatting
    ax_main.set_ylabel("Number of Diphoton Candidates", fontsize=20)
    ax_main.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax_main.yaxis.get_offset_text().set_fontsize(18)
    ax_main.yaxis.get_offset_text().set_x(-0.06)
    #ax_main.legend(fontsize=18, loc='best')
    from matplotlib.lines import Line2D
    header = Line2D([], [], color='none', label=r'$\bf{HLT\ Scouting}$')
    handles, labels = ax_main.get_legend_handles_labels()
    legend = ax_main.legend(
        handles=[header] + handles,
        labels=[r'$\bf{HLT\ Scouting}$'] + labels,
        fontsize=18,
        loc='best'
    )

    ax_main.set_yscale('linear')
    ax_main.set_xlim(0.02, 0.5)
    
    # Add vertical line to ratio plot as well
    ax_ratio.axvline(0.1349766, color='grey', linestyle='--', linewidth=1.5, alpha=0.8)
    
    ax_main.grid(True, linestyle='--', alpha=0.3)
    
    ax_ratio.set_ylabel("Ratio w.r.t. Prompt", fontsize=20)
    ax_ratio.axhline(1.0, color='gray', linestyle='--', linewidth=1)
    # Ratio range zoomed even more to 0.7 to 1.3
    ax_ratio.set_ylim(0.7, 1.3)
    ax_ratio.grid(True, linestyle='--', alpha=0.3)
    ax_ratio.legend(fontsize=14, loc='best')
    
    xlabel = r"$m_{\gamma \gamma}$ [GeV]"
    ax_ratio.set_xlabel(xlabel, fontsize=20)
    
    # Save to PDF with title
    ax_main.set_title(plot_name, fontsize=22, pad=20)
    pdf_pages.savefig(fig, bbox_inches='tight')
    
    # Save as PNG without title
    ax_main.set_title("")
    png_filename = f"Comparison_{plot_name}.png"
    fig.savefig(png_filename, bbox_inches='tight')
    print(f"      [Info] Saved {png_filename}")
    
    plt.close(fig)


# ==========================================
# --- MAIN EXECUTION ---
# ==========================================
if __name__ == "__main__":
    try:
        print(f"--- Starting targeted analysis for {output_pdf} ---")
        
        with PdfPages(output_pdf) as pdf:
            for subfolder, hist_name in target_histograms:
                print(f" > Processing {subfolder}/{hist_name}...")
                
                hist_list = []
                all_file_handles = []
                
                for cfg in files_config:
                    dir_path = cfg['path']
                    files = glob.glob(os.path.join(dir_path, "*.root"))
                    
                    if not files:
                        print(f"   [Warning] No .root files found in {dir_path}")
                        hist_list.append({
                            "label": cfg['label'], "color": cfg['color'], "style": cfg['style'], "data": None
                        })
                        continue
                        
                    tag_dirs = []
                    for fname in files:
                        try:
                            f = uproot.open(fname)
                            all_file_handles.append(f)
                            base = get_base_dir(f, subfolder)
                            tag_dirs.append(base)
                        except Exception as e:
                            print(f"   [Error] reading {fname}: {e}")
                            tag_dirs.append(None)
                    
                    agg_data = fetch_and_sum(tag_dirs, hist_name)
                    
                    hist_list.append({
                        "label": cfg['label'],
                        "color": cfg['color'],
                        "style": cfg['style'],
                        "data": agg_data
                    })
                
                plot_comparison(hist_name, hist_list, pdf)
                
                # Close files for this histogram to avoid hitting open file limits
                for f in all_file_handles:
                    f.close()

        print(f"SUCCESS: Targeted Analysis Complete. Output: {output_pdf}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
