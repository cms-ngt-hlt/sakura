# Recipe on obtaining plot

![time variations of physics performance on varying conditions demonstrated on Z peak fit](screenshot_stability_comparison_sigma_over_mu.png)

Included in [CMS-DP-2025/082](https://twiki.cern.ch/twiki/bin/view/CMSPublic/DP2025082).
## Re-HLT with different conditions
As a first step, we reran HLT with various conditions. Re-HLT was ran on: 
1. HLT Global Tag
2. Prompt Global Tag
3. HLT Global Tag with Prompt ECAL Laser Corrections
4. HLT Global Tag with Prompt ECAL Pedestals
5. HLT Global Tag with Prompt ECAL Laser Corrections and Prompt ECAL Pedestals

Please note that in the final plot we only included 1., 2., and 5. but the recipe here still includes all of them.

For this, as a first step we need to get the config files (already existing in this directory and named as dump*py here):
```bash
voms-proxy-init --voms cms --valid 168:00
scram project -n LCtimeseries CMSSW_15_0_6
cd LCtimeseries/src/sakura/etc/etc/etc
./getConfig.sh && \
./getConfigPrompt.sh && \
./getLCPedconfig.sh && \
./getLCconfig.sh && \
./getPedconfig.sh
```
the dumps are needed for the HTCondor submission. The mass HTCondor submission is done through:
```bash
./batchsub_HLT.sh && \
./batchsub_Prompt.sh && \
./batchsub_HLT-LC.sh && \
./batchsub_HLT-Ped.sh && \
./batchsub_HLT-LCPed.sh
```
One can use `condor_q` to check the status of things. Now it is very frequent that jobs fail. To resubmit which jobs failed and to resubmit these, simply check with:
```bash
./passtojobs.sh
./resubandcheck.sh
```
Repeat as often as needed.

## DQM on Re-HLT
To successfully run the DQM on the the obtained .root files with the varying conditions used, minor changes need to be made to pre-existing DQM packages of CMSSW. The basic set up as follows:
```bash
cmsrel CMSSW_15_0_8 && cd CMSSW_15_0_8/src && cmsenv
cmsenv
git cms-addpkg DQM/HLTEvF DQM/Integration
scram b -j
```
and these are the changes that need to be made:
1. in file `DQM/HLTEvF/python/HLTObjectMonitor_cfi.py`: change `NbinsX = cms.int32(50)`, to `NbinsX = cms.int32(100),` . This is so hat we have finer binning.
2. in file `DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py`, add
```
process.hltObjectsMonitor4all.processName  = cms.string("HLTX")
process.hltObjectMonitor.processName = cms.string("HLTX")
```
at the end of the file. 
Once this is guranteed, you can start running the DQM client:
```bash
./run_DQM_HLT.sh && \
./run_DQM_Prompt.sh && \
./run_DQM_LC.sh && \
./run_DQM_Ped.sh && \
./run_DQM_LCPed.sh
```
This will result in DQM output root files.

## Final plot

By hand, restructure the output DQM files to follow this structure:
```
.
├── dCal_dt-ECAL-plotter.py      <-- The main execution script
├── lumi.csv                     <-- Required for plot
├── scripts.py                   <-- Python script that fits the data
│
├── upload_HLTTag/               <-- Data directory for "HLT conditions"
│   ├── *.root
│
├── upload_Prompt/               <-- Data directory for "Prompt conditions"
│   ├── *.root
│
└── upload_HLT-LCPed/            <-- Data directory for "HLT+Prompt LC and Prompt Ped"
    ├── *.root
```

If you have all the packages required installed, the final plots will apprear with running:
```bash
python3 dCal_dt-ECAL-plotter.py
```
and you have it ! 🎉
