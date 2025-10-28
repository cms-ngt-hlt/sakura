#!/usr/bin/env python3
from datetime import datetime, timedelta
import os
import re
import sqlite3
import subprocess
import sys
import json

TAG_MAIN = "EcalLaserAPDPNRatios_prompt_v3"
TAG_REF = "EcalLaserAPDPNRatios_prompt_v3_inRunLSIoVs"
LS_DURATION = 23.3  # seconds

def pack(high, low):
    """Pack run,ls (both 32-bit) into a 64-bit integer."""
    return (high << 32) | low

def run_cmd(cmd):
    """Run a shell command and return stdout as text."""
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(result.stderr)
    return result.stdout

def parse_conddb_list(output):
    """Extract (timestamp, hash) pairs from conddb list output."""
    entries = []
    for line in output.splitlines():
        m = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\s([0-9a-f]{40})\s+EcalLaserAPDPNRatios", line)
        if m:
            timestamp_str, payload_hash = m.groups()
            entries.append((timestamp_str, payload_hash))
        else:
            print("NO MATCH!!!")
    return entries

def parse_conddb_list_main(output):
    """
    Parse 'conddb list' output for timestamp-based IOVs.
    Returns list of tuples: (timestamp_str, since_iov, payload_hash)
    """
    entries = []
    for line in output.splitlines():
        m = re.match(
            r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \((\d+)\).*?([0-9a-f]{40})\s+EcalLaserAPDPNRatios",
            line,
        )
        if m:
            timestamp_str, since_iov, payload_hash = m.groups()
            entries.append((timestamp_str, since_iov, payload_hash))
    return entries

def parse_conddb_list_inrun(output):
    """Parse 'conddb list' output for run-based IOVs."""
    entries = []
    for line in output.splitlines():
        # Match e.g. "398421  2025-10-24 14:13:57  7a38b1...  EcalLaserAPDPNRatios"
        m = re.match(
            r"(\d+)\s+\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\s+([0-9a-f]{40})\s+EcalLaserAPDPNRatios",
            line,
        )
        if m:
            run_str, payload_hash = m.groups()
            entries.append((int(run_str), payload_hash))
    return entries

def parse_conddb_list_inrunls(output):
    """Parse 'conddb list' output for run-lumi based IOVs (with packed since values)."""
    entries = []
    for line in output.splitlines():
        # Example line:
        # 398515 :   1326 (1711608891966766)  2025-10-27 16:39:52  26b2f052da7fbe7c4884d4ed875e027f9885e799  EcalLaserAPDPNRatios
        m = re.match(
            r"\s*(\d+)\s*:\s*(\d+)\s*\((\d+)\)\s+\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+([0-9a-f]{40})\s+EcalLaserAPDPNRatios",
            line,
        )
        if m:
            run_str, lumi_str, raw_since, payload_hash = m.groups()
            entries.append((int(run_str), int(lumi_str), int(raw_since), payload_hash))
    return entries

