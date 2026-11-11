#!/usr/bin/env python3
"""Cross-check Z->ee event counts in the Scouting DQM files of each condition.

For every run, reads the DiLepton/electrons_mass histogram and reports
GetEntries against the summed bin contents, the yield ratio of every
condition to the reference, and per-condition totals, then writes
Zee_EventCounts_PerRun.png (entries vs. run number).

Conditions, the reference and the CMS label come from the plotting config;
inputs and the plot destination are found like for the other Scouting plots
(DQM_DEST_BASE/scouting and PLOTS_DEST from pipeline.cfg, or --local with
--output-dir).  Runs are read from
the DQMData/Run <run> folders, so multi-run files are handled too.

Usage: python3 sanity_check_event_counter.py [--local] [--output-dir DIR] ...
"""
import argparse
import glob
import os
import re
from pathlib import Path

import matplotlib.pyplot as plt
import mplhep as hep
import numpy as np
import uproot

from luminosity import cms_lumi_label
from plotting_functions import (add_common_arguments, cms_text, condition_styles,
                                load_config, lumi_csv_path, make_output_dir,
                                scouting_input_dir)

plt.style.use(hep.style.CMS)

HIST_SUBPATH = "DiLepton/electrons_mass"


def read_counts(folder, dqm_prefix):
    """{run: (GetEntries, sum of bin contents)} summed over all files."""
    entries, sums = {}, {}
    files = sorted(glob.glob(os.path.join(folder, "*.root")))
    if not files:
        print(f"  [Warning] No .root files found in {folder}")
    for fname in files:
        try:
            with uproot.open(fname) as f:
                if "DQMData" not in f:
                    continue
                for key in f["DQMData"].keys(recursive=False, cycle=False):
                    match = re.fullmatch(r"Run (\d+)", key)
                    path = f"DQMData/{key}/{dqm_prefix}/{HIST_SUBPATH}"
                    if not match or path not in f:
                        continue
                    run = int(match.group(1))
                    h = f[path]
                    entries[run] = entries.get(run, 0) + h.member("fEntries")
                    sums[run] = sums.get(run, 0) + np.sum(h.values())
        except Exception as exc:
            print(f"  [Warning] Error reading {fname}: {exc}")
    return entries, sums


def draw_label(ax, entries_by_source, config, lumi_csv):
    """CMS label with luminosity; without it if the CSV lacks some runs."""
    cl = config["cms_label"]
    runs = {label: set(e) for label, e in entries_by_source.items() if e}
    try:
        cms_lumi_label(ax, runs, lumi_csv, data=True, text=cms_text(config),
                       year=cl["year"], com=cl["com"], fontsize=22)
    except (ValueError, OSError) as exc:
        print(f"[Warning] No luminosity in the label: {exc}")
        hep.cms.label(ax=ax, data=True, text=cms_text(config), year=cl["year"],
                      com=cl["com"], fontsize=22)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_arguments(parser)
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        output_dir = make_output_dir(args.pipeline_cfg, args.local, args.output_dir)
        input_dir = scouting_input_dir(args.pipeline_cfg, local=args.local)
    except (ValueError, KeyError, OSError) as exc:
        parser.error(str(exc))
    sources = condition_styles(config)
    reference = config["reference"]

    entries_by_source, sums_by_source = {}, {}
    print("Loading data and counting events...")
    for label, info in sources.items():
        folder = input_dir / Path(info["folder"]).expanduser()
        entries_by_source[label], sums_by_source[label] = read_counts(
            str(folder), config["dqm_prefix"])

    # --- GetEntries vs sum(counts), per condition per run ---
    print("\n=== GetEntries vs sum(counts) ===")
    for label in sources:
        print(f"\n-- {label} --")
        for run in sorted(entries_by_source[label]):
            n_entries = entries_by_source[label][run]
            n_sum = sums_by_source[label][run]
            print(f"  Run {run}: GetEntries={n_entries:.0f}, "
                  f"sum(counts)={n_sum:.0f}, diff={n_entries - n_sum:.0f}")

    # --- Factor w.r.t. the reference, per run ---
    print(f"\n=== Factor vs {reference} (GetEntries) ===")
    ref_entries = entries_by_source.get(reference, {})
    for run in sorted(ref_entries):
        line = f"  Run {run}:"
        for label in sources:
            if label == reference:
                continue
            if run in entries_by_source[label] and ref_entries[run] > 0:
                line += f" {label}/{reference}={entries_by_source[label][run] / ref_entries[run]:.2f}"
            else:
                line += f" {label}/{reference}=N/A"
        print(line)

    # --- Totals per condition ---
    print("\n=== Total events per condition (sum of GetEntries over all runs) ===")
    for label in sources:
        print(f"  {label}: {sum(entries_by_source[label].values()):.0f}")

    if not any(entries_by_source.values()):
        print("\n[Warning] No electrons_mass histograms found; no plot written")
        return

    # --- Plot: GetEntries vs run number, one series per condition ---
    fig, ax = plt.subplots(figsize=(10, 7))
    draw_label(ax, entries_by_source, config,
               lumi_csv_path(config, args.lumi_csv))

    for label, info in sources.items():
        runs = sorted(entries_by_source[label])
        counts = [entries_by_source[label][r] for r in runs]
        ax.plot(runs, counts, label=label, color=info["color"],
                marker=info["marker"], linestyle="none", markersize=10)

    ax.set_xlabel("Run number", fontsize=20)
    ax.set_ylabel("Number of Events (GetEntries)", fontsize=20)
    ax.legend(fontsize=18, loc="best")
    ax.grid(True, alpha=0.3)

    out_path = os.path.join(output_dir, "Zee_EventCounts_PerRun.png")
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
