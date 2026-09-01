#!/bin/bash

SCRIPT_PATH="$(pwd)/cmsCondorDataFiles.py"
PROXY="/afs/cern.ch/user/j/jprendi/CMSSW_15_0_17/src/x509up_u167055"
EOS_DEST="/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas"

TESTS=(
    "NGT" "fullstatsEgammaConfig_NGT.py"
    "HLT" "fullstatsEgammaConfig_HLT.py"
    "Prompt" "fullstatsEgammaConfig_Prompt.py"
)

for ((i=0; i<${#TESTS[@]}; i+=2)); do
    TAG=${TESTS[i]}
    CFG=${TESTS[i+1]}

    for list_file in run_*.txt; do
        RUN=$(basename "$list_file" | sed 's/run_//;s/.txt//')
        LOCAL_DIR="Jobs_${TAG}_Run_${RUN}"
        
        echo ">>> Submitting $TAG for Run $RUN..."
        mkdir -p "$LOCAL_DIR" && cd "$LOCAL_DIR" || exit

        python3 "$SCRIPT_PATH" \
            "../$CFG" \
            "$CMSSW_BASE/src/" \
            "$EOS_DEST" \
            -p "$PROXY" \
            -n 1 \
            --inputList "../$list_file" \
            --outPrefix "run_${RUN}" \
            --jobTag "$TAG"

        condor_submit condor_cluster.sub
        cd ..
    done
done
