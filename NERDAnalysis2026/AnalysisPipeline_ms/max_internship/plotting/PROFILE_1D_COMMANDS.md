# 1D profiles

`all_1D_ScoutingDQM.py` automatically discovers both TH1 histograms and TProfile
objects in all selected files. Use `--include` with the profile path, just as
for counts. Existing `--runs`, `--exclude-runs`, `--per-run`, and axis options apply.

For each TProfile bin, the plotter sums ROOT's stored weighted numerators and
`fBinEntries` across the selected files/runs, then divides. It does not add or
average the individual file means. Empty bins are undefined (NaN); occupied
bins with zero or negative means remain valid. Incompatible bin edges and
TH1/TProfile mixtures are skipped with warnings.

The main panel shows profile means and the lower panel their ratio to the
configured reference. Profile uncertainty propagation is not implemented:
profile curves and ratios have no error bars or reference uncertainty band.
The count-histogram Poisson errors are not applied to means. TH1 plots keep
their existing counting-error behavior.

```bash
python3 all_1D_ScoutingDQM.py --list --include '^Muons/'
```

Use a profile path from that listing with `--include '^PATH$'` to plot it.
