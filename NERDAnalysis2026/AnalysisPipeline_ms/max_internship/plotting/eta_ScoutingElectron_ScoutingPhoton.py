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

    def decorate(self, ax_main, ax_ratio, target):
        # y-ranges are left to autoscaling (main) and the shared 0-2
        # default (ratio): fixed ranges only fit one dataset.
        ax_main.set_ylabel(f"Number of {target['label']}", fontsize=20)
        ax_ratio.set_xlabel(r"$\eta$", fontsize=20)


if __name__ == "__main__":
    EtaPlot.main()
