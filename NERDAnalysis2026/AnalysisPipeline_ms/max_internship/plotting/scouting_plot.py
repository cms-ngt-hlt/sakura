"""
scouting_plot.py
================
Shared plotting framework for the Scouting DQM comparison plots.

This module contains everything that is COMMON to all eight plotting
scripts.  Anything that is specific to a single plot (histogram names,
axis labels, axis limits, z-limits, figure geometry, ...) is hardcoded in
the concrete subclasses, which live in the thin entry scripts.

Class hierarchy
---------------
    ScoutingPlot            (abstract: config + data access + run() lifecycle)
    |-- ComparisonPlot1D    (template: 3-condition overlay + ratio panel)
    |     concrete subclasses live in the entry scripts:
    |     RecHitsPlot, EtaPlot, PiZeroMassPlot, DileptonMassPlot
    |-- DifferenceMap2D     (template: pairwise 2D map + projection panels)
          |-- AbsDiffMap          (A - B, SymLogNorm, cartesian projections)
          |-- RelDiffMap          ((A - B) / B, TwoSlopeNorm, cartesian proj.)
                |-- RelDiffMapRadial  (radial projection around the beam axis)

The following changes were made when refactoring the code:
* Every PDF page now carries the histogram name as a title, and every PNG
  is saved with dpi=150 (previously only some scripts did either).
* PNGs (and the dielectron standalone per-plot PDFs) go into the
  `output.png_dir` folder from config.yaml instead of the working dir.
* Warnings are printed for file-read errors and histogram shape
  mismatches (previously swallowed silently).
* The dielectron-only `plt.rcParams['font.size'] = 20` override is gone.
* Dead code (unused `global_max_abs`, marker-size debug print) not ported.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import glob
import os
import traceback

import numpy as np
import uproot
import yaml # additional dependency
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import SymLogNorm, TwoSlopeNorm
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mplhep as hep


# ----------------------------------------------------------------------
# Module-wide output constants
# Previously: dpi was 150 only for the EE relative-diff PNGs (matplotlib
# default of 100 elsewhere); the title fontsize was 22 in the 1D scripts
# and 20 in the 2D scripts.
# ----------------------------------------------------------------------
PNG_DPI = 150
PDF_TITLE_FONTSIZE = 20
PDF_TITLE_PAD = 20


# ======================================================================
# Configuration
# ======================================================================

_REQUIRED_CONFIG_KEYS = (
    "conditions", "reference", "cms_label", "dqm_prefix",
    "diff_pairs", "output",
)


def load_config(config_path="config.yaml"):
    """
    Read config.yaml and return it as a nested dict.

    Fails loudly if the file or a required key is missing.
    """
    with open(config_path) as fh:
        config = yaml.safe_load(fh)
    missing = [k for k in _REQUIRED_CONFIG_KEYS if k not in config]
    if missing:
        raise KeyError(
            f"Config file '{config_path}' is missing required keys: {missing}")
    return config


@dataclass
class Condition:
    """
    One conditions scenario (one entry of `files_config` in the old
    scripts).

    label        : short key used for diff-pair lookup, 2D titles and
                   filenames (e.g. "Prompt")
    legend_label : long form used in the 1D legends
                   (e.g. "Prompt Conditions")
    path         : directory globbed for "*.root"
    color, style : matplotlib color / linestyle (1D overlays only)
    """
    label: str
    legend_label: str
    path: str
    color: str = "black"
    style: str = "-"


# ======================================================================
# Data access layer
# ======================================================================

class HistogramSource:
    """
    Encapsulates all ROOT I/O:
      * globbing the per-condition directories for *.root files
      * resolving the run-dependent DQM path
      * summing histograms across runs/files
      * opening and ALWAYS closing file handles

    Replaces the free functions `get_base_dir`, `fetch_and_sum` and
    `fetch_and_sum_2d` from the original scripts.
    """

    def __init__(self, dqm_prefix):
        # e.g. "HLT/Run summary/ScoutingOnline" (from config.yaml)
        self.dqm_prefix = dqm_prefix

    def _resolve_dir(self, file_handle, subpath):
        """
        Find the run-dependent directory inside one open ROOT file.
        Verbatim port of `get_base_dir` (identical in all eight scripts):
        require "DQMData", find the first key containing "Run ", build
        "DQMData/{run folder}/{dqm_prefix}/{subpath}", return the
        directory handle if it exists, else None.
        """
        if "DQMData" not in file_handle:
            return None
        dqm_keys = file_handle["DQMData"].keys(cycle=False)
        run_folder = next((k for k in dqm_keys if "Run " in k), None)
        if run_folder is None:
            return None
        full_path = f"DQMData/{run_folder}/{self.dqm_prefix}/{subpath}"
        if full_path in file_handle:
            return file_handle[full_path]
        return None

    def fetch_summed(self, condition, subpath, hist_name):
        """
        Open every *.root file under `condition.path`, resolve the DQM
        directory, and sum the histogram `hist_name` across all files.

        Returns a tuple of numpy arrays `(values, *edges)` -- i.e.
        (values, edges) for 1D and (values, xedges, yedges) for 2D --
        or None if the histogram was not found in any file.  The
        dimensionality is taken from `to_numpy()`, which is why this one
        method replaces both `fetch_and_sum` and `fetch_and_sum_2d`.

        Behaviour preserved from the originals:
          * first successfully read histogram initialises the sum
            (cast to float) and the edges
          * later histograms are added only if the shapes match
          * per-file problems do not abort the aggregation
        Changed: shape mismatches and per-file errors now print a
        warning instead of being swallowed silently.
        """
        files = glob.glob(os.path.join(condition.path, "*.root"))
        if not files:
            print(f"   [Warning] No .root files found in {condition.path}")
            return None

        sum_values = None
        edges = None
        for fname in files:
            try:
                with uproot.open(fname) as f:
                    d = self._resolve_dir(f, subpath)
                    if d is None or hist_name not in d:
                        continue
                    data = d[hist_name].to_numpy()
                    if sum_values is None:
                        sum_values = np.array(data[0], dtype=float)
                        edges = data[1:]
                    elif data[0].shape == sum_values.shape:
                        sum_values += data[0]
                    else:
                        print(f"   [Warning] Shape mismatch for "
                              f"'{hist_name}' in {fname}: "
                              f"{data[0].shape} vs {sum_values.shape}; "
                              f"file skipped for this histogram")
            except Exception as e:
                print(f"   [Warning] Error reading {fname}: {e}")

        if sum_values is None:
            return None
        return (sum_values, *edges)


# ======================================================================
# Figure output description
# ======================================================================

@dataclass
class FigureOutput:
    """
    One finished matplotlib figure plus the instructions for saving it.
    """
    fig: object                 # matplotlib Figure
    png_name: str               # basename; saved under output.png_dir
    pdf_title: str              # shown on the PdfPages page, stripped
                                # again before the PNG save
    extra_pdf_name: str = None  # dielectron also writes a standalone
                                # per-plot PDF (into png_dir as well)


# ======================================================================
# Abstract base class
# ======================================================================

class ScoutingPlot(ABC):
    """
    The abstract idea of "one plotting script":

        load config -> for each target: fetch data -> build figure(s)
        -> save (PdfPages + PNGs) -> report

    `run()` is fixed (Template Method); subclasses provide `targets()`,
    `fetch()` and `make_figures()`.
    """

    # name of the multi-page PDF; set by each concrete subclass
    output_pdf = None

    def __init__(self, config_path="config.yaml"):
        self.config = load_config(config_path)
        self.conditions = [Condition(**c) for c in self.config["conditions"]]

        # The reference condition is named explicitly in the config
        # (replaces the old "reference = first entry" convention).
        ref_label = self.config["reference"]
        try:
            self.reference = next(
                c for c in self.conditions if c.label == ref_label)
        except StopIteration:
            raise ValueError(
                f"reference '{ref_label}' not found among condition labels "
                f"{[c.label for c in self.conditions]}")

        self.source = HistogramSource(self.config["dqm_prefix"])

        self.png_dir = self.config["output"]["png_dir"]
        os.makedirs(self.png_dir, exist_ok=True)

        plt.style.use(hep.style.CMS)

    def cms_label(self, ax, fontsize):
        """The experiment label; year/lumi/com come from config.yaml (single source of truth for all eight plots)."""
        cl = self.config["cms_label"]
        hep.cms.label(ax=ax, data=True, label="Private Work (CMS data)",
                      year=cl["year"], lumi=cl["lumi"], com=cl["com"],
                      fontsize=fontsize)

    # ---- hooks -------------------------------------------------------

    @abstractmethod
    def targets(self):
        """
        Return the list of histograms to process.  Each element is a
        plain dict with at least "subpath" and "hist_name"
        """

    @abstractmethod
    def fetch(self, target):
        """Gather the input data for one target (see the two
        intermediate classes for the exact return shape).  Return None
        to skip the target."""

    @abstractmethod
    def make_figures(self, target, fetched):
        """Build the figure(s) for one target and return a list of
        FigureOutput (1D: exactly one; 2D: one per diff pair)."""

    # ---- the fixed template ------------------------------------------

    def run(self):
        """The fixed lifecycle, identical for all eight scripts."""
        try:
            print(f"--- Starting analysis for {self.output_pdf} ---")
            with PdfPages(self.output_pdf) as pdf:
                for target in self.targets():
                    print(f" > Processing {target['hist_name']}...")
                    fetched = self.fetch(target)
                    if fetched is None:
                        print(f"   [Warning] No valid data for "
                              f"{target['hist_name']}")
                        continue
                    for out in self.make_figures(target, fetched):
                        self._save(out, pdf)
            print(f"SUCCESS: Analysis complete. Output: {self.output_pdf}")
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            traceback.print_exc()

    def _save(self, out, pdf_pages):
        """
        The single saving routine, driven entirely by FigureOutput:
        PDF page with title, then PNG (and optional standalone PDF)
        without it.  fig.axes[0] is always the main axes: it is created
        first, and colorbar/spacer axes are only appended afterwards.
        """
        ax_main = out.fig.axes[0]
        ax_main.set_title(out.pdf_title,
                          fontsize=PDF_TITLE_FONTSIZE, pad=PDF_TITLE_PAD)
        pdf_pages.savefig(out.fig, bbox_inches="tight")

        ax_main.set_title("")
        png_path = os.path.join(self.png_dir, out.png_name)
        out.fig.savefig(png_path, bbox_inches="tight", dpi=PNG_DPI)
        print(f"   [Info] Saved {png_path}")
        if out.extra_pdf_name:
            out.fig.savefig(os.path.join(self.png_dir, out.extra_pdf_name),
                            bbox_inches="tight")
        plt.close(out.fig)


# ======================================================================
# Intermediate class 1: 1D condition-overlay comparison
# ======================================================================

class ComparisonPlot1D(ScoutingPlot):
    """
    Template for the four 1D scripts: overlay all conditions in a main
    panel, ratio-to-reference in a lower panel, gray band = statistical
    uncertainty of the reference.
    """

    # ---- data access -------------------------------------------------

    def fetch(self, target):
        """
        Ordered list (same order as self.conditions) of
        {"condition": Condition, "data": (values, edges) or None}.
        None entries stay in the list as placeholders: the originals
        keep plotting the remaining conditions if one is missing.
        Returns None (-> target skipped) only if nothing was found.
        """
        fetched = []
        for cond in self.conditions:
            data = self.source.fetch_summed(
                cond, target["subpath"], target["hist_name"])
            fetched.append({"condition": cond, "data": self.transform(data)})
        if all(item["data"] is None for item in fetched):
            return None
        return fetched

    # ---- hooks with defaults (override only where needed) ------------

    def transform(self, data):
        """Optional preprocessing of one (values, edges) tuple; default
        identity.  DileptonMassPlot overrides this with the rebin-by-2.
        PHYSICS: transformations change bin contents, so they must live
        in exactly one subclass and nowhere else."""
        return data

    def decorate(self, ax_main, ax_ratio, target):
        """Subclass hook for everything plot-specific: axis labels,
        x/y limits, ratio y-range, extra reference lines.  Runs AFTER
        the common defaults (so it can override them) and BEFORE the
        legends (so labelled artists added here -- e.g. the pi0 mass
        line -- appear in the legend).  Default: no-op."""

    def legend_loc(self, target):
        """Legend location for both panels; default 'best'
        (EtaPlot overrides for the photon histogram)."""
        return "best"

    def ratio_marker_size(self, edges, target):
        """Adaptive marker size shared by three of the four scripts.
        (The fallback is unreachable in practice -- edges are never
        empty -- and only kept to mirror the originals.)
        RecHitsPlot overrides this for 'eeRechitsN'."""
        return 600 / len(edges) if len(edges) > 0 else 8

    def png_name(self, target):
        """Default matches RecHits / PiZero / Eta;
        DileptonMassPlot overrides."""
        return f"Comparison_{target['hist_name']}.png"

    def pdf_title(self, target):
        return target["hist_name"]

    def extra_pdf_name(self, target):
        """Only the dielectron script writes a standalone per-plot PDF."""
        return None

    @abstractmethod
    def apply_yscale(self, ax_main, max_y, target):
        """Set the main-panel y-scale.  Deliberately abstract with NO
        default (review decision): every subclass states its rule
        explicitly.  Use `self._sci_notation(ax_main)` for the shared
        'linear + scientific y ticks' style."""

    @staticmethod
    def _sci_notation(ax_main):
        """Linear scale with scientific-notation y ticks, shared verbatim
        by all four originals."""
        ax_main.set_yscale("linear")
        ax_main.ticklabel_format(style="sci", axis="y", scilimits=(0, 0))
        ax_main.yaxis.get_offset_text().set_fontsize(18)
        ax_main.yaxis.get_offset_text().set_x(-0.06)

    # ---- the fixed 1D figure template --------------------------------

    def make_figures(self, target, fetched):
        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, figsize=(10, 10), sharex=True,
            gridspec_kw={"height_ratios": [3, 1], "hspace": 0.05})
        self.cms_label(ax_main, fontsize=22)

        # -- reference (gray band) ------------------------------------
        ref_item = next(
            i for i in fetched if i["condition"] is self.reference)
        ref_values = ref_edges = None
        if ref_item["data"] is not None:
            ref_values, ref_edges = ref_item["data"]
            ref_rel_err = np.divide(np.sqrt(ref_values), ref_values,
                                    out=np.zeros_like(ref_values),
                                    where=ref_values > 0)
            bin_centers = 0.5 * (ref_edges[:-1] + ref_edges[1:])
            ax_ratio.fill_between(
                bin_centers, 1 - ref_rel_err, 1 + ref_rel_err,
                step="mid", alpha=0.3, color="gray",
                label=f"Stat. unc. ({self.reference.label})")

        # -- main + ratio panels --------------------------------------
        max_y = 0.0
        last_edges = ref_edges
        for item in fetched:
            if item["data"] is None:
                continue
            values, edges = item["data"]
            if np.sum(values) == 0:
                continue
            max_y = max(max_y, np.max(values))
            last_edges = edges
            cond = item["condition"]

            hep.histplot(values, bins=edges, ax=ax_main,
                         label=cond.legend_label, color=cond.color,
                         linestyle=cond.style, linewidth=2, yerr=True)

            if ref_values is not None and len(values) == len(ref_values):
                ratio = np.divide(values, ref_values,
                                  out=np.full_like(values, np.nan),
                                  where=ref_values != 0)
                # PHYSICS: propagated uncorrelated uncertainty
                # sigma_R = R * sqrt(1/N + 1/D), guarded divides.
                err_ratio = ratio * np.sqrt(
                    np.divide(1, values, out=np.zeros_like(values),
                              where=values > 0)
                    + np.divide(1, ref_values,
                                out=np.zeros_like(ref_values),
                                where=ref_values > 0))
                is_reference = cond is self.reference
                hep.histplot(
                    ratio, bins=edges, ax=ax_ratio, color=cond.color,
                    linestyle="none", histtype="errorbar", marker="_",
                    markersize=self.ratio_marker_size(edges, target),
                    markeredgewidth=2,
                    # the reference is drawn without error bars: its
                    # uncertainty is already the gray band
                    yerr=err_ratio if not is_reference else False)

        # -- common defaults (decorate() may override any of these) ----
        if last_edges is not None:
            ax_main.set_xlim(last_edges[0], last_edges[-1])
        ax_main.grid(True, linestyle="--", alpha=0.3)
        ax_ratio.grid(True, linestyle="--", alpha=0.3)
        ax_ratio.axhline(1.0, color="gray", linestyle="--", linewidth=1)
        ax_ratio.set_ylabel(f"Ratio w.r.t. {self.reference.label}",
                            fontsize=20)
        ax_ratio.set_ylim(0.0, 2.0)

        self.apply_yscale(ax_main, max_y, target)
        self.decorate(ax_main, ax_ratio, target)

        # -- legends (after decorate, see decorate() docstring) --------
        loc = self.legend_loc(target)
        header = Line2D([], [], color="none", label=r"$\bf{HLT\ Scouting}$")
        handles, labels = ax_main.get_legend_handles_labels()
        ax_main.legend(handles=[header] + handles,
                       labels=[r"$\bf{HLT\ Scouting}$"] + labels,
                       fontsize=18, loc=loc)
        ax_ratio.legend(fontsize=14, loc=loc)

        return [FigureOutput(fig=fig,
                             png_name=self.png_name(target),
                             pdf_title=self.pdf_title(target),
                             extra_pdf_name=self.extra_pdf_name(target))]


# ======================================================================
# Intermediate class 2: 2D pairwise difference maps
# ======================================================================

class DifferenceMap2D(ScoutingPlot):
    """
    Template for the four 2D scripts: for each configured (A, B) pair,
    compute a difference map, draw it with a colorbar, and add 1D
    projection panel(s) below.  One figure (page + PNG) per pair.
    """

    # ---- figure geometry as subclass DATA (differs per script) -------
    figsize = (12, 18)
    height_ratios = [4, 1, 1]     # 2D map + two projection panels
    hspace = 0.25
    subplots_adjust = None        # dict for plt.subplots_adjust, or None
    aspect_equal = False          # rel EE sets the 2D map to equal aspect
    cms_fontsize = 22             # 22 abs / 20 rel (pixel-preserved)
    cbar_fontsize = 22            # 22 abs / 20 rel EB / 18 rel EE

    #: "EB" or "EE"; set by the concrete subclass, selects axis labels
    region = None

    # ---- data access -------------------------------------------------

    def fetch(self, target):
        """
        ({label: 2D values}, (xedges, yedges)); edges taken from the
        first condition that has data.  Fewer than 2 conditions with
        data -> None (target skipped), as in the originals.
        """
        tag_data = {}
        edges = None
        for cond in self.conditions:
            data = self.source.fetch_summed(
                cond, target["subpath"], target["hist_name"])
            if data is not None:
                tag_data[cond.label] = data[0]
                if edges is None:
                    edges = (data[1], data[2])
        if edges is None or len(tag_data) < 2:
            return None
        return (tag_data, edges)

    # ---- abstract hooks (the real behavioural differences) -----------

    @abstractmethod
    def compute_diff(self, a, b):
        """The comparison quantity of the 2D map (absolute or relative
        difference)."""

    @abstractmethod
    def make_norm(self):
        """Color normalisation incl. z-limits."""

    @abstractmethod
    def draw_projections(self, proj_axes, pair, raw_pair, diff_vals,
                         edges, target):
        """
        Draw the lower projection panel(s).  A hook because the
        projection LOGIC genuinely differs -- see the subclasses.
        Receives the raw per-condition maps (`raw_pair`) precisely so
        the relative variants can implement project-THEN-divide.
        """

    @abstractmethod
    def cbar_label(self, label_a, label_b):
        """Colorbar label text."""

    @abstractmethod
    def figure_title(self, label_a, label_b, target):
        """PDF page title for one pair."""

    @abstractmethod
    def png_name(self, label_a, label_b, target):
        """PNG basename for one pair."""

    @abstractmethod
    def pair_description(self, label_a, label_b):
        """Progress-print text for one pair."""

    # ---- small hooks with defaults -----------------------------------

    def format_cbar(self, cbar):
        """Colorbar tick formatting; default no-op (the relative
        variants set a fixed-decimals formatter)."""

    def axis_labels(self, target):
        """2D-map axis labels, selected by `region`.  For EE the side
        (EE+/EE-/EE) is detected from the histogram name, verbatim from
        the originals."""
        if self.region == "EB":
            return r"RecHit EB $i\eta$", r"RecHit EB $i\phi$"
        hist_name = target["hist_name"]
        if "Plus" in hist_name:
            side = "EE+"
        elif "Minus" in hist_name:
            side = "EE-"
        else:
            side = "EE"
        return rf"RecHit {side} $ix$", rf"RecHit {side} $iy$"

    # ---- shared helpers ----------------------------------------------

    @staticmethod
    def _finish_proj(ax_p, xlim):
        """Cosmetics shared by every projection panel: zero line, grid,
        x-limits, and the switched-off dummy axes on the right that
        keeps the panel width-aligned with the 2D map + colorbar."""
        ax_p.axhline(0, color="gray", linestyle="--", linewidth=1)
        ax_p.grid(True, linestyle="--", alpha=0.3)
        ax_p.set_xlim(*xlim)
        divider = make_axes_locatable(ax_p)
        divider.append_axes("right", size="5%", pad=0.05).axis("off")

    def _make_layout(self):
        """Build the figure from the geometry class attributes."""
        fig, axes = plt.subplots(
            len(self.height_ratios), 1, figsize=self.figsize,
            gridspec_kw={"height_ratios": self.height_ratios,
                         "hspace": self.hspace})
        if self.subplots_adjust is not None:
            plt.subplots_adjust(**self.subplots_adjust)
        ax = axes[0]
        if self.aspect_equal:
            ax.set_aspect("equal")
        return fig, ax, axes[1:]

    # ---- the fixed 2D figure template --------------------------------

    def make_figures(self, target, fetched):
        tag_data, (xedges, yedges) = fetched
        outputs = []
        for label_a, label_b in self.config["diff_pairs"]:
            if label_a not in tag_data or label_b not in tag_data:
                continue
            data_a = tag_data[label_a]
            data_b = tag_data[label_b]
            diff_vals = self.compute_diff(data_a, data_b)
            print(f"   >> Plotting {self.pair_description(label_a, label_b)}")

            fig, ax, proj_axes = self._make_layout()
            self.cms_label(ax, fontsize=self.cms_fontsize)

            # 2D map + explicit colorbar via make_axes_locatable
            hep.hist2dplot(diff_vals, xbins=xedges, ybins=yedges, ax=ax,
                           cbar=False, cmap=plt.get_cmap("PiYG"),
                           norm=self.make_norm())
            xlabel, ylabel = self.axis_labels(target)
            ax.set_xlabel(xlabel, fontsize=22)
            ax.set_ylabel(ylabel, fontsize=22)

            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            cbar = fig.colorbar(ax.collections[0], cax=cax)
            cbar.set_label(self.cbar_label(label_a, label_b),
                           fontsize=self.cbar_fontsize)
            self.format_cbar(cbar)

            self.draw_projections(proj_axes, (label_a, label_b),
                                  (data_a, data_b), diff_vals,
                                  (xedges, yedges), target)

            outputs.append(FigureOutput(
                fig=fig,
                png_name=self.png_name(label_a, label_b, target),
                pdf_title=self.figure_title(label_a, label_b, target)))
        return outputs


# ----------------------------------------------------------------------
# Absolute difference maps: A - B
# ----------------------------------------------------------------------

class AbsDiffMap(DifferenceMap2D):
    """
    Absolute difference of the occupancy maps, symmetric-log color
    scale.  Projections: the diff map is projected directly
    (np.sum over one axis) -- fine because subtraction is linear.
    Used for both EB and EE via the `region` attribute of the concrete
    subclass in the entry script.
    """

    z_limit = 1000.0

    def compute_diff(self, a, b):
        return a - b

    def make_norm(self):
        return SymLogNorm(linthresh=1.0, vmin=-self.z_limit,
                          vmax=self.z_limit, base=10)

    def cbar_label(self, label_a, label_b):
        return f"Diff. in Number of RecHits ({label_a} - {label_b})"

    def figure_title(self, label_a, label_b, target):
        return f"Diff: {label_a} - {label_b}\n{target['hist_name']}"

    def png_name(self, label_a, label_b, target):
        return f"Diff_{label_a}_vs_{label_b}_{target['hist_name']}.png"

    def pair_description(self, label_a, label_b):
        return f"Diff: {label_a} - {label_b} (z-limit={self.z_limit})"

    def draw_projections(self, proj_axes, pair, raw_pair, diff_vals,
                         edges, target):
        label_a, label_b = pair
        xedges, yedges = edges
        ax_x, ax_y = proj_axes
        xlabel, ylabel = self.axis_labels(target)

        # x-axis projection (ieta resp. ix); carries the y-axis label
        proj_x = np.sum(diff_vals, axis=1)
        hep.histplot(proj_x, bins=xedges, ax=ax_x, color="black",
                     histtype="step", lw=2)
        ax_x.set_xlabel(xlabel, fontsize=22)
        ax_x.set_ylabel(
            f"Diff. in Number of RecHits ({label_a} - {label_b})",
            fontsize=20)
        self._finish_proj(ax_x, (xedges[0], xedges[-1]))

        # y-axis projection (iphi resp. iy); y-label intentionally empty
        # (shared with the panel above), as in the originals
        proj_y = np.sum(diff_vals, axis=0)
        hep.histplot(proj_y, bins=yedges, ax=ax_y, color="black",
                     histtype="step", lw=2)
        ax_y.set_xlabel(ylabel, fontsize=22)
        ax_y.set_ylabel("", fontsize=20)
        self._finish_proj(ax_y, (yedges[0], yedges[-1]))


# ----------------------------------------------------------------------
# Relative difference maps: (A - B) / B
# ----------------------------------------------------------------------

class RelDiffMap(DifferenceMap2D):
    """
    True relative difference, linear diverging color scale around 0.
    This (cartesian-projection) variant is used for EB.

    PHYSICS -- projection order: the 1D panels are the relative
    difference OF THE PROJECTIONS (sum A and B first, then divide),
    NOT the projection of the 2D relative-difference map.  These are
    mathematically different; never "unify" this with AbsDiffMap.
    """

    hspace = 0.35
    subplots_adjust = {"top": 0.92, "bottom": 0.08,
                       "left": 0.1, "right": 0.9}
    cms_fontsize = 20
    cbar_fontsize = 20

    #: color-scale half-range; set by the concrete subclass
    #: (0.08 for EB, 0.30 for EE)
    z_limit = None

    def compute_diff(self, a, b):
        # NaN where the reference B has no hits (ignored by the plot).
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(b != 0, (a - b) / b, np.nan)

    def make_norm(self):
        return TwoSlopeNorm(vcenter=0, vmin=-self.z_limit,
                            vmax=self.z_limit)

    def format_cbar(self, cbar):
        cbar.formatter = plt.FuncFormatter(lambda val, pos: f"{val:.2f}")
        cbar.update_ticks()

    def cbar_label(self, label_a, label_b):
        return f"Rel. Diff. ({label_a} - {label_b}) / {label_b}"

    def figure_title(self, label_a, label_b, target):
        return (f"Relative Difference: ({label_a} - {label_b}) / {label_b}"
                f"\n{target['hist_name']}")

    def png_name(self, label_a, label_b, target):
        return f"RelDiff_{label_a}_vs_{label_b}_{target['hist_name']}.png"

    def pair_description(self, label_a, label_b):
        return (f"True Relative Diff: "
                f"({label_a} - {label_b}) / {label_b}")

    @staticmethod
    def _rel_diff(a, b):
        """(a - b) / b with NaN where b == 0 (shared guarded divide)."""
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.where(b != 0, (a - b) / b, np.nan)

    def draw_projections(self, proj_axes, pair, raw_pair, diff_vals,
                         edges, target):
        data_a, data_b = raw_pair
        xedges, yedges = edges
        ax_x, ax_y = proj_axes
        xlabel, ylabel = self.axis_labels(target)

        # PHYSICS: sum first, then divide (see class docstring).
        for ax_p, axis, e, lab in ((ax_x, 1, xedges, xlabel),
                                   (ax_y, 0, yedges, ylabel)):
            proj_a = np.nansum(data_a, axis=axis)
            proj_b = np.nansum(data_b, axis=axis)
            rel = self._rel_diff(proj_a, proj_b)
            hep.histplot(rel, bins=e, ax=ax_p, color="black",
                         histtype="step", lw=2)
            ax_p.set_xlabel(lab, fontsize=22)
            ax_p.set_ylabel("Rel. Diff.", fontsize=20)
            self._finish_proj(ax_p, (e[0], e[-1]))


class RelDiffMapRadial(RelDiffMap):
    """
    Relative difference with a RADIAL projection around the beam axis
    instead of the cartesian x/y projections -- used for EE, where
    occupancy and radiation damage are approximately radially symmetric.
    Two-row layout (2D map + one radial panel), equal-aspect 2D map.
    """

    figsize = (8, 10)
    height_ratios = [4, 1]
    subplots_adjust = {"top": 0.92, "bottom": 0.1,
                       "left": 0.1, "right": 0.9}
    aspect_equal = True
    cbar_fontsize = 18

    #: beam-pipe position in (ix, iy) crystal coordinates
    BEAM_CENTER = (50.5, 50.5)

    def png_name(self, label_a, label_b, target):
        return (f"RelDiff_{label_a}_vs_{label_b}_"
                f"{target['hist_name']}_rad2D.png")

    def draw_projections(self, proj_axes, pair, raw_pair, diff_vals,
                         edges, target):
        data_a, data_b = raw_pair
        xedges, yedges = edges
        (ax_r,) = proj_axes

        # Radius of every (ix, iy) bin center w.r.t. the beam center;
        # radial bin width = the (ix) bin width. Verbatim port.
        ix_centers = 0.5 * (xedges[:-1] + xedges[1:])
        iy_centers = 0.5 * (yedges[:-1] + yedges[1:])
        ix_grid, iy_grid = np.meshgrid(ix_centers, iy_centers,
                                       indexing="ij")
        r_grid = np.sqrt((ix_grid - self.BEAM_CENTER[0]) ** 2
                         + (iy_grid - self.BEAM_CENTER[1]) ** 2)
        r_bin_width = np.min(np.diff(ix_centers))
        r_bins = np.arange(0, np.max(r_grid) + r_bin_width, r_bin_width)
        r_vals = r_grid.flatten()

        # PHYSICS: sum raw hits of A and B in radial bins FIRST, then
        # take the relative difference of the radial sums.
        sum_a_r, r_edges = np.histogram(r_vals, bins=r_bins,
                                        weights=data_a.flatten())
        sum_b_r, _ = np.histogram(r_vals, bins=r_bins,
                                  weights=data_b.flatten())
        rel_diff_r = self._rel_diff(sum_a_r, sum_b_r)

        hep.histplot(rel_diff_r, bins=r_edges, ax=ax_r, color="black",
                     histtype="step", lw=2)
        ax_r.set_xlabel(r"r$_{ix,iy}$", fontsize=20)
        ax_r.set_ylabel("Rel. Diff.", fontsize=20)
        self._finish_proj(ax_r, (0, 60))   # hardcoded zoom, as before
