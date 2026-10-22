"""Discover all TH2 histograms and compare conditions with difference maps.

Shares input selection, caching, run filtering, PDF grouping and multiprocessing
with all_1D_ScoutingDQM. Each histogram produces one page per pair and difference
kind, with x/y projections. TProfiles are excluded because their means cannot
be aggregated by summing bin contents.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import SymLogNorm, TwoSlopeNorm

from all_1D_ScoutingDQM import All1DPlot, main
from scouting_plot import FigureOutput, RelDiffMap


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

    def _first_files(self):
        # Unlike representative-file discovery, scan every selected file so
        # histograms introduced in later files/runs are also included.
        for cond in self.conditions:
            for fname, run in self._file_runs(cond):
                yield cond, fname, run

    def fetch(self, target):
        key = self._full_name(target)
        data = {c.label: self._cache[(c.label, key)] for c in self.conditions
                if (c.label, key) in self._cache}
        if not self.keep_empty and all(not np.any(d[0]) for d in data.values()):
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
                fig.colorbar(mesh, ax=ax, label=formula, extend="both")
                ax.set_xlabel(xlabel)
                ax.set_ylabel(ylabel)
                # Keep the comparison identifiable in PNGs, which omit PDF titles.
                ax.text(0.02, 0.98, formula, transform=ax.transAxes, va="top",
                        fontsize=14, bbox={"facecolor": "white", "alpha": .8,
                                           "edgecolor": "none"})
                for panel, axis, edges, label in ((axes[1], 1, xedges, xlabel),
                                                  (axes[2], 0, yedges, ylabel)):
                    # Relative differences of projections: sum FIRST, then divide.
                    values = self.difference(np.sum(a, axis=axis),
                                             np.sum(b, axis=axis), kind)
                    panel.stairs(values, edges, color="black", linewidth=1.5)
                    panel.axhline(0, color="gray", linestyle="--", linewidth=1)
                    panel.grid(alpha=.3)
                    panel.set_xlim(edges[0], edges[-1])
                    panel.set_xlabel(label)
                    panel.set_ylabel("Difference" if kind == "absolute" else "Rel. diff.")
                name = self.png_name(target).removeprefix("Comparison_")
                yield FigureOutput(
                    fig=fig,
                    png_name=f"Comparison_All2D_{kind}_{label_a}_vs_{label_b}_{name}",
                    pdf_title=f"{self.pdf_title(target)}\n{kind.capitalize()} difference: {formula}")


if __name__ == "__main__":
    main(All2DPlot)
