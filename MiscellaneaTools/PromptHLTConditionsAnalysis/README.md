# PromptHLTConditionsAnalysis 
Analysis of using prompt conditions directly at HLT.

## CMSSW setup
```bash
cmsrel CMSSW_14_2_0_pre4
cd CMSSW_14_2_0_pre4/src
cmsenv
git cms-init
scram b -j 20
```

## Provisional recipe
```bash
cd $CMSSW_BASE/src
git cms-addpkg DQM/Integration
git cms-addpkg Configuration/StandardSequences
scram b -j 20

cd $CMSSW_BASE/src
git clone git@github.com:cms-ngt-hlt/sakura.git
cd sakura/MiscellaneaTools/PromptHLTConditionsAnalysis
cmsenv
./testOfflineGT.sh

cd $CMSSW_BASE/src
mkdir -p upload
cmsRun DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py inputFiles=sakura/MiscellaneaTools/PromptHLTConditionsAnalysis/output_Prompt.root

# change the GT in the script to the HLT one (141X_dataRun3_HLT_v1), rinse and repeat
# once both files are available run the plotting script
```

## Recipe to run on full statistic of `/EphemeralHLTPhysics0/Run2024H-v1/RAW`
```bash
# optional, to re-generate the configuration
./prepareConfiguration.sh
python3 submitAllTemplatedJobs.py -j ReHLT_HLTGT -i configHLT.ini --submit
python3 submitAllTemplatedJobs.py -j ReHLT_PromptGT -i configPrompt.ini --submit
```

## Recipe to run the DQM hlt client
```bash
cd $CMSSW_BASE/src
cp -pr sakura/MiscellaneaTools/PromptHLTConditionsAnalysis/dqmHarvesting/submit* .
./submitAll.sh
```
