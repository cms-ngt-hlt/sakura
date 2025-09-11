#!/bin/bash -ex

dir="/eos/user/j/jprendi/repacked_files"
prefix="file:"
sep=","

file_list=$(ls "$dir"/repacked_*.root | sort -V | sed "s|^|$prefix|" | paste -sd "$sep" -)

cmsDriver.py expressStep2 \
         --conditions 140X_dataRun3_Express_v3 \
         -s RAW2DIGI,RECO:reconstruction_trackingOnly,ALCAPRODUCER:SiStripPCLHistos+SiStripCalZeroBias+SiStripCalMinBias+SiStripCalMinBiasAAG+TkAlMinBias+SiPixelCalZeroBias \
         --datatier ALCARECO --eventcontent ALCARECO --data --process RECO \
         --scenario pp --era Run3 \
         --nThreads 8 \
         --nStreams 8 \
         --procModifiers trackingIters01 \
         -n -1 --filein "$file_list" \
         --fileout file:step2_onlyTracking.root --no_exec \
         --python_filename expressStep2_RAW2DIGI_RECO_ALCAPRODUCER_onlyTracking.py

##--customise RecoTracker/MkFit/customizeInitialStepOnly.customizeInitialStepOnly \


cat <<@EOF>> expressStep2_RAW2DIGI_RECO_ALCAPRODUCER_onlyTracking.py
process.load('HLTrigger.Timer.FastTimerService_cfi')
process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_tracking_upperbound_s2_onlyTracking.json"
@EOF

#cmsRun expressStep2_RAW2DIGI_RECO_ALCAPRODUCER_onlyTracking.py >& step2_onlyTracking.log
