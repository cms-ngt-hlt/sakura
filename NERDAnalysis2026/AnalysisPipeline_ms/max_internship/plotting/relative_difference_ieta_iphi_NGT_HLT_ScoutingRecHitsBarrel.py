"""
Entry script: relative difference maps ((A - B) / B) of the EB RecHit
occupancy in ieta/iphi, with ieta and iphi projections
(relative difference OF the projections -- see RelDiffMap docstring).
Replaces the old relative_difference_ieta_iphi_NGT_HLT_ScoutingRecHitsBarrel.py.
"""

from scouting_plot import RelDiffMap


class RelDiffMapEB(RelDiffMap):

    output_pdf = "Comparison_EB_Maps_RelDiffs.pdf"
    region = "EB"
    z_limit = 0.08   # color scale: +-8%

    def targets(self):
        return [{"subpath": "Miscellaneous/CaloRecHitsAccepted",
                 "hist_name": "ebRecHitsEtaPhitMap"}]


if __name__ == "__main__":
    RelDiffMapEB(config_path="config.yaml").run()
