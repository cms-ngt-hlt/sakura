#!/bin/bash
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CFG="${HERE}/pipeline.cfg"

# shellcheck source=pipeline.cfg
source "$CFG"

[[ ${#RUNS[@]} -gt 0 ]] || { echo "RUNS is empty in $CFG" >&2; exit 1; }
[[ -n "$DATASET_PATTERN" ]] || { echo "DATASET_PATTERN is empty in $CFG" >&2; exit 1; }
[[ -n "$FILELIST" ]] || { echo "FILELIST is empty in $CFG" >&2; exit 1; }
command -v dasgoclient >/dev/null || { echo "dasgoclient is not available" >&2; exit 1; }

if [[ "$FILELIST" = /* ]]; then
  FILELIST_PATH="$FILELIST"
else
  FILELIST_PATH="${HERE}/${FILELIST}"
fi

# Start with an empty output file, then append each run's files to it.
: > "$FILELIST_PATH"

for run in "${RUNS[@]}"; do
  echo "run ${run}"

  # Find the datasets available for this run, then retain the one configured
  # dataset family.
  all=$(dasgoclient --query="dataset run=${run}")
  datasets=$(grep -E "$DATASET_PATTERN" <<< "$all" || true)
  echo "Found the following datasets: ${datasets}"

  if [[ -z "$datasets" ]]; then
    echo "Warning: no dataset found for this run - skipping"
    continue
  fi

  # Resolve every matching dataset shard to its files for this run.
  files=$(
    while read -r ds; do
      dasgoclient --query="file dataset=${ds} run=${run}"
    done <<< "$datasets"
  )

  if [[ -n "$files" ]]; then
    printf '%s\n' "$files" >> "$FILELIST_PATH"
    file_count=$(printf '%s\n' "$files" | wc -l | tr -d ' ')
  else
    file_count=0
  fi

  echo "  ${file_count} files"
done

echo "---"
echo "Done. File list: ${FILELIST_PATH} ($(wc -l < "$FILELIST_PATH" | tr -d ' ') files)"

