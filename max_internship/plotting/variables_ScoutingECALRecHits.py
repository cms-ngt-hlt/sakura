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

        #if hist_name == "ebRechitsN_bad":
        #    ax_main.set_ylim(0, 2e6) # changed


    @staticmethod
    def _xlabel(hist_name):
        """Human-readable x-label from the histogram name (verbatim
        substring mapping from the original script)."""
        aaa = hist_name
        lower = hist_name.lower()
        if "energy" in lower:
            if "eb" in lower:
                return "RecHit EB Energy [GeV] " + aaa
            if "ee" in lower:
                return "RecHit EE Energy [GeV] " + aaa
            return "RecHit Energy [GeV] " + aaa
        if "time" in lower:
            if "eb" in lower:
                return "RecHit EB Time [ns] " + aaa
            if "ee" in lower:
                return "RecHit EE Time [ns] " + aaa
            return "RecHit Time [ns] " + aaa
        if "rechitsn" in lower:
            if "eb" in lower:
                return "Number of EB RecHits " + aaa
            if "ee" in lower:
                return "Number of EE RecHits " + aaa
            return "Number of RecHits " + aaa
        return hist_name


if __name__ == "__main__":
    RecHitsPlot(config_path="config.yaml").run()
