"""
Entry script: generic comparison of ALL 1D histograms (TH1*) in the
Scouting DQM files.

Unlike the other entry scripts (e.g. variables_ScoutingECALRecHits.py),
the histogram list is NOT hardcoded: the DQM directory tree below
`dqm_prefix` is walked at start-up and every TH1* found is turned into a
target.  Everything else (3-condition overlay + ratio panel, config.yaml,
PdfPages + PNG output) is inherited unchanged from ComparisonPlot1D.

Compared to the hand-tuned scripts, the per-plot cosmetics are generic:
  * x-label  : the ROOT x-axis title (ROOT '#eta' style converted to
               mathtext), falling back to the histogram name
  * y-label  : the ROOT y-axis title, falling back to "Entries"
  * y-scale  : log if max bin > 100 else linear + scientific ticks
               (same rule as invariantMass_ScoutingDielectron.py);
               forceable with --yscale
  * x-range  : full histogram range (base-class default)
  * output   : one multi-page PDF per top-level DQM folder
               (Comparison_All1D_<Folder>.pdf; --group-by subdir for one
               per sub-folder, --single-pdf for a single file); PNGs go
               to output.png_dir as usual, named
               Comparison_<sub_path>_<hist_name>.png so that identical
               histogram names in different folders do not collide.

Performance: with ~2500 histograms the framework's fetch-per-histogram
(re-opening every ROOT file each time) is far too slow, so this script
reads all selected histograms from each file in ONE pass up front
(`_preload`) and serves `fetch()` from that cache.  The remaining cost is
matplotlib rendering (~0.7 s per histogram); --jobs N renders the PDF
groups in parallel processes and --no-png skips the PNGs.

Histograms that are empty in every condition are skipped by default
(in a typical file more than half of them are); --keep-empty plots them
anyway.  Use --list to see what would be plotted without plotting.

Usage: see README.md in this folder, or `python3 all_1D_ScoutingDQM.py -h`.
"""

from luminosity import add_lumi_arguments, directory_run, load_lumi_info

import argparse
import multiprocessing
import os
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

import matplotlib
matplotlib.use("Agg")           # headless; required for --jobs > 1

import numpy as np
import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.mathtext import MathTextParser

from dqm_runs import DQMRunSelection, add_run_arguments

from scouting_plot import (ComparisonPlot1D, PDF_TITLE_FONTSIZE,
                           PDF_TITLE_PAD)


# ROOT TLatex symbol names understood by matplotlib mathtext.  Matched
# longest-first so that e.g. "#mum" becomes "\mu{}m" (as ROOT renders it)
# and "#DeltaN" becomes "\Delta{}N", instead of the invalid "\mum"/"\DeltaN".
_GREEK = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu "
          "nu xi omicron pi rho sigma tau upsilon phi chi psi omega").split()
_ROOT_SYMBOLS = (_GREEK + [g.capitalize() for g in _GREEK]
                 + ["varepsilon", "vartheta", "varphi", "varsigma",
                    "pm", "mp", "times", "cdot", "leq", "geq", "neq",
                    "approx", "equiv", "infty", "partial", "nabla",
                    "rightarrow", "leftarrow", "sqrt", "prime"])
_ROOT_SYMBOL_RE = re.compile(
    "#(" + "|".join(sorted(_ROOT_SYMBOLS, key=len, reverse=True)) + ")")


def scouting_input_dir(pipeline_cfg):
    """Read the shell config using the same working directory as the pipeline."""
    cfg = Path(pipeline_cfg).expanduser().resolve()
    if not cfg.is_file():
        raise ValueError(f"Pipeline config not found: {cfg}")
    result = subprocess.run(
        ["bash", "-c", 'set -e; source "$1" >&2; printf "%s" "${DQM_DEST_BASE:-}"',
         "bash", str(cfg)],
        cwd=cfg.parent, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"Error reading {cfg}: {result.stderr.strip()}")
    if not result.stdout.strip():
        raise ValueError(f"DQM_DEST_BASE is empty or unset in {cfg}")
    base = Path(result.stdout).expanduser()
    if not base.is_absolute():
        base = cfg.parent / base
    # Prefer separated scouting output; older pipelines wrote tags directly
    # under DQM_DEST_BASE. Also allows DQM_DEST_BASE to point at scouting itself.
    scouting = base / "scouting"
    return scouting if scouting.is_dir() else base


