import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob
import os
import mplhep as hep

# Set CMS style
plt.style.use(hep.style.CMS)

# ==========================================
# --- USER CONFIGURATION ---
# ==========================================

files_config = [
    {"label": "Prompt", "path": "Prompt"},
    {"label": "HLT", "path": "HLT"},
    {"label": "NGT", "path": "NGT"}
]

target_histograms = [
    "ebRecHitsEtaPhitMap"
]

output_pdf = "Comparison_EB_Maps_Diffs.pdf"
subfolder = "CaloRecHitsAccepted"

# Pairs for Diff: (Numerator/Minuend, Denominator/Subtrahend)
diff_pairs = [
    ("Prompt", "NGT"),
    ("HLT", "NGT"),
    ("HLT", "Prompt")
]

# ==========================================
# --- LOGIC START ---
# ==========================================

def get_base_dir(file_handle, subfolder):
    if "DQMData" not in file_handle: return None
    dqm_keys = file_handle["DQMData"].keys(cycle=False)
    run_folder = next((k for k in dqm_keys if "Run " in k), None)
    if run_folder:
        full_path = f"DQMData/{run_folder}/HLT/Run summary/ScoutingOnline/Miscellaneous/{subfolder}"
        if full_path in file_handle:
            return file_handle[full_path]
    return None

def fetch_and_sum_2d(dir_list, key):
    sum_values = None
    xedges = None
    yedges = None
    found_any = False
    for d in dir_list:
        if d is None: continue
        try:
            if key in d:
                obj = d[key]
                data = obj.to_numpy()
                if not found_any:
                    sum_values = np.array(data[0], dtype=float)
                    xedges = data[1]
                    yedges = data[2]
                    found_any = True
                else:
                    if data[0].shape == sum_values.shape:
                        sum_values += data[0]
        except Exception:
            continue
    return (sum_values, xedges, yedges) if found_any else None

if __name__ == "__main__":
    try:
        print(f"--- Starting EB Diff Maps analysis for {output_pdf} ---")
        
        with PdfPages(output_pdf) as pdf:
            for hist_name in target_histograms:
                print(f" > Processing {hist_name}...")
                
                # Fetch data for all tags
                all_tag_data = {}
                edges = None
                
                for cfg in files_config:
                    label = cfg['label']
                    files = glob.glob(os.path.join(cfg['path'], "*.root"))
                    tag_dirs = []
                    handles = []
                    for fname in files:
                        f = uproot.open(fname)
                        handles.append(f)
                        tag_dirs.append(get_base_dir(f, subfolder))
                    
                    data = fetch_and_sum_2d(tag_dirs, hist_name)
                    if data:
                        all_tag_data[label] = data[0]
                        if edges is None:
                            edges = (data[1], data[2])
                    
                    for f in handles: f.close()

                if not edges or len(all_tag_data) < 2:
                    print(f"   [Warning] Not enough data for diffs in {hist_name}")
                    continue

                xedges, yedges = edges

                # Compute all diffs first to find global max_abs
                diff_data = {}
                global_max_abs = 0
                
                for label_a, label_b in diff_pairs:
                    if label_a not in all_tag_data or label_b not in all_tag_data:
                        continue
                    
                    diff_vals = all_tag_data[label_a] - all_tag_data[label_b]
                    diff_data[(label_a, label_b)] = diff_vals
                    
                    current_max = np.max(np.abs(diff_vals))
                    if current_max > global_max_abs:
                        global_max_abs = current_max
                
                # Color scale limits
                z_limit = 1000.0

                # Plot differences
                for (label_a, label_b), diff_vals in diff_data.items():
                    print(f"   >> Plotting Diff: {label_a} - {label_b} (z-limit={z_limit})")
                    
                    fig, (ax, ax_eta, ax_phi) = plt.subplots(3, 1, figsize=(12, 18),
                                                      gridspec_kw={'height_ratios': [4, 1, 1], 'hspace': 0.25})
                    
                    hep.cms.label(ax=ax, data=True, label="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=22)
                    
                    from matplotlib.colors import SymLogNorm
                    norm = SymLogNorm(linthresh=1.0, vmin=-z_limit, vmax=z_limit, base=10)
                    cmap = plt.get_cmap('PiYG')
                    
                    im = hep.hist2dplot(diff_vals, xbins=xedges, ybins=yedges, ax=ax, 
                                       cbar=False, cmap=cmap, norm=norm)
                    
                    ax.set_title(f"Diff: {label_a} - {label_b}\n{hist_name}", fontsize=20, pad=20)
                    ax.set_xlabel(r"RecHit EB $i\eta$", fontsize=22)
                    ax.set_ylabel(r"RecHit EB $i\phi$", fontsize=22)
                    
                    # Explicit colorbar for 2D
                    from mpl_toolkits.axes_grid1 import make_axes_locatable
                    divider_2d = make_axes_locatable(ax)
                    cax = divider_2d.append_axes("right", size="5%", pad=0.05)
                    cbar = fig.colorbar(ax.collections[0], cax=cax)
                    cbar.set_label(f"Diff. in Number of RecHits ({label_a} - {label_b})", fontsize=22)

                    # 1D ieta Projection
                    diff_proj_eta = np.sum(diff_vals, axis=1)
                    hep.histplot(diff_proj_eta, bins=xedges, ax=ax_eta, color='black', histtype='step', lw=2)
                    ax_eta.set_xlabel(r"RecHit EB $i\eta$", fontsize=22)
                    ax_eta.set_ylabel(f"Diff. in Number of RecHits ({label_a} - {label_b})", fontsize=20)
                    ax_eta.axhline(0, color='gray', linestyle='--', linewidth=1)
                    ax_eta.grid(True, linestyle='--', alpha=0.3)
                    ax_eta.set_xlim(xedges[0], xedges[-1])
                    divider_eta = make_axes_locatable(ax_eta)
                    divider_eta.append_axes("right", size="5%", pad=0.05).axis("off")

                    # 1D iphi Projection
                    diff_proj_phi = np.sum(diff_vals, axis=0)
                    hep.histplot(diff_proj_phi, bins=yedges, ax=ax_phi, color='black', histtype='step', lw=2)
                    ax_phi.set_xlabel(r"RecHit EB $i\phi$", fontsize=22)
                    ax_phi.set_ylabel("", fontsize=20)
                    ax_phi.axhline(0, color='gray', linestyle='--', linewidth=1)
                    ax_phi.grid(True, linestyle='--', alpha=0.3)
                    ax_phi.set_xlim(yedges[0], yedges[-1])
                    divider_phi = make_axes_locatable(ax_phi)
                    divider_phi.append_axes("right", size="5%", pad=0.05).axis("off")
                    
                    pdf.savefig(fig, bbox_inches='tight')
                    
                    # Remove title for PNG version
                    ax.set_title("")
                    png_filename = f"Diff_{label_a}_vs_{label_b}_{hist_name}.png"
                    fig.savefig(png_filename, bbox_inches='tight')
                    plt.close(fig)

        print(f"SUCCESS: EB Diff Maps Complete. Output: {output_pdf}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
