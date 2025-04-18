# TestStandDataAnalysis 
Analysis and scripts for HLT test stand and NGT demonstrator.

## CMSSW setup
```bash
cmsrel CMSSW_15_0_4
cd CMSSW_15_0_4/src
cmsenv
git cms-init
scram b -j 20
```

## Provisional recipe
```bash
#cd $CMSSW_BASE/src
#git cms-addpkg EventFilter/Utilities 
#git cms-addpkg HLTrigger/Tools
#scram b -j 20

cd $CMSSW_BASE/src
git clone git@github.com:cms-ngt-hlt/SAKURA.git
cd SAKURA/MiscellaneaTools/TestStandDataAnalysis
cmsenv
```

## Test the HLT stand path
Test the HLT test stand path (`HLT_TestData`) within the corresponding streams (`LocalTestDataRaw`, `LocalTestDataScouting`) and datasets (`TestDataRaw`, `TestDataScouting`) within a simplified menu ([/users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V3](https://cmshltcfg.app.cern.ch/open?cfg=/users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V3&db=offline-run3)).
```bash
./testStand.sh
wget https://raw.githubusercontent.com/sanuvarghese/L1PhysicsSkim/refs/heads/main/L1PhysicsFilter/test/cmsCondorData.py
cp -pr /tmp/x509up_u* .
edmConfigDump hltData.py > dump.py
python3 cmsCondorData.py dump.py $PWD /eos/cms/store/group/tsg-phase2/user/musich/test_out/ -p $PWD/x509up_u* -q espresso -n 20
condor_submit condor_cluster.sub
```

## Conversion of streamer files into the DAQ FRD format
Conversion of streamer (.dat) files into the DAQ FRD (.raw) format:
```bash
cmsRun convertStreamerToFRD.py runNumber=NNNNNN inputFiles=/store/path/file.root[,/store/path/file.root,...]

# add filePrepend=file: if the files are stored locally
```

## Large streamer preparation (2024 data)
Preparation of a large streamer (.dat) file with 23 k events, corresponding to ~ 1 % of the HLT input (~ 1 kHz) in 1 LS (~ 23 s). This involves re-running the HLT with a simplified menu ([/users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V3](https://cmshltcfg.app.cern.ch/open?cfg=/users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V3&db=offline-run3)) with the HLT test stand path (`HLT_TestData`) within the corresponding streams (`LocalTestDataRaw`, `LocalTestDataScouting`) and datasets (`TestDataRaw`, `TestDataScouting`). The script runs the streamer-to-FRD conversion of the file at the end.
```bash
./createStreamers.sh

# Note the hard-coded values in the script that need to be changed accordingly
```

## Running a simple (loop) file-discovery
Simple file-discovery of streamer (.dat) files based on `ls` and a simple loop, automatically running the streamer-to-FRD conversion (in background/parallel).
```bash
./watchDirectory.sh

# Note the hard-coded values in the script that need to be changed accordingly
```
