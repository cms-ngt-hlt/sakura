#!/bin/bash -ex

# cmsrel CMSSW_15_0_17
# cd CMSSW_15_0_17/src
# cmsenv

hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V119 \
		    --globaltag 150X_dataRun3_NGT_v2 \
		    --data \
		    --unprescale \
		    --output none \
		    --max-events -1 \
		    --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
		    --input /store/data/Run2025G/EGamma1/RAW-RECO/ZElectron-PromptReco-v1/000/398/858/00000/42288e8b-fdfc-4369-96e7-0ab2b9ab0dff.root \
		    --paths Dataset_TestDataRaw,LocalTestDataRawOutput,Dataset_TestDataScouting,LocalTestDataScoutingOutput,DST_PFScouting*,HLT_TestData_v* \
		    > test.py

cat <<@EOF >> test.py
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
process.hltOutputLocalTestDataScouting.outputCommands = [
    'drop *',
    'keep *_hltFEDSelectorL1_*_HLTX',
    'keep *_hltScoutingEgammaPacker_*_HLTX',
    'keep *_hltScoutingMuonPackerNoVtx_*_HLTX',
    'keep *_hltScoutingMuonPackerVtx_*_HLTX',
    'keep *_hltScoutingPFPacker_*_HLTX',
    'keep *_hltScoutingPrimaryVertexPacker_*_HLTX',
    'keep *_hltScoutingRecHitPacker_*_HLTX',
    'keep *_hltScoutingTrackPacker_*_HLTX',
    'keep edmTriggerResults_*_*_HLTX'
]

# make summary avaliable
process.options.wantSummary = True
@EOF

cmsRun test.py >& test.log
