# `all_1D_ScoutingDQM.py` — compare *all* 1D histograms of the Scouting DQM

The hand-tuned entry scripts (`variables_ScoutingECALRecHits.py`,
`invariantMass_ScoutingDielectron.py`, ...) each compare a short, hardcoded
list of histograms across the conditions in `config.yaml`. The Scouting DQM
files, however, contain about 2500 1D histograms (`TH1*`) in ~45 sub-folders
(`Jet/...`, `EGamma/...`, `Muons/...`, `Miscellaneous/...`, `Tracks/...`, ...).

`all_1D_ScoutingDQM.py` is a generic entry script built on the same
`scouting_plot.ComparisonPlot1D` framework: it **discovers** every `TH1*`
below `dqm_prefix` in the DQM files and produces, for each one, the usual
3-condition overlay with the ratio-to-reference panel and the gray statistical
uncertainty band of the reference.

## Prerequisites

* Python 3 with `numpy`, `uproot`, `pyyaml`, `matplotlib`, `mplhep`
  (same as the other plotting scripts; `pip3 install --user mplhep uproot pyyaml`
  if missing).
* Run from the `plotting/` directory (the script imports `scouting_plot.py`
  and reads `config.yaml` from there).
* Set `DQM_DEST_BASE` in the pipeline's `pipeline.cfg`, for example
  `DQM_DEST_BASE="DQM_OUTPUT"`. Relative base paths are resolved from the
  directory containing `pipeline.cfg`, not from `plotting/`; absolute paths
  and Bash variable expansion are supported. The config is sourced with Bash,
  just as in the pipeline, so use a trusted config file.
* The per-condition paths from `config.yaml` (`Prompt`, `HLT`, `NGT`
  by default) are resolved under `$DQM_DEST_BASE/scouting/` when that folder
  exists, otherwise directly under `$DQM_DEST_BASE/` for older outputs.
  With the example above, inputs are `DQM_OUTPUT/scouting/Prompt/*.root`,
  `DQM_OUTPUT/scouting/HLT/*.root`, and `DQM_OUTPUT/scouting/NGT/*.root`.
  Absolute condition paths remain explicit overrides. Missing directories or
  an empty `DQM_DEST_BASE` produce an error. These directories must contain
  the DQM files (`DQM_V0001_ScoutingDQM_R00XXXXXX.root`). Everything about *which*
  conditions, the reference, colours, the CMS label (year / lumi / √s) and the
  path inside the ROOT file is taken from `config.yaml` exactly as for the
  other scripts; nothing plot-specific has to be edited in the script.

## Basic usage

```bash
cd plotting
python3 all_1D_ScoutingDQM.py
```

This walks the DQM tree of the reference condition's first ROOT file (plus the
first file of every other condition, so the union is used), then reads all
selected histograms from every file **in one pass per file** (summing over
files per condition), renders the PDF groups **in parallel** (one process per
group, all cores by default) and writes:

* one multi-page PDF **per top-level DQM folder**:
  `Comparison_All1D_Jet.pdf`, `Comparison_All1D_EGamma.pdf`,
  `Comparison_All1D_Miscellaneous.pdf`, ... (one page per histogram, page
  title = `sub/folder/histogram_name`);
* one PNG per histogram in `output.png_dir` (default `png/`), named
  `Comparison_<sub_folder>_<histogram_name>.png`, e.g.
  `png/Comparison_Miscellaneous_CaloRecHitsAccepted_ebRechits_energy.png`
  (the folder is part of the name because e.g. `Jet/L1_HTT200er` and
  `Jet/L1_HTT255er` contain identically named histograms).

Histograms that are **empty in every condition** are skipped (in a typical
single-run file more than half of them are). A summary line at the end says
how many were plotted / skipped. A folder with nothing to plot produces no PDF.

Timing: reading the data is fast (a few seconds per ROOT file, once); the cost
is matplotlib rendering, ~0.6 s per non-empty histogram per core. A full run
(~1000 non-empty histograms) takes ~10 min on one core, divided by the number
of parallel groups you allow (`--jobs`, `--group-by subdir` gives many small
groups and hence the best speed-up). `--no-png` saves another ~25 %. Use the
filters below to run only what you need.

