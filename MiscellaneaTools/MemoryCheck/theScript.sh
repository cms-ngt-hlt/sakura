#!/bin/sh
clean_up () {
    ls -l
    rm -fr tree*.root
    rm -fr *.db
    rm -fr pede*
    rm -fr mille*
    ls -l
    exit
}

#LSF signals according to http://batch.web.cern.ch/batch/lsf-return-codes.html
trap clean_up HUP INT TERM SEGV USR2 XCPU XFSZ IO

cd ${CMSSW_BASE}/src
echo $CMSSW_BASE
eval `scramv1 runtime -sh`
cd -
#cmsRun expressStep2_RAW2DIGI_RECO_ALCA.py &
#cmsRun expressStep2_RAW2DIGI_L1Reco_RECO_ALCAPRODUCER.py &
cmsRun step3_ALCAOUTPUT_ALCA.py &
#./memoryCheck.sh 1 cmsRun RSS_tar.out
#./memoryCheck.sh 1 cmsRun RSS_step2.out
./memoryCheck.sh 1 cmsRun RSS_step3.out
#tail -f RSS.out
clean_up
