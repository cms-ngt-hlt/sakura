import uproot
import matplotlib.pyplot as plt
import numpy as np
import os
import mplhep as hep

# Apply CMS Style
plt.style.use(hep.style.CMS)

# Configuration
files = {
    'Prompt': './Prompt/DQM_V0001_ScoutingDQM_R000398858.root',
    'HLT': './HLT/DQM_V0001_ScoutingDQM_R000398858.root',
    'NGT': './NGT/DQM_V0001_ScoutingDQM_R000398858.root'
}

keys_2d = {
    'MuonNoVtx': 'DQMData/Run 398858/HLT/Run summary/ScoutingOnline/Muons/Properties/MuonNoVtx_nTrackerLayersWithMeasurement_vs_eta_phi_prof;1',
    'MuonVtx': 'DQMData/Run 398858/HLT/Run summary/ScoutingOnline/Muons/Properties/MuonVtx_nTrackerLayersWithMeasurement_vs_eta_phi_prof;1'
}

from matplotlib.backends.backend_pdf import PdfPages

output_dir = 'muon_cms_plots'
os.makedirs(output_dir, exist_ok=True)
pdf_report_path = os.path.join(output_dir, 'muon_diff_report_cms.pdf')

def plot_cms_diff(ax, title_prefix, diff_data, x_edges, y_edges, diff_label):
    # Standardize Z-axis to [-4, 4] as requested
    limit = 4.0
    
    # Use hep.hist2dplot for the 2D diff
    mesh = hep.hist2dplot(
        diff_data, x_edges, y_edges,
        ax=ax,
        cmap="PiYG",
        cmin=-limit,
        cmax=limit,
        cbar=True,
        cbarextend=True,
        flow='none'
    )
    
    ax.set_xlabel(r"Muon $\eta$", fontsize=18)
    ax.set_ylabel(r"Muon $\phi$", fontsize=18)
    
    # CMS Label
    hep.cms.label(ax=ax, data=True, label="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=20)
    
    # Colorbar label
    fig = ax.get_figure()
    cbar_ax = fig.get_axes()[-1]
    cbar_label = f'Diff. in Number of Silicon Tracker Hits ({diff_label})'
    cbar_ax.set_ylabel(cbar_label, fontsize=18)
    #ax.set_title(f"{title_prefix}", fontsize=20, pad=20)

# Execution
# Load 2D data
vals = {src: {} for src in files}
edges = None

for src, path in files.items():
    with uproot.open(path) as f:
        for coll, key in keys_2d.items():
            h = f[key]
            vals[src][coll] = h.values()
            if edges is None:
                e = h.axes
                edges = (e[0].edges(), e[1].edges())

# Task: Generate Diffs and Save to PDF
diff_configs = [
    ('NGT_vs_Prompt', 'NGT', 'Prompt', 'NGT - Prompt'),
    ('NGT_vs_HLT', 'NGT', 'HLT', 'NGT - HLT')
]

with PdfPages(pdf_report_path) as pdf:
    for coll in ['MuonNoVtx', 'MuonVtx', 'Combined']:
        print(f'Processing {coll}...')
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))
        
        for i, (suffix, src1, src2, label) in enumerate(diff_configs):
            ax = axes[i]
            if coll == 'Combined':
                d1 = vals[src1]['MuonVtx'] + vals[src1]['MuonNoVtx']
                d2 = vals[src2]['MuonVtx'] + vals[src2]['MuonNoVtx']
                title_prefix = "Combined (Vtx+NoVtx)"
            else:
                d1 = vals[src1][coll]
                d2 = vals[src2][coll]
                title_prefix = coll
                
            diff = d1 - d2
            plot_cms_diff(ax, title_prefix, diff, edges[0], edges[1], label)
            
            # Also save individual PNG for convenience
            individual_fig, individual_ax = plt.subplots(figsize=(10, 10))
            plot_cms_diff(individual_ax, title_prefix, diff, edges[0], edges[1], label)
            individual_fig.savefig(os.path.join(output_dir, f"{coll}_{suffix}.png"), bbox_inches='tight')
            plt.close(individual_fig)

        plt.tight_layout()
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

print(f'\nDone! Results saved in {output_dir} and report at {pdf_report_path}')
