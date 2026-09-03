#!/usr/bin/env python3
"""this script generates condor jobs for one tag.

Usage:
    python3 02_submit.py --tag NGT [--cfg pipeline.cfg] [--force]
Then submit manually with the printed condor_submit command.
"""
import argparse
import importlib.util
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


# acessing/reading pipeline.cfg
def _bash(cfg, expr):
    r = subprocess.run(["bash", "-c", f'set -e; source "{cfg}"; {expr}'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR reading {cfg}: {r.stderr.strip()}")
    return r.stdout.rstrip("\n")

def cfg_scalar(cfg, name):
    return _bash(cfg, f'printf "%s" "${{{name}}}"')

def cfg_array(cfg, name):
    out = _bash(cfg, f'printf "%s\\n" "${{{name}[@]}}"')
    return [l for l in out.split("\n") if l]


def load_process(dump_path):
    spec = importlib.util.spec_from_file_location("pycfg", dump_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # requires cmsenv (imports FWCore)
    return mod.process


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield i // n, lst[i:i + n]


def write_job_sh(path, jobdir, cmssw_src, streams, local_files, eos_xrd, eos_paths, proxy_abs_path):
    """Wrapper run on the worker node. Exit codes:
    1 = cmsRun failed, 2 = expected output missing, 3 = stage-out copy failed."""
    lines = [
        "#!/bin/bash",
        "set -uo pipefail",   # NOT -e: phases handle their own exit codes
        'cd "${TMPDIR:-/tmp}"',
        "mkdir -p work_$$ && cd work_$$",
        f'cp "{jobdir}/run_cfg.py" .',
        f'cd "{cmssw_src}" && eval "$(scramv1 runtime -sh)" && cd - >/dev/null',
        f'export X509_USER_PROXY="{proxy_abs_path}"',

        'echo "=== PROXY DEBUG START ==="',
        'echo "Looking for proxy at: $X509_USER_PROXY"',
        'ls -la "$X509_USER_PROXY" || echo "[ERROR] Worker node cannot read the proxy file from AFS!"',
        'voms-proxy-info -all -file "$X509_USER_PROXY" || echo "[ERROR] Proxy is invalid or unreadable!"',
        'echo "=== PROXY DEBUG END ==="',
        'export X509_CERT_DIR=/cvmfs/grid.cern.ch/etc/grid-security/certificates',
        "cmsRun run_cfg.py 2> /dev/null",
        "rc=$?",
        "echo \"--- files in workdir after cmsRun (exit $rc) ---\"",
        "ls -la",
        '[ "$rc" -eq 0 ] || exit 1',
    ]
    for stream, local, eos_path in zip(streams, local_files, eos_paths):
        lines += [
            f'[ -f "{local}" ] || {{ echo "MISSING expected output {local} ({stream})"; exit 2; }}',
            f'xrdcp -f "{local}" "{eos_xrd}//{eos_path}" || {{ echo "STAGE-OUT FAILED {stream}"; exit 3; }}',
        ]
    lines += ["echo JOB_DONE_OK", "exit 0"]
    path.write_text("\n".join(lines) + "\n")
    path.chmod(0o755)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cfg", default=str(HERE / "pipeline.cfg"))
    ap.add_argument("--force", action="store_true",
                    help="delete an existing Jobs_<TAG> tree first")
    a = ap.parse_args()
    cfg, tag = a.cfg, a.tag
    print(f"Creating jobs for tag {tag}...", flush=True)

    tags = cfg_array(cfg, "TAGS")
    if tag not in tags:
        sys.exit(f"ERROR: tag {tag!r} not in TAGS={tags}")
    gtags = cfg_array(cfg, "GTAGS")
    gt = gtags[tags.index(tag)] # looking up the globaltag for the globaltag (sic)


    filelist = Path(cfg_scalar(cfg, "FILELIST"))
    eos_base = cfg_scalar(cfg, "EOS_BASE")
    eos_xrd = cfg_scalar(cfg, "EOS_XRD")
    streams = cfg_array(cfg, "STREAMS")
    local_files = cfg_array(cfg, "LOCAL_FILES")
    n_per_job = int(cfg_scalar(cfg, "N_PER_JOB"))
    flavour = cfg_scalar(cfg, "JOB_FLAVOUR")
    req_mem = cfg_scalar(cfg, "REQUEST_MEMORY_MB")
    proxy = cfg_scalar(cfg, "PROXY")
    cmssw_src = cfg_scalar(cfg, "CMSSW_SRC")
    assert len(streams) == len(local_files), "STREAMS/LOCAL_FILES length mismatch"

    dump = HERE / "configs" / f"hltDataDump.py"
    if not dump.exists():
        sys.exit(f"ERROR: {dump} not found: run 01_make_configs.sh first")

    jobs_root = HERE / f"Jobs_{tag}"
    if jobs_root.exists():
        if not a.force:
            sys.exit(f"ERROR: {jobs_root} exists. Use --force to regenerate "
                     f"(this deletes local job dirs and logs, NOT EOS outputs).")
        shutil.rmtree(jobs_root)

    # Flat filelist -> grouped by run, parsed from the LFN's /000/RRR/RRR/ segment
    if not filelist.exists():
        sys.exit(f"ERROR: {filelist} not found")
    print(f"Reading input files from {filelist}...", flush=True)
    RUN_RE = re.compile(r"/000/(\d{3})/(\d{3})/")
    run_lists = defaultdict(list)
    for line in filelist.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        m = RUN_RE.search(line)
        if not m:
            sys.exit(f"ERROR: could not parse run number from line: {line}")
        run = int(m.group(1) + m.group(2))
        run_lists[run].append(line)
    if not run_lists:
        sys.exit(f"ERROR: no files parsed from {filelist}")
    parsed_files = sum(len(files) for files in run_lists.values())
    print(f"Found {parsed_files} input files across {len(run_lists)} runs.",
          flush=True)

    print(f"Loading CMSSW configuration {dump}...", flush=True)
    process = load_process(str(dump))
    process.GlobalTag.globaltag = gt # now we set the correct globaltag in the dump that was prev. an empty string
    print(f"CMSSW configuration loaded; GlobalTag set to {gt}.", flush=True)

    snapshots = {}
    if tag == "NGT":
        oms_csv = HERE / "oms_runs.csv"
        if not oms_csv.exists():
            sys.exit(f"ERROR: {oms_csv} not found :( (needed for NGT Snapshot time)")
        for line in oms_csv.read_text().splitlines()[1:]:
            f = line.split(",")
            snapshots[int(f[0])] = f[5].strip()

    manifest_rows, job_scripts = [], []
    n_files_total = 0
    sorted_runs = sorted(run_lists.items())
    for run, files in sorted_runs:
        n_files_total += len(files)
        jobs_before_run = len(job_scripts)
        eos_run_dir = f"{eos_base}/{tag}/run_{run}"
        os.makedirs(eos_run_dir, exist_ok=True)
        if tag == "NGT":
            if run not in snapshots:
                sys.exit(f"ERROR: no snapshot time for run {run} in oms_runs.csv")
            process.GlobalTag.snapshotTime = snapshots[run]
        for k, chunk in chunks(files, n_per_job):
            jobdir = jobs_root / f"run_{run}" / f"job_{k}"
            jobdir.mkdir(parents=True)

            xrootd_prefix = "root://cms-xrd-global.cern.ch/"
            process.source.fileNames = [
                    xrootd_prefix + filename
                    for filename in chunk
            ]
           # process.source.fileNames = chunk
            (jobdir / "run_cfg.py").write_text(process.dumpPython())

            eos_paths = [f"{eos_run_dir}/{tag}_run{run}_job{k}_{s}.root" for s in streams]
            proxy_abs_path = HERE / proxy

            write_job_sh(jobdir / "job.sh", str(jobdir), cmssw_src,
                         streams, local_files, eos_xrd, eos_paths, str(proxy_abs_path))
            job_scripts.append(str(jobdir / "job.sh"))
            for s, ep in zip(streams, eos_paths):
                manifest_rows.append(f"{run}\t{k}\t{s}\t{ep}\t{';'.join(chunk)}")
        jobs_created = len(job_scripts) - jobs_before_run
        print(f"Finished run {run}: created {jobs_created} jobs "
              f"from {len(files)} input files.", flush=True)

    print("Writing manifest and Condor submission files...", flush=True)
    (HERE / f"manifest_{tag}.tsv").write_text(
        "run\tjob\tstream\teos_path\tinputs\n" + "\n".join(manifest_rows) + "\n")
    (HERE / f"jobs_to_run_{tag}.txt").write_text("\n".join(job_scripts) + "\n")

    sub = "\n".join([
        "executable = $(jobscript)",
        "output = $Fp(jobscript)hlt.stdout",
        "error  = $Fp(jobscript)hlt.stderr",
        "log    = $Fp(jobscript)hlt.log",
        f"request_memory = {req_mem}",
        f'+JobFlavour = "{flavour}"',
        f"queue jobscript from {HERE}/jobs_to_run_{tag}.txt",
    ]) + "\n"
    (HERE / f"condor_{tag}.sub").write_text(sub)

    print(f"[{tag}] {len(run_lists)} runs, {n_files_total} files -> "
          f"{len(job_scripts)} jobs ({len(manifest_rows)} expected output files).")
    print(f"Manifest: manifest_{tag}.tsv")
    print(f"Check proxy first:  voms-proxy-info -timeleft   (proxy: {proxy})")
    print(f"Submit with:        condor_submit condor_{tag}.sub")


if __name__ == "__main__":
    main()
