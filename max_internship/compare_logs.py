#!/usr/bin/env python3
"""Compare per-log summaries across the HLT, NGT and Prompt calibration tags.

Reads the {tag}_{run}.json files written by summarize_logs.py and prints per-run
tables (events, input files, dropped messages), log messages present under one
tag but not another, and per-log internal consistency checks.

Usage: python3 compare.py <summarydir>
  summarydir  output directory of summarize_logs.py
"""

import json
import sys
from pathlib import Path

TAGS = ["HLT", "NGT", "Prompt"]


def load(d):
    summaries = {}
    for path in sorted(d.glob("*.json")):
        s = json.loads(path.read_text())
        summaries[(s["tag"], s["run"])] = s
    return summaries


def vertex_warnings(s):
    return [m["count"] for m in s["messages"]
            if m["payload"].startswith("Run3ScoutingVertex")]


def internal_checks(s):
    """Inconsistencies visible within a single log."""
    bad = []
    n_in = s["n_input_files"]
    if s["n_open_success"] != n_in:
        bad.append(f"opened {s['n_open_success']} of {n_in} input files")
    if s["n_closed"] != n_in:
        bad.append(f"closed {s['n_closed']} of {n_in} input files")

    opened = {o["job"] for o in s["opens"]}
    never = [j for j in s["input_files"] if j not in opened]
    if never:
        bad.append(f"no open line for: {', '.join(never)}")

    unclosed = [o["job"] for o in s["opens"] if o["record_at_close"] is None]
    if unclosed:
        bad.append(f"never closed: {', '.join(unclosed)}")

    if not s["terminal_write"]:
        bad.append("no terminal DQM write (job did not finish)")
    if s["unterminated_blocks"]:
        bad.append(f"{s['unterminated_blocks']} unterminated %MSG blocks")

    # ratio is only meaningful when nothing was thrown away
    warn = vertex_warnings(s)
    if s["dropped_messages"] == 0 and s["n_records"] and len(warn) == 2:
        ratio = sum(warn) / s["n_records"]
        if abs(ratio - 2.0) > 1e-9:
            bad.append(f"vertex-warning ratio {ratio:.4f} with 0 dropped messages")
    return bad


def numeric_table(summaries, runs, field, title):
    print(f"\n=== {title}")
    print(f"{'run':<9}" + "".join(f"{t:>12}" for t in TAGS) + f"{'spread':>10}")
    for run in runs:
        values, cells = [], ""
        for tag in TAGS:
            s = summaries.get((tag, run))
            if s is None:
                cells += f"{'-':>12}"
            else:
                values.append(s[field])
                cells += f"{s[field]:>12}"
        spread = ""
        if len(values) > 1 and max(values) and min(values) != max(values):
            spread = f"{100 * (max(values) - min(values)) / max(values):.1f}%"
        print(f"{run:<9}{cells}{spread:>10}" + ("  <--" if spread else ""))


def template_diffs(summaries, runs, field, keyfn, title):
    print(f"\n=== {title}")
    found = False
    for run in runs:
        present = {tag: summaries[(tag, run)] for tag in TAGS
                   if (tag, run) in summaries}
        if len(present) < 2:
            continue
        keys = {tag: {keyfn(x) for x in s[field]} for tag, s in present.items()}
        union = set().union(*keys.values())
        odd = [k for k in union if any(k not in v for v in keys.values())]
        if not odd:
            continue
        found = True
        print(f"\n  run {run}")
        for key in sorted(odd):
            has = [t for t in TAGS if t in keys and key in keys[t]]
            missing = [t for t in TAGS if t in keys and key not in keys[t]]
            print(f"    in {'+'.join(has)}, not in {'+'.join(missing)}:")
            print(f"      {key}")
    if not found:
        print("  (none)")


def main():
    summaries = load(Path(sys.argv[1]))
    if not summaries:
        sys.exit("no summaries found")
    runs = sorted({run for _, run in summaries})

    print(f"{len(summaries)} summaries, {len(runs)} runs")
    missing = [(t, r) for r in runs for t in TAGS if (t, r) not in summaries]
    if missing:
        print("MISSING: " + ", ".join(f"{t}/{r}" for t, r in missing))

    gtags = {s["global_tag"] for s in summaries.values()}
    print(f"global tags in use: {', '.join(sorted(gtags))}")

    numeric_table(summaries, runs, "n_records", "events processed")
    numeric_table(summaries, runs, "n_input_files", "input files")
    numeric_table(summaries, runs, "dropped_messages", "dropped log messages")

    template_diffs(
        summaries, runs, "messages",
        lambda m: f"{m['severity']} {m['category']}/{m['module']}: {m['payload']}",
        "message templates not common to all tags")
    template_diffs(
        summaries, runs, "other_lines", lambda o: o["template"],
        "other log lines not common to all tags")

    print("\n=== per-log internal inconsistencies")
    clean = True
    for key in sorted(summaries):
        bad = internal_checks(summaries[key])
        if bad:
            clean = False
            print(f"  {key[0]}/{key[1]}")
            for b in bad:
                print(f"    - {b}")
    if clean:
        print("  (none)")


if __name__ == "__main__":
    main()
