# Quick recipe

### To copy the input DQM files

```bash
./copyAll.sh
```

### To produce the per-run efficiencies
```bash
  python3 compute_eff.py --folder dqm_files
```

### To produce the per-filter efficiency vs run
```bash
  python3 plotAll.py --infile out_barrelendcaps_NGT.root --outdir ./plots_NGT --label "NGT demonstrator"
  python3 plotAll.py --infile out_barrelendcaps_HTS.root --outdir ./plots_HTS --label "HLT Test Stand"
```

### To overal NGT and Test Stand
```bash
  python3 overlay.py --regions EB EE --which total
```
of
```bash
  python3 overlay.py --which all
```
### TO produce the aggregated efficiencies
```bash
  python3 aggregate_eff.py --pattern NGT --outfile aggregated_NGT.root --outdir plots_agg_NGT
  python3 aggregate_eff.py --pattern Test --outfile aggregated_HTS.root --outdir plots_agg_HTS
```
