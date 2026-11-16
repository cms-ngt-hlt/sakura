# Tracker-alignment plots: HLT vs NGT (vs Prompt) conditions

These scripts produce the tracker-alignment and muon-tracking figures of
[CMS-DP-2026/158](../../../../../ApprovedPlots/CMS-DP-2026/158): track impact
parameters, the Z&rarr;&mu;&mu; vertex pointing angle and the Z&rarr;&mu;&mu;
mass resolution versus &eta;. They compare the same events reprocessed with the
HLT, Prompt and NGT conditions.

They read the Scouting DQM output of the analysis pipeline (`dqm/scouting.sh`).
Unlike the scripts in `..`, they do not use `scouting_plot.py` or `config.yaml`.
Running the chain below on the DQM files of the DP note reproduces its PNGs pixel for pixel.

## Inputs

* **DQM files:** `<DQMDIR>/scouting/{HLT,Prompt,NGT}/DQM_scouting_R<run 9 digits>.root`.
  This is the layout `04_run_dqm.sh` writes below `DQM_DEST_BASE`, so pass
  `-d $DQM_DEST_BASE`. The default is the `plotting/` directory. The histograms
  used are in `HLT/Run summary/ScoutingOffline/`:
  * `Tracks/TracksPV/{dxy,dz}Vs{Eta,Phi,Pt}_pt{1,10}`, for the impact parameters;
  * `DiMuon/DiMuonVertexMonitor/CosPhi3D`, for the pointing angle;
  * `DiMuon/DiMuonAlignmentMonitor`, for the mass versus &eta;.
* **Luminosity:** `../lumi_data.csv`, the brilcalc CSV shared with the other plotters.
* **Run selection** (`data/`): `run_exclusion.csv` and `metrics.csv` of the
  online NGT-demonstrator DQM scan. These give the EXCLUDE-TRACKING runs and the
  run start times. `plot_trends.py` uses them to write `results/runs_used.txt`,
  which every later step reads. A run is also removed if one condition set has
  ≥ 0.3 fewer layers per track than the median of the three, or fewer than 6
  layers. It is also removed if it has fewer than 5000 events, or if a condition
  set is missing. `results/excluded_runs.csv` gives the reason for each removal.

## Environment

Python 3 with `numpy`, `pandas`, `scipy`, `uproot`, `matplotlib` and `mplhep`.
No ROOT or CMSSW is needed. The Scouting-plots virtual environment of
[`../README.md`](../README.md) works after `pip install pandas scipy`.

## Full chain (in this order)

```bash
cd plotting/alignment
DQMDIR=/path/to/DQM_DEST_BASE        # holds scouting/{HLT,Prompt,NGT}
python3 extract_ip.py -d $DQMDIR                   # results/ip_summary.csv, results/quality.csv
python3 plot_trends.py --lumi auto                 # run selection -> results/runs_used.txt, excluded_runs.csv; IP trends
python3 alignment_trends.py -d $DQMDIR --lumi auto # results/alignment_trends.csv (per-run <cos phi>, ...)
python3 plot_profile_averages.py -d $DQMDIR --lumi 11.89   # profiles averaged over the runs
python3 cosphi_aggregate.py -d $DQMDIR --lumi 11.89        # cos phi summed over the runs
python3 cosphi_asymmetry_trend.py -d $DQMDIR       # per-run asymmetry A -> plots/selected/<set>/dimu_CosPhi3D_asym
python3 make_selected_plots.py -d $DQMDIR          # plots/selected/<set>/ (the figure sets, see below)
python3 weakmodes_aggregate.py -d $DQMDIR -j 8     # plots/weakmodes/DiMuon/<set>/mass_fits/ (mass resolution vs eta)
python3 draw_pointing_angle_sketch.py              # plots/sketches/pointing_angle (no input)
```

