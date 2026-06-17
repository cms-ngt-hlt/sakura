#!/bin/bash

TAGS=("Prompt" "HLT" "NGT")
BASE_DIR="/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas"

for TAG in "${TAGS[@]}"; do
    echo "===================================================="
    echo "STARTING TAG: $TAG"
    echo "===================================================="

    EOS_DIR="${BASE_DIR}/${TAG}"
    mkdir -p "$TAG"

    echo "Scanning for runs in $EOS_DIR..."
    RUNS=$(find "$EOS_DIR" -maxdepth 1 -name "*_run_*Raw.root" | grep -o 'run_[0-9]*' | sort -u | cut -d_ -f2)

    if [ -z "$RUNS" ]; then
        echo "No runs found for tag $TAG. Skipping..."
        continue
    fi

    echo "Found runs: $RUNS"
    echo "----------------------------------------------------"

    for RUN in $RUNS; do
        echo "--> Processing RUN: $RUN (Tag: $TAG)"

        FILES=$(find "$EOS_DIR" -maxdepth 1 -name "*_run_${RUN}_*Raw.root" | sort | sed 's|^/eos/cms/|root://eoscms.cern.ch//eos/cms/|' | paste -sd, -)
        LOG_FILE="dqmclient_${TAG}_run${RUN}.log"
        cmsRun DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py inputFiles="$FILES" >& "$LOG_FILE"

        echo "--> Finished Run $RUN. Log: $LOG_FILE"
    done

    echo "Moving results for $TAG to local folder..."
    
    mv dqmclient_${TAG}_run*.log "/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/DQM_Raws/$TAG/"
    mv upload/DQM* "/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/DQM_Raws/$TAG/" 2>/dev/null

    echo "Finished processing all runs for $TAG."
    echo "----------------------------------------------------"
done

echo "All tags completed!"
