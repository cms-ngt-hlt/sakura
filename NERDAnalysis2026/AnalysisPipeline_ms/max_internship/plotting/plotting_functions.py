"""
plotting_functions.py
=====================
Plain helper functions shared by the plotting entry scripts:

* plotting_config.yaml loading
* locating the DQM inputs (DQM_DEST_BASE) and the plot output directory
  (PLOTS_DEST, default DQM_DEST_BASE/plots) via pipeline.cfg
* the command-line options every script accepts
* run-number parsing
* the double-sided Crystal Ball (DCB) + exponential fit used by the
  Z -> ee scripts

The Scouting comparison framework (classes) lives in scouting_plot.py,
luminosity labels in luminosity.py and run selection in dqm_runs.py.
"""

import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

from luminosity import add_lumi_arguments

DEFAULT_CONFIG = "plotting_config.yaml"
DEFAULT_PIPELINE_CFG = Path(__file__).resolve().parents[1] / "pipeline.cfg"


# ======================================================================
# Configuration and output
# ======================================================================

_REQUIRED_CONFIG_KEYS = (
    "conditions", "reference", "cms_label", "dqm_prefix", "diff_pairs",
)


def load_config(config_path=DEFAULT_CONFIG):
    """Read plotting_config.yaml as a nested dict; fail loudly on missing keys."""
    with open(config_path) as fh:
        config = yaml.safe_load(fh)
    missing = [k for k in _REQUIRED_CONFIG_KEYS if k not in config]
    if missing:
        raise KeyError(
            f"Config file '{config_path}' is missing required keys: {missing}")
    if "output" in config:
        raise ValueError(
            f"Config file '{config_path}': the 'output' section is no longer "
            "used; remove it and set PLOTS_DEST in pipeline.cfg "
            "(or pass --output-dir)")
    return config


def make_output_dir(pipeline_cfg, local=False, override=None):
    """Create and return the plot output directory: --output-dir if
    given, else PLOTS_DEST from pipeline.cfg (default DQM_DEST_BASE/plots).
    --local never reads pipeline.cfg, so it needs --output-dir."""
    if override:
        path = Path(override).expanduser()
    elif local:
        raise ValueError("--local does not read pipeline.cfg, so the plot "
                         "destination is unknown: pass --output-dir")
    else:
        path = plots_dest(pipeline_cfg)
    path.mkdir(parents=True, exist_ok=True)
    return str(path)


def cms_text(config):
    """Label text next to "CMS" (cms_label.text, default Preliminary)."""
    return config["cms_label"].get("text", "Preliminary")


def lumi_csv_path(config, override=None):
    """--lumi-csv if given, else lumi_csv from the config."""
    return override or config.get("lumi_csv", "lumi_data.csv")


def condition_styles(config):
    """{label: {"folder", "color", "marker"}} in config order, for the
    scripts that do not use the ScoutingPlot classes."""
    return {
        c["label"]: {"folder": str(Path(c["path"]).expanduser()),
                     "color": c.get("color", "black"),
                     "marker": c.get("marker", "o")}
        for c in config["conditions"]
    }


# ======================================================================
# Input location (pipeline.cfg)
# ======================================================================

@lru_cache(maxsize=None)
def _read_pipeline_cfg(pipeline_cfg):
    """(directory, DQM_DEST_BASE, PLOTS_DEST) from pipeline.cfg, sourced
    with Bash from its own directory, exactly as the pipeline does."""
    cfg = Path(pipeline_cfg).expanduser().resolve()
    if not cfg.is_file():
        raise ValueError(f"Pipeline config not found: {cfg}")
    result = subprocess.run(
        ["bash", "-c", 'set -e; source "$1" >&2; '
         'printf "%s\\0%s" "${DQM_DEST_BASE:-}" "${PLOTS_DEST:-}"',
         "bash", str(cfg)],
        cwd=cfg.parent, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"Error reading {cfg}: {result.stderr.strip()}")
    dqm, plots = result.stdout.split("\0")
    return cfg, dqm.strip(), plots.strip()