class All1DPlot(ComparisonPlot1D):

    dimension = 1
    output_pdf = "Comparison_All1D.pdf"     # rewritten per group in run()

    def __init__(self, config_path="config.yaml", include=(), exclude=(),
                 group_by="top", single_pdf=False, yscale="auto",
                 keep_empty=False, limit=None, jobs=1, save_png=True,
                 pipeline_cfg=Path(__file__).resolve().parents[1] / "pipeline.cfg",
                 local=False, per_run=False, runs=(), exclude_runs=(), lumi_csv=None,
                 xlabel=None, ylabel=None, xlim=None, ylim=None, ratio_ylim=None):
        super().__init__(config_path=config_path)
        if lumi_csv is not None:
            self.config["lumi_csv"] = lumi_csv
        # Local mode must not read or source pipeline.cfg at all.
        input_dir = Path.cwd() if local else scouting_input_dir(pipeline_cfg)
        for cond in self.conditions:
            # Absolute paths in custom plotting configs remain explicit overrides.
            cond.path = str(input_dir / Path(cond.path).expanduser())
            if not Path(cond.path).is_dir():
                hint = ("Check condition paths in the plotting config "
                        "(relative to the current working directory in --local mode)."
                        if local else
                        f"Check DQM_DEST_BASE in {pipeline_cfg} and condition paths "
                        "in the plotting config.")
                raise ValueError(
                    f"DQM input directory not found for {cond.label}: {cond.path}. "
                    + hint)
        self.include = [re.compile(p) for p in include]
        self.exclude = [re.compile(p) for p in exclude]
        self.group_by = group_by
        self.single_pdf = single_pdf
        self.yscale = yscale
        self.xlabel = xlabel
        self.ylabel = ylabel
        for name, limits in (("xlim", xlim), ("ylim", ylim),
                             ("ratio-ylim", ratio_ylim)):
            if limits is not None and (len(limits) != 2 or
                    not all(np.isfinite(v) for v in limits) or
                    limits[0] >= limits[1]):
                raise ValueError(f"--{name} requires finite MIN < MAX")
        if ylim is not None and yscale == "log" and ylim[0] <= 0:
            raise ValueError("--ylim requires positive limits with --yscale log")
        self.xlim = xlim
        self.ylim = ylim
        self.ratio_ylim = ratio_ylim
        self.keep_empty = keep_empty
        self.limit = limit
        self.jobs = 1 if single_pdf else max(1, jobs)
        self.save_png = save_png
        self.run_selection = DQMRunSelection(
            {c.label: c.path for c in self.conditions}, self.source.dqm_prefix,
            per_run=per_run, runs=runs, exclude_runs=exclude_runs)
        self.per_run = self.run_selection.per_run
        self.include_runs = self.run_selection.include_runs
        self.exclude_runs = self.run_selection.exclude_runs
        self.active_run = None
        self._targets = None
        self._cache = {}        # (condition label, "sub/path/name") -> (values, edges)

    # ---- discovery ---------------------------------------------------

    def _dqm_root(self, file_handle, run=None):
        """Directory handle of DQMData/{Run XXXXXX}/{dqm_prefix}, or None
        (same resolution logic as HistogramSource._resolve_dir)."""
        if "DQMData" not in file_handle:
            return None
        run = self.active_run if run is None else run
        if run is not None:
            full_path = (f"DQMData/Run {run}/"
                         f"{self.source.dqm_prefix}")
            return file_handle[full_path] if full_path in file_handle else None
        run_folder = next(
            (k for k in file_handle["DQMData"].keys(recursive=False, cycle=False)
             if "Run " in k), None)
        if run_folder is None:
            return None
        full_path = f"DQMData/{run_folder}/{self.source.dqm_prefix}"
        return file_handle[full_path] if full_path in file_handle else None

    def runs(self):
        """Validate luminosity coverage once, before discovery or summation."""
        if not hasattr(self, "_lumi_selected_runs"):
            selected = self.run_selection.runs()
            lumi_csv = str(Path(self.config.get("lumi_csv", "lumi_data.csv")).resolve())
            _, recorded = load_lumi_info(lumi_csv)
            missing = [run for run in selected if run not in recorded]
            if missing:
                lines = ["!" * 78,
                         f"WARNING: DQM RUNS EXCLUDED FROM ALL FINAL {self.dimension}D PLOTS",
                         f"Missing recorded luminosity in {lumi_csv}"]
                for run in missing:
                    lines.append(f"  SKIPPING RUN {run} (all conditions):")
                    for label, files in self.run_selection._run_files[run].items():
                        for fname in files:
                            lines.append(f"    [{label}] {fname} [Run {run}]")
                lines.extend([
                    "These runs contribute NO histogram bins and NO luminosity.",
                    "For multi-run files, only the listed run directories are excluded.",
                    "!" * 78])
                print("\n".join(lines), file=sys.stderr, flush=True)
            allowed = [run for run in selected if run in recorded]
            if not allowed:
                raise ValueError("No DQM runs remain with recorded luminosity; "
                                 f"no {self.dimension}D plots will be generated. Update the luminosity CSV.")
            # A comparison needs the same run inventory in every condition.
            # The inventory contains only readable files with the configured
            # DQM directory, not merely filenames that happen to exist.
            incomplete = {
                run: [c.label for c in self.conditions
                      if not self.run_selection._run_files[run].get(c.label)]
                for run in allowed}
            incomplete = {run: labels for run, labels in incomplete.items() if labels}
            if incomplete:
                lines = ["!" * 78,
                         f"WARNING: INCOMPLETE DQM RUNS EXCLUDED FROM ALL FINAL {self.dimension}D PLOTS"]
                for run, labels in incomplete.items():
                    lines.append(f"  SKIPPING RUN {run}: missing readable DQM for {', '.join(labels)}")
                    for label, files in self.run_selection._run_files[run].items():
                        for fname in files:
                            lines.append(f"    EXCLUDING [{label}] {fname} [Run {run}]")
                lines.extend(["The entire run is excluded from every condition and luminosity total.",
                              "!" * 78])
                print("\n".join(lines), file=sys.stderr, flush=True)
                allowed = [run for run in allowed if run not in incomplete]
            if not allowed:
                raise ValueError("No common DQM runs remain across all configured conditions; "
                                 f"no {self.dimension}D plots will be generated.")
            self._lumi_selected_runs = allowed
        return self._lumi_selected_runs

    def _select_run(self, run):
        self.active_run = run
        self.run_selection.active_run = run
        self._targets = None
        self._cache = {}
        missing = [c.label for c in self.conditions
                   if not self.run_selection._run_files[run].get(c.label)]
        print(f"=== Run {run} ===")
        if missing:
            print(f"   [Warning] Run {run}: no files for {', '.join(missing)}")

    def _file_runs(self, cond, representative=False):
        # Always resolve actual ROOT run directories, including in summed mode.
        # Discovery and aggregation must use exactly the same accepted runs.
        allowed = self.runs()
        selected = allowed if self.active_run is None else [self.active_run]
        for run in selected:
            if run not in allowed:
                continue
            files = self.run_selection._run_files[run].get(cond.label, [])
            for fname in files[:1] if representative else files:
                yield fname, run

    def _first_files(self):
        """One representative *.root file per condition, reference
        first, so the discovered set is the union over all conditions."""
        ordered = [self.reference] + [c for c in self.conditions
                                      if c is not self.reference]
        for cond in ordered:
            for fname, run in self._file_runs(cond, representative=True):
                yield cond, fname, run

    def _selected(self, full_name):
        if self.include and not any(p.search(full_name) for p in self.include):
            return False
        if any(p.search(full_name) for p in self.exclude):
            return False
        return True

    @classmethod
    def _histogram_keys(cls, root_dir):
        """Keys of TH1* (or TH2* in the 2D subclass); exclude profiles."""
        return [key for key, classname in root_dir.iterclassnames(recursive=True,
                                                            cycle=False)
                if classname.startswith(f"TH{cls.dimension}")]

    def targets(self):
        """Walk the DQM tree of one file per condition and collect every
        selected TH1*, with its axis titles."""
        if self._targets is not None:
            return self._targets

        found = {}
        for cond, fname, run in self._first_files():
            try:
                with uproot.open(fname) as f:
                    root = self._dqm_root(f, run)
                    if root is None:
                        print(f"   [Warning] DQM path not found in {fname}")
                        continue
                    for key in self._histogram_keys(root):
                        if key in found or not self._selected(key):
                            continue
                        subpath, _, hist_name = key.rpartition("/")
                        h = root[key]
                        found[key] = {
                            "subpath": subpath,
                            "hist_name": hist_name,
                            "xtitle": h.member("fXaxis").member("fTitle").strip(),
                            "ytitle": h.member("fYaxis").member("fTitle").strip(),
                        }
            except Exception as e:
                print(f"   [Warning] Error walking {fname}: {e}")

        targets = sorted(found.values(),
                         key=lambda t: (t["subpath"], t["hist_name"]))
        if self.limit is not None:
            targets = targets[:self.limit]
        self._targets = targets
        return targets

    # ---- data access -------------------------------------------------

    def _preload(self, targets):
        """
        Read every selected histogram from every file in ONE pass per
        file and sum over files per condition (same rules as
        HistogramSource.fetch_summed: first hit initialises the sum as
        float, later ones are added only if the shapes match).
        Replaces the per-histogram file re-opening of the base class,
        which for ~2500 histograms x N files is the dominant cost.
        """
        self.source.contributing_runs.clear()
        wanted = [self._full_name(t) for t in targets]
        t0 = time.time()
        n_files = 0
        for cond in self.conditions:
            for fname, run in self._file_runs(cond):
                try:
                    with uproot.open(fname) as f:
                        root = self._dqm_root(f, run)
                        if root is None:
                            print(f"   [Warning] DQM path not found in "
                                  f"{fname}; file skipped")
                            continue
                        present = set(self._histogram_keys(root))
                        for key in wanted:
                            if key not in present:
                                continue
                            values, *edges = root[key].to_numpy()
                            entry = self._cache.get((cond.label, key))
                            if entry is None:
                                self._cache[(cond.label, key)] = [
                                    np.array(values, dtype=float), *edges]
                            elif (values.shape == entry[0].shape and
                                  (self.dimension == 1 or all(
                                      np.array_equal(a, b)
                                      for a, b in zip(edges, entry[1:])))):
                                entry[0] += values
                            else:
                                print(f"   [Warning] Binning mismatch for "
                                      f"'{key}' in {fname}: {values.shape} "
                                      f"vs {entry[0].shape}; file skipped "
                                      f"for this histogram")
                                continue
                            subpath, _, hist_name = key.rpartition("/")
                            self.source.contributing_runs.setdefault(
                                (cond.label, subpath, hist_name), set()).add(directory_run(root))
                    n_files += 1
                except Exception as e:
                    print(f"   [Warning] Error reading {fname}: {e}")
        print(f"Loaded {len(wanted)} histograms from {n_files} file(s) "
              f"in {time.time() - t0:.1f} s")

    def fetch(self, target):
        """Served from the preloaded cache; same return shape as
        ComparisonPlot1D.fetch (None placeholders for missing
        conditions, None overall if nothing / nothing non-empty)."""
        key = self._full_name(target)
        fetched = []
        for cond in self.conditions:
            entry = self._cache.get((cond.label, key))
            data = None if entry is None else tuple(entry)
            fetched.append({"condition": cond, "data": self.transform(data)})
        if all(item["data"] is None for item in fetched):
            print("   [Warning] Not found in any condition -> skipped")
            return None
        if not self.keep_empty and all(
                item["data"] is None or np.sum(item["data"][0]) == 0
                for item in fetched):
            print("   [Info] Empty in all conditions -> skipped "
                  "(use --keep-empty to plot anyway)")
            return None
        return fetched

    # ---- cosmetics ---------------------------------------------------

    def apply_yscale(self, ax_main, max_y, target):
        if self.ylim is not None and self.ylim[0] <= 0 and self.yscale == "auto":
            self._sci_notation(ax_main)
            return
        if self.yscale == "log" or (self.yscale == "auto" and max_y > 100):
            ax_main.set_yscale("log")
        else:
            self._sci_notation(ax_main)

    def decorate(self, ax_main, ax_ratio, target):
        if self.xlim is not None:
            ax_main.set_xlim(*self.xlim)
            ax_ratio.set_xlim(*self.xlim)
        if self.ylim is not None:
            ax_main.set_ylim(*self.ylim)
        if self.ratio_ylim is not None:
            ax_ratio.set_ylim(*self.ratio_ylim)
        if self.active_run is not None:
            ax_main.text(0.02, 0.04, f"Run {self.active_run}",
                         transform=ax_main.transAxes, fontsize=16)
        ax_main.set_ylabel(self.ylabel if self.ylabel is not None else
                           self._label(target["ytitle"], "Entries"),
                           fontsize=20)
        ax_ratio.set_xlabel(self.xlabel if self.xlabel is not None else
                            self._label(target["xtitle"], target["hist_name"]),
                            fontsize=20)

    @staticmethod
    def _label(root_title, fallback):
        """ROOT axis title -> matplotlib label.

        1. tokens containing ROOT markup ('#eta', 'p_{T}', 'E^{2}') are
           converted to mathtext, plain words stay upright text;
        2. if that does not parse (e.g. a '_{...}' group containing a
           space), the whole title is put into one mathtext expression;
        3. if that fails too, the title is used as plain text.
        """
        if not root_title:
            return fallback
        parser = MathTextParser("agg")

        def parses(s):
            try:
                parser.parse(s)
                return True
            except Exception:
                return False

        def symbol(m):
            # terminate the command only if a letter/digit follows, so
            # that "#mum" -> "\mu{}m" while "#chi^{2}" -> "\chi^{2}"
            nxt = m.string[m.end():m.end() + 1]
            return "\\" + m.group(1) + ("{}" if nxt.isalnum() else "")

        conv = _ROOT_SYMBOL_RE.sub(symbol, root_title)
        tokens = [f"${t}$" if re.search(r"\\|_\{|\^\{", t) else t
                  for t in conv.split()]
        label = " ".join(tokens)
        if parses(label):
            return label
        label = "$" + conv.replace(" ", r"\ ") + "$"
        if parses(label):
            return label
        return root_title.replace("$", "")

    def _full_name(self, target):
        return f"{target['subpath']}/{target['hist_name']}"

    def pdf_title(self, target):
        prefix = "" if self.active_run is None else f"Run {self.active_run}: "
        return prefix + self._full_name(target)

    def png_name(self, target):
        run = "" if self.active_run is None else f"Run{self.active_run}_"
        return f"Comparison_{run}{self._full_name(target).replace('/', '_')}.png"

    def _group(self, target):
        if self.single_pdf:
            return "All"
        if self.group_by == "subdir":
            return target["subpath"].replace("/", "_")
        return target["subpath"].split("/")[0]

    def _pdf_name(self, group):
        run = "" if self.active_run is None else f"_Run{self.active_run}"
        return (f"Comparison_All{self.dimension}D{run}.pdf" if self.single_pdf
                else f"Comparison_All{self.dimension}D{run}_{group}.pdf")

    # ---- saving ------------------------------------------------------

    def _save(self, out, pdf_pages):
        """As ScoutingPlot._save, but the PNG (and its second render)
        can be skipped with --no-png."""
        if self.save_png:
            return super()._save(out, pdf_pages)
        out.fig.axes[0].set_title(out.pdf_title, fontsize=PDF_TITLE_FONTSIZE,
                                  pad=PDF_TITLE_PAD)
        pdf_pages.savefig(out.fig, bbox_inches="tight")
        plt.close(out.fig)

    # ---- lifecycle ---------------------------------------------------

    def _run_group(self, group, tgts):
        """One PdfPages for one group; returns (n_plotted, n_skipped)."""
        self.output_pdf = self._pdf_name(group)
        n_plotted = n_skipped = n_pages = 0
        try:
            print(f"--- Starting analysis for {self.output_pdf} "
                  f"({len(tgts)} histograms) ---")
            with PdfPages(self.output_pdf) as pdf:
                for target in tgts:
                    print(f" > Processing {self._full_name(target)}...")
                    fetched = self.fetch(target)
                    if fetched is None:
                        n_skipped += 1
                        continue
                    pages_before = n_pages
                    for out in self.make_figures(target, fetched):
                        self._save(out, pdf)
                        n_pages += 1
                    if n_pages > pages_before:
                        n_plotted += 1
                    else:
                        n_skipped += 1
            if n_plotted:
                print(f"SUCCESS: Analysis complete. Output: "
                      f"{self.output_pdf} ({n_pages} pages)")
            else:
                # matplotlib >= 3.10 does not write an empty PdfPages
                print(f"[Warning] Nothing to plot for {group}; "
                      f"{self.output_pdf} not written")
        except Exception as e:
            print(f"CRITICAL ERROR in {self.output_pdf}: {e}")
            traceback.print_exc()
        return n_plotted, n_skipped

    def run(self):
        if self.per_run:
            runs = self.runs()
            if not runs:
                raise ValueError("No DQM runs found (check inputs and dqm_prefix)")
            for run in runs:
                self._select_run(run)
                self._run_selected()
        else:
            if self.include_runs or self.exclude_runs:
                print("Summing runs: " + ", ".join(map(str, self.runs())))
            self._run_selected()

    def _run_selected(self):
        """Discover -> preload all data -> render each group (optionally
        in parallel processes) -> summary."""
        t0 = time.time()
        targets = self.targets()
        if not targets:
            print(f"CRITICAL ERROR: no {self.dimension}D histograms found "
                  "(check condition paths, dqm_prefix and --include)")
            return
        print(f"Discovered {len(targets)} {self.dimension}D histograms")
        self._preload(targets)

        groups = {}
        for t in targets:
            groups.setdefault(self._group(t), []).append(t)
        # largest groups first for better load balancing across workers
        items = sorted(groups.items(), key=lambda kv: -len(kv[1]))

        n_jobs = min(self.jobs, len(items))
        if n_jobs > 1:
            print(f"Rendering {len(items)} PDF groups with {n_jobs} processes")
            global _WORKER_PLOTTER
            _WORKER_PLOTTER = self          # inherited by forked workers
            with multiprocessing.get_context("fork").Pool(n_jobs) as pool:
                results = pool.starmap(_run_group_in_worker, items)
        else:
            results = [self._run_group(g, tgts) for g, tgts in items]

        n_plotted = sum(r[0] for r in results)
        n_skipped = sum(r[1] for r in results)
        print(f"Summary: {n_plotted} plotted, {n_skipped} skipped "
              f"(empty or missing), {len(items)} PDF group(s), "
              f"{time.time() - t0:.0f} s")


