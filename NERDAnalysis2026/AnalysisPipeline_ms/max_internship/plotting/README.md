# Plotting scripts

This directory contains the [Scouting DQM comparison plotter](#scouting-dqm-comparison)
and the [HLT Z-to-ee fit plotters](#hlt-z-to-ee-fit-plotters).

## Scouting DQM comparison

`all_1D_ScoutingDQM.py` compares *all* 1D histograms of the Scouting DQM.

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
  (same as the other plotting scripts; see the virtual-environment recipe below).
* Run from the `plotting/` directory (the script imports `scouting_plot.py`
  and reads `config.yaml` from there).
* In default pipeline mode, set `DQM_DEST_BASE` in the pipeline's `pipeline.cfg`, for example
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
* With `--local`, `pipeline.cfg` is never read or sourced, and `DQM_DEST_BASE`
  is not required. Each condition's `path` in `config.yaml` is used relative
  to the current working directory; absolute paths and `~` paths also work.
  This flag controls input lookup, so it can also be used on LXPLUS.

## Python environment for Scouting plots (LXPLUS or laptop)

For LXPLUS, first connect with `ssh YOUR_CERN_USERNAME@lxplus.cern.ch`.
Run the following setup on the machine where you will plot. Use a fresh shell
without `cmsenv` or an LCG environment: plotting uses uproot, not PyROOT, and
does not require CMSSW. On LXPLUS, `/usr/bin/python3` can be used in place of
`python3` below to explicitly select the system Python.

Create the environment once (do not copy a laptop environment to LXPLUS):

```bash
mkdir -p "$HOME/venvs"
python3 -m venv "$HOME/venvs/scouting-plots"
source "$HOME/venvs/scouting-plots/bin/activate"
python -m pip install --upgrade pip
python -m pip install numpy uproot pyyaml matplotlib mplhep
```

For every subsequent login or new terminal, activate it again:

```bash
source "$HOME/venvs/scouting-plots/bin/activate"
```

Check the environment before running:

```bash
which python
python -m pip --version
python -c "import numpy, uproot, yaml, matplotlib, mplhep; print('Environment ready')"
```

The Python executable and pip location should both be inside
`$HOME/venvs/scouting-plots`. If pip defaults to a user installation, check that
you activated the environment. If pip or packages still come from `/cvmfs/cms-ib/...`,
the shell is still exposing CMS packages (for example through `PYTHONPATH`).
Start a clean shell without the CMS setup and create a separate environment
with `/usr/bin/python3 -m venv "$HOME/venvs/scouting-plots-clean"`, then activate
that environment and install the packages as above.

The script uses Matplotlib's headless backend; no display or `ssh -X` is needed.
If an older checkout raises `exp_label() got an unexpected keyword argument 'text'`,
update the `hep.cms.label(...)` call in `scouting_plot.py` to use
`label="Private Work (CMS data)"` instead of `text=...` (already fixed here).

## LXPLUS recipe: use pipeline output

After activating the environment, enter the checkout's `plotting/` directory.
Set `DQM_DEST_BASE` in `../pipeline.cfg` to the actual input location accessible
on LXPLUS, for example `DQM_DEST_BASE="/eos/.../DQM_OUTPUT"` (replace the example
path). The expected directories are `scouting/Prompt`, `scouting/HLT` and
`scouting/NGT` below that base, or directly `Prompt`, `HLT` and `NGT` for older
outputs without a `scouting/` directory.

```bash
cd /path/to/max_internship/plotting
python all_1D_ScoutingDQM.py --limit 5 --jobs 1
python all_1D_ScoutingDQM.py --jobs 1 --no-png
```

Keep `--jobs 1` on a shared LXPLUS login node: the default otherwise uses all
available cores. For larger parallel runs, use batch resources and set `--jobs`
to the number of allocated cores. Omit `--no-png` to also write PNGs.

## Local recipe: use condition folders directly

Place the DQM ROOT files in these folders (or edit the condition paths in
`config.yaml` to point to their actual locations):

```text
plotting/
  config.yaml
  Prompt/*.root
  HLT/*.root
  NGT/*.root
```

With the environment activated, run:

```bash
cd /path/to/max_internship/plotting
python all_1D_ScoutingDQM.py --local --list
python all_1D_ScoutingDQM.py --local --limit 5 --jobs 1
python all_1D_ScoutingDQM.py --local --jobs 2 --no-png
```

`--local` does not search recursively or add a `scouting/` prefix. For example,
`path: "Prompt"` means `./Prompt`, and `path: "../DQM_OUTPUT/scouting/Prompt"`
uses that relative directory. Relative paths remain relative to your working
directory even when using `--config /somewhere/other.yaml`. A missing or empty
`pipeline.cfg` is irrelevant; even an explicit `--pipeline-cfg` is ignored.
Every configured condition directory must exist and should contain its `.root`
files. PDFs are written to the working directory and PNGs to `output.png_dir`.

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
| `--local` | bypass `pipeline.cfg`; use condition paths relative to the current working directory (absolute paths also work) |
| `--pipeline-cfg PATH` | alternative pipeline config (default: `pipeline.cfg` beside the pipeline scripts); ignored with `--local` |
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

Full survey on allocated compute resources: everything, one PDF per sub-folder,
no PNGs, all cores (on an LXPLUS login node, add `--jobs 1`):

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

## HLT Z-to-ee fit plotters

The two `Z_to_ee*.py` scripts compare the **HLT**, **NGT**, and **Prompt**
conditions using the HLT DQM `di-Electron_Mass` histogram. Both fit a
double-sided Crystal Ball signal plus an exponential background.

* `Z_to_ee_fit.py` combines the runs for each condition, fits the mass
  distribution, and writes `Zee_Comparison_Final.png`, with fit sanity checks
  in `fit_sanity_checks/`.
* `Z_to_ee_fit_stability_per_fill.py` combines runs within each LHC fill and
  fits each condition per fill. It plots the fitted peak position and relative
  resolution (`sigma / mu`) versus cumulative recorded luminosity in
  `Zee_Stability_Lumi_PerFillFit.png`, writes individual fit checks in
  `fit_sanity_checks_per_fill/`, and prints a fit summary table.

### Environment and inputs

These scripts require **ROOT with PyROOT** (`import ROOT`), plus `numpy`,
`matplotlib`, `mplhep`, and `uproot`. Use a Python environment with these
packages and a compatible ROOT installation; the uproot-only Scouting
environment above is not sufficient. Check it with:

```bash
python -c "import ROOT, numpy, matplotlib, mplhep, uproot; print('HLT plotting environment ready')"
```

By default, both scripts read `DQM_DEST_BASE` from the pipeline's
`pipeline.cfg` and use the HLT recipe output:

```text
DQM_DEST_BASE/
  hlt/
    HLT/*.root
    NGT/*.root
    Prompt/*.root
```

They also accept older layouts with `HLT/`, `NGT/`, and `Prompt/` directly
under `DQM_DEST_BASE`, or a base pointing at the recipe directory itself.
Relative `DQM_DEST_BASE` paths are resolved from the directory containing
`pipeline.cfg`. All three condition folders must exist and contain the HLT
DQM inputs. Filenames must end in `_R<run>.root` so the scripts can extract
the run number. The histogram path is:

```text
DQMData/Run <run>/HLT/Run summary/ObjectMonitor/MainShifter/di-Electron_Mass
```

These scripts do not read `config.yaml`; condition names, fit settings, and
plot labels are defined in the scripts.

### Get the luminosity CSV with brilcalc

For the per-fill stability plot, generate the run-to-fill mapping and recorded
luminosity on LXPLUS (or a machine with the CERN BRIL CVMFS setup available).
Run these commands from `max_internship/plotting/` to save the CSV beside the
plotters:

```bash
export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH
brilcalc lumi --begin 401623 --end 403937 -u /pb --output-style csv > lumi_data.csv
```

Adjust the run range when plotting a different dataset, keeping the output
units as `/pb`. The per-fill script reads the fill and recorded luminosity
for each run from this CSV. Its cumulative luminosity axis starts at the
first input run with luminosity metadata and ends at the last, retaining
luminosity from intervening CSV runs even if their DQM files are absent.

### Run the HLT plots

From the checkout's `plotting/` directory, with the ROOT-enabled environment
active and `DQM_DEST_BASE` configured:

```bash
cd /path/to/max_internship/plotting
python Z_to_ee_fit.py
python Z_to_ee_fit_stability_per_fill.py --lumi-csv lumi_data.csv
```

Both scripts accept `--pipeline-cfg /path/to/pipeline.cfg` to select another
pipeline configuration. To use `HLT/`, `NGT/`, and `Prompt/` folders directly
under the current directory instead, bypass the pipeline config with `--local`:

```bash
python Z_to_ee_fit.py --local
python Z_to_ee_fit_stability_per_fill.py --local --lumi-csv lumi_data.csv
```

All plots are saved under the current working directory. `--lumi-csv` also
accepts an absolute path; its default is `lumi_data.csv` in the current
directory. The combined-run plotter does not require a luminosity CSV.
