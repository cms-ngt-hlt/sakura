"""Run discovery and selection extracted from all_1D_ScoutingDQM.py.

The inventory is keyed by run, then condition. Histogram loading and plotting
remain in the callers. No PyROOT dependency is needed here.
"""
import glob
import os
import re
import uproot


def add_run_arguments(parser):
    parser.add_argument("--per-run", nargs="?", const=True, default=False,
                   type=int, metavar="RUN",
                   help="process conditions separately for all DQM runs, "
                        "or only RUN if supplied; "
                        "include run numbers in PDF and PNG filenames")
    parser.add_argument("--runs", nargs="+", type=int, default=[], metavar="RUN",
                   help="use only these runs (space-separated); sum them unless "
                        "--per-run is also set")
    parser.add_argument("--exclude-runs", nargs="+", type=int, default=[], metavar="RUN",
                   help="omit these runs (space-separated), also with --per-run; "
                        "exclusions take precedence over --runs")


class DQMRunSelection:
    def __init__(self, condition_paths, dqm_prefix, per_run=False,
                 runs=(), exclude_runs=()):
        self.condition_paths = condition_paths
        self.dqm_prefix = dqm_prefix
        # bool preserves the all-runs/default modes; an integer selects one run.
        self.per_run = per_run is not False
        self.requested_run = None if isinstance(per_run, bool) else per_run
        if self.requested_run is not None and self.requested_run <= 0:
            raise ValueError("--per-run RUN must be a positive run number")
        self.include_runs = set(runs)
        self.exclude_runs = set(exclude_runs)
        if any(run <= 0 for run in self.include_runs | self.exclude_runs):
            raise ValueError("--runs and --exclude-runs require positive run numbers")
        self.active_run = None
        self._run_files = None

    def _files(self, label):
        if self.active_run is not None:
            return self._run_files[self.active_run].get(label, [])
        files = sorted(glob.glob(os.path.join(self.condition_paths[label], "*.root")))
        if not files:
            print(f"   [Warning] No .root files found in {self.condition_paths[label]} "
                  f"({label})")
        return files

    def runs(self):
        """Index actual DQM run directories, including multi-run ROOT files."""
        if self._run_files is None:
            self._run_files = {}
            for label in self.condition_paths:
                for fname in self._files(label):
                    try:
                        with uproot.open(fname) as f:
                            keys = (f["DQMData"].keys(recursive=False, cycle=False)
                                    if "DQMData" in f else [])
                            matched = False
                            for key in keys:
                                match = re.fullmatch(r"Run (\d+)", key)
                                if match and (f"DQMData/{key}/"
                                              f"{self.dqm_prefix}") in f:
                                    run = int(match.group(1))
                                    self._run_files.setdefault(run, {}).setdefault(
                                        label, []).append(fname)
                                    matched = True
                            if not matched:
                                print(f"   [Warning] No matching DQM runs in {fname}")
                    except Exception as exc:
                        print(f"   [Warning] Error indexing {fname}: {exc}")
        available = sorted(self._run_files)
        requested = self.include_runs.copy()
        if self.requested_run is not None:
            requested.add(self.requested_run)
        missing = requested - set(available)
        if missing:
            choices = ", ".join(map(str, available)) or "none"
            raise ValueError(
                f"Requested runs not found: {', '.join(map(str, sorted(missing)))}. "
                f"Available runs: {choices}")
        selected = set(available)
        if self.include_runs:
            selected &= self.include_runs
        if self.requested_run is not None:
            selected &= {self.requested_run}
        selected -= self.exclude_runs
        if not selected:
            raise ValueError("No DQM runs remain after run selection "
                             "(check inputs, dqm_prefix and run filters)")
        return sorted(selected)

    def file_runs(self, label, representative=False):
        """Yield file/run pairs, restricting ROOT directories as well as files."""
        if self.active_run is not None:
            runs = [self.active_run]
        elif self.include_runs or self.exclude_runs:
            runs = self.runs()
        else:
            files = self._files(label)
            for fname in files[:1] if representative else files:
                yield fname, None
            return
        for run in runs:
            files = self._run_files[run].get(label, [])
            for fname in files[:1] if representative else files:
                yield fname, run

