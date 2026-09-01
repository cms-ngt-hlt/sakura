# DQM from the HLT output ROOT files

## Setting up the offline DQM environment

Use a recent CMSSW integration build, available from the
[CMSSW IB page](https://cmssdt.cern.ch/SDT/html/cmssdt-ib/), and add the DQM
packages:

```bash
git cms-addpkg HLTriggerOffline/Scouting DQM/HLTEvF DQM/Integration DQMOffline/HLTScouting DQMOffline/Configuration
```

The following sections describe the additional changes needed for the regular
HLT muon DQM and the HLT Scouting muon DQM.

## Configuring the HLT Muon DQM

The HLT output uses the process name `HLTX`, so update
`DQM/HLTEvF/python/FourVectorHLT_cfi.py`:

```diff
-     triggerSummaryLabel = cms.InputTag("hltTriggerSummaryAOD::HLT")
+     triggerSummaryLabel = cms.InputTag("hltTriggerSummaryAOD::HLTX")
```

Also configure the HLT object monitors in
`DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py` after loading
`HLTObjectMonitor_Client_cff`:

```python
process.hltObjectsMonitor4all.processName = cms.string("HLTX")
process.hltObjectMonitor.processName = cms.string("HLTX")
```

Finally, add the filter used for the muon eta-phi comparison to the `filters`
`cms.VPSet` in `DQM/HLTEvF/python/listOfFilters_cff.py`. Both muon charges are
required:

```python
cms.PSet(
    name = cms.string('hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered'),
    type = cms.int32(13),
    ptMin = cms.untracked.double(0),
    ptMax = cms.untracked.double(200)
),
cms.PSet(
    name = cms.string('hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered'),
    type = cms.int32(-13),
    ptMin = cms.untracked.double(0),
    ptMax = cms.untracked.double(200)
),
```

## Configuring the HLT Scouting Muon DQM

In `DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py`, set
the Scouting collection monitor to process only Scouting data:

```python
process.scoutingCollectionMonitor.onlyScouting = True
```

The input products were written under the `HLTX` process name. Configure the
Scouting collection monitor inputs accordingly:

```python
process.scoutingCollectionMonitor.muons = cms.InputTag(
    "hltScoutingMuonPackerNoVtx", "", "HLTX"
)
process.scoutingCollectionMonitor.muonsVtx = cms.InputTag(
    "hltScoutingMuonPackerVtx", "", "HLTX"
)
process.scoutingCollectionMonitor.electrons = cms.InputTag(
    "hltScoutingEgammaPacker", "", "HLTX"
)
process.scoutingCollectionMonitor.photons = cms.InputTag(
    "hltScoutingEgammaPacker", "", "HLTX"
)
process.scoutingCollectionMonitor.pfcands = cms.InputTag(
    "hltScoutingPFPacker", "", "HLTX"
)
process.scoutingCollectionMonitor.pfjets = cms.InputTag(
    "hltScoutingPFPacker", "", "HLTX"
)
process.scoutingCollectionMonitor.tracks = cms.InputTag(
    "hltScoutingTrackPacker", "", "HLTX"
)
process.scoutingCollectionMonitor.primaryVertices = cms.InputTag(
    "hltScoutingPrimaryVertexPacker", "primaryVtx", "HLTX"
)
process.scoutingCollectionMonitor.displacedVertices = cms.InputTag(
    "hltScoutingMuonPackerVtx", "displacedVtx", "HLTX"
)
process.scoutingCollectionMonitor.displacedVerticesNoVtx = cms.InputTag(
    "hltScoutingMuonPackerNoVtx", "displacedVtx", "HLTX"
)
process.scoutingCollectionMonitor.pfMetPt = cms.InputTag(
    "hltScoutingPFPacker", "pfMetPt", "HLTX"
)
process.scoutingCollectionMonitor.pfMetPhi = cms.InputTag(
    "hltScoutingPFPacker", "pfMetPhi", "HLTX"
)
process.scoutingCollectionMonitor.rho = cms.InputTag(
    "hltScoutingPFPacker", "rho", "HLTX"
)
```

Apply the 2025 Scouting RecHit configuration with the same process name:

```python
from Configuration.Eras.Modifier_run3_scouting_2025_cff import run3_scouting_2025

run3_scouting_2025.toModify(
    process.scoutingCollectionMonitor,
    pfRecHitsEB=cms.InputTag("hltScoutingRecHitPacker", "EB", "HLTX"),
    pfRecHitsEE=cms.InputTag("hltScoutingRecHitPacker", "EE", "HLTX"),
    pfCleanedRecHitsEB=cms.InputTag(
        "hltScoutingRecHitPacker", "EBCleaned", "HLTX"
    ),
    pfCleanedRecHitsEE=cms.InputTag(
        "hltScoutingRecHitPacker", "EECleaned", "HLTX"
    ),
    pfRecHitsHBHE=cms.InputTag("hltScoutingRecHitPacker", "HBHE", "HLTX"),
)
```

## Running the HLT Scouting Muon DQM

Run the moved Scouting DQM script from the configured CMSSW environment:

```bash
./ScoutingMuonDQM.sh
```

It processes the Prompt, NGT, and HLT Scouting ROOT files below
`MoreStats/Muons` using
`DQM/Integration/python/clients/scouting_dqm_sourceclient-live_cfg.py`. The
script moves the resulting DQM files and logs into tag-specific directories
under:

```text
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/DQM_090526
```

## Running the HLT Muon DQM

The supplied script collects all `*Raw.root` files from the HLT muon output
directory and passes them to the HLT DQM source client:

```bash
./HLTMuonDQM.sh
```

The DQM files used for the final plots are stored in:

```text
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/DQMs_Feb4th
```

The plotting inputs for the NGT, HLT, and Prompt comparison should be named so
that they match `*NGT.root`, `*HLT.root`, and `*Prompt.root`, as expected by
`FinalPlots/HLTMuons/eta_phi_diffs.py`.
