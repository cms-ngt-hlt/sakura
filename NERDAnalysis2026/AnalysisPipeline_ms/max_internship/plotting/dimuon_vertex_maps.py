"""HLT and NGT DiMuonNoVtx vertex maps side by side, with projections.

Run from the usual plotting working directory, e.g.::

    python dimuon_vertex_maps.py --config config.yaml

Uses the same inputs, common-run selection and luminosity handling as
all_2D_ScoutingDQM.py. Counts are not normalised. Each page has a common
colour scale and matching projection limits across conditions. Axis titles
come from ROOT (the histogram name does not determine axis ordering).
"""

import argparse
from pathlib import Path
import re

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, SymLogNorm
import numpy as np

from all_2D_ScoutingDQM import All2DPlot
from scouting_plot import FigureOutput


class DiMuonVertexMaps(All2DPlot):
    def __init__(self, *args, map_scale="symlog", beamline_copies=True, **kwargs):
        self.map_scale = map_scale
        self.beamline_copies = beamline_copies
        if map_scale not in ("linear", "symlog"):
            raise ValueError("map_scale must be linear or symlog")
        super().__init__(
            *args, pairs=[("HLT", "NGT")],
            pdf_name="Comparison_DiMuonNoVtx_VertexMaps_HLT_vs_NGT.pdf", **kwargs)

    def _selected(self, full_name):
        return bool(re.fullmatch(
            r"DiMuonNoVtx/DiMuonVertexMonitor/Vtx(?:RvsZ|ZvsR|XvsY|YvsX)(?:_.*)?",
            full_name)) and super()._selected(full_name)

    def make_figures(self, target, fetched):
        xlabel = self._label(target["xtitle"], "x")
        ylabel = self._label(target["ytitle"], "y")
        for label_a, label_b, da, db in fetched:
            _, xedges, yedges = da
            beam_mask = (self._beamline_mask(target, xedges, yedges)
                         if self.beamline_copies else None)
            for mask in ([None, beam_mask] if beam_mask is not None else [None]):
                arrays = [np.where(mask, np.nan, d[0]) if mask is not None else d[0]
                          for d in (da, db)]
                finite = np.concatenate([a[np.isfinite(a)] for a in arrays])
                vmin = min(0., float(finite.min())) if finite.size else 0.
                vmax = max(1., float(finite.max())) if finite.size else 1.
                norm = (SymLogNorm(linthresh=1., vmin=vmin, vmax=vmax)
                        if self.map_scale == "symlog" else Normalize(vmin, vmax))
                fig, axes = plt.subplots(
                    3, 2, figsize=(18, 15), sharey="row",
                    gridspec_kw={"height_ratios": [3.5, 1, 1]}, layout="none")
                fig.subplots_adjust(left=.08, right=.88, bottom=.07,
                                    top=.91, wspace=.23, hspace=.42)
                for col, (label, data, values) in enumerate(
                        zip((label_a, label_b), (da, db), arrays)):
                    ax = axes[0, col]
                    mesh = ax.pcolormesh(xedges, yedges, np.ma.masked_invalid(values.T),
                                         cmap="viridis", norm=norm, rasterized=True)
                    self.cms_label(ax, fontsize=17, target=target, labels=[label])
                    ax.text(.03, .96, label, transform=ax.transAxes, va="top",
                            fontsize=22, fontweight="bold",
                            bbox=dict(facecolor="white", alpha=.85, edgecolor="none"))
                    ax.set(xlabel=xlabel, ylabel=ylabel,
                           xlim=(xedges[0], xedges[-1]), ylim=(yedges[0], yedges[-1]))
                    for row, axis, edges, title in (
                            (1, 1, xedges, xlabel), (2, 0, yedges, ylabel)):
                        panel = axes[row, col]
                        projection = self._projection(label, target, data[0], axis, mask)
                        panel.stairs(projection, edges, color=("#5790fc" if col == 0 else "#e68613"),
                                     linewidth=1.8)
                        panel.set(xlabel=title, ylabel="Entries / bin",
                                  xlim=(edges[0], edges[-1]))
                        panel.grid(alpha=.25)
                for row in (1, 2):
                    axes[row, 0].set_ylim(bottom=0)
                cax = fig.add_axes([.90, axes[0, 1].get_position().y0,
                                    .015, axes[0, 1].get_position().height])
                fig.colorbar(mesh, cax=cax, label="Entries / bin")
                if mask is not None:
                    fig.text(.5, .97, "Beam line masked: r ≤ 1 cm (bin centres)",
                             ha="center", fontsize=17)
                name = self.png_name(target).removeprefix("Comparison_").removesuffix(".png")
                suffix = "_beamlineMasked" if mask is not None else ""
                yield FigureOutput(
                    fig=fig, png_name=f"SideBySide_{name}_HLT_vs_NGT{suffix}.png",
                    pdf_title=self.pdf_title(target))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--pipeline-cfg", type=Path,
                        default=Path(__file__).resolve().parents[1] / "pipeline.cfg")
    parser.add_argument("--local", action="store_true",
                        help="resolve config input paths from the working directory")
    parser.add_argument("--runs", nargs="+", type=int, default=[])
    parser.add_argument("--exclude-runs", nargs="+", type=int, default=[])
    parser.add_argument("--per-run", action="store_true")
    parser.add_argument("--lumi-csv")
    parser.add_argument("--include", action="append", default=[], metavar="REGEX",
                        help="further restrict the vertex maps, e.g. VtxRvsZ")
    parser.add_argument("--exclude", action="append", default=[], metavar="REGEX")
    parser.add_argument("--map-scale", choices=["linear", "symlog"], default="symlog",
                        help="shared colour scale; symlog reveals low-count structure")
    parser.add_argument("--no-beamline-copies", action="store_true")
    parser.add_argument("--no-png", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    options = vars(args).copy()
    options["config_path"] = options.pop("config")
    options["beamline_copies"] = not options.pop("no_beamline_copies")
    options["save_png"] = not options.pop("no_png")
    list_only = options.pop("list")
    try:
        plot = DiMuonVertexMaps(**options)
        if list_only:
            for run in plot.runs() if plot.per_run else [None]:
                if run is not None:
                    plot._select_run(run)
                for target in plot.targets():
                    print(plot.pdf_title(target))
        else:
            plot.run()
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc


if __name__ == "__main__":
    main()
