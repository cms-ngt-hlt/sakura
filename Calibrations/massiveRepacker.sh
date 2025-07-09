#!/bin/bash -ex

# Set the environment
# export $SCRAM_ARCH=el8_amd64_gcc12
# cmsrel CMSSW_14_0_18_patch1
# cd CMSSW_14_0_18_patch1/src
# cmsenv
# voms-proxy-init --voms cms

# Get the list of files
eos ls -lh /store/t0streamer/Data/Calibration/000/386/925 |\
awk '{print $10}' |\
sed 's!run!/store/t0streamer/Data/Calibration/000/386/925/run!g' \
> run386926Streamers.txt

input_list="run386926Streamers.txt"

# Write repacking script dynamically to file
cat << 'EOF' > repacker_cfg.py
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.parseArguments()

process = cms.Process( 'REPACK' )

process.source = cms.Source("NewEventStreamFileReader", # T0 source (streamer .dat)
                            fileNames = cms.untracked.vstring(options.inputFiles))

process.output = cms.OutputModule( 'PoolOutputModule',
    fileName = cms.untracked.string( options.outputFile ),
    outputCommands = cms.untracked.vstring( 'keep *' )
)

process.options.numberOfThreads = 8
process.options.numberOfStreams = 8

process.endPath = cms.EndPath( process.output )
EOF

while read -r line; do
  # Skip empty lines and comments
  [[ -z "$line" || "$line" =~ ^# ]] && continue

  # Extract base name and replace extension
  datfile="$line"
  base=$(basename "$datfile")
  rootfile="${base%.dat}.root"

  echo "Processing: $datfile -> $rootfile"

  cmsRun repacker_cfg.py inputFiles="$datfile" outputFile="$rootfile"

done < "$input_list"
