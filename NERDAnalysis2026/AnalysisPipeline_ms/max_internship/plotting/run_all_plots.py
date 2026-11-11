#!/usr/bin/env python3
"""Run every plotting script with the same config, inputs and output directory.

The common options (--config, --pipeline-cfg, --local, --output-dir,
--lumi-csv) are passed to every script.  The Z -> ee fit scripts need PyROOT;
without it they are skipped with a warning.  A failing script does not stop
the others; the summary at the end lists what failed and the exit code is
non-zero if anything did.

Examples:
  python3 run_all_plots.py
  python3 run_all_plots.py --local --output-dir /path/to/plots --jobs 4
  python3 run_all_plots.py --only all_1D_ScoutingDQM Z_to_ee_fit
"""
import argparse
import importlib.util
import subprocess
import sys
import time
from pathlib import Path

from plotting_functions import add_common_arguments

HERE = Path(__file__).resolve().parent

SCOUTING_SCRIPTS = [
    "variables_ScoutingECALRecHits",
    "eta_ScoutingElectron_ScoutingPhoton",
    "invariantMass_ScoutingDielectron",
    "invariantMassPiZero_PF_ScoutingDiphotons",
    "absolute_difference_ieta_iphi_NGT_HLT_ScoutingRecHitsBarrel",
    "absolute_difference_ix_iy_NGT_HLT_ScoutingRecHitsEndcapPlus",
    "relative_difference_ieta_iphi_NGT_HLT_ScoutingRecHitsBarrel",
    "relative_difference_ix_iy_NGT_HLT_ScoutingRecHitsEndcapPlus",
    "all_1D_ScoutingDQM",
    "sanity_check_event_counter",
]
ROOT_SCRIPTS = [
    "Z_to_ee_fit",
    "Z_to_ee_fit_stability_per_fill",
]


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    add_common_arguments(parser)
    parser.add_argument("--jobs", "-j", type=int, default=None, metavar="N",
                        help="parallel processes for all_1D_ScoutingDQM.py "
                             "(default: its own default, all cores)")
    parser.add_argument("--only", nargs="+", metavar="SCRIPT",
                        choices=SCOUTING_SCRIPTS + ROOT_SCRIPTS,
                        help="run only these scripts (names without .py)")
    parser.add_argument("--skip", nargs="+", default=[], metavar="SCRIPT",
                        choices=SCOUTING_SCRIPTS + ROOT_SCRIPTS,
                        help="skip these scripts (names without .py)")
    args = parser.parse_args()
    if args.local and not args.output_dir:
        parser.error("--local does not read pipeline.cfg: pass --output-dir")

    common = ["--config", args.config, "--pipeline-cfg", args.pipeline_cfg]
    if args.local:
        common.append("--local")
    if args.output_dir:
        common += ["--output-dir", args.output_dir]
    if args.lumi_csv:
        common += ["--lumi-csv", args.lumi_csv]

    scripts = [s for s in (args.only or SCOUTING_SCRIPTS + ROOT_SCRIPTS)
               if s not in args.skip]
    have_root = importlib.util.find_spec("ROOT") is not None

    failed, skipped = [], []
    for name in scripts:
        if name in ROOT_SCRIPTS and not have_root:
            print(f"[Warning] Skipping {name}.py: PyROOT (import ROOT) not available")
            skipped.append(name)
            continue
        cmd = [sys.executable, str(HERE / f"{name}.py")] + common
        if name == "all_1D_ScoutingDQM" and args.jobs is not None:
            cmd += ["--jobs", str(args.jobs)]
        print(f"\n===== {name}.py =====", flush=True)
        t0 = time.time()
        code = subprocess.call(cmd)
        print(f"===== {name}.py: {'OK' if code == 0 else f'FAILED ({code})'}, "
              f"{time.time() - t0:.0f} s =====", flush=True)
        if code:
            failed.append(name)

    n_ok = len(scripts) - len(failed) - len(skipped)
    print(f"\nSummary: {n_ok} succeeded, {len(failed)} failed, {len(skipped)} skipped")
    for name in failed:
        print(f"  FAILED : {name}.py")
    for name in skipped:
        print(f"  SKIPPED: {name}.py")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
