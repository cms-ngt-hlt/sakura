#!/bin/bash

# Set the environment
export $SCRAM_ARCH=el8_amd64_gcc12
CMSSW_VERSION="CMSSW_14_0_18_patch1"
if [ -d "$CMSSW_VERSION" ]; then
  echo "Directory $CMSSW_VERSION already exists. Skipping scram project."
else
  scram p CMSSW $CMSSW_VERSION
fi

cd $CMSSW_VERSION/src
eval `scram runtime -sh`
voms-proxy-init --voms cms

# Get the configuration files
wget -O ecalPedestalPCL_step1_cfg.py https://github.com/cms-sw/cmssw/raw/refs/heads/CMSSW_14_0_X/Calibration/EcalCalibAlgos/test/ecalPedestalPCL_step1_cfg.py
wget -O ecalPedestalPCL_step2_cfg.py https://github.com/cms-sw/cmssw/raw/refs/heads/CMSSW_14_0_X/Calibration/EcalCalibAlgos/test/ecalPedestalPCL_step2_cfg.py

# The streamer files are available in here 
# `eos ls -lh /store/t0streamer/Data/Calibration/000/386/925`
# We have to hack the ecalPedestalPCL_step1_cfg.py to read those files

# Get the list of files
eos ls -lh /store/t0streamer/Data/Calibration/000/386/925 |\
awk '{print $10}' |\
sed 's!run!/store/t0streamer/Data/Calibration/000/386/925/run!g' \
> run386926Streamers.txt

# A bit of twiddling to get around the SwitchProducer
sed 's/process.ecalDigis.InputLabel/process.ecalDigis.cpu.InputLabel/g' \
< ecalPedestalPCL_step1_cfg.py > tmp.py
mv tmp.py ecalPedestalPCL_step1_cfg.py

# Now do the hacking
cat <<EOF >> ecalPedestalPCL_step1_cfg.py
with open("run386926Streamers.txt") as f: 
	myFileNamesTuple = tuple(f.read().splitlines())

process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring(*myFileNamesTuple)
)

process.GlobalTag = GlobalTag(process.GlobalTag, '140X_dataRun3_Express_v3', '')
EOF

# Not go crazy
cat <<EOF >> ecalPedestalPCL_step1_cfg.py
process.MessageLogger.cerr.FwkReport.reportEvery = 500

process.options.numberOfStreams = 8
process.options.numberOfThreads = 8

process.load('HLTrigger.Timer.FastTimerService_cfi')

process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_ecalped_s1.json"
EOF

# This should work to produce OUT_step1.root
# Should take half an hour
cmsRun ecalPedestalPCL_step1_cfg.py

# Now fix ecalPedestalPCL_step2_cfg.py
cat <<EOF >> ecalPedestalPCL_step2_cfg.py
process.GlobalTag = GlobalTag(process.GlobalTag, '140X_dataRun3_Express_v3', '')
process.load('HLTrigger.Timer.FastTimerService_cfi')

process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_ecalped_s2.json"
EOF

# And this will produce MyPedestals.db
cmsRun ecalPedestalPCL_step2_cfg.py

# And check that it exists
conddb --db MyPedestals.db list myPedestal_test
