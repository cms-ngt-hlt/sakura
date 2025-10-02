#!/bin/bash

file_list='file:outputLocalTestDataRaw.root'

cmsDriver.py expressStep2 \
             --conditions 150X_dataRun3_Express_v2 \
             -s RAW2DIGI,RECO,ALCAPRODUCER:EcalTestPulsesRaw \
             --datatier ALCARECO --eventcontent ALCARECO --data --process RECO \
             --scenario pp --era Run3 \
             --nThreads 8 \
             --nStreams 8 \
             -n -1 --filein "$file_list" \
             --fileout file:step2.root --no_exec \
             --python_filename ecalPedsStep1.py

cat <<@EOF>> ecalPedsStep1.py
process.load('HLTrigger.Timer.FastTimerService_cfi')
process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_ECALpeds.json"
process.ALCARECOEcalTestPulsesRawHLT.HLTPaths=['HLT_EcalCalibration_v*','HLT_HcalCalibration_v*']
process.OutALCARECOEcalTestPulsesRaw.outputCommands = cms.untracked.vstring('keep  FEDRawDataCollection_*_*_*',
                                        'keep  edmTriggerResults_*_*_*')
@EOF

cmsRun ecalPedsStep1.py >& step2.log

cmsDriver.py step3 --conditions 150X_dataRun3_Express_v2 \
         -s ALCAOUTPUT:EcalTestPulsesRaw,ALCA:PromptCalibProdEcalPedestals \
         --datatier ALCARECO \
         --eventcontent ALCARECO \
         --triggerResultsProcess RECO \
         -n -1 \
         --filein file:step2.root \
         --no_exec \
         --fileout file:step3.root

cat <<@EOF>> step3_ALCAOUTPUT_ALCA.py
process.options.numberOfStreams = 8
process.options.numberOfThreads = 8
process.load('HLTrigger.Timer.FastTimerService_cfi')
process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_ECALpeds_ALCAOUTPUT.json"
@EOF

cmsRun step3_ALCAOUTPUT_ALCA.py >& step3.log
