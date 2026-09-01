# HLT Muons

## Dataset

The ROOT files used to produce these plots can be found in:

```text
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/NGT
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/HLT
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/Prompt
```

The script looks for files matching `*NGT.root`, `*HLT.root`, and
`*Prompt.root` in the directory from which it is run. Please copy or link the
input files there, or adjust the patterns in `eta_phi_diffs.py` accordingly.

## Requirements

Use the same Python environment described in the
[HLT Scouting Muons requirements](../HLTScoutingMuons/README.md#requirements).

## Plots and Scripts

| Plot | Python Script |
| :--- | :--- |
| <img src="plots/Eta_Phi_Diff_NGT_vs_HLT.png" width="100%" /> | `eta_phi_diffs.py` |
| <img src="plots/Eta_Phi_Diff_NGT_vs_Prompt.png" width="100%" /> | `eta_phi_diffs.py` |
