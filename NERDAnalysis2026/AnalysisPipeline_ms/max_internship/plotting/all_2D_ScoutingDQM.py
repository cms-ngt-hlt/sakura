"""Discover all TH2 histograms and compare conditions with difference maps.

Shares input selection, caching, run filtering, PDF grouping and multiprocessing
with all_1D_ScoutingDQM. Each histogram produces one page per pair and difference
kind, with x/y projections. TProfile2D means are merged using their stored
weighted sums and bin weights.
"""

import sys
import re
from itertools import product
import time
import uproot
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm, TwoSlopeNorm
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

from all_1D_ScoutingDQM import All1DPlot, main
from scouting_plot import FigureOutput, RelDiffMap
from luminosity import load_lumi_info, directory_run


class All2DPlot(All1DPlot):
    dimension = 2
    pairs = (("NGT", "Prompt"), ("Prompt", "HLT"), ("HLT", "NGT"))

    def __init__(self, *args, difference="both", z_limit=None, abs_z_limit=None,
                 rel_z_limit=None, pairs=None, cbar_label=None, aspect="auto",
                 projection="xy", radial_center=(0., 0.), radial_bin_width=None,
                 radial_xlim=None, pdf_name=None, **kwargs):
        if pdf_name is not None:
            kwargs["single_pdf"] = True
        self.custom_pdf_name = pdf_name
        super().__init__(*args, **kwargs)
        if difference not in ("both", "absolute", "relative"):
            raise ValueError("difference must be both, absolute or relative")
        for name, value in (("z-limit", z_limit), ("abs-z-limit", abs_z_limit),
                            ("rel-z-limit", rel_z_limit)):
            if value is not None and (not np.isfinite(value) or value <= 0):
                raise ValueError(f"--{name} must be finite and positive")
        self.kinds = ("absolute", "relative") if difference == "both" else (difference,)
        if z_limit is not None:
            if abs_z_limit is not None or rel_z_limit is not None:
                raise ValueError("Use --z-limit alone, without the legacy per-kind limits")
            abs_z_limit = rel_z_limit = z_limit
        self.z_limits = {"absolute": abs_z_limit, "relative": rel_z_limit}
        self.pairs = tuple(tuple(pair) for pair in pairs) if pairs is not None else type(self).pairs
        labels = {c.label for c in self.conditions}
        if not self.pairs or any(len(pair) != 2 or not set(pair) <= labels for pair in self.pairs):
            raise ValueError("--pair requires two configured condition labels")
        self.pairs = tuple(dict.fromkeys(self.pairs))
        if projection not in ("xy", "radial") or aspect not in ("auto", "equal"):
            raise ValueError("Invalid projection or aspect")
        if len(radial_center) != 2 or not np.all(np.isfinite(radial_center)):
            raise ValueError("--radial-center requires two finite coordinates")
        if radial_bin_width is not None and (not np.isfinite(radial_bin_width) or radial_bin_width <= 0):
            raise ValueError("--radial-bin-width must be finite and positive")
        if radial_xlim is not None and (len(radial_xlim) != 2 or
                not np.all(np.isfinite(radial_xlim)) or radial_xlim[0] >= radial_xlim[1]):
            raise ValueError("--radial-xlim requires finite MIN < MAX")
        self.cbar_label = cbar_label
        self.aspect = aspect
        self.projection = projection
        self.radial_center = radial_center
        self.radial_bin_width = radial_bin_width
        self.radial_xlim = radial_xlim

    def _pdf_name(self, group):
        if self.custom_pdf_name is None:
            return super()._pdf_name(group)
        path = Path(self.custom_pdf_name)
        if self.active_run is not None:
            path = path.with_name(f"{path.stem}_Run{self.active_run}{path.suffix}")
        return str(path)

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

    def _projection(self, label, target, values, axis, mask=None):
        stats = self._profiles.get((label, self._full_name(target)))
        if stats is None:
            return np.sum(values if mask is None else np.where(mask, 0., values), axis=axis)
        sums, weights = stats
        if mask is not None:
            sums = np.where(mask, 0., sums)
            weights = np.where(mask, 0., weights)
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

    @staticmethod
    def _beamline_mask(target, xedges, yedges):
        """Exclude the nominal beam-line cylinder (radius 1 cm) in XY and RZ.

        These DQM vertex coordinates default to cm. Honour explicit mm or m
        axis units too; never apply a spatial mask to generic eta/phi maps.
        """
        if not re.match(r"^Vtx(?:XvsY|YvsX|RvsZ|ZvsR)(?:_|$)", target["hist_name"]):
            return None

        def to_cm(title):
            unit = re.search(r"(?:\[|\()\s*(cm|mm|m)\s*(?:\]|\))", title)
            return {"cm": 1., "mm": .1, "m": 100.}[unit.group(1)] if unit else 1.

        x = .5 * (xedges[:-1] + xedges[1:]) * to_cm(target["xtitle"])
        y = .5 * (yedges[:-1] + yedges[1:]) * to_cm(target["ytitle"])
        if re.match(r"^Vtx(?:RvsZ|ZvsR)(?:_|$)", target["hist_name"]):
            # Do not infer axis ordering from 'A vs B': use ROOT axis titles.
            radial = [bool(re.search(r"(?<![a-z])(?:r|rho|radius)(?![a-z])",
                                     target[title].lower()))
                      for title in ("xtitle", "ytitle")]
            if radial == [True, False]:
                return np.broadcast_to(np.abs(x[:, None]) <= 1., (len(x), len(y)))
            if radial == [False, True]:
                return np.broadcast_to(np.abs(y[None, :]) <= 1., (len(x), len(y)))
            print(f"   [Warning] Cannot identify radial axis for {target['hist_name']} "
                  f"from titles {target['xtitle']!r}, {target['ytitle']!r}; "
                  "beam-line-masked copy skipped (original retained)")
            return None
        return x[:, None] ** 2 + y[None, :] ** 2 <= 1.

    def _radial_geometry(self, xedges, yedges):
        x = .5 * (xedges[:-1] + xedges[1:]) - self.radial_center[0]
        y = .5 * (yedges[:-1] + yedges[1:]) - self.radial_center[1]
        radii = np.hypot(x[:, None], y[None, :])
        width = self.radial_bin_width or float(np.min(np.diff(xedges)))
        edges = np.arange(max(1, int(np.ceil(radii.max() / width))) + 1) * width
        return radii, edges

    def _radial_projection(self, label, target, values, radii, edges, mask):
        keep = np.ones(values.shape, dtype=bool) if mask is None else ~mask
        def project(array):
            return np.histogram(radii[keep], bins=edges, weights=array[keep])[0]
        stats = self._profiles.get((label, self._full_name(target)))
        if stats is None:
            return project(values)
        return self._mean(project(stats[0]), project(stats[1]))

    def make_figures(self, target, fetched):
        xlabel = self.xlabel if self.xlabel is not None else self._label(target["xtitle"], "x")
        ylabel = self.ylabel if self.ylabel is not None else self._label(target["ytitle"], "y")
        for label_a, label_b, da, db in fetched:
            a, xedges, yedges = da
            b = db[0]
            beam_mask = self._beamline_mask(target, xedges, yedges)
            for kind, masked in product(self.kinds, (False, True) if beam_mask is not None else (False,)):
                mask = beam_mask if masked else None
                diff = self.difference(a, b, kind)
                if masked:
                    diff = np.where(mask, np.nan, diff)
                formula = f"{label_a} − {label_b}"
                if kind == "relative":
                    formula = f"({formula}) / {label_b}"
                finite = np.abs(diff[np.isfinite(diff)])
                limit = self.z_limits[kind]
                if limit is None:
                    limit = max(float(finite.max()) if finite.size else 0., 1e-12)
                    if not finite.size or not np.any(finite):
                        limit = 1.
                norm = (SymLogNorm(linthresh=1., vmin=-limit, vmax=limit, base=10)
                        if kind == "absolute" else
                        TwoSlopeNorm(vmin=-limit, vcenter=0., vmax=limit))
                radial = self.projection == "radial"
                fig, axes = plt.subplots(2 if radial else 3, 1,
                                         figsize=(8, 10) if radial else (12, 14),
                                         gridspec_kw={"height_ratios": [4, 1] if radial else [4, 1, 1]},
                                         layout="constrained")
                ax = axes[0]
                self.cms_label(ax, fontsize=18, target=target,
                               labels=[label_a, label_b])
                mesh = ax.pcolormesh(xedges, yedges, np.ma.masked_invalid(diff.T),
                                     cmap="PiYG", norm=norm, rasterized=True)
                quantity = "Profile mean: " if (label_a, self._full_name(target)) in self._profiles else ""
                # Match the approved DP RecHit scripts: 5%-width rectangular
                # bar, 0.05-inch gap, same height as the map, no extension caps.
                cax = make_axes_locatable(ax).append_axes("right", size="5%", pad=0.05)
                cbar = fig.colorbar(mesh, cax=cax)
                cbar.set_label(self.cbar_label if self.cbar_label is not None else quantity + formula,
                               fontsize=22 if kind == "absolute" else (18 if radial else 20))
                if kind == "relative":
                    cbar.formatter = FuncFormatter(lambda value, pos: f"{value:.2f}")
                    cbar.update_ticks()
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                ax.set_aspect(self.aspect)
                if self.xlim is not None:
                    ax.set_xlim(*self.xlim)
                if self.ylim is not None:
                    ax.set_ylim(*self.ylim)
                # Keep the comparison identifiable in PNGs, which omit PDF titles.
                annotation = formula + ("\nBeam line masked: r ≤ 1 cm (bin centres)" if masked else "")
                ax.text(0.02, 0.98, annotation, transform=ax.transAxes, va="top",
                        fontsize=14, bbox={"facecolor": "white", "alpha": .8,
                                           "edgecolor": "none"})
                if radial:
                    radii, redges = self._radial_geometry(xedges, yedges)
                    pa = self._radial_projection(label_a, target, a, radii, redges, mask)
                    pb = self._radial_projection(label_b, target, b, radii, redges, mask)
                    panels = [(axes[1], redges, r"$r_{ix,iy}$", self.radial_xlim,
                               self.difference(pa, pb, kind))]
                else:
                    panels = []
                    for panel, axis, edges, label, limits in (
                            (axes[1], 1, xedges, xlabel, self.xlim),
                            (axes[2], 0, yedges, ylabel, self.ylim)):
                        values = self.difference(self._projection(label_a, target, a, axis, mask),
                                                 self._projection(label_b, target, b, axis, mask), kind)
                        panels.append((panel, edges, label, limits, values))
                for panel, edges, label, limits, values in panels:
                    panel.stairs(values, edges, color="black", linewidth=1.5)
                    panel.axhline(0, color="gray", linestyle="--", linewidth=1)
                    panel.grid(alpha=.3)
                    panel.set_xlim(*(limits if limits is not None else (edges[0], edges[-1])))
                    panel.set_xlabel(label)
                    panel.set_ylabel("Difference" if kind == "absolute" else "Rel. diff.")
                    make_axes_locatable(panel).append_axes(
                        "right", size="5%", pad=0.05).axis("off")
                name = self.png_name(target).removeprefix("Comparison_").removesuffix(".png")
                if radial:
                    name += "_radial"
                if masked:
                    name += "_beamlineMasked"
                yield FigureOutput(
                    fig=fig,
                    png_name=f"Comparison_All2D_{name}_{kind}_{label_a}_vs_{label_b}.png",
                    pdf_title=f"{self.pdf_title(target)}\n{kind.capitalize()} difference: {annotation}")


if __name__ == "__main__":
    main(All2DPlot)
