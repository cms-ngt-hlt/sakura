"""
Entry script: relative difference maps ((A - B) / B) of the EE RecHit
occupancy in ix/iy (both endcaps), with a RADIAL projection around the
beam axis instead of cartesian projections.
Replaces the old relative_difference_ix_iy_NGT_HLT_ScoutingRecHitsEndcapPlus.py
(which, despite its name, always processed EE- as well).
"""

from scouting_plot import RelDiffMapRadial


class RelDiffMapEE(RelDiffMapRadial):

    output_pdf = "Comparison_EE_Maps_RelDiffs_RadialProj.pdf"
    region = "EE"
    z_limit = 0.30   # color scale: +-30%

    def targets(self):
        return [
            {"subpath": "Miscellaneous/CaloRecHitsAccepted",
             "hist_name": "eeMinusRecHitsEtaPhitMap"},
            {"subpath": "Miscellaneous/CaloRecHitsAccepted",
             "hist_name": "eePlusRecHitsEtaPhitMap"},
        ]


if __name__ == "__main__":
    RelDiffMapEE(config_path="config.yaml").run()
