import uproot
import glob
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from matplotlib.backends.backend_pdf import PdfPages

# Apply CMS Style
plt.style.use(hep.style.CMS)

class EtaPhiDiffPlotter:
    def __init__(self, target_folder_substring):
        self.target_folder = target_folder_substring
        self.sources_config = {
            'HLT':    {'pattern': '*HLT.root'}, 
            'NGT':    {'pattern': '*NGT.root'},
            'Prompt': {'pattern': '*Prompt.root'} 
        }
        self.aggregated_maps = {label: {} for label in self.sources_config}
        self.load_and_aggregate()

    def _get_base_and_flavor(self, name):
        """Parses the histogram name to separate the variable name from the PDG ID."""
        if "-13" in name:
            base = name.replace("-13", "").replace("__", "_").strip("_")
            return base, 'neg'
        elif "13" in name:
            base = name.replace("13", "").replace("__", "_").strip("_")
            return base, 'pos'
        return name, None

    def load_and_aggregate(self):
        """Loads files and splits data into +13 (pos) and -13 (neg) buckets."""
        for label, config in self.sources_config.items():
            files = sorted(glob.glob(config['pattern']))
            if not files: continue
            print(f"[{label}] Aggregating {len(files)} runs...")

            for filename in files:
                try:
                    with uproot.open(filename) as f:
                        d_path = next((k for k in f.keys() if self.target_folder in k), None)
                        if not d_path: continue
                        d = f[d_path]

                        for key in d.keys(cycle=False):
                            clean_name = key.split(";")[0]
                            if "etaphi" not in clean_name.lower(): continue

                            obj = d[key]
                            if not hasattr(obj, "values"): continue
                            vals = obj.values()
                            if vals.ndim != 2: continue
                            
                            base_name, flavor = self._get_base_and_flavor(clean_name)
                            if not flavor: continue

                            if base_name not in self.aggregated_maps[label]:
                                self.aggregated_maps[label][base_name] = {}

                            if flavor not in self.aggregated_maps[label][base_name]:
                                self.aggregated_maps[label][base_name][flavor] = [
                                    np.zeros_like(vals), 
                                    obj.axis(0).edges(), 
                                    obj.axis(1).edges()
                                ]
                            self.aggregated_maps[label][base_name][flavor][0] += vals
                except Exception as e:
                    print(f" Error {filename}: {e}")

    def plot_diffs(self, output_prefix="Eta_Phi_Diff"):
        common_base_names = set.intersection(*(set(d.keys()) for d in self.aggregated_maps.values() if d))
        
        for base_name in sorted(common_base_names):
            print(f"Creating differences for {base_name}...")
            # We will save separate PNGs for each diff
            self._create_diff_pngs(base_name, "Combined", output_prefix)

        print(f"Differences saved as PNG files with prefix {output_prefix}")

    def _get_data_for_mode(self, label, base_name, mode):
        data_dict = self.aggregated_maps[label].get(base_name, {})
        pos_data = data_dict.get('pos')
        neg_data = data_dict.get('neg')
        def extract(d): return (d[0], d[1], d[2]) if d else (None, None, None)

        if mode == 'pos': return extract(pos_data)
        elif mode == 'neg': return extract(neg_data)
        elif mode == 'combined':
            if pos_data and neg_data:
                return (pos_data[0] + neg_data[0], pos_data[1], pos_data[2])
            elif pos_data: return extract(pos_data)
            elif neg_data: return extract(neg_data)
        return None, None, None

    def _create_diff_pngs(self, base_name, subtitle_suffix, output_prefix):
        """Creates separate PNGs for NGT-HLT and NGT-Prompt maps."""
        
        # 1. Gather Data
        data_map = {}
        valid_plot = True
        for label in ['NGT', 'HLT', 'Prompt']:
            vals, x, y = self._get_data_for_mode(label, base_name, 'combined')
            if vals is None: 
                valid_plot = False
                break
            data_map[label] = (vals, x, y)
        if not valid_plot: return

        diff_ngt_hlt = data_map['NGT'][0] - data_map['HLT'][0]
        diff_ngt_prompt = data_map['NGT'][0] - data_map['Prompt'][0]
        
        limit = max(np.max(np.abs(diff_ngt_hlt)), np.max(np.abs(diff_ngt_prompt)))
        limit = limit if limit > 0 else 1

        x, y = data_map['NGT'][1], data_map['NGT'][2]

        # Plot 1: NGT - HLT
        fig1, ax1 = plt.subplots(figsize=(10, 10))
        self._plot_single_diff(ax1, diff_ngt_hlt, x, y, None, limit, "NGT - HLT")
        plt.tight_layout()
        fig1.savefig(f"{output_prefix}_NGT_vs_HLT.png", bbox_inches='tight')
        plt.close(fig1)
        
        # Plot 2: NGT - Prompt
        fig2, ax2 = plt.subplots(figsize=(10, 10))
        self._plot_single_diff(ax2, diff_ngt_prompt, x, y, None, limit, "NGT - Prompt")
        plt.tight_layout()
        fig2.savefig(f"{output_prefix}_NGT_vs_Prompt.png", bbox_inches='tight')
        plt.close(fig2)

    def _plot_single_diff(self, ax, diff, x, y, title, limit, z_label_suffix=None):
            # Bring back cmap and set it to something much nicer!
            mesh = hep.hist2dplot(
                diff, x, y, 
                ax=ax, 
                cmap="PiYG",      # <--- Change your color palette here
                cmin=-limit, 
                cmax=limit, 
                cbar=True,            
                cbarextend=True,      
                flow='none'           
            )
            
            if title:
                ax.set_title(title, fontsize=22, y=-0.15)
            ax.set_xlabel(r"Muon $\eta$", fontsize=20)
            ax.set_ylabel(r"Muon $\phi$", fontsize=20)
            
            # CMS Label
            hep.cms.label(ax=ax, data=True, label="Preliminary", year=2025, lumi=2.09, com=13.6, fontsize=22)
            
            # Grab the auto-generated colorbar axis and set the label
            fig = ax.get_figure()
            cbar_ax = fig.get_axes()[-1]
            cbar_label = 'Diff. in events'
            if z_label_suffix:
                cbar_label += f' ({z_label_suffix})'
            cbar_ax.set_ylabel(cbar_label, fontsize=20)

if __name__ == "__main__":
    target = "FourVectorHLT/hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered"
    plotter = EtaPhiDiffPlotter(target)
    plotter.plot_diffs("Eta_Phi_Diff")
