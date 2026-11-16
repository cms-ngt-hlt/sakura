#!/usr/bin/env python3
"""
Latency of condition uploads with respect to the CMS run: the NGT-demonstrator
tags, plus two prompt/PCL tags for comparison.

Inputs (parent directory):
  runs.txt                          run number, start, end   (CMS run registry dump)
  <tag dump>.txt                    since (run [: lumi]), insertion time, payload hash, type
                                    (conddb listTags dump; see WORKFLOWS)

For every (workflow, run) the uploads are collapsed to two records,

    FIRST upload : the earliest insertion time of a payload whose since is that run
    LAST  upload : the latest  insertion time of a payload whose since is that run

and each is referenced to both run boundaries:

    from_start_h = insertion - run start        (how old is the oldest data used)
    from_end_h   = insertion - run end          (negative = delivered while the run
                                                 was still going on)

Outputs (analysis/out/):
  uploads_<wf>.csv     every upload with run start/end and both latencies
  perrun_<wf>.csv      one row per run: n uploads, first/last, latencies, cadence
  perrun_all.csv       the three workflows stacked
  summary.csv          per-workflow x {first,last} x {start,end} statistics
  summary.json         same + run inventory + dropped uploads
  dropped.csv          uploads outside the sanity window (listed, not analysed)
  perls_<wf>.csv       by-LS tags only: latency of every lumisection's condition
"""

import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")

WORKFLOWS = {
    "BeamSpot": "BeamSpot_NGTDemonstrator.txt",
    "EcalPedestals": "EcalPedestals_NGTDemonstrator.txt",
    "SiStripQuality": "SiStripQuality_NGTDemonstrator.txt",
    "SiStripDetVOff": "SiStripDetVOff_NGTDemonstrator.txt",
    "EcalLaserAPDPNRatios": "EcalLaserAPDPNRatios_prompt_v3_inRunLSIoVs.txt",
    "SiPixelAliHLTHGCombined": "SiPixelAliHLTHGCombined_PCL_v0_hlt.txt",
}
# Tags filled by the NGT demonstrator loop; the others are prompt / PCL tags
# kept for comparison.  "NGT" in the summaries is the union of these.
DEMONSTRATOR = ["BeamSpot", "EcalPedestals", "SiStripQuality", "SiStripDetVOff"]

# Sanity window on (insertion - run end).  Uploads later than MAX_H after the run
# are not produced by the demonstrator loop on that run's data (tag bootstraps,
# manual re-uploads weeks later); they are listed in dropped.csv.  Same value as
# the PCL analysis in NGT/3.4/db/stitch so the two are comparable.
MAX_H = 48.0
# The latency budgets of the demonstrator (h).
BUDGETS = {"Tiny": 1.0, "Small": 3.0, "Medium": 6.0, "Large": 12.0}

ANSI = re.compile(r"\x1b\[[0-9;]*m")
UPLOAD_RE = re.compile(
    r"(\d+)\s*(?::\s*(\d+)\s*\((\d+)\))?\s+"       # run [: lumi (rawSince)]
    r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\s+"          # insertion time
    r"([0-9a-f]{40})\s+(\S+)"                      # payload hash, object type
)


def clean(line):
    return ANSI.sub("", line).strip()


def load_runs():
    rows = []
    with open(os.path.join(DATA, "runs.txt")) as fh:
        for line in fh:
            line = clean(line)
            if not line or line.startswith(("Run_number", "---")):
                continue
            p = line.split()
            if len(p) < 5:
                continue
            rows.append((int(p[0]), p[1] + " " + p[2], p[3] + " " + p[4]))
    runs = pd.DataFrame(rows, columns=["run", "start", "end"])
    runs["start"] = pd.to_datetime(runs["start"], format="ISO8601")
    runs["end"] = pd.to_datetime(runs["end"], format="ISO8601")
    runs["duration_h"] = (runs["end"] - runs["start"]).dt.total_seconds() / 3600.0
    return runs.drop_duplicates("run").reset_index(drop=True)


