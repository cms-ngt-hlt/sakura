#!/usr/bin/env python3
"""Summarise CMSSW DQM client logs (Scouting stream) into one JSON per log.

Parses every dqmclient_<TAG>_DQMTestDataScouting_run<RUN>.log under <logdir-root>
and writes {tag}_{run}.json holding the global tag, input files, event count,
file open/close bookkeeping and a de-duplicated tally of all log messages.

Usage: python3 summarize_logs.py <logdir-root> <outdir>
  logdir-root  directory containing HLT/, NGT/, Prompt/
  outdir       where {tag}_{run}.json is written
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

LOG_NAME = re.compile(
    r"^dqmclient_(?P<tag>[A-Za-z]+)_DQMTestDataScouting_run(?P<run>\d+)\.log$")

# --- normalisation: applied in order, most specific first ------------------
SUBS = [
    (re.compile(r"\?cap\.format=\S*"), "?<QUERY>"),
    (re.compile(r"\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}:\d{2}(?:\.\d+)? [A-Z]+"), "<TS>"),
    (re.compile(r"(?:file://)?root://\S+"), "<PATH>"),
    (re.compile(r"\./upload/\S+"), "<DQMFILE>"),
    (re.compile(r"the \d+(?:st|nd|rd|th) record"), "the <N>th record"),
    (re.compile(r"\bRun:? \d+"), "Run <N>"),
    (re.compile(r"\bEvent:? \d+"), "Event <N>"),
    (re.compile(r"\bLumiSection \d+"), "LumiSection <N>"),
    (re.compile(r"\bstream \d+"), "stream <N>"),
    (re.compile(r"\b[\w.-]+\.cern\.ch\b"), "<HOST>"),
    (re.compile(r"\(\d+\)"), "(<N>)")
]

# --- structured lines ------------------------------------------------------
RE_GLOBALTAG = re.compile(r"^Global Tag used: (\S+)")
RE_INPUT = re.compile(r"run\d+_(job\d+)_DQMTestDataScouting\.root")
RE_RECORD = re.compile(
    r"^Begin processing the (\d+)\w{2} record\. Run (\d+), Event (\d+), "
    r"LumiSection (\d+) on stream (\d+) at (.+)$")
RE_OPEN_INIT = re.compile(r"^(.+?)\s+Initiating request to open file .*_(job\d+)_")
RE_OPEN_OK = re.compile(r"Successfully opened file .*_(job\d+)_")
RE_CLOSED = re.compile(r"Closed file .*_(job\d+)_")
RE_WRITE = re.compile(r"Writing DQM Root file: (\S+)")
RE_DROPPED = re.compile(r"dropped waiting message count (\d+)")
RE_MSG_HEAD = re.compile(r"^%MSG-(\w)\s+([^:]+):\s*(.*)$")
RE_TS = re.compile(r"^(\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}:\d{2}(?:\.\d+)? [A-Z]+)")
RE_TS_ANY = re.compile(r"\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}:\d{2}(?:\.\d+)? [A-Z]+")

MAX_BLOCK = 50  # guard against an unterminated %MSG block running to EOF


def normalise(text):
    for pattern, repl in SUBS:
        text = pattern.sub(repl, text)
    return " ".join(text.split())


def parse_header(header):
    """Return (severity, category, module). Torn headers give <unparsed>."""
    m = RE_MSG_HEAD.match(header)
    if not m:
        return "?", "<unparsed>", "<unparsed>"
    sev, category, rest = m.groups()
    module = RE_TS_ANY.split(rest)[0].strip() or "<none>"
    return sev, category.strip(), module


def extract(path, tag, run):
    messages = Counter()
    other = Counter()
    opens = []          # one dict per input-file open, in order
    lumis = []
    streams = set()
    n_records = 0
    global_tag = None
    inputs = []
    in_preamble = True
    n_open_ok = n_closed = n_snapshots = unlink_failures = 0
    terminal_write = False
    dropped = 0
    unterminated = 0
    first_ts = last_ts = None

    in_block = False
    header = ""
    payload = []

    def flush():
        sev, category, module = parse_header(header)
        body = normalise(" ".join(payload)) if payload else "<empty>"
        messages[(sev, category, module, body)] += 1

    with open(path, "r", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\n")

            # --- %MSG block folding ---
            if line.startswith("%MSG-"):
                if in_block:
                    unterminated += 1
                    flush()
                in_block, header, payload = True, line, []
                continue
            if in_block:
                if line.strip() == "%MSG":
                    flush()
                    in_block = False
                    continue
                elif len(payload) >= MAX_BLOCK:
                    unterminated += 1
                    flush()
                    in_block = False
                else:
                    payload.append(line)
                    continue

            ts = RE_TS.match(line)
            if ts:
                in_preamble = False   # preamble lines carry no timestamp
                if first_ts is None:
                    first_ts = ts.group(1)
                last_ts = ts.group(1)

            # --- preamble: input list and global tag ---
            if in_preamble:
                m = RE_GLOBALTAG.match(line)
                if m:
                    global_tag = m.group(1)
                    inputs = []  # keep only the Final Source list that follows
                    continue
                m = RE_INPUT.search(line)
                if m:
                    inputs.append(m.group(1))
                    continue

            # --- body ---
            m = RE_RECORD.match(line)
            if m:
                in_preamble = False
                n_records = int(m.group(1))
                lumis.append(int(m.group(4)))
                streams.add(int(m.group(5)))
                continue

            m = RE_OPEN_INIT.search(line)
            if m:
                in_preamble = False
                opens.append({"job": m.group(2), "record_at_open": n_records,
                              "opened": False, "record_at_close": None})
                continue

            m = RE_OPEN_OK.search(line)
            if m:
                n_open_ok += 1
                for entry in reversed(opens):
                    if entry["job"] == m.group(1):
                        entry["opened"] = True
                        break
                continue

            m = RE_CLOSED.search(line)
            if m:
                n_closed += 1
                for entry in reversed(opens):
                    if entry["job"] == m.group(1):
                        entry["record_at_close"] = n_records
                        break
                continue

            m = RE_WRITE.search(line)
            if m:
                if ".ls" in m.group(1):
                    n_snapshots += 1
                else:
                    terminal_write = True
                continue

            m = RE_DROPPED.search(line)
            if m:
                dropped = int(m.group(1))
                continue

            if "Unlink failed" in line:
                unlink_failures += 1
                continue

            if line.strip():
                other[normalise(line)] += 1

    if in_block:
        unterminated += 1
        flush()

    return {
        "tag": tag,
        "run": run,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "global_tag": global_tag,
        "input_files": inputs,
        "n_input_files": len(inputs),
        "n_records": n_records,
        "lumi_min": min(lumis) if lumis else None,
        "lumi_max": max(lumis) if lumis else None,
        "streams": sorted(streams),
        "opens": opens,
        "n_open_initiated": len(opens),
        "n_open_success": n_open_ok,
        "n_closed": n_closed,
        "terminal_write": terminal_write,
        "snapshot_writes": n_snapshots,
        "dropped_messages": dropped,
        "unlink_failures": unlink_failures,
        "unterminated_blocks": unterminated,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "messages": [
            {"severity": s, "category": c, "module": m, "payload": p, "count": n}
            for (s, c, m, p), n in messages.most_common()
        ],
        "other_lines": [{"template": t, "count": n} for t, n in other.most_common()],
    }


def main():
    root, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)

    logs = sorted(p for pattern in ("*.log", "*/*.log")
                  for p in root.glob(pattern) if LOG_NAME.match(p.name))
    if not logs:
        sys.exit(f"no scouting logs found under {root}")
    for i, path in enumerate(logs, 1):
        m = LOG_NAME.match(path.name)
        tag, run = m.group("tag"), int(m.group("run"))
        print(f"[{i}/{len(logs)}] {tag} {run}", file=sys.stderr, flush=True)
        summary = extract(path, tag, run)
        (outdir / f"{tag}_{run}.json").write_text(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
