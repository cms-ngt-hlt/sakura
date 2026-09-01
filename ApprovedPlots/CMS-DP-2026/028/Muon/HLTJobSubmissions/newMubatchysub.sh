#!/bin/bash

SCRIPT_PATH="/afs/cern.ch/user/j/jprendi/CMSSW_15_0_17/src/cmsCondorDataFiles.py"
CMSSW_SRC="/afs/cern.ch/user/j/jprendi/CMSSW_15_0_17/src/"
PROXY="/afs/cern.ch/user/j/jprendi/CMSSW_15_0_17/src/x509up_u167055"
FILELIST_DIR="/afs/cern.ch/user/j/jprendi/CMSSW_15_0_17/src"

BASE_EOS_DEST="/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons"

# Specific file configuration
INPUT_FILE="dimulist.txt"
BATCH_BASE_NAME="MuList_Submission"

declare -A TAG_MAP
TAG_MAP["NGT"]="150X_dataRun3_NGT_v2"
TAG_MAP["HLT"]="150X_dataRun3_HLT_v1"
TAG_MAP["Prompt"]="150X_dataRun3_Prompt_v3"

TAGS_TO_RUN=("NGT" "HLT" "Prompt")

for short_tag in "${TAGS_TO_RUN[@]}"; do

    full_gt="${TAG_MAP[$short_tag]}"

    echo "========================================================"
    echo "STARTING SUBMISSION FOR: $short_tag"
    echo "FULL GLOBAL TAG IS:      $full_gt"
    echo "========================================================"

    CFG_FILE="${CMSSW_SRC}/MuFullStatsConfig_${full_gt}.py"

    CURRENT_EOS_DEST="${BASE_EOS_DEST}/${short_tag}"
    
    local_folder="Jobs_${BATCH_BASE_NAME}_${short_tag}"

    echo "Config File:     $CFG_FILE"
    echo "Local Folder:    $local_folder"
    echo "EOS Destination: $CURRENT_EOS_DEST"

    mkdir -p "$local_folder"
    cd "$local_folder" || exit

    python3 "$SCRIPT_PATH" \
      "$CFG_FILE" \
      "$CMSSW_SRC" \
      "$CURRENT_EOS_DEST" \
      -p "$PROXY" \
      -q workday \
      -n 1 \
      --inputList "$FILELIST_DIR/$INPUT_FILE" \
      --outPrefix "${BATCH_BASE_NAME}_${short_tag}" \
      --jobTag "$short_tag"

    if [ -f "condor_cluster.sub" ]; then
        condor_submit condor_cluster.sub
    else
        echo "Warning: condor_cluster.sub was not generated for $short_tag."
    fi

    cd ..
    
    echo "--------------------------------------------------------"
    echo "Finished submission for $short_tag"
    echo ""

done

echo "All submissions complete. Check 'condor_q' for status."
