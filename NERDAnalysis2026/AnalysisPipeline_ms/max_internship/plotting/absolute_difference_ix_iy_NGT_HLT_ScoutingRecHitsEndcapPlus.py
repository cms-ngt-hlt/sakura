"""
Entry script: absolute difference maps (A - B) of the EE RecHit
occupancy in ix/iy (both endcaps), with ix and iy projections.
Replaces the old absolute_difference_ix_iy_NGT_HLT_ScoutingRecHitsEndcapPlus.py
(which, despite its name, always processed EE- as well).
"""

from scouting_plot import AbsDiffMap


class AbsDiffMapEE(AbsDiffMap):

    output_pdf = "Comparison_EE_Maps_Diffs.pdf"
    region = "EE"

    def targets(self):
        return [
            {"subpath": "Miscellaneous/CaloRecHitsAccepted",
             "hist_name": "eeMinusRecHitsEtaPhitMap"},
            {"subpath": "Miscellaneous/CaloRecHitsAccepted",
             "hist_name": "eePlusRecHitsEtaPhitMap"},
        ]


if __name__ == "__main__":
    AbsDiffMapEE(config_path="config.yaml").run()
