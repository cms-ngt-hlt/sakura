#!/bin/bash
eval `scramv1 runtime -sh`
CMSSW_DIR=${CMSSW_BASE}/src/

if [ -d $CMSSW_DIR/outfiles ]; then
    echo "$CMSSW_DIR/outfiles already exists, skipping"
else
    mkdir $CMSSW_DIR/outfiles
fi

# Define an array
scenarios=('test_PromptGT_ReHLT_PromptGT') # 'test_PromptGT_ReHLT_HLTGT')

# Loop over the array and print each element
for scenario in "${scenarios[@]}"
do
  echo "$scenario"
  condor_submit par1=${scenario} par2=${CMSSW_DIR} submit.sub
done