def load_uploads(wf, fname):
    rows = []
    with open(os.path.join(DATA, fname)) as fh:
        for line in fh:
            line = clean(line)
            if not line or "Insertion" in line or line.startswith("---"):
                continue
            m = UPLOAD_RE.match(line)
            if not m:
                print(f"!! {fname}: cannot parse: {line[:80]}", file=sys.stderr)
                continue
            rows.append(
                dict(
                    workflow=wf,
                    run=int(m.group(1)),
                    lumi=int(m.group(2)) if m.group(2) else np.nan,
                    inserted=pd.Timestamp(m.group(4)),
                    payload=m.group(5),
                    object_type=m.group(6),
                )
            )
    return pd.DataFrame(rows)


def attach_runs(up, runs):
    m = up.merge(runs[["run", "start", "end", "duration_h"]], on="run", how="left")
    m["in_registry"] = m["start"].notna()
    m["from_start_h"] = (m["inserted"] - m["start"]).dt.total_seconds() / 3600.0
    m["from_end_h"] = (m["inserted"] - m["end"]).dt.total_seconds() / 3600.0
    m["dropped"] = (~m["in_registry"]) | (m["from_end_h"] >= MAX_H) | (m["from_start_h"] < 0)
    return m


def per_run(m):
    """One record per run: first and last upload plus cadence figures."""
    g = m[~m["dropped"]].sort_values("inserted").groupby("run")
    rows = []
    for run, d in g:
        t = d["inserted"].drop_duplicates().sort_values()
        gaps = t.diff().dt.total_seconds().dropna() / 60.0  # minutes
        first, last = d["inserted"].min(), d["inserted"].max()
        start, end = d["start"].iloc[0], d["end"].iloc[0]
        rows.append(
            dict(
                workflow=d["workflow"].iloc[0],
                run=run,
                start=start,
                end=end,
                duration_h=d["duration_h"].iloc[0],
                n_uploads=len(d),
                n_distinct_payloads=d["payload"].nunique(),
                n_lumis=d["lumi"].nunique() if d["lumi"].notna().any() else np.nan,
                first=first,
                last=last,
                first_from_start_h=(first - start).total_seconds() / 3600.0,
                first_from_end_h=(first - end).total_seconds() / 3600.0,
                last_from_start_h=(last - start).total_seconds() / 3600.0,
                last_from_end_h=(last - end).total_seconds() / 3600.0,
                span_h=(last - first).total_seconds() / 3600.0,
                cadence_median_min=float(gaps.median()) if len(gaps) else np.nan,
                n_during_run=int((d["inserted"] <= end).sum()),
                n_dropped=int(m[(m["run"] == run) & m["dropped"]].shape[0]),
            )
        )
    return pd.DataFrame(rows)


# One CMS lumisection = 2^18 LHC orbits x 88.924 us = 23.31 s
LS_SECONDS = 2**18 * 88.924e-6


def per_lumisection(up):
    """Beam spot only: latency of each lumisection's condition.

    The since of a by-LS payload is (run, LS).  The LS is taken to be acquired
    at  run start + LS * 23.31 s  (end of that lumisection).  When the same
    (run, LS) received several payloads the FIRST upload is used.
    """
    d = up[up["lumi"].notna()].sort_values("inserted")
    n_all = d.groupby(["run", "lumi"]).size().rename("n_uploads_for_ls")
    f = d.groupby(["run", "lumi"], as_index=False).first()
    f = f.merge(n_all, on=["run", "lumi"])
    f["lumi"] = f["lumi"].astype(int)
    f["ls_time"] = f["start"] + pd.to_timedelta(f["lumi"] * LS_SECONDS, unit="s")
    f["ls_from_start_h"] = (f["ls_time"] - f["start"]).dt.total_seconds() / 3600.0
    f["latency_h"] = (f["inserted"] - f["ls_time"]).dt.total_seconds() / 3600.0
    f["upload_from_start_h"] = (f["inserted"] - f["start"]).dt.total_seconds() / 3600.0
    f["upload_from_end_h"] = (f["inserted"] - f["end"]).dt.total_seconds() / 3600.0
    cols = ["workflow", "run", "lumi", "start", "end", "duration_h", "ls_time",
            "ls_from_start_h", "inserted", "payload", "n_uploads_for_ls",
            "latency_h", "upload_from_start_h", "upload_from_end_h"]
    return f[cols].sort_values(["run", "lumi"]).reset_index(drop=True)


