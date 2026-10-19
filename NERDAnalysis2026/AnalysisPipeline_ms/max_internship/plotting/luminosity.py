"""Shared run-level recorded luminosity and CMS labels for all plotters.

Inputs must represent full runs. Partial lumisection coverage needs a
lumisection-level luminosity calculation instead.
"""
import csv
import math
import re
from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=None)
def load_lumi_info(lumi_csv):
    """Read one-row-per-run brilcalc CSV in /pb; reject ambiguous metadata."""
    run_fill, run_lumi = {}, {}
    with open(lumi_csv, newline="") as stream:
        lines = stream.readlines()
    header = next((line for line in lines if line.startswith("#run:fill,")), "")
    if "recorded(/pb)" not in header:
        raise ValueError(f"{lumi_csv}: expected brilcalc recorded(/pb) column")
    for row in csv.reader(line for line in lines
                          if line.strip() and not line.startswith("#")):
        if ":" not in row[0]:
            continue
        run, fill = map(int, row[0].split(":"))
        value = float(row[5])
        if run in run_lumi:
            raise ValueError(f"{lumi_csv}: duplicate run {run}; use run-level CSV")
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{lumi_csv}: invalid luminosity for run {run}")
        run_fill[run], run_lumi[run] = fill, value
    return run_fill, run_lumi


def directory_run(directory):
    """Read the run from the actual uproot directory used for aggregation."""
    match = re.search(r"(?:^|/)Run (\d+)(?:/|$)", directory.object_path)
    if not match:
        raise ValueError(f"Cannot identify DQM run: {directory.object_path}")
    return int(match.group(1))


def luminosity_fb(runs, lumi_csv):
    """Sum unique contributing runs, never files or reconstruction conditions."""
    runs = set(runs)
    _, recorded = load_lumi_info(str(Path(lumi_csv).resolve()))
    missing = runs - recorded.keys()
    if missing:
        raise ValueError(f"{lumi_csv}: missing recorded luminosity for runs "
                         + ", ".join(map(str, sorted(missing))))
    if not runs:
        raise ValueError("Cannot label luminosity without contributing runs")
    return sum(recorded[run] for run in runs) / 1000.0


def cms_lumi_label(ax, runs_by_condition, lumi_csv, **kwargs):
    """Draw one common total, or explicit condition totals if run sets differ."""
    import mplhep as hep
    groups = {label: set(runs) for label, runs in runs_by_condition.items()}
    if not groups:
        raise ValueError("No contributing conditions for luminosity label")
    totals = {label: luminosity_fb(runs, lumi_csv) for label, runs in groups.items()}
    same = all(runs == next(iter(groups.values())) for runs in groups.values())
    unit = r"fb$^{-1}$"
    if same:
        text = f"{next(iter(totals.values())):.3g} {unit}"
    else:
        text = "; ".join(f"{label}: {total:.3g} {unit}" for label, total in totals.items())
    com = kwargs.pop("com", 13.6)
    kwargs.pop("lumi", None)
    year = kwargs.get("year")
    prefix = f"{year}, " if year else ""
    return hep.cms.label(ax=ax, lumi=None,
                         rlabel=f"{prefix}{text} ({com:g} TeV)", **kwargs)
