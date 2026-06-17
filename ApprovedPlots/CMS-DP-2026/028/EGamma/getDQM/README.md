# DQM out of the HLT output root files

Given the frequent additions to the DQM clients, it is of high benefit to always take the possibly latest CMSSW IB, which you can find [here](https://cmssdt.cern.ch/SDT/html/cmssdt-ib/).

When CMSSW of choice is checked out, the following packages are also needed:
```
git cms-addpkg HLTriggerOffline/Scouting DQM/HLTEvF DQM/Integration DQMOffline/HLTScouting DQMOffline/Configuration
```
all the changes need to be added onto the pre-existing code:

```
jprendi@lxplus953 src (from-CMSSW_16_1_X_2026-04-26-0000)$ git diff
diff --git a/DQM/HLTEvF/python/FourVectorHLT_cfi.py b/DQM/HLTEvF/python/FourVectorHLT_cfi.py
index d84928327a5..72f5164ec9e 100644
--- a/DQM/HLTEvF/python/FourVectorHLT_cfi.py
+++ b/DQM/HLTEvF/python/FourVectorHLT_cfi.py
@@ -9,7 +9,7 @@ hltResults = DQMEDAnalyzer("FourVectorHLT",
      ptMax = cms.untracked.double(100.0),
      ptMin = cms.untracked.double(0.0),
      filters = _filters,
-     triggerSummaryLabel = cms.InputTag("hltTriggerSummaryAOD::HLT")
+     triggerSummaryLabel = cms.InputTag("hltTriggerSummaryAOD::HLTX")
 )
 
 
diff --git a/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py b/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py
index 69eedae6c92..75d36bb5d27 100644
--- a/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py
+++ b/DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py
@@ -133,6 +133,9 @@ process.load("DQM.HLTEvF.HLTObjectMonitor_cff")
 
 process.load("DQM.HLTEvF.HLTObjectMonitor_Client_cff")
 
+process.hltObjectsMonitor4all.processName  = cms.string("HLTX")
+process.hltObjectMonitor.processName = cms.string("HLTX")
+
 #process.p = cms.EndPath(process.hlts+process.hltsClient)
 
 process.pp = cms.Path(process.dqmEnv+process.dqmSaver)#+process.dqmSaverPB)
diff --git a/DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py b/DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py
index 36986f59b0a..f3075d6959a 100644
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
+process.scoutingCollectionMonitor.muons           = cms.InputTag("hltScoutingMuonPackerNoVtx", "", "HLTX")
+process.scoutingCollectionMonitor.muonsVtx        = cms.InputTag("hltScoutingMuonPackerVtx",   "", "HLTX")
+process.scoutingCollectionMonitor.electrons       = cms.InputTag("hltScoutingEgammaPacker",    "", "HLTX")
+process.scoutingCollectionMonitor.photons         = cms.InputTag("hltScoutingEgammaPacker",    "", "HLTX")
+process.scoutingCollectionMonitor.pfcands         = cms.InputTag("hltScoutingPFPacker",        "", "HLTX")
+process.scoutingCollectionMonitor.pfjets          = cms.InputTag("hltScoutingPFPacker",        "", "HLTX")
+process.scoutingCollectionMonitor.tracks          = cms.InputTag("hltScoutingTrackPacker",     "", "HLTX")
+process.scoutingCollectionMonitor.primaryVertices = cms.InputTag("hltScoutingPrimaryVertexPacker", "primaryVtx", "HLTX")
+process.scoutingCollectionMonitor.displacedVertices = cms.InputTag("hltScoutingMuonPackerVtx", "displacedVtx", "HLTX")
+process.scoutingCollectionMonitor.displacedVerticesNoVtx = cms.InputTag("hltScoutingMuonPackerNoVtx", "displacedVtx", "HLTX")
+process.scoutingCollectionMonitor.pfMetPt         = cms.InputTag("hltScoutingPFPacker", "pfMetPt",  "HLTX")
+process.scoutingCollectionMonitor.pfMetPhi        = cms.InputTag("hltScoutingPFPacker", "pfMetPhi", "HLTX")
+process.scoutingCollectionMonitor.rho             = cms.InputTag("hltScoutingPFPacker", "rho",      "HLTX")
+
+# 2025 RecHits updates (Integrated in your script, but ensuring HLTX is set)
+from Configuration.Eras.Modifier_run3_scouting_2025_cff import run3_scouting_2025
+run3_scouting_2025.toModify(process.scoutingCollectionMonitor,
+    pfRecHitsEB        = cms.InputTag("hltScoutingRecHitPacker", "EB", "HLTX"),
+    pfRecHitsEE        = cms.InputTag("hltScoutingRecHitPacker", "EE", "HLTX"),
+    pfCleanedRecHitsEB = cms.InputTag("hltScoutingRecHitPacker", "EBCleaned", "HLTX"),
+    pfCleanedRecHitsEE = cms.InputTag("hltScoutingRecHitPacker", "EECleaned", "HLTX"),
+    pfRecHitsHBHE      = cms.InputTag("hltScoutingRecHitPacker", "HBHE", "HLTX")
+)
+
 process.load("DQM.HLTEvF.ScoutingTrackingMonitor_cff")
 process.load("DQM.HLTEvF.ScoutingMuonMonitoring_cff")
 process.load("DQM.HLTEvF.ScoutingJetMonitoring_cff")
(END)

```