# Set in run() before forking; the workers inherit the fully loaded
# plotter (targets + histogram cache) without pickling anything.
_WORKER_PLOTTER = None


def _run_group_in_worker(group, tgts):
    return _WORKER_PLOTTER._run_group(group, tgts)


def _parse_args(dimension=1):
    p = argparse.ArgumentParser(
        description=f"Compare ALL {dimension}D histograms of the Scouting DQM files "
                    "across the conditions in config.yaml.")
    p.add_argument("--config", default="config.yaml",
                   help="path to config.yaml (default: %(default)s)")
    p.add_argument("--pipeline-cfg",
                   default=str(Path(__file__).resolve().parents[1] / "pipeline.cfg"),
                   help="pipeline.cfg defining DQM_DEST_BASE "
                        "(default: pipeline.cfg next to the pipeline scripts; "
                        "ignored with --local)")
    p.add_argument("--local", action="store_true",
                   help="ignore pipeline.cfg and use condition paths from config.yaml "
                        "relative to the current working directory")
    p.add_argument("--include", action="append", default=[], metavar="REGEX",
                   help="only histograms whose 'subpath/name' matches "
                        "(repeatable, OR-ed)")
    p.add_argument("--exclude", action="append", default=[], metavar="REGEX",
                   help="drop histograms whose 'subpath/name' matches "
                        "(repeatable)")
    p.add_argument("--list", action="store_true",
                   help="print the selected histograms and exit")
    add_run_arguments(p)
    add_lumi_arguments(p, default=None)
    p.add_argument("--group-by", choices=["top", "subdir"], default="top",
                   help="one PDF per top-level DQM folder (default) or per "
                        "sub-folder (smaller PDFs, better parallelism)")
    p.add_argument("--single-pdf", action="store_true",
                   help=f"one Comparison_All{dimension}D.pdf for everything "
                        "(implies --jobs 1)")
    if dimension == 1:
        for option, description in (
                ("--xlim", "shared x-axis limits for main and ratio panels"),
                ("--ylim", "main-panel y-axis limits; nonpositive MIN makes auto scale linear"),
                ("--ratio-ylim", "ratio-panel y-axis limits (default: 0 2)")):
            p.add_argument(option, nargs=2, type=float, metavar=("MIN", "MAX"),
                           help=description)
        p.add_argument("--xlabel", default=None, metavar="TEXT",
                       help="override the x-axis label on every selected plot "
                            "(plain text or matplotlib mathtext)")
        p.add_argument("--ylabel", default=None, metavar="TEXT",
                       help="override the main-panel y-axis label on every selected "
                            "plot (plain text or matplotlib mathtext)")
        p.add_argument("--yscale", choices=["auto", "log", "linear"],
                       default="auto", help="main-panel y-scale (default: "
                                            "log if max bin > 100 else linear)")
    else:
        p.set_defaults(yscale="auto")
        p.add_argument("--xlabel", help="override the map x-axis and x-projection label")
        p.add_argument("--ylabel", help="override the map y-axis and y-projection label")
        for option in ("--xlim", "--ylim", "--radial-xlim"):
            p.add_argument(option, nargs=2, type=float, metavar=("MIN", "MAX"),
                           help="display limits (do not change aggregation)")
        p.add_argument("--pair", nargs=2, action="append", metavar=("A", "B"),
                       help="compare A - B and (A - B) / B; repeatable, default: all three pairs")
        p.add_argument("--pdf-name", help="custom combined PDF filename (implies --single-pdf)")
        p.add_argument("--cbar-label", help="override colorbar label (literal text/mathtext)")
        p.add_argument("--aspect", choices=["auto", "equal"], default="auto")
        p.add_argument("--projection", choices=["xy", "radial"], default="xy")
        p.add_argument("--radial-center", nargs=2, type=float, default=(0., 0.),
                       metavar=("X", "Y"), help="radial origin in histogram coordinates")
        p.add_argument("--radial-bin-width", type=float,
                       help="radial bin width (default: minimum x-bin width)")
        p.add_argument("--difference", choices=["both", "absolute", "relative"],
                       default="both", help="difference maps to render (default: both)")
        p.add_argument("--z-limit", type=float, default=None,
                       help="symmetric color range [-N, N] for the selected difference(s); "
                            "default: automatic per map")
        # Retain historical per-kind options for existing command lines.
        p.add_argument("--abs-z-limit", type=float, default=None, help=argparse.SUPPRESS)
        p.add_argument("--rel-z-limit", type=float, default=None, help=argparse.SUPPRESS)
    p.add_argument("--keep-empty", action="store_true",
                   help="also plot histograms that are empty in every "
                        "condition")
    p.add_argument("--limit", type=int, default=None, metavar="N",
                   help="only the first N selected histograms (quick tests)")
    p.add_argument("--jobs", "-j", type=int, default=os.cpu_count() or 1,
                   metavar="N", help="render PDF groups in N parallel "
                                     "processes (default: all cores)")
    p.add_argument("--no-png", action="store_true",
                   help="write only the PDFs, skip the per-histogram PNGs")
    return p.parse_args()


