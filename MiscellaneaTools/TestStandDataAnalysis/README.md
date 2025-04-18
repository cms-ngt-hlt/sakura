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

## Test HLT stand path
```bash
./testStand.sh
wget https://raw.githubusercontent.com/sanuvarghese/L1PhysicsSkim/refs/heads/main/L1PhysicsFilter/test/cmsCondorData.py
cp -pr /tmp/x509up_u* .
edmConfigDump hltData.py > dump.py
python3 cmsCondorData.py dump.py $PWD /eos/cms/store/group/tsg-phase2/user/musich/test_out/ -p $PWD/x509up_u* -q espresso -n 20
condor_submit condor_cluster.sub
```

## Conversion between streamer (.dat) files into FRD (.raw) DAQ format
```bash
cmsRun convertStreamerToFRD.py runNumber=NNNNNN inputFiles=/store/path/file.root[,/store/path/file.root,...]

# add filePrepend=file: if the files are stored locally
```


## Running a simple file-discovery (loop) 
```bash
./watchDirectory.sh

# Note the hard-coded values in the script that need to be changed accordingly
```
