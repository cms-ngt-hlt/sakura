"""
Entry script: dilepton invariant mass spectra (Z, J/psi, barrel/endcap
splits, for electrons and both muon collections).
Replaces the old invariantMass_ScoutingDielectron.py.

The recursive directory traversal (`traverse_and_compare`) always found the same 15 histograms, so they
are now listed explicitly and the traversal is gone.
"""

from scouting_plot import ComparisonPlot1D

# The 15 histograms the old traversal found in the DiLepton folder.
HISTOGRAMS = [
    "electrons_barrelMass",
    "electrons_endcapMass",
    "electrons_jpsiMass",
    "electrons_mass",
    "electrons_zMass",
    "muonsNoVtx_barrelMass",
    "muonsNoVtx_endcapMass",
    "muonsNoVtx_jpsiMass",
    "muonsNoVtx_mass",
    "muonsNoVtx_zMass",
    "muons_barrelMass",
    "muons_endcapMass",
    "muons_jpsiMass",
    "muons_mass",
    "muons_zMass",
]


class DileptonMassPlot(ComparisonPlot1D):

    output_pdf = "Comparison_DiLepton_rebin_err.pdf"

    def targets(self):
        return [{"subpath": "DiLepton", "hist_name": h} for h in HISTOGRAMS]

    def transform(self, data):
        """
        Rebin by a factor of 2 (merge adjacent bins), verbatim from the
        old `rebin_hist` including the drop-last-bin-if-odd behaviour.
        This changes bin contents and is deliberately local to
        this subclass - it must never apply to the other plots.
        """
        if data is None:
            return None
        values, edges = data
        if len(values) % 2 != 0:
            values = values[:-1]
            edges = edges[:-1]
        new_values = values.reshape(-1, 2).sum(axis=1)
        new_edges = edges[::2]
        return (new_values, new_edges)

    def apply_yscale(self, ax_main, max_y, target):
        # Dynamic rule kept per review decision: log for well-populated
        # spectra, linear + scientific ticks otherwise.
        if max_y > 100:
            ax_main.set_yscale("log")
        else:
            self._sci_notation(ax_main)

    def decorate(self, ax_main, ax_ratio, target):
        # Electron vs muon labels from the histogram name prefix
        # (electrons_*, muons_*, muonsNoVtx_*).
        if target["hist_name"].startswith("muons"):
            candidates, mass = "Dimuon", r"$m_{\mu\mu}$ [GeV]"
        else:
            candidates, mass = "Dielectron", r"$m_{ee}$ [GeV]"
        ax_main.set_ylabel(f"Number of {candidates} Candidates", fontsize=20)
        ax_ratio.set_xlabel(mass, fontsize=20)

    # -- saving style of the old script: different PNG names plus a
    # -- standalone per-plot PDF next to each PNG.

    def png_name(self, target):
        return f"{target['hist_name']}_rebin_err.png"

    def extra_pdf_name(self, target):
        return f"{target['hist_name']}_rebin_err.pdf"


if __name__ == "__main__":
    DileptonMassPlot.main()
