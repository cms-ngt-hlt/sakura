#!/bin/bash -ex

# cmsrel CMSSW_14_0_15_patch1
# cd CMSSW_14_0_15_patch1/src
# cmsenv                                                                                                                                                                                                    

# Get the run number from the first argument
RUN_NUMBER=386593

# Define the directory with the given run number
DIR="/eos/user/m/mzarucki/NGT/SAKURA/demonstrator/data/converted/testing/run${RUN_NUMBER}/"

# Generate a comma-separated list of the full file paths                                                                                                                                                    
FILE_LIST=$(ls "$DIR" | awk -v dir="$DIR" '{printf "    '\''%s%s'\'',\n", dir, $0}')

# Print the result                                                                                                                                                                                          
echo "$FILE_LIST"

hltConfigFromDB --runNumber ${RUN_NUMBER} > hlt_${RUN_NUMBER}.py 

cat <<EOF >> hlt_${RUN_NUMBER}.py
from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
    buBaseDir = '.',
    runNumber = ${RUN_NUMBER}
)
from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
  fileListMode = True,
  fileNames = cms.untracked.vstring(
$FILE_LIST
  )
)
process.options.wantSummary = True

process.options.numberOfThreads = 32
process.options.numberOfStreams = 24
EOF

# Run cmsRun with the generated configuration                                                                                                                                                               
mkdir -p run${RUN_NUMBER}
cmsRun hlt_${RUN_NUMBER}.py &> hlt_${RUN_NUMBER}.log