def parse_runs_old(output):
    """Parse conddb listRuns output into [(run_number, start_time, end_time, start_iov, end_iov)]"""
    runs = []
    for line in output.splitlines():
        m = re.match(r"(\d{6,})\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.\d+\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
        if m:
            run, start, end = m.groups()
            runs.append((int(run), datetime.strptime(start, "%Y-%m-%d %H:%M:%S"), datetime.strptime(end, "%Y-%m-%d %H:%M:%S")))
    return runs

from typing import List, Tuple, Optional

def parse_runs(output):
    """
    Parse `conddb listRuns` output into [(run_number, start_time, end_time)],
    where end_time is None for ongoing runs.
    """
    runs = []
    for line in output.splitlines():
        # Example lines:
        # 398599  2025-10-27 19:15:17.756000  2025-10-27 19:59:12.412000  7565982249393324032  7565993566632148992
        # 398600  2025-10-27 20:04:21.316000  on going...                 7565994893777043456  -
        m = re.match(
            r"\s*(\d+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})(?:\.\d+)?\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}|on going\.\.\.)",
            line,
            flags=re.IGNORECASE,
        )
        if not m:
            continue

        run_str, start_str, end_str = m.groups()
        run = int(run_str)

        start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")

        if end_str.lower().startswith("on"):
            end_time = None
        else:
            end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

        runs.append((run, start_time, end_time))

    return runs

def find_run_and_ls(timestamp, runs):
    """Find the run and approximate LS corresponding to a timestamp.
    If the run has no end time, assume it's still open and include any later timestamps.
    """
    for run, start, end in runs:
        # handle open-ended run (end may be None)
        if end is None:
            #print("end is NONE")
            #print("start: ",start,"- end:",end,"  | timestamp",timestamp)
            if timestamp >= start:
                dt = (timestamp - start).total_seconds()
                ls = int(round(dt / LS_DURATION))
                return run, max(1, ls)
        else:
            #print("start: ",start,"- end:",end,"  | timestamp",timestamp)
            if start <= timestamp <= end:
                dt = (timestamp - start).total_seconds()
                ls = int(round(dt / LS_DURATION))
                return run, max(1, ls)
    return None, None


########################################################################
# --- Check that CMSSW environment is set up ---
if "CMSSW_BASE" not in os.environ:
    print("CMSSW environment not detected. Please run 'cmsenv' before executing this script.")
    sys.exit(1)
else:
    print(f"CMSSW environment detected: {os.environ['CMSSW_BASE']}")

sqlite_file = TAG_REF+".db"

# --- Step 1: remove old DB if it exists ---
if os.path.exists(sqlite_file):
    print(f"Found existing {sqlite_file}, deleting it before starting...")
    os.remove(sqlite_file)
else:
    print(f"No existing {sqlite_file} found. Proceeding.")

# Step 2: identify new payloads newer than last reference IOV

# Parse both outputs with their respective parsers
iov_main = parse_conddb_list_main(run_cmd(f"conddb --noLimit list {TAG_MAIN}"))
iov_ref = parse_conddb_list_inrunls(run_cmd(f"conddb --noLimit list {TAG_REF}"))

# Step 3: identify new payloads appearing after the last matched hash in the reference tag
known_hashes = [payload_hash for _, _, _, payload_hash in iov_ref]
main_hashes = [h for _, _, h in iov_main]

# Build a set of known payload hashes from the reference tag (4-tuple entries)
known_hashes_set = {payload_hash for _, _, _, payload_hash in iov_ref}

last_common_index = None

# Scan from oldest to newest (reversed list)
for rev_idx, h in enumerate(reversed(main_hashes)):
    if h in known_hashes_set:
        # compute the index in the original main_hashes list
        last_common_index = len(main_hashes) - 1 - rev_idx
        break

if last_common_index is None:
    # no common hash found
    new_iovs = iov_main  # take all
    print("No last common hash found: taking all payloads.")
else:
    # everything *after* that index (newer entries)
    print(f"Last common hash: {main_hashes[last_common_index]} at index {last_common_index}")
    new_iovs = iov_main[last_common_index + 1:]

print(f"Found {len(new_iovs)} new payload(s) after the last matched hash.")

# Step 4: get recent runs
runs_output = run_cmd("conddb listRuns --limit 500")
runs = parse_runs(runs_output)

# Step 5: Import payload into local SQLite

for ts_str, since_iov, payload_hash in new_iovs:
    print(f"\nProcessing payload {payload_hash} (since {since_iov})")

    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")

    # Find run and LS corresponding to this timestamp
    run, ls = find_run_and_ls(ts, runs)
    if run is None:
        print(f"  No matching run found for timestamp {ts_str}")
        continue

    print(f"  Closest run: {run}, LS ~ {ls}")

    cmd = (
        f"conddb --yes copy "
        f"--destdb {sqlite_file} "
        f"--from {since_iov} "
        f"--to {since_iov} "
        f"--type tag "
        f"{TAG_MAIN} {TAG_REF}"
    )

    print(f"  Importing payload from PromptProd into {sqlite_file} ...")
    print(f"{cmd}")
    result = run_cmd(cmd)

    print(f"  Imported {payload_hash} (IOV={since_iov}) corresponding to Run {run}, LS {ls}")

#### final touch re-derive the iovs

print(f"\nOpening {sqlite_file} for IOV conversion...")

# --- Protection: check that the file exists and is not empty ---
if not os.path.exists(sqlite_file):
    print(f"SQLite file '{sqlite_file}' not found in current directory. Exiting gracefully.")
    sys.exit(1)

if os.path.getsize(sqlite_file) == 0:
    print(f"SQLite file '{sqlite_file}' exists but is empty (0 bytes). Exiting gracefully.")
    sys.exit(1)

conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

# 1. Change TIME_TYPE
cur.execute("UPDATE TAG SET TIME_TYPE='Lumi' WHERE TIME_TYPE='Time';")

# 2. For each imported payload, compute packed IOV and update SINCE
for ts_str, since_iov, payload_hash in new_iovs:
    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    run, ls = find_run_and_ls(ts, runs)
    if run is None:
        print(f"  Skipping {payload_hash}: could not find matching run.")
        continue

    packed_iov = pack(run, ls)
    print(f"  Updating IOV {since_iov} -> Run {run}, LS {ls} -> packed {packed_iov}")

    query = "UPDATE IOV SET SINCE=? WHERE SINCE=?;"
    params = (packed_iov, since_iov)

    print("Executing SQL:", query, "with parameters:", params)
    cur.execute(query, params)
    if cur.rowcount == 0:
        print(f" No rows updated for IOV {since_iov}")
    else:
        print(f" Updated {cur.rowcount} row(s)")

conn.commit()
conn.close()

print("\n All IOVs updated to Run-LS format and TIME_TYPE changed to 'Lumi'.")

# --- Final step : show the resulting IOVs using conddb ---
print("\n Listing the resulting IOVs using conddb:")
cmd = [
    "conddb",
    "--db",
    sqlite_file,
    "list",
    "EcalLaserAPDPNRatios_prompt_v3_inRunLSIoVs",
]
subprocess.run(cmd, check=True)

# and now upload it!

metadata_file = f"{TAG_REF}.txt"

metadata = {
    "destinationDatabase": "oracle://cms_orcon_prod/CMS_CONDITIONS",
    "destinationTags": {TAG_REF: {}},
    "inputTag": TAG_REF,
    "since": None,
    "userText": "Periodical fill-up upload for NGT test demonstrator",
}

with open(metadata_file, "w") as f:
    json.dump(metadata, f, indent=4)

print(f"Created metadata file: {metadata_file}")

# --- Step 3: Upload the conditions ---
print("\n Uploading conditions with uploadConditions.py...")
subprocess.run(
    ["uploadConditions.py", sqlite_file],
    check=True
)

print("\n All steps completed successfully.")
