"""Muon eta/phi differences, adapted from CMS-DP-2026/028/FinalPlots.

Scouting TProfile2D means are pooled using fBinEntries (sum of weights).
HLT TH2 occupancies are summed across runs and PDG IDs +13/-13.
"""
import argparse
from pathlib import Path
import re
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import Normalize
import mplhep as hep
import numpy as np
import uproot
import yaml

SCOUTING_NAMES = {
    coll: f"{coll}_nTrackerLayersWithMeasurement_vs_eta_phi_prof"
    for coll in ("MuonNoVtx", "MuonVtx")
}
HLT_FOLDER = "FourVectorHLT/hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered"


def input_base(config_path, recipe):
    cfg = Path(config_path).expanduser().resolve()
    if not cfg.is_file():
        raise ValueError(f"Pipeline config not found: {cfg}")
    result = subprocess.run(
        ["bash", "-c", 'set -e; source "$1" >&2; printf "%s" "${DQM_DEST_BASE:-}"',
         "bash", str(cfg)], cwd=cfg.parent, capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"Error reading {cfg}: {result.stderr.strip()}")
    if not result.stdout.strip():
        raise ValueError(f"DQM_DEST_BASE is empty in {cfg}; set it or use --local")
    base = Path(result.stdout).expanduser()
    if not base.is_absolute():
        base = cfg.parent / base
    if recipe == "hlt" and all((base / tag).is_dir() for tag in ("HLT", "NGT", "Prompt")):
        return base  # also works on case-insensitive filesystems
    return base / recipe if (base / recipe).is_dir() else base


def read_map(hist, profile):
    values = np.asarray(hist.values(flow=False), dtype=float)
    if values.ndim != 2:
        raise ValueError(f"Expected a 2D histogram, got {hist.classname}")
    edges = tuple(np.asarray(axis.edges()) for axis in hist.axes)
    if profile:
        if hist.classname != "TProfile2D":
            raise ValueError(f"Expected TProfile2D, got {hist.classname}")
        # ROOT global bin order has x varying fastest, including flow bins.
        weights = np.asarray(hist.member("fBinEntries"), dtype=float)
        weights = weights.reshape(values.shape[1] + 2, values.shape[0] + 2).T[1:-1, 1:-1]
        numerator = np.zeros_like(values)
        np.multiply(values, weights, out=numerator, where=weights != 0)
        return numerator, weights.copy(), edges
    if not hist.classname.startswith("TH2"):
        raise ValueError(f"Expected TH2 occupancy, got {hist.classname}")
    return values.copy(), None, edges


def merge(left, right):
    if left is None:
        return right
    if any(not np.array_equal(a, b) for a, b in zip(left[2], right[2])):
        raise ValueError("Incompatible bin edges; refusing to merge maps")
    if (left[1] is None) != (right[1] is None):
        raise ValueError("Cannot mix profiles and occupancy maps")
    return (left[0] + right[0], None if left[1] is None else left[1] + right[1], left[2])


def mean_or_counts(data):
    numerator, weights, _ = data
    if weights is None:
        return numerator
    return np.divide(numerator, weights, out=np.full_like(numerator, np.nan), where=weights != 0)


def load_maps(files, mode, prefix, target_folder):
    maps = {}
    for filename in files:
        with uproot.open(filename) as root:
            if "DQMData" not in root:
                raise ValueError(f"No DQMData directory in {filename}")
            runs = [k for k in root["DQMData"].keys(cycle=False, recursive=False) if k.startswith("Run ")]
            for run in runs:
                stem = f"DQMData/{run}/HLT/Run summary"
                if mode == "scouting":
                    candidates = ([prefix] if prefix else ["ScoutingOffline", "ScoutingOnline"])
                    for collection, name in SCOUTING_NAMES.items():
                        # Prefer Offline, use Online only when the target is absent.
                        key = next((f"{stem}/{p}/Muons/Properties/{name}" for p in candidates
                                    if f"{stem}/{p}/Muons/Properties/{name}" in root), None)
                        if key:
                            maps[collection] = merge(maps.get(collection), read_map(root[key], True))
                else:
                    path = f"{stem}/{target_folder.strip('/')}"
                    if path not in root:
                        continue
                    directory = root[path]
                    for name, cls in directory.classnames(cycle=False, recursive=False).items():
                        if "etaphi" not in name.lower() or not cls.startswith("TH2"):
                            continue
                        # PDG IDs must be standalone numeric tokens, not part of 130, etc.
                        if not re.search(r"(?<!\d)-?13(?!\d)", name):
                            continue
                        base = re.sub(r"(?<!\d)-?13(?!\d)", "", name)
                        base = re.sub(r"_+", "_", base).strip("_")
                        maps[base] = merge(maps.get(base), read_map(directory[name], False))
    if mode == "scouting" and all(c in maps for c in SCOUTING_NAMES):
        maps["Combined"] = merge(maps["MuonVtx"], maps["MuonNoVtx"])
    return maps


