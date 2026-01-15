import uproot
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep

plt.style.use(hep.style.CMS)

class ZeeComparator:
    def __init__(self, base_path):
        self.base_path = base_path
        
        self.sources = {
            'HLT':    {'folder': 'HLTDQM_Raw',    'color': '#5790fc'}, 
            'NGT':    {'folder': 'NGTDQM_Raw',    'color': '#f89c20'},
            'Prompt': {'folder': 'PromptDQM_Raw', 'color': 'black'} 
        }
        
        self.global_histos = {src: None for src in self.sources}
        self.common_bins = None
        
        self.load_all_data()

    def extract_run_number(self, filename):
        match = re.search(r'_R(\d+)\.root', filename)
        return int(match.group(1)) if match else None

    def load_all_data(self):
        """Iterates through folders and purely sums the histograms."""
        for label, info in self.sources.items():
            folder_path = os.path.join(self.base_path, info['folder'])
            
            if not os.path.exists(folder_path):
                print(f"Warning: Folder {folder_path} not found.")
                continue

            files = sorted([f for f in os.listdir(folder_path) if f.endswith(".root")])
            print(f"Processing {label}: Found {len(files)} files.")

            for item in files:
                run_number = self.extract_run_number(item)
                if run_number is None: continue

                file_path = os.path.join(folder_path, item)
               
                try:
                    with uproot.open(file_path) as file:
                        keys = [k for k in file.keys() if "di-Electron_Mass" in k]
                        if not keys: continue
                        
                        hist = file[keys[0]]
                        
                        bin_edges = hist.axis().edges()
                        counts = hist.values()
                        
                        if self.common_bins is None:
                            self.common_bins = bin_edges
                        
                        if self.global_histos[label] is None:
                            self.global_histos[label] = np.zeros_like(counts)
                            
                        if len(counts) == len(self.global_histos[label]):
                            self.global_histos[label] += counts
                            
                except Exception as e:
                    print(f"Error reading {item}: {e}")

    def plot_aggregated_comparison(self):
        if self.common_bins is None:
            print("No data loaded.")
            return

        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, 
            figsize=(12, 12), 
            sharex=True, 
            gridspec_kw={'height_ratios': [3, 1], 'hspace': 0.05}
        )

        # --- Top Plot: Distributions ---
        hep.cms.label(ax=ax_main, data=True, label="Preliminary", year=2025, rlabel="2025")
        
        prompt_counts = self.global_histos.get('Prompt')
        
        for label, info in self.sources.items():
            counts = self.global_histos[label]
            if counts is None: continue

            #total_events = int(np.sum(counts))
            
            hep.histplot(
                counts,
                bins=self.common_bins,
                label=f"{label} Tag",#(N={total_events})",
                color=info['color'],
                yerr=True,            
                histtype='step',  
                linewidth=2,
                ax=ax_main
            )

        ax_main.set_ylabel("Event Count", fontsize=22)
        ax_main.legend(fontsize=16, loc='upper right')
        ax_main.set_xlim(60, 120)
        ax_main.grid(True, alpha=0.3)

        # --- Bottom Plot: Ratios (X / Prompt) ---
        if prompt_counts is not None:
            valid_mask = prompt_counts > 0
            
            for label, info in self.sources.items():
                counts = self.global_histos[label]
                if counts is None: continue

                ratio = np.full_like(counts, np.nan, dtype=float)
                ratio[valid_mask] = counts[valid_mask] / prompt_counts[valid_mask]

                hep.histplot(                
                    ratio,
                    bins=self.common_bins,
                    color=info['color'],
                    yerr=False, 
                    histtype='errorbar',
                    marker='_',
                    markersize=10,
                    linewidth=0, 
                    markeredgewidth=2,
                    ax=ax_ratio
                )

            ax_ratio.axhline(1.0, color='gray', linestyle='--', alpha=0.5)

        ax_ratio.set_ylabel("Ratio / Prompt", fontsize=20)
        ax_ratio.set_xlabel("Di-Electron Mass Spectrum [GeV]", fontsize=22)
        ax_ratio.set_ylim(0.0, 2.0)
        ax_ratio.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("Zee_Comparison_Simple.png")
        print("Saved Zee_Comparison_Simple.png")
        plt.close()

if __name__ == "__main__":
    base_dir = "/Users/jessicaprendi/NERDAnalysis2025/Zee"
    analyzer = ZeeComparator(base_dir)
    analyzer.plot_aggregated_comparison()
