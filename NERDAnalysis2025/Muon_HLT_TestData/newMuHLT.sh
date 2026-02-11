#!/bin/bash -ex

#INPUT_FILES=$(cat run_398802.txt | tr -d '\r' | tr '\n' ',' | sed 's/,$//')
		   # --input "${INPUT_FILES}" \
hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V119 \
		    --globaltag 150X_dataRun3_NGT_v2 \
		    --data \
		    --unprescale \
		    --output none \
		    --max-events -1 \
		    --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
		    --input " " \
		    --paths Dataset_TestDataRaw,LocalTestDataRawOutput,Dataset_TestDataScouting,LocalTestDataScoutingOutput,DST_PFScouting*,HLT_TestData_v*,HLTriggerFinalPath,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*,HLT_IsoMu24_v* \
		    > newMumu.py

cat <<@EOF >> newMumu.py
# filter on the input event trigger results
process.hltTestDataInInputFilter = cms.EDFilter("TriggerResultsFilter",
    hltResults = cms.InputTag("TriggerResults","","HLT"),
    l1tIgnoreMaskAndPrescale = cms.bool(False),
    l1tResults = cms.InputTag(""),
    throw = cms.bool(False),
    triggerConditions = cms.vstring('HLT_TestData_v*'),
    usePathStatus = cms.bool(False)
)
process.HLTBeginSequenceTestData += process.hltTestDataInInputFilter

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

edmConfigDump newMumu.py >& newMumuMassConfig.py