## Options

```
python3 all_1D_ScoutingDQM.py -h
```

| option | meaning |
|---|---|
| `--config PATH` | alternative `config.yaml` (default `config.yaml`) |
| `--pipeline-cfg PATH` | alternative pipeline config (default: `pipeline.cfg` beside the pipeline scripts) |
| `--include REGEX` | only histograms whose `sub/folder/name` matches; repeatable (OR-ed) |
| `--exclude REGEX` | drop histograms whose `sub/folder/name` matches; repeatable |
| `--list` | print the selected histograms (after include/exclude) and exit, no plotting |
| `--group-by top\|subdir` | one PDF per top-level folder (`Comparison_All1D_Jet.pdf`, default) or per sub-folder (`Comparison_All1D_Jet_L1_HTT200er.pdf`, ...) |
| `--single-pdf` | write one `Comparison_All1D.pdf` for everything (implies `--jobs 1`) |
| `--jobs N`, `-j N` | render the PDF groups in N parallel processes (default: all cores) |
| `--no-png` | write only the PDFs, skip the per-histogram PNGs |
| `--yscale auto\|log\|linear` | main-panel y-scale; `auto` (default) = log if the highest bin is > 100, else linear with scientific ticks (same rule as the dilepton script) |
| `--keep-empty` | also plot histograms that are empty in every condition |
| `--limit N` | only the first N selected histograms (quick tests) |

The regexes are Python `re.search` patterns against the path relative to
`dqm_prefix`, e.g. `Miscellaneous/CaloRecHitsAccepted/ebRechits_energy`.
Anchor with `^` to match a folder from its start.

## Examples

See what is in the files without plotting anything:

```bash
python3 all_1D_ScoutingDQM.py --list
```

Only the ECAL/HCAL RecHit folders, in one PDF:

```bash
python3 all_1D_ScoutingDQM.py --include "^Miscellaneous/CaloRecHits" --single-pdf
```

All Jet histograms of the `PFScoutingJetHT` path, but not the L1-seed folders:

```bash
python3 all_1D_ScoutingDQM.py --include "^Jet/" --exclude "^Jet/L1_"
```

Everything muon-related, forced to log scale:

```bash
python3 all_1D_ScoutingDQM.py --include "^Muons/" --include "^Miscellaneous/muons" --include "^DiMuon/" --yscale log
```

Quick smoke test (first 5 histograms of the Tracks folder):

```bash
python3 all_1D_ScoutingDQM.py --include "^Tracks/" --limit 5
```

Fastest full survey: everything, one PDF per sub-folder, no PNGs, all cores:

```bash
python3 all_1D_ScoutingDQM.py --group-by subdir --no-png
```

## What is generic (and how to override it)

Because nothing is known in advance about the ~2500 histograms, the per-plot
cosmetics are derived from the ROOT objects themselves:

* **x-label**: the ROOT x-axis title. ROOT markup (`#eta`, `p_{T}`,
  `#chi^{2}/ndof`, `d_{xy} [#mum]`, ...) is converted to matplotlib mathtext;
  titles that cannot be converted are shown as plain text. If the axis title is
  empty, the histogram name is used.
* **y-label**: the ROOT y-axis title, or `Entries` if empty.
* **x-range**: the full histogram range; **ratio range**: 0–2 (framework default).
* **y-scale**: see `--yscale`.

If a particular histogram needs dedicated treatment (zoomed x-range, special
labels, rebinning, reference lines), do what the other entry scripts do:
write a small subclass of `ComparisonPlot1D` (or of `All1DPlot`) and override
`decorate()` / `transform()` for that histogram — see
`variables_ScoutingECALRecHits.py` for the pattern. Keep `all_1D_ScoutingDQM.py`
generic.

## Relation to the other scripts

The dedicated scripts remain the reference for the "publication" versions of
their histograms (hand-tuned ranges and labels, rebinning for the dilepton
masses). `all_1D_ScoutingDQM.py` is meant for the broad survey: spotting
*where* the conditions differ across the full DQM content before zooming in
with a dedicated script.
