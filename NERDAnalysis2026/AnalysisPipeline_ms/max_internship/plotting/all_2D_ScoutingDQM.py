"""Discover all TH2 histograms and compare conditions with difference maps.

Shares input selection, caching, run filtering, PDF grouping and multiprocessing
with all_1D_ScoutingDQM. Each histogram produces one page per pair and difference
kind, with x/y projections. TProfile2D means are merged using their stored
weighted sums and bin weights.
"""

import sys
import time
import uproot
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm, TwoSlopeNorm

from all_1D_ScoutingDQM import All1DPlot, main
from scouting_plot import FigureOutput, RelDiffMap
from luminosity import load_lumi_info, directory_run


class All2DPlot(All1DPlot):
    dimension = 2
    pairs = (("NGT", "Prompt"), ("Prompt", "HLT"), ("HLT", "NGT"))

    def __init__(self, *args, difference="both", abs_z_limit=None,
                 rel_z_limit=None, **kwargs):
        super().__init__(*args, **kwargs)
        if difference not in ("both", "absolute", "relative"):
            raise ValueError("difference must be both, absolute or relative")
        for name, value in (("abs-z-limit", abs_z_limit),
                            ("rel-z-limit", rel_z_limit)):
            if value is not None and (not np.isfinite(value) or value <= 0):
                raise ValueError(f"--{name} must be finite and positive")
        self.kinds = ("absolute", "relative") if difference == "both" else (difference,)
        self.z_limits = {"absolute": abs_z_limit, "relative": rel_z_limit}

    def runs(self):
        """Validate luminosity coverage once, before discovery or summation."""
        if not hasattr(self, "_lumi_selected_runs"):
            selected = self.run_selection.runs()
            lumi_csv = str(Path(self.config.get("lumi_csv", "lumi_data.csv")).resolve())
            _, recorded = load_lumi_info(lumi_csv)
            missing = [run for run in selected if run not in recorded]
            if missing:
                lines = ["!" * 78,
                         "WARNING: DQM RUNS EXCLUDED FROM ALL FINAL 2D PLOTS",
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
                                 "no 2D plots will be generated. Update the luminosity CSV.")
            self._lumi_selected_runs = allowed
        return self._lumi_selected_runs

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
        # Unlike representative-file discovery, scan every selected file so
        # histograms introduced in later files/runs are also included.
        for cond in self.conditions:
            for fname, run in self._file_runs(cond):
                yield cond, fname, run

    @classmethod
    def _histogram_keys(cls, root_dir):
        return [key for key, kind in root_dir.iterclassnames(recursive=True, cycle=False)
                if kind.startswith("TH2") or kind == "TProfile2D"]

    @staticmethod
    def _mean(sums, weights):
        return np.divide(sums, weights, out=np.full_like(sums, np.nan, dtype=float),
                         where=weights != 0)

    def _preload(self, targets):
        """Merge counts, or profile sufficient statistics, once per file/run."""
        self._cache = {}
        self._profiles = {}
        self.source.contributing_runs.clear()
        wanted = [self._full_name(t) for t in targets]
        kinds = {}
        start = time.time()
        n_files = 0
        for cond in self.conditions:
            for fname, run in self._file_runs(cond):
                try:
                    with uproot.open(fname) as f:
                        root = self._dqm_root(f, run)
                        if root is None:
                            continue
                        present = set(self._histogram_keys(root))
                        for key in wanted:
                            if key not in present:
                                continue
                            try:
                                h = root[key]
                                profile = h.classname == "TProfile2D"
                                if key in kinds and kinds[key] != profile:
                                    raise ValueError("TH2/TProfile2D type mismatch")
                                edges = [h.axis(i).edges() for i in (0, 1)]
                                if profile:
                                    # ROOT stores x as the fastest-varying index,
                                    # including underflow and overflow on both axes.
                                    shape = (len(edges[1]) + 1, len(edges[0]) + 1)
                                    raw, = h.base(uproot.models.TArray.Model_TArray)
                                    values = np.asarray(raw, dtype=float).reshape(shape).T[1:-1, 1:-1].copy()
                                    weights = np.asarray(h.member("fBinEntries"), dtype=float).reshape(shape).T[1:-1, 1:-1].copy()
                                else:
                                    values = np.array(h.values(), dtype=float)
                                cache_key = (cond.label, key)
                                entry = self._cache.get(cache_key)
                                if entry is not None:
                                    if (entry[0].shape != values.shape or any(
                                            not np.array_equal(a, b) for a, b in zip(entry[1:], edges))):
                                        raise ValueError("incompatible bin edges")
                                    entry[0] += values
                                    if profile:
                                        self._profiles[cache_key][1] += weights
                                else:
                                    self._cache[cache_key] = [values, *edges]
                                    if profile:
                                        self._profiles[cache_key] = [values, weights]
                                kinds[key] = profile
                                subpath, _, name = key.rpartition("/")
                                self.source.contributing_runs.setdefault(
                                    (cond.label, subpath, name), set()).add(directory_run(root))
                            except Exception as exc:
                                print(f"   [Warning] Skipping {key} in {fname}: {exc}")
                    n_files += 1
                except Exception as exc:
                    print(f"   [Warning] Error reading {fname}: {exc}")
        for key, (sums, weights) in self._profiles.items():
            self._cache[key][0] = self._mean(sums, weights)
        print(f"Loaded {len(wanted)} histograms/profiles from {n_files} file/run(s) "
              f"in {time.time() - start:.1f} s")

    def _projection(self, label, target, values, axis):
        stats = self._profiles.get((label, self._full_name(target)))
        if stats is None:
            return np.sum(values, axis=axis)
        sums, weights = stats
        return self._mean(np.sum(sums, axis=axis), np.sum(weights, axis=axis))

    def fetch(self, target):
        key = self._full_name(target)
        data = {c.label: self._cache[(c.label, key)] for c in self.conditions
                if (c.label, key) in self._cache}
        if not self.keep_empty and all(
                not np.any(np.isfinite(d[0]) & (d[0] != 0))
                and not np.any(getattr(self, "_profiles", {}).get(
                    (label, key), (None, np.array([])))[1])
                for label, d in data.items()):
            return None
        pairs = []
        for a, b in self.pairs:
            if a not in data or b not in data:
                print(f"   [Warning] Missing {a} or {b}; pair skipped")
                continue
            da, db = data[a], data[b]
            if (da[0].shape != db[0].shape or
                    any(not np.array_equal(x, y) for x, y in zip(da[1:], db[1:]))):
                print(f"   [Warning] Binning mismatch for {a} vs {b}; pair skipped")
                continue
            pairs.append((a, b, da, db))
        return pairs or None

    @staticmethod
    def difference(a, b, kind):
        return a - b if kind == "absolute" else RelDiffMap._rel_diff(a, b)

    def make_figures(self, target, fetched):
        xlabel = self._label(target["xtitle"], "x")
        ylabel = self._label(target["ytitle"], "y")
        for label_a, label_b, da, db in fetched:
            a, xedges, yedges = da
            b = db[0]
            for kind in self.kinds:
                diff = self.difference(a, b, kind)
                formula = f"{label_a} − {label_b}"
                if kind == "relative":
                    formula = f"({formula}) / {label_b}"
                finite = np.abs(diff[np.isfinite(diff)])
                limit = self.z_limits[kind]
                if limit is None:
                    limit = max(float(finite.max()) if finite.size else 0., 1e-12)
                    if not finite.size or not np.any(finite):
                        limit = 1.
                norm = (SymLogNorm(linthresh=min(1., limit), vmin=-limit, vmax=limit)
                        if kind == "absolute" else
                        TwoSlopeNorm(vmin=-limit, vcenter=0., vmax=limit))
                fig, axes = plt.subplots(3, 1, figsize=(12, 14),
                                         gridspec_kw={"height_ratios": [4, 1, 1]},
                                         layout="constrained")
                ax = axes[0]
                self.cms_label(ax, fontsize=18, target=target,
                               labels=[label_a, label_b])
                mesh = ax.pcolormesh(xedges, yedges, np.ma.masked_invalid(diff.T),
                                     cmap="PiYG", norm=norm, rasterized=True)
                quantity = "Profile mean: " if (label_a, self._full_name(target)) in self._profiles else ""
                fig.colorbar(mesh, ax=ax, label=quantity + formula, extend="both")
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                # Keep the comparison identifiable in PNGs, which omit PDF titles.
                ax.text(0.02, 0.98, formula, transform=ax.transAxes, va="top",
                        fontsize=14, bbox={"facecolor": "white", "alpha": .8,
                                           "edgecolor": "none"})
                for panel, axis, edges, label in ((axes[1], 1, xedges, xlabel),
                                                  (axes[2], 0, yedges, ylabel)):
                    # Relative differences of projections: sum FIRST, then divide.
                    values = self.difference(self._projection(label_a, target, a, axis),
                                             self._projection(label_b, target, b, axis), kind)
                    panel.stairs(values, edges, color="black", linewidth=1.5)
                    panel.axhline(0, color="gray", linestyle="--", linewidth=1)
                    panel.grid(alpha=.3)
                    panel.set_xlim(edges[0], edges[-1])
                    panel.set_xlabel(label)
                    panel.set_ylabel("Difference" if kind == "absolute" else "Rel. diff.")
                name = self.png_name(target).removeprefix("Comparison_").removesuffix(".png")
                yield FigureOutput(
                    fig=fig,
                    png_name=f"Comparison_All2D_{name}_{kind}_{label_a}_vs_{label_b}.png",
                    pdf_title=f"{self.pdf_title(target)}\n{kind.capitalize()} difference: {formula}")


if __name__ == "__main__":
    main(All2DPlot)