def _cfg_path(cfg, value):
    """Relative pipeline.cfg paths are relative to its directory."""
    path = Path(value).expanduser()
    return path if path.is_absolute() else cfg.parent / path


def dqm_dest_base(pipeline_cfg):
    """DQM_DEST_BASE from pipeline.cfg."""
    cfg, dqm, _ = _read_pipeline_cfg(str(pipeline_cfg))
    if not dqm:
        raise ValueError(f"DQM_DEST_BASE is empty or unset in {cfg}")
    return _cfg_path(cfg, dqm)


def plots_dest(pipeline_cfg):
    """PLOTS_DEST from pipeline.cfg, or DQM_DEST_BASE/plots if unset."""
    cfg, _, plots = _read_pipeline_cfg(str(pipeline_cfg))
    return _cfg_path(cfg, plots) if plots else dqm_dest_base(pipeline_cfg) / "plots"


def scouting_input_dir(pipeline_cfg, local=False):
    """Base directory of the Scouting DQM inputs.  Prefers
    DQM_DEST_BASE/scouting; older pipelines wrote the tags directly under
    DQM_DEST_BASE.  --local uses the working directory instead."""
    if local:
        return Path.cwd()
    base = dqm_dest_base(pipeline_cfg)
    scouting = base / "scouting"
    return scouting if scouting.is_dir() else base


def hlt_input_dir(pipeline_cfg, folders, local=False):
    """Base directory of the HLT DQM inputs (DQM_DEST_BASE/hlt).  Also
    accepts the tag folders directly under DQM_DEST_BASE, or a base
    pointing at the recipe itself.  On case-insensitive filesystems the
    HLT tag also matches "hlt", hence the check for all folders first."""
    if local:
        return Path.cwd()
    base = dqm_dest_base(pipeline_cfg)
    if all((base / f).is_dir() for f in folders):
        return base
    hlt = base / "hlt"
    return hlt if hlt.is_dir() else base


# ======================================================================
# Command line
# ======================================================================

def add_common_arguments(parser):
    """Options shared by every plotting script."""
    parser.add_argument(
        "--config", default=DEFAULT_CONFIG,
        help="plotting config (default: %(default)s)")
    parser.add_argument(
        "--pipeline-cfg", default=str(DEFAULT_PIPELINE_CFG),
        help="pipeline.cfg defining DQM_DEST_BASE "
             "(default: pipeline.cfg next to the pipeline scripts; "
             "ignored with --local)")
    parser.add_argument(
        "--local", action="store_true",
        help="ignore pipeline.cfg and use condition paths from the config "
             "relative to the current working directory (needs --output-dir)")
    parser.add_argument(
        "--output-dir", default=None, metavar="DIR",
        help="where all plots are written (default: PLOTS_DEST from "
             "pipeline.cfg, else DQM_DEST_BASE/plots)")
    add_lumi_arguments(parser, default=None)


def common_kwargs(args):
    """The add_common_arguments() options as ScoutingPlot keyword args."""
    return dict(config_path=args.config, pipeline_cfg=args.pipeline_cfg,
                local=args.local, output_dir=args.output_dir,
                lumi_csv=args.lumi_csv)


# ======================================================================
# Misc
# ======================================================================

def extract_run_number(filename):
    """Run number from a DQM filename ending in _R<run>.root, else None."""
    match = re.search(r"_R(\d+)\.root", os.path.basename(filename))
    return int(match.group(1)) if match else None


# ======================================================================
# Z -> ee fit: double-sided Crystal Ball + exponential background
#   p[0], p[1]  background p0 * exp(p1 * x)
#   p[2]        signal normalisation
#   p[3], p[4]  mean, sigma
#   p[5]..p[8]  aL, nL, aH, nH (tails)
# ======================================================================

