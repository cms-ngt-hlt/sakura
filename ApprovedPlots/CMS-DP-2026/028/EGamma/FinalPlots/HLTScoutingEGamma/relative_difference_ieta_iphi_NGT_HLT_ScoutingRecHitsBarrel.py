import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import glob
import os
import mplhep as hep
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import TwoSlopeNorm

# Set CMS style
plt.style.use(hep.style.CMS)

files_config = [
    {"label": "Prompt", "path": "Prompt"},
    {"label": "HLT",    "path": "HLT"},
    {"label": "NGT",    "path": "NGT"}
]

target_histograms = [
    "ebRecHitsEtaPhitMap"
]

output_pdf = "Comparison_EB_Maps_RelDiffs.pdf"
subfolder  = "CaloRecHitsAccepted"

diff_pairs = [
    ("Prompt", "NGT"),
    ("HLT",    "NGT"),
    ("HLT",    "Prompt")
]

Z_LIMIT_REL  = 0.08       

def get_base_dir(file_handle, subfolder):
    if "DQMData" not in file_handle:
        return None
    dqm_keys   = file_handle["DQMData"].keys(cycle=False)
    run_folder = next((k for k in dqm_keys if "Run " in k), None)
    if run_folder:
        full_path = f"DQMData/{run_folder}/HLT/Run summary/ScoutingOnline/Miscellaneous/{subfolder}"
        if full_path in file_handle:
            return file_handle[full_path]
    return None

def fetch_and_sum_2d(dir_list, key):
    sum_values = None
    xedges = yedges = None
    found_any = False
    for d in dir_list:
        if d is None:
            continue
        try:
            if key in d:
                obj  = d[key]
                data = obj.to_numpy()
                if not found_any:
                    sum_values = np.array(data[0], dtype=float)
                    xedges, yedges = data[1], data[2]
                    found_any = True
                else:
                    if data[0].shape == sum_values.shape:
                        sum_values += data[0]
        except Exception:
            continue
    return (sum_values, xedges, yedges) if found_any else None

