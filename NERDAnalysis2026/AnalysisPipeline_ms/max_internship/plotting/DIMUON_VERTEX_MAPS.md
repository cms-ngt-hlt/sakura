# Side-by-side DiMuonNoVtx vertex maps

From your usual plotting working directory:

```bash
python dimuon_vertex_maps.py --config config.yaml
```

The new script selects `DiMuonNoVtx/DiMuonVertexMonitor/VtxRvsZ` and
`VtxXvsY` (also reversed names and underscore suffixes such as `_zoom`).
Each page shows HLT on the left and NGT on the right, with the original
counts on one shared colour scale. Each map has its two coordinate
projections underneath, with matching vertical scales across conditions.
ROOT axis titles determine coordinate labels/order. Counts are summed over
regular bins, excluding underflow/overflow, without area normalisation.

The default colour scale is symmetric-logarithmic with a linear region up
to one entry; use `--map-scale linear` for linear colours. Projection axes
are linear. Both full maps and extra copies excluding the beam-line region
(`r ≤ 1 cm`, using bin centres) are saved. The masked copies also exclude
those bins from their projections. Use `--no-beamline-copies` to omit them.

```bash
python dimuon_vertex_maps.py --config config.yaml --runs 403244
python dimuon_vertex_maps.py --config config.yaml --include VtxRvsZ
python dimuon_vertex_maps.py --config config.yaml --exclude _zoom --map-scale linear
```

Input paths, luminosity CSV and common-run filtering follow
`all_2D_ScoutingDQM.py`, including validation of **all conditions in the
configuration**. With the standard config this includes Prompt, even though
only HLT and NGT are drawn. A two-condition config can omit Prompt if its
`reference` is also changed to HLT or NGT. `--local`, `--pipeline-cfg`,
`--lumi-csv`, `--per-run`, `--exclude-runs`, `--list` and `--no-png` are
supported.

Output: `Comparison_DiMuonNoVtx_VertexMaps_HLT_vs_NGT.pdf` in the working
directory, plus `SideBySide_*_HLT_vs_NGT*.png` in the configured `png_dir`.
Per-run output names include the run number. The original difference-map
script and its outputs are unchanged.
