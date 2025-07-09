#!/bin/bash

# input files are available at /eos/cms/store/group/tsg-phase2/user/jprendi/CMSSW_14_0_18_patch1/src/C/repacked

file_list=$(ls repacked_*.root | awk '{print "file:"$0}' | paste -sd, -)

cmsDriver.py expressStep2 --conditions 140X_dataRun3_Express_v3 \
-s RAW2DIGI,RECO,ALCAPRODUCER:SiStripPCLHistos+SiStripCalZeroBias+SiStripCalMinBias+SiStripCalMinBiasAAG+TkAlMinBias+SiPixelCalZeroBias+SiPixelCalSingleMuon+SiPixelCalSingleMuonTight+TkAlZMuMu \
--datatier ALCARECO --eventcontent ALCARECO --data --process RECO \
--scenario pp --era Run3 \
--customise Configuration/DataProcessing/RecoTLR.customiseExpress \
-n -1 --filein "$file_list" \
--fileout file:step2.root --no_exec

cat <<@EOF>> expressStep2_RAW2DIGI_RECO_ALCAPRODUCER.py
process.options.numberOfStreams = 8
process.options.numberOfThreads = 8

process.load('HLTrigger.Timer.FastTimerService_cfi')

process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_tracking_upperbound_s2.json"

@EOF


cmsDriver.py step3 --conditions 140X_dataRun3_Express_v3 \
-s ALCAOUTPUT:SiStripCalZeroBias+SiStripPCLHistos,ALCA:PromptCalibProd+PromptCalibProdSiStrip+PromptCalibProdSiPixelAli+PromptCalibProdSiStripGains+PromptCalibProdSiStripGainsAAG+PromptCalibProdSiPixel+PromptCalibProdSiPixelLA+PromptCalibProdSiStripHitEff+PromptCalibProdSiPixelAliHG+PromptCalibProdSiPixelAliHGComb \
--datatier ALCARECO --eventcontent ALCARECO --triggerResultsProcess RECO -n -1 \
--filein file:step2.root --no_exec --fileout file:step3.root

cat <<@EOF>> step3_ALCAOUTPUT_ALCA.py
process.options.numberOfStreams = 8
process.options.numberOfThreads = 8

process.load('HLTrigger.Timer.FastTimerService_cfi')

process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_tracking_upperbound_s3.json"

@EOF
