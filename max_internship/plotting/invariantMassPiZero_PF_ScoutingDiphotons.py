"""
Entry script: pi0 -> gamma gamma invariant mass comparison.
Replaces the old invariantMassPiZero_PF_ScoutingDiphotons.py.
"""

from scouting_plot import ComparisonPlot1D

PI0_MASS = 0.1349766  # GeV (PDG)


class PiZeroMassPlot(ComparisonPlot1D):

    output_pdf = "Comparison_PiZero_Mass.pdf"

    def targets(self):
        return [{"subpath": "PiZero", "hist_name": "h_mass_Scouting"}]

    def apply_yscale(self, ax_main, max_y, target):
        # Always linear with scientific y ticks.
        self._sci_notation(ax_main)

    def decorate(self, ax_main, ax_ratio, target):
        # Reference line at the PDG pi0 mass, on BOTH panels.  The
        # labelled main-panel line ends up in the legend because
        # decorate() runs before the legend is built.
        ax_main.axvline(PI0_MASS, color="grey", linestyle="--",
                        linewidth=1.5, alpha=0.8, label=r"$\pi^0$ Mass")
        ax_ratio.axvline(PI0_MASS, color="grey", linestyle="--",
                         linewidth=1.5, alpha=0.8)

        ax_main.set_xlim(0.02, 0.5)
        ax_ratio.set_ylim(0.7, 1.3)  # tighter ratio zoom than default
        ax_main.set_ylabel("Number of Diphoton Candidates", fontsize=20)
        ax_ratio.set_xlabel(r"$m_{\gamma \gamma}$ [GeV]", fontsize=20)


if __name__ == "__main__":
    PiZeroMassPlot(config_path="config.yaml").run()
