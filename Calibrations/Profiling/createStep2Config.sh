#!/bin/bash

# Check if we are in a CMSSW environment
if [[ -z "$CMSSW_BASE" ]]; then
  echo "Error: CMSSW environment not set. Please run 'cmsenv' inside your CMSSW release area."
  exit 1
fi

# Default values
PU=""
doTrimming=0

usage() {
  echo "Usage: $0 --PU [31|40|60] [--doTrimming]"
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --PU)
      PU="$2"
      shift 2
      ;;
    --doTrimming)
      doTrimming=1
      shift
      ;;
    *)
      echo "Unknown option: $1"
      usage
      ;;
  esac
done

if [[ -z "$PU" ]]; then
  echo "Error: PU value is required."
  usage
fi

# Select input directory depending on PU
case "$PU" in
  31)
    dir="/eos/cms/store/group/tsg-phase2/user/jprendi/repacked_397186_ls0048"
    ;;
  40)
    dir="/eos/cms/store/group/tsg-phase2/user/tomei/repacked/run386925"
    ;;
  60)
    dir="/eos/cms/store/group/tsg-phase2/user/jprendi/repacked_397383_ls0460_ls0480"
    ;;
  *)
    echo "Error: unsupported PU=$PU (valid: 31,40,60)"
    exit 1
    ;;
esac

sep=","
file_list=$(xrdfs root://eoscms.cern.ch/ ls "$dir" \
  | sort -V \
  | sed 's|/eos/cms||' \
  | paste -sd "$sep" -)

echo "Using PU=$PU"
echo "Input directory: $dir"
echo "doTrimming=$doTrimming"
echo "Files: $file_list"

# Decide on procModifiers and output filename
extraArgs=""
outFile="expressStep2_RAW2DIGI_RECO_ALCAPRODUCER_config.py"
if [[ $doTrimming -eq 1 ]]; then
  extraArgs="--procModifiers trackingIters01"
  outFile="expressStep2_RAW2DIGI_RECO_ALCAPRODUCER_trimmed_config.py"
fi

cmsDriver.py expressStep2 \
         --conditions 140X_dataRun3_Express_v3 \
         -s RAW2DIGI,RECO,ALCAPRODUCER:SiStripPCLHistos+SiStripCalZeroBias+SiStripCalMinBias+SiStripCalMinBiasAAG+TkAlMinBias+SiPixelCalZeroBias+SiPixelCalSingleMuon+SiPixelCalSingleMuonTight+TkAlZMuMu \
         --datatier ALCARECO --eventcontent ALCARECO --data --process RECO \
         --scenario pp --era Run3 \
         --nThreads 8 \
         --nStreams 8 \
         $extraArgs \
         -n -1 --filein "$file_list" \
         --fileout file:step2.root --no_exec \
         --python_filename "$outFile"

cat <<@EOF>> "$outFile"
process.load('HLTrigger.Timer.FastTimerService_cfi')
process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_tracking_upperbound_s2.json"

import re
genericConsumerCfg = [k.replace('keep ', '') for k in process.ALCARECOoutput.outputCommands if re.match('^keep.*', k)]

process.genericConsumerALCARECOOutput = cms.EDAnalyzer("GenericConsumer",
          eventProducts = cms.untracked.vstring(genericConsumerCfg),
          verbose = cms.untracked.bool(True)
          )

process.ALCARECOoutput_step = cms.EndPath(process.genericConsumerALCARECOOutput)
@EOF

# Run step (optional)
# cmsRun "$outFile" >& step2.log
