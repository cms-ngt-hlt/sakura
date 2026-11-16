# CMS-DP-2026/158

**NGT Optimal Calibrations Demonstrator: Physics and Computing Performance Update** (November 2026)

The note uses proton-proton data at √s = 13.6 TeV, recorded in 2025 and 2026.
It compares the HLT reconstruction run with three sets of conditions: standard
HLT, Prompt (offline) and NGT. It covers:

* the ECAL crystal transparency (laser) corrections and the silicon strip tracker
  bad-component mask derived by the demonstrator;
* the HLT Z→e⁺e⁻ peak for fill 11237 (2025);
* the online monitoring in 2026: HLT path rates, and the Z→e⁺e⁻ and π⁰→γγ
  peaks in the DQM;
* the effect of the per-run HLT tracker alignment on the track impact
  parameters, the dimuon vertex pointing angle, the unconstrained dimuon
  vertices and the Z→μ⁺μ⁻ mass resolution;
* the computing performance of the calibration workflows: derivation times,
  upload latencies, and the margin to the 8 h buffer limit.

All approved figures are in [`figures/`](figures), as PNG and, where one exists,
PDF. The file names are the ones on the TWiki.

## Contents

| directory | what |
|---|---|
| [`figures/`](figures) | the approved figures, with their TWiki names |
| [`Alignment/`](Alignment) | the run selection used for the alignment figures; the scripts are in [`NERDAnalysis2026/.../plotting/alignment`](../../../NERDAnalysis2026/AnalysisPipeline_ms/max_internship/plotting/alignment) |
| [`DiMuonNoVtx/`](DiMuonNoVtx) | the `config.yaml` and `luminosity.py` patch used for the unconstrained dimuon vertex mass figure |
| [`Computing/uploads/`](Computing/uploads) | the conddb tag dumps, the run list and the scripts behind the upload latency and margin figures |

## Figures and how they were made

### Tracker and ECAL calibrations

