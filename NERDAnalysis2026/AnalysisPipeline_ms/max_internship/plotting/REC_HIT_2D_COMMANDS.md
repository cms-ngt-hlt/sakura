# Approved RecHit comparisons with the generic 2D plotter

Run these from `plotting/`, in the plotting Python environment. The commands
reproduce the histogram selection, comparison direction, axis labels, color
limits and projection definitions from the scripts in
`ApprovedPlots/CMS-DP-2026/028/EGamma/FinalPlots/HLTScoutingEGamma`.
They use the current generic layout, CMS label and configured data/luminosity;
matching numerical results requires the same input files and run selection.
These are not pixel-for-pixel reproductions of the approved images.

The approved PNG examples compare HLT against NGT. The regexes accept both
older `EtaPhitMap` names and newer `EtaPhiMap`/`XYMap` names. Check availability
with the same `--include` followed by `--list` if necessary. `--local` selects
input paths relative to the working directory instead of the pipeline config.

## EB absolute difference, with ieta and iphi projections

```bash
python3 all_2D_ScoutingDQM.py \
  --include '^Miscellaneous/CaloRecHitsAccepted/ebRecHitsEtaPhit?Map$' \
  --pair HLT NGT --difference absolute --abs-z-limit 1000 \
  --xlabel 'RecHit EB $i\eta$' --ylabel 'RecHit EB $i\phi$' \
  --cbar-label 'Diff. in Number of RecHits (HLT - NGT)' \
  --pdf-name Comparison_EB_Maps_Diffs.pdf
```

## EB relative difference, with ieta and iphi projections

```bash
python3 all_2D_ScoutingDQM.py \
  --include '^Miscellaneous/CaloRecHitsAccepted/ebRecHitsEtaPhit?Map$' \
  --pair HLT NGT --difference relative --rel-z-limit 0.08 \
  --xlabel 'RecHit EB $i\eta$' --ylabel 'RecHit EB $i\phi$' \
  --cbar-label 'Rel. Diff. (HLT - NGT) / NGT' \
  --pdf-name Comparison_EB_Maps_RelDiffs.pdf
```

## EE+ absolute difference, with ix and iy projections

```bash
python3 all_2D_ScoutingDQM.py \
  --include '^Miscellaneous/CaloRecHitsAccepted/eePlusRecHits(EtaPhit?Map|XYMap)$' \
  --pair HLT NGT --difference absolute --abs-z-limit 1000 \
  --xlabel 'RecHit EE+ $ix$' --ylabel 'RecHit EE+ $iy$' \
  --cbar-label 'Diff. in Number of RecHits (HLT - NGT)' \
  --pdf-name Comparison_EEPlus_Maps_Diffs.pdf
```

## EE+ relative difference, with radial projection

```bash
python3 all_2D_ScoutingDQM.py \
  --include '^Miscellaneous/CaloRecHitsAccepted/eePlusRecHits(EtaPhit?Map|XYMap)$' \
  --pair HLT NGT --difference relative --rel-z-limit 0.30 \
  --xlabel 'RecHit EE+ $ix$' --ylabel 'RecHit EE+ $iy$' \
  --cbar-label 'Rel. Diff. (HLT - NGT) / NGT' \
  --projection radial --radial-center 50.5 50.5 \
  --radial-bin-width 1 --radial-xlim 0 60 --aspect equal \
  --pdf-name Comparison_EEPlus_Maps_RelDiffs_RadialProj.pdf
```

The radius is in crystal-index coordinates here, **not cm**. Width 1 matches
the original unit-spaced crystal bins; omit `--radial-bin-width` to use the
minimum x-bin width automatically. Radial projections sum each condition in
annuli first and then compute the difference (or relative difference).
For profiles, weighted sums and weights are projected before computing means.

For EE-, replace `eePlus` with `eeMinus`, `EE+` with `EE-`, and `EEPlus` in
the output filename with `EEMinus`.

For the three pair directions used by the old scripts, replace `--pair HLT NGT`
with `--pair Prompt NGT --pair HLT NGT --pair HLT Prompt` and omit the literal
`--cbar-label` so that each map gets its own automatically generated formula.
Omitting `--pair` uses the generic plotter's defaults (NGT/Prompt, Prompt/HLT,
HLT/NGT), which differ in direction from two of the old scripts' pairs.

Additional controls: `--xlim MIN MAX` and `--ylim MIN MAX` set map display
limits and the corresponding Cartesian projection limits. They do not crop
bins before summation or change radial projections. `--xlabel` and `--ylabel`
override labels only. `--pdf-name` implies a single PDF and appends the run
number in per-run mode. Radial PNGs include `_radial` before comparison tags
so Cartesian and radial versions coexist. Existing run filters, luminosity
exclusions, PNG options and beam-line masks still apply.

As before, these maps show differences, not statistical significance; profile
uncertainties and correlations are not propagated.
