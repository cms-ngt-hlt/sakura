#!/bin/bash

echo "Hello World"
echo "Running job $1"
echo "$HOSTNAME"
export STARTINGDIR="$PWD"
### First we setup the initial CMS environment
ls /cvmfs/cms.cern.ch/
source /cvmfs/cms.cern.ch/cmsset_default.sh
export EOS_MGM_URL=root://eoscms.cern.ch
### Cross check that we can see the CMSSW area and use it
### (Of course, this should be parameterised instead of using Thiago's area)
ls /afs/cern.ch/user/t/tomei/
cd /afs/cern.ch/user/t/tomei/tmp/CMSSW_14_0_18_patch1/src
cmsenv
which cmsRun
### Come back and run
cd "$STARTINGDIR"
date
cp /afs/cern.ch/user/t/tomei/tmp/express"$1".py .
cmsRun express"$1".py
ls
if [ -f "output.root" ]; then
   echo "File output.root exists."
   eos cp output.root "$EOS_MGM_URL"//eos/cms/store/group/tsg-phase2/user/tomei/express/run386925/step2_40k_"$1".root
else
   echo "File output.root does not exist."
fi
date
