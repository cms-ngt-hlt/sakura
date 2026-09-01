# DQM from the HLT output ROOT files

## Setting up the offline DQM environment

Given the frequent additions to the DQM clients, use a recent CMSSW
integration build from the [CMSSW IB page](https://cmssdt.cern.ch/SDT/html/cmssdt-ib/).

After checking out the chosen CMSSW release, add the required packages:

```bash
git cms-addpkg HLTriggerOffline/Scouting DQM/HLTEvF DQM/Integration DQMOffline/HLTScouting DQMOffline/Configuration
```

The following changes must be applied to the existing CMSSW code.

## Configuring the HLT EGamma DQM

The HLT output uses the process name `HLTX`. Update
`DQM/HLTEvF/python/FourVectorHLT_cfi.py` accordingly:

```diff
diff --git a/DQM/HLTEvF/python/FourVectorHLT_cfi.py b/DQM/HLTEvF/python/FourVectorHLT_cfi.py
--- a/DQM/HLTEvF/python/FourVectorHLT_cfi.py
+++ b/DQM/HLTEvF/python/FourVectorHLT_cfi.py
@@ -9,7 +9,7 @@ hltResults = DQMEDAnalyzer("FourVectorHLT",
      ptMax = cms.untracked.double(100.0),
      ptMin = cms.untracked.double(0.0),
      filters = _filters,
-     triggerSummaryLabel = cms.InputTag("hltTriggerSummaryAOD::HLT")
+     triggerSummaryLabel = cms.InputTag("hltTriggerSummaryAOD::HLTX")
 )
```

Set the process name for both HLT object monitors in
`DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py`:

```diff
diff --git a/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py b/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py
--- a/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py
+++ b/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py
@@ -133,6 +133,9 @@ process.load("DQM.HLTEvF.HLTObjectMonitor_cff")
 
 process.load("DQM.HLTEvF.HLTObjectMonitor_Client_cff")
 
+process.hltObjectsMonitor4all.processName = cms.string("HLTX")
+process.hltObjectMonitor.processName = cms.string("HLTX")
+
 #process.p = cms.EndPath(process.hlts+process.hltsClient)
 
 process.pp = cms.Path(process.dqmEnv+process.dqmSaver)#+process.dqmSaverPB)
```

## Configuring the HLT Scouting EGamma DQM

In `DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py`,
process only Scouting data and configure the collection inputs for the `HLTX`
process. The 2025 Scouting RecHit inputs must use the same process name:

```diff
diff --git a/DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py b/DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py
--- a/DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py
+++ b/DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py
@@ -47,12 +47,38 @@ process.hltOnlineBeamSpot = _onlineBeamSpotProducer.clone()
 ### for pp collisions
 process.load("DQM.HLTEvF.ScoutingCollectionMonitor_cfi")
 process.scoutingCollectionMonitor.topfoldername = "HLT/ScoutingOnline/Miscellaneous"
-process.scoutingCollectionMonitor.onlyScouting = False # this can flipped due to https://its.cern.ch/jira/browse/CMSHLT-3585
+process.scoutingCollectionMonitor.onlyScouting = True # this can flipped due to https://its.cern.ch/jira/browse/CMSHLT-3585
 process.scoutingCollectionMonitor.onlineMetaDataDigis = "hltOnlineMetaDataDigis"
 process.scoutingCollectionMonitor.rho = ["hltScoutingPFPacker", "rho"]
 process.dqmcommon = cms.Sequence(process.dqmEnv
                                * process.dqmSaver)#*process.dqmSaverPB)
 
+#process.scoutingCollectionMonitor.processName = cms.string("HLTX")
+
+process.scoutingCollectionMonitor.muons = cms.InputTag("hltScoutingMuonPackerNoVtx", "", "HLTX")
+process.scoutingCollectionMonitor.muonsVtx = cms.InputTag("hltScoutingMuonPackerVtx", "", "HLTX")
+process.scoutingCollectionMonitor.electrons = cms.InputTag("hltScoutingEgammaPacker", "", "HLTX")
+process.scoutingCollectionMonitor.photons = cms.InputTag("hltScoutingEgammaPacker", "", "HLTX")
+process.scoutingCollectionMonitor.pfcands = cms.InputTag("hltScoutingPFPacker", "", "HLTX")
+process.scoutingCollectionMonitor.pfjets = cms.InputTag("hltScoutingPFPacker", "", "HLTX")
+process.scoutingCollectionMonitor.tracks = cms.InputTag("hltScoutingTrackPacker", "", "HLTX")
+process.scoutingCollectionMonitor.primaryVertices = cms.InputTag("hltScoutingPrimaryVertexPacker", "primaryVtx", "HLTX")
+process.scoutingCollectionMonitor.displacedVertices = cms.InputTag("hltScoutingMuonPackerVtx", "displacedVtx", "HLTX")
+process.scoutingCollectionMonitor.displacedVerticesNoVtx = cms.InputTag("hltScoutingMuonPackerNoVtx", "displacedVtx", "HLTX")
+process.scoutingCollectionMonitor.pfMetPt = cms.InputTag("hltScoutingPFPacker", "pfMetPt", "HLTX")
+process.scoutingCollectionMonitor.pfMetPhi = cms.InputTag("hltScoutingPFPacker", "pfMetPhi", "HLTX")
+process.scoutingCollectionMonitor.rho = cms.InputTag("hltScoutingPFPacker", "rho", "HLTX")
+
+# 2025 RecHit inputs
+from Configuration.Eras.Modifier_run3_scouting_2025_cff import run3_scouting_2025
+run3_scouting_2025.toModify(process.scoutingCollectionMonitor,
+    pfRecHitsEB = cms.InputTag("hltScoutingRecHitPacker", "EB", "HLTX"),
+    pfRecHitsEE = cms.InputTag("hltScoutingRecHitPacker", "EE", "HLTX"),
+    pfCleanedRecHitsEB = cms.InputTag("hltScoutingRecHitPacker", "EBCleaned", "HLTX"),
+    pfCleanedRecHitsEE = cms.InputTag("hltScoutingRecHitPacker", "EECleaned", "HLTX"),
+    pfRecHitsHBHE = cms.InputTag("hltScoutingRecHitPacker", "HBHE", "HLTX")
+)
+
 process.load("DQM.HLTEvF.ScoutingTrackingMonitor_cff")
 process.load("DQM.HLTEvF.ScoutingMuonMonitoring_cff")
 process.load("DQM.HLTEvF.ScoutingJetMonitoring_cff")
```

## Running the HLT Scouting EGamma DQM

Run the prepared script from the configured CMSSW environment:

```bash
./ScoutingAutoDQM.sh
```

The script processes the Prompt, NGT, and HLT Scouting ROOT files run by run.
The resulting DQM files and logs are stored in tag-specific directories under:

```text
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/DQM_260426
```

## Running the HLT EGamma DQM

Run the prepared regular HLT DQM script:

```bash
./AaDQM.sh
```

The script processes the Prompt, HLT, and NGT `*Raw.root` files run by run.
The resulting DQM files and logs are stored in tag-specific directories under:

```text
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/DQM_Raws
```