def render(all_maps, pairs, config, mode, outdir, z_limit):
    common = sorted(set.union(*(set(m) for m in all_maps.values())))
    pages = []
    for name in common:
        differences = []
        for a, b in pairs:
            if name not in all_maps[a] or name not in all_maps[b]:
                print(f"Warning: skipping {name}: missing data for {a} or {b}")
                continue
            first, second = all_maps[a][name], all_maps[b][name]
            if any(not np.array_equal(x, y) for x, y in zip(first[2], second[2])):
                raise ValueError(f"Incompatible bin edges for {name}: {a} and {b}")
            diff = mean_or_counts(first) - mean_or_counts(second)
            if not np.any(np.isfinite(diff)):
                print(f"Warning: skipping {name}, {a} - {b}: no bins with data in both profiles")
                continue
            differences.append((a, b, diff, first[2]))
        if differences:
            limit = z_limit or (4.0 if mode == "scouting" else
                               max(float(np.nanmax(np.abs(d[2]))) for d in differences) or 1.0)
            pages.append((name, differences, limit))
    if not pages:
        raise ValueError("No comparable muon maps found. Check inputs and DQM folder (use --list).")
    outdir.mkdir(parents=True, exist_ok=True)
    pdf_path = outdir / f"Muon_{mode}_2D_differences.pdf"
    plt.style.use(hep.style.CMS)
    with PdfPages(pdf_path) as pdf:
        for name, differences, limit in pages:
            for a, b, diff, edges in differences:
                fig, ax = plt.subplots(figsize=(10, 10))
                mesh = ax.pcolormesh(*edges, np.ma.masked_invalid(diff.T),
                                     cmap="PiYG", norm=Normalize(-limit, limit), shading="flat")
                cbar = fig.colorbar(mesh, ax=ax, extend="both")
                quantity = "Mean tracker layers with measurements" if mode == "scouting" else "Muon entries"
                cbar.set_label(f"{quantity}: {a} − {b}", fontsize=16)
                ax.set_xlabel(r"Muon $\eta$")
                ax.set_ylabel(r"Muon $\phi$")
                label = config.get("cms_label", {})
                hep.cms.label(ax=ax, data=True, label="Private Work (CMS data)",
                              year=label.get("year"), lumi=label.get("lumi"),
                              com=label.get("com", 13.6), fontsize=18)
                fig.suptitle(name + (" (pooled profile)" if name == "Combined" and mode == "scouting" else ""), fontsize=15)
                safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{name}_{a}_vs_{b}")
                fig.savefig(outdir / f"{mode}_{safe}.png", dpi=150, bbox_inches="tight")
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)
    print(f"Saved {sum(len(p[1]) for p in pages)} maps and {pdf_path}")


def main(mode):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--pipeline-cfg", default=str(Path(__file__).resolve().parents[1] / "pipeline.cfg"))
    parser.add_argument("--local", action="store_true", help="use config condition paths relative to cwd; ignore pipeline.cfg")
    parser.add_argument("--output-dir", help="default: output.png_dir (png/)")
    parser.add_argument("--pair", nargs=2, action="append", metavar=("A", "B"), help="plot A-B; repeatable; default NGT-Prompt and NGT-HLT")
    parser.add_argument("--z-limit", type=float, help="symmetric colour half-range; default 4 for Scouting, automatic for HLT")
    parser.add_argument("--list", action="store_true", help="list loaded map names without plotting")
    if mode == "scouting":
        parser.add_argument("--scouting-prefix", choices=["ScoutingOffline", "ScoutingOnline"], help="default: prefer Offline, fall back to Online per histogram")
    else:
        parser.add_argument("--target-folder", default=HLT_FOLDER, help="path relative to HLT/Run summary")
    args = parser.parse_args()
    try:
        if args.z_limit is not None and (not np.isfinite(args.z_limit) or args.z_limit <= 0):
            raise ValueError("--z-limit must be finite and positive")
        with open(args.config) as stream:
            config = yaml.safe_load(stream)
        pairs = args.pair or [("NGT", "Prompt"), ("NGT", "HLT")]
        conditions = {c["label"]: c["path"] for c in config["conditions"]}
        needed = sorted({label for pair in pairs for label in pair})
        if any(label not in conditions for label in needed):
            raise ValueError("Pair labels must match conditions in config.yaml")
        base = Path.cwd() if args.local else input_base(args.pipeline_cfg, mode)
        all_maps = {}
        for label in needed:
            folder = base / Path(conditions[label]).expanduser()
            files = sorted(folder.glob("*.root"))
            if not files:
                raise ValueError(f"No ROOT files for {label} in {folder}")
            print(f"{label}: reading {len(files)} files from {folder}")
            all_maps[label] = load_maps(files, mode, getattr(args, "scouting_prefix", None), getattr(args, "target_folder", None))
            print(f"{label}: {', '.join(sorted(all_maps[label])) or 'no matching maps'}")
        if not args.list:
            outdir = Path(args.output_dir or config.get("output", {}).get("png_dir", "png"))
            render(all_maps, pairs, config, mode, outdir, args.z_limit)
    except (ValueError, OSError, KeyError) as exc:
        parser.error(str(exc))
