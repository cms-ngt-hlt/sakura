#!/bin/bash

file_list='file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/368/00000/c38e47fd-8d7d-4f30-ab3d-08d14bb0432e.root'

cmsDriver.py expressStep2 \
             --conditions 150X_dataRun3_Express_v2 \
             -s RAW2DIGI,RECO,ALCAPRODUCER:EcalTestPulsesRaw \
             --datatier ALCARECO --eventcontent ALCARECO --data --process RERECO \
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
@EOF

cmsRun ecalPedsStep1.py >& step2.log

cmsDriver.py step3 --conditions 150X_dataRun3_Express_v2 \
         -s ALCAOUTPUT:EcalTestPulsesRaw,ALCA:PromptCalibProdEcalPedestals \
         --datatier ALCARECO \
         --eventcontent ALCARECO \
         --triggerResultsProcess RERECO \
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
process.ALCARECOEcalTestPulsesRaw.TriggerResultsTag = cms.InputTag("TriggerResults", "", "RERECO")
@EOF

cmsRun step3_ALCAOUTPUT_ALCA.py >& step3.log
