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

## All 2D histograms

`all_2D_ScoutingDQM.py` is the matching generic TH2 and TProfile2D plotter. Run it from
`plotting/` with the same environment and config as the 1D plotter:

```bash
python all_2D_ScoutingDQM.py
python all_2D_ScoutingDQM.py --local --list
python all_2D_ScoutingDQM.py --per-run --include CaloRecHits --no-png -j 4
python all_2D_ScoutingDQM.py --difference relative --rel-z-limit 0.08
```

For each histogram it writes **six pages** (and six PNGs by default):
absolute and relative differences for **NGT vs Prompt**, **Prompt vs HLT**,
and **HLT vs NGT**, in that direction. These pairs are fixed for this entry
script; the older scripts still use `config.yaml`'s `diff_pairs`.
Absolute means signed `A - B`, not `abs(A - B)`; relative means `(A - B) / B`.
Bins with a zero denominator are masked. Each page includes a 2D map and
x/y projection panels. Relative projections sum A and B first, then divide.
No event-count or integral normalization is applied.

The script discovers all `TH2*` and `TProfile2D` objects in every selected
file, using ROOT axis titles and full axis ranges. Profiles are merged by
summing their stored weighted values and bin weights, then dividing to get
the combined mean. Their x/y projections also combine weighted sums and
weights before comparing means; unfilled bins are masked. Absolute profile
differences are in the units of the profiled quantity, relative differences
are dimensionless. Missing pairs and incompatible
binning are skipped with warnings; both edge arrays must match for sums
and comparisons. Histograms empty in every available condition are skipped
unless `--keep-empty` is supplied.

Vertex x/y maps named `VtxXvsY` or `VtxYvsX` (including underscore suffixes
such as `_zoom`) also get an **additional beam-line-masked copy** for each
pair and difference type. Original plots remain unchanged. The extra copy
excludes bins whose centres satisfy `x² + y² ≤ (1 cm)²`, around nominal
`(0, 0)`, from both the map and projections. Vertex coordinates default to
cm; explicit `[mm]`, `(mm)`, `[m]`, or `(m)` axis units are converted to cm.
For `VtxRvsZ` and `VtxZvsR` (also `_zoom`), the extra copy masks radial
bin centres with `|r| ≤ 1 cm` at **every z**, representing the same beam-line
cylinder. The radial axis is identified from ROOT titles (`r`, `rho`, or
`radius`), in either axis order. If it cannot be identified unambiguously,
a warning is printed and only the original is produced. Eta/phi maps are
unaffected. Profile projections
exclude both weighted sums and weights in the disk. The masked copy has
its own automatic color range (explicit z-limits still apply), a visible
mask annotation, and `_beamlineMasked` before the final comparison tags:
`Comparison_All2D_DiMuonNoVtx_DiMuonVertexMonitor_VtxXvsY_beamlineMasked_absolute_HLT_vs_NGT.png`.
Both copies are included in the grouped PDF. Existing output files are not
renamed or removed.

Before discovering or summing 2D histograms, the plotter checks selected runs
against the recorded luminosities in `lumi_csv` (or `--lumi-csv`). Runs missing
from that CSV are **excluded across all conditions**, with a prominent stderr
warning listing every excluded run and DQM file. Neither their bins nor their
luminosity enter the final plots. This also applies to `--list` and per-run
mode; in multi-run files, valid run directories are retained. If all selected
runs lack luminosity, the script stops before rendering. Missing or malformed
CSV files still raise errors rather than silently excluding the dataset.

All input/run/filter/grouping options work as for 1D: `--config`, `--local`,
`--pipeline-cfg`, `--per-run [RUN]`, `--runs`, `--exclude-runs`, `--lumi-csv`,
`--include`, `--exclude`, `--list`, `--limit`, `--group-by`, `--single-pdf`,
`--jobs`, and `--no-png`. The 1D `--yscale` is replaced by:

* `--difference both|absolute|relative` (default: both).
* `--abs-z-limit N`: symmetric absolute color range, with a symmetric-log scale.
* `--rel-z-limit N`: symmetric relative color range, with a linear scale
  (`0.08` means ±8%).

