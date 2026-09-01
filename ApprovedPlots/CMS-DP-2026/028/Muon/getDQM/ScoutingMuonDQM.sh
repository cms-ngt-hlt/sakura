#!/bin/bash

BASE_EOS_DIR="/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons"
DEST_BASE_DIR="/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/DQM_090526"

TAGS=("Prompt" "NGT" "HLT")
DQM_CONFIG="DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py"

for TAG in "${TAGS[@]}"; do
    echo "===================================================="
    echo "STARTING TAG: $TAG (Scouting via XRootD)"
    echo "===================================================="

    EOS_DIR="${BASE_EOS_DIR}/${TAG}"
    DEST_DIR="${DEST_BASE_DIR}/${TAG}"

    mkdir -p "$DEST_DIR"
    FILES=$(find "$EOS_DIR" -name "*_Scouting.root" | sort | sed 's|^/eos/cms/|root://eoscms.cern.ch//eos/cms/|' | paste -sd, -)

    LOG_FILE="dqmclient_${TAG}_scouting_run.log"

    echo "    > Starting cmsRun... (Log: $LOG_FILE)"

    cmsRun "$DQM_CONFIG" inputFiles="$FILES" >& "$LOG_FILE"

    echo "Cleaning up and moving DQM files to: $DEST_DIR/"
    
    if [ -d "upload" ] && [ "$(ls -A upload)" ]; then
        mv upload/* "$DEST_DIR/" 2>/dev/null
        echo "    > DQM output files moved successfully."
    fi
    
    mv dqmclient_${TAG}_scouting_run*.log "$DEST_DIR/" 2>/dev/null

    echo "Finished processing for tag: $TAG"
    echo ""
done

echo "All tags completed successfully! <3"
