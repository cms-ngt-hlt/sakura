#!/bin/bash

# Set constants
SCRIPT_PATH="/afs/cern.ch/user/j/jprendi/LCtimeseries/src/hltSub/cmsCondorDataFiles.py"
CFG_FILE="/afs/cern.ch/user/j/jprendi/dump.py"
CMSSW_SRC="/afs/cern.ch/user/j/jprendi/LCtimeseries/src/"
PROXY="/afs/cern.ch/user/j/jprendi/LCtimeseries/src/x509up_u167055"
FILELIST_DIR="/afs/cern.ch/user/j/jprendi/LCtimeseries/src/hltSub/"
EOS_BASE="/eos/cms/store/group/tsg-phase2/user/jprendi/Pr_Run2024I_386"

# Loop over all fileList_*.txt
for file in "$FILELIST_DIR"/fileList_*.txt; do
    # Extract the number from the filename
    filename=$(basename -- "$file")
    file_number="${filename#fileList_}"
    file_number="${file_number%.txt}"

    folder_name="${file_number}_off"
    eos_path="${EOS_BASE}${file_number}"

    echo ""
    echo "========================================"
    echo "Processing fileNumber: $file_number"
    echo "Creating folder: $folder_name"
    echo "EOS path: $eos_path"
    echo "========================================"

    # Create and move into working directory
    mkdir -p "$folder_name"
    cd "$folder_name" || exit 1

    python3 "$SCRIPT_PATH" \
      "$CFG_FILE" \
      "$CMSSW_SRC" \
      "$eos_path" \
      -p "$PROXY" \
      -q tomorrow \
      -n 20 \
      --fileNumber "$file_number"

    condor_submit condor_cluster.sub
    cd ..  
done