Without explicit limits each map uses its largest finite absolute difference.
Use fixed limits when comparing color intensities across pages.
Outputs are `Comparison_All2D_<Folder>.pdf` (or `Comparison_All2D.pdf` with
`--single-pdf`), with run identifiers in per-run mode. PNG filenames include
histogram path followed by the difference kind and condition pair, and go to
`output.png_dir`, e.g.
`Comparison_All2D_Tracks_eta_vs_phi_absolute_NGT_vs_Prompt.png`.

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

To compare Prompt, HLT and NGT **separately for each run**, add `--per-run`:

```bash
python all_1D_ScoutingDQM.py --local --per-run --jobs 1
```

Supply a run number to plot only that run (also works with `--list`):

```bash
python all_1D_ScoutingDQM.py --include "^Dilepton/" --per-run 403894 --jobs 1
```

If the requested run is unavailable, the script reports an error and lists
the available runs. Bare `--per-run` continues to process all available runs.

Run numbers are read from the `DQMData/Run <number>` directories inside the
ROOT files. Files for the same run and condition are summed; different runs
are never combined. Each run has its own histogram discovery and empty-plot
filtering. Outputs include the run number, for example
`Comparison_All1D_Run403775_EGamma.pdf` and
`png/Comparison_Run403775_EGamma_<histogram>.png`, with the run also labelled
on each plot. `--single-pdf` writes one PDF **per run**;
`--limit N` applies separately to each run, and `--list` lists histograms per run.
Runs available in any condition are included; missing conditions are reported
and omitted from the overlay. If Prompt (or the configured reference) is
missing, the ratio panel has no ratios. Empty histograms are still skipped
unless `--keep-empty` is set. The CMS luminosity label is calculated from that plot’s contributing runs
using the run-level CSV configured by `lumi_csv` in `config.yaml`.
Without `--per-run`, histograms are summed across runs within each condition.
Use `--runs` or `--exclude-runs` to control which runs enter that sum:

```bash
# Sum all available runs except 403894
python all_1D_ScoutingDQM.py --exclude-runs 403894 --jobs 1

# Sum only these three runs
python all_1D_ScoutingDQM.py --runs 403775 403894 403895 --jobs 1

# Plot those runs separately instead
python all_1D_ScoutingDQM.py --runs 403775 403894 403895 --per-run --jobs 1
```

Both filters accept space-separated run numbers and work with `--list` and
histogram filters such as `--include "^Dilepton/"`. Exclusions take precedence;
`--per-run RUN` further restricts the selection to that one run. Unknown
included runs or an empty final selection produce an error. Excluding a run
that is already absent has no effect. Filtered summed plots retain the usual
summed-output filenames (so a later selection overwrites the previous plots);
the selected runs are printed in the terminal. The luminosity label is recalculated for the contributing selected runs.
With neither run filter nor `--per-run`, the existing behavior is unchanged.

```
python3 all_1D_ScoutingDQM.py -h
```

| option | meaning |
|---|---|
| `--config PATH` | alternative `config.yaml` (default `config.yaml`) |
| `--lumi-csv PATH` | override the run-level luminosity CSV configured in `config.yaml` |
| `--xlabel TEXT` | override the x-axis label on every selected 1D plot |
| `--xlim MIN MAX` | shared x limits for the main and ratio panels |
| `--ylim MIN MAX` | main-panel y limits; a nonpositive minimum makes `auto` scale linear; explicit `log` requires positive limits |
| `--ratio-ylim MIN MAX` | ratio-panel y limits (default: `0 2`) |
| `--ylabel TEXT` | override the main-panel y-axis label on every selected 1D plot; the ratio label stays unchanged |
| `--local` | bypass `pipeline.cfg`; use condition paths relative to the current working directory (absolute paths also work) |
| `--per-run [RUN]` | compare conditions separately for all runs, or only RUN if supplied, with run numbers in output names and plots |
| `--runs RUN [RUN ...]` | use only the listed runs; sum them unless `--per-run` is set |
| `--exclude-runs RUN [RUN ...]` | omit the listed runs from summed or per-run plots |
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

Redo one histogram with custom axis labels:

```bash
python3 all_1D_ScoutingDQM.py \
  --include '^DiLepton/electrons_zMass$' \
  --xlabel '$m_{ee}$ [GeV]' \
  --ylabel 'Number of dielectron candidates' \
  --xlim 70 110 --ylim 0 5000 --ratio-ylim 0.8 1.2
```