def main(plot_class=All1DPlot):
    args = _parse_args(plot_class.dimension)
    options = (dict(xlabel=args.xlabel, ylabel=args.ylabel, xlim=args.xlim,
                    ylim=args.ylim, ratio_ylim=args.ratio_ylim)
               if plot_class.dimension == 1 else
               dict(difference=args.difference, z_limit=args.z_limit, abs_z_limit=args.abs_z_limit,
                    rel_z_limit=args.rel_z_limit, xlabel=args.xlabel, ylabel=args.ylabel,
                    xlim=args.xlim, ylim=args.ylim, pairs=args.pair,
                    cbar_label=args.cbar_label, aspect=args.aspect, pdf_name=args.pdf_name,
                    projection=args.projection, radial_center=args.radial_center,
                    radial_bin_width=args.radial_bin_width, radial_xlim=args.radial_xlim))
    try:
        plot = plot_class(**options, config_path=args.config, include=args.include,
                     exclude=args.exclude, group_by=args.group_by,
                     single_pdf=args.single_pdf, yscale=args.yscale,
                     keep_empty=args.keep_empty, limit=args.limit,
                     jobs=args.jobs, save_png=not args.no_png,
                     pipeline_cfg=args.pipeline_cfg, local=args.local,
                     per_run=args.per_run, runs=args.runs,
                     exclude_runs=args.exclude_runs, lumi_csv=args.lumi_csv)
        if args.list:
            if not plot.per_run and (plot.include_runs or plot.exclude_runs):
                print("Summing runs: " + ", ".join(map(str, plot.runs())))
            runs = plot.runs() if args.per_run else [None]
            if not runs:
                raise ValueError("No DQM runs found (check inputs and dqm_prefix)")
            for run in runs:
                if run is not None:
                    plot._select_run(run)
                for t in plot.targets():
                    print(f"{t['subpath']}/{t['hist_name']}")
                print(f"{len(plot.targets())} histograms selected")
        else:
            plot.run()
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc


if __name__ == "__main__":
    main()
