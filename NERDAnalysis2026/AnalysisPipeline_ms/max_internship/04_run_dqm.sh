#!/bin/bash
# Run each script in DQM_CONFIGS for the selected tags and runs.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$HERE"
source ./pipeline.cfg

SELECT_TAG=""
SELECT_RUN=""
while (( $# )); do
    case "$1" in
        --tag|--run)
            [[ $# -ge 2 ]] || { echo "ERROR: $1 needs a value" >&2; exit 1; }
            case "$1" in
                --tag) SELECT_TAG="$2" ;;
                --run) SELECT_RUN="$2" ;;
            esac
            shift 2 ;;
        -h|--help)
            echo "Usage: bash 04_run_dqm.sh [--tag NGT] [--run 403863]"
            exit 0 ;;
        *) echo "ERROR: unknown argument '$1'" >&2; exit 1 ;;
    esac
done

[[ -n "${CMSSW_BASE:-}" ]] || { echo "ERROR: run cmsenv first" >&2; exit 1; }
[[ -n "${EOS_BASE//[[:space:]]/}" && -n "${DQM_DEST_BASE//[[:space:]]/}" ]] || {
    echo "ERROR: set EOS_BASE and DQM_DEST_BASE in pipeline.cfg" >&2; exit 1;
}
[[ ${#TAGS[@]} -eq ${#GTAGS[@]} ]] || { echo "ERROR: TAGS and GTAGS must match" >&2; exit 1; }
[[ "$DQM_THREADS" =~ ^[1-9][0-9]*$ ]] || { echo "ERROR: DQM_THREADS must be positive" >&2; exit 1; }
if [[ -n "$SELECT_TAG" ]]; then
    found=false
    for TAG in "${TAGS[@]}"; do [[ "$TAG" != "$SELECT_TAG" ]] || found=true; done
    $found || { echo "ERROR: unknown tag '$SELECT_TAG'" >&2; exit 1; }
fi
if [[ -n "$SELECT_RUN" ]]; then
    found=false
    for RUN in "${RUNS[@]}"; do [[ "$RUN" != "$SELECT_RUN" ]] || found=true; done
    $found || { echo "ERROR: unknown run '$SELECT_RUN'" >&2; exit 1; }
fi

# Resolve paths before moving into each job's working directory.
mkdir -p "$DQM_WORK_BASE" "$DQM_DEST_BASE"
WORK_BASE=$(cd "$DQM_WORK_BASE" && pwd)
DEST_BASE=$(cd "$DQM_DEST_BASE" && pwd)
EOS_BASE=$(cd "$EOS_BASE" && pwd)
if [[ -n "${CMSSW_SRC//[[:space:]]/}" ]]; then
    CMSSW_SRC=$(cd "$CMSSW_SRC" && pwd)
fi
export ERA DQM_THREADS DQM_HARVEST_CONDITIONS CMSSW_SRC

for SCRIPT in "${DQM_CONFIGS[@]}"; do
    NAME=$(basename "$SCRIPT" .sh)
    [[ "$SCRIPT" = /* ]] || SCRIPT="$HERE/$SCRIPT"
    [[ -f "$SCRIPT" ]] || { echo "ERROR: missing script $SCRIPT" >&2; exit 1; }
    for i in "${!TAGS[@]}"; do
        TAG=${TAGS[$i]}
        GTAG=${GTAGS[$i]}
        [[ -z "$SELECT_TAG" || "$TAG" == "$SELECT_TAG" ]] || continue
        for RUN in "${RUNS[@]}"; do
            [[ -z "$SELECT_RUN" || "$RUN" == "$SELECT_RUN" ]] || continue
            LOCALPATH="$EOS_BASE/$TAG/run_$RUN"
            export TAG GTAG RUN LOCALPATH
            mkdir -p "$WORK_BASE/$NAME/$TAG/run_$RUN" "$DEST_BASE/$NAME/$TAG"
            WORK=$(mktemp -d "$WORK_BASE/$NAME/$TAG/run_$RUN/attempt_XXXXXX")
            echo "Running $NAME / $TAG / $RUN in $WORK"
            # Keep the exact recipe alongside the generated configs and logs.
            cp "$SCRIPT" "$WORK/recipe.sh"
            (cd "$WORK" && bash recipe.sh) || {
                echo "ERROR: $NAME failed; see $WORK" >&2; exit 1;
            }
            [[ -s "$WORK/result.root" ]] || { echo "ERROR: no result.root in $WORK" >&2; exit 1; }
            OUTPUT="$DEST_BASE/$NAME/$TAG/DQM_${NAME}_R$(printf '%09d' "$RUN").root"
            TEMP_OUTPUT=$(mktemp "$DEST_BASE/$NAME/$TAG/.publishing_XXXXXX")
            cp "$WORK/result.root" "$TEMP_OUTPUT"
            mv -f "$TEMP_OUTPUT" "$OUTPUT"
            echo "Saved $OUTPUT"
        done
    done
done
