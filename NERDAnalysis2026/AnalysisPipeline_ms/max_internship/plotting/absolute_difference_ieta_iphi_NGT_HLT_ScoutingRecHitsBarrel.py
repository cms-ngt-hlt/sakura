"""
Entry script: absolute difference maps (A - B) of the EB RecHit
occupancy in ieta/iphi, with ieta and iphi projections.
Replaces the old absolute_difference_ieta_iphi_NGT_HLT_ScoutingRecHitsBarrel.py.
"""

from scouting_plot import AbsDiffMap


class AbsDiffMapEB(AbsDiffMap):

    output_pdf = "Comparison_EB_Maps_Diffs.pdf"
    region = "EB"

    def targets(self):
        return [{"subpath": "Miscellaneous/CaloRecHitsAccepted",
                 "hist_name": "ebRecHitsEtaPhitMap"}]


if __name__ == "__main__":
    AbsDiffMapEB(config_path="config.yaml").run()
