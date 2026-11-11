"""
Entry script: ECAL RecHit variables (multiplicity, energy, time; EB/EE;
accepted/rejected).  Replaces the old variables_ScoutingECALRecHits.py.
"""

from scouting_plot import ComparisonPlot1D

ACCEPTED = "Miscellaneous/CaloRecHitsAccepted"
REJECTED = "Miscellaneous/CaloRecHitsRejected"


class RecHitsPlot(ComparisonPlot1D):

    output_pdf = "Comparison_RecHits_Miscellaneous.pdf"

    def targets(self):
        return [
            {"subpath": ACCEPTED, "hist_name": "ebRechitsN"},
            {"subpath": ACCEPTED, "hist_name": "ebRechits_energy"},
            {"subpath": ACCEPTED, "hist_name": "ebRechits_time"},
            {"subpath": REJECTED, "hist_name": "ebRechitsN_bad"},
            {"subpath": REJECTED, "hist_name": "ebRechits_energy_bad"},
            {"subpath": REJECTED, "hist_name": "ebRechits_time_bad"},
            {"subpath": ACCEPTED, "hist_name": "eeRechitsN"},
            {"subpath": ACCEPTED, "hist_name": "eeRechits_energy"},
            {"subpath": ACCEPTED, "hist_name": "eeRechits_time"},
            {"subpath": REJECTED, "hist_name": "eeRechitsN_bad"},
            {"subpath": REJECTED, "hist_name": "eeRechits_energy_bad"},
            {"subpath": REJECTED, "hist_name": "eeRechits_time_bad"},
        ]

    def apply_yscale(self, ax_main, max_y, target):
        # Timing distributions: linear with scientific ticks;
        # everything else (multiplicity, energy): log.
        if "time" in target["hist_name"].lower():
            self._sci_notation(ax_main)
        else:
            ax_main.set_yscale("log")

    def ratio_marker_size(self, edges, target):
        # Preserved special case for the EE multiplicity plots
        # (matches 'eeRechitsN' and 'eeRechitsN_bad').
        if "eeRechitsN" in target["hist_name"]:
            return 25
        return super().ratio_marker_size(edges, target)

    def decorate(self, ax_main, ax_ratio, target):
        hist_name = target["hist_name"]

        # Zoomed x-ranges for the multiplicity plots (default is the
        # full histogram range set by the base class).
        if "eeRechitsN" in hist_name:
            ax_main.set_xlim(0, 180)
        elif "ebRechitsN" in hist_name:
            ax_main.set_xlim(0, 450)

        # Multiplicity plots count events; the others count RecHits.
        if "N" in hist_name:
            ax_main.set_ylabel("Number of Events", fontsize=20)
        else:
            ax_main.set_ylabel("Number of RecHits", fontsize=20)

        ax_ratio.set_xlabel(self._xlabel(hist_name), fontsize=20)

    @staticmethod
    def _xlabel(hist_name):
        """Human-readable x-label from the histogram name; rejected
        RecHits (*_bad) are marked as such."""
        lower = hist_name.lower()
        region = ("EB " if lower.startswith("eb") else
                  "EE " if lower.startswith("ee") else "")
        rejected = " (rejected)" if lower.endswith("_bad") else ""
        if "energy" in lower:
            return f"RecHit {region}Energy [GeV]{rejected}"
        if "time" in lower:
            return f"RecHit {region}Time [ns]{rejected}"
        if "rechitsn" in lower:
            return f"Number of {region}RecHits{rejected}"
        return hist_name


if __name__ == "__main__":
    RecHitsPlot.main()
