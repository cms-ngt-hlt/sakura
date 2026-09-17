#!/usr/bin/env python3

import json
import argparse
from collections import defaultdict

def convert_f3mon_to_oms(input_file):

    with open(input_file) as f:
        data = json.load(f)["data"]

    run_number = data[0]["id"].split("_")[0]

    result = {
        str(run_number): defaultdict(list)
    }

    for entry in data:
        attrs = entry["attributes"]

        result[str(run_number)][attrs["stream_name"]].append({
            "LS": attrs["lumisection_number"],
            "rate": attrs["rate"],
            "size": attrs["n_events"] * attrs["event_size"],
            "bandwidth": attrs["bandwidth"] * 1e6,
        })

    # sort lumisections
    for stream in result[str(run_number)]:
        result[str(run_number)][stream].sort(
            key=lambda x: x["LS"]
        )

    # convert defaultdict to normal dict
    result[str(run_number)] = dict(result[str(run_number)])

    return run_number, result


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument(
    "-o",
    "--output",
    help="Output filename"
)

args = parser.parse_args()

run_number, result = convert_f3mon_to_oms(args.input)

output_file = (
    args.output
    if args.output
    else f"{args.input}".replace('.json', '_F3MonToOMS.json')
)

with open(output_file, "w") as f:
    json.dump(result, f, indent=4)

print(f"Wrote {output_file}")
