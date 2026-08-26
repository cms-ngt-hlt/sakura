#!/usr/bin/env python3
"""Cross-check Z->ee event counts in the DQM output files of each calibration tag.

For every run, reads the electrons_mass histogram and reports GetEntries against
the summed bin contents, the NGT/Prompt and HLT/Prompt yield ratios and per-tag
totals, then writes Zee_EventCounts_PerRun.png (entries vs. run number).

Usage: python3 sanitiy_check_event_counter.py
  No arguments. Expects HLT/, NGT/ and Prompt/ subfolders next to this script,
  each containing DQM files named ..._R<run>.root.
"""
import os
import re
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot

plt.style.use(hep.style.CMS)


def extract_run_number(filename):
    match = re.search(r'_R(\d+)\.root', filename)
    return int(match.group(1)) if match else None


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    sources = {
        'HLT': {'folder': 'HLT', 'color': '#5790fc', 'marker': 'o'},
        'NGT': {'folder': 'NGT', 'color': '#f89c20', 'marker': 'D'},
        'Prompt': {'folder': 'Prompt', 'color': 'black', 'marker': 'v'}
    }

    # run_number -> entries, for each tag
    entries_by_source = {label: {} for label in sources}
    # run_number -> sum(counts), for each tag (for manual comparison only)
    sums_by_source = {label: {} for label in sources}

    print("Loading data and counting events...")
    for label, info in sources.items():
        folder_path = os.path.join(base_dir, info['folder'])
        files = sorted([f for f in os.listdir(folder_path) if f.endswith(".root")])

        for item in files:
            run_num = extract_run_number(item)
            if not run_num:
                continue
            with uproot.open(os.path.join(folder_path, item)) as f:
                keys = [k for k in f.keys() if "electrons_mass" in k]
                if not keys:
                    continue
                h = f[keys[0]]
                n_entries = h.member("fEntries")
                n_sum = np.sum(h.values())

                entries_by_source[label][run_num] = n_entries
                sums_by_source[label][run_num] = n_sum

    # --- Manual comparison printout: GetEntries vs sum(counts), per tag per run ---
    print("\n=== GetEntries vs sum(counts) ===")
    for label in sources:
        print(f"\n-- {label} --")
        for run_num in sorted(entries_by_source[label]):
            n_entries = entries_by_source[label][run_num]
            n_sum = sums_by_source[label][run_num]
            print(f"  Run {run_num}: GetEntries={n_entries:.0f}, sum(counts)={n_sum:.0f}, diff={n_entries - n_sum:.0f}")

    # --- Factor between Prompt and NGT / HLT, per run ---
    print("\n=== Factor vs Prompt (GetEntries) ===")
    for run_num in sorted(entries_by_source['Prompt']):
        prompt_entries = entries_by_source['Prompt'][run_num]
        line = f"  Run {run_num}:"
        for label in ('NGT', 'HLT'):
            if run_num in entries_by_source[label] and prompt_entries > 0:
                factor = entries_by_source[label][run_num] / prompt_entries
                line += f" {label}/Prompt={factor:.2f}"
            else:
                line += f" {label}/Prompt=N/A"
        print(line)

    # --- Totals per tag ---
    print("\n=== Total events per Tag (sum of GetEntries over all runs) ===")
    for label in sources:
        total_entries = sum(entries_by_source[label].values())
        print(f"  {label}: {total_entries:.0f}")

    # --- Plot: GetEntries vs run number, one series per tag ---
    fig, ax = plt.subplots(figsize=(10, 7))
    hep.cms.label(ax=ax, data=True, text="Preliminary", year=2026, com=13.6, fontsize=22)

    for label, info in sources.items():
        runs = sorted(entries_by_source[label])
        counts = [entries_by_source[label][r] for r in runs]
        ax.plot(runs, counts, label=label, color=info['color'], marker=info['marker'],
                linestyle='none', markersize=10)

    ax.set_xlabel("Run number", fontsize=20)
    ax.set_ylabel("Number of Events (GetEntries)", fontsize=20)
    ax.legend(fontsize=18, loc='best')
    ax.grid(True, alpha=0.3)

    out_path = os.path.join(base_dir, "Zee_EventCounts_PerRun.png")
    fig.savefig(out_path, bbox_inches='tight')
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