| figure | source |
|---|---|
| `NGT_SiStripBadComponents_HLTvsNGT_Fill11737` | Tracker map of the SiStrip bad-component difference HLT − NGT, fill 11737 (15 May 2026), from the CMS Conditions Database. *Recipe still to be added.* |
| `NGT_SiStripBadComponents_PromptvsNGT_Fill11737` | The same map for Prompt − NGT. *Recipe still to be added.* |
| `NGT_EcalLaser_P2_History_2025` | `P2_MeanHistoryComparison_2025_time` of [EcalLaser_DPNote_Fall2026_plotsFinal](https://marcomusich.web.cern.ch/display/EcalLaser_DPNote_Fall2026_plotsFinal/), from the CMS Conditions Database. *Script still to be added.* |
| `NGT_EcalLaser_P2_RelDiffHistory_2025` | `P2_PercentDiffHistory_2025_time` of the same page. |
| `NGT_EcalLaser_Fill11237_EndOfFill` | `LS_0842` of the same page: p1, p2 and p3 differences NGT vs HLT for EB, EE+ and EE−, at the end of fill 11237. |
| `NGT_HLT_Zee_Fill11237` | The HLT Z→e⁺e⁻ peak with HLT, Prompt and NGT conditions, fitted with a double-sided Crystal Ball plus an exponential (the model of [`Z_to_ee_fit.py`](../../../NERDAnalysis2026/AnalysisPipeline_ms/max_internship/plotting/Z_to_ee_fit.py)). *Command still to be added.* |

### Tracker alignment and muon tracking

The data are the 2026 HLT Scouting DQM of the NERD reprocessing (pipeline
step `dqm/scouting.sh`) for 90 runs, 402536–403867. The run selection keeps 76
runs, 11.89 fb⁻¹ ([`Alignment/selection/`](Alignment/selection): `runs_used.txt`,
and `excluded_runs.csv` with the reason for each removed run).

The scripts and the full command chain are in
[`plotting/alignment/README.md`](../../../NERDAnalysis2026/AnalysisPipeline_ms/max_internship/plotting/alignment/README.md).
Running that chain on the same DQM files reproduces the approved PNGs listed
below.

| figure | output of the chain |
|---|---|
| `NGT_IP_dxyVsPt_pt1` | `plots/selected/without_prompt_single_no_outliers/profile_dxyVsPt_pt1` |
| `NGT_IP_dxy_vsLumi_pt1` | `plots/selected/without_prompt_single_no_outliers/dxyVsEta_pt1_average` |
| `NGT_IP_dxy_vsLumi_pt10` | `plots/selected/without_prompt_single_no_outliers/dxyVsEta_pt10_average` |
| `NGT_IP_dzRMS_vsLumi_pt1` | `plots/selected/without_prompt_single_no_outliers/dzVsEta_pt1_spread` |
| `NGT_DimuonPointingAngle_Sketch` | `plots/sketches/pointing_angle` |
| `NGT_DimuonPointingAngle_CosPhi3D` | `plots/selected/without_prompt_vs0/aggregate_CosPhi3D` |
| `NGT_DimuonPointingAngle_Asymmetry_vsLumi` | `plots/selected/without_prompt_single_no_outliers/dimu_CosPhi3D_asym` |
| `NGT_Zmumu_MassResolution_vsEtaMinus` | `plots/weakmodes/DiMuon/without_prompt/mass_fits/MassVsEtaMinus_width` |

#### `NGT_DimuonNoVtx_InvariantMass`

This figure is `Muons/Properties/SVSelection/SVNoVtx_mass_JPsi`, made with the
generic 1D Scouting DQM plotter `all_1D_ScoutingDQM.py`. That plotter is at
`ae38ba9` of the branch `codex/scouting-2d-comparisons`, which has not been
merged into `main` yet. The run used [`DiMuonNoVtx/config.yaml`](DiMuonNoVtx/config.yaml)
and the mplhep ≥ 1.0 label fix in
[`DiMuonNoVtx/luminosity_mplhep1.patch`](DiMuonNoVtx/luminosity_mplhep1.patch).
The patch changes only how the CMS label is passed. From the `plotting/`
directory of that branch:

```bash
git checkout ae38ba9 -- .        # or the merged version, once available
cp <path to ApprovedPlots>/CMS-DP-2026/158/DiMuonNoVtx/config.yaml .
patch -p1 < <path to ApprovedPlots>/CMS-DP-2026/158/DiMuonNoVtx/luminosity_mplhep1.patch
python3 all_1D_ScoutingDQM.py --local \
  --include '^Muons/Properties/SVSelection/SVNoVtx_mass_JPsi$' \
  --ratio-ylim 0.5 1.5 --jobs 1
# -> png/Comparison_Muons_Properties_SVSelection_SVNoVtx_mass_JPsi.png
```

This reproduces the approved PNG pixel for pixel. The condition paths in
`config.yaml` (`../scouting/{HLT,NGT}/`) are relative to the working directory.

> **Note on `config.yaml`:** as used, it reads the `HLT Conditions` entry from
> `../scouting/NGT/` and the `NGT Conditions` entry from `../scouting/HLT/`.
> The file is kept here unchanged, as the record of what produced the approved
> figure.

### Monitoring

| figure | source |
|---|---|
| `NGT_HLTPathRates_Fill11745` | A screenshot of the CMS trigger-rate monitoring tool for fill 11745. The NGT demonstrator rates are scaled by its prescale of 110. |
| `NGT_DQM_Zee_Fill11675` | A screenshot of the online DQM display, `HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ` `di-Electron_Mass`, HLT farm vs NGT demonstrator, fill 11675. |
| `NGT_DQM_Pi0_Fill11675` | A screenshot of the online DQM display, Scouting diphoton invariant mass `h_mass_Scouting`, fill 11675. |

### Computing performance

| figure | source |
|---|---|
| `NGT_Calib_DerivationTime` | The derivation time of five calibrations, NGT demonstrator vs PCL, October 2025 to June 2026. *Script still to be added.* |
| `NGT_Calib_DerivationTime_Distributions` | The same data as distributions (Gaussian KDE on a log scale). *Script still to be added.* |
| `NGT_Upload_First_vsRunStart` | `Computing/uploads`: `figs/fig2_cdf_first_start` |
| `NGT_Upload_First_vsRunEnd` | `Computing/uploads`: `figs/fig2_cdf_first_end` |
| `NGT_Upload_Last_vsRunStart` | `Computing/uploads`: `figs/fig2_cdf_last_start` |
| `NGT_Upload_Last_vsRunEnd` | `Computing/uploads`: `figs/fig2_cdf_last_end` |
| `NGT_Upload_MarginToTimeout_First` | `Computing/uploads`: `figs/fig10_margin_to_timeout_start` |
| `NGT_Upload_MarginToTimeout_Last` | `Computing/uploads`: `figs/fig10_margin_to_timeout_end` |

To produce the upload figures (Python 3 with `numpy`, `pandas`, `matplotlib`, `mplhep`):

```bash
cd Computing/uploads/analysis
python3 analyze_uploads.py     # reads ../*.txt -> out/*.csv, out/summary.json
python3 make_figures.py        # -> figs/*.png, figs/*.pdf
```

This reproduces the six approved PNGs pixel for pixel.

* The `*_NGTDemonstrator.txt`, `EcalLaserAPDPNRatios_prompt_v3_inRunLSIoVs.txt`
  and `SiPixelAliHLTHGCombined_PCL_v0_hlt.txt` files are conddb tag dumps: every
  payload of the tag, with its since and insertion time.
* `runs.txt` is the CMS run list with start and end times (the `conddb listRuns`
  format), cut to runs ≥ 390000.

[`Computing/uploads/analysis/README.md`](Computing/uploads/analysis/README.md)
gives the definitions, the selection and the headline numbers.
