#!/bin/bash -ex

tags=("NGT" "HLT" "Prompt")
gtags=("150X_dataRun3_NGT_v2" "150X_dataRun3_HLT_v1" "150X_dataRun3_Prompt_v3")

for i in ${!tags[@]}; do
    tag=${tags[$i]}
    gt=${gtags[$i]}

    hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V119 \
		    --globaltag ${gt} \
		    --data \
		    --unprescale \
		    --output none \
		    --max-events -1 \
		    --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
		    --input " " \
		    --paths Dataset_TestDataRaw,LocalTestDataRawOutput,Dataset_TestDataScouting,LocalTestDataScoutingOutput,DST_PFScouting*,HLT_TestData_v*,HLTriggerFinalPath,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v* \
		    > fullstatsEgamma_${tag}.py

    cat <<@EOF >> fullstatsEgamma_${tag}.py
# customize the output modules
process.hltOutputLocalTestDataRaw.outputCommands = [
   'drop *',
   'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
   'keep edmTriggerResults_*_*_HLTX',
   'keep triggerTriggerEvent_*_*_HLTX'
]

# make summary avaliable
process.options.wantSummary = True
@EOF

    edmConfigDump fullstatsEgamma_${tag}.py > fullstatsEgammaConfig_${tag}.py
done