`--lumi 11.89` is the recorded luminosity (fb<sup>&minus;1</sup>) of the
selected runs that `plot_trends.py --lumi auto` prints. Set it to the value for
your own selection. Outputs go to `plots/` and `results/` in this directory.

`make_selected_plots.py` and `cosphi_asymmetry_trend.py` write one sub-folder
per style in `make_selected_plots.SETS`. The two styles used in the DP note are
listed below, and the docstring of `make_selected_plots.py` describes the others.

* `without_prompt_single_no_outliers/`: HLT and NGT only, in a single square
  panel. The luminosity label has the year and 3 significant digits. Runs whose
  error is more than 3 times the median error are not drawn in the trends.
* `without_prompt_vs0/`: HLT and NGT only. Below the cos &phi; distribution is the
  unbalance U(x) = N(x) &minus; N(&minus;x), in per mille.

## Figures of CMS-DP-2026/158

| DP figure | output of this chain | script |
|---|---|---|
| `NGT_IP_dxyVsPt_pt1` | `plots/selected/without_prompt_single_no_outliers/profile_dxyVsPt_pt1` | `make_selected_plots.py` (`plot_profile_averages.plot`) |
| `NGT_IP_dxy_vsLumi_pt1` | `plots/selected/without_prompt_single_no_outliers/dxyVsEta_pt1_average` | `make_selected_plots.py` (`plot_trends.styled_plot`) |
| `NGT_IP_dxy_vsLumi_pt10` | `plots/selected/without_prompt_single_no_outliers/dxyVsEta_pt10_average` | `make_selected_plots.py` |
| `NGT_IP_dzRMS_vsLumi_pt1` | `plots/selected/without_prompt_single_no_outliers/dzVsEta_pt1_spread` | `make_selected_plots.py` |
| `NGT_DimuonPointingAngle_Sketch` | `plots/sketches/pointing_angle` | `draw_pointing_angle_sketch.py` |
| `NGT_DimuonPointingAngle_CosPhi3D` | `plots/selected/without_prompt_vs0/aggregate_CosPhi3D` | `make_selected_plots.py` (`cosphi_aggregate.plot`) |
| `NGT_DimuonPointingAngle_Asymmetry_vsLumi` | `plots/selected/without_prompt_single_no_outliers/dimu_CosPhi3D_asym` | `cosphi_asymmetry_trend.py` |
| `NGT_Zmumu_MassResolution_vsEtaMinus` | `plots/weakmodes/DiMuon/without_prompt/mass_fits/MassVsEtaMinus_width` | `weakmodes_aggregate.py` |

## Quantities

* **average**: the entries-weighted mean of the profile bins, with its
  statistical error. Bins with fewer than 100 entries, and &eta; bins outside
  &#124;&eta;&#124; < 2.5, are not used.
* **spread** (RMS): the RMS of the bin contents with the statistical part
  removed, &radic;(RMS&sup2; &minus; &lang;&sigma;&sup2;&rang;).
* **asymmetry**: A = (N<sub>cos &phi;<sub>3D</sub> > 0</sub> &minus;
  N<sub>cos &phi;<sub>3D</sub> < 0</sub>) / N, with
  &sigma;<sub>A</sub> = &radic;((1 &minus; A&sup2;) / N). For prompt Z decays it is
  expected to be 0. Runs with fewer than 1000 pairs are not drawn.
* **mass resolution vs &eta;** (`weakmodes_aggregate.py`): the TH2 of mass
  versus &eta; is summed over the runs, and the mass is fitted in each &eta; bin.
  The fit model is a Breit&ndash;Wigner (&Gamma;<sub>Z</sub> fixed) convolved
  with a double-sided Crystal Ball, plus an exponential. The tails are fitted
  once on the sum of the condition sets, then fixed. The "width" is the Gaussian
  core &sigma;. `fit_dilepton.py` and `fit_zmumu.py` provide the fit functions.

The three condition sets contain the same events, so their statistical
uncertainties are largely correlated.
