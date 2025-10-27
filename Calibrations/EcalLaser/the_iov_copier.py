#!/usr/bin/env python3
import subprocess
import re
import sqlite3
from datetime import datetime, timedelta

TAG_MAIN = "EcalLaserAPDPNRatios_prompt_v3"
TAG_REF = "EcalLaserAPDPNRatios_prompt_v3_inRunIoVs"
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

def parse_runs(output):
    """Parse conddb listRuns output into [(run_number, start_time, end_time, start_iov, end_iov)]"""
    runs = []
    for line in output.splitlines():
        m = re.match(r"(\d{6,})\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.\d+\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
        if m:
            run, start, end = m.groups()
            runs.append((int(run), datetime.strptime(start, "%Y-%m-%d %H:%M:%S"), datetime.strptime(end, "%Y-%m-%d %H:%M:%S")))
    return runs

def find_run_and_ls(timestamp, runs):
    """Find the run and approximate LS corresponding to a timestamp."""
    for run, start, end in runs:
        if start <= timestamp <= end:
            dt = (timestamp - start).total_seconds()
            ls = int(round(dt / LS_DURATION))
            return run, max(1, ls)
    return None, None

# Step 3: identify new payloads newer than last reference IOV

# Parse both outputs with their respective parsers
iov_main = parse_conddb_list_main(run_cmd(f"conddb --noLimit list {TAG_MAIN}"))
iov_ref = parse_conddb_list_inrun(run_cmd(f"conddb --noLimit list {TAG_REF}"))

# Step 3: identify new payloads appearing after the last matched hash in the reference tag

known_hashes = [h for _, h in iov_ref]
main_hashes = [h for _, _, h in iov_main]
#main_hashes = [h for _, h in iov_main]

known_hashes_set = set(h for _, h in iov_ref)
last_common_index = None

# scan from oldest to newest (reverse the list)
for rev_idx, h in enumerate(reversed(main_hashes)):
    if h in known_hashes_set:
        # compute the index in the original main_hashes list
        last_common_index = len(main_hashes) - 1 - rev_idx
        break

if last_common_index is None:
    # no common hash found
    new_iovs = iov_main        # take all
else:
    # everything after that index (newer entries) is at indices 0..last_common_index-1
    print(f"Last common hash: {main_hashes[last_common_index]} at index {last_common_index}")
    # Take all payloads *after* that one (older entries)
    new_iovs = iov_main[last_common_index + 1:]
    
print(f"Found {len(new_iovs)} new payload(s) after the last matched hash.")

# # Step 4: get recent runs
runs_output = run_cmd("conddb listRuns --limit 200")
runs = parse_runs(runs_output)


# Step 5: Import payload into local SQLite
sqlite_file = "EcalLaserAPDPNRatios_prompt_v3_inRunIoVs.db"

for ts_str, since_iov, payload_hash in new_iovs:
    print(f"\nProcessing payload {payload_hash} (since {since_iov})")

    ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")

    # Find run and LS corresponding to this timestamp
    run, ls = find_run_and_ls(ts, runs)
    if run is None:
        print(f"  No matching run found for timestamp {ts_str}")
        continue

    print(f"  Closest run: {run}, LS ~ {ls}")

    # Import the payload directly into local SQLite
    cmd = (
        f"conddb_import "
        f"-c sqlite_file:{sqlite_file} "
        f"-f frontier://FrontierProd/CMS_CONDITIONS "
        f"-i {TAG_MAIN} "
        f"-t {TAG_REF} "
        f"-b {since_iov} -e {since_iov}"
    )

    print(f"  Importing payload from PromptProd into {sqlite_file} ...")
    result = run_cmd(cmd)

    print(f"  Imported {payload_hash} (IOV={since_iov}) corresponding to Run {run}, LS {ls}")

#### final touch re-derive the iovs

print(f"\nOpening {sqlite_file} for IOV conversion...")

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
    print(f"  Updating {payload_hash}: Run {run}, LS {ls} → packed {packed_iov}")

    cur.execute(
        "UPDATE IOV SET SINCE=? WHERE PAYLOAD_HASH=?;",
        (packed_iov, payload_hash),
    )

conn.commit()
conn.close()

print("\n All IOVs updated to Run–LS format and TIME_TYPE changed to 'Lumi'.")