def q(x, p):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    return float(np.percentile(x, p)) if len(x) else float("nan")


def stats(v, label_prefix=""):
    v = pd.Series(v).dropna()
    s = {
        "n": int(len(v)),
        "median_h": float(v.median()),
        "mean_h": float(v.mean()),
        "std_h": float(v.std(ddof=0)),
        "p16_h": q(v, 16),
        "p84_h": q(v, 84),
        "p95_h": q(v, 95),
        "min_h": float(v.min()),
        "max_h": float(v.max()),
        "frac_before_zero": float((v <= 0).mean()),
    }
    for name, b in BUDGETS.items():
        s[f"frac_within_{name}"] = float((v <= b).mean())
    return {label_prefix + k: val for k, val in s.items()}


def summarize(pr):
    rows = []
    groups = [(wf, pr[pr["workflow"] == wf]) for wf in WORKFLOWS if wf in set(pr["workflow"])]
    groups.append(("NGT", pr[pr["workflow"].isin(DEMONSTRATOR)]))
    for wf, d in groups:
        for which in ("first", "last"):
            for ref in ("start", "end"):
                r = dict(workflow=wf, upload=which, reference=ref)
                r.update(stats(d[f"{which}_from_{ref}_h"]))
                r["n_runs"] = int(len(d))
                r["n_uploads"] = int(d["n_uploads"].sum())
                r["uploads_per_run_median"] = float(d["n_uploads"].median())
                r["run_duration_median_h"] = float(d["duration_h"].median())
                r["span_median_h"] = float(d["span_h"].median())
                r["cadence_median_min"] = float(d["cadence_median_min"].median())
                rows.append(r)
    return pd.DataFrame(rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    runs = load_runs()
    report = {
        "runs_registry": {
            "n": int(len(runs)),
            "run_range": [int(runs["run"].min()), int(runs["run"].max())],
            "time_range": [str(runs["start"].min()), str(runs["end"].max())],
        },
        "max_h": MAX_H,
        "budgets_h": BUDGETS,
        "workflows": {},
    }

    all_pr, all_dropped = [], []
    for wf, fname in WORKFLOWS.items():
        up = attach_runs(load_uploads(wf, fname), runs)
        up.to_csv(os.path.join(OUT, f"uploads_{wf}.csv"), index=False)
        pr = per_run(up)
        pr.to_csv(os.path.join(OUT, f"perrun_{wf}.csv"), index=False)
        all_pr.append(pr)
        dropped = up[up["dropped"]].copy()
        all_dropped.append(dropped)

        report["workflows"][wf] = {
            "file": fname,
            "object_type": up["object_type"].iloc[0],
            "n_uploads": int(len(up)),
            "n_runs_in_file": int(up["run"].nunique()),
            "n_uploads_used": int((~up["dropped"]).sum()),
            "n_runs_used": int(len(pr)),
            "n_uploads_dropped": int(len(dropped)),
            "dropped_reasons": {
                "run_not_in_registry": int((~up["in_registry"]).sum()),
                f"later_than_{MAX_H:.0f}h_after_run_end": int(
                    (up["in_registry"] & (up["from_end_h"] >= MAX_H)).sum()
                ),
                "before_run_start": int((up["in_registry"] & (up["from_start_h"] < 0)).sum()),
            },
            "insertion_range": [str(up["inserted"].min()), str(up["inserted"].max())],
            "run_range_used": [int(pr["run"].min()), int(pr["run"].max())] if len(pr) else None,
            "by_lumi": bool(up["lumi"].notna().any()),
        }

    # ------------------------------------------- by-LS tags: per-LS latency
    report["per_lumisection"] = {"ls_length_s": LS_SECONDS}
    for wf, info in report["workflows"].items():
        if not info["by_lumi"]:
            continue
        u = pd.read_csv(os.path.join(OUT, f"uploads_{wf}.csv"),
                        parse_dates=["inserted", "start", "end"])
        perls = per_lumisection(u[~u["dropped"]])
        perls.to_csv(os.path.join(OUT, f"perls_{wf}.csv"), index=False)
        report["per_lumisection"][wf] = {
            "n_run_ls_pairs": int(len(perls)),
            "n_runs": int(perls["run"].nunique()),
            "n_uploads_total": int((~u["dropped"]).sum()),
            "latency_h": stats(perls["latency_h"]),
            "latency_lt12h_h": stats(perls[perls["latency_h"] < 12]["latency_h"]),
        }

    pr_all = pd.concat(all_pr, ignore_index=True)
    pr_all.to_csv(os.path.join(OUT, "perrun_all.csv"), index=False)
    dropped = pd.concat(all_dropped, ignore_index=True)
    dropped.to_csv(os.path.join(OUT, "dropped.csv"), index=False)

    summ = summarize(pr_all)
    summ.to_csv(os.path.join(OUT, "summary.csv"), index=False)

    # compact median / mean table: one row per workflow (the fig7 numbers)
    tab = []
    for wf in list(WORKFLOWS) + ["NGT"]:
        row = {"workflow": wf, "n_runs": int(summ[summ["workflow"] == wf]["n"].iloc[0])}
        for which in ("first", "last"):
            for ref in ("start", "end"):
                x = summ[(summ["workflow"] == wf) & (summ["upload"] == which)
                         & (summ["reference"] == ref)].iloc[0]
                row[f"{which}_from_{ref}_median_h"] = round(x["median_h"], 2)
                row[f"{which}_from_{ref}_mean_h"] = round(x["mean_h"], 2)
        tab.append(row)
    pd.DataFrame(tab).to_csv(os.path.join(OUT, "median_mean_table.csv"), index=False)
    report["summary"] = json.loads(summ.to_json(orient="records"))
    with open(os.path.join(OUT, "summary.json"), "w") as fh:
        json.dump(report, fh, indent=2, default=str)

    # ------------------------------------------------------------- console
    pd.set_option("display.width", 220)
    print(f"run registry: {len(runs)} runs, {runs['run'].min()}-{runs['run'].max()}")
    for wf, info in report["workflows"].items():
        print(f"\n{wf:15s} {info['n_uploads']:4d} uploads in {info['n_runs_in_file']:3d} runs "
              f"-> used {info['n_uploads_used']} uploads / {info['n_runs_used']} runs "
              f"(dropped {info['n_uploads_dropped']}: {info['dropped_reasons']})")
    cols = ["workflow", "upload", "reference", "n", "median_h", "mean_h", "p16_h", "p84_h",
            "p95_h", "frac_before_zero", "frac_within_Tiny", "frac_within_Small",
            "frac_within_Medium", "frac_within_Large"]
    print()
    print(summ[cols].to_string(index=False, float_format=lambda v: f"{v:7.2f}"))
    print("\nper lumisection (LS -> first upload of that LS):")
    for wf, b in report["per_lumisection"].items():
        if wf == "ls_length_s":
            continue
        L = b["latency_h"]
        print(f"  {wf:22s} {b['n_run_ls_pairs']:5d} (run, LS) pairs in {b['n_runs']:3d} runs "
              f"from {b['n_uploads_total']:5d} uploads: median {L['median_h']:.2f} h, "
              f"mean {L['mean_h']:.2f} h, p16 {L['p16_h']:.2f}, p84 {L['p84_h']:.2f}, "
              f"min {L['min_h']:.2f}, max {L['max_h']:.2f}")
    print("\ndropped uploads:")
    print(dropped[["workflow", "run", "inserted", "from_end_h", "in_registry"]]
          .to_string(index=False))
    print(f"\nwritten to {OUT}/")


if __name__ == "__main__":
    main()
