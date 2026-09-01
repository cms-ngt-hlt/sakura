#!/bin/bash
# 04_run_dqm.sh — run the DQM clients over the staged HLT/Prompt/NGT outputs.
# Meant to be run inside tmux because it takes quite a while
#   tmux new -d -s dqm 'bash 04_run_dqm.sh 2>&1 | tee dqm_master.log; exec bash'
#
# By default processes all TAGS x STREAMS from pipeline.cfg
# Pass --tag <TAG> and/or --stream <STREAM> to restrict to a single value,
# e.g. for running one (tag, stream) combo per node in parallel:
#   bash 04_run_dqm.sh --tag HLT --stream LocalTestDataRaw
set -uo pipefail
cd "$(dirname "$0")"
source ./pipeline.cfg

ARG_TAG=""
ARG_STREAM=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --tag) ARG_TAG="$2"; shift 2 ;;
        --stream) ARG_STREAM="$2"; shift 2 ;;
        *) echo "ERROR: unknown argument '$1'"; exit 1 ;;
    esac
done

if [ -n "$ARG_TAG" ]; then
    tag_ok=false
    for t in "${TAGS[@]}"; do [ "$t" = "$ARG_TAG" ] && tag_ok=true; done
    [ "$tag_ok" = true ] || { echo "ERROR: --tag '$ARG_TAG' not in TAGS=(${TAGS[*]})"; exit 1; }
    RUN_TAGS=("$ARG_TAG")
else
    RUN_TAGS=("${TAGS[@]}")
fi

if [ -n "$ARG_STREAM" ]; then
    stream_ok=false
    for s in "${STREAMS[@]}"; do [ "$s" = "$ARG_STREAM" ] && stream_ok=true; done
    [ "$stream_ok" = true ] || { echo "ERROR: --stream '$ARG_STREAM' not in STREAMS=(${STREAMS[*]})"; exit 1; }
    RUN_STREAMS=("$ARG_STREAM")
else
    RUN_STREAMS=("${STREAMS[@]}")
fi

[ -n "${CMSSW_BASE:-}" ] || { echo "ERROR: cmsenv not active (CMSSW_BASE unset)"; exit 1; }
mkdir -p "$DQM_DEST_BASE"
mkdir -p upload   # DQMFileSaverOnline writes here and does not create it itself

for TAG in "${RUN_TAGS[@]}"; do
    echo "===================================================="
    echo "STARTING TAG: $TAG"
    echo "===================================================="

    SRC_DIR="${EOS_BASE}/${TAG}"
    DEST_DIR="${DQM_DEST_BASE}/${TAG}"
    LOG_DIR="${DQM_DEST_BASE}/DQM_logs/${TAG}"
    mkdir -p "$DEST_DIR" "$LOG_DIR"

    for STREAM in "${RUN_STREAMS[@]}"; do
        if [ "$STREAM" = "LocalTestDataRaw" ]; then
            CFG="${CMSSW_SRC}/${DQM_HLT_CFG}"
        elif [ "$STREAM" = "DQMTestDataScouting" ]; then
            CFG="${CMSSW_SRC}/${DQM_SCOUTING_CFG}"
        else
            echo "ERROR: no DQM config mapped for stream '$STREAM'"; exit 1
        fi

        echo "--- Stream: $STREAM  (config: $CFG)"

        RUNS=$(find "$SRC_DIR" -name "${TAG}_run*_job*_${STREAM}.root" \
                   | sed -n "s/.*run\([0-9]\+\)_job.*/\1/p" | sort -un)
        echo "    Found runs: $RUNS"

        for RUN in $RUNS; do
            echo "    --> Processing run $RUN"
            FILES=$(find "$SRC_DIR" -name "${TAG}_run${RUN}_job*_${STREAM}.root" \
                        | sort | sed "s|^${SRC_DIR}|${EOS_XRD}/${SRC_DIR}|" | paste -sd, -)
            LOG_FILE="dqmclient_${TAG}_${STREAM}_run${RUN}.log"

            cmsRun "$CFG" inputFiles="$FILES" >& "$LOG_FILE"
            echo "    <-- Finished run $RUN (log: $LOG_FILE)"
        done
    done

    echo "Moving DQM output for $TAG -> $DEST_DIR/"
    if [ -d upload ] && [ -n "$(ls -A upload 2>/dev/null)" ]; then
        mv upload/* "$DEST_DIR/"
    else
        echo "    WARNING: upload/ empty or missing for tag $TAG"
    fi
    mv "dqmclient_${TAG}_"*.log "$LOG_DIR/" 2>/dev/null || true

    echo "Finished tag: $TAG"
    echo ""
done

echo "All done."
