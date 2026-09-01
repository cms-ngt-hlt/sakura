#!/bin/bash

TAGS=(
  "150X_dataRun3_NGT_v2"
  "150X_dataRun3_HLT_v1"
  "150X_dataRun3_Prompt_v3"
)

for TAG in "${TAGS[@]}"; do
    echo "Processing Global Tag: $TAG"
    
    CONFIG_FILE="MuFullStats_${TAG}.py"
    DUMP_FILE="MuFullStatsConfig_${TAG}.py"

    hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V119 \
        --globaltag "$TAG" \
        --data \
        --unprescale \
        --output none \
        --max-events -1 \
        --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
        --input " " \
        --paths Dataset_TestDataRaw,LocalTestDataRawOutput,Dataset_TestDataScouting,LocalTestDataScoutingOutput,DST_PFScouting*,HLT_TestData_v*,HLTriggerFinalPath,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*,HLT_IsoMu24_v* \
        > "$CONFIG_FILE"

    cat <<@EOF >> "$CONFIG_FILE"
process.hltOutputLocalTestDataRaw.outputCommands = [
   'drop *',
   'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
   'keep edmTriggerResults_*_*_HLTX',
   'keep triggerTriggerEvent_*_*_HLTX'
]

process.options.wantSummary = True
@EOF

    edmConfigDump "$CONFIG_FILE" >& "$DUMP_FILE"
    
    echo "Done. Created $DUMP_FILE"
    echo "-----------------------------------"
done