Labels accept plain text or matplotlib mathtext (use single shell quotes to
preserve `$` and backslashes). Each override applies to **all histograms selected
in that invocation**; run separate commands for plots needing different labels.
Omitted labels retain the ROOT-title defaults; an empty string hides a label.
Limits must be finite with MIN < MAX and apply to every selected plot.
These options change display only, not binning or data. Add `--list` to preview
the selected histogram paths before plotting. Paths use `/`, even though PNG
filenames replace it with `_`.

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
* **x-range**: the full histogram range, overridden by `--xlim MIN MAX`;
  **main y-range**: automatic, overridden by `--ylim MIN MAX`;
  **ratio range**: 0–2, overridden by `--ratio-ylim MIN MAX`.
* **y-scale**: see `--yscale`.

Use `--xlabel` / `--ylabel` to override the axis labels directly.
Use `--xlim`, `--ylim`, and `--ratio-ylim` to set display ranges.
If a particular histogram needs dedicated treatment (rebinning, reference lines),
do what the other entry scripts do:
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
directory. Both HLT plotters require the luminosity CSV and accept `--lumi-csv`.

### Automatic luminosity labels

All plotters use `luminosity.py` to calculate recorded luminosity from the
unique runs actually contributing to each histogram. Scouting scripts use
`lumi_csv: "lumi_data.csv"` in `config.yaml` (relative to the working directory);
all three entry scripts accept `--lumi-csv` (overriding the config for
`all_1D_ScoutingDQM.py`). The HLT scripts default to `lumi_data.csv`.
The CSV must contain one row per run with
`recorded(/pb)`, as generated by the brilcalc command above. Luminosity is
converted to fb⁻¹; repeated files for a run do not duplicate its luminosity.
The former `cms_label.lumi` setting is no longer used.

Run selection and per-run plotting automatically affect the label. Missing
histograms and incompatible shapes skipped during Scouting aggregation do not
contribute runs. Identical condition run sets share one total; differing run
sets show explicitly labelled condition totals at the top. Missing CSV runs,
duplicate run rows, or incompatible units raise an error rather than displaying
an incomplete total. These totals assume full-run coverage, not partial
lumisection inputs. Year and collision energy remain separately configured.

The per-fill stability plot retains intervening CSV luminosity on its x-axis;
its top label counts only runs contributing to successful fits, per condition.
Individual fit sanity plots also get labels for their contributing runs.

The shared module also provides `cumulative_luminosity(...)` for the stability
plot's fill/run membership, cumulative ranges, and midpoints.
For `Z_to_ee_fit_stability_per_fill.py`, the default remains one fit per fill.
Add `--per-run` for one fit per run and condition:

```bash
python Z_to_ee_fit_stability_per_fill.py --lumi-csv lumi_data.csv --per-run
```

Each run point sits at its luminosity midpoint. Its horizontal bar spans the
run's full **recorded** luminosity (half on either side), using the same CSV
quantity as the axis; it is a run extent, not a luminosity uncertainty. Both
mean and resolution panels retain vertical **fill** boundaries and fill labels.
Run outputs use `Zee_Stability_Lumi_PerRunFit.png` and
`fit_sanity_checks_per_run/`, leaving fill outputs separate.

`--per-run RUN` optionally selects just one run. These run-length bars and
retained fill boundaries apply only to `Z_to_ee_fit_stability_per_fill.py`;
other plotters keep their existing behavior. With or without `--per-run`, `--runs` and `--exclude-runs` restrict group membership
while retaining intervening CSV luminosity on the axis. CSV loading, unit
conversion, cumulative coordinates, and CMS labels all live in `luminosity.py`;
ROOT histogram loading and fitting remain in the individual plotters.

For example, each entry script accepts the same luminosity and run options:

```bash
python all_1D_ScoutingDQM.py --lumi-csv lumi_data.csv --per-run 401623
python Z_to_ee_fit.py --lumi-csv lumi_data.csv --per-run 401623
python Z_to_ee_fit_stability_per_fill.py --lumi-csv lumi_data.csv --per-run 401623
```
