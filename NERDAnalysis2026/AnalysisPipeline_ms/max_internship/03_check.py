#!/usr/bin/env python3
"""diff manifest vs EOS, parse job logs, emit report + resubmit list.

Usage: python3 03_check.py --tag NGT [--cfg pipeline.cfg]
Outputs: check_report_<TAG>.md, resubmit_<TAG>.txt, condor_resubmit_<TAG>.sub
Statuses: OK, EMPTY (0 events), FAIL (errors>0), CRASHED, NO_SUMMARY,
          PENDING (still running or not submitted),
          MISSING_OUTPUT (job fine, file(s) not on EOS).
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

# find relevant lines with regex
SUMMARY_RE = re.compile(
    r"Events total\s*=\s*(\d+)\s*passed\s*=\s*(\d+)\s*(?:errors|failed)\s*=\s*(\d+)"
)
CRASH_RE = re.compile(r"Fatal Exception|FatalRootError|segmentation|bad_alloc", re.I)


def job_status(jobdir: Path):
    """-> (status, total, passed, errors)"""
    texts = []
    for name in ("hlt.stderr", "hlt.stdout"):
        p = jobdir / name
        if p.exists():
            texts.append(p.read_text(errors="replace"))
    if not texts:
        return "PENDING", "-", "-", "-"
    m = None
    for t in texts:
        for m in SUMMARY_RE.finditer(t):
            pass                      # keep last match
        if m:
            break
    if m is None:
        if any(CRASH_RE.search(t) for t in texts):
            return "CRASHED", "-", "-", "-"
        return "NO_SUMMARY", "-", "-", "-"
    total, passed, errors = (int(g) for g in m.groups())
    if errors:
        return "FAIL", total, passed, errors
    if total == 0:
        return "EMPTY", total, passed, errors
    return "OK", total, passed, errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--cfg", default=str(HERE / "pipeline.cfg"))
    a = ap.parse_args()
    tag = a.tag

    manifest = HERE / f"manifest_{tag}.tsv"
    if not manifest.exists():
        sys.exit(f"ERROR: {manifest} not found: run 02_submit.py first")

    # manifest rows -> expected files grouped per (run, job)
    expected = defaultdict(list)          # (run, job) -> [(stream, eos_path)]
    for line in manifest.read_text().splitlines()[1:]:
        run, job, stream, eos_path, _inputs = line.split("\t")
        expected[(int(run), int(job))].append((stream, eos_path))

    # One directory listing per run dir (cheap), then set membership.
    on_eos = set()
    for run_dir in {Path(p).parent for pairs in expected.values() for _, p in pairs}:
        if run_dir.is_dir():
            on_eos.update(str(run_dir / f.name) for f in run_dir.iterdir())

    # condor still busy? -> report is provisional
    q = subprocess.run(["condor_q", "-totals", "-af", "ClusterId"],
                       capture_output=True, text=True)
    queued = len([l for l in q.stdout.splitlines() if l.strip()]) if q.returncode == 0 else 0

    counts = defaultdict(int)
    resubmit, report_rows = [], []
    for (run, job) in sorted(expected):
        jobdir = HERE / f"Jobs_{tag}" / f"run_{run}" / f"job_{job}"
        status, total, passed, errors = job_status(jobdir)
        missing = [s for s, p in expected[(run, job)] if p not in on_eos]
        if status == "OK" and missing:
            status = "MISSING_OUTPUT"
        good = status in ("OK", "EMPTY") and not missing   # EMPTY: see note below
        # With no stdout/stderr there is no evidence of failure: Condor may still
        # be running the job, or the job may not have been submitted yet.
        if not good and status != "PENDING":
            resubmit.append(str(jobdir / "job.sh"))
        counts[status] += 1
        report_rows.append(
            f"| {run} | {job} | {total} | {passed} | {errors} | {status} "
            f"| {','.join(missing) if missing else 'all'} |")

    (HERE / f"resubmit_{tag}.txt").write_text("\n".join(resubmit) + ("\n" if resubmit else ""))

    # identical .sub, queue from the resubmit list (architecture decision 3)
    base_sub = (HERE / f"condor_{tag}.sub").read_text().splitlines()
    resub = [l for l in base_sub if not l.startswith("queue")]
    resub.append(f"queue jobscript from {HERE}/resubmit_{tag}.txt")
    (HERE / f"condor_resubmit_{tag}.sub").write_text("\n".join(resub) + "\n")

    lines = [f"# Check report: {tag}", ""]
    if queued:
        lines += [f"> **WARNING:** ~{queued} job(s) still in condor_q: provisional report.", ""]
    lines += ["| Run | Job | Total | Passed | Errors | Status | on EOS |",
              "|---:|---:|---:|---:|---:|:--|:--|"] + report_rows + [
        "",
        "**Totals:** " + " · ".join(f"{v} {k}" for k, v in sorted(counts.items())),
        f"**To resubmit:** {len(resubmit)} job(s) -> resubmit_{tag}.txt",
        "",
        "NOTE: EMPTY (ran, 0 events) counts as done - a 0-event chunk is possible "
    ]
    (HERE / f"check_report_{tag}.md").write_text("\n".join(lines) + "\n")

    print(f"[{tag}] " + " · ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    if resubmit:
        print(f"{len(resubmit)} job(s) to redo ->  condor_submit condor_resubmit_{tag}.sub")
    else:
        print("No failed jobs to resubmit.")
    if counts["PENDING"]:
        print(f"{counts['PENDING']} job(s) are either still running or have not been submitted.")


if __name__ == "__main__":
    main()

