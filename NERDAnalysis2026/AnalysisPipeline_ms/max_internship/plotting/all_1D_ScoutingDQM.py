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

Usage: see README_all_1D_ScoutingDQM.md, or `python3 all_1D_ScoutingDQM.py -h`.
"""

import argparse
import glob
import multiprocessing
import os
import re
import time
import traceback

import matplotlib
matplotlib.use("Agg")           # headless; required for --jobs > 1

import numpy as np
import uproot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.mathtext import MathTextParser

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


class All1DPlot(ComparisonPlot1D):

    output_pdf = "Comparison_All1D.pdf"     # rewritten per group in run()

    def __init__(self, config_path="config.yaml", include=(), exclude=(),
                 group_by="top", single_pdf=False, yscale="auto",
                 keep_empty=False, limit=None, jobs=1, save_png=True):
        super().__init__(config_path=config_path)
        self.include = [re.compile(p) for p in include]
        self.exclude = [re.compile(p) for p in exclude]
        self.group_by = group_by
        self.single_pdf = single_pdf
        self.yscale = yscale
        self.keep_empty = keep_empty
        self.limit = limit
        self.jobs = 1 if single_pdf else max(1, jobs)
        self.save_png = save_png
        self._targets = None
        self._cache = {}        # (condition label, "sub/path/name") -> (values, edges)

    # ---- discovery ---------------------------------------------------

    def _dqm_root(self, file_handle):
        """Directory handle of DQMData/{Run XXXXXX}/{dqm_prefix}, or None
        (same resolution logic as HistogramSource._resolve_dir)."""
        if "DQMData" not in file_handle:
            return None
        run_folder = next(
            (k for k in file_handle["DQMData"].keys(recursive=False, cycle=False)
             if "Run " in k), None)
        if run_folder is None:
            return None
        full_path = f"DQMData/{run_folder}/{self.source.dqm_prefix}"
        return file_handle[full_path] if full_path in file_handle else None

    def _files(self, cond):
        files = sorted(glob.glob(os.path.join(cond.path, "*.root")))
        if not files:
            print(f"   [Warning] No .root files found in {cond.path} "
                  f"({cond.label})")
        return files

    def _first_files(self):
        """One representative *.root file per condition, reference
        first, so the discovered set is the union over all conditions."""
        ordered = [self.reference] + [c for c in self.conditions
                                      if c is not self.reference]
        for cond in ordered:
            files = self._files(cond)
            if files:
                yield cond, files[0]

    def _selected(self, full_name):
        if self.include and not any(p.search(full_name) for p in self.include):
            return False
        if any(p.search(full_name) for p in self.exclude):
            return False
        return True

    @staticmethod
    def _th1_keys(root_dir):
        """'sub/path/name' of every TH1* below `root_dir` (TProfiles and
        TH2s are not 1D histograms and are skipped)."""
        return [key for key, cls in root_dir.iterclassnames(recursive=True,
                                                            cycle=False)
                if cls.startswith("TH1")]

    def targets(self):
        """Walk the DQM tree of one file per condition and collect every
        selected TH1*, with its axis titles."""
        if self._targets is not None:
            return self._targets

        found = {}
        for cond, fname in self._first_files():
            try:
                with uproot.open(fname) as f:
                    root = self._dqm_root(f)
                    if root is None:
                        print(f"   [Warning] DQM path not found in {fname}")
                        continue
                    for key in self._th1_keys(root):
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
        wanted = [self._full_name(t) for t in targets]
        t0 = time.time()
        n_files = 0
        for cond in self.conditions:
            for fname in self._files(cond):
                try:
                    with uproot.open(fname) as f:
                        root = self._dqm_root(f)
                        if root is None:
                            print(f"   [Warning] DQM path not found in "
                                  f"{fname}; file skipped")
                            continue
                        present = set(self._th1_keys(root))
                        for key in wanted:
                            if key not in present:
                                continue
                            values, edges = root[key].to_numpy()
                            entry = self._cache.get((cond.label, key))
                            if entry is None:
                                self._cache[(cond.label, key)] = [
                                    np.array(values, dtype=float), edges]
                            elif values.shape == entry[0].shape:
                                entry[0] += values
                            else:
                                print(f"   [Warning] Shape mismatch for "
                                      f"'{key}' in {fname}: {values.shape} "
                                      f"vs {entry[0].shape}; file skipped "
                                      f"for this histogram")
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
            data = None if entry is None else (entry[0], entry[1])
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
        if self.yscale == "log" or (self.yscale == "auto" and max_y > 100):
            ax_main.set_yscale("log")
        else:
            self._sci_notation(ax_main)

    def decorate(self, ax_main, ax_ratio, target):
        ax_main.set_ylabel(self._label(target["ytitle"], "Entries"),
                           fontsize=20)
        ax_ratio.set_xlabel(self._label(target["xtitle"], target["hist_name"]),
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
        return self._full_name(target)

    def png_name(self, target):
        return f"Comparison_{self._full_name(target).replace('/', '_')}.png"

    def _group(self, target):
        if self.single_pdf:
            return "All"
        if self.group_by == "subdir":
            return target["subpath"].replace("/", "_")
        return target["subpath"].split("/")[0]

    def _pdf_name(self, group):
        return ("Comparison_All1D.pdf" if self.single_pdf
                else f"Comparison_All1D_{group}.pdf")

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
        n_plotted = n_skipped = 0
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
                    for out in self.make_figures(target, fetched):
                        self._save(out, pdf)
                    n_plotted += 1
            if n_plotted:
                print(f"SUCCESS: Analysis complete. Output: "
                      f"{self.output_pdf} ({n_plotted} pages)")
            else:
                # matplotlib >= 3.10 does not write an empty PdfPages
                print(f"[Warning] Nothing to plot for {group}; "
                      f"{self.output_pdf} not written")
        except Exception as e:
            print(f"CRITICAL ERROR in {self.output_pdf}: {e}")
            traceback.print_exc()
        return n_plotted, n_skipped

    def run(self):
        """Discover -> preload all data -> render each group (optionally
        in parallel processes) -> summary."""
        t0 = time.time()
        targets = self.targets()
        if not targets:
            print("CRITICAL ERROR: no 1D histograms found "
                  "(check condition paths, dqm_prefix and --include)")
            return
        print(f"Discovered {len(targets)} 1D histograms")
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


def _parse_args():
    p = argparse.ArgumentParser(
        description="Compare ALL 1D histograms of the Scouting DQM files "
                    "across the conditions in config.yaml.")
    p.add_argument("--config", default="config.yaml",
                   help="path to config.yaml (default: %(default)s)")
    p.add_argument("--include", action="append", default=[], metavar="REGEX",
                   help="only histograms whose 'subpath/name' matches "
                        "(repeatable, OR-ed)")
    p.add_argument("--exclude", action="append", default=[], metavar="REGEX",
                   help="drop histograms whose 'subpath/name' matches "
                        "(repeatable)")
    p.add_argument("--list", action="store_true",
                   help="print the selected histograms and exit")
    p.add_argument("--group-by", choices=["top", "subdir"], default="top",
                   help="one PDF per top-level DQM folder (default) or per "
                        "sub-folder (smaller PDFs, better parallelism)")
    p.add_argument("--single-pdf", action="store_true",
                   help="one Comparison_All1D.pdf for everything "
                        "(implies --jobs 1)")
    p.add_argument("--yscale", choices=["auto", "log", "linear"],
                   default="auto", help="main-panel y-scale (default: "
                                        "log if max bin > 100 else linear)")
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


if __name__ == "__main__":
    args = _parse_args()
    plot = All1DPlot(config_path=args.config, include=args.include,
                     exclude=args.exclude, group_by=args.group_by,
                     single_pdf=args.single_pdf, yscale=args.yscale,
                     keep_empty=args.keep_empty, limit=args.limit,
                     jobs=args.jobs, save_png=not args.no_png)
    if args.list:
        for t in plot.targets():
            print(f"{t['subpath']}/{t['hist_name']}")
        print(f"{len(plot.targets())} histograms selected")
    else:
        plot.run()
