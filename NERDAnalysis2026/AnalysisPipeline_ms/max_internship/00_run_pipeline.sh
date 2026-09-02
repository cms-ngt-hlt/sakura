#!/bin/bash
# Run pipeline preparation and create (optionally submit) all tag jobs.

set -uo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$HERE"

usage() {
  cat <<'EOF'
Usage: bash ./00_run_pipeline.sh [--force] [--fulltrust]

  --force      Regenerate existing Jobs_<TAG> directories.
  --fulltrust  Submit every generated condor_<TAG>.sub file to HTCondor.
  -h, --help   Show this help message.

Without --fulltrust, the script only prepares the Condor submission files.
EOF
}

force=false
fulltrust=false
while (( $# > 0 )); do
  case "$1" in
    --force)
      force=true
      ;;
    --fulltrust)
      fulltrust=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

# shellcheck source=pipeline.cfg
source "$HERE/pipeline.cfg"
(( ${#TAGS[@]} > 0 )) || { echo "ERROR: TAGS is empty in pipeline.cfg" >&2; exit 1; }

echo "Starting file-list and CMSSW configuration generation in parallel..."
bash "$HERE/generate_filelists.sh" &
filelist_pid=$!
bash "$HERE/01_make_config.sh" &
config_pid=$!

# Wait for both processes even if one fails, so no preparation process is left
# running after this wrapper exits.
filelist_rc=0
config_rc=0
wait "$filelist_pid" || filelist_rc=$?
wait "$config_pid" || config_rc=$?

if (( filelist_rc != 0 || config_rc != 0 )); then
  echo "ERROR: preparation failed (generate_filelists.sh=$filelist_rc, 01_make_config.sh=$config_rc)." >&2
  exit 1
fi

echo "Preparation complete. Generating Condor jobs for: ${TAGS[*]}"
submit_args=()
if [[ "$force" == true ]]; then
  submit_args+=(--force)
fi

for tag in "${TAGS[@]}"; do
  python3 "$HERE/02_submit.py" --tag "$tag" "${submit_args[@]}" || {
    echo "ERROR: job generation failed for tag $tag; nothing was submitted." >&2
    exit 1
  }
done

if [[ "$fulltrust" == true ]]; then
  command -v condor_submit >/dev/null || {
    echo "ERROR: condor_submit is not available; no jobs were submitted." >&2
    exit 1
  }
  echo "All job files generated successfully. Submitting to HTCondor..."
  for tag in "${TAGS[@]}"; do
    condor_submit "$HERE/condor_${tag}.sub" || {
      echo "ERROR: submission failed for tag $tag." >&2
      exit 1
    }
  done
  echo "All tags submitted successfully."
else
  echo "All job files generated. Review them, then submit manually or rerun with --fulltrust."
fi

