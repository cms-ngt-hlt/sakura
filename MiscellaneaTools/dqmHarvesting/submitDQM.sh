#!/bin/bash 

# Check if the folder path argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <eos_directory_path>"
  exit 1
fi

# Define the EOS directory path (passed as the first argument)
EOS_DIR=/eos/cms/store/group/tsg-phase2/user/musich/test_out/$1

# List files in the EOS directory and construct the inputFiles argument
# Here we use xargs to construct a comma-separated list
INPUT_FILES=$(eos ls "$EOS_DIR" | awk -v dir="$EOS_DIR" '{print "root://eoscms.cern.ch/"dir"/"$0}' | paste -sd, -)

echo $INPUT_FILES

#export X509_USER_PROXY=/afs/cern.ch/work/m/musich/public/2024DataAnalysis/NGT/CMSSW_14_2_0_pre3/src/.user_proxy 
echo  "Job started at " `date`
CMSSW_DIR=$2

OUT_DIR=/eos/cms/store/group/tsg-phase2/user/musich/test_out/$1
LXBATCH_DIR=$PWD 
cd ${CMSSW_DIR} 
eval `scramv1 runtime -sh` 
echo "batch dir: $LXBATCH_DIR release: $CMSSW_DIR release base: $CMSSW_RELEASE_BASE" 
cd $LXBATCH_DIR 
cp /afs/cern.ch/work/m/musich/public/2024DataAnalysis/NGT/CMSSW_14_2_0_pre3/src/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py .

echo "cmsRun hlt_dqm_sourceclient-live_cfg.py"

# Run the cmsRun command with the constructed inputFiles list
cmsRun hlt_dqm_sourceclient-live_cfg.py inputFiles=$INPUT_FILES

echo "Content of working dir is "`ls -lh upload` 
for RootOutputFile in $(ls upload/*root ); do xrdcp -f ${RootOutputFile} root://eoscms/${OUT_DIR}/${RootOutputFile} ; done 
echo  "Job ended at " `date` 
exit 0 
