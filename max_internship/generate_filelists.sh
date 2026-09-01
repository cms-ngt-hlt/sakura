#!/bin/bash
set -euo pipefail

CSV=oms_runs.csv
OUTDIR=filelists

# regex to match valid file paths
DATASET_REGEX='^/EGamma[0-9]+/[^/]+ZElectron-PromptReco-v[0-9]+/RAW-RECO$'

# quick sanity check if we can really read from the csv file
[[ -f "$CSV" ]] || { echo "can not read $CSV" >&2; exit 1; }

mkdir -p "$OUTDIR" # create outdir if it doesn't exist

while read -r run; do
  echo "run ${run}"

  # first, we check which datasets are actually contained in this run
  all=$(dasgoclient --query="dataset run=${run}")

  # then, we filter down to ZElectron RAW_RECO datasets that match the regex string
  datasets=$(grep -E "$DATASET_REGEX" <<< "$all" || true)
  echo "Found the following datasets: ${datasets}"
  if [[ -z "$datasets" ]]; then
    echo "Warning: no dataset found for this run - skipping"
    continue
  fi

  # finally, we create one file per dataset query
  files=$(
    while read -r ds; do
      dasgoclient --query="file dataset=${ds} run=${run}"
    done <<< "$datasets"
  )

    printf '%s\n' "$files" > "${OUTDIR}/run_${run}.txt"
    echo "  $(wc -l <<< "$datasets") datasets -> $(wc -l <<< "$files") files"
 
done < <(tail -n +2 "$CSV" | cut -d, -f1)
 
echo "---"
echo "Done. Lists in ${OUTDIR}/"