if __name__ == "__main__":
    try:
        print(f"--- Starting EB Relative Diff Maps for {output_pdf} ---")

        with PdfPages(output_pdf) as pdf:
            for hist_name in target_histograms:
                print(f" > Processing {hist_name}...")

                xlabel = r"RecHit EB $i\eta$"
                ylabel = r"RecHit EB $i\phi$"

                # --- Load and sum all files per label ---
                all_tag_data = {}
                edges = None
                for cfg in files_config:
                    label    = cfg['label']
                    files    = glob.glob(os.path.join(cfg['path'], "*.root"))
                    tag_dirs, handles = [], []
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
                    for f in handles:
                        f.close()

                if not edges or len(all_tag_data) < 2:
                    print(f"   >> Skipping {hist_name}: insufficient data")
                    continue

                xedges, yedges = edges

                # --- Loop over diff pairs ---
                for label_a, label_b in diff_pairs:
                    if label_a not in all_tag_data or label_b not in all_tag_data:
                        continue

                    data_a = all_tag_data[label_a]
                    data_b = all_tag_data[label_b]

                    # TRUE RELATIVE DIFFERENCE: (A - B) / B
                    # We use np.where to safely handle division by zero where data_b has no hits.
                    # Bins with zero reference hits will be set to np.nan (ignored in plot).
                    with np.errstate(divide='ignore', invalid='ignore'):
                        rel_diff_2d = np.where(data_b != 0, (data_a - data_b) / data_b, np.nan)
                    
                    print(f"   >> Plotting True Relative Diff: ({label_a} - {label_b}) / {label_b}")

                    # --- Figure: 3 rows (2D, Eta proj, Phi proj) ---
                    fig, (ax, ax_eta, ax_phi) = plt.subplots(
                        3, 1, figsize=(12, 18),
                        gridspec_kw={'height_ratios': [4, 1, 1], 'hspace': 0.35},
                        constrained_layout=False
                    )
                    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.1, right=0.9)

                    hep.cms.label(ax=ax, data=True, label="Preliminary",
                                  year=2025, lumi=2.09, com=13.6, fontsize=20)

                    # --- Relative 2D map ---
                    norm_rel = TwoSlopeNorm(vcenter=0,
                                           vmin=-Z_LIMIT_REL, vmax=Z_LIMIT_REL)
                    cmap_rel = plt.get_cmap('PiYG')

                    hep.hist2dplot(rel_diff_2d, xbins=xedges, ybins=yedges,
                                  ax=ax, cbar=False, cmap=cmap_rel, norm=norm_rel)
                    
                    ax.set_title(f"Relative Difference: ({label_a} - {label_b}) / {label_b}\n{hist_name}",
                                 fontsize=20, pad=20)
                    ax.set_xlabel(xlabel, fontsize=22)
                    ax.set_ylabel(ylabel, fontsize=22)

                    divider = make_axes_locatable(ax)
                    cax     = divider.append_axes("right", size="5%", pad=0.05)
                    cbar    = fig.colorbar(ax.collections[0], cax=cax)
                    cbar.set_label(f"Rel. Diff. ({label_a} - {label_b}) / {label_b}", fontsize=20)
                    
                    # Formatter updated to standard text formatting (can change back to ScalarFormatter if needed)
                    cbar.formatter = plt.FuncFormatter(lambda val, pos: f"{val:.2f}") 
                    cbar.update_ticks()

                    # --- Eta projection ---
                    # To get a 1D relative diff, we sum the raw hits first, then calculate ratio
                    proj_a_eta = np.nansum(data_a, axis=1)
                    proj_b_eta = np.nansum(data_b, axis=1)
                    
                    with np.errstate(divide='ignore', invalid='ignore'):
                        rel_diff_eta = np.where(proj_b_eta != 0, (proj_a_eta - proj_b_eta) / proj_b_eta, np.nan)
                    
                    hep.histplot(rel_diff_eta, bins=xedges, ax=ax_eta,
                                 color='black', histtype='step', lw=2)
                    ax_eta.set_xlabel(xlabel, fontsize=22)
                    ax_eta.set_ylabel("Rel. Diff.", fontsize=20)
                    ax_eta.axhline(0, color='gray', linestyle='--', linewidth=1)
                    ax_eta.grid(True, linestyle='--', alpha=0.3)
                    ax_eta.set_xlim(xedges[0], xedges[-1])

                    divider_eta = make_axes_locatable(ax_eta)
                    divider_eta.append_axes("right", size="5%", pad=0.05).axis("off")

                    # --- Phi projection ---
                    proj_a_phi = np.nansum(data_a, axis=0)
                    proj_b_phi = np.nansum(data_b, axis=0)
                    
                    with np.errstate(divide='ignore', invalid='ignore'):
                        rel_diff_phi = np.where(proj_b_phi != 0, (proj_a_phi - proj_b_phi) / proj_b_phi, np.nan)

                    hep.histplot(rel_diff_phi, bins=yedges, ax=ax_phi,
                                 color='black', histtype='step', lw=2)
                    ax_phi.set_xlabel(ylabel, fontsize=22)
                    ax_phi.set_ylabel("Rel. Diff.", fontsize=20)
                    ax_phi.axhline(0, color='gray', linestyle='--', linewidth=1)
                    ax_phi.grid(True, linestyle='--', alpha=0.3)
                    ax_phi.set_xlim(yedges[0], yedges[-1])

                    divider_phi = make_axes_locatable(ax_phi)
                    divider_phi.append_axes("right", size="5%", pad=0.05).axis("off")

                    # --- Save ---
                    pdf.savefig(fig, bbox_inches='tight')
                    ax.set_title("")
                    png_name = f"RelDiff_{label_a}_vs_{label_b}_{hist_name}.png"
                    fig.savefig(png_name, bbox_inches='tight', dpi=150)
                    print(f"      Saved PNG: {png_name}")
                    plt.close(fig)

        print(f"\nSUCCESS: Output written to {output_pdf}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()