# Z -> ee inputs (HLT DQM recipe) and fit range, shared by both Z scripts
ZEE_DQM_PREFIX = "HLT/Run summary"
ZEE_HIST_SUBPATH = "ObjectMonitor/MainShifter/di-Electron_Mass"
ZEE_HIST_NAME = ZEE_HIST_SUBPATH.rsplit("/", 1)[-1]
ZEE_FIT_RANGE = (60, 120)

DCB_PAR_NAMES = ["Bkg C0", "Bkg C1", "Sig Norm", "Mean", "Sigma",
                 "aL", "nL", "aH", "nH"]


def dcb_signal(x, p):
    mean, sigma = p[3], p[4]
    aL, nL, aH, nH = abs(p[5]), p[6], abs(p[7]), p[8]
    t = (x - mean) / sigma
    if -aL < t < aH:
        return p[2] * np.exp(-0.5 * t**2)
    if t <= -aL:
        A = (nL / aL)**nL * np.exp(-0.5 * aL**2)
        B = nL / aL - aL
        return p[2] * A * (B - t)**(-nL)
    A = (nH / aH)**nH * np.exp(-0.5 * aH**2)
    B = nH / aH - aH
    return p[2] * A * (B + t)**(-nH)


def dcb_background(x, p):
    return p[0] * np.exp(p[1] * x)


def dcb_func(x, p):
    """Signal + background with the ROOT TF1 signature (x is an array)."""
    return dcb_signal(x[0], p) + dcb_background(x[0], p)


def fit_dcb(root_hist, name, fit_range=ZEE_FIT_RANGE):
    """Fit root_hist with DCB + exponential background and return the
    TF1.  Initial values and limits are derived from the histogram peak."""
    import ROOT  # only the Z -> ee scripts need PyROOT
    fit_min, fit_max = fit_range
    fit_func = ROOT.TF1(name, dcb_func, fit_min, fit_max, 9)
    peak_val = root_hist.GetMaximum()
    peak_x = root_hist.GetXaxis().GetBinCenter(root_hist.GetMaximumBin())

    fit_func.SetParameters(peak_val * 0.05, -0.04, peak_val, peak_x,
                           3.0, 1.5, 5.0, 1.5, 5.0)
    fit_func.SetParLimits(0, 0, peak_val)
    fit_func.SetParLimits(1, -0.8, 0.0)
    fit_func.SetParLimits(2, peak_val * 0.01, peak_val * 5.0)
    fit_func.SetParLimits(3, peak_x - 5.0, peak_x + 5.0)  # mean near peak
    fit_func.SetParLimits(4, 0.5, 8.0)
    fit_func.SetParLimits(5, 0.1, 10.0)
    fit_func.SetParLimits(6, 1.01, 100.0)
    fit_func.SetParLimits(7, 0.1, 10.0)
    fit_func.SetParLimits(8, 1.01, 100.0)

    # Fit options: S = return the fit result, R = use the function range,
    # L = binned log-likelihood, I = integrate the function over each bin,
    # M = run Minuit's IMPROVE step after MIGRAD, Q = quiet.
    # CAVEAT (kept as in the original scripts; changing it shifts the
    # results): with this DCB function, I and M make the fit unreliable.
    #   * M is a random search whose generator state persists within the
    #     ROOT session, so a fit depends on how many fits ran before it:
    #     the first condition fitted gets different uncertainties (e.g.
    #     sigma error 0.020 vs 0.152 for the same Prompt histogram).
    #   * I makes the minimum ill-conditioned: MIGRAD fails (status 4) or
    #     reports unreliable errors (status 1).
    # "SRLQ" converges (status 0), is independent of the fit order and
    # gives plausible uncertainties; mu/sigma move slightly (Prompt:
    # sigma 3.896 -> 3.927 GeV, mu 89.701 -> 89.691 GeV).
    root_hist.Fit(fit_func, "SRLIMQ", "", fit_min, fit_max)
    return fit_func
