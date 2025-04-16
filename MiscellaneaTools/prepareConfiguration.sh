#!/bin/bash -ex

hltGetConfiguration /dev/CMSSW_14_1_0/GRun \
   --globaltag GLOBALTAG_TEMPLATE \
   --data \
   --output minimal \
   --max-events -1 \
   --eras Run3_2024 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_3_0_xml \
   --input FILEINPUT_TEMPLATE  > hltData.py

cat <<@EOF >> hltData.py

## put here the output commands of the OnlineMonitor PD
process.hltOutputMinimal.outputCommands = [
    'drop *',
    'keep *_hltDoubletRecoveryPFlowTrackSelectionHighPurity_*_*',
    'keep *_hltEcalRecHit_*_*',
    'keep *_hltEgammaCandidates_*_*',
    'keep *_hltEgammaGsfTracks_*_*',
    'keep *_hltGlbTrkMuonCandsNoVtx_*_*',
    'keep *_hltHbhereco_*_*',
    'keep *_hltHfreco_*_*',
    'keep *_hltHoreco_*_*',
    'keep *_hltIter0PFlowCtfWithMaterialTracks_*_*',
    'keep *_hltIter0PFlowTrackSelectionHighPurity_*_*',
    'keep *_hltL3NoFiltersNoVtxMuonCandidates_*_*',
    'keep *_hltMergedTracks_*_*',
    'keep *_hltPFMuonMerging_*_*',
    'keep *_hltOnlineBeamSpot_*_*',
    'keep *_hltPixelTracks_*_*',
    'keep *_hltPixelVertices_*_*',
    'keep *_hltSiPixelClusters_*_*',
    'keep *_hltSiStripRawToClustersFacility_*_*',
    'keep *_hltTrimmedPixelVertices_*_*',
    'keep *_hltVerticesPFFilter_*_*',
    'keep FEDRawDataCollection_rawDataCollector_*_*',
    'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_*',
    'keep edmTriggerResults_*_*_*',
    'keep triggerTriggerEvent_*_*_*' 
]

#process.hltOutputMinimal.SelectEvents = cms.untracked.PSet(  SelectEvents = cms.vstring( 'Dataset_OnlineMonitor' ) )

#process.PrescaleService.lvl1DefaultLabel = "2p0E34"
#process.PrescaleService.forceDefault = True

# write the timing summary
#process.FastTimerService.jsonFileName = "resources.json"
#process.FastTimerService.writeJSONSummary = True

# set the process parameters
process.options.numberOfConcurrentLuminosityBlocks = 2      # default: 2
process.options.numberOfStreams = 32                        # default: 32
process.options.numberOfThreads = 32                        # default: 32

#del process.MessageLogger
#process.load('FWCore.MessageLogger.MessageLogger_cfi')
@EOF

edmConfigDump hltData.py > config.py

#cmsRun hltData.py >& hltData.log
