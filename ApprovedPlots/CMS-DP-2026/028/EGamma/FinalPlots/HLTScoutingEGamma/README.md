# HLT Scouting Electrons
## Dataset
The root files used here to get the plots can be found in:
```
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/DQM_260426
```
however, I downloaded the DQMs onto my laptop and just ran locally. Please adjust the directory accordingly in case of use.

## Requirements
The plots were created locally using python in my local virtual environment. The versions at which the packages were used to create the plots can be found int `requirements.txt`. They can be installed using:
```
pip install -r requirements.txt
```
or
```
conda install --file requirements.txt
```
best while using a virtual environment please.

## Plots and Scripts

| Plot | Python Script |
| :--- | :--- |
| <img src="plots/electrons_mass_rebin_err.png" width="100%" /> | `invariantMass_ScoutingDielectron.py` |
| <img src="plots/electrons_zMass_rebin_err.png" width="100%" /> | `invariantMass_ScoutingDielectron.py` |
| <img src="plots/electrons_barrelMass_rebin_err.png" width="100%" /> | `invariantMass_ScoutingDielectron.py` |
| <img src="plots/electrons_endcapMass_rebin_err.png" width="100%" /> | `invariantMass_ScoutingDielectron.py` |
| <img src="plots/Comparison_eta_ele.png" width="100%" /> | `eta_ScoutingElectron_ScoutingPhoton.py` |
| <img src="plots/Comparison_eta_pho.png" width="100%" /> | `eta_ScoutingElectron_ScoutingPhoton.py` |
| <img src="plots/Diff_HLT_vs_NGT_ebRecHitsEtaPhitMap.png" width="100%" /> | `absolute_difference_ieta_iphi_NGT_HLT_ScoutingRecHitsBarrel.py` |
| <img src="plots/RelDiff_HLT_vs_NGT_ebRecHitsEtaPhitMap.png" width="100%" /> | `relative_difference_ieta_iphi_NGT_HLT_ScoutingRecHitsBarrel.py` |
| <img src="plots/Diff_HLT_vs_NGT_eePlusRecHitsEtaPhitMap.png" width="100%" /> | `absolute_difference_ix_iy_NGT_HLT_ScoutingRecHitsEndcapPlus.py` |
| <img src="plots/RelDiff_HLT_vs_NGT_eePlusRecHitsEtaPhitMap_rad2D.png" width="100%" /> | `relative_difference_ix_iy_NGT_HLT_ScoutingRecHitsEndcapPlus.py` |
| <img src="plots/Comparison_ebRechitsN.png" width="100%" /> | `variables_ScoutingECALRecHits.py` |
| <img src="plots/Comparison_ebRechits_energy_bad.png" width="100%" /> | `variables_ScoutingECALRecHits.py` |
| <img src="plots/Comparison_ebRechits_time.png" width="100%" /> | `variables_ScoutingECALRecHits.py` |
| <img src="plots/Comparison_eeRechitsN.png" width="100%" /> | `variables_ScoutingECALRecHits.py` |
| <img src="plots/Comparison_eeRechits_energy.png" width="100%" /> | `variables_ScoutingECALRecHits.py` |
| <img src="plots/Comparison_eeRechits_time.png" width="100%" /> | `variables_ScoutingECALRecHits.py` |
| <img src="plots/Comparison_h_mass_Scouting.png" width="100%" /> | `invariantMassPiZero_PF_ScoutingDiphotons.py` |





