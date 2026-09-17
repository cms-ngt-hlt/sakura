# Running `NGT_Studies_2025G.ipynb`

Tag-and-probe electron trigger efficiency comparison, HLT reference vs NGT target, using [egamma-tnp](https://github.com/ikrommyd/egamma-tnp) on top of coffea/dask. Produces per-trigger-leg efficiency histograms and pt/eta/phi efficiency-ratio plots.

## 1. One-time setup (on lxplus)

Connect to lxplus with VS Code's Remote-SSH extension, open its integrated terminal, `cd` into any working directory, then:

```bash
git clone -b 2024_Studies git@github.com:saumyaphor4252/egamma-tnp.git
cd egamma-tnp/
python3 -m venv egmtnpenv
source egmtnpenv/bin/activate
pip install jupyter
pip install ipython
pip install ipykernel
ipython kernel install --user --name=egmtnpenv
python -m ipykernel install --user --name=egmtnpenv
pip install . --no-cache-dir
```

This registers `egmtnpenv` as a Jupyter kernel.

## 2. Open and run the notebook

Connect to lxplus with the Remote-SSH extension, open the folder with the notebook, open `NGT_Studies_2025G.ipynb`, and pick `egmtnpenv` from the kernel picker.

## 3. Input data

The notebook reads pre-produced tag-and-probe ntuples (ROOT files with a `tnpEleTrig/fitter_tree` tree), one for the reference sample and one for the target/NGT sample. Producing these ntuples is covered in
[README_Run3_NGTstudies.md](https://github.com/saumyaphor4252/EGamma-Workflow/blob/master/README_Run3_NGTstudies.md).

Default ntuples used ([`Set3`](https://indico.cern.ch/event/1709644/contributions/7190983/subcontributions/625007/attachments/3313091/5932298/EGM_HLT_NGTstudies_Set3.pdf)). The slides show the first version of the plots made with this set, the final versions used in the DPS note come from this notebook.

- Reference: `/eos/cms/store/group/phys_egamma/ssaumya/NGT_Jessica/merged/tnpNtuple_Reference_Set3.root`
- Target: `/eos/cms/store/group/phys_egamma/ssaumya/NGT_Jessica/merged/tnpNtuple_Target_Set3.root`

`plot_NGT_Studies_2025G_ROOT.py` defaults to the same `Set3` files, but at a different location (`/afs/cern.ch/work/s/ssaumya/public/ForNGT/Ntuples/`), overridable with its `--ref`/`--tgt` flags.

Runs used for `Set3`: 398675, 398680, 398681, 398802.

## 4. Edit before running

- `fileset`, near the top: the reference (`events_HLT`) and target
  (`events_NGT`) ntuple paths.
- Every hardcoded output directory in the notebook (currently
  `/eos/user/m/mzarucki/www/2026/NGT/SAKURA/NERD/efficiencies/...`), change
  to a directory you can write to.
- `hlt_paths` / `plateau_cuts`, only if adding or removing an HLT leg.

## 5. Run it

Run all cells top to bottom.

## 6. Output

Under the output directory from step 4:

- `<dataset>/<leg>_hists.root` and `<dataset>/<leg>_report.json`: one pair
  per dataset (`events_HLT`, `events_NGT`) per HLT leg.
- `<leg>_<ref>_vs_<target>_HLT_eff_<region>.{png,pdf}`: one per HLT leg per
  region (`barrel_pt`, `endcap_loweta_pt`, `endcap_higheta_pt`,
  `combined_pt`, `eta`, `phi`).

`<leg>` is one of `Ele30`, `Ele32`, `Ele115`, `Ele135`, `Ele23Ele12Leg1`,
`Ele23Ele12Leg2`, `DoubleEle33SeededLeg`, `DoubleEle33UnseededLeg`.

---

*Also included in this repo: `plot_NGT_Studies_2025G_ROOT.py`, a PyROOT/RDataFrame alternative that reads the ntuples directly (no coffea/dask/egamma-tnp) and writes the same efficiency-ratio plots as a CLI script. Kept for reference.*

Credits: [@saumyaphor4252](https://github.com/saumyaphor4252)
