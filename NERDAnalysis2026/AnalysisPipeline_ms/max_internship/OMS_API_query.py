#!/usr/bin/env python3
"""Run with: python3 OMS_API_query.py

Requires the CERN omsapi client and a valid Kerberos session.
Writes oms_runs.csv in the current directory, replacing any existing file.
Start/end times are taken from OMS in UTC. snapshot_time is start_time +
8 hours, matching the supplied CSV (the original rationale is undocumented).
"""

from datetime import datetime, timedelta, timezone
import csv


PER_PAGE = 999 # how many results do we want to see per page
ERA_NAMES = ["Run2026A", "Run2026B", "Run2026C", "Run2026D"]
 
RUN_FILTERS = {
    "fill_type_runtime": "PROTONS",
    "l1_hlt_mode": "collisions2026",
    "stable_beam": True,
}

def connect(verbose=True):
    from omsapi import OMSAPI

    omsapi = OMSAPI("https://cmsoms.cern.ch/agg/api", "v1",
                    cert_verify=False, verbose=verbose, throw_on_err=True)
    omsapi.auth_krb()
    return omsapi

def _fetch_all(omsapi, resource, filters=None, per_page=PER_PAGE):
    """Walk every page of a resource and return the list of JSON:API objects.
 
    The client has no page walker, so we bump page[offset] until a page comes
    back shorter than the requested limit.
    """
    query = omsapi.query(resource)
    for attribute, value in (filters or {}).items():
        query.filter(attribute, value)
 
    rows = []
    page = 1
    while True:
        query.paginate(page=page, per_page=per_page)
        batch = query.data().json()["data"]
 
        rows.extend(batch)
        if len(batch) < per_page:
            return rows
        page += 1

def get_eras(omsapi, era_names=ERA_NAMES):
    """Fetch all eras, keep the requested ones (drops HI and non-2026 eras)."""
    eras = _fetch_all(omsapi, "eras")
    by_name = {era["attributes"]["name"]: era["attributes"] for era in eras}
    return [by_name[name] for name in era_names]

def get_runs(omsapi, era_name, run_filters=RUN_FILTERS):
    filters = dict(run_filters, era=era_name)
    return [run["attributes"] for run in _fetch_all(omsapi, "runs", filters)]

def get_fill_schemes(omsapi, era_name):
    """Map fill_number -> injection_scheme (the filling scheme lives on fills)."""
    fills = _fetch_all(omsapi, "fills", {"era": era_name})
    return {fill["attributes"]["fill_number"]: fill["attributes"]["injection_scheme"]
            for fill in fills}

def collect(omsapi):
    """Return [{"era": <era attributes>, "runs": [<run attributes>, ...]}]."""
    eras = get_eras(omsapi)
    print("eras: {}".format(", ".join(era["name"] for era in eras)))
 
    collected = []
    for era in eras:
        runs = get_runs(omsapi, era["name"])
        fills = sorted({run["fill_number"] for run in runs})
        schemes = get_fill_schemes(omsapi, era["name"]) 
        for run in runs:
            run["injection_scheme"] = schemes.get(run["fill_number"]) # query injection scheme based on fill number
        print("=== era {}contains {} runs in {} fills===".format(
            era["name"], len(runs), len(fills)))
        print("  fills: {}".format(fills))
        print("  runs:  {}".format(sorted(run["run_number"] for run in runs)))
 
        collected.append({"era": era, "runs": runs})
 
    return collected

def save_csv(eras, path="oms_runs.csv"):
    # Validate and build all rows before opening the destination file.
    rows = []
    for era in eras:
        for run in era["runs"]:
            start = run["start_time"]
            end = run["end_time"]
            if not start or not end:
                raise ValueError(
                    f"Run {run['run_number']} has no start_time or end_time"
                )
            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
            if start_dt.tzinfo is None:
                raise ValueError(
                    f"Run {run['run_number']} has a start_time without a timezone"
                )
            snapshot = start_dt.astimezone(timezone.utc) + timedelta(
                hours=8
            )
            rows.append([
                run["run_number"], run["injection_scheme"], run["era"],
                start, end,
                snapshot.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            ])

    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow([
            "run_number", "injection_scheme", "Run era",
            "Start time", "End_time", "snapshot_time",
        ])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} runs to {path}")


if __name__ == "__main__":
    save_csv(collect(connect()))

