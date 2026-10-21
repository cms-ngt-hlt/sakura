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
    columns = next(csv.reader([header.lstrip("#").strip()]))
    run_column = columns.index("run:fill")
    recorded_column = columns.index("recorded(/pb)")
    for row in csv.reader(line for line in lines
                          if line.strip() and not line.startswith("#")):
        if ":" not in row[run_column]:
            continue
        run, fill = map(int, row[run_column].split(":"))
        value = float(row[recorded_column])
        if run in run_lumi:
            raise ValueError(f"{lumi_csv}: duplicate run {run}; use run-level CSV")
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{lumi_csv}: invalid luminosity for run {run}")
        run_fill[run], run_lumi[run] = fill, value
    return run_fill, run_lumi


def add_lumi_arguments(parser, default="lumi_data.csv"):
    """Shared CLI; use default=None to defer to a plotter's configuration."""
    parser.add_argument(
        "--lumi-csv", default=default,
        help="run-level brilcalc CSV in /pb, relative to the current directory "
             + ("(default: %(default)s)" if default else "(default: lumi_csv in config.yaml)"))


def cumulative_luminosity(runs, lumi_csv, *, per_run=False, selected_runs=None):
    """Return group membership and cumulative ranges for runs or fills.

    The axis retains all CSV runs between the first and last input run.
    selected_runs restricts group membership, not the elapsed luminosity axis.
    Ranges (start, end, x midpoint) are in /fb; group lumi is in /pb.
    Empty input returns empty mappings. Labels should separately use only
    contributing runs through luminosity_fb/cms_lumi_label.
    """
    runs = set(runs)
    if not runs:
        return {}, {}
    luminosity_fb(runs, lumi_csv)  # Validate coverage before building the axis.
    run_fill, recorded = load_lumi_info(str(Path(lumi_csv).resolve()))
    selected = None if selected_runs is None else set(selected_runs)
    first, last = min(runs), max(runs)
    groups, ranges = {}, {}
    current = 0.0
    for run in sorted(r for r in recorded if first <= r <= last):
        start = current
        current += recorded[run]
        if selected is not None and run not in selected:
            continue
        group = run if per_run else run_fill[run]
        groups.setdefault(group, []).append(run)
        info = ranges.setdefault(group, {"start": start / 1000.0, "lumi": 0.0})
        info["end"] = current / 1000.0
        info["x"] = (info["start"] + info["end"]) / 2.0
        info["lumi"] += recorded[run]
    return groups, ranges


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
    suffix = f", {year}" if year else ""
    return hep.cms.label(ax=ax, lumi=None,
                         rlabel=f"{text}{suffix} ({com:g} TeV)", **kwargs)
