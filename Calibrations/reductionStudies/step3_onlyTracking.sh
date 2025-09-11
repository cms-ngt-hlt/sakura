#!/bin/bash

cmsDriver.py step3 --conditions 140X_dataRun3_Express_v3 \
	-s ALCAOUTPUT:SiStripCalZeroBias+SiStripPCLHistos,ALCA:PromptCalibProd+PromptCalibProdSiStrip+PromptCalibProdSiPixelAli+PromptCalibProdSiStripGains+PromptCalibProdSiStripGainsAAG+PromptCalibProdSiPixel+PromptCalibProdSiStripHitEff+PromptCalibProdSiPixelAliHG \
	--datatier ALCARECO --eventcontent ALCARECO --triggerResultsProcess RECO -n -1 \
	--filein file:step2_onlyTracking.root --no_exec --fileout file:step3_onlyTracking.root --python_filename step3_ALCAOUTPUT_ALCA_onlyTracking.py

cat <<@EOF>> step3_ALCAOUTPUT_ALCA_onlyTracking.py
process.options.numberOfStreams = 8
process.options.numberOfThreads = 8

process.load('HLTrigger.Timer.FastTimerService_cfi')

process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_tracking_upperbound_s3_onlyTracking.json"

@EOF

cmsRun step3_ALCAOUTPUT_ALCA_onlyTracking.py
