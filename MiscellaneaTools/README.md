# NGT-Task-3.4
Tools and scripts for NGT Task 3.4 - "HLT Optimal Calibrations"

## Provisional recipe
```
cmsrel CMSSW_14_2_0_pre4
cd CMSSW_14_2_0_pre4/src
cmsenv
git cms-addpkg DQM/Integration
git cms-addpkg Configuration/StandardSequences
scram b -j 20
git clone git@github.com:mmusich/NGT-Task-3.4.git
cd NGT-Task-3.4
./testOfflineGT.sh
cd ..
mkdir -p upload
cmsRun DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py inputFiles=NGT-Task-3.4/output.root

# change the GT in the script to the HLT one (141X_dataRun3_HLT_v1), rinse and repeat
# once both files are available run the plotting script
```

## Recipe to run on full statistic of `/EphemeralHLTPhysics0/Run2024H-v1/RAW`
```
# optional, to re-generate the configuration
./prepareConfiguration.sh
python3 submitAllTemplatedJobs.py -j ReHLT_HLTGT -i configHLT.ini --submit
python3 submitAllTemplatedJobs.py -j ReHLT_PromptGT -i configPrompt.ini --submit
```

## Recipe to run the DQM hlt client
```
cd $CMSSW_BASE/src
cp -pr NGT-Task-3.4/dmqHarvesting/submit* .
./submitAll.sh
```
