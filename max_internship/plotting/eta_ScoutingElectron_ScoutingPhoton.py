"""
Entry script: pseudorapidity (eta) of scouting electrons and photons.
Replaces the old eta_ScoutingElectron_ScoutingPhoton.py.
"""

from scouting_plot import ComparisonPlot1D


class EtaPlot(ComparisonPlot1D):

    output_pdf = "Comparison_Eta_Plots.pdf"

    def targets(self):
        # "label" is an extra key our own decorate() understands
        # (particle name for the y-axis label).
        return [
            {"subpath": "Miscellaneous/Electron", "hist_name": "eta_ele",
             "label": "Electrons"},
            {"subpath": "Miscellaneous/Photon", "hist_name": "eta_pho",
             "label": "Photons"},
        ]

    def apply_yscale(self, ax_main, max_y, target):
        # Always linear with scientific y ticks.
        self._sci_notation(ax_main)

    def legend_loc(self, target):
        # The photon plot needs a fixed legend position.
        return "upper right" if target["hist_name"] == "eta_pho" else "best"

    def decorate(self, ax_main, ax_ratio, target):
        ax_main.set_ylabel(f"Number of {target['label']}", fontsize=20)

        # Hardcoded per-histogram zooms (verbatim from the original).
        if target["hist_name"] == "eta_ele":
            ax_main.set_ylim(0, 170000) # changed this by an order of magnitude
            ax_ratio.set_ylim(0.75, 1.15)
        elif target["hist_name"] == "eta_pho":
            ax_main.set_ylim(0, 105000) # this as well
            ax_ratio.set_ylim(0.55, 1.55)

        ax_ratio.set_xlabel(r"$\eta$", fontsize=20)


if __name__ == "__main__":
    EtaPlot(config_path="config.yaml").run()
