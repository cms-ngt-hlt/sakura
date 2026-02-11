#!/bin/bash -ex

#INPUT_FILES=$(cat run_398802.txt | tr -d '\r' | tr '\n' ',' | sed 's/,$//')

hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V119 \
		    --globaltag 150X_dataRun3_NGT_v2 \
		    --data \
		    --unprescale \
		    --output none \
		    --max-events -1 \
		    --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
		    --input " " \
		    --paths Dataset_TestDataRaw,LocalTestDataRawOutput,Dataset_TestDataScouting,LocalTestDataScoutingOutput,DST_PFScouting*,HLT_TestData_v*,HLTriggerFinalPath,HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v* \
		    > fullstatsEgamma.py

cat <<@EOF >> fullstatsEgamma.py
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

