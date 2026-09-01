import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob
import os
import mplhep as hep
from mpl_toolkits.axes_grid1 import make_axes_locatable

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
    "eeMinusRecHitsEtaPhitMap",
    "eePlusRecHitsEtaPhitMap"
]

output_pdf = "Comparison_EE_Maps_Diffs.pdf"
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
        except Exception as e:
            continue
    return (sum_values, xedges, yedges) if found_any else None

if __name__ == "__main__":
    try:
        print(f"--- Starting EE Diff Maps analysis for {output_pdf} ---")
        
        with PdfPages(output_pdf) as pdf:
            for hist_name in target_histograms:
                print(f" > Processing {hist_name}...")
                
                all_tag_data = {}
                edges = None
                
                for cfg in files_config:
                    label = cfg['label']
                    files = glob.glob(os.path.join(cfg['path'], "*.root"))
                    tag_dirs = []
                    handles = []
                    for fname in files:
                        try:
                            f = uproot.open(fname)
                            handles.append(f)
                            tag_dirs.append(get_base_dir(f, subfolder))
                        except Exception:
                            tag_dirs.append(None)
                    
                    data = fetch_and_sum_2d(tag_dirs, hist_name)
                    if data:
                        all_tag_data[label] = data[0]
                        if edges is None:
                            edges = (data[1], data[2])
                    for f in handles: f.close()

                if not edges or len(all_tag_data) < 2:
                    continue
                xedges, yedges = edges

                diff_data = {}
                global_max_abs = 0
                for label_a, label_b in diff_pairs:
                    if label_a in all_tag_data and label_b in all_tag_data:
                        diff_vals = all_tag_data[label_a] - all_tag_data[label_b]
                        diff_data[(label_a, label_b)] = diff_vals
                        m = np.max(np.abs(diff_vals))
                        if m > global_max_abs: global_max_abs = m
                # Color scale limits
                z_limit = 1000.0

                for (label_a, label_b), diff_vals in diff_data.items():
                    print(f"   >> Plotting Diff: {label_a} - {label_b} (z-limit={z_limit})")
                    fig, (ax, ax_x, ax_y) = plt.subplots(3, 1, figsize=(12, 18), 
                                                         gridspec_kw={'height_ratios': [4, 1, 1], 'hspace': 0.25})
                    
                    hep.cms.label(ax=ax, data=True, label="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=22)
                    
                    from matplotlib.colors import SymLogNorm
                    norm = SymLogNorm(linthresh=1.0, vmin=-z_limit, vmax=z_limit, base=10)
                    cmap = plt.get_cmap('PiYG')
                    
                    # Determine EE side for labeling in this map
                    if "Plus" in hist_name:
                        ee_side = "EE+"
                    elif "Minus" in hist_name:
                        ee_side = "EE-"
                    else:
                        ee_side = "EE"
                    im = hep.hist2dplot(diff_vals, xbins=xedges, ybins=yedges, ax=ax, cbar=False, cmap=cmap, norm=norm)
                    ax.set_title(f"Diff: {label_a} - {label_b}\n{hist_name}", fontsize=20, pad=20)
                    ax.set_xlabel(rf"RecHit {ee_side} $ix$", fontsize=22)
                    ax.set_ylabel(rf"RecHit {ee_side} $iy$", fontsize=22)

                    
                    divider = make_axes_locatable(ax)
                    cax = divider.append_axes("right", size="5%", pad=0.05)
                    cbar = fig.colorbar(ax.collections[0], cax=cax)
                    cbar.set_label(f"Diff. in Number of RecHits ({label_a} - {label_b})", fontsize=22)

                    # ix Proj
                    ix_proj = np.sum(diff_vals, axis=1)
                    hep.histplot(ix_proj, bins=xedges, ax=ax_x, color='black', histtype='step', lw=2)
                    ax_x.set_xlabel(rf"RecHit {ee_side} $ix$", fontsize=22)
                    ax_x.set_ylabel(f"Diff. in Number of RecHits ({label_a} - {label_b})", fontsize=20)
                    ax_x.axhline(0, color='gray', linestyle='--', linewidth=1)
                    ax_x.grid(True, linestyle='--', alpha=0.3)
                    ax_x.set_xlim(xedges[0], xedges[-1])
                    divider_x = make_axes_locatable(ax_x)
                    divider_x.append_axes("right", size="5%", pad=0.05).axis("off")

                    # iy Proj
                    iy_proj = np.sum(diff_vals, axis=0)
                    hep.histplot(iy_proj, bins=yedges, ax=ax_y, color='black', histtype='step', lw=2)
                    ax_y.set_xlabel(rf"RecHit {ee_side} $iy$", fontsize=22)
                    ax_y.set_ylabel("", fontsize=20)
                    ax_y.axhline(0, color='gray', linestyle='--', linewidth=1)
                    ax_y.grid(True, linestyle='--', alpha=0.3)
                    ax_y.set_xlim(yedges[0], yedges[-1])
                    divider_y = make_axes_locatable(ax_y)
                    divider_y.append_axes("right", size="5%", pad=0.05).axis("off")
                    
                    pdf.savefig(fig, bbox_inches='tight')
                    # Remove title for PNG version
                    ax.set_title("")
                    png_filename = f"Diff_{label_a}_vs_{label_b}_{hist_name}.png"
                    fig.savefig(png_filename, bbox_inches='tight')
                    plt.close(fig)


        print(f"SUCCESS: EE Diff Maps Complete.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
