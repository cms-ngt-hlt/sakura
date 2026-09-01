# L1T INFO:  L1REPACK:uGT will unpack uGMT and CaloLayer2 outputs, and re-emulate uGT
import FWCore.ParameterSet.Config as cms
from HeterogeneousCore.AlpakaCore.ProcessAcceleratorAlpaka import ProcessAcceleratorAlpaka
from HeterogeneousCore.CUDACore.ProcessAcceleratorCUDA import ProcessAcceleratorCUDA
from HeterogeneousCore.ROCmCore.ProcessAcceleratorROCm import ProcessAcceleratorROCm

process = cms.Process("HLTX")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(' '),
    inputCommands = cms.untracked.vstring('keep *')
)
process.HLTCkfBaseTrajectoryFilterP5 = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(3),
    maxLostHits = cms.int32(4),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.5),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTCkfBaseTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTConfigVersion = cms.PSet(
    tableName = cms.string('/dev/CMSSW_15_0_0/GRun/V119')
)

process.HLTGroupedCkfTrajectoryBuilderP5 = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESChi2MeasurementEstimatorForP5'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(1),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTCkfBaseTrajectoryFilterP5')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTIter0GroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator9'),
    foundHitBonus = cms.double(5.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0PSetTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0PSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTIter0HighPtTkMuPSetTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('CkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(4),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0HighPtTkMuPSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator')
)

process.HLTIter0HighPtTkMuPSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.3),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter0IterL3FromL1MuonGroupedCkfTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(10.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter0IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonGroupedCkfTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(1.0),
    maxCand = cms.int32(5),
    minNrOfHitsForRebuild = cms.int32(2),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonGroupedCkfTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(10.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter0IterL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(1000.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(1.0),
    maxCand = cms.int32(5),
    minNrOfHitsForRebuild = cms.int32(2),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTIter0PSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.3),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter1GroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator16'),
    foundHitBonus = cms.double(5.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter1PSetTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter1PSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTIter1PSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.2),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter2GroupedCkfTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator16'),
    foundHitBonus = cms.double(5.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter2PSetTrajectoryFilterIT')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter2PSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTIter2PSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.3),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(1),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTIter4PSetTrajectoryBuilderIT = cms.PSet(
    ComponentType = cms.string('CkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator16'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(1),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTIter4PSetTrajectoryFilterIT')
    ),
    updator = cms.string('hltESPKFUpdator')
)

process.HLTIter4PSetTrajectoryFilterIT = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(0),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.3),
    minimumNumberOfHits = cms.int32(6),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetCkfBaseTrajectoryFilter_block = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetHighPtTripletStepTrajectoryBuilderForDmesonPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPHighPtTripletStepChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(3),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetHighPtTripletStepTrajectoryFilterForDmesonPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetHighPtTripletStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPHighPtTripletStepChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(3),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetHighPtTripletStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetHighPtTripletStepTrajectoryFilterForDmesonPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(3.5),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetHighPtTripletStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(1.0),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetInitialStepTrajectoryBuilderForDmesonPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPInitialStepChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(3),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(1),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetInitialStepTrajectoryFilterForDmesonPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetInitialStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPInitialStepChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(True),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(3),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(1),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetInitialStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetInitialStepTrajectoryBuilderPreSplittingForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPInitialStepChi2ChargeMeasurementEstimator30'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(3),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetInitialStepTrajectoryFilterPreSplittingForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetInitialStepTrajectoryFilterBasePreSplittingForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(1.0),
    minimumNumberOfHits = cms.int32(4),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetInitialStepTrajectoryFilterForDmesonPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(3.0),
    minimumNumberOfHits = cms.int32(4),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetInitialStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(1.0),
    minimumNumberOfHits = cms.int32(4),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetInitialStepTrajectoryFilterPreSplittingForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CompositeTrajectoryFilter'),
    filters = cms.VPSet(
        cms.PSet(
            refToPSet_ = cms.string('HLTPSetInitialStepTrajectoryFilterBasePreSplittingForFullTrackingPPOnAA')
        ),
        cms.PSet(
            refToPSet_ = cms.string('HLTPSetInitialStepTrajectoryFilterShapePreSplittingPPOnAA')
        )
    )
)

process.HLTPSetInitialStepTrajectoryFilterShapePreSplittingPPOnAA = cms.PSet(
    ComponentType = cms.string('StripSubClusterShapeTrajectoryFilter'),
    layerMask = cms.PSet(
        TEC = cms.bool(False),
        TIB = cms.vuint32(1, 2),
        TID = cms.vuint32(1, 2),
        TOB = cms.bool(False)
    ),
    maxNSat = cms.uint32(3),
    maxTrimmedSizeDiffNeg = cms.double(1.0),
    maxTrimmedSizeDiffPos = cms.double(0.7),
    seedCutMIPs = cms.double(0.35),
    seedCutSN = cms.double(7.0),
    subclusterCutMIPs = cms.double(0.45),
    subclusterCutSN = cms.double(12.0),
    subclusterWindow = cms.double(0.7),
    trimMaxADC = cms.double(30.0),
    trimMaxFracNeigh = cms.double(0.25),
    trimMaxFracTotal = cms.double(0.15)
)

process.HLTPSetJetCoreStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(50),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetJetCoreStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetJetCoreStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(5.0),
    minimumNumberOfHits = cms.int32(4),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetLowPtQuadStepTrajectoryBuilderForDmesonPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPLowPtQuadStepChi2ChargeMeasurementEstimator9'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(4),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetLowPtQuadStepTrajectoryFilterForDmesonPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetLowPtQuadStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPLowPtQuadStepChi2ChargeMeasurementEstimator9'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(4),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetLowPtQuadStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetLowPtQuadStepTrajectoryFilterForDmesonPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(2.8),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetLowPtQuadStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(1.0),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetLowPtTripletStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPLowPtTripletStepChi2ChargeMeasurementEstimator9'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(4),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetLowPtTripletStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetLowPtTripletStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(0),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(2.8),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetMixedTripletStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPMixedTripletStepChi2ChargeMeasurementEstimator16'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterialForMixedStep'),
    propagatorOpposite = cms.string('PropagatorWithMaterialForMixedStepOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetMixedTripletStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetMixedTripletStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.4),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(999),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(5.0),
    minimumNumberOfHits = cms.int32(3),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetMuTrackJpsiTrajectoryBuilder = cms.PSet(
    ComponentType = cms.string('CkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    intermediateCleaning = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(1),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetMuTrackJpsiTrajectoryFilter')
    ),
    updator = cms.string('hltESPKFUpdator')
)

process.HLTPSetMuTrackJpsiTrajectoryFilter = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(8),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(10.0),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetMuonCkfTrajectoryBuilder = cms.PSet(
    ComponentType = cms.string('MuonCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    deltaEta = cms.double(-1.0),
    deltaPhi = cms.double(-1.0),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    intermediateCleaning = cms.bool(False),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(5),
    propagatorAlong = cms.string('PropagatorWithMaterial'),
    propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
    propagatorProximity = cms.string('SteppingHelixPropagatorAny'),
    rescaleErrorIfFail = cms.double(1.0),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetMuonCkfTrajectoryFilter')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSeedLayer = cms.bool(False)
)

process.HLTPSetMuonCkfTrajectoryFilter = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(-1),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(0.9),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetMuonTrackingRegionBuilder8356 = cms.PSet(
    DeltaEta = cms.double(0.2),
    DeltaPhi = cms.double(0.2),
    DeltaR = cms.double(0.2),
    DeltaZ = cms.double(15.9),
    EtaR_UpperLimit_Par1 = cms.double(0.25),
    EtaR_UpperLimit_Par2 = cms.double(0.15),
    Eta_fixed = cms.bool(False),
    Eta_min = cms.double(0.1),
    MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
    OnDemand = cms.int32(-1),
    PhiR_UpperLimit_Par1 = cms.double(0.6),
    PhiR_UpperLimit_Par2 = cms.double(0.2),
    Phi_fixed = cms.bool(False),
    Phi_min = cms.double(0.1),
    Pt_fixed = cms.bool(False),
    Pt_min = cms.double(1.5),
    Rescale_Dz = cms.double(3.0),
    Rescale_eta = cms.double(3.0),
    Rescale_phi = cms.double(3.0),
    UseVertex = cms.bool(False),
    Z_fixed = cms.bool(True),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    input = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
    maxRegions = cms.int32(2),
    precise = cms.bool(True),
    vertexCollection = cms.InputTag("pixelVertices")
)

process.HLTPSetPixelLessStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPPixelLessStepChi2ChargeMeasurementEstimator16'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetCkfBaseTrajectoryFilter_block')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(4),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetPixelLessStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(True)
)

process.HLTPSetPixelLessStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(0),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(5.0),
    minimumNumberOfHits = cms.int32(4),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(1),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetPvClusterComparerForBTag = cms.PSet(
    track_chi2_max = cms.double(20.0),
    track_prob_min = cms.double(-1.0),
    track_pt_max = cms.double(20.0),
    track_pt_min = cms.double(0.1)
)

process.HLTPSetPvClusterComparerForIT = cms.PSet(
    track_chi2_max = cms.double(20.0),
    track_prob_min = cms.double(-1.0),
    track_pt_max = cms.double(20.0),
    track_pt_min = cms.double(1.0)
)

process.HLTPSetTobTecStepInOutTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(0),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(5.0),
    minimumNumberOfHits = cms.int32(4),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(1),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetTobTecStepTrajectoryBuilderForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(False),
    bestHitOnly = cms.bool(True),
    estimator = cms.string('hltESPTobTecStepChi2ChargeMeasurementEstimator16'),
    foundHitBonus = cms.double(10.0),
    inOutTrajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetTobTecStepInOutTrajectoryFilterForFullTrackingPPOnAA')
    ),
    intermediateCleaning = cms.bool(True),
    keepOriginalIfRebuildFails = cms.bool(False),
    lockHits = cms.bool(True),
    lostHitPenalty = cms.double(30.0),
    maxCand = cms.int32(2),
    maxDPhiForLooperReconstruction = cms.double(2.0),
    maxPtForLooperReconstruction = cms.double(0.0),
    minNrOfHitsForRebuild = cms.int32(4),
    propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
    propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    requireSeedHitsInRebuild = cms.bool(True),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetTobTecStepTrajectoryFilterForFullTrackingPPOnAA')
    ),
    updator = cms.string('hltESPKFUpdator'),
    useSameTrajFilter = cms.bool(False)
)

process.HLTPSetTobTecStepTrajectoryFilterForFullTrackingPPOnAA = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(2.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(0),
    maxLostHitsFraction = cms.double(0.1),
    maxNumberOfHits = cms.int32(100),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(3),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(5.0),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(1),
    strictSeedExtension = cms.bool(False)
)

process.HLTPSetTrajectoryBuilderForGsfElectrons = cms.PSet(
    ComponentType = cms.string('CkfTrajectoryBuilder'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    alwaysUseInvalidHits = cms.bool(True),
    estimator = cms.string('hltESPChi2ChargeMeasurementEstimator2000'),
    intermediateCleaning = cms.bool(False),
    lostHitPenalty = cms.double(90.0),
    maxCand = cms.int32(5),
    propagatorAlong = cms.string('hltESPFwdElectronPropagator'),
    propagatorOpposite = cms.string('hltESPBwdElectronPropagator'),
    seedAs5DHit = cms.bool(False),
    trajectoryFilter = cms.PSet(
        refToPSet_ = cms.string('HLTPSetTrajectoryFilterForElectrons')
    ),
    updator = cms.string('hltESPKFUpdator')
)

process.HLTPSetTrajectoryFilterForElectrons = cms.PSet(
    ComponentType = cms.string('CkfBaseTrajectoryFilter'),
    chargeSignificance = cms.double(-1.0),
    constantValueForLostHitsFractionFilter = cms.double(1.0),
    extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
    highEtaSwitch = cms.double(5.0),
    maxCCCLostHits = cms.int32(9999),
    maxConsecLostHits = cms.int32(1),
    maxLostHits = cms.int32(1),
    maxLostHitsFraction = cms.double(999.0),
    maxNumberOfHits = cms.int32(-1),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    minHitsAtHighEta = cms.int32(5),
    minHitsMinPt = cms.int32(-1),
    minNumberOfHitsForLoopers = cms.int32(13),
    minNumberOfHitsPerLoop = cms.int32(4),
    minPt = cms.double(2.0),
    minimumNumberOfHits = cms.int32(5),
    nSigmaMinPt = cms.double(5.0),
    pixelSeedExtension = cms.bool(False),
    seedExtension = cms.int32(0),
    seedPairPenalty = cms.int32(0),
    strictSeedExtension = cms.bool(False)
)

process.HLTSeedFromConsecutiveHitsCreator = cms.PSet(
    ComponentName = cms.string('SeedFromConsecutiveHitsCreator'),
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string(''),
    propagator = cms.string('PropagatorWithMaterial')
)

process.HLTSeedFromProtoTracks = cms.PSet(
    ComponentName = cms.string('SeedFromConsecutiveHitsCreator'),
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf')
)

process.HLTSiStripClusterChargeCutForHI = cms.PSet(
    value = cms.double(2069.0)
)

process.HLTSiStripClusterChargeCutLoose = cms.PSet(
    value = cms.double(1620.0)
)

process.HLTSiStripClusterChargeCutNone = cms.PSet(
    value = cms.double(-1.0)
)

process.HLTSiStripClusterChargeCutTight = cms.PSet(
    value = cms.double(1945.0)
)

process.datasets = cms.PSet(
    AlCaHcalIsoTrk = cms.vstring('AlCa_IsoTrackHBHE_v3'),
    AlCaLowPtJet = cms.vstring(
        'AlCa_AK8PFJet40_v31',
        'AlCa_PFJet40_v36'
    ),
    AlCaLumiPixelsCountsExpress = cms.vstring('AlCa_LumiPixelsCounts_Random_v12'),
    AlCaLumiPixelsCountsPrompt = cms.vstring(
        'AlCa_LumiPixelsCounts_Random_v12',
        'AlCa_LumiPixelsCounts_ZeroBias_v15'
    ),
    AlCaP0 = cms.vstring(
        'AlCa_EcalEtaEBonly_v27',
        'AlCa_EcalEtaEEonly_v27',
        'AlCa_EcalPi0EBonly_v27',
        'AlCa_EcalPi0EEonly_v27'
    ),
    AlCaPPSExpress = cms.vstring(
        'HLT_PPSMaxTracksPerArm1_v10',
        'HLT_PPSMaxTracksPerRP4_v10'
    ),
    AlCaPPSPrompt = cms.vstring(
        'HLT_PPSMaxTracksPerArm1_v10',
        'HLT_PPSMaxTracksPerRP4_v10'
    ),
    AlCaPhiSym = cms.vstring('AlCa_EcalPhiSym_v22'),
    BTagMu = cms.vstring(
        'HLT_BTagMu_AK4DiJet110_Mu5_v29',
        'HLT_BTagMu_AK4DiJet170_Mu5_v28',
        'HLT_BTagMu_AK4DiJet20_Mu5_v29',
        'HLT_BTagMu_AK4DiJet40_Mu5_v29',
        'HLT_BTagMu_AK4DiJet70_Mu5_v29',
        'HLT_BTagMu_AK4Jet300_Mu5_v28',
        'HLT_BTagMu_AK8DiJet170_Mu5_v25',
        'HLT_BTagMu_AK8Jet170_DoubleMu5_v18',
        'HLT_BTagMu_AK8Jet300_Mu5_v28'
    ),
    Commissioning = cms.vstring(
        'HLT_L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142_v10',
        'HLT_PFJet40_GPUvsCPU_v8'
    ),
    Cosmics = cms.vstring('HLT_L1SingleMuCosmics_v9'),
    DQMGPUvsCPU = cms.vstring(
        'DQM_EcalReconstruction_v13',
        'DQM_HcalReconstruction_v11',
        'DQM_PixelReconstruction_v14'
    ),
    DQMOnlineBeamspot = cms.vstring(
        'HLT_HT300_Beamspot_v27',
        'HLT_ZeroBias_Beamspot_v20'
    ),
    DQMOnlineScouting = cms.vstring(
        'DST_PFScouting_DoubleEGMonitorJPsi_v1',
        'DST_PFScouting_DoubleEGMonitorZ_v1',
        'DST_PFScouting_DoubleMuonVtxMonitorJPsi_v4',
        'DST_PFScouting_DoubleMuonVtxMonitorZ_v4',
        'DST_PFScouting_SinglePhotonEBMonitorJPsi_v1',
        'DST_PFScouting_SinglePhotonEBMonitorZ_v1',
        'HLT_TriggersForScoutingPFMonitor_PS1000_v1',
        'HLT_TriggersForScoutingPFMonitor_PS125_v1',
        'HLT_TriggersForScoutingPFMonitor_PS250_v1',
        'HLT_TriggersForScoutingPFMonitor_PS500_v1'
    ),
    DQMPPSRandom = cms.vstring('HLT_PPSRandom_v1'),
    EGamma0 = cms.vstring(
        'HLT_DiEle27_WPTightCaloOnly_L1DoubleEG_v16',
        'HLT_DiPhoton10Time1ns_v11',
        'HLT_DiPhoton10Time1p2ns_v11',
        'HLT_DiPhoton10Time1p4ns_v11',
        'HLT_DiPhoton10Time1p6ns_v11',
        'HLT_DiPhoton10Time1p8ns_v11',
        'HLT_DiPhoton10Time2ns_v11',
        'HLT_DiPhoton10_CaloIdL_v11',
        'HLT_DiSC30_18_EIso_AND_HE_Mass70_v25',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2_v4',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v4',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_16_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_Mass55_v14',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_v14',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v26',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v26',
        'HLT_DiphotonMVA14p25_High_Mass60_v1',
        'HLT_DiphotonMVA14p25_Low_Mass60_v1',
        'HLT_DiphotonMVA14p25_Medium_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightHigh_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightLow_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightMedium_Mass60_v1',
        'HLT_DoubleEle10_eta1p22_mMax6_v13',
        'HLT_DoubleEle25_CaloIdL_MW_v18',
        'HLT_DoubleEle27_CaloIdL_MW_v18',
        'HLT_DoubleEle33_CaloIdL_MW_v31',
        'HLT_DoubleEle6p5_eta1p22_mMax6_v13',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v36',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v36',
        'HLT_DoubleEle8_eta1p22_mMax6_v13',
        'HLT_DoublePhoton33_CaloIdL_v18',
        'HLT_DoublePhoton70_v18',
        'HLT_DoublePhoton85_v26',
        'HLT_ECALHT800_v22',
        'HLT_Ele115_CaloIdVT_GsfTrkIdT_v28',
        'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele135_CaloIdVT_GsfTrkIdT_v21',
        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53_v9',
        'HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v32',
        'HLT_Ele15_IsoVVVL_PFHT450_v32',
        'HLT_Ele15_IsoVVVL_PFHT600_v36',
        'HLT_Ele17_CaloIdM_TrackIdM_PFJet30_v32',
        'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele23_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v33',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Loose_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Medium_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Tight_eta2p3_CrossL1_v11',
        'HLT_Ele28_HighEta_SC20_Mass55_v27',
        'HLT_Ele30_WPTight_Gsf_v16',
        'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v24',
        'HLT_Ele32_WPTight_Gsf_v30',
        'HLT_Ele35_WPTight_Gsf_v24',
        'HLT_Ele38_WPTight_Gsf_v24',
        'HLT_Ele40_WPTight_Gsf_v24',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v34',
        'HLT_Ele50_IsoVVVL_PFHT450_v32',
        'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30_v32',
        'HLT_Ele8_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Photon100EBHE10_v13',
        'HLT_Photon110EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon110EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon110EB_TightID_TightIso_v15',
        'HLT_Photon120_R9Id90_HE10_IsoM_v27',
        'HLT_Photon120_v24',
        'HLT_Photon150_v18',
        'HLT_Photon165_R9Id90_HE10_IsoM_v28',
        'HLT_Photon175_v26',
        'HLT_Photon200_v25',
        'HLT_Photon20_HoverELoose_v21',
        'HLT_Photon300_NoHE_v24',
        'HLT_Photon30EB_TightID_TightIso_v15',
        'HLT_Photon30_HoverELoose_v21',
        'HLT_Photon32_OneProng32_M50To105_v14',
        'HLT_Photon33_v16',
        'HLT_Photon34_R9Id90_CaloIdL_IsoL_DisplacedIdL_MediumChargedIsoDisplacedPFTauHPS34_v12',
        'HLT_Photon35_TwoProngs35_v17',
        'HLT_Photon40EB_TightID_TightIso_v6',
        'HLT_Photon40EB_v4',
        'HLT_Photon45EB_TightID_TightIso_v6',
        'HLT_Photon45EB_v4',
        'HLT_Photon50EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon50EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon50EB_TightID_TightIso_v11',
        'HLT_Photon50EB_v5',
        'HLT_Photon50_R9Id90_HE10_IsoM_v27',
        'HLT_Photon50_TimeGt2p5ns_v8',
        'HLT_Photon50_TimeLtNeg2p5ns_v8',
        'HLT_Photon50_v24',
        'HLT_Photon55EB_TightID_TightIso_v7',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT380_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT400_v14',
        'HLT_Photon60_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v13',
        'HLT_Photon75EB_TightID_TightIso_v11',
        'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v21',
        'HLT_Photon75_R9Id90_HE10_IsoM_v27',
        'HLT_Photon75_v24',
        'HLT_Photon90EB_TightID_TightIso_v11',
        'HLT_Photon90_R9Id90_HE10_IsoM_v27',
        'HLT_Photon90_v24',
        'HLT_SingleEle8_SingleEGL1_v12',
        'HLT_SingleEle8_v12'
    ),
    EGamma1 = cms.vstring(
        'HLT_DiEle27_WPTightCaloOnly_L1DoubleEG_v16',
        'HLT_DiPhoton10Time1ns_v11',
        'HLT_DiPhoton10Time1p2ns_v11',
        'HLT_DiPhoton10Time1p4ns_v11',
        'HLT_DiPhoton10Time1p6ns_v11',
        'HLT_DiPhoton10Time1p8ns_v11',
        'HLT_DiPhoton10Time2ns_v11',
        'HLT_DiPhoton10_CaloIdL_v11',
        'HLT_DiSC30_18_EIso_AND_HE_Mass70_v25',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2_v4',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v4',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_16_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_Mass55_v14',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_v14',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v26',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v26',
        'HLT_DiphotonMVA14p25_High_Mass60_v1',
        'HLT_DiphotonMVA14p25_Low_Mass60_v1',
        'HLT_DiphotonMVA14p25_Medium_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightHigh_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightLow_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightMedium_Mass60_v1',
        'HLT_DoubleEle10_eta1p22_mMax6_v13',
        'HLT_DoubleEle25_CaloIdL_MW_v18',
        'HLT_DoubleEle27_CaloIdL_MW_v18',
        'HLT_DoubleEle33_CaloIdL_MW_v31',
        'HLT_DoubleEle6p5_eta1p22_mMax6_v13',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v36',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v36',
        'HLT_DoubleEle8_eta1p22_mMax6_v13',
        'HLT_DoublePhoton33_CaloIdL_v18',
        'HLT_DoublePhoton70_v18',
        'HLT_DoublePhoton85_v26',
        'HLT_ECALHT800_v22',
        'HLT_Ele115_CaloIdVT_GsfTrkIdT_v28',
        'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele135_CaloIdVT_GsfTrkIdT_v21',
        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53_v9',
        'HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v32',
        'HLT_Ele15_IsoVVVL_PFHT450_v32',
        'HLT_Ele15_IsoVVVL_PFHT600_v36',
        'HLT_Ele17_CaloIdM_TrackIdM_PFJet30_v32',
        'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele23_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v33',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Loose_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Medium_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Tight_eta2p3_CrossL1_v11',
        'HLT_Ele28_HighEta_SC20_Mass55_v27',
        'HLT_Ele30_WPTight_Gsf_v16',
        'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v24',
        'HLT_Ele32_WPTight_Gsf_v30',
        'HLT_Ele35_WPTight_Gsf_v24',
        'HLT_Ele38_WPTight_Gsf_v24',
        'HLT_Ele40_WPTight_Gsf_v24',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v34',
        'HLT_Ele50_IsoVVVL_PFHT450_v32',
        'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30_v32',
        'HLT_Ele8_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Photon100EBHE10_v13',
        'HLT_Photon110EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon110EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon110EB_TightID_TightIso_v15',
        'HLT_Photon120_R9Id90_HE10_IsoM_v27',
        'HLT_Photon120_v24',
        'HLT_Photon150_v18',
        'HLT_Photon165_R9Id90_HE10_IsoM_v28',
        'HLT_Photon175_v26',
        'HLT_Photon200_v25',
        'HLT_Photon20_HoverELoose_v21',
        'HLT_Photon300_NoHE_v24',
        'HLT_Photon30EB_TightID_TightIso_v15',
        'HLT_Photon30_HoverELoose_v21',
        'HLT_Photon32_OneProng32_M50To105_v14',
        'HLT_Photon33_v16',
        'HLT_Photon34_R9Id90_CaloIdL_IsoL_DisplacedIdL_MediumChargedIsoDisplacedPFTauHPS34_v12',
        'HLT_Photon35_TwoProngs35_v17',
        'HLT_Photon40EB_TightID_TightIso_v6',
        'HLT_Photon40EB_v4',
        'HLT_Photon45EB_TightID_TightIso_v6',
        'HLT_Photon45EB_v4',
        'HLT_Photon50EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon50EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon50EB_TightID_TightIso_v11',
        'HLT_Photon50EB_v5',
        'HLT_Photon50_R9Id90_HE10_IsoM_v27',
        'HLT_Photon50_TimeGt2p5ns_v8',
        'HLT_Photon50_TimeLtNeg2p5ns_v8',
        'HLT_Photon50_v24',
        'HLT_Photon55EB_TightID_TightIso_v7',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT380_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT400_v14',
        'HLT_Photon60_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v13',
        'HLT_Photon75EB_TightID_TightIso_v11',
        'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v21',
        'HLT_Photon75_R9Id90_HE10_IsoM_v27',
        'HLT_Photon75_v24',
        'HLT_Photon90EB_TightID_TightIso_v11',
        'HLT_Photon90_R9Id90_HE10_IsoM_v27',
        'HLT_Photon90_v24',
        'HLT_SingleEle8_SingleEGL1_v12',
        'HLT_SingleEle8_v12'
    ),
    EGamma2 = cms.vstring(
        'HLT_DiEle27_WPTightCaloOnly_L1DoubleEG_v16',
        'HLT_DiPhoton10Time1ns_v11',
        'HLT_DiPhoton10Time1p2ns_v11',
        'HLT_DiPhoton10Time1p4ns_v11',
        'HLT_DiPhoton10Time1p6ns_v11',
        'HLT_DiPhoton10Time1p8ns_v11',
        'HLT_DiPhoton10Time2ns_v11',
        'HLT_DiPhoton10_CaloIdL_v11',
        'HLT_DiSC30_18_EIso_AND_HE_Mass70_v25',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2_v4',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v4',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_16_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_Mass55_v14',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_v14',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v26',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v26',
        'HLT_DiphotonMVA14p25_High_Mass60_v1',
        'HLT_DiphotonMVA14p25_Low_Mass60_v1',
        'HLT_DiphotonMVA14p25_Medium_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightHigh_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightLow_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightMedium_Mass60_v1',
        'HLT_DoubleEle10_eta1p22_mMax6_v13',
        'HLT_DoubleEle25_CaloIdL_MW_v18',
        'HLT_DoubleEle27_CaloIdL_MW_v18',
        'HLT_DoubleEle33_CaloIdL_MW_v31',
        'HLT_DoubleEle6p5_eta1p22_mMax6_v13',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v36',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v36',
        'HLT_DoubleEle8_eta1p22_mMax6_v13',
        'HLT_DoublePhoton33_CaloIdL_v18',
        'HLT_DoublePhoton70_v18',
        'HLT_DoublePhoton85_v26',
        'HLT_ECALHT800_v22',
        'HLT_Ele115_CaloIdVT_GsfTrkIdT_v28',
        'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele135_CaloIdVT_GsfTrkIdT_v21',
        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53_v9',
        'HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v32',
        'HLT_Ele15_IsoVVVL_PFHT450_v32',
        'HLT_Ele15_IsoVVVL_PFHT600_v36',
        'HLT_Ele17_CaloIdM_TrackIdM_PFJet30_v32',
        'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele23_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v33',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Loose_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Medium_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Tight_eta2p3_CrossL1_v11',
        'HLT_Ele28_HighEta_SC20_Mass55_v27',
        'HLT_Ele30_WPTight_Gsf_v16',
        'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v24',
        'HLT_Ele32_WPTight_Gsf_v30',
        'HLT_Ele35_WPTight_Gsf_v24',
        'HLT_Ele38_WPTight_Gsf_v24',
        'HLT_Ele40_WPTight_Gsf_v24',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v34',
        'HLT_Ele50_IsoVVVL_PFHT450_v32',
        'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30_v32',
        'HLT_Ele8_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Photon100EBHE10_v13',
        'HLT_Photon110EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon110EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon110EB_TightID_TightIso_v15',
        'HLT_Photon120_R9Id90_HE10_IsoM_v27',
        'HLT_Photon120_v24',
        'HLT_Photon150_v18',
        'HLT_Photon165_R9Id90_HE10_IsoM_v28',
        'HLT_Photon175_v26',
        'HLT_Photon200_v25',
        'HLT_Photon20_HoverELoose_v21',
        'HLT_Photon300_NoHE_v24',
        'HLT_Photon30EB_TightID_TightIso_v15',
        'HLT_Photon30_HoverELoose_v21',
        'HLT_Photon32_OneProng32_M50To105_v14',
        'HLT_Photon33_v16',
        'HLT_Photon34_R9Id90_CaloIdL_IsoL_DisplacedIdL_MediumChargedIsoDisplacedPFTauHPS34_v12',
        'HLT_Photon35_TwoProngs35_v17',
        'HLT_Photon40EB_TightID_TightIso_v6',
        'HLT_Photon40EB_v4',
        'HLT_Photon45EB_TightID_TightIso_v6',
        'HLT_Photon45EB_v4',
        'HLT_Photon50EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon50EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon50EB_TightID_TightIso_v11',
        'HLT_Photon50EB_v5',
        'HLT_Photon50_R9Id90_HE10_IsoM_v27',
        'HLT_Photon50_TimeGt2p5ns_v8',
        'HLT_Photon50_TimeLtNeg2p5ns_v8',
        'HLT_Photon50_v24',
        'HLT_Photon55EB_TightID_TightIso_v7',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT380_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT400_v14',
        'HLT_Photon60_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v13',
        'HLT_Photon75EB_TightID_TightIso_v11',
        'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v21',
        'HLT_Photon75_R9Id90_HE10_IsoM_v27',
        'HLT_Photon75_v24',
        'HLT_Photon90EB_TightID_TightIso_v11',
        'HLT_Photon90_R9Id90_HE10_IsoM_v27',
        'HLT_Photon90_v24',
        'HLT_SingleEle8_SingleEGL1_v12',
        'HLT_SingleEle8_v12'
    ),
    EGamma3 = cms.vstring(
        'HLT_DiEle27_WPTightCaloOnly_L1DoubleEG_v16',
        'HLT_DiPhoton10Time1ns_v11',
        'HLT_DiPhoton10Time1p2ns_v11',
        'HLT_DiPhoton10Time1p4ns_v11',
        'HLT_DiPhoton10Time1p6ns_v11',
        'HLT_DiPhoton10Time1p8ns_v11',
        'HLT_DiPhoton10Time2ns_v11',
        'HLT_DiPhoton10_CaloIdL_v11',
        'HLT_DiSC30_18_EIso_AND_HE_Mass70_v25',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2_v4',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v4',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_16_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_Mass55_v14',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_v14',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v26',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v26',
        'HLT_DiphotonMVA14p25_High_Mass60_v1',
        'HLT_DiphotonMVA14p25_Low_Mass60_v1',
        'HLT_DiphotonMVA14p25_Medium_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightHigh_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightLow_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightMedium_Mass60_v1',
        'HLT_DoubleEle10_eta1p22_mMax6_v13',
        'HLT_DoubleEle25_CaloIdL_MW_v18',
        'HLT_DoubleEle27_CaloIdL_MW_v18',
        'HLT_DoubleEle33_CaloIdL_MW_v31',
        'HLT_DoubleEle6p5_eta1p22_mMax6_v13',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v36',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v36',
        'HLT_DoubleEle8_eta1p22_mMax6_v13',
        'HLT_DoublePhoton33_CaloIdL_v18',
        'HLT_DoublePhoton70_v18',
        'HLT_DoublePhoton85_v26',
        'HLT_ECALHT800_v22',
        'HLT_Ele115_CaloIdVT_GsfTrkIdT_v28',
        'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele135_CaloIdVT_GsfTrkIdT_v21',
        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53_v9',
        'HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v32',
        'HLT_Ele15_IsoVVVL_PFHT450_v32',
        'HLT_Ele15_IsoVVVL_PFHT600_v36',
        'HLT_Ele17_CaloIdM_TrackIdM_PFJet30_v32',
        'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele23_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v33',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Loose_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Medium_eta2p3_CrossL1_v11',
        'HLT_Ele24_eta2p1_WPTight_Gsf_PNetTauhPFJet30_Tight_eta2p3_CrossL1_v11',
        'HLT_Ele28_HighEta_SC20_Mass55_v27',
        'HLT_Ele30_WPTight_Gsf_v16',
        'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v24',
        'HLT_Ele32_WPTight_Gsf_v30',
        'HLT_Ele35_WPTight_Gsf_v24',
        'HLT_Ele38_WPTight_Gsf_v24',
        'HLT_Ele40_WPTight_Gsf_v24',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v34',
        'HLT_Ele50_IsoVVVL_PFHT450_v32',
        'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30_v32',
        'HLT_Ele8_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Photon100EBHE10_v13',
        'HLT_Photon110EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon110EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon110EB_TightID_TightIso_v15',
        'HLT_Photon120_R9Id90_HE10_IsoM_v27',
        'HLT_Photon120_v24',
        'HLT_Photon150_v18',
        'HLT_Photon165_R9Id90_HE10_IsoM_v28',
        'HLT_Photon175_v26',
        'HLT_Photon200_v25',
        'HLT_Photon20_HoverELoose_v21',
        'HLT_Photon300_NoHE_v24',
        'HLT_Photon30EB_TightID_TightIso_v15',
        'HLT_Photon30_HoverELoose_v21',
        'HLT_Photon32_OneProng32_M50To105_v14',
        'HLT_Photon33_v16',
        'HLT_Photon34_R9Id90_CaloIdL_IsoL_DisplacedIdL_MediumChargedIsoDisplacedPFTauHPS34_v12',
        'HLT_Photon35_TwoProngs35_v17',
        'HLT_Photon40EB_TightID_TightIso_v6',
        'HLT_Photon40EB_v4',
        'HLT_Photon45EB_TightID_TightIso_v6',
        'HLT_Photon45EB_v4',
        'HLT_Photon50EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon50EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon50EB_TightID_TightIso_v11',
        'HLT_Photon50EB_v5',
        'HLT_Photon50_R9Id90_HE10_IsoM_v27',
        'HLT_Photon50_TimeGt2p5ns_v8',
        'HLT_Photon50_TimeLtNeg2p5ns_v8',
        'HLT_Photon50_v24',
        'HLT_Photon55EB_TightID_TightIso_v7',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT380_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT400_v14',
        'HLT_Photon60_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v13',
        'HLT_Photon75EB_TightID_TightIso_v11',
        'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v21',
        'HLT_Photon75_R9Id90_HE10_IsoM_v27',
        'HLT_Photon75_v24',
        'HLT_Photon90EB_TightID_TightIso_v11',
        'HLT_Photon90_R9Id90_HE10_IsoM_v27',
        'HLT_Photon90_v24',
        'HLT_SingleEle8_SingleEGL1_v12',
        'HLT_SingleEle8_v12'
    ),
    EcalLaser = cms.vstring('HLT_EcalCalibration_v4'),
    EmittanceScan0 = cms.vstring('HLT_L1AlwaysTrue_v1'),
    EmittanceScan1 = cms.vstring('HLT_L1AlwaysTrue_v1'),
    EmittanceScan2 = cms.vstring('HLT_L1AlwaysTrue_v1'),
    EmittanceScan3 = cms.vstring('HLT_L1AlwaysTrue_v1'),
    EmittanceScan4 = cms.vstring('HLT_L1AlwaysTrue_v1'),
    EmittanceScan5 = cms.vstring('HLT_L1AlwaysTrue_v1'),
    EphemeralHLTPhysics0 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics1 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics2 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics3 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics4 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics5 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics6 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralHLTPhysics7 = cms.vstring('HLT_EphemeralPhysics_v10'),
    EphemeralZeroBias0 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias1 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias2 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias3 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias4 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias5 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias6 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EphemeralZeroBias7 = cms.vstring('HLT_EphemeralZeroBias_v10'),
    EventDisplay = cms.vstring(
        'HLT_DoublePhoton85_v26',
        'HLT_PFJet500_v37',
        'HLT_Physics_v15'
    ),
    ExpressAlignment = cms.vstring(
        'HLT_HT300_Beamspot_v27',
        'HLT_ZeroBias_Beamspot_v20'
    ),
    ExpressPhysics = cms.vstring(
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_IsoMu20_v31',
        'HLT_IsoMu24_v29',
        'HLT_IsoMu27_v32',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v31',
        'HLT_Physics_v15',
        'HLT_Random_v3',
        'HLT_ZeroBias_Alignment_v9',
        'HLT_ZeroBias_FirstCollisionAfterAbortGap_v13',
        'HLT_ZeroBias_IsolatedBunches_v13',
        'HLT_ZeroBias_v14'
    ),
    HLTMonitor = cms.vstring(
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_Ele32_WPTight_Gsf_v30',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_v16',
        'HLT_HT400_DisplacedDijet40_DisplacedTrack_v26',
        'HLT_HT550_DisplacedDijet60_Inclusive_v26',
        'HLT_IsoMu24_HLTTracking_v4',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_v16',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_HLTTracking_v4',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_HLTTracking_v4',
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v31',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PNet2BTagMean0p50_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_v17',
        'HLT_PFHT510_v33',
        'HLT_PFJet260_v36',
        'HLT_PFJet320_v36',
        'HLT_PFMET130_PFMHT130_IDTight_v36',
        'HLT_PFMET140_PFMHT140_IDTight_v36'
    ),
    HLTPhysics = cms.vstring('HLT_Physics_v15'),
    HcalNZS = cms.vstring(
        'HLT_HcalNZS_v22',
        'HLT_HcalPhiSym_v24'
    ),
    JetMET0 = cms.vstring(
        'HLT_AK8DiPFJet250_250_SoftDropMass40_v10',
        'HLT_AK8DiPFJet250_250_SoftDropMass50_v10',
        'HLT_AK8DiPFJet260_260_SoftDropMass30_v10',
        'HLT_AK8DiPFJet260_260_SoftDropMass40_v10',
        'HLT_AK8DiPFJet270_270_SoftDropMass30_v10',
        'HLT_AK8DiPFJet280_280_SoftDropMass30_v16',
        'HLT_AK8DiPFJet290_290_SoftDropMass30_v10',
        'HLT_AK8PFJet140_v31',
        'HLT_AK8PFJet200_v31',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p50_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p53_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p55_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p60_v13',
        'HLT_AK8PFJet220_SoftDropMass40_v17',
        'HLT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet230_SoftDropMass40_v17',
        'HLT_AK8PFJet250_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet260_v32',
        'HLT_AK8PFJet275_Nch40_v10',
        'HLT_AK8PFJet275_Nch45_v10',
        'HLT_AK8PFJet275_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet320_v32',
        'HLT_AK8PFJet380_SoftDropMass30_v10',
        'HLT_AK8PFJet400_SoftDropMass30_v10',
        'HLT_AK8PFJet400_v32',
        'HLT_AK8PFJet40_v32',
        'HLT_AK8PFJet425_SoftDropMass30_v10',
        'HLT_AK8PFJet450_SoftDropMass30_v10',
        'HLT_AK8PFJet450_v32',
        'HLT_AK8PFJet500_v32',
        'HLT_AK8PFJet550_v27',
        'HLT_AK8PFJet60_v31',
        'HLT_AK8PFJet80_v32',
        'HLT_AK8PFJetFwd140_v30',
        'HLT_AK8PFJetFwd200_v30',
        'HLT_AK8PFJetFwd260_v31',
        'HLT_AK8PFJetFwd320_v31',
        'HLT_AK8PFJetFwd400_v31',
        'HLT_AK8PFJetFwd40_v31',
        'HLT_AK8PFJetFwd450_v31',
        'HLT_AK8PFJetFwd500_v31',
        'HLT_AK8PFJetFwd60_v30',
        'HLT_AK8PFJetFwd80_v30',
        'HLT_CaloJet500_NoJetID_v24',
        'HLT_CaloJet550_NoJetID_v19',
        'HLT_CaloMET350_NotCleaned_v16',
        'HLT_CaloMET90_NotCleaned_v16',
        'HLT_CaloMHT90_v16',
        'HLT_DiPFJetAve100_HFJEC_v33',
        'HLT_DiPFJetAve140_v29',
        'HLT_DiPFJetAve160_HFJEC_v32',
        'HLT_DiPFJetAve180_PPSMatch_Xi0p3_QuadJet_Max2ProtPerRP_v10',
        'HLT_DiPFJetAve200_v29',
        'HLT_DiPFJetAve220_HFJEC_v32',
        'HLT_DiPFJetAve260_HFJEC_v15',
        'HLT_DiPFJetAve260_v30',
        'HLT_DiPFJetAve300_HFJEC_v32',
        'HLT_DiPFJetAve320_v30',
        'HLT_DiPFJetAve400_v30',
        'HLT_DiPFJetAve40_v30',
        'HLT_DiPFJetAve500_v30',
        'HLT_DiPFJetAve60_HFJEC_v31',
        'HLT_DiPFJetAve60_v30',
        'HLT_DiPFJetAve80_HFJEC_v33',
        'HLT_DiPFJetAve80_v30',
        'HLT_DoublePFJets100_PNetBTag_0p11_v10',
        'HLT_DoublePFJets116MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_DoublePFJets128MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_DoublePFJets200_PNetBTag_0p11_v10',
        'HLT_DoublePFJets350_PNetBTag_0p11_v10',
        'HLT_DoublePFJets40_PNetBTag_0p11_v10',
        'HLT_HT350_v9',
        'HLT_HT425_v21',
        'HLT_L1ETMHadSeeds_v11',
        'HLT_L1Mu6HT240_v10',
        'HLT_MET105_IsoTrk50_v23',
        'HLT_MET120_IsoTrk50_v23',
        'HLT_Mu12_DoublePFJets100_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets200_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets350_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets40MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_Mu12_DoublePFJets40_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets54MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_Mu12eta2p3_PFJet40_v17',
        'HLT_Mu12eta2p3_v17',
        'HLT_PFHT1050_v34',
        'HLT_PFHT180_v33',
        'HLT_PFHT250_v33',
        'HLT_PFHT350_v35',
        'HLT_PFHT370_v33',
        'HLT_PFHT430_v33',
        'HLT_PFHT500_PFMET100_PFMHT100_IDTight_v28',
        'HLT_PFHT500_PFMET110_PFMHT110_IDTight_v28',
        'HLT_PFHT510_v33',
        'HLT_PFHT590_v33',
        'HLT_PFHT680_v33',
        'HLT_PFHT700_PFMET85_PFMHT85_IDTight_v28',
        'HLT_PFHT780_v33',
        'HLT_PFHT800_PFMET75_PFMHT75_IDTight_v28',
        'HLT_PFHT890_v33',
        'HLT_PFJet110_v16',
        'HLT_PFJet140_v35',
        'HLT_PFJet200_v35',
        'HLT_PFJet260_v36',
        'HLT_PFJet320_v36',
        'HLT_PFJet400_v36',
        'HLT_PFJet40_v37',
        'HLT_PFJet450_v37',
        'HLT_PFJet500_v37',
        'HLT_PFJet550_v27',
        'HLT_PFJet60_v37',
        'HLT_PFJet80_v37',
        'HLT_PFJetFwd140_v34',
        'HLT_PFJetFwd200_v34',
        'HLT_PFJetFwd260_v35',
        'HLT_PFJetFwd320_v35',
        'HLT_PFJetFwd400_v35',
        'HLT_PFJetFwd40_v35',
        'HLT_PFJetFwd450_v35',
        'HLT_PFJetFwd500_v35',
        'HLT_PFJetFwd60_v35',
        'HLT_PFJetFwd80_v34',
        'HLT_PFMET105_IsoTrk50_v17',
        'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v25',
        'HLT_PFMET120_PFMHT120_IDTight_v36',
        'HLT_PFMET130_PFMHT130_IDTight_v36',
        'HLT_PFMET140_PFMHT140_IDTight_v36',
        'HLT_PFMET200_BeamHaloCleaned_v25',
        'HLT_PFMET200_NotCleaned_v25',
        'HLT_PFMET250_NotCleaned_v25',
        'HLT_PFMET300_NotCleaned_v25',
        'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v25',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v36',
        'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v35',
        'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v35',
        'HLT_PFMETTypeOne140_PFMHT140_IDTight_v27',
        'HLT_PFMETTypeOne200_BeamHaloCleaned_v25'
    ),
    JetMET1 = cms.vstring(
        'HLT_AK8DiPFJet250_250_SoftDropMass40_v10',
        'HLT_AK8DiPFJet250_250_SoftDropMass50_v10',
        'HLT_AK8DiPFJet260_260_SoftDropMass30_v10',
        'HLT_AK8DiPFJet260_260_SoftDropMass40_v10',
        'HLT_AK8DiPFJet270_270_SoftDropMass30_v10',
        'HLT_AK8DiPFJet280_280_SoftDropMass30_v16',
        'HLT_AK8DiPFJet290_290_SoftDropMass30_v10',
        'HLT_AK8PFJet140_v31',
        'HLT_AK8PFJet200_v31',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p50_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p53_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p55_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p60_v13',
        'HLT_AK8PFJet220_SoftDropMass40_v17',
        'HLT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet230_SoftDropMass40_v17',
        'HLT_AK8PFJet250_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet260_v32',
        'HLT_AK8PFJet275_Nch40_v10',
        'HLT_AK8PFJet275_Nch45_v10',
        'HLT_AK8PFJet275_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet320_v32',
        'HLT_AK8PFJet380_SoftDropMass30_v10',
        'HLT_AK8PFJet400_SoftDropMass30_v10',
        'HLT_AK8PFJet400_v32',
        'HLT_AK8PFJet40_v32',
        'HLT_AK8PFJet425_SoftDropMass30_v10',
        'HLT_AK8PFJet450_SoftDropMass30_v10',
        'HLT_AK8PFJet450_v32',
        'HLT_AK8PFJet500_v32',
        'HLT_AK8PFJet550_v27',
        'HLT_AK8PFJet60_v31',
        'HLT_AK8PFJet80_v32',
        'HLT_AK8PFJetFwd140_v30',
        'HLT_AK8PFJetFwd200_v30',
        'HLT_AK8PFJetFwd260_v31',
        'HLT_AK8PFJetFwd320_v31',
        'HLT_AK8PFJetFwd400_v31',
        'HLT_AK8PFJetFwd40_v31',
        'HLT_AK8PFJetFwd450_v31',
        'HLT_AK8PFJetFwd500_v31',
        'HLT_AK8PFJetFwd60_v30',
        'HLT_AK8PFJetFwd80_v30',
        'HLT_CaloJet500_NoJetID_v24',
        'HLT_CaloJet550_NoJetID_v19',
        'HLT_CaloMET350_NotCleaned_v16',
        'HLT_CaloMET90_NotCleaned_v16',
        'HLT_CaloMHT90_v16',
        'HLT_DiPFJetAve100_HFJEC_v33',
        'HLT_DiPFJetAve140_v29',
        'HLT_DiPFJetAve160_HFJEC_v32',
        'HLT_DiPFJetAve180_PPSMatch_Xi0p3_QuadJet_Max2ProtPerRP_v10',
        'HLT_DiPFJetAve200_v29',
        'HLT_DiPFJetAve220_HFJEC_v32',
        'HLT_DiPFJetAve260_HFJEC_v15',
        'HLT_DiPFJetAve260_v30',
        'HLT_DiPFJetAve300_HFJEC_v32',
        'HLT_DiPFJetAve320_v30',
        'HLT_DiPFJetAve400_v30',
        'HLT_DiPFJetAve40_v30',
        'HLT_DiPFJetAve500_v30',
        'HLT_DiPFJetAve60_HFJEC_v31',
        'HLT_DiPFJetAve60_v30',
        'HLT_DiPFJetAve80_HFJEC_v33',
        'HLT_DiPFJetAve80_v30',
        'HLT_DoublePFJets100_PNetBTag_0p11_v10',
        'HLT_DoublePFJets116MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_DoublePFJets128MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_DoublePFJets200_PNetBTag_0p11_v10',
        'HLT_DoublePFJets350_PNetBTag_0p11_v10',
        'HLT_DoublePFJets40_PNetBTag_0p11_v10',
        'HLT_HT350_v9',
        'HLT_HT425_v21',
        'HLT_L1ETMHadSeeds_v11',
        'HLT_L1Mu6HT240_v10',
        'HLT_MET105_IsoTrk50_v23',
        'HLT_MET120_IsoTrk50_v23',
        'HLT_Mu12_DoublePFJets100_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets200_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets350_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets40MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_Mu12_DoublePFJets40_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets54MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_Mu12eta2p3_PFJet40_v17',
        'HLT_Mu12eta2p3_v17',
        'HLT_PFHT1050_v34',
        'HLT_PFHT180_v33',
        'HLT_PFHT250_v33',
        'HLT_PFHT350_v35',
        'HLT_PFHT370_v33',
        'HLT_PFHT430_v33',
        'HLT_PFHT500_PFMET100_PFMHT100_IDTight_v28',
        'HLT_PFHT500_PFMET110_PFMHT110_IDTight_v28',
        'HLT_PFHT510_v33',
        'HLT_PFHT590_v33',
        'HLT_PFHT680_v33',
        'HLT_PFHT700_PFMET85_PFMHT85_IDTight_v28',
        'HLT_PFHT780_v33',
        'HLT_PFHT800_PFMET75_PFMHT75_IDTight_v28',
        'HLT_PFHT890_v33',
        'HLT_PFJet110_v16',
        'HLT_PFJet140_v35',
        'HLT_PFJet200_v35',
        'HLT_PFJet260_v36',
        'HLT_PFJet320_v36',
        'HLT_PFJet400_v36',
        'HLT_PFJet40_v37',
        'HLT_PFJet450_v37',
        'HLT_PFJet500_v37',
        'HLT_PFJet550_v27',
        'HLT_PFJet60_v37',
        'HLT_PFJet80_v37',
        'HLT_PFJetFwd140_v34',
        'HLT_PFJetFwd200_v34',
        'HLT_PFJetFwd260_v35',
        'HLT_PFJetFwd320_v35',
        'HLT_PFJetFwd400_v35',
        'HLT_PFJetFwd40_v35',
        'HLT_PFJetFwd450_v35',
        'HLT_PFJetFwd500_v35',
        'HLT_PFJetFwd60_v35',
        'HLT_PFJetFwd80_v34',
        'HLT_PFMET105_IsoTrk50_v17',
        'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v25',
        'HLT_PFMET120_PFMHT120_IDTight_v36',
        'HLT_PFMET130_PFMHT130_IDTight_v36',
        'HLT_PFMET140_PFMHT140_IDTight_v36',
        'HLT_PFMET200_BeamHaloCleaned_v25',
        'HLT_PFMET200_NotCleaned_v25',
        'HLT_PFMET250_NotCleaned_v25',
        'HLT_PFMET300_NotCleaned_v25',
        'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v25',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v36',
        'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v35',
        'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v35',
        'HLT_PFMETTypeOne140_PFMHT140_IDTight_v27',
        'HLT_PFMETTypeOne200_BeamHaloCleaned_v25'
    ),
    L1Accept = cms.vstring(
        'DST_Physics_v17',
        'DST_ZeroBias_v12'
    ),
    MonteCarlo = cms.vstring(
        'MC_AK4CaloJetsFromPV_v21',
        'MC_AK4CaloJets_v21',
        'MC_AK4PFJetPNet_v9',
        'MC_AK4PFJets_v33',
        'MC_AK8CaloHT_v20',
        'MC_AK8PFHT_v32',
        'MC_AK8PFJetPNet_v9',
        'MC_AK8PFJets_v33',
        'MC_CaloHT_v20',
        'MC_CaloMET_JetIdCleaned_v21',
        'MC_CaloMET_v20',
        'MC_CaloMHT_v20',
        'MC_Diphoton10_10_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass10_v26',
        'MC_DoubleEle5_CaloIdL_MW_v29',
        'MC_DoubleMuNoFiltersNoVtx_v20',
        'MC_DoubleMu_TrkIsoVVL_DZ_v27',
        'MC_Egamma_Open_Unseeded_v12',
        'MC_Egamma_Open_v12',
        'MC_Ele15_Ele10_CaloIdL_TrackIdL_IsoVL_DZ_v29',
        'MC_Ele5_WPTight_Gsf_v23',
        'MC_IsoMu_v31',
        'MC_PFHT_v32',
        'MC_PFMET_v33',
        'MC_PFMHT_v32',
        'MC_PFScouting_v10',
        'MC_ReducedIterativeTracking_v26'
    ),
    Muon0 = cms.vstring(
        'HLT_CascadeMu100_v16',
        'HLT_CscCluster100_Ele5_v7',
        'HLT_CscCluster100_Mu5_v10',
        'HLT_CscCluster100_PNetTauhPFJet10_Loose_v10',
        'HLT_CscCluster50_Photon20Unseeded_v5',
        'HLT_CscCluster50_Photon30Unseeded_v5',
        'HLT_CscCluster_Loose_v11',
        'HLT_CscCluster_Medium_v11',
        'HLT_CscCluster_Tight_v11',
        'HLT_DisplacedMu24_MediumChargedIsoDisplacedPFTauHPS24_v12',
        'HLT_DoubleCscCluster100_v8',
        'HLT_DoubleCscCluster75_v8',
        'HLT_DoubleL2Mu10NoVtx_2Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v16',
        'HLT_DoubleL2Mu12NoVtx_2Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu12NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu14NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v12',
        'HLT_DoubleL2Mu23NoVtx_2Cha_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_Eta2p4_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_v12',
        'HLT_DoubleL2Mu30NoVtx_2Cha_CosmicSeed_Eta2p4_v12',
        'HLT_DoubleL2Mu30NoVtx_2Cha_Eta2p4_v12',
        'HLT_DoubleL2Mu50_v12',
        'HLT_DoubleL2Mu_L3Mu16NoVtx_VetoL3Mu0DxyMax0p1cm_v13',
        'HLT_DoubleL2Mu_L3Mu18NoVtx_VetoL3Mu0DxyMax0p1cm_v13',
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v14',
        'HLT_DoubleL3Mu18_10NoVtx_DxyMin0p01cm_v13',
        'HLT_DoubleL3Mu20_10NoVtx_DxyMin0p01cm_v13',
        'HLT_DoubleL3dTksMu16_10NoVtx_DxyMin0p01cm_v14',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_noDCA_v10',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_v10',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v26',
        'HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v26',
        'HLT_DoubleMu3_DZ_PFMET70_PFMHT70_v26',
        'HLT_DoubleMu3_DZ_PFMET90_PFMHT90_v26',
        'HLT_DoubleMu43NoFiltersNoVtx_v17',
        'HLT_DoubleMu48NoFiltersNoVtx_v17',
        'HLT_DoubleMu4_Mass3p8_DZ_PFHT350_v24',
        'HLT_HighPtTkMu100_v16',
        'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Loose_eta2p3_CrossL1_v10',
        'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Medium_eta2p3_CrossL1_v10',
        'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Tight_eta2p3_CrossL1_v10',
        'HLT_IsoMu20_v31',
        'HLT_IsoMu24_OneProng32_v13',
        'HLT_IsoMu24_TwoProngs35_v17',
        'HLT_IsoMu24_eta2p1_L1HT200_QuadPFJet25_PNet1Tauh0p50_v4',
        'HLT_IsoMu24_eta2p1_L1HT200_QuadPFJet25_v4',
        'HLT_IsoMu24_eta2p1_L1HT200_v4',
        'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_PNet1Tauh0p50_v10',
        'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_v10',
        'HLT_IsoMu24_eta2p1_PFHT250_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Loose_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Medium_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Tight_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet20_eta2p2_SingleL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_PFJet60_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_PFJet75_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Loose_eta2p3_CrossL1_ETau_Monitoring_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_eta2p3_CrossL1_ETau_Monitoring_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_eta2p3_CrossL1_ETau_Monitoring_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet45_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_SinglePFJet25_PNet1Tauh0p50_v10',
        'HLT_IsoMu24_eta2p1_v31',
        'HLT_IsoMu24_v29',
        'HLT_IsoMu27_MediumChargedIsoDisplacedPFTauHPS24_eta2p1_SingleL1_v12',
        'HLT_IsoMu27_v32',
        'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_v16',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_v16',
        'HLT_IsoTrk200_L1SingleMuShower_v8',
        'HLT_IsoTrk400_L1SingleMuShower_v8',
        'HLT_L1CSCShower_DTCluster50_v11',
        'HLT_L1CSCShower_DTCluster75_v11',
        'HLT_L2Mu50NoVtx_3Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v8',
        'HLT_L2Mu50NoVtx_3Cha_VetoL3Mu0DxyMax1cm_v8',
        'HLT_L3Mu30NoVtx_DxyMin0p01cm_v6',
        'HLT_L3Mu50NoVtx_DxyMin0p01cm_v6',
        'HLT_L3dTksMu10_NoVtx_DxyMin0p01cm_v14',
        'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53_v9',
        'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v31',
        'HLT_Mu15_IsoVVVL_PFHT450_v31',
        'HLT_Mu15_IsoVVVL_PFHT600_v35',
        'HLT_Mu15_v19',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_AK8CaloJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_AK8PFJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_CaloJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_PFJet30_v10',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v31',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v30',
        'HLT_Mu17_TrkIsoVVL_v29',
        'HLT_Mu17_v29',
        'HLT_Mu18_Mu9_SameSign_v20',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_v19',
        'HLT_Mu19_TrkIsoVVL_v20',
        'HLT_Mu19_v20',
        'HLT_Mu20_v28',
        'HLT_Mu27_v29',
        'HLT_Mu37_TkMu27_v21',
        'HLT_Mu3_PFJet40_v32',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight_v18',
        'HLT_Mu50_IsoVVVL_PFHT450_v31',
        'HLT_Mu50_L1SingleMuShower_v15',
        'HLT_Mu50_v29',
        'HLT_Mu55_v19',
        'HLT_Mu8_TrkIsoVVL_v28',
        'HLT_Mu8_v28',
        'HLT_TripleMu_10_5_5_DZ_v26',
        'HLT_TripleMu_12_10_5_v26',
        'HLT_TripleMu_5_3_3_Mass3p8_DCA_v19',
        'HLT_TripleMu_5_3_3_Mass3p8_DZ_v24',
        'HLT_TrkMu12_DoubleTrkMu5NoFiltersNoVtx_v21'
    ),
    Muon1 = cms.vstring(
        'HLT_CascadeMu100_v16',
        'HLT_CscCluster100_Ele5_v7',
        'HLT_CscCluster100_Mu5_v10',
        'HLT_CscCluster100_PNetTauhPFJet10_Loose_v10',
        'HLT_CscCluster50_Photon20Unseeded_v5',
        'HLT_CscCluster50_Photon30Unseeded_v5',
        'HLT_CscCluster_Loose_v11',
        'HLT_CscCluster_Medium_v11',
        'HLT_CscCluster_Tight_v11',
        'HLT_DisplacedMu24_MediumChargedIsoDisplacedPFTauHPS24_v12',
        'HLT_DoubleCscCluster100_v8',
        'HLT_DoubleCscCluster75_v8',
        'HLT_DoubleL2Mu10NoVtx_2Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v16',
        'HLT_DoubleL2Mu12NoVtx_2Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu12NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu14NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v12',
        'HLT_DoubleL2Mu23NoVtx_2Cha_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_Eta2p4_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_v12',
        'HLT_DoubleL2Mu30NoVtx_2Cha_CosmicSeed_Eta2p4_v12',
        'HLT_DoubleL2Mu30NoVtx_2Cha_Eta2p4_v12',
        'HLT_DoubleL2Mu50_v12',
        'HLT_DoubleL2Mu_L3Mu16NoVtx_VetoL3Mu0DxyMax0p1cm_v13',
        'HLT_DoubleL2Mu_L3Mu18NoVtx_VetoL3Mu0DxyMax0p1cm_v13',
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v14',
        'HLT_DoubleL3Mu18_10NoVtx_DxyMin0p01cm_v13',
        'HLT_DoubleL3Mu20_10NoVtx_DxyMin0p01cm_v13',
        'HLT_DoubleL3dTksMu16_10NoVtx_DxyMin0p01cm_v14',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_noDCA_v10',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_v10',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v26',
        'HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v26',
        'HLT_DoubleMu3_DZ_PFMET70_PFMHT70_v26',
        'HLT_DoubleMu3_DZ_PFMET90_PFMHT90_v26',
        'HLT_DoubleMu43NoFiltersNoVtx_v17',
        'HLT_DoubleMu48NoFiltersNoVtx_v17',
        'HLT_DoubleMu4_Mass3p8_DZ_PFHT350_v24',
        'HLT_HighPtTkMu100_v16',
        'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Loose_eta2p3_CrossL1_v10',
        'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Medium_eta2p3_CrossL1_v10',
        'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Tight_eta2p3_CrossL1_v10',
        'HLT_IsoMu20_v31',
        'HLT_IsoMu24_OneProng32_v13',
        'HLT_IsoMu24_TwoProngs35_v17',
        'HLT_IsoMu24_eta2p1_L1HT200_QuadPFJet25_PNet1Tauh0p50_v4',
        'HLT_IsoMu24_eta2p1_L1HT200_QuadPFJet25_v4',
        'HLT_IsoMu24_eta2p1_L1HT200_v4',
        'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_PNet1Tauh0p50_v10',
        'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_v10',
        'HLT_IsoMu24_eta2p1_PFHT250_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Loose_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Medium_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Tight_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet20_eta2p2_SingleL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_PFJet60_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_PFJet75_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Loose_eta2p3_CrossL1_ETau_Monitoring_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_eta2p3_CrossL1_ETau_Monitoring_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_eta2p3_CrossL1_ETau_Monitoring_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet45_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_SinglePFJet25_PNet1Tauh0p50_v10',
        'HLT_IsoMu24_eta2p1_v31',
        'HLT_IsoMu24_v29',
        'HLT_IsoMu27_MediumChargedIsoDisplacedPFTauHPS24_eta2p1_SingleL1_v12',
        'HLT_IsoMu27_v32',
        'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_v16',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_v16',
        'HLT_IsoTrk200_L1SingleMuShower_v8',
        'HLT_IsoTrk400_L1SingleMuShower_v8',
        'HLT_L1CSCShower_DTCluster50_v11',
        'HLT_L1CSCShower_DTCluster75_v11',
        'HLT_L2Mu50NoVtx_3Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v8',
        'HLT_L2Mu50NoVtx_3Cha_VetoL3Mu0DxyMax1cm_v8',
        'HLT_L3Mu30NoVtx_DxyMin0p01cm_v6',
        'HLT_L3Mu50NoVtx_DxyMin0p01cm_v6',
        'HLT_L3dTksMu10_NoVtx_DxyMin0p01cm_v14',
        'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53_v9',
        'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v31',
        'HLT_Mu15_IsoVVVL_PFHT450_v31',
        'HLT_Mu15_IsoVVVL_PFHT600_v35',
        'HLT_Mu15_v19',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_AK8CaloJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_AK8PFJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_CaloJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_PFJet30_v10',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v31',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v30',
        'HLT_Mu17_TrkIsoVVL_v29',
        'HLT_Mu17_v29',
        'HLT_Mu18_Mu9_SameSign_v20',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_v19',
        'HLT_Mu19_TrkIsoVVL_v20',
        'HLT_Mu19_v20',
        'HLT_Mu20_v28',
        'HLT_Mu27_v29',
        'HLT_Mu37_TkMu27_v21',
        'HLT_Mu3_PFJet40_v32',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight_v18',
        'HLT_Mu50_IsoVVVL_PFHT450_v31',
        'HLT_Mu50_L1SingleMuShower_v15',
        'HLT_Mu50_v29',
        'HLT_Mu55_v19',
        'HLT_Mu8_TrkIsoVVL_v28',
        'HLT_Mu8_v28',
        'HLT_TripleMu_10_5_5_DZ_v26',
        'HLT_TripleMu_12_10_5_v26',
        'HLT_TripleMu_5_3_3_Mass3p8_DCA_v19',
        'HLT_TripleMu_5_3_3_Mass3p8_DZ_v24',
        'HLT_TrkMu12_DoubleTrkMu5NoFiltersNoVtx_v21'
    ),
    MuonEG = cms.vstring(
        'HLT_DiMu4_Ele9_CaloIdL_TrackIdL_DZ_Mass3p8_v33',
        'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v33',
        'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v33',
        'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v31',
        'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v23',
        'HLT_Mu17_Photon30_IsoCaloId_v22',
        'HLT_Mu20NoFiltersNoVtxDisplaced_Photon20_CaloCustomId_v14',
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v31',
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v23',
        'HLT_Mu27_Ele37_CaloIdL_MW_v21',
        'HLT_Mu37_Ele27_CaloIdL_MW_v21',
        'HLT_Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL_v14',
        'HLT_Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL_v14',
        'HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL_v18',
        'HLT_Mu48NoFiltersNoVtx_Photon48_CaloIdL_v18',
        'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v34',
        'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v34',
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v35',
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_v35',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_DoubleAK4PFJet60_30_PNet2BTagMean0p50_v14',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_DoubleAK4PFJet60_30_v14',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_QuadPFJet20_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_QuadPFJet25_PNet1BTag0p50_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_QuadPFJet25_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PNet2BTagMean0p50_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_v17',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_QuadPFJet25_PNet1BTag0p20_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_QuadPFJet25_PNet2BTagMean0p55_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_QuadPFJet25_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT280_QuadPFJet30_PNet2BTagMean0p55_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT280_QuadPFJet30_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT280_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v29',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v27'
    ),
    NoBPTX = cms.vstring(
        'HLT_CDC_L2cosmic_10_er1p0_v11',
        'HLT_CDC_L2cosmic_5p5_er1p0_v11',
        'HLT_L2Mu10_NoVertex_NoBPTX3BX_v15',
        'HLT_L2Mu10_NoVertex_NoBPTX_v16',
        'HLT_L2Mu40_NoVertex_3Sta_NoBPTX3BX_v15',
        'HLT_L2Mu45_NoVertex_3Sta_NoBPTX3BX_v14',
        'HLT_UncorrectedJetE30_NoBPTX3BX_v16',
        'HLT_UncorrectedJetE30_NoBPTX_v16',
        'HLT_UncorrectedJetE60_NoBPTX3BX_v16',
        'HLT_UncorrectedJetE70_NoBPTX3BX_v16'
    ),
    OnlineMonitor = cms.vstring( (
        'HLT_AK8DiPFJet250_250_SoftDropMass40_v10',
        'HLT_AK8DiPFJet250_250_SoftDropMass50_v10',
        'HLT_AK8DiPFJet260_260_SoftDropMass30_v10',
        'HLT_AK8DiPFJet260_260_SoftDropMass40_v10',
        'HLT_AK8DiPFJet270_270_SoftDropMass30_v10',
        'HLT_AK8DiPFJet280_280_SoftDropMass30_v16',
        'HLT_AK8DiPFJet290_290_SoftDropMass30_v10',
        'HLT_AK8PFJet140_v31',
        'HLT_AK8PFJet200_v31',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p50_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p53_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p55_v13',
        'HLT_AK8PFJet220_SoftDropMass40_PNetBB0p06_DoubleAK4PFJet60_30_PNet2BTagMean0p60_v13',
        'HLT_AK8PFJet220_SoftDropMass40_v17',
        'HLT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet230_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet230_SoftDropMass40_v17',
        'HLT_AK8PFJet250_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet250_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet260_v32',
        'HLT_AK8PFJet275_Nch40_v10',
        'HLT_AK8PFJet275_Nch45_v10',
        'HLT_AK8PFJet275_SoftDropMass40_PNetBB0p06_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetBB0p10_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetTauTau0p03_v13',
        'HLT_AK8PFJet275_SoftDropMass40_PNetTauTau0p05_v13',
        'HLT_AK8PFJet320_v32',
        'HLT_AK8PFJet380_SoftDropMass30_v10',
        'HLT_AK8PFJet400_SoftDropMass30_v10',
        'HLT_AK8PFJet400_v32',
        'HLT_AK8PFJet40_v32',
        'HLT_AK8PFJet425_SoftDropMass30_v10',
        'HLT_AK8PFJet450_SoftDropMass30_v10',
        'HLT_AK8PFJet450_v32',
        'HLT_AK8PFJet500_v32',
        'HLT_AK8PFJet550_v27',
        'HLT_AK8PFJet60_v31',
        'HLT_AK8PFJet80_v32',
        'HLT_AK8PFJetFwd140_v30',
        'HLT_AK8PFJetFwd200_v30',
        'HLT_AK8PFJetFwd260_v31',
        'HLT_AK8PFJetFwd320_v31',
        'HLT_AK8PFJetFwd400_v31',
        'HLT_AK8PFJetFwd40_v31',
        'HLT_AK8PFJetFwd450_v31',
        'HLT_AK8PFJetFwd500_v31',
        'HLT_AK8PFJetFwd60_v30',
        'HLT_AK8PFJetFwd80_v30',
        'HLT_BTagMu_AK4DiJet110_Mu5_v29',
        'HLT_BTagMu_AK4DiJet170_Mu5_v28',
        'HLT_BTagMu_AK4DiJet20_Mu5_v29',
        'HLT_BTagMu_AK4DiJet40_Mu5_v29',
        'HLT_BTagMu_AK4DiJet70_Mu5_v29',
        'HLT_BTagMu_AK4Jet300_Mu5_v28',
        'HLT_BTagMu_AK8DiJet170_Mu5_v25',
        'HLT_BTagMu_AK8Jet170_DoubleMu5_v18',
        'HLT_BTagMu_AK8Jet300_Mu5_v28',
        'HLT_CDC_L2cosmic_10_er1p0_v11',
        'HLT_CDC_L2cosmic_5p5_er1p0_v11',
        'HLT_CaloJet500_NoJetID_v24',
        'HLT_CaloJet550_NoJetID_v19',
        'HLT_CaloMET350_NotCleaned_v16',
        'HLT_CaloMET60_DTCluster50_v13',
        'HLT_CaloMET60_DTClusterNoMB1S50_v13',
        'HLT_CaloMET90_NotCleaned_v16',
        'HLT_CaloMHT90_v16',
        'HLT_CascadeMu100_v16',
        'HLT_CscCluster50_Photon20Unseeded_v5',
        'HLT_CscCluster50_Photon30Unseeded_v5',
        'HLT_CscCluster_Loose_v11',
        'HLT_CscCluster_Medium_v11',
        'HLT_CscCluster_Tight_v11',
        'HLT_DiEle27_WPTightCaloOnly_L1DoubleEG_v16',
        'HLT_DiMu4_Ele9_CaloIdL_TrackIdL_DZ_Mass3p8_v33',
        'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v33',
        'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v33',
        'HLT_DiPFJetAve100_HFJEC_v33',
        'HLT_DiPFJetAve140_v29',
        'HLT_DiPFJetAve160_HFJEC_v32',
        'HLT_DiPFJetAve200_v29',
        'HLT_DiPFJetAve220_HFJEC_v32',
        'HLT_DiPFJetAve260_HFJEC_v15',
        'HLT_DiPFJetAve260_v30',
        'HLT_DiPFJetAve300_HFJEC_v32',
        'HLT_DiPFJetAve320_v30',
        'HLT_DiPFJetAve400_v30',
        'HLT_DiPFJetAve40_v30',
        'HLT_DiPFJetAve500_v30',
        'HLT_DiPFJetAve60_HFJEC_v31',
        'HLT_DiPFJetAve60_v30',
        'HLT_DiPFJetAve80_HFJEC_v33',
        'HLT_DiPFJetAve80_v30',
        'HLT_DiPhoton10Time1ns_v11',
        'HLT_DiPhoton10Time1p2ns_v11',
        'HLT_DiPhoton10Time1p4ns_v11',
        'HLT_DiPhoton10Time1p6ns_v11',
        'HLT_DiPhoton10Time1p8ns_v11',
        'HLT_DiPhoton10Time2ns_v11',
        'HLT_DiPhoton10_CaloIdL_v11',
        'HLT_DiSC30_18_EIso_AND_HE_Mass70_v25',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2_v4',
        'HLT_Dielectron12_5_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v4',
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_10_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2_v3',
        'HLT_Diphoton15_12_EBEB_TightID_ECALTrackIsoDr0p2to0p4_v3',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton20_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton22_14_eta1p5_R9IdL_AND_HE_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_14_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton24_16_eta1p5_R9IdL_AND_HET_AND_IsoTCaloIdT_v13',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_Mass55_v14',
        'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_v14',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v26',
        'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v26',
        'HLT_DiphotonMVA14p25_High_Mass60_v1',
        'HLT_DiphotonMVA14p25_Low_Mass60_v1',
        'HLT_DiphotonMVA14p25_Medium_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightHigh_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightLow_Mass60_v1',
        'HLT_DiphotonMVA14p25_TightMedium_Mass60_v1',
        'HLT_DisplacedMu24_MediumChargedIsoDisplacedPFTauHPS24_v12',
        'HLT_DoubleCscCluster100_v8',
        'HLT_DoubleCscCluster75_v8',
        'HLT_DoubleEle25_CaloIdL_MW_v18',
        'HLT_DoubleEle27_CaloIdL_MW_v18',
        'HLT_DoubleEle33_CaloIdL_MW_v31',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v36',
        'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v36',
        'HLT_DoubleL2Mu10NoVtx_2Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu10NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v16',
        'HLT_DoubleL2Mu12NoVtx_2Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu12NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu14NoVtx_2Cha_VetoL3Mu0DxyMax1cm_v15',
        'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v12',
        'HLT_DoubleL2Mu23NoVtx_2Cha_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_Eta2p4_v12',
        'HLT_DoubleL2Mu25NoVtx_2Cha_v12',
        'HLT_DoubleL2Mu30NoVtx_2Cha_CosmicSeed_Eta2p4_v12',
        'HLT_DoubleL2Mu30NoVtx_2Cha_Eta2p4_v12',
        'HLT_DoubleL2Mu50_v12',
        'HLT_DoubleL2Mu_L3Mu16NoVtx_VetoL3Mu0DxyMax0p1cm_v13',
        'HLT_DoubleL2Mu_L3Mu18NoVtx_VetoL3Mu0DxyMax0p1cm_v13',
        'HLT_DoubleL3Mu16_10NoVtx_DxyMin0p01cm_v14',
        'HLT_DoubleL3Mu18_10NoVtx_DxyMin0p01cm_v13',
        'HLT_DoubleL3Mu20_10NoVtx_DxyMin0p01cm_v13',
        'HLT_DoubleL3dTksMu16_10NoVtx_DxyMin0p01cm_v14',
        'HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_noDxy_v12',
        'HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_v17',
        'HLT_DoubleMediumChargedIsoDisplacedPFTauHPS36_Trk1_eta2p1_v12',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_noDCA_v10',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_v10',
        'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v26',
        'HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v26',
        'HLT_DoubleMu3_DZ_PFMET70_PFMHT70_v26',
        'HLT_DoubleMu3_DZ_PFMET90_PFMHT90_v26',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu43NoFiltersNoVtx_v17',
        'HLT_DoubleMu48NoFiltersNoVtx_v17',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_Mass3p8_DZ_PFHT350_v24',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_DoublePFJets100_PNetBTag_0p11_v10',
        'HLT_DoublePFJets116MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_DoublePFJets128MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_DoublePFJets200_PNetBTag_0p11_v10',
        'HLT_DoublePFJets350_PNetBTag_0p11_v10',
        'HLT_DoublePFJets40_PNetBTag_0p11_v10',
        'HLT_DoublePhoton33_CaloIdL_v18',
        'HLT_DoublePhoton70_v18',
        'HLT_DoublePhoton85_v26',
        'HLT_ECALHT800_v22',
        'HLT_Ele115_CaloIdVT_GsfTrkIdT_v28',
        'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele135_CaloIdVT_GsfTrkIdT_v21',
        'HLT_Ele14_eta2p5_IsoVVVL_Gsf_PFHT200_PNetBTag0p53_v9',
        'HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v32',
        'HLT_Ele15_IsoVVVL_PFHT450_v32',
        'HLT_Ele15_IsoVVVL_PFHT600_v36',
        'HLT_Ele17_CaloIdM_TrackIdM_PFJet30_v32',
        'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30_v34',
        'HLT_Ele23_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v33',
        'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v33',
        'HLT_Ele28_HighEta_SC20_Mass55_v27',
        'HLT_Ele30_WPTight_Gsf_v16',
        'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v24',
        'HLT_Ele32_WPTight_Gsf_v30',
        'HLT_Ele35_WPTight_Gsf_v24',
        'HLT_Ele38_WPTight_Gsf_v24',
        'HLT_Ele40_WPTight_Gsf_v24',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet220_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_AK8PFJet230_SoftDropMass40_v16',
        'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v34',
        'HLT_Ele50_IsoVVVL_PFHT450_v32',
        'HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30_v32',
        'HLT_Ele8_CaloIdM_TrackIdM_PFJet30_v34',
        'HLT_HT170_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay0p5nsTrackless_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay1nsInclusive_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay1nsTrackless_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay2nsInclusive_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet60_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_PFJet60_NeutralHadronFrac0p7_v10',
        'HLT_HT200_L1SingleLLPJet_PFJet60_NeutralHadronFrac0p8_v10',
        'HLT_HT240_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v11',
        'HLT_HT270_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT280_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v11',
        'HLT_HT320_L1SingleLLPJet_DisplacedDijet60_Inclusive_v14',
        'HLT_HT350_DelayedJet40_SingleDelay3nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3p25nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3p5nsInclusive_v9',
        'HLT_HT350_v9',
        'HLT_HT400_DisplacedDijet40_DisplacedTrack_v26',
        'HLT_HT420_L1SingleLLPJet_DisplacedDijet60_Inclusive_v14',
        'HLT_HT425_v21',
        'HLT_HT430_DelayedJet40_DoubleDelay0p5nsInclusive_v12',
        'HLT_HT430_DelayedJet40_DoubleDelay0p5nsTrackless_v14',
        'HLT_HT430_DelayedJet40_DoubleDelay0p75nsTrackless_v10',
        'HLT_HT430_DelayedJet40_DoubleDelay1nsInclusive_v13',
        'HLT_HT430_DelayedJet40_DoubleDelay1nsTrackless_v10',
        'HLT_HT430_DelayedJet40_DoubleDelay1p25nsInclusive_v9',
        'HLT_HT430_DelayedJet40_DoubleDelay1p5nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay0p5nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay0p5nsTrackless_v12',
        'HLT_HT430_DelayedJet40_SingleDelay1nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay1nsTrackless_v14',
        'HLT_HT430_DelayedJet40_SingleDelay1p25nsTrackless_v10',
        'HLT_HT430_DelayedJet40_SingleDelay1p5nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay1p5nsTrackless_v10',
        'HLT_HT430_DelayedJet40_SingleDelay2nsInclusive_v13',
        'HLT_HT430_DelayedJet40_SingleDelay2p25nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay2p5nsInclusive_v9',
        'HLT_HT550_DisplacedDijet60_Inclusive_v26',
        'HLT_HcalNZS_v22',
        'HLT_HcalPhiSym_v24',
        'HLT_HighPtTkMu100_v16',
        'HLT_IsoMu20_v31',
        'HLT_IsoMu24_OneProng32_v13',
        'HLT_IsoMu24_TwoProngs35_v17',
        'HLT_IsoMu24_eta2p1_L1HT200_QuadPFJet25_PNet1Tauh0p50_v4',
        'HLT_IsoMu24_eta2p1_L1HT200_QuadPFJet25_v4',
        'HLT_IsoMu24_eta2p1_L1HT200_v4',
        'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_PNet1Tauh0p50_v10',
        'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_v10',
        'HLT_IsoMu24_eta2p1_PFHT250_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Loose_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Medium_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Tight_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_L2NN_eta2p3_CrossL1_v10',
        'HLT_IsoMu24_eta2p1_SinglePFJet25_PNet1Tauh0p50_v10',
        'HLT_IsoMu24_eta2p1_v31',
        'HLT_IsoMu24_v29',
        'HLT_IsoMu27_MediumChargedIsoDisplacedPFTauHPS24_eta2p1_SingleL1_v12',
        'HLT_IsoMu27_v32',
        'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_v16',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p06_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p10_v13',
        'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_v16',
        'HLT_L1CSCShower_DTCluster50_v11',
        'HLT_L1CSCShower_DTCluster75_v11',
        'HLT_L1ETMHadSeeds_v11',
        'HLT_L1MET_DTCluster50_v13',
        'HLT_L1MET_DTClusterNoMB1S50_v13',
        'HLT_L1Mu6HT240_v10',
        'HLT_L1SingleLLPJet_v8',
        'HLT_L1SingleMuCosmics_v9',
        'HLT_L1Tau_DelayedJet40_DoubleDelay0p5nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_DoubleDelay0p75nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p25nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p25nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p5nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p5nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p75nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p5nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p75nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_SingleDelay3nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_SingleDelay3p5nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_SingleDelay3p75nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay4nsInclusive_v9',
        'HLT_L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142_v10',
        'HLT_L2Mu10_NoVertex_NoBPTX3BX_v15',
        'HLT_L2Mu10_NoVertex_NoBPTX_v16',
        'HLT_L2Mu40_NoVertex_3Sta_NoBPTX3BX_v15',
        'HLT_L2Mu45_NoVertex_3Sta_NoBPTX3BX_v14',
        'HLT_L2Mu50NoVtx_3Cha_CosmicSeed_VetoL3Mu0DxyMax1cm_v8',
        'HLT_L2Mu50NoVtx_3Cha_VetoL3Mu0DxyMax1cm_v8',
        'HLT_L3Mu30NoVtx_DxyMin0p01cm_v6',
        'HLT_L3Mu50NoVtx_DxyMin0p01cm_v6',
        'HLT_L3dTksMu10_NoVtx_DxyMin0p01cm_v14',
        'HLT_MET105_IsoTrk50_v23',
        'HLT_MET120_IsoTrk50_v23',
        'HLT_Mu12_DoublePFJets100_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets200_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets350_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets40MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_Mu12_DoublePFJets40_PNetBTag_0p11_v10',
        'HLT_Mu12_DoublePFJets54MaxDeta1p6_PNet2BTag_0p11_v10',
        'HLT_Mu12_IsoVVL_PFHT150_PNetBTag0p53_v9',
        'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v31',
        'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v23',
        'HLT_Mu12eta2p3_PFJet40_v17',
        'HLT_Mu12eta2p3_v17',
        'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v31',
        'HLT_Mu15_IsoVVVL_PFHT450_v31',
        'HLT_Mu15_IsoVVVL_PFHT600_v35',
        'HLT_Mu15_v19',
        'HLT_Mu17_Photon30_IsoCaloId_v22',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_AK8CaloJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_AK8PFJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_CaloJet30_v9',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_PFJet30_v10',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v21',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v31',
        'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_v30',
        'HLT_Mu17_TrkIsoVVL_v29',
        'HLT_Mu17_v29',
        'HLT_Mu18_Mu9_SameSign_v20',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_v19',
        'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_v19',
        'HLT_Mu19_TrkIsoVVL_v20',
        'HLT_Mu19_v20',
        'HLT_Mu20NoFiltersNoVtxDisplaced_Photon20_CaloCustomId_v14',
        'HLT_Mu20_v28',
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v31',
        'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v23',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu27_Ele37_CaloIdL_MW_v21',
        'HLT_Mu27_v29',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu37_Ele27_CaloIdL_MW_v21',
        'HLT_Mu37_TkMu27_v21',
        'HLT_Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL_v14',
        'HLT_Mu3_PFJet40_v32',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight_v18',
        'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight_v18',
        'HLT_Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL_v14',
        'HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL_v18',
        'HLT_Mu48NoFiltersNoVtx_Photon48_CaloIdL_v18',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu50_IsoVVVL_PFHT450_v31',
        'HLT_Mu50_L1SingleMuShower_v15',
        'HLT_Mu50_v29',
        'HLT_Mu55_v19',
        'HLT_Mu6HT240_DisplacedDijet30_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet35_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet35_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet40_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet40_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet45_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet50_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v34',
        'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v34',
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v35',
        'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_v35',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_DoubleAK4PFJet60_30_PNet2BTagMean0p50_v14',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_DoubleAK4PFJet60_30_v14',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_QuadPFJet20_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_QuadPFJet25_PNet1BTag0p50_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_QuadPFJet25_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_L1HT200_v4',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PNet2BTagMean0p50_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_v17',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_QuadPFJet25_PNet1BTag0p20_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_QuadPFJet25_PNet2BTagMean0p55_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_QuadPFJet25_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT250_v10',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT280_QuadPFJet30_PNet2BTagMean0p55_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT280_QuadPFJet30_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFHT280_v13',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v29',
        'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v27',
        'HLT_Mu8_TrkIsoVVL_v28',
        'HLT_Mu8_v28',
        'HLT_PFHT1050_v34',
        'HLT_PFHT180_v33',
        'HLT_PFHT250_v33',
        'HLT_PFHT350_v35',
        'HLT_PFHT370_v33',
        'HLT_PFHT430_v33',
        'HLT_PFHT500_PFMET100_PFMHT100_IDTight_v28',
        'HLT_PFHT500_PFMET110_PFMHT110_IDTight_v28',
        'HLT_PFHT510_v33',
        'HLT_PFHT590_v33',
        'HLT_PFHT680_v33',
        'HLT_PFHT700_PFMET85_PFMHT85_IDTight_v28',
        'HLT_PFHT780_v33',
        'HLT_PFHT800_PFMET75_PFMHT75_IDTight_v28',
        'HLT_PFHT890_v33',
        'HLT_PFJet110_v16',
        'HLT_PFJet140_v35',
        'HLT_PFJet200_TimeGt2p5ns_v14',
        'HLT_PFJet200_TimeLtNeg2p5ns_v14',
        'HLT_PFJet200_v35',
        'HLT_PFJet260_v36',
        'HLT_PFJet320_v36',
        'HLT_PFJet400_v36',
        'HLT_PFJet40_v37',
        'HLT_PFJet450_v37',
        'HLT_PFJet500_v37',
        'HLT_PFJet550_v27',
        'HLT_PFJet60_v37',
        'HLT_PFJet80_v37',
        'HLT_PFJetFwd140_v34',
        'HLT_PFJetFwd200_v34',
        'HLT_PFJetFwd260_v35',
        'HLT_PFJetFwd320_v35',
        'HLT_PFJetFwd400_v35',
        'HLT_PFJetFwd40_v35',
        'HLT_PFJetFwd450_v35',
        'HLT_PFJetFwd500_v35',
        'HLT_PFJetFwd60_v35',
        'HLT_PFJetFwd80_v34',
        'HLT_PFMET105_IsoTrk50_v17',
        'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v25',
        'HLT_PFMET120_PFMHT120_IDTight_v36',
        'HLT_PFMET130_PFMHT130_IDTight_v36',
        'HLT_PFMET140_PFMHT140_IDTight_v36',
        'HLT_PFMET200_BeamHaloCleaned_v25',
        'HLT_PFMET200_NotCleaned_v25',
        'HLT_PFMET250_NotCleaned_v25',
        'HLT_PFMET300_NotCleaned_v25',
        'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v25',
        'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v36',
        'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v35',
        'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_FilterHF_v16',
        'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v35',
        'HLT_PFMETTypeOne140_PFMHT140_IDTight_v27',
        'HLT_PFMETTypeOne200_BeamHaloCleaned_v25',
        'HLT_Photon100EBHE10_v13',
        'HLT_Photon110EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon110EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon110EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon110EB_TightID_TightIso_v15',
        'HLT_Photon120_R9Id90_HE10_IsoM_v27',
        'HLT_Photon120_v24',
        'HLT_Photon150_v18',
        'HLT_Photon165_R9Id90_HE10_IsoM_v28',
        'HLT_Photon175_v26',
        'HLT_Photon200_v25',
        'HLT_Photon20_HoverELoose_v21',
        'HLT_Photon300_NoHE_v24',
        'HLT_Photon30EB_TightID_TightIso_v15',
        'HLT_Photon30_HoverELoose_v21',
        'HLT_Photon32_OneProng32_M50To105_v14',
        'HLT_Photon33_v16',
        'HLT_Photon34_R9Id90_CaloIdL_IsoL_DisplacedIdL_MediumChargedIsoDisplacedPFTauHPS34_v12',
        'HLT_Photon35_TwoProngs35_v17',
        'HLT_Photon40EB_TightID_TightIso_v6',
        'HLT_Photon40EB_v4',
        'HLT_Photon45EB_TightID_TightIso_v6',
        'HLT_Photon45EB_v4',
        'HLT_Photon50EB_TightID_TightIso_AK8CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_AK8PFJet30_v9',
        'HLT_Photon50EB_TightID_TightIso_CaloJet30_v6',
        'HLT_Photon50EB_TightID_TightIso_PFJet30_v10',
        'HLT_Photon50EB_TightID_TightIso_v11',
        'HLT_Photon50_R9Id90_HE10_IsoM_v27',
        'HLT_Photon50_TimeGt2p5ns_v8',
        'HLT_Photon50_TimeLtNeg2p5ns_v8',
        'HLT_Photon50_v24',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT380_v14',
        'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT400_v14',
        'HLT_Photon60_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v13',
        'HLT_Photon75EB_TightID_TightIso_v11',
        'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v21',
        'HLT_Photon75_R9Id90_HE10_IsoM_v27',
        'HLT_Photon75_v24',
        'HLT_Photon90EB_TightID_TightIso_v11',
        'HLT_Photon90_R9Id90_HE10_IsoM_v27',
        'HLT_Photon90_v24',
        'HLT_Physics_v15',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_Random_v3',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18',
        'HLT_TripleMu_10_5_5_DZ_v26',
        'HLT_TripleMu_12_10_5_v26',
        'HLT_TripleMu_5_3_3_Mass3p8_DCA_v19',
        'HLT_TripleMu_5_3_3_Mass3p8_DZ_v24',
        'HLT_TrkMu12_DoubleTrkMu5NoFiltersNoVtx_v21',
        'HLT_UncorrectedJetE30_NoBPTX3BX_v16',
        'HLT_UncorrectedJetE30_NoBPTX_v16',
        'HLT_UncorrectedJetE60_NoBPTX3BX_v16',
        'HLT_UncorrectedJetE70_NoBPTX3BX_v16',
        'HLT_ZeroBias_Alignment_v9',
        'HLT_ZeroBias_FirstBXAfterTrain_v11',
        'HLT_ZeroBias_FirstCollisionAfterAbortGap_v13',
        'HLT_ZeroBias_FirstCollisionInTrain_v12',
        'HLT_ZeroBias_IsolatedBunches_v13',
        'HLT_ZeroBias_LastCollisionInTrain_v11',
        'HLT_ZeroBias_v14'
     ) ),
    ParkingAnomalyDetection = cms.vstring(
        'HLT_L1AXOVVTight_v1',
        'HLT_L1AXOVVVTight_v1',
        'HLT_L1CICADA_VVTight_v1',
        'HLT_L1CICADA_VVVTight_v1',
        'HLT_L1CICADA_VVVVTight_v1'
    ),
    ParkingDoubleMuonLowMass0 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass1 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass2 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass3 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass4 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass5 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass6 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingDoubleMuonLowMass7 = cms.vstring(
        'HLT_Dimuon0_Jpsi3p5_Muon2_v21',
        'HLT_Dimuon0_Jpsi_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_L1_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_L1_4R_0er1p5R_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_NoOS_v23',
        'HLT_Dimuon0_Jpsi_NoVertexing_v24',
        'HLT_Dimuon0_Jpsi_v24',
        'HLT_Dimuon0_LowMass_Inclusive_v1',
        'HLT_Dimuon0_LowMass_L1_0er1p5_v24',
        'HLT_Dimuon0_LowMass_L1_4_v24',
        'HLT_Dimuon0_LowMass_L1_TM530_v22',
        'HLT_Dimuon0_LowMass_v24',
        'HLT_Dimuon0_Upsilon_L1_4p5_v25',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v23',
        'HLT_Dimuon0_Upsilon_L1_4p5er2p0_v25',
        'HLT_Dimuon0_Upsilon_Muon_NoL1Mass_v22',
        'HLT_Dimuon0_Upsilon_NoVertexing_v23',
        'HLT_Dimuon0_Upsilon_v2',
        'HLT_Dimuon10_Upsilon_y1p4_v17',
        'HLT_Dimuon12_Upsilon_y1p4_v18',
        'HLT_Dimuon14_Phi_Barrel_Seagulls_v23',
        'HLT_Dimuon14_PsiPrime_noCorrL1_v21',
        'HLT_Dimuon14_PsiPrime_v29',
        'HLT_Dimuon18_PsiPrime_noCorrL1_v22',
        'HLT_Dimuon18_PsiPrime_v30',
        'HLT_Dimuon24_Phi_noCorrL1_v22',
        'HLT_Dimuon24_Upsilon_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_noCorrL1_v22',
        'HLT_Dimuon25_Jpsi_v30',
        'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v22',
        'HLT_DoubleMu2_Jpsi_LowPt_v10',
        'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v20',
        'HLT_DoubleMu3_TkMu_DsTau3Mu_v20',
        'HLT_DoubleMu3_Trk_Tau3mu_NoL1Mass_v22',
        'HLT_DoubleMu3_Trk_Tau3mu_v28',
        'HLT_DoubleMu4_3_Bs_v31',
        'HLT_DoubleMu4_3_Displaced_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_3_Jpsi_v31',
        'HLT_DoubleMu4_3_LowMass_SS_v10',
        'HLT_DoubleMu4_3_LowMass_v17',
        'HLT_DoubleMu4_3_Photon4_BsToMMG_v16',
        'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v23',
        'HLT_DoubleMu4_JpsiTrk_Bc_v16',
        'HLT_DoubleMu4_Jpsi_Displaced_v23',
        'HLT_DoubleMu4_Jpsi_NoVertexing_v23',
        'HLT_DoubleMu4_LowMass_Displaced_v17',
        'HLT_DoubleMu4_MuMuTrk_Displaced_v31',
        'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v20',
        'HLT_Mu25_TkMu0_Phi_v24',
        'HLT_Mu30_TkMu0_Psi_v17',
        'HLT_Mu30_TkMu0_Upsilon_v17',
        'HLT_Mu4_L1DoubleMu_v17',
        'HLT_Mu7p5_L2Mu2_Jpsi_v26',
        'HLT_Mu7p5_L2Mu2_Upsilon_v26',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_Charge1_v20',
        'HLT_Tau3Mu_Mu7_Mu1_TkMu1_Tau15_v20',
        'HLT_Trimuon5_3p5_2_Upsilon_Muon_v21',
        'HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v18'
    ),
    ParkingHH0 = cms.vstring(
        'HLT_L1HT200_QuadPFJet20_PNet1BTag0p50_PNet1Tauh0p50_v4',
        'HLT_L1HT200_QuadPFJet25_PNet1BTag0p50_PNet1Tauh0p50_v4',
        'HLT_PFHT250_QuadPFJet25_PNet1BTag0p20_PNet1Tauh0p50_v10',
        'HLT_PFHT250_QuadPFJet25_PNet2BTagMean0p55_v10',
        'HLT_PFHT250_QuadPFJet25_v10',
        'HLT_PFHT250_QuadPFJet30_PNet1BTag0p20_PNet1Tauh0p50_v10',
        'HLT_PFHT250_QuadPFJet30_PNet2BTagMean0p55_v10',
        'HLT_PFHT280_QuadPFJet30_PNet1BTag0p20_PNet1Tauh0p50_v10',
        'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55_v13',
        'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p60_v13',
        'HLT_PFHT280_QuadPFJet30_v13',
        'HLT_PFHT280_QuadPFJet35_PNet2BTagMean0p60_v13',
        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_2p0_v9',
        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3_v9',
        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_v25',
        'HLT_PFHT340_QuadPFJet70_50_40_40_PNet2BTagMean0p70_v14',
        'HLT_PFHT400_FivePFJet_120_120_60_30_30_PNet2BTag_4p3_v10',
        'HLT_PFHT400_FivePFJet_120_120_60_30_30_PNet2BTag_5p6_v10',
        'HLT_PFHT400_FivePFJet_120_120_60_30_30_v10',
        'HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50_v13',
        'HLT_PFHT400_SixPFJet32_v25',
        'HLT_PFHT450_SixPFJet36_PNetBTag0p35_v13',
        'HLT_PFHT450_SixPFJet36_v24'
    ),
    ParkingHH1 = cms.vstring(
        'HLT_L1HT200_QuadPFJet20_PNet1BTag0p50_PNet1Tauh0p50_v4',
        'HLT_L1HT200_QuadPFJet25_PNet1BTag0p50_PNet1Tauh0p50_v4',
        'HLT_PFHT250_QuadPFJet25_PNet1BTag0p20_PNet1Tauh0p50_v10',
        'HLT_PFHT250_QuadPFJet25_PNet2BTagMean0p55_v10',
        'HLT_PFHT250_QuadPFJet25_v10',
        'HLT_PFHT250_QuadPFJet30_PNet1BTag0p20_PNet1Tauh0p50_v10',
        'HLT_PFHT250_QuadPFJet30_PNet2BTagMean0p55_v10',
        'HLT_PFHT280_QuadPFJet30_PNet1BTag0p20_PNet1Tauh0p50_v10',
        'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p55_v13',
        'HLT_PFHT280_QuadPFJet30_PNet2BTagMean0p60_v13',
        'HLT_PFHT280_QuadPFJet30_v13',
        'HLT_PFHT280_QuadPFJet35_PNet2BTagMean0p60_v13',
        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_2p0_v9',
        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_PNet3BTag_4p3_v9',
        'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_v25',
        'HLT_PFHT340_QuadPFJet70_50_40_40_PNet2BTagMean0p70_v14',
        'HLT_PFHT400_FivePFJet_120_120_60_30_30_PNet2BTag_4p3_v10',
        'HLT_PFHT400_FivePFJet_120_120_60_30_30_PNet2BTag_5p6_v10',
        'HLT_PFHT400_FivePFJet_120_120_60_30_30_v10',
        'HLT_PFHT400_SixPFJet32_PNet2BTagMean0p50_v13',
        'HLT_PFHT400_SixPFJet32_v25',
        'HLT_PFHT450_SixPFJet36_PNetBTag0p35_v13',
        'HLT_PFHT450_SixPFJet36_v24'
    ),
    ParkingLLP0 = cms.vstring(
        'HLT_CaloMET60_DTCluster50_v13',
        'HLT_CaloMET60_DTClusterNoMB1S50_v13',
        'HLT_CscCluster150_DisplacedSingleJet30_Inclusive1PtrkShortSig5_v3',
        'HLT_CscCluster150_DisplacedSingleJet35_Inclusive1PtrkShortSig5_v3',
        'HLT_CscCluster150_DisplacedSingleJet40_Inclusive1PtrkShortSig5_v3',
        'HLT_HT170_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay0p5nsTrackless_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay1nsInclusive_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay1nsTrackless_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay2nsInclusive_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet60_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_PFJet60_NeutralHadronFrac0p7_v10',
        'HLT_HT200_L1SingleLLPJet_PFJet60_NeutralHadronFrac0p8_v10',
        'HLT_HT240_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v11',
        'HLT_HT270_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT280_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v11',
        'HLT_HT320_L1SingleLLPJet_DisplacedDijet60_Inclusive_v14',
        'HLT_HT350_DelayedJet40_SingleDelay1p5To3p5nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay1p6To3p5nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay1p75To3p5nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3p25nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3p5nsInclusive_v9',
        'HLT_HT360_DisplacedDijet40_Inclusive1PtrkShortSig5_v10',
        'HLT_HT360_DisplacedDijet45_Inclusive1PtrkShortSig5_v10',
        'HLT_HT390_DisplacedDijet40_Inclusive1PtrkShortSig5_v10',
        'HLT_HT390_DisplacedDijet45_Inclusive1PtrkShortSig5_v10',
        'HLT_HT390eta2p0_DisplacedDijet40_Inclusive1PtrkShortSig5_v10',
        'HLT_HT400_DisplacedDijet40_DisplacedTrack_v26',
        'HLT_HT420_L1SingleLLPJet_DisplacedDijet60_Inclusive_v14',
        'HLT_HT430_DelayedJet40_DoubleDelay0p5nsInclusive_v12',
        'HLT_HT430_DelayedJet40_DoubleDelay0p5nsTrackless_v14',
        'HLT_HT430_DelayedJet40_DoubleDelay0p75nsTrackless_v10',
        'HLT_HT430_DelayedJet40_DoubleDelay1nsInclusive_v13',
        'HLT_HT430_DelayedJet40_DoubleDelay1nsTrackless_v10',
        'HLT_HT430_DelayedJet40_DoubleDelay1p25nsInclusive_v9',
        'HLT_HT430_DelayedJet40_DoubleDelay1p5nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay0p5nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay0p5nsTrackless_v12',
        'HLT_HT430_DelayedJet40_SingleDelay1To1p5nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay1nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay1nsTrackless_v14',
        'HLT_HT430_DelayedJet40_SingleDelay1p1To1p6nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay1p25To1p75nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay1p25nsTrackless_v10',
        'HLT_HT430_DelayedJet40_SingleDelay1p5nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay1p5nsTrackless_v10',
        'HLT_HT430_DelayedJet40_SingleDelay2nsInclusive_v13',
        'HLT_HT430_DelayedJet40_SingleDelay2p25nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay2p5nsInclusive_v9',
        'HLT_HT430_DisplacedDijet40_DisplacedTrack_v26',
        'HLT_HT430_DisplacedDijet40_Inclusive1PtrkShortSig5_v14',
        'HLT_HT550_DisplacedDijet60_Inclusive_v26',
        'HLT_HT650_DisplacedDijet60_Inclusive_v26',
        'HLT_L1MET_DTCluster50_v13',
        'HLT_L1MET_DTClusterNoMB1S50_v13',
        'HLT_L1SingleLLPJet_v8',
        'HLT_L1SingleMuShower_v1',
        'HLT_L1Tau_DelayedJet40_DoubleDelay0p5nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_DoubleDelay0p75nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p25nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p25nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p5nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p5nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p75nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p5To4nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p5nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p6To4nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p75To4nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p75nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_SingleDelay3nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_SingleDelay3p5nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_SingleDelay3p75nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay4nsInclusive_v9',
        'HLT_Mu6HT240_DisplacedDijet30_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet35_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet35_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet40_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet40_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet45_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet50_Inclusive0PtrkShortSig5_v14',
        'HLT_PFJet200_TimeGt2p5ns_v14',
        'HLT_PFJet200_TimeLtNeg2p5ns_v14'
    ),
    ParkingLLP1 = cms.vstring(
        'HLT_CaloMET60_DTCluster50_v13',
        'HLT_CaloMET60_DTClusterNoMB1S50_v13',
        'HLT_CscCluster150_DisplacedSingleJet30_Inclusive1PtrkShortSig5_v3',
        'HLT_CscCluster150_DisplacedSingleJet35_Inclusive1PtrkShortSig5_v3',
        'HLT_CscCluster150_DisplacedSingleJet40_Inclusive1PtrkShortSig5_v3',
        'HLT_HT170_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay0p5nsTrackless_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay1nsInclusive_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay1nsTrackless_v14',
        'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay2nsInclusive_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v14',
        'HLT_HT200_L1SingleLLPJet_DisplacedDijet60_DisplacedTrack_v14',
        'HLT_HT200_L1SingleLLPJet_PFJet60_NeutralHadronFrac0p7_v10',
        'HLT_HT200_L1SingleLLPJet_PFJet60_NeutralHadronFrac0p8_v10',
        'HLT_HT240_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v11',
        'HLT_HT270_L1SingleLLPJet_DisplacedDijet40_DisplacedTrack_v14',
        'HLT_HT280_L1SingleLLPJet_DisplacedDijet40_Inclusive1PtrkShortSig5_v11',
        'HLT_HT320_L1SingleLLPJet_DisplacedDijet60_Inclusive_v14',
        'HLT_HT350_DelayedJet40_SingleDelay1p5To3p5nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay1p6To3p5nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay1p75To3p5nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3p25nsInclusive_v9',
        'HLT_HT350_DelayedJet40_SingleDelay3p5nsInclusive_v9',
        'HLT_HT360_DisplacedDijet40_Inclusive1PtrkShortSig5_v10',
        'HLT_HT360_DisplacedDijet45_Inclusive1PtrkShortSig5_v10',
        'HLT_HT390_DisplacedDijet40_Inclusive1PtrkShortSig5_v10',
        'HLT_HT390_DisplacedDijet45_Inclusive1PtrkShortSig5_v10',
        'HLT_HT390eta2p0_DisplacedDijet40_Inclusive1PtrkShortSig5_v10',
        'HLT_HT400_DisplacedDijet40_DisplacedTrack_v26',
        'HLT_HT420_L1SingleLLPJet_DisplacedDijet60_Inclusive_v14',
        'HLT_HT430_DelayedJet40_DoubleDelay0p5nsInclusive_v12',
        'HLT_HT430_DelayedJet40_DoubleDelay0p5nsTrackless_v14',
        'HLT_HT430_DelayedJet40_DoubleDelay0p75nsTrackless_v10',
        'HLT_HT430_DelayedJet40_DoubleDelay1nsInclusive_v13',
        'HLT_HT430_DelayedJet40_DoubleDelay1nsTrackless_v10',
        'HLT_HT430_DelayedJet40_DoubleDelay1p25nsInclusive_v9',
        'HLT_HT430_DelayedJet40_DoubleDelay1p5nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay0p5nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay0p5nsTrackless_v12',
        'HLT_HT430_DelayedJet40_SingleDelay1To1p5nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay1nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay1nsTrackless_v14',
        'HLT_HT430_DelayedJet40_SingleDelay1p1To1p6nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay1p25To1p75nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay1p25nsTrackless_v10',
        'HLT_HT430_DelayedJet40_SingleDelay1p5nsInclusive_v11',
        'HLT_HT430_DelayedJet40_SingleDelay1p5nsTrackless_v10',
        'HLT_HT430_DelayedJet40_SingleDelay2nsInclusive_v13',
        'HLT_HT430_DelayedJet40_SingleDelay2p25nsInclusive_v9',
        'HLT_HT430_DelayedJet40_SingleDelay2p5nsInclusive_v9',
        'HLT_HT430_DisplacedDijet40_DisplacedTrack_v26',
        'HLT_HT430_DisplacedDijet40_Inclusive1PtrkShortSig5_v14',
        'HLT_HT550_DisplacedDijet60_Inclusive_v26',
        'HLT_HT650_DisplacedDijet60_Inclusive_v26',
        'HLT_L1MET_DTCluster50_v13',
        'HLT_L1MET_DTClusterNoMB1S50_v13',
        'HLT_L1SingleLLPJet_v8',
        'HLT_L1SingleMuShower_v1',
        'HLT_L1Tau_DelayedJet40_DoubleDelay0p5nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_DoubleDelay0p75nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p25nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p25nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p5nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p5nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_DoubleDelay1p75nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p5To4nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p5nsTrackless_v12',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p6To4nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p75To4nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay2p75nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_SingleDelay3nsTrackless_v10',
        'HLT_L1Tau_DelayedJet40_SingleDelay3p5nsInclusive_v11',
        'HLT_L1Tau_DelayedJet40_SingleDelay3p75nsInclusive_v9',
        'HLT_L1Tau_DelayedJet40_SingleDelay4nsInclusive_v9',
        'HLT_Mu6HT240_DisplacedDijet30_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet35_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet35_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet40_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet40_Inclusive1PtrkShortSig5_DisplacedLoose_v14',
        'HLT_Mu6HT240_DisplacedDijet45_Inclusive0PtrkShortSig5_v14',
        'HLT_Mu6HT240_DisplacedDijet50_Inclusive0PtrkShortSig5_v14',
        'HLT_PFJet200_TimeGt2p5ns_v14',
        'HLT_PFJet200_TimeLtNeg2p5ns_v14'
    ),
    ParkingSingleMuon0 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon1 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon10 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon11 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon12 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon13 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon14 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon15 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon2 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon3 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon4 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon5 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon6 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon7 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon8 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingSingleMuon9 = cms.vstring(
        'HLT_Mu0_Barrel_L1HP10_v10',
        'HLT_Mu0_Barrel_L1HP11_v10',
        'HLT_Mu0_Barrel_L1HP13_v4',
        'HLT_Mu0_Barrel_L1HP6_IP6_v7',
        'HLT_Mu0_Barrel_L1HP6_v7',
        'HLT_Mu0_Barrel_L1HP7_v7',
        'HLT_Mu0_Barrel_L1HP8_v8',
        'HLT_Mu0_Barrel_L1HP9_v8',
        'HLT_Mu0_Barrel_v10',
        'HLT_Mu10_Barrel_L1HP11_IP4_v4',
        'HLT_Mu10_Barrel_L1HP11_IP6_v10',
        'HLT_Mu12_Barrel_L1HP13_IP4_v4',
        'HLT_Mu12_Barrel_L1HP13_IP6_v4',
        'HLT_Mu4_Barrel_IP4_v4',
        'HLT_Mu4_Barrel_IP6_v4',
        'HLT_Mu6_Barrel_L1HP7_IP6_v7',
        'HLT_Mu7_Barrel_L1HP8_IP6_v8',
        'HLT_Mu8_Barrel_L1HP9_IP6_v8',
        'HLT_Mu9_Barrel_L1HP10_IP6_v10'
    ),
    ParkingVBF0 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF1 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF2 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF3 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF4 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF5 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF6 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    ParkingVBF7 = cms.vstring(
        'HLT_QuadPFJet100_88_70_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet100_88_70_30_v14',
        'HLT_QuadPFJet103_88_75_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet103_88_75_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet103_88_75_15_v21',
        'HLT_QuadPFJet105_88_75_30_PNet1CvsAll0p5_VBF3Tight_v14',
        'HLT_QuadPFJet105_88_75_30_v13',
        'HLT_QuadPFJet105_88_76_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet105_88_76_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet105_88_76_15_v21',
        'HLT_QuadPFJet111_90_80_15_PNet2BTag_0p4_0p12_VBF1_v10',
        'HLT_QuadPFJet111_90_80_15_PNetBTag_0p4_VBF2_v10',
        'HLT_QuadPFJet111_90_80_15_v21',
        'HLT_QuadPFJet111_90_80_30_PNet1CvsAll0p6_VBF3Tight_v14',
        'HLT_QuadPFJet111_90_80_30_v13',
        'HLT_VBF_DiPFJet115_40_Mjj1000_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1100_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj1200_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet115_40_Mjj850_DoublePNetTauhPFJet20_eta2p3_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1050_v12',
        'HLT_VBF_DiPFJet125_45_Mjj1150_v4',
        'HLT_VBF_DiPFJet125_45_Mjj1250_v4',
        'HLT_VBF_DiPFJet45_Mjj650_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj750_PNetTauhPFJet45_L2NN_eta2p3_v10',
        'HLT_VBF_DiPFJet45_Mjj850_PNetTauhPFJet45_L2NN_eta2p3_v4',
        'HLT_VBF_DiPFJet50_Mjj600_Ele22_eta2p1_WPTight_Gsf_v11',
        'HLT_VBF_DiPFJet50_Mjj650_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj700_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj750_Photon22_v10',
        'HLT_VBF_DiPFJet50_Mjj800_Ele22_eta2p1_WPTight_Gsf_v5',
        'HLT_VBF_DiPFJet50_Mjj850_Photon22_v4',
        'HLT_VBF_DiPFJet75_45_Mjj1000_DiPFJet60_v4',
        'HLT_VBF_DiPFJet75_45_Mjj800_DiPFJet60_v10',
        'HLT_VBF_DiPFJet75_45_Mjj900_DiPFJet60_v4',
        'HLT_VBF_DiPFJet80_45_Mjj650_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj750_PFMETNoMu85_v10',
        'HLT_VBF_DiPFJet80_45_Mjj850_PFMETNoMu85_v4',
        'HLT_VBF_DiPFJet95_45_Mjj750_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj850_Mu3_TrkIsoVVL_v10',
        'HLT_VBF_DiPFJet95_45_Mjj950_Mu3_TrkIsoVVL_v4'
    ),
    RPCMonitor = cms.vstring('AlCa_RPCMuonNormalisation_v25'),
    ScoutingPF0 = cms.vstring(
        'DST_PFScouting_AXOLoose_v8',
        'DST_PFScouting_AXOMedium_v4',
        'DST_PFScouting_AXOTight_v10',
        'DST_PFScouting_AXOVLoose_v8',
        'DST_PFScouting_AXOVTight_v8',
        'DST_PFScouting_CICADALoose_v6',
        'DST_PFScouting_CICADAMedium_v6',
        'DST_PFScouting_CICADATight_v6',
        'DST_PFScouting_CICADAVLoose_v6',
        'DST_PFScouting_CICADAVTight_v6',
        'DST_PFScouting_DoubleEGMonitorJPsi_v1',
        'DST_PFScouting_DoubleEGMonitorZ_v1',
        'DST_PFScouting_DoubleEG_v10',
        'DST_PFScouting_DoubleMuonNoVtx_v4',
        'DST_PFScouting_DoubleMuonVtxMonitorJPsi_v4',
        'DST_PFScouting_DoubleMuonVtxMonitorZ_v4',
        'DST_PFScouting_DoubleMuonVtx_v4',
        'DST_PFScouting_JetHT_v10',
        'DST_PFScouting_SingleMuon_v10',
        'DST_PFScouting_SinglePhotonEBMonitorJPsi_v1',
        'DST_PFScouting_SinglePhotonEBMonitorZ_v1',
        'DST_PFScouting_SinglePhotonEB_v7',
        'DST_PFScouting_ZeroBias_v8'
    ),
    ScoutingPF1 = cms.vstring(
        'DST_PFScouting_AXOLoose_v8',
        'DST_PFScouting_AXOMedium_v4',
        'DST_PFScouting_AXOTight_v10',
        'DST_PFScouting_AXOVLoose_v8',
        'DST_PFScouting_AXOVTight_v8',
        'DST_PFScouting_CICADALoose_v6',
        'DST_PFScouting_CICADAMedium_v6',
        'DST_PFScouting_CICADATight_v6',
        'DST_PFScouting_CICADAVLoose_v6',
        'DST_PFScouting_CICADAVTight_v6',
        'DST_PFScouting_DoubleEGMonitorJPsi_v1',
        'DST_PFScouting_DoubleEGMonitorZ_v1',
        'DST_PFScouting_DoubleEG_v10',
        'DST_PFScouting_DoubleMuonNoVtx_v4',
        'DST_PFScouting_DoubleMuonVtxMonitorJPsi_v4',
        'DST_PFScouting_DoubleMuonVtxMonitorZ_v4',
        'DST_PFScouting_DoubleMuonVtx_v4',
        'DST_PFScouting_JetHT_v10',
        'DST_PFScouting_SingleMuon_v10',
        'DST_PFScouting_SinglePhotonEBMonitorJPsi_v1',
        'DST_PFScouting_SinglePhotonEBMonitorZ_v1',
        'DST_PFScouting_SinglePhotonEB_v7',
        'DST_PFScouting_ZeroBias_v8'
    ),
    ScoutingPFMonitor = cms.vstring(
        'DST_PFScouting_DoubleEGMonitorJPsi_v1',
        'DST_PFScouting_DoubleEGMonitorZ_v1',
        'DST_PFScouting_DoubleMuonVtxMonitorJPsi_v4',
        'DST_PFScouting_DoubleMuonVtxMonitorZ_v4',
        'DST_PFScouting_SinglePhotonEBMonitorJPsi_v1',
        'DST_PFScouting_SinglePhotonEBMonitorZ_v1',
        'HLT_TriggersForScoutingPFMonitor_PS1000_v1',
        'HLT_TriggersForScoutingPFMonitor_PS125_v1',
        'HLT_TriggersForScoutingPFMonitor_PS250_v1',
        'HLT_TriggersForScoutingPFMonitor_PS500_v1'
    ),
    Tau = cms.vstring(
        'HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_noDxy_v12',
        'HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1_v17',
        'HLT_DoubleMediumChargedIsoDisplacedPFTauHPS36_Trk1_eta2p1_v12',
        'HLT_DoublePNetTauhPFJet26_L2NN_eta2p3_PFJet60_v10',
        'HLT_DoublePNetTauhPFJet26_L2NN_eta2p3_PFJet75_v10',
        'HLT_DoublePNetTauhPFJet30_Medium_L2NN_eta2p3_v10',
        'HLT_DoublePNetTauhPFJet30_Tight_L2NN_eta2p3_v10',
        'HLT_SinglePNetTauhPFJet130_Loose_L2NN_eta2p3_v10',
        'HLT_SinglePNetTauhPFJet130_Medium_L2NN_eta2p3_v10',
        'HLT_SinglePNetTauhPFJet130_Tight_L2NN_eta2p3_v10'
    ),
    TestDataRaw = cms.vstring('HLT_TestData_v1'),
    TestDataScouting = cms.vstring('HLT_TestData_v1'),
    TestEnablesEcalHcal = cms.vstring(
        'HLT_EcalCalibration_v4',
        'HLT_HcalCalibration_v6'
    ),
    TestEnablesEcalHcalDQM = cms.vstring(
        'HLT_EcalCalibration_v4',
        'HLT_HcalCalibration_v6'
    ),
    ZeroBias = cms.vstring(
        'HLT_Random_v3',
        'HLT_ZeroBias_Alignment_v9',
        'HLT_ZeroBias_FirstBXAfterTrain_v11',
        'HLT_ZeroBias_FirstCollisionAfterAbortGap_v13',
        'HLT_ZeroBias_FirstCollisionInTrain_v12',
        'HLT_ZeroBias_IsolatedBunches_v13',
        'HLT_ZeroBias_LastCollisionInTrain_v11',
        'HLT_ZeroBias_v14'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.maxLuminosityBlocks = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.nanoDQMIO_perLSoutput = cms.PSet(
    MEsToSave = cms.untracked.vstring( (
        'Hcal/DigiTask/Occupancy/depth/depth1',
        'Hcal/DigiTask/Occupancy/depth/depth2',
        'Hcal/DigiTask/Occupancy/depth/depth3',
        'Hcal/DigiTask/Occupancy/depth/depth4',
        'Hcal/DigiTask/Occupancy/depth/depth5',
        'Hcal/DigiTask/Occupancy/depth/depth6',
        'Hcal/DigiTask/Occupancy/depth/depth7',
        'Hcal/DigiTask/Occupancy/depth/depthHO',
        'Hcal/DigiTask/OccupancyCut/depth/depth1',
        'Hcal/DigiTask/OccupancyCut/depth/depth2',
        'Hcal/DigiTask/OccupancyCut/depth/depth3',
        'Hcal/DigiTask/OccupancyCut/depth/depth4',
        'Hcal/DigiTask/OccupancyCut/depth/depth5',
        'Hcal/DigiTask/OccupancyCut/depth/depth6',
        'Hcal/DigiTask/OccupancyCut/depth/depth7',
        'Hcal/DigiTask/OccupancyCut/depth/depthHO',
        'EcalBarrel/EBOccupancyTask/EBOT digi occupancy',
        'EcalEndcap/EEOccupancyTask/EEOT digi occupancy EE -',
        'EcalEndcap/EEOccupancyTask/EEOT digi occupancy EE +',
        'EcalBarrel/EBOccupancyTask/EBOT DCC entries',
        'EcalEndcap/EEOccupancyTask/EEOT DCC entries',
        'Ecal/EventInfo/processedEvents',
        'PixelPhase1/Tracks/charge_PXBarrel',
        'PixelPhase1/Tracks/charge_PXForward',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_1',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_2',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_3',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_4',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_+1',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_+2',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_+3',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_-1',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_-2',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_-3',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_1',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_2',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_3',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_4',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_+1',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_+2',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_+3',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_-1',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_-2',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_-3',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm1',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm2',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm3',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm4',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp1',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp2',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp3',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp4',
        'GEM/RecHits/occ_xy_GE11-M-L1',
        'GEM/RecHits/occ_xy_GE11-M-L2',
        'GEM/RecHits/occ_xy_GE11-P-L1',
        'GEM/RecHits/occ_xy_GE11-P-L2',
        'GEM/Digis/occ_GE11-M-L1',
        'GEM/Digis/occ_GE11-M-L2',
        'GEM/Digis/occ_GE11-P-L1',
        'GEM/Digis/occ_GE11-P-L2',
        'HLT/Vertexing/hltPixelVertices/hltPixelVertices/goodvtxNbr',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_pt',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_pt',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_pt',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_pt',
        'HLT/Tracking/pixelTracks/GeneralProperties/Chi2Prob_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/Chi2oNDFVsEta_ImpactPoint_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/DeltaZToPVZoom_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/DistanceOfClosestApproachToPVVsPhi_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/DistanceOfClosestApproachToPVZoom_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/NumberOfTracks_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/Chi2Prob_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/Chi2oNDFVsEta_ImpactPoint_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/DeltaZToPVZoom_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/DistanceOfClosestApproachToPVVsPhi_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/DistanceOfClosestApproachToPVZoom_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/NumberOfTracks_GenTk',
        'HLT/Tracking/tracks/LUMIanalysis/NumberEventsVsLUMI',
        'HLT/Tracking/tracks/PUmonitoring/NumberEventsVsGoodPVtx',
        'PixelPhase1/Tracks/num_clusters_ontrack_PXBarrel',
        'PixelPhase1/Tracks/num_clusters_ontrack_PXForward',
        'PixelPhase1/Tracks/clusterposition_zphi_ontrack',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_1',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_2',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_3',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_4',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_+1',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_+2',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_+3',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_-1',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_-2',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_-3',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_1',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_2',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_3',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_4',
        'PixelPhase1/Phase1_MechanicalView/PXForward/digi_occupancy_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_1',
        'PixelPhase1/Phase1_MechanicalView/PXForward/digi_occupancy_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_2',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_1',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_2',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_3',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_4',
        'PixelPhase1/Phase1_MechanicalView/PXForward/clusters_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_1',
        'PixelPhase1/Phase1_MechanicalView/PXForward/clusters_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_2',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/NormalizedHitResiduals_TEC__wheel__1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_2/NormalizedHitResiduals_TEC__wheel__2',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_3/NormalizedHitResiduals_TEC__wheel__3',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_4/NormalizedHitResiduals_TEC__wheel__4',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_5/NormalizedHitResiduals_TEC__wheel__5',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_6/NormalizedHitResiduals_TEC__wheel__6',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_7/NormalizedHitResiduals_TEC__wheel__7',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_8/NormalizedHitResiduals_TEC__wheel__8',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_9/NormalizedHitResiduals_TEC__wheel__9',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_1/NormalizedHitResiduals_TEC__wheel__1',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_2/NormalizedHitResiduals_TEC__wheel__2',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_3/NormalizedHitResiduals_TEC__wheel__3',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_4/NormalizedHitResiduals_TEC__wheel__4',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_5/NormalizedHitResiduals_TEC__wheel__5',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_6/NormalizedHitResiduals_TEC__wheel__6',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_7/NormalizedHitResiduals_TEC__wheel__7',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_8/NormalizedHitResiduals_TEC__wheel__8',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_9/NormalizedHitResiduals_TEC__wheel__9',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__2',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__3',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_4/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__4',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_5/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__5',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_6/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__6',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_7/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__7',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_8/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__8',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_9/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__9',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__1',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__2',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__3',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_4/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__4',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_5/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__5',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_6/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__6',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_7/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__7',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_8/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__8',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_9/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__9',
        'SiStrip/MechanicalView/TIB/layer_1/NormalizedHitResiduals_TIB__Layer__1',
        'SiStrip/MechanicalView/TIB/layer_2/NormalizedHitResiduals_TIB__Layer__2',
        'SiStrip/MechanicalView/TIB/layer_3/NormalizedHitResiduals_TIB__Layer__3',
        'SiStrip/MechanicalView/TIB/layer_4/NormalizedHitResiduals_TIB__Layer__4',
        'SiStrip/MechanicalView/TIB/layer_1/Summary_ClusterStoNCorr__OnTrack__TIB__layer__1',
        'SiStrip/MechanicalView/TIB/layer_2/Summary_ClusterStoNCorr__OnTrack__TIB__layer__2',
        'SiStrip/MechanicalView/TIB/layer_3/Summary_ClusterStoNCorr__OnTrack__TIB__layer__3',
        'SiStrip/MechanicalView/TIB/layer_4/Summary_ClusterStoNCorr__OnTrack__TIB__layer__4',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/NormalizedHitResiduals_TID__wheel__1',
        'SiStrip/MechanicalView/TID/PLUS/wheel_2/NormalizedHitResiduals_TID__wheel__2',
        'SiStrip/MechanicalView/TID/PLUS/wheel_3/NormalizedHitResiduals_TID__wheel__3',
        'SiStrip/MechanicalView/TID/MINUS/wheel_1/NormalizedHitResiduals_TID__wheel__1',
        'SiStrip/MechanicalView/TID/MINUS/wheel_2/NormalizedHitResiduals_TID__wheel__2',
        'SiStrip/MechanicalView/TID/MINUS/wheel_3/NormalizedHitResiduals_TID__wheel__3',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TID__PLUS__wheel__1',
        'SiStrip/MechanicalView/TID/PLUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TID__PLUS__wheel__2',
        'SiStrip/MechanicalView/TID/PLUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TID__PLUS__wheel__3',
        'SiStrip/MechanicalView/TID/MINUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TID__MINUS__wheel__1',
        'SiStrip/MechanicalView/TID/MINUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TID__MINUS__wheel__2',
        'SiStrip/MechanicalView/TID/MINUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TID__MINUS__wheel__3',
        'SiStrip/MechanicalView/TOB/layer_1/NormalizedHitResiduals_TOB__Layer__1',
        'SiStrip/MechanicalView/TOB/layer_2/NormalizedHitResiduals_TOB__Layer__2',
        'SiStrip/MechanicalView/TOB/layer_3/NormalizedHitResiduals_TOB__Layer__3',
        'SiStrip/MechanicalView/TOB/layer_4/NormalizedHitResiduals_TOB__Layer__4',
        'SiStrip/MechanicalView/TOB/layer_5/NormalizedHitResiduals_TOB__Layer__5',
        'SiStrip/MechanicalView/TOB/layer_6/NormalizedHitResiduals_TOB__Layer__6',
        'SiStrip/MechanicalView/TOB/layer_1/Summary_ClusterStoNCorr__OnTrack__TOB__layer__1',
        'SiStrip/MechanicalView/TOB/layer_2/Summary_ClusterStoNCorr__OnTrack__TOB__layer__2',
        'SiStrip/MechanicalView/TOB/layer_3/Summary_ClusterStoNCorr__OnTrack__TOB__layer__3',
        'SiStrip/MechanicalView/TOB/layer_4/Summary_ClusterStoNCorr__OnTrack__TOB__layer__4',
        'SiStrip/MechanicalView/TOB/layer_5/Summary_ClusterStoNCorr__OnTrack__TOB__layer__5',
        'SiStrip/MechanicalView/TOB/layer_6/Summary_ClusterStoNCorr__OnTrack__TOB__layer__6',
        'SiStrip/MechanicalView/MainDiagonal Position',
        'SiStrip/MechanicalView/NumberOfClustersInPixel',
        'SiStrip/MechanicalView/NumberOfClustersInStrip',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/TkHMap_NumberOfDigi_TIDP_D1',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/TkHMap_NumberOfCluster_TIDP_D1',
        'SiStrip/MechanicalView/TIB/layer_1/TkHMap_NumberOfDigi_TIB_L1',
        'SiStrip/MechanicalView/TIB/layer_1/TkHMap_NumberOfCluster_TIB_L1',
        'SiStrip/MechanicalView/TOB/layer_1/TkHMap_NumberOfDigi_TOB_L1',
        'SiStrip/MechanicalView/TOB/layer_1/TkHMap_NumberOfCluster_TOB_L1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/TkHMap_NumberOfDigi_TECP_W1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/TkHMap_NumberOfCluster_TECP_W1',
        'Tracking/TrackParameters/generalTracks/LSanalysis/Chi2oNDF_lumiFlag_GenTk',
        'Tracking/TrackParameters/generalTracks/LSanalysis/NumberOfRecHitsPerTrack_lumiFlag_GenTk',
        'Tracking/TrackParameters/generalTracks/LSanalysis/NumberOfTracks_lumiFlag_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/SIPDxyToPV_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/SIPDzToPV_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/SIP3DToPV_GenTk',
        'Tracking/TrackParameters/generalTracks/HitProperties/NumberOfMissingOuterRecHitsPerTrack_GenTk',
        'Tracking/TrackParameters/generalTracks/HitProperties/NumberMORecHitsPerTrackVsPt_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/NumberOfTracks_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPt_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/Chi2oNDF_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPhi_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEta_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_Strip_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_Pixel_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBS_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBSdz_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBSVsPhi_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBSVsEta_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackQoverP_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/Quality_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/NumberofTracks_Hardvtx_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/NumberofTracks_PUvtx_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackPtHighpurity_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackPtTight_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackPtLoose_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaHighpurity_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaTight_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaLoose_ImpactPoint_GenTk',
        'Tracking/PrimaryVertices/highPurityTracks/pt_0to1/offline/NumberOfGoodPVtx_offline',
        'Tracking/PrimaryVertices/highPurityTracks/pt_0to1/offline/GoodPVtxNumberOfTracks_offline',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/NumberofTracks_Hardvtx_PUvtx_GenTk',
        'Tracking/PrimaryVertices/highPurityTracks/pt_0to1/offline/FractionOfGoodPVtx_offline',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_Ratio_byFoldingmap_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_Ratio_byFoldingmap_op_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_RelativeDifference_byFoldingmap_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_RelativeDifference_byFoldingmap_op_ImpactPoint_GenTk',
        'OfflinePV/offlinePrimaryVertices/tagVtxProb',
        'OfflinePV/offlinePrimaryVertices/tagType',
        'OfflinePV/Resolution/PV/pull_x',
        'OfflinePV/Resolution/PV/pull_y',
        'OfflinePV/Resolution/PV/pull_z',
        'OfflinePV/offlinePrimaryVertices/tagDiffX',
        'OfflinePV/offlinePrimaryVertices/tagDiffY',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_highPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_highPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_mediumPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_mediumPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_lowPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_lowPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Constituents',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Eta',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Eta_uncor',
        'JetMET/Jet/Cleanedak4PFJetsCHS/JetEnergyCorr',
        'JetMET/Jet/Cleanedak4PFJetsCHS/NJets',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Phi',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Phi_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Phi_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Pt',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/PtJetMET/Jet/Cleanedak4PFJetsPuppi/Phi',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Phi_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Phi_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/JetEnergyCorr',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/NJets',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Eta',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Eta_uncor',
        'JetMET/MET/pfMETT1/Cleaned/METSig',
        'JetMET/vertices',
        'JetMET/HIJetValidation/akCs4PFJets/SumPFPt',
        'JetMET/HIJetValidation/akCs4PFJets/NJets',
        'JetMET/HIJetValidation/akCs4PFJets/NPFpart',
        'JetMET/HIJetValidation/akPu4CaloJets/SumCaloPt',
        'JetMET/HIJetValidation/akPu4CaloJets/NCalopart',
        'JetMET/HIJetValidation/akPu4CaloJets/NJets',
        'Muons/MuonRecoAnalyzer/GlbMuon_Glb_pt',
        'Muons/MuonRecoAnalyzer/GlbMuon_Glb_eta',
        'Muons/MuonRecoAnalyzer/GlbMuon_Glb_phi',
        'Muons/MuonRecoAnalyzer/Res_TkGlb_qOverlap',
        'Muons/diMuonHistograms/GlbGlbMuon_LM',
        'Muons/diMuonHistograms/GlbGlbMuon_HM',
        'Muons/Isolation/global/relPFIso_R03',
        'Muons/globalMuons/GeneralProperties/NumberOfMeanRecHitsPerTrack_glb',
        'Muons/standAloneMuonsUpdatedAtVtx/HitProperties/NumberOfValidRecHitsPerTrack_sta',
        'Muons/MuonRecoOneHLT/GlbMuon_Glb_pt',
        'Muons/MuonRecoOneHLT/GlbMuon_Glb_eta',
        'Egamma/Electrons/Ele5_TagAndProbe/ele0_vertexPt_barrel',
        'Egamma/Electrons/Ele5_TagAndProbe/ele1_vertexPt_endcaps',
        'Egamma/Electrons/Ele5_TagAndProbe/ele2_vertexEta',
        'Egamma/Electrons/Ele5_TagAndProbe/ele5_vertexZ',
        'Egamma/Electrons/Ele5_TagAndProbe/ele10_Eop_barrel',
        'Egamma/Electrons/Ele5_TagAndProbe/ele10_Eop_endcaps',
        'Egamma/Electrons/Ele5_TagAndProbe/ele101_etaEff',
        'Egamma/Electrons/Ele5_TagAndProbe/ele102_phiEff',
        'Egamma/Electrons/Ele5_TagAndProbe/ele201_mee_os'
     ) )
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    TryToContinue = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    holdsReferencesToDeleteEarly = cms.untracked.VPSet(),
    makeTriggerResults = cms.obsolete.untracked.bool,
    modulesToCallForTryToContinue = cms.untracked.vstring(),
    modulesToIgnoreForDeleteEarly = cms.untracked.vstring(),
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(4),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(True)
)

process.streams = cms.PSet(
    ALCAHcalIsoTrk = cms.vstring('AlCaHcalIsoTrk'),
    ALCALowPtJet = cms.vstring('AlCaLowPtJet'),
    ALCALumiPixelsCountsExpress = cms.vstring('AlCaLumiPixelsCountsExpress'),
    ALCALumiPixelsCountsPrompt = cms.vstring('AlCaLumiPixelsCountsPrompt'),
    ALCAP0 = cms.vstring('AlCaP0'),
    ALCAPHISYM = cms.vstring('AlCaPhiSym'),
    ALCAPPSExpress = cms.vstring('AlCaPPSExpress'),
    ALCAPPSPrompt = cms.vstring('AlCaPPSPrompt'),
    Calibration = cms.vstring('TestEnablesEcalHcal'),
    DQM = cms.vstring('OnlineMonitor'),
    DQMCalibration = cms.vstring('TestEnablesEcalHcalDQM'),
    DQMEventDisplay = cms.vstring('EventDisplay'),
    DQMGPUvsCPU = cms.vstring('DQMGPUvsCPU'),
    DQMOnlineBeamspot = cms.vstring('DQMOnlineBeamspot'),
    DQMOnlineScouting = cms.vstring('DQMOnlineScouting'),
    DQMPPSRandom = cms.vstring('DQMPPSRandom'),
    EcalCalibration = cms.vstring('EcalLaser'),
    Express = cms.vstring('ExpressPhysics'),
    ExpressAlignment = cms.vstring('ExpressAlignment'),
    HLTMonitor = cms.vstring('HLTMonitor'),
    LocalTestDataRaw = cms.vstring('TestDataRaw'),
    LocalTestDataScouting = cms.vstring('TestDataScouting'),
    NanoDST = cms.vstring('L1Accept'),
    ParkingAnomalyDetection = cms.vstring('ParkingAnomalyDetection'),
    ParkingDoubleMuonLowMass0 = cms.vstring(
        'ParkingDoubleMuonLowMass0',
        'ParkingDoubleMuonLowMass1'
    ),
    ParkingDoubleMuonLowMass1 = cms.vstring(
        'ParkingDoubleMuonLowMass2',
        'ParkingDoubleMuonLowMass3'
    ),
    ParkingDoubleMuonLowMass2 = cms.vstring(
        'ParkingDoubleMuonLowMass4',
        'ParkingDoubleMuonLowMass5'
    ),
    ParkingDoubleMuonLowMass3 = cms.vstring(
        'ParkingDoubleMuonLowMass6',
        'ParkingDoubleMuonLowMass7'
    ),
    ParkingHH = cms.vstring(
        'ParkingHH0',
        'ParkingHH1'
    ),
    ParkingLLP = cms.vstring(
        'ParkingLLP0',
        'ParkingLLP1'
    ),
    ParkingSingleMuon0 = cms.vstring('ParkingSingleMuon0'),
    ParkingSingleMuon1 = cms.vstring('ParkingSingleMuon1'),
    ParkingSingleMuon10 = cms.vstring('ParkingSingleMuon10'),
    ParkingSingleMuon11 = cms.vstring('ParkingSingleMuon11'),
    ParkingSingleMuon12 = cms.vstring('ParkingSingleMuon12'),
    ParkingSingleMuon13 = cms.vstring('ParkingSingleMuon13'),
    ParkingSingleMuon14 = cms.vstring('ParkingSingleMuon14'),
    ParkingSingleMuon15 = cms.vstring('ParkingSingleMuon15'),
    ParkingSingleMuon2 = cms.vstring('ParkingSingleMuon2'),
    ParkingSingleMuon3 = cms.vstring('ParkingSingleMuon3'),
    ParkingSingleMuon4 = cms.vstring('ParkingSingleMuon4'),
    ParkingSingleMuon5 = cms.vstring('ParkingSingleMuon5'),
    ParkingSingleMuon6 = cms.vstring('ParkingSingleMuon6'),
    ParkingSingleMuon7 = cms.vstring('ParkingSingleMuon7'),
    ParkingSingleMuon8 = cms.vstring('ParkingSingleMuon8'),
    ParkingSingleMuon9 = cms.vstring('ParkingSingleMuon9'),
    ParkingVBF0 = cms.vstring(
        'ParkingVBF0',
        'ParkingVBF1'
    ),
    ParkingVBF1 = cms.vstring(
        'ParkingVBF2',
        'ParkingVBF3'
    ),
    ParkingVBF2 = cms.vstring(
        'ParkingVBF4',
        'ParkingVBF5'
    ),
    ParkingVBF3 = cms.vstring(
        'ParkingVBF6',
        'ParkingVBF7'
    ),
    PhysicsBTagMuEGTau = cms.vstring(
        'BTagMu',
        'MuonEG',
        'Tau'
    ),
    PhysicsCommissioning = cms.vstring(
        'Commissioning',
        'Cosmics',
        'HLTPhysics',
        'HcalNZS',
        'MonteCarlo',
        'NoBPTX',
        'ZeroBias'
    ),
    PhysicsEGamma0 = cms.vstring('EGamma0'),
    PhysicsEGamma1 = cms.vstring('EGamma1'),
    PhysicsEGamma2 = cms.vstring('EGamma2'),
    PhysicsEGamma3 = cms.vstring('EGamma3'),
    PhysicsEmittanceScan0 = cms.vstring(
        'EmittanceScan0',
        'EmittanceScan1'
    ),
    PhysicsEmittanceScan1 = cms.vstring(
        'EmittanceScan2',
        'EmittanceScan3'
    ),
    PhysicsEmittanceScan2 = cms.vstring(
        'EmittanceScan4',
        'EmittanceScan5'
    ),
    PhysicsHLTPhysics0 = cms.vstring(
        'EphemeralHLTPhysics0',
        'EphemeralHLTPhysics1'
    ),
    PhysicsHLTPhysics1 = cms.vstring(
        'EphemeralHLTPhysics2',
        'EphemeralHLTPhysics3'
    ),
    PhysicsHLTPhysics2 = cms.vstring(
        'EphemeralHLTPhysics4',
        'EphemeralHLTPhysics5'
    ),
    PhysicsHLTPhysics3 = cms.vstring(
        'EphemeralHLTPhysics6',
        'EphemeralHLTPhysics7'
    ),
    PhysicsJetMET0 = cms.vstring('JetMET0'),
    PhysicsJetMET1 = cms.vstring('JetMET1'),
    PhysicsMuon0 = cms.vstring('Muon0'),
    PhysicsMuon1 = cms.vstring('Muon1'),
    PhysicsScoutingPFMonitor = cms.vstring('ScoutingPFMonitor'),
    PhysicsZeroBias0 = cms.vstring(
        'EphemeralZeroBias0',
        'EphemeralZeroBias1'
    ),
    PhysicsZeroBias1 = cms.vstring(
        'EphemeralZeroBias2',
        'EphemeralZeroBias3'
    ),
    PhysicsZeroBias2 = cms.vstring(
        'EphemeralZeroBias4',
        'EphemeralZeroBias5'
    ),
    PhysicsZeroBias3 = cms.vstring(
        'EphemeralZeroBias6',
        'EphemeralZeroBias7'
    ),
    RPCMON = cms.vstring('RPCMonitor'),
    ScoutingPF0 = cms.vstring('ScoutingPF0'),
    ScoutingPF1 = cms.vstring('ScoutingPF1')
)

process.hltAK4CaloJetsPF = cms.EDProducer("FastjetJetProducer",
    Active_Area_Repeats = cms.int32(5),
    DxyTrVtxMax = cms.double(0.0),
    DzTrVtxMax = cms.double(0.0),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(6.0),
    MaxVtxZ = cms.double(15.0),
    MinVtxNdof = cms.int32(5),
    R0 = cms.double(-1.0),
    Rho_EtaMax = cms.double(4.4),
    UseOnlyOnePV = cms.bool(False),
    UseOnlyVertexTracks = cms.bool(False),
    applyWeight = cms.bool(False),
    beta = cms.double(-1.0),
    correctShape = cms.bool(False),
    csRParam = cms.double(-1.0),
    csRho_EtaMax = cms.double(-1.0),
    dRMax = cms.double(-1.0),
    dRMin = cms.double(-1.0),
    doAreaDiskApprox = cms.bool(False),
    doAreaFastjet = cms.bool(False),
    doFastJetNonUniform = cms.bool(False),
    doPUOffsetCorr = cms.bool(False),
    doPVCorrection = cms.bool(False),
    doRhoFastjet = cms.bool(False),
    gridMaxRapidity = cms.double(-1.0),
    gridSpacing = cms.double(-1.0),
    inputEMin = cms.double(0.0),
    inputEtMin = cms.double(0.3),
    jetAlgorithm = cms.string('AntiKt'),
    jetCollInstanceName = cms.string(''),
    jetPtMin = cms.double(1.0),
    jetType = cms.string('CaloJet'),
    maxBadEcalCells = cms.uint32(9999999),
    maxBadHcalCells = cms.uint32(9999999),
    maxDepth = cms.int32(-1),
    maxInputs = cms.uint32(1),
    maxProblematicEcalCells = cms.uint32(9999999),
    maxProblematicHcalCells = cms.uint32(9999999),
    maxRecoveredEcalCells = cms.uint32(9999999),
    maxRecoveredHcalCells = cms.uint32(9999999),
    minSeed = cms.uint32(0),
    minimumTowersFraction = cms.double(0.0),
    muCut = cms.double(-1.0),
    muMax = cms.double(-1.0),
    muMin = cms.double(-1.0),
    nExclude = cms.uint32(0),
    nFilt = cms.int32(-1),
    nSigmaPU = cms.double(1.0),
    puCenters = cms.vdouble(),
    puPtMin = cms.double(10.0),
    puWidth = cms.double(0.0),
    rFilt = cms.double(-1.0),
    rFiltFactor = cms.double(-1.0),
    rParam = cms.double(0.4),
    radiusPU = cms.double(0.4),
    rcut_factor = cms.double(-1.0),
    restrictInputs = cms.bool(False),
    src = cms.InputTag("hltTowerMakerForAll"),
    srcPVs = cms.InputTag("NotUsed"),
    srcWeights = cms.InputTag(""),
    subjetPtMin = cms.double(-1.0),
    subtractorName = cms.string(''),
    sumRecHits = cms.bool(False),
    trimPtFracMin = cms.double(-1.0),
    useCMSBoostedTauSeedingAlgorithm = cms.bool(False),
    useConstituentSubtraction = cms.bool(False),
    useDeterministicSeed = cms.bool(True),
    useDynamicFiltering = cms.bool(False),
    useExplicitGhosts = cms.bool(False),
    useFiltering = cms.bool(False),
    useKtPruning = cms.bool(False),
    useMassDropTagger = cms.bool(False),
    usePruning = cms.bool(False),
    useSoftDrop = cms.bool(False),
    useTrimming = cms.bool(False),
    verbosity = cms.int32(0),
    voronoiRfact = cms.double(-9.0),
    writeCompound = cms.bool(False),
    writeJetsWithConst = cms.bool(False),
    yCut = cms.double(-1.0),
    yMax = cms.double(-1.0),
    yMin = cms.double(-1.0),
    zcut = cms.double(-1.0)
)


process.hltAK4PFAbsoluteCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFHLT'),
    level = cms.string('L3Absolute')
)


process.hltAK4PFCorrector = cms.EDProducer("ChainedJetCorrectorProducer",
    correctors = cms.VInputTag("hltAK4PFFastJetCorrector", "hltAK4PFRelativeCorrector", "hltAK4PFAbsoluteCorrector", "hltAK4PFResidualCorrector")
)


process.hltAK4PFFastJetCorrector = cms.EDProducer("L1FastjetCorrectorProducer",
    algorithm = cms.string('AK4PFHLT'),
    level = cms.string('L1FastJet'),
    srcRho = cms.InputTag("hltFixedGridRhoFastjetAll")
)


process.hltAK4PFJets = cms.EDProducer("FastjetJetProducer",
    Active_Area_Repeats = cms.int32(5),
    DxyTrVtxMax = cms.double(0.0),
    DzTrVtxMax = cms.double(0.0),
    GhostArea = cms.double(0.01),
    Ghost_EtaMax = cms.double(6.0),
    MaxVtxZ = cms.double(15.0),
    MinVtxNdof = cms.int32(0),
    R0 = cms.double(-1.0),
    Rho_EtaMax = cms.double(4.4),
    UseOnlyOnePV = cms.bool(False),
    UseOnlyVertexTracks = cms.bool(False),
    applyWeight = cms.bool(False),
    beta = cms.double(-1.0),
    correctShape = cms.bool(False),
    csRParam = cms.double(-1.0),
    csRho_EtaMax = cms.double(-1.0),
    dRMax = cms.double(-1.0),
    dRMin = cms.double(-1.0),
    doAreaDiskApprox = cms.bool(True),
    doAreaFastjet = cms.bool(False),
    doFastJetNonUniform = cms.bool(False),
    doPUOffsetCorr = cms.bool(False),
    doPVCorrection = cms.bool(False),
    doRhoFastjet = cms.bool(False),
    gridMaxRapidity = cms.double(-1.0),
    gridSpacing = cms.double(-1.0),
    inputEMin = cms.double(0.0),
    inputEtMin = cms.double(0.0),
    jetAlgorithm = cms.string('AntiKt'),
    jetCollInstanceName = cms.string(''),
    jetPtMin = cms.double(0.0),
    jetType = cms.string('PFJet'),
    maxBadEcalCells = cms.uint32(9999999),
    maxBadHcalCells = cms.uint32(9999999),
    maxDepth = cms.int32(-1),
    maxInputs = cms.uint32(1),
    maxProblematicEcalCells = cms.uint32(9999999),
    maxProblematicHcalCells = cms.uint32(9999999),
    maxRecoveredEcalCells = cms.uint32(9999999),
    maxRecoveredHcalCells = cms.uint32(9999999),
    minSeed = cms.uint32(0),
    minimumTowersFraction = cms.double(0.0),
    muCut = cms.double(-1.0),
    muMax = cms.double(-1.0),
    muMin = cms.double(-1.0),
    nExclude = cms.uint32(0),
    nFilt = cms.int32(-1),
    nSigmaPU = cms.double(1.0),
    puCenters = cms.vdouble(),
    puPtMin = cms.double(10.0),
    puWidth = cms.double(0.0),
    rFilt = cms.double(-1.0),
    rFiltFactor = cms.double(-1.0),
    rParam = cms.double(0.4),
    radiusPU = cms.double(0.4),
    rcut_factor = cms.double(-1.0),
    restrictInputs = cms.bool(False),
    src = cms.InputTag("hltParticleFlow"),
    srcPVs = cms.InputTag("hltPixelVertices"),
    srcWeights = cms.InputTag(""),
    subjetPtMin = cms.double(-1.0),
    subtractorName = cms.string(''),
    sumRecHits = cms.bool(False),
    trimPtFracMin = cms.double(-1.0),
    useCMSBoostedTauSeedingAlgorithm = cms.bool(False),
    useConstituentSubtraction = cms.bool(False),
    useDeterministicSeed = cms.bool(True),
    useDynamicFiltering = cms.bool(False),
    useExplicitGhosts = cms.bool(False),
    useFiltering = cms.bool(False),
    useKtPruning = cms.bool(False),
    useMassDropTagger = cms.bool(False),
    usePruning = cms.bool(False),
    useSoftDrop = cms.bool(False),
    useTrimming = cms.bool(False),
    verbosity = cms.int32(0),
    voronoiRfact = cms.double(-9.0),
    writeCompound = cms.bool(False),
    writeJetsWithConst = cms.bool(False),
    yCut = cms.double(-1.0),
    yMax = cms.double(-1.0),
    yMin = cms.double(-1.0),
    zcut = cms.double(-1.0)
)


process.hltAK4PFJetsCorrected = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("hltAK4PFCorrector"),
    src = cms.InputTag("hltAK4PFJets"),
    verbose = cms.untracked.bool(False)
)


process.hltAK4PFJetsLooseID = cms.EDProducer("HLTPFJetIDProducer",
    CEF = cms.double(0.99),
    CHF = cms.double(0.0),
    NCH = cms.int32(0),
    NEF = cms.double(0.99),
    NHF = cms.double(0.99),
    NTOT = cms.int32(1),
    jetsInput = cms.InputTag("hltAK4PFJets"),
    maxCF = cms.double(99.0),
    maxEta = cms.double(1e+99),
    minPt = cms.double(20.0)
)


process.hltAK4PFJetsLooseIDCorrected = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("hltAK4PFCorrector"),
    src = cms.InputTag("hltAK4PFJetsLooseID"),
    verbose = cms.untracked.bool(False)
)


process.hltAK4PFJetsTightID = cms.EDProducer("HLTPFJetIDProducer",
    CEF = cms.double(0.99),
    CHF = cms.double(0.0),
    NCH = cms.int32(0),
    NEF = cms.double(0.99),
    NHF = cms.double(0.9),
    NTOT = cms.int32(1),
    jetsInput = cms.InputTag("hltAK4PFJets"),
    maxCF = cms.double(99.0),
    maxEta = cms.double(1e+99),
    minPt = cms.double(20.0)
)


process.hltAK4PFJetsTightIDCorrected = cms.EDProducer("CorrectedPFJetProducer",
    correctors = cms.VInputTag("hltAK4PFCorrector"),
    src = cms.InputTag("hltAK4PFJetsTightID"),
    verbose = cms.untracked.bool(False)
)


process.hltAK4PFRelativeCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFHLT'),
    level = cms.string('L2Relative')
)


process.hltAK4PFResidualCorrector = cms.EDProducer("LXXXCorrectorProducer",
    algorithm = cms.string('AK4PFHLT'),
    level = cms.string('L2L3Residual')
)


process.hltCsc2DRecHits = cms.EDProducer("CSCRecHitDProducer",
    CSCDebug = cms.untracked.bool(False),
    CSCNoOfTimeBinsForDynamicPedestal = cms.int32(2),
    CSCStripClusterChargeCut = cms.double(25.0),
    CSCStripPeakThreshold = cms.double(10.0),
    CSCStripxtalksOffset = cms.double(0.03),
    CSCUseCalibrations = cms.bool(True),
    CSCUseGasGainCorrections = cms.bool(False),
    CSCUseReducedWireTimeWindow = cms.bool(True),
    CSCUseStaticPedestals = cms.bool(False),
    CSCUseTimingCorrections = cms.bool(True),
    CSCWireClusterDeltaT = cms.int32(1),
    CSCWireTimeWindowHigh = cms.int32(11),
    CSCWireTimeWindowLow = cms.int32(5),
    CSCstripWireDeltaTime = cms.int32(8),
    ConstSyst_ME12 = cms.double(0.02),
    ConstSyst_ME13 = cms.double(0.03),
    ConstSyst_ME1a = cms.double(0.01),
    ConstSyst_ME1b = cms.double(0.02),
    ConstSyst_ME21 = cms.double(0.03),
    ConstSyst_ME22 = cms.double(0.03),
    ConstSyst_ME31 = cms.double(0.03),
    ConstSyst_ME32 = cms.double(0.03),
    ConstSyst_ME41 = cms.double(0.03),
    NoiseLevel_ME12 = cms.double(7.0),
    NoiseLevel_ME13 = cms.double(4.0),
    NoiseLevel_ME1a = cms.double(9.0),
    NoiseLevel_ME1b = cms.double(6.0),
    NoiseLevel_ME21 = cms.double(5.0),
    NoiseLevel_ME22 = cms.double(7.0),
    NoiseLevel_ME31 = cms.double(5.0),
    NoiseLevel_ME32 = cms.double(7.0),
    NoiseLevel_ME41 = cms.double(5.0),
    UseAverageTime = cms.bool(False),
    UseFivePoleFit = cms.bool(True),
    UseParabolaFit = cms.bool(False),
    XTasymmetry_ME12 = cms.double(0.015),
    XTasymmetry_ME13 = cms.double(0.02),
    XTasymmetry_ME1a = cms.double(0.023),
    XTasymmetry_ME1b = cms.double(0.01),
    XTasymmetry_ME21 = cms.double(0.023),
    XTasymmetry_ME22 = cms.double(0.023),
    XTasymmetry_ME31 = cms.double(0.023),
    XTasymmetry_ME32 = cms.double(0.023),
    XTasymmetry_ME41 = cms.double(0.023),
    readBadChambers = cms.bool(True),
    readBadChannels = cms.bool(False),
    stripDigiTag = cms.InputTag("hltMuonCSCDigis","MuonCSCStripDigi"),
    wireDigiTag = cms.InputTag("hltMuonCSCDigis","MuonCSCWireDigi")
)


process.hltCscSegments = cms.EDProducer("CSCSegmentProducer",
    algo_psets = cms.VPSet(cms.PSet(
        algo_name = cms.string('CSCSegAlgoRU'),
        algo_psets = cms.VPSet(
            cms.PSet(
                chi2Max = cms.double(100.0),
                chi2Norm_2D_ = cms.double(35.0),
                chi2_str = cms.double(50.0),
                dPhiIntMax = cms.double(0.005),
                dPhiMax = cms.double(0.006),
                dRIntMax = cms.double(2.0),
                dRMax = cms.double(1.5),
                doCollisions = cms.bool(True),
                minLayersApart = cms.int32(1),
                wideSeg = cms.double(3.0)
            ),
            cms.PSet(
                chi2Max = cms.double(100.0),
                chi2Norm_2D_ = cms.double(35.0),
                chi2_str = cms.double(50.0),
                dPhiIntMax = cms.double(0.004),
                dPhiMax = cms.double(0.005),
                dRIntMax = cms.double(2.0),
                dRMax = cms.double(1.5),
                doCollisions = cms.bool(True),
                minLayersApart = cms.int32(1),
                wideSeg = cms.double(3.0)
            ),
            cms.PSet(
                chi2Max = cms.double(100.0),
                chi2Norm_2D_ = cms.double(35.0),
                chi2_str = cms.double(50.0),
                dPhiIntMax = cms.double(0.003),
                dPhiMax = cms.double(0.004),
                dRIntMax = cms.double(2.0),
                dRMax = cms.double(1.5),
                doCollisions = cms.bool(True),
                minLayersApart = cms.int32(1),
                wideSeg = cms.double(3.0)
            ),
            cms.PSet(
                chi2Max = cms.double(60.0),
                chi2Norm_2D_ = cms.double(20.0),
                chi2_str = cms.double(30.0),
                dPhiIntMax = cms.double(0.002),
                dPhiMax = cms.double(0.003),
                dRIntMax = cms.double(2.0),
                dRMax = cms.double(1.5),
                doCollisions = cms.bool(True),
                minLayersApart = cms.int32(1),
                wideSeg = cms.double(3.0)
            ),
            cms.PSet(
                chi2Max = cms.double(180.0),
                chi2Norm_2D_ = cms.double(60.0),
                chi2_str = cms.double(80.0),
                dPhiIntMax = cms.double(0.005),
                dPhiMax = cms.double(0.007),
                dRIntMax = cms.double(2.0),
                dRMax = cms.double(1.5),
                doCollisions = cms.bool(True),
                minLayersApart = cms.int32(1),
                wideSeg = cms.double(3.0)
            ),
            cms.PSet(
                chi2Max = cms.double(100.0),
                chi2Norm_2D_ = cms.double(35.0),
                chi2_str = cms.double(50.0),
                dPhiIntMax = cms.double(0.004),
                dPhiMax = cms.double(0.006),
                dRIntMax = cms.double(2.0),
                dRMax = cms.double(1.5),
                doCollisions = cms.bool(True),
                minLayersApart = cms.int32(1),
                wideSeg = cms.double(3.0)
            )
        ),
        chamber_types = cms.vstring(
            'ME1/a',
            'ME1/b',
            'ME1/2',
            'ME1/3',
            'ME2/1',
            'ME2/2',
            'ME3/1',
            'ME3/2',
            'ME4/1',
            'ME4/2'
        ),
        parameters_per_chamber_type = cms.vint32(
            1, 2, 3, 4, 5,
            6, 5, 6, 5, 6
        )
    )),
    algo_type = cms.int32(1),
    inputObjects = cms.InputTag("hltCsc2DRecHits")
)


process.hltDisplacedmumuVtxNoMatchingProducerNoVtx = cms.EDProducer("HLTDisplacedmumuVtxProducer",
    ChargeOpt = cms.int32(0),
    MaxEta = cms.double(2.5),
    MaxInvMass = cms.double(99999.0),
    MinInvMass = cms.double(0.0),
    MinPt = cms.double(0.0),
    MinPtPair = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltDoubleMu3L3FilteredNoVtx"),
    Src = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    matchToPrevious = cms.bool(False)
)


process.hltDisplacedmumuVtxNoMatchingProducerVtx = cms.EDProducer("HLTDisplacedmumuVtxProducer",
    ChargeOpt = cms.int32(0),
    MaxEta = cms.double(2.5),
    MaxInvMass = cms.double(99999.0),
    MinInvMass = cms.double(0.0),
    MinPt = cms.double(0.0),
    MinPtPair = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltDoubleMu3L3Filtered"),
    Src = cms.InputTag("hltIterL3MuonCandidates"),
    matchToPrevious = cms.bool(False)
)


process.hltDoubletRecoveryClustersRefRemoval = cms.EDProducer("TrackClusterRemover",
    TrackQuality = cms.string('highPurity'),
    maxChi2 = cms.double(16.0),
    minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
    oldClusterRemovalInfo = cms.InputTag(""),
    overrideTrkQuals = cms.InputTag(""),
    pixelClusters = cms.InputTag("hltSiPixelClusters"),
    stripClusters = cms.InputTag("hltSiStripRawToClustersFacility"),
    trackClassifier = cms.InputTag("","QualityMasks"),
    trajectories = cms.InputTag("hltIter0PFlowTrackSelectionHighPurity")
)


process.hltDoubletRecoveryMaskedMeasurementTrackerEvent = cms.EDProducer("MaskedMeasurementTrackerEventProducer",
    clustersToSkip = cms.InputTag("hltDoubletRecoveryClustersRefRemoval"),
    phase2clustersToSkip = cms.InputTag(""),
    src = cms.InputTag("hltMeasurementTrackerEvent")
)


process.hltDoubletRecoveryPFlowCkfTrackCandidates = cms.EDProducer("MkFitOutputConverter",
    batchSize = cms.int32(16),
    candMVASel = cms.bool(False),
    candWP = cms.double(0.0),
    doErrorRescale = cms.bool(True),
    mkFitEventOfHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitEventOfHits"),
    mkFitPixelHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits"),
    mkFitSeeds = cms.InputTag("hltDoubletRecoveryPFlowCkfTrackCandidatesMkFitSeeds"),
    mkFitStripHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits"),
    propagatorAlong = cms.ESInputTag("","PropagatorWithMaterialParabolicMf"),
    propagatorOpposite = cms.ESInputTag("","PropagatorWithMaterialParabolicMfOpposite"),
    qualityMaxInvPt = cms.double(100.0),
    qualityMaxPosErr = cms.double(100.0),
    qualityMaxR = cms.double(120.0),
    qualityMaxZ = cms.double(280.0),
    qualityMinTheta = cms.double(0.01),
    qualitySignPt = cms.bool(True),
    seeds = cms.InputTag("hltDoubletRecoveryPFlowPixelSeeds"),
    tfDnnLabel = cms.string('trackSelectionTf'),
    tracks = cms.InputTag("hltDoubletRecoveryPFlowCkfTrackCandidatesMkFit"),
    ttrhBuilder = cms.ESInputTag("","hltESPTTRHBWithTrackAngle")
)


process.hltDoubletRecoveryPFlowCkfTrackCandidatesMkFit = cms.EDProducer("MkFitProducer",
    backwardFitInCMSSW = cms.bool(False),
    buildingRoutine = cms.string('cloneEngine'),
    clustersToSkip = cms.InputTag("hltDoubletRecoveryClustersRefRemoval"),
    config = cms.ESInputTag("","hltDoubletRecoveryPFlowTrackCandidatesMkFitConfig"),
    eventOfHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitEventOfHits"),
    limitConcurrency = cms.untracked.bool(False),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    mkFitSilent = cms.untracked.bool(True),
    pixelHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits"),
    removeDuplicates = cms.bool(True),
    seedCleaning = cms.bool(True),
    seeds = cms.InputTag("hltDoubletRecoveryPFlowCkfTrackCandidatesMkFitSeeds"),
    stripHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits")
)


process.hltDoubletRecoveryPFlowCkfTrackCandidatesMkFitSeeds = cms.EDProducer("MkFitSeedConverter",
    maxNSeeds = cms.uint32(500000),
    seeds = cms.InputTag("hltDoubletRecoveryPFlowPixelSeeds"),
    ttrhBuilder = cms.ESInputTag("","hltESPTTRHBWithTrackAngle")
)


process.hltDoubletRecoveryPFlowCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltDoubletRecovery'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltDoubletRecoveryMaskedMeasurementTrackerEvent"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltDoubletRecoveryPFlowCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltDoubletRecoveryPFlowPixelClusterCheck = cms.EDProducer("ClusterCheckerEDProducer",
    ClusterCollectionLabel = cms.InputTag("hltMeasurementTrackerEvent"),
    DontCountDetsAboveNClusters = cms.uint32(0),
    MaxNumberOfPixelClusters = cms.uint32(40000),
    MaxNumberOfStripClusters = cms.uint32(50000),
    PixelClusterCollectionLabel = cms.InputTag("hltSiPixelClusters"),
    cut = cms.string(''),
    doClusterCheck = cms.bool(False),
    silentClusterCheck = cms.untracked.bool(False)
)


process.hltDoubletRecoveryPFlowPixelHitDoublets = cms.EDProducer("HitPairEDProducer",
    clusterCheck = cms.InputTag("hltDoubletRecoveryPFlowPixelClusterCheck"),
    layerPairs = cms.vuint32(0),
    maxElement = cms.uint32(0),
    maxElementTotal = cms.uint32(50000000),
    produceIntermediateHitDoublets = cms.bool(False),
    produceSeedingHitSets = cms.bool(True),
    putEmptyIfMaxElementReached = cms.bool(False),
    seedingLayers = cms.InputTag(""),
    trackingRegions = cms.InputTag(""),
    trackingRegionsSeedingLayers = cms.InputTag("hltDoubletRecoveryPixelLayersAndRegions")
)


process.hltDoubletRecoveryPFlowPixelSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    seedingHitSets = cms.InputTag("hltDoubletRecoveryPFlowPixelHitDoublets")
)


process.hltDoubletRecoveryPFlowTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 0.003),
            d0err_par = cms.vdouble(0.001, 0.001, 0.001),
            dr_exp = cms.vint32(4, 4, 4),
            dr_par1 = cms.vdouble(3.40282346639e+38, 0.45, 0.45),
            dr_par2 = cms.vdouble(3.40282346639e+38, 0.34, 0.34)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 4),
            dz_par1 = cms.vdouble(3.40282346639e+38, 0.45, 0.45),
            dz_par2 = cms.vdouble(3.40282346639e+38, 0.39, 0.39)
        ),
        maxChi2 = cms.vdouble(999.0, 999.0, 4.9),
        maxChi2n = cms.vdouble(999.0, 999.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
        maxLostLayers = cms.vint32(0, 0, 0),
        min3DLayers = cms.vint32(0, 0, 3),
        minHits = cms.vint32(0, 0, 5),
        minLayers = cms.vint32(0, 0, 4),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltDoubletRecoveryPFlowCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltDoubletRecoveryPFlowTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltDoubletRecoveryPFlowTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltDoubletRecoveryPFlowTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltDoubletRecoveryPFlowCtfWithMaterialTracks")
)


process.hltDoubletRecoveryPixelLayersAndRegions = cms.EDProducer("PixelInactiveAreaTrackingRegionsSeedingLayersProducer",
    BPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0027),
        hitErrorRZ = cms.double(0.006),
        skipClusters = cms.InputTag("hltDoubletRecoveryClustersRefRemoval"),
        useErrorsFromParam = cms.bool(True)
    ),
    FPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0051),
        hitErrorRZ = cms.double(0.0036),
        skipClusters = cms.InputTag("hltDoubletRecoveryClustersRefRemoval"),
        useErrorsFromParam = cms.bool(True)
    ),
    MTEC = cms.PSet(

    ),
    MTIB = cms.PSet(

    ),
    MTID = cms.PSet(

    ),
    MTOB = cms.PSet(

    ),
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        extraEta = cms.double(0.0),
        extraPhi = cms.double(0.0),
        maxNVertices = cms.int32(3),
        measurementTrackerName = cms.InputTag("hltDoubletRecoveryMaskedMeasurementTrackerEvent"),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        operationMode = cms.string('VerticesFixed'),
        originRadius = cms.double(0.015),
        precise = cms.bool(True),
        ptMin = cms.double(1.2),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
        whereToUseMeasurementTracker = cms.string('ForSiStrips'),
        zErrorBeamSpot = cms.double(15.0),
        zErrorVertex = cms.double(0.03)
    ),
    TEC = cms.PSet(

    ),
    TIB = cms.PSet(

    ),
    TID = cms.PSet(

    ),
    TOB = cms.PSet(

    ),
    badPixelFEDChannelCollectionLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    createPlottingFiles = cms.untracked.bool(False),
    debug = cms.untracked.bool(False),
    ignoreSingleFPixPanelModules = cms.bool(True),
    inactivePixelDetectorLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    layerList = cms.vstring(
        'BPix1+BPix2',
        'BPix2+FPix1_pos',
        'BPix2+FPix1_neg',
        'FPix1_pos+FPix2_pos',
        'FPix1_neg+FPix2_neg',
        'BPix1+FPix2_neg',
        'BPix2+FPix2_neg',
        'FPix2_neg+FPix3_neg',
        'BPix2+BPix3'
    )
)


process.hltDt1DRecHits = cms.EDProducer("DTRecHitProducer",
    debug = cms.untracked.bool(False),
    dtDigiLabel = cms.InputTag("hltMuonDTDigis"),
    recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
    recAlgoConfig = cms.PSet(
        debug = cms.untracked.bool(False),
        doVdriftCorr = cms.bool(True),
        maxTime = cms.double(420.0),
        minTime = cms.double(-3.0),
        readLegacyTTrigDB = cms.bool(True),
        readLegacyVDriftDB = cms.bool(True),
        stepTwoFromDigi = cms.bool(False),
        tTrigMode = cms.string('DTTTrigSyncFromDB'),
        tTrigModeConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            doT0Correction = cms.bool(True),
            doTOFCorrection = cms.bool(True),
            doWirePropCorrection = cms.bool(True),
            t0Label = cms.string(''),
            tTrigLabel = cms.string(''),
            tofCorrType = cms.int32(0),
            vPropWire = cms.double(24.4),
            wirePropCorrType = cms.int32(0)
        ),
        useUncertDB = cms.bool(True)
    )
)


process.hltDt4DSegments = cms.EDProducer("DTRecSegment4DProducer",
    Reco4DAlgoConfig = cms.PSet(
        AllDTRecHits = cms.bool(True),
        Reco2DAlgoConfig = cms.PSet(
            AlphaMaxPhi = cms.double(1.0),
            AlphaMaxTheta = cms.double(0.9),
            MaxAllowedHits = cms.uint32(50),
            debug = cms.untracked.bool(False),
            hit_afterT0_resolution = cms.double(0.03),
            nSharedHitsMax = cms.int32(2),
            nUnSharedHitsMin = cms.int32(2),
            performT0SegCorrection = cms.bool(False),
            performT0_vdriftSegCorrection = cms.bool(False),
            perform_delta_rejecting = cms.bool(False),
            recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
            recAlgoConfig = cms.PSet(
                debug = cms.untracked.bool(False),
                doVdriftCorr = cms.bool(True),
                maxTime = cms.double(420.0),
                minTime = cms.double(-3.0),
                readLegacyTTrigDB = cms.bool(True),
                readLegacyVDriftDB = cms.bool(True),
                stepTwoFromDigi = cms.bool(False),
                tTrigMode = cms.string('DTTTrigSyncFromDB'),
                tTrigModeConfig = cms.PSet(
                    debug = cms.untracked.bool(False),
                    doT0Correction = cms.bool(True),
                    doTOFCorrection = cms.bool(True),
                    doWirePropCorrection = cms.bool(True),
                    t0Label = cms.string(''),
                    tTrigLabel = cms.string(''),
                    tofCorrType = cms.int32(0),
                    vPropWire = cms.double(24.4),
                    wirePropCorrType = cms.int32(0)
                ),
                useUncertDB = cms.bool(True)
            ),
            segmCleanerMode = cms.int32(2)
        ),
        Reco2DAlgoName = cms.string('DTCombinatorialPatternReco'),
        debug = cms.untracked.bool(False),
        hit_afterT0_resolution = cms.double(0.03),
        nSharedHitsMax = cms.int32(2),
        nUnSharedHitsMin = cms.int32(2),
        performT0SegCorrection = cms.bool(False),
        performT0_vdriftSegCorrection = cms.bool(False),
        perform_delta_rejecting = cms.bool(False),
        recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
        recAlgoConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            doVdriftCorr = cms.bool(True),
            maxTime = cms.double(420.0),
            minTime = cms.double(-3.0),
            readLegacyTTrigDB = cms.bool(True),
            readLegacyVDriftDB = cms.bool(True),
            stepTwoFromDigi = cms.bool(False),
            tTrigMode = cms.string('DTTTrigSyncFromDB'),
            tTrigModeConfig = cms.PSet(
                debug = cms.untracked.bool(False),
                doT0Correction = cms.bool(True),
                doTOFCorrection = cms.bool(True),
                doWirePropCorrection = cms.bool(True),
                t0Label = cms.string(''),
                tTrigLabel = cms.string(''),
                tofCorrType = cms.int32(0),
                vPropWire = cms.double(24.4),
                wirePropCorrType = cms.int32(0)
            ),
            useUncertDB = cms.bool(True)
        ),
        segmCleanerMode = cms.int32(2)
    ),
    Reco4DAlgoName = cms.string('DTCombinatorialPatternReco4D'),
    debug = cms.untracked.bool(False),
    recHits1DLabel = cms.InputTag("hltDt1DRecHits"),
    recHits2DLabel = cms.InputTag("dt2DSegments")
)


process.hltEcalDetIdToBeRecovered = cms.EDProducer("EcalDetIdToBeRecoveredProducer",
    ebDetIdToBeRecovered = cms.string('ebDetId'),
    ebFEToBeRecovered = cms.string('ebFE'),
    ebIntegrityChIdErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityChIdErrors"),
    ebIntegrityGainErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityGainErrors"),
    ebIntegrityGainSwitchErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityGainSwitchErrors"),
    ebSrFlagCollection = cms.InputTag("hltEcalDigisLegacy"),
    eeDetIdToBeRecovered = cms.string('eeDetId'),
    eeFEToBeRecovered = cms.string('eeFE'),
    eeIntegrityChIdErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityChIdErrors"),
    eeIntegrityGainErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityGainErrors"),
    eeIntegrityGainSwitchErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityGainSwitchErrors"),
    eeSrFlagCollection = cms.InputTag("hltEcalDigisLegacy"),
    integrityBlockSizeErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityBlockSizeErrors"),
    integrityTTIdErrors = cms.InputTag("hltEcalDigisLegacy","EcalIntegrityTTIdErrors")
)


process.hltEcalDigis = cms.EDProducer("EcalDigisFromPortableProducer",
    digisInLabelEB = cms.InputTag("hltEcalDigisSoA","ebDigis"),
    digisInLabelEE = cms.InputTag("hltEcalDigisSoA","eeDigis"),
    digisOutLabelEB = cms.string('ebDigis'),
    digisOutLabelEE = cms.string('eeDigis'),
    produceDummyIntegrityCollections = cms.bool(False)
)


process.hltEcalDigisLegacy = cms.EDProducer("EcalRawToDigi",
    DoRegional = cms.bool(False),
    FEDs = cms.vint32(
        601, 602, 603, 604, 605,
        606, 607, 608, 609, 610,
        611, 612, 613, 614, 615,
        616, 617, 618, 619, 620,
        621, 622, 623, 624, 625,
        626, 627, 628, 629, 630,
        631, 632, 633, 634, 635,
        636, 637, 638, 639, 640,
        641, 642, 643, 644, 645,
        646, 647, 648, 649, 650,
        651, 652, 653, 654
    ),
    FedLabel = cms.InputTag("listfeds"),
    InputLabel = cms.InputTag("rawDataCollector"),
    eventPut = cms.bool(True),
    feIdCheck = cms.bool(True),
    feUnpacking = cms.bool(True),
    forceToKeepFRData = cms.bool(False),
    headerUnpacking = cms.bool(True),
    memUnpacking = cms.bool(True),
    numbTriggerTSamples = cms.int32(1),
    numbXtalTSamples = cms.int32(10),
    orderedDCCIdList = cms.vint32(
        1, 2, 3, 4, 5,
        6, 7, 8, 9, 10,
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25,
        26, 27, 28, 29, 30,
        31, 32, 33, 34, 35,
        36, 37, 38, 39, 40,
        41, 42, 43, 44, 45,
        46, 47, 48, 49, 50,
        51, 52, 53, 54
    ),
    orderedFedList = cms.vint32(
        601, 602, 603, 604, 605,
        606, 607, 608, 609, 610,
        611, 612, 613, 614, 615,
        616, 617, 618, 619, 620,
        621, 622, 623, 624, 625,
        626, 627, 628, 629, 630,
        631, 632, 633, 634, 635,
        636, 637, 638, 639, 640,
        641, 642, 643, 644, 645,
        646, 647, 648, 649, 650,
        651, 652, 653, 654
    ),
    silentMode = cms.untracked.bool(True),
    srpUnpacking = cms.bool(True),
    syncCheck = cms.bool(True),
    tccUnpacking = cms.bool(True)
)


process.hltEcalDigisSoA = cms.EDProducer("EcalRawToDigiPortable@alpaka",
    FEDs = cms.vint32(
        601, 602, 603, 604, 605,
        606, 607, 608, 609, 610,
        611, 612, 613, 614, 615,
        616, 617, 618, 619, 620,
        621, 622, 623, 624, 625,
        626, 627, 628, 629, 630,
        631, 632, 633, 634, 635,
        636, 637, 638, 639, 640,
        641, 642, 643, 644, 645,
        646, 647, 648, 649, 650,
        651, 652, 653, 654
    ),
    InputLabel = cms.InputTag("rawDataCollector"),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    digisLabelEB = cms.string('ebDigis'),
    digisLabelEE = cms.string('eeDigis'),
    maxChannelsEB = cms.uint32(61200),
    maxChannelsEE = cms.uint32(14648)
)


process.hltEcalPreshowerDigis = cms.EDProducer("ESRawToDigi",
    ESdigiCollection = cms.string(''),
    InstanceES = cms.string(''),
    LookupTable = cms.FileInPath('EventFilter/ESDigiToRaw/data/ES_lookup_table.dat'),
    debugMode = cms.untracked.bool(False),
    sourceTag = cms.InputTag("rawDataCollector")
)


process.hltEcalPreshowerRecHit = cms.EDProducer("ESRecHitProducer",
    ESRecoAlgo = cms.int32(0),
    ESdigiCollection = cms.InputTag("hltEcalPreshowerDigis"),
    ESrechitCollection = cms.string('EcalRecHitsES'),
    algo = cms.string('ESRecHitWorker')
)


process.hltEcalRecHit = cms.EDProducer("EcalRecHitProducer",
    ChannelStatusToBeExcluded = cms.vstring(),
    EBLaserMAX = cms.double(3.0),
    EBLaserMIN = cms.double(0.5),
    EBrechitCollection = cms.string('EcalRecHitsEB'),
    EBuncalibRecHitCollection = cms.InputTag("hltEcalUncalibRecHit","EcalUncalibRecHitsEB"),
    EELaserMAX = cms.double(8.0),
    EELaserMIN = cms.double(0.5),
    EErechitCollection = cms.string('EcalRecHitsEE'),
    EEuncalibRecHitCollection = cms.InputTag("hltEcalUncalibRecHit","EcalUncalibRecHitsEE"),
    algo = cms.string('EcalRecHitWorkerSimple'),
    algoRecover = cms.string('EcalRecHitWorkerRecover'),
    bdtWeightFileCracks = cms.FileInPath('RecoLocalCalo/EcalDeadChannelRecoveryAlgos/data/BDTWeights/bdtgAllRH_8GT700MeV_onlyCracks_ZskimData2017_v1.xml'),
    bdtWeightFileNoCracks = cms.FileInPath('RecoLocalCalo/EcalDeadChannelRecoveryAlgos/data/BDTWeights/bdtgAllRH_8GT700MeV_noCracks_ZskimData2017_v1.xml'),
    cleaningConfig = cms.PSet(
        cThreshold_barrel = cms.double(4.0),
        cThreshold_double = cms.double(10.0),
        cThreshold_endcap = cms.double(15.0),
        e4e1Threshold_barrel = cms.double(0.08),
        e4e1Threshold_endcap = cms.double(0.3),
        e4e1_a_barrel = cms.double(0.04),
        e4e1_a_endcap = cms.double(0.02),
        e4e1_b_barrel = cms.double(-0.024),
        e4e1_b_endcap = cms.double(-0.0125),
        e6e2thresh = cms.double(0.04),
        ignoreOutOfTimeThresh = cms.double(1000000000.0),
        tightenCrack_e1_double = cms.double(2.0),
        tightenCrack_e1_single = cms.double(2.0),
        tightenCrack_e4e1_single = cms.double(3.0),
        tightenCrack_e6e2_double = cms.double(3.0)
    ),
    dbStatusToBeExcludedEB = cms.vint32(14, 78, 142),
    dbStatusToBeExcludedEE = cms.vint32(14, 78, 142),
    ebDetIdToBeRecovered = cms.InputTag("hltEcalDetIdToBeRecovered","ebDetId"),
    ebFEToBeRecovered = cms.InputTag("hltEcalDetIdToBeRecovered","ebFE"),
    eeDetIdToBeRecovered = cms.InputTag("hltEcalDetIdToBeRecovered","eeDetId"),
    eeFEToBeRecovered = cms.InputTag("hltEcalDetIdToBeRecovered","eeFE"),
    flagsMapDBReco = cms.PSet(
        kDead = cms.vstring('kNoDataNoTP'),
        kGood = cms.vstring(
            'kOk',
            'kDAC',
            'kNoLaser',
            'kNoisy'
        ),
        kNeighboursRecovered = cms.vstring(
            'kFixedG0',
            'kNonRespondingIsolated',
            'kDeadVFE'
        ),
        kNoisy = cms.vstring(
            'kNNoisy',
            'kFixedG6',
            'kFixedG1'
        ),
        kTowerRecovered = cms.vstring('kDeadFE')
    ),
    killDeadChannels = cms.bool(True),
    laserCorrection = cms.bool(True),
    logWarningEtThreshold_EB_FE = cms.double(-1.0),
    logWarningEtThreshold_EE_FE = cms.double(-1.0),
    recoverEBFE = cms.bool(False),
    recoverEBIsolatedChannels = cms.bool(False),
    recoverEBVFE = cms.bool(False),
    recoverEEFE = cms.bool(False),
    recoverEEIsolatedChannels = cms.bool(False),
    recoverEEVFE = cms.bool(False),
    singleChannelRecoveryMethod = cms.string('NeuralNetworks'),
    singleChannelRecoveryThreshold = cms.double(8.0),
    skipTimeCalib = cms.bool(False),
    sum8ChannelRecoveryThreshold = cms.double(0.0),
    timeCalibTag = cms.ESInputTag("",""),
    timeOffsetTag = cms.ESInputTag("",""),
    triggerPrimitiveDigiCollection = cms.InputTag("hltEcalDigisLegacy","EcalTriggerPrimitives")
)


process.hltEcalUncalibRecHit = cms.EDProducer("EcalUncalibRecHitSoAToLegacy",
    inputCollectionEB = cms.InputTag("hltEcalUncalibRecHitSoA","EcalUncalibRecHitsEB"),
    inputCollectionEE = cms.InputTag("hltEcalUncalibRecHitSoA","EcalUncalibRecHitsEE"),
    isPhase2 = cms.bool(False),
    outputLabelEB = cms.string('EcalUncalibRecHitsEB'),
    outputLabelEE = cms.string('EcalUncalibRecHitsEE')
)


process.hltEcalUncalibRecHitSoA = cms.EDProducer("EcalUncalibRecHitProducerPortable@alpaka",
    EBamplitudeFitParameters = cms.vdouble(1.138, 1.652),
    EBtimeConstantTerm = cms.double(0.6),
    EBtimeFitLimits_Lower = cms.double(0.2),
    EBtimeFitLimits_Upper = cms.double(1.4),
    EBtimeFitParameters = cms.vdouble(
        -2.015452, 3.130702, -12.3473, 41.88921, -82.83944,
        91.01147, -50.35761, 11.05621
    ),
    EBtimeNconst = cms.double(28.5),
    EEamplitudeFitParameters = cms.vdouble(1.89, 1.4),
    EEtimeConstantTerm = cms.double(1.0),
    EEtimeFitLimits_Lower = cms.double(0.2),
    EEtimeFitLimits_Upper = cms.double(1.4),
    EEtimeFitParameters = cms.vdouble(
        -2.390548, 3.553628, -17.62341, 67.67538, -133.213,
        140.7432, -75.41106, 16.20277
    ),
    EEtimeNconst = cms.double(31.8),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    amplitudeThresholdEB = cms.double(10.0),
    amplitudeThresholdEE = cms.double(10.0),
    digisLabelEB = cms.InputTag("hltEcalDigisSoA","ebDigis"),
    digisLabelEE = cms.InputTag("hltEcalDigisSoA","eeDigis"),
    kernelMinimizeThreads = cms.untracked.vuint32(32, 1, 1),
    outOfTimeThresholdGain12mEB = cms.double(1000.0),
    outOfTimeThresholdGain12mEE = cms.double(1000.0),
    outOfTimeThresholdGain12pEB = cms.double(1000.0),
    outOfTimeThresholdGain12pEE = cms.double(1000.0),
    outOfTimeThresholdGain61mEB = cms.double(1000.0),
    outOfTimeThresholdGain61mEE = cms.double(1000.0),
    outOfTimeThresholdGain61pEB = cms.double(1000.0),
    outOfTimeThresholdGain61pEE = cms.double(1000.0),
    recHitsLabelEB = cms.string('EcalUncalibRecHitsEB'),
    recHitsLabelEE = cms.string('EcalUncalibRecHitsEE'),
    shouldRunTimingComputation = cms.bool(True)
)


process.hltEgammaCandidates = cms.EDProducer("EgammaHLTRecoEcalCandidateProducers",
    recoEcalCandidateCollection = cms.string(''),
    scHybridBarrelProducer = cms.InputTag("hltParticleFlowSuperClusterECALL1Seeded","hltParticleFlowSuperClusterECALBarrel"),
    scIslandEndcapProducer = cms.InputTag("hltParticleFlowSuperClusterECALL1Seeded","hltParticleFlowSuperClusterECALEndcapWithPreshower")
)


process.hltEgammaCandidatesUnseeded = cms.EDProducer("EgammaHLTRecoEcalCandidateProducers",
    recoEcalCandidateCollection = cms.string(''),
    scHybridBarrelProducer = cms.InputTag("hltParticleFlowSuperClusterECALUnseeded","hltParticleFlowSuperClusterECALBarrel"),
    scIslandEndcapProducer = cms.InputTag("hltParticleFlowSuperClusterECALUnseeded","hltParticleFlowSuperClusterECALEndcapWithPreshower")
)


process.hltEgammaCkfTrackCandidatesForGSFUnseeded = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTPSetTrajectoryBuilderForGsfElectrons')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(True),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(True),
    maxNSeeds = cms.uint32(1000000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltEgammaElectronPixelSeedsUnseeded"),
    useHitsSplitting = cms.bool(True)
)


process.hltEgammaClusterShape = cms.EDProducer("EgammaHLTClusterShapeProducer",
    ecalRechitEB = cms.InputTag("hltRechitInRegionsECAL","EcalRecHitsEB"),
    ecalRechitEE = cms.InputTag("hltRechitInRegionsECAL","EcalRecHitsEE"),
    multThresEB = cms.double(1.0),
    multThresEE = cms.double(1.25),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidates")
)


process.hltEgammaClusterShapeUnseeded = cms.EDProducer("EgammaHLTClusterShapeProducer",
    ecalRechitEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    ecalRechitEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    multThresEB = cms.double(1.0),
    multThresEE = cms.double(1.25),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded")
)


process.hltEgammaEcalPFClusterIsoDr0p2 = cms.EDProducer("EgammaHLTEcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doRhoCorrection = cms.bool(False),
    drMax = cms.double(0.2),
    drVetoBarrel = cms.double(0.0),
    drVetoEndcap = cms.double(0.0),
    effectiveAreas = cms.vdouble(0.085, 0.0),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducer = cms.InputTag("hltParticleFlowClusterECALL1Seeded"),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidates"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    rhoScale = cms.double(1.0)
)


process.hltEgammaEcalPFClusterIsoUnseeded = cms.EDProducer("EgammaHLTEcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doRhoCorrection = cms.bool(False),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.0),
    drVetoEndcap = cms.double(0.0),
    effectiveAreas = cms.vdouble(0.16544, 0.13212),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducer = cms.InputTag("hltParticleFlowClusterECALUnseeded"),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    rhoScale = cms.double(1.0)
)


process.hltEgammaEleGsfTrackIsoUnseeded = cms.EDProducer("EgammaHLTElectronTrackIsolationProducers",
    beamSpotProducer = cms.InputTag("hltOnlineBeamSpot"),
    egTrkIsoConeSize = cms.double(0.2),
    egTrkIsoPtMin = cms.double(1.0),
    egTrkIsoRSpan = cms.double(999999.0),
    egTrkIsoStripBarrel = cms.double(0.01),
    egTrkIsoStripEndcap = cms.double(0.01),
    egTrkIsoVetoConeSizeBarrel = cms.double(0.03),
    egTrkIsoVetoConeSizeEndcap = cms.double(0.03),
    egTrkIsoZSpan = cms.double(0.15),
    electronProducer = cms.InputTag("hltEgammaGsfElectronsUnseeded"),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded"),
    trackProducer = cms.InputTag("hltMergedTracks"),
    useGsfTrack = cms.bool(True),
    useSCRefs = cms.bool(True)
)


process.hltEgammaElectronPixelSeedsUnseeded = cms.EDProducer("ElectronNHitSeedProducer",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    initialSeeds = cms.InputTag("hltElePixelSeedsCombinedUnseeded"),
    matcherConfig = cms.PSet(
        detLayerGeom = cms.ESInputTag("","hltESPGlobalDetLayerGeometry"),
        matchingCuts = cms.VPSet(
            cms.PSet(
                dPhiMaxHighEt = cms.vdouble(0.05),
                dPhiMaxHighEtThres = cms.vdouble(20.0),
                dPhiMaxLowEtGrad = cms.vdouble(-0.002),
                dRZMaxHighEt = cms.vdouble(9999.0),
                dRZMaxHighEtThres = cms.vdouble(0.0),
                dRZMaxLowEtGrad = cms.vdouble(0.0),
                version = cms.int32(2)
            ),
            cms.PSet(
                dPhiMaxHighEt = cms.vdouble(0.003),
                dPhiMaxHighEtThres = cms.vdouble(0.0),
                dPhiMaxLowEtGrad = cms.vdouble(0.0),
                dRZMaxHighEt = cms.vdouble(0.05),
                dRZMaxHighEtThres = cms.vdouble(30.0),
                dRZMaxLowEtGrad = cms.vdouble(-0.002),
                etaBins = cms.vdouble(),
                version = cms.int32(2)
            ),
            cms.PSet(
                dPhiMaxHighEt = cms.vdouble(0.003),
                dPhiMaxHighEtThres = cms.vdouble(0.0),
                dPhiMaxLowEtGrad = cms.vdouble(0.0),
                dRZMaxHighEt = cms.vdouble(0.05),
                dRZMaxHighEtThres = cms.vdouble(30.0),
                dRZMaxLowEtGrad = cms.vdouble(-0.002),
                etaBins = cms.vdouble(),
                version = cms.int32(2)
            )
        ),
        minNrHits = cms.vuint32(2, 3),
        minNrHitsValidLayerBins = cms.vint32(4),
        navSchool = cms.ESInputTag("","SimpleNavigationSchool"),
        paramMagField = cms.ESInputTag("","ParabolicMf"),
        useRecoVertex = cms.bool(False)
    ),
    measTkEvt = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    superClusters = cms.VInputTag("hltEgammaSuperClustersToPixelMatchUnseeded"),
    vertices = cms.InputTag("")
)


process.hltEgammaGsfElectronsUnseeded = cms.EDProducer("EgammaHLTPixelMatchElectronProducers",
    BSProducer = cms.InputTag("hltOnlineBeamSpot"),
    GsfTrackProducer = cms.InputTag("hltEgammaGsfTracksUnseeded"),
    TrackProducer = cms.InputTag(""),
    UseGsfTracks = cms.bool(True)
)


process.hltEgammaGsfTrackVarsBestTrkUnseeded = cms.EDProducer("EgammaHLTGsfTrackVarProducer",
    beamSpotProducer = cms.InputTag("hltOnlineBeamSpot"),
    inputCollection = cms.InputTag("hltEgammaGsfElectronsUnseeded"),
    lowerTrackNrToRemoveCut = cms.int32(-1),
    produceAbsValues = cms.bool(False),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded"),
    upperTrackNrToRemoveCut = cms.int32(9999),
    useDefaultValuesForBarrel = cms.bool(False),
    useDefaultValuesForEndcap = cms.bool(False)
)


process.hltEgammaGsfTracksUnseeded = cms.EDProducer("GsfTrackProducer",
    AlgorithmName = cms.string('gsf'),
    Fitter = cms.string('hltESPGsfElectronFittingSmoother'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string('hltESPMeasurementTracker'),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    Propagator = cms.string('hltESPFwdElectronPropagator'),
    SimpleMagneticField = cms.string(''),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(True),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltEgammaCkfTrackCandidatesForGSFUnseeded"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(False)
)


process.hltEgammaHcalPFClusterIso = cms.EDProducer("EgammaHLTHcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doEffAreaCorrection = cms.bool(False),
    doRhoCorrection = cms.bool(False),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.0),
    drVetoEndcap = cms.double(0.0),
    effectiveAreas = cms.vdouble(0.2, 0.25),
    effectiveAreasCorr = cms.vdouble(0.0, 0.0),
    effectiveAreasThres = cms.vdouble(0.0, 0.0),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducerHCAL = cms.InputTag("hltParticleFlowClusterHCAL"),
    pfClusterProducerHFEM = cms.InputTag(""),
    pfClusterProducerHFHAD = cms.InputTag(""),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidates"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    rhoScale = cms.double(1.0),
    useEt = cms.bool(True),
    useHF = cms.bool(False)
)


process.hltEgammaHcalPFClusterIsoUnseeded = cms.EDProducer("EgammaHLTHcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doEffAreaCorrection = cms.bool(False),
    doRhoCorrection = cms.bool(False),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.0),
    drVetoEndcap = cms.double(0.0),
    effectiveAreas = cms.vdouble(0.2, 0.25),
    effectiveAreasCorr = cms.vdouble(0.0, 0.0),
    effectiveAreasThres = cms.vdouble(0.0, 0.0),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducerHCAL = cms.InputTag("hltParticleFlowClusterHCAL"),
    pfClusterProducerHFEM = cms.InputTag(""),
    pfClusterProducerHFHAD = cms.InputTag(""),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    rhoScale = cms.double(1.0),
    useEt = cms.bool(True),
    useHF = cms.bool(False)
)


process.hltEgammaHollowTrackIsoDr0p2 = cms.EDProducer("EgammaHLTPhotonTrackIsolationProducersRegional",
    countTracks = cms.bool(False),
    egTrkIsoConeSize = cms.double(0.2),
    egTrkIsoPtMin = cms.double(1.0),
    egTrkIsoRSpan = cms.double(999999.0),
    egTrkIsoStripBarrel = cms.double(0.01),
    egTrkIsoStripEndcap = cms.double(0.03),
    egTrkIsoVetoConeSize = cms.double(0.0),
    egTrkIsoZSpan = cms.double(999999.0),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidates"),
    trackProducer = cms.InputTag("hltMergedTracks")
)


process.hltEgammaHoverE = cms.EDProducer("EgammaHLTHcalVarProducerFromRecHit",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    depth = cms.int32(0),
    doEtSum = cms.bool(False),
    doRhoCorrection = cms.bool(False),
    eThresHB = cms.vdouble(0.4, 0.3, 0.3, 0.3),
    eThresHE = cms.vdouble(
        0.1, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2
    ),
    effectiveAreas = cms.vdouble(0.105, 0.17),
    etThresHB = cms.vdouble(0.0, 0.0, 0.0, 0.0),
    etThresHE = cms.vdouble(
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0
    ),
    hbheRecHitsTag = cms.InputTag("hltHbhereco"),
    innerCone = cms.double(0.0),
    maxSeverityHB = cms.int32(9),
    maxSeverityHE = cms.int32(9),
    outerCone = cms.double(0.14),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidates"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    rhoScale = cms.double(1.0),
    usePFThresholdsFromDB = cms.bool(True),
    useSingleTower = cms.bool(False)
)


process.hltEgammaHoverEUnseeded = cms.EDProducer("EgammaHLTHcalVarProducerFromRecHit",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    depth = cms.int32(0),
    doEtSum = cms.bool(False),
    doRhoCorrection = cms.bool(False),
    eThresHB = cms.vdouble(0.4, 0.3, 0.3, 0.3),
    eThresHE = cms.vdouble(
        0.1, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2
    ),
    effectiveAreas = cms.vdouble(0.105, 0.17),
    etThresHB = cms.vdouble(0.0, 0.0, 0.0, 0.0),
    etThresHE = cms.vdouble(
        0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0
    ),
    hbheRecHitsTag = cms.InputTag("hltHbhereco"),
    innerCone = cms.double(0.0),
    maxSeverityHB = cms.int32(9),
    maxSeverityHE = cms.int32(9),
    outerCone = cms.double(0.14),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    rhoScale = cms.double(1.0),
    usePFThresholdsFromDB = cms.bool(True),
    useSingleTower = cms.bool(False)
)


process.hltEgammaPixelMatchVarsUnseeded = cms.EDProducer("EgammaHLTPixelMatchVarProducer",
    dPhi1SParams = cms.PSet(
        bins = cms.VPSet(
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00112, 0.000752, -0.00122, 0.00109),
                funcType = cms.string('TF1:=pol3'),
                xMax = cms.double(1.5),
                xMin = cms.double(0.0),
                yMax = cms.int32(1),
                yMin = cms.int32(1)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00222, 0.000196, -0.000203, 0.000447),
                funcType = cms.string('TF1:=pol3'),
                xMax = cms.double(1.5),
                xMin = cms.double(0.0),
                yMax = cms.int32(2),
                yMin = cms.int32(2)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00236, 0.000691, 0.000199, 0.000416),
                funcType = cms.string('TF1:=pol3'),
                xMax = cms.double(1.5),
                xMin = cms.double(0.0),
                yMax = cms.int32(99999),
                yMin = cms.int32(3)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00823, -0.0029),
                funcType = cms.string('TF1:=pol1'),
                xMax = cms.double(2.0),
                xMin = cms.double(1.5),
                yMax = cms.int32(1),
                yMin = cms.int32(1)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00282),
                funcType = cms.string('TF1:=pol0'),
                xMax = cms.double(3.0),
                xMin = cms.double(2.0),
                yMax = cms.int32(1),
                yMin = cms.int32(1)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.010838, -0.00345),
                funcType = cms.string('TF1:=pol1'),
                xMax = cms.double(2.0),
                xMin = cms.double(1.5),
                yMax = cms.int32(2),
                yMin = cms.int32(2)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.0043),
                funcType = cms.string('TF1:=pol0'),
                xMax = cms.double(3.0),
                xMin = cms.double(2.0),
                yMax = cms.int32(2),
                yMin = cms.int32(2)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.0208, -0.0125, 0.00231),
                funcType = cms.string('TF1:=pol2'),
                xMax = cms.double(3.0),
                xMin = cms.double(1.5),
                yMax = cms.int32(99999),
                yMin = cms.int32(3)
            )
        )
    ),
    dPhi2SParams = cms.PSet(
        bins = cms.VPSet(
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00013),
                funcType = cms.string('TF1:=pol0'),
                xMax = cms.double(1.6),
                xMin = cms.double(0.0),
                yMax = cms.int32(99999),
                yMin = cms.int32(1)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00045, -0.000199),
                funcType = cms.string('TF1:=pol1'),
                xMax = cms.double(1.9),
                xMin = cms.double(1.5),
                yMax = cms.int32(99999),
                yMin = cms.int32(1)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(7.94e-05),
                funcType = cms.string('TF1:=pol0'),
                xMax = cms.double(3.0),
                xMin = cms.double(1.9),
                yMax = cms.int32(99999),
                yMin = cms.int32(1)
            )
        )
    ),
    dRZ2SParams = cms.PSet(
        bins = cms.VPSet(
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.00299, 0.000299, -4.13e-06, 0.00191),
                funcType = cms.string('TF1:=pol3'),
                xMax = cms.double(1.5),
                xMin = cms.double(0.0),
                yMax = cms.int32(99999),
                yMin = cms.int32(1)
            ),
            cms.PSet(
                binType = cms.string('AbsEtaClus'),
                funcParams = cms.vdouble(0.248, -0.329, 0.148, -0.0222),
                funcType = cms.string('TF1:=pol3'),
                xMax = cms.double(3.0),
                xMin = cms.double(1.5),
                yMax = cms.int32(99999),
                yMin = cms.int32(1)
            )
        )
    ),
    pixelSeedsProducer = cms.InputTag("hltEgammaElectronPixelSeedsUnseeded"),
    productsToWrite = cms.int32(0),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded")
)


process.hltEgammaR9ID = cms.EDProducer("EgammaHLTR9IDProducer",
    ecalRechitEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    ecalRechitEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidates")
)


process.hltEgammaR9IDUnseeded = cms.EDProducer("EgammaHLTR9IDProducer",
    ecalRechitEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    ecalRechitEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    recoEcalCandidateProducer = cms.InputTag("hltEgammaCandidatesUnseeded")
)


process.hltEgammaSuperClustersToPixelMatchUnseeded = cms.EDProducer("EgammaHLTFilteredSuperClusterProducer",
    cands = cms.InputTag("hltEgammaCandidatesUnseeded"),
    cuts = cms.VPSet(cms.PSet(
        barrelCut = cms.PSet(
            cutOverE = cms.double(0.2),
            useEt = cms.bool(False)
        ),
        endcapCut = cms.PSet(
            cutOverE = cms.double(0.2),
            useEt = cms.bool(False)
        ),
        var = cms.InputTag("hltEgammaHoverEUnseeded")
    )),
    minEtCutEB = cms.double(0.0),
    minEtCutEE = cms.double(0.0)
)


process.hltElePixelHitDoubletsForTripletsUnseeded = cms.EDProducer("HitPairEDProducer",
    clusterCheck = cms.InputTag(""),
    layerPairs = cms.vuint32(0, 1),
    maxElement = cms.uint32(0),
    maxElementTotal = cms.uint32(50000000),
    produceIntermediateHitDoublets = cms.bool(True),
    produceSeedingHitSets = cms.bool(False),
    putEmptyIfMaxElementReached = cms.bool(False),
    seedingLayers = cms.InputTag("hltPixelLayerTriplets"),
    trackingRegions = cms.InputTag("hltEleSeedsTrackingRegionsUnseeded"),
    trackingRegionsSeedingLayers = cms.InputTag("")
)


process.hltElePixelHitDoubletsUnseeded = cms.EDProducer("HitPairEDProducer",
    clusterCheck = cms.InputTag(""),
    layerPairs = cms.vuint32(0),
    maxElement = cms.uint32(0),
    maxElementTotal = cms.uint32(50000000),
    produceIntermediateHitDoublets = cms.bool(False),
    produceSeedingHitSets = cms.bool(True),
    putEmptyIfMaxElementReached = cms.bool(False),
    seedingLayers = cms.InputTag("hltPixelLayerPairs"),
    trackingRegions = cms.InputTag("hltEleSeedsTrackingRegionsUnseeded"),
    trackingRegionsSeedingLayers = cms.InputTag("")
)


process.hltElePixelHitTripletsUnseeded = cms.EDProducer("CAHitTripletEDProducer",
    CAHardPtCut = cms.double(0.3),
    CAPhiCut = cms.double(0.1),
    CAPhiCut_byTriplets = cms.VPSet(cms.PSet(
        cut = cms.double(-1.0),
        seedingLayers = cms.string('')
    )),
    CAThetaCut = cms.double(0.004),
    CAThetaCut_byTriplets = cms.VPSet(cms.PSet(
        cut = cms.double(-1.0),
        seedingLayers = cms.string('')
    )),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    doublets = cms.InputTag("hltElePixelHitDoubletsForTripletsUnseeded"),
    extraHitRPhitolerance = cms.double(0.032),
    maxChi2 = cms.PSet(
        enabled = cms.bool(True),
        pt1 = cms.double(0.8),
        pt2 = cms.double(8.0),
        value1 = cms.double(100.0),
        value2 = cms.double(6.0)
    ),
    useBendingCorrection = cms.bool(True)
)


process.hltElePixelSeedsCombinedUnseeded = cms.EDProducer("SeedCombiner",
    clusterRemovalInfos = cms.VInputTag(),
    seedCollections = cms.VInputTag("hltElePixelSeedsDoubletsUnseeded", "hltElePixelSeedsTripletsUnseeded")
)


process.hltElePixelSeedsDoubletsUnseeded = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    seedingHitSets = cms.InputTag("hltElePixelHitDoubletsUnseeded")
)


process.hltElePixelSeedsTripletsUnseeded = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    seedingHitSets = cms.InputTag("hltElePixelHitTripletsUnseeded")
)


process.hltEleSeedsTrackingRegionsUnseeded = cms.EDProducer("TrackingRegionsFromSuperClustersEDProducer",
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        defaultZ = cms.double(0.0),
        deltaEtaRegion = cms.double(0.1),
        deltaPhiRegion = cms.double(0.4),
        measurementTrackerEvent = cms.InputTag(""),
        minBSDeltaZ = cms.double(0.0),
        nrSigmaForBSDeltaZ = cms.double(4.0),
        originHalfLength = cms.double(12.5),
        originRadius = cms.double(0.05),
        precise = cms.bool(True),
        ptMin = cms.double(1.5),
        superClusters = cms.VInputTag("hltEgammaSuperClustersToPixelMatchUnseeded"),
        useZInBeamspot = cms.bool(False),
        useZInVertex = cms.bool(False),
        vertices = cms.InputTag(""),
        whereToUseMeasTracker = cms.string('kNever')
    )
)


process.hltFEDSelectorL1 = cms.EDProducer("EvFFEDSelector",
    fedList = cms.vuint32(1404),
    inputTag = cms.InputTag("rawDataCollector")
)


process.hltFixedGridRhoFastjetAll = cms.EDProducer("FixedGridRhoProducerFastjet",
    gridSpacing = cms.double(0.55),
    maxRapidity = cms.double(5.0),
    pfCandidatesTag = cms.InputTag("hltParticleFlow")
)


process.hltFixedGridRhoFastjetAllCalo = cms.EDProducer("FixedGridRhoProducerFastjet",
    gridSpacing = cms.double(0.55),
    maxRapidity = cms.double(5.0),
    pfCandidatesTag = cms.InputTag("hltTowerMakerForAll")
)


process.hltFixedGridRhoFastjetAllCaloForMuons = cms.EDProducer("FixedGridRhoProducerFastjetFromRecHit",
    eThresHB = cms.vdouble(0.4, 0.3, 0.3, 0.3),
    eThresHE = cms.vdouble(
        0.1, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2
    ),
    ebRecHitsTag = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    eeRecHitsTag = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    gridSpacing = cms.double(0.55),
    hbheRecHitsTag = cms.InputTag("hltHbhereco"),
    maxRapidity = cms.double(2.5),
    skipECAL = cms.bool(False),
    skipHCAL = cms.bool(False),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltFixedGridRhoFastjetECALMFForMuons = cms.EDProducer("FixedGridRhoProducerFastjetFromRecHit",
    eThresHB = cms.vdouble(0.4, 0.3, 0.3, 0.3),
    eThresHE = cms.vdouble(
        0.1, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2
    ),
    ebRecHitsTag = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    eeRecHitsTag = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    gridSpacing = cms.double(0.55),
    hbheRecHitsTag = cms.InputTag("hltHbhereco"),
    maxRapidity = cms.double(2.5),
    skipECAL = cms.bool(False),
    skipHCAL = cms.bool(True),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltFixedGridRhoFastjetHCAL = cms.EDProducer("FixedGridRhoProducerFastjetFromRecHit",
    eThresHB = cms.vdouble(0.4, 0.3, 0.3, 0.3),
    eThresHE = cms.vdouble(
        0.1, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2
    ),
    ebRecHitsTag = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    eeRecHitsTag = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    gridSpacing = cms.double(0.55),
    hbheRecHitsTag = cms.InputTag("hltHbhereco"),
    maxRapidity = cms.double(2.5),
    skipECAL = cms.bool(True),
    skipHCAL = cms.bool(False),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltGemRecHits = cms.EDProducer("GEMRecHitProducer",
    applyMasking = cms.bool(True),
    ge21Off = cms.bool(False),
    gemDigiLabel = cms.InputTag("hltMuonGEMDigis"),
    recAlgo = cms.string('GEMRecHitStandardAlgo'),
    recAlgoConfig = cms.PSet(

    )
)


process.hltGemSegments = cms.EDProducer("GEMSegmentProducer",
    algo_name = cms.string('GEMSegmentAlgorithm'),
    algo_pset = cms.PSet(
        clusterOnlySameBXRecHits = cms.bool(True),
        dEtaChainBoxMax = cms.double(0.05),
        dPhiChainBoxMax = cms.double(0.02),
        dXclusBoxMax = cms.double(1.0),
        dYclusBoxMax = cms.double(5.0),
        maxRecHitsInCluster = cms.int32(4),
        minHitsPerSegment = cms.uint32(2),
        preClustering = cms.bool(True),
        preClusteringUseChaining = cms.bool(True)
    ),
    enableGE0 = cms.bool(True),
    enableGE12 = cms.bool(False),
    ge0_name = cms.string('GE0SegAlgoRU'),
    ge0_pset = cms.PSet(
        allowWideSegments = cms.bool(True),
        doCollisions = cms.bool(True),
        maxChi2Additional = cms.double(100.0),
        maxChi2GoodSeg = cms.double(50.0),
        maxChi2Prune = cms.double(50.0),
        maxETASeeds = cms.double(0.1),
        maxNumberOfHits = cms.uint32(300),
        maxNumberOfHitsPerLayer = cms.uint32(100),
        maxPhiAdditional = cms.double(0.001096605744),
        maxPhiSeeds = cms.double(0.001096605744),
        maxTOFDiff = cms.double(25.0),
        minNumberOfHits = cms.uint32(4),
        requireCentralBX = cms.bool(True)
    ),
    gemRecHitLabel = cms.InputTag("hltGemRecHits")
)


process.hltGtStage2Digis = cms.EDProducer("L1TRawToDigi",
    CTP7 = cms.untracked.bool(False),
    DmxFWId = cms.uint32(0),
    FWId = cms.uint32(0),
    FWOverride = cms.bool(False),
    FedIds = cms.vint32(1404),
    InputLabel = cms.InputTag("rawDataCollector"),
    MTF7 = cms.untracked.bool(False),
    MinFeds = cms.uint32(0),
    Setup = cms.string('stage2::GTSetup'),
    TMTCheck = cms.bool(True),
    debug = cms.untracked.bool(False),
    lenAMC13Header = cms.untracked.int32(8),
    lenAMC13Trailer = cms.untracked.int32(8),
    lenAMCHeader = cms.untracked.int32(8),
    lenAMCTrailer = cms.untracked.int32(0),
    lenSlinkHeader = cms.untracked.int32(8),
    lenSlinkTrailer = cms.untracked.int32(8)
)


process.hltGtStage2ObjectMap = cms.EDProducer("L1TGlobalProducer",
    AlgoBlkInputTag = cms.InputTag("hltGtStage2Digis"),
    AlgorithmTriggersUnmasked = cms.bool(True),
    AlgorithmTriggersUnprescaled = cms.bool(True),
    AlternativeNrBxBoardDaq = cms.uint32(0),
    BstLengthBytes = cms.int32(-1),
    CICADAInputTag = cms.InputTag("hltGtStage2Digis","CICADAScore"),
    EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    EmulateBxInEvent = cms.int32(1),
    EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    ExtInputTag = cms.InputTag("hltGtStage2Digis"),
    GetPrescaleColumnFromData = cms.bool(False),
    JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1DataBxInEvent = cms.int32(5),
    MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    PrescaleSet = cms.uint32(1),
    PrintL1Menu = cms.untracked.bool(False),
    ProduceL1GtDaqRecord = cms.bool(True),
    ProduceL1GtObjectMapRecord = cms.bool(True),
    RequireMenuToMatchAlgoBlkInput = cms.bool(True),
    TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    TriggerMenuLuminosity = cms.string('startup'),
    Verbosity = cms.untracked.int32(0),
    produceAXOL1TLScore = cms.bool(False),
    resetPSCountersEachLumiSec = cms.bool(True),
    semiRandomInitialPSCounters = cms.bool(False),
    useMuonShowers = cms.bool(True)
)


process.hltHbheRecoSoA = cms.EDProducer("HBHERecHitProducerPortable@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    applyTimeSlew = cms.bool(True),
    digisLabelF01HE = cms.InputTag("hltHcalDigisSoA","f01HEDigis"),
    digisLabelF3HB = cms.InputTag("hltHcalDigisSoA","f3HBDigis"),
    digisLabelF5HB = cms.InputTag("hltHcalDigisSoA","f5HBDigis"),
    firstSampleShift = cms.int32(0),
    kernelMinimizeThreads = cms.vuint32(16, 1, 1),
    kprep1dChannelsPerBlock = cms.uint32(32),
    maxTimeSamples = cms.uint32(10),
    meanTime = cms.double(0.0),
    pulseOffsets = cms.vint32(
        -3, -2, -1, 0, 1,
        2, 3, 4
    ),
    recHitsLabelM0HBHE = cms.string(''),
    sipmQNTStoSum = cms.int32(3),
    sipmQTSShift = cms.int32(0),
    slopeTimeSlewParameters = cms.vdouble(-3.178648, -1.5610227, -1.075824),
    timeSigmaHPD = cms.double(5.0),
    timeSigmaSiPM = cms.double(2.5),
    tmaxTimeSlewParameters = cms.vdouble(16.0, 10.0, 6.25),
    ts4Thresh = cms.double(0.0),
    tzeroTimeSlewParameters = cms.vdouble(23.960177, 11.977461, 9.109694),
    useEffectivePedestals = cms.bool(True)
)


process.hltHbhereco = cms.EDProducer("HcalRecHitSoAToLegacy",
    src = cms.InputTag("hltHbheRecoSoA")
)


process.hltHcalDigis = cms.EDProducer("HcalRawToDigi",
    ComplainEmptyData = cms.untracked.bool(False),
    ElectronicsMap = cms.string(''),
    ExpectedOrbitMessageTime = cms.untracked.int32(-1),
    FEDs = cms.untracked.vint32(),
    FilterDataQuality = cms.bool(True),
    HcalFirstFED = cms.untracked.int32(700),
    InputLabel = cms.InputTag("rawDataCollector"),
    UnpackCalib = cms.untracked.bool(True),
    UnpackTTP = cms.untracked.bool(False),
    UnpackUMNio = cms.untracked.bool(True),
    UnpackZDC = cms.untracked.bool(True),
    UnpackerMode = cms.untracked.int32(0),
    firstSample = cms.int32(0),
    lastSample = cms.int32(9),
    saveQIE10DataNSamples = cms.untracked.vint32(),
    saveQIE10DataTags = cms.untracked.vstring(),
    saveQIE11DataNSamples = cms.untracked.vint32(),
    saveQIE11DataTags = cms.untracked.vstring(),
    silent = cms.untracked.bool(True)
)


process.hltHcalDigisSoA = cms.EDProducer("HcalDigisSoAProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    digisLabelF01HE = cms.string('f01HEDigis'),
    digisLabelF3HB = cms.string('f3HBDigis'),
    digisLabelF5HB = cms.string('f5HBDigis'),
    hbheDigisLabel = cms.InputTag("hltHcalDigis"),
    maxChannelsF01HE = cms.uint32(10000),
    maxChannelsF3HB = cms.uint32(10000),
    maxChannelsF5HB = cms.uint32(10000),
    qie11DigiLabel = cms.InputTag("hltHcalDigis")
)


process.hltHfprereco = cms.EDProducer("HFPreReconstructor",
    digiLabel = cms.InputTag("hltHcalDigis"),
    dropZSmarkedPassed = cms.bool(True),
    forceSOI = cms.int32(-1),
    soiShift = cms.int32(0),
    sumAllTimeSlices = cms.bool(False),
    tsFromDB = cms.bool(False)
)


process.hltHfreco = cms.EDProducer("HFPhase1Reconstructor",
    HFStripFilter = cms.PSet(
        gap = cms.int32(2),
        lstrips = cms.int32(2),
        maxStripTime = cms.double(10.0),
        maxThreshold = cms.double(100.0),
        seedHitIetaMax = cms.int32(35),
        stripThreshold = cms.double(40.0),
        timeMax = cms.double(6.0),
        verboseLevel = cms.untracked.int32(10),
        wedgeCut = cms.double(0.05)
    ),
    PETstat = cms.PSet(
        HcalAcceptSeverityLevel = cms.int32(9),
        longETParams = cms.vdouble(
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ),
        longEnergyParams = cms.vdouble(
            43.5, 45.7, 48.32, 51.36, 54.82,
            58.7, 63.0, 67.72, 72.86, 78.42,
            84.4, 90.8, 97.62
        ),
        long_R = cms.vdouble(0.98),
        long_R_29 = cms.vdouble(0.8),
        shortETParams = cms.vdouble(
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ),
        shortEnergyParams = cms.vdouble(
            35.1773, 35.37, 35.7933, 36.4472, 37.3317,
            38.4468, 39.7925, 41.3688, 43.1757, 45.2132,
            47.4813, 49.98, 52.7093
        ),
        short_R = cms.vdouble(0.8),
        short_R_29 = cms.vdouble(0.8)
    ),
    S8S1stat = cms.PSet(
        HcalAcceptSeverityLevel = cms.int32(9),
        isS8S1 = cms.bool(True),
        longETParams = cms.vdouble(
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ),
        longEnergyParams = cms.vdouble(
            40.0, 100.0, 100.0, 100.0, 100.0,
            100.0, 100.0, 100.0, 100.0, 100.0,
            100.0, 100.0, 100.0
        ),
        long_optimumSlope = cms.vdouble(
            0.3, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1
        ),
        shortETParams = cms.vdouble(
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ),
        shortEnergyParams = cms.vdouble(
            40.0, 100.0, 100.0, 100.0, 100.0,
            100.0, 100.0, 100.0, 100.0, 100.0,
            100.0, 100.0, 100.0
        ),
        short_optimumSlope = cms.vdouble(
            0.3, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1, 0.1, 0.1,
            0.1, 0.1, 0.1
        )
    ),
    S9S1stat = cms.PSet(
        HcalAcceptSeverityLevel = cms.int32(9),
        isS8S1 = cms.bool(False),
        longETParams = cms.vdouble(
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ),
        longEnergyParams = cms.vdouble(
            43.5, 45.7, 48.32, 51.36, 54.82,
            58.7, 63.0, 67.72, 72.86, 78.42,
            84.4, 90.8, 97.62
        ),
        long_optimumSlope = cms.vdouble(
            -99999.0, 0.0164905, 0.0238698, 0.0321383, 0.041296,
            0.0513428, 0.0622789, 0.0741041, 0.0868186, 0.100422,
            0.135313, 0.136289, 0.0589927
        ),
        shortETParams = cms.vdouble(
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0
        ),
        shortEnergyParams = cms.vdouble(
            35.1773, 35.37, 35.7933, 36.4472, 37.3317,
            38.4468, 39.7925, 41.3688, 43.1757, 45.2132,
            47.4813, 49.98, 52.7093
        ),
        short_optimumSlope = cms.vdouble(
            -99999.0, 0.0164905, 0.0238698, 0.0321383, 0.041296,
            0.0513428, 0.0622789, 0.0741041, 0.0868186, 0.100422,
            0.135313, 0.136289, 0.0589927
        )
    ),
    algoConfigClass = cms.string('HFPhase1PMTParams'),
    algorithm = cms.PSet(
        Class = cms.string('HFFlexibleTimeCheck'),
        energyWeights = cms.vdouble(
            1.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 2.0, 0.0, 2.0, 0.0,
            2.0, 0.0, 1.0, 0.0, 0.0,
            1.0, 0.0, 1.0, 0.0, 2.0,
            0.0, 2.0, 0.0, 2.0, 0.0,
            1.0
        ),
        rejectAllFailures = cms.bool(True),
        soiPhase = cms.uint32(1),
        tfallIfNoTDC = cms.double(-101.0),
        timeShift = cms.double(0.0),
        tlimits = cms.vdouble(-1000.0, 1000.0, -1000.0, 1000.0),
        triseIfNoTDC = cms.double(-100.0)
    ),
    checkChannelQualityForDepth3and4 = cms.bool(False),
    inputLabel = cms.InputTag("hltHfprereco"),
    runHFStripFilter = cms.bool(False),
    setNoiseFlags = cms.bool(True),
    useChannelQualityFromDB = cms.bool(False)
)


process.hltHoreco = cms.EDProducer("HcalHitReconstructor",
    HFInWindowStat = cms.PSet(

    ),
    PETstat = cms.PSet(

    ),
    S8S1stat = cms.PSet(

    ),
    S9S1stat = cms.PSet(

    ),
    Subdetector = cms.string('HO'),
    correctForPhaseContainment = cms.bool(True),
    correctForTimeslew = cms.bool(True),
    correctTiming = cms.bool(False),
    correctionPhaseNS = cms.double(13.0),
    dataOOTCorrectionCategory = cms.string('Data'),
    dataOOTCorrectionName = cms.string(''),
    digiLabel = cms.InputTag("hltHcalDigis"),
    digiTimeFromDB = cms.bool(True),
    digistat = cms.PSet(

    ),
    dropZSmarkedPassed = cms.bool(True),
    firstAuxTS = cms.int32(4),
    firstSample = cms.int32(4),
    hfTimingTrustParameters = cms.PSet(

    ),
    mcOOTCorrectionCategory = cms.string('MC'),
    mcOOTCorrectionName = cms.string(''),
    recoParamsFromDB = cms.bool(True),
    samplesToAdd = cms.int32(4),
    saturationParameters = cms.PSet(
        maxADCvalue = cms.int32(127)
    ),
    setNegativeFlags = cms.bool(False),
    setNoiseFlags = cms.bool(False),
    setSaturationFlags = cms.bool(False),
    setTimingTrustFlags = cms.bool(False),
    tsFromDB = cms.bool(True),
    useLeakCorrection = cms.bool(False)
)


process.hltIter03IterL3FromL1MuonMerged = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity", "hltIter3IterL3FromL1MuonTrackSelectionHighPurity"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity", "hltIter3IterL3FromL1MuonTrackSelectionHighPurity"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltIter0IterL3FromL1MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('none'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(True),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered"),
    useHitsSplitting = cms.bool(True)
)


process.hltIter0IterL3FromL1MuonCkfTrackCandidatesNoVtx = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('none'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(True),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx"),
    useHitsSplitting = cms.bool(True)
)


process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3FromL1MuonCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0IterL3FromL1MuonCtfWithMaterialTracksNoVtx = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3FromL1MuonCkfTrackCandidatesNoVtx"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracksInRegionL1"),
    InputVertexCollection = cms.InputTag(""),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
    L1Muon = cms.InputTag("hltGtStage2Digis","Muon"),
    L2Muon = cms.InputTag("hltL2MuonCandidates"),
    baseScore = cms.double(0.5),
    doSort = cms.bool(False),
    etaEdge = cms.double(1.2),
    isFromL1 = cms.bool(True),
    minL1Qual = cms.int32(7),
    mvaCutB = cms.double(0.04),
    mvaCutE = cms.double(0.04),
    mvaFileB = cms.FileInPath('RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3.xml'),
    mvaFileE = cms.FileInPath('RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3.xml'),
    mvaScaleMeanB = cms.vdouble(
        0.0003999966523561405, 1.5340202670472034e-05, 2.6710290157638425e-05, 0.0005978116313043455, 0.0049135275917734636,
        3.4305653488182246e-05, 0.24525118734715307, -0.0024635178849904426
    ),
    mvaScaleMeanE = cms.vdouble(
        0.0003017047347441654, 9.077959353128816e-05, 0.00027101609045025927, 0.004557390407735609, -0.020781128525626812,
        0.0009286198943080588, 0.26674085200387376, -0.002971698676536822
    ),
    mvaScaleStdB = cms.vdouble(
        0.0007666933596884494, 0.015685297920984408, 0.026294325262867256, 0.07665283880432934, 0.834879854164998,
        0.5397258722194461, 0.2807075832224741, 0.32820882609116625
    ),
    mvaScaleStdE = cms.vdouble(
        0.0008125341035878315, 0.19268436761240013, 0.579019516987623, 0.3222327708969556, 1.0567488273501275,
        0.2648980106841699, 0.30889713721141826, 0.3593729790466801
    ),
    nSeedsMaxB = cms.int32(99999),
    nSeedsMaxE = cms.int32(99999),
    rejectAll = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks")
)


process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracksInRegionL1NoVtx"),
    InputVertexCollection = cms.InputTag(""),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0IterL3FromL1MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 4),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0IterL3FromL1MuonCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 4),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0IterL3FromL1MuonCtfWithMaterialTracksNoVtx"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0IterL3FromL1MuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0IterL3FromL1MuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter0IterL3FromL1MuonCtfWithMaterialTracks")
)


process.hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx","QualityMasks"),
    originalSource = cms.InputTag("hltIter0IterL3FromL1MuonCtfWithMaterialTracksNoVtx")
)


process.hltIter0IterL3MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('none'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3MuonPSetGroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(True),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered"),
    useHitsSplitting = cms.bool(True)
)


process.hltIter0IterL3MuonCkfTrackCandidatesNoVtx = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('none'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0IterL3MuonPSetGroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(True),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx"),
    useHitsSplitting = cms.bool(True)
)


process.hltIter0IterL3MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3MuonCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0IterL3MuonCtfWithMaterialTracksNoVtx = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3MuonCkfTrackCandidatesNoVtx"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0IterL3MuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracksInRegionL2"),
    InputVertexCollection = cms.InputTag(""),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
    L1Muon = cms.InputTag("hltGtStage2Digis","Muon"),
    L2Muon = cms.InputTag("hltL2MuonCandidates"),
    baseScore = cms.double(0.5),
    doSort = cms.bool(False),
    etaEdge = cms.double(1.2),
    isFromL1 = cms.bool(False),
    minL1Qual = cms.int32(7),
    mvaCutB = cms.double(0.04),
    mvaCutE = cms.double(0.04),
    mvaFileB = cms.FileInPath('RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_barrel_v3.xml'),
    mvaFileE = cms.FileInPath('RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_endcap_v3.xml'),
    mvaScaleMeanB = cms.vdouble(
        0.0004332629261558539, 4.689795312031938e-06, 7.644844964566431e-06, 0.0006580623848546099, 0.00523266117445817,
        0.00056968993532947, 0.20322471101222087, -0.005575351463397025, 0.18247595248098955, 0.00015342398341020196
    ),
    mvaScaleMeanE = cms.vdouble(
        0.0003120747098810717, 4.5298701434656295e-06, 1.2002076996572005e-05, 0.007900535887258366, -0.022166389143849694,
        0.000712338927507459, 0.22819667672872926, -0.0039375694144792705, 0.19304371973554835, -1.2936058928324214e-05
    ),
    mvaScaleStdB = cms.vdouble(
        0.0007444819891335438, 0.0014335177986615237, 0.003503839482232683, 0.07764362324530726, 0.8223406268068466,
        0.6392468338330071, 0.2405783807668161, 0.2904161358810494, 0.21887441827342669, 0.27045195352036544
    ),
    mvaScaleStdE = cms.vdouble(
        0.0006302274350028021, 0.0013138279991871378, 0.004880335178644773, 0.32509543981045624, 0.9449952711981982,
        0.279802349646327, 0.3193063648341999, 0.3334815828876066, 0.22528017441813106, 0.2822750719936266
    ),
    nSeedsMaxB = cms.int32(99999),
    nSeedsMaxE = cms.int32(99999),
    rejectAll = cms.bool(False),
    src = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracks")
)


process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracksInRegionL2NoVtx"),
    InputVertexCollection = cms.InputTag(""),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0IterL3MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 4),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0IterL3MuonCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0IterL3MuonTrackCutClassifierNoVtx = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 4),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0IterL3MuonCtfWithMaterialTracksNoVtx"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0IterL3MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0IterL3MuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0IterL3MuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter0IterL3MuonCtfWithMaterialTracks")
)


process.hltIter0IterL3MuonTrackSelectionHighPurityNoVtx = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0IterL3MuonTrackCutClassifierNoVtx","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0IterL3MuonTrackCutClassifierNoVtx","QualityMasks"),
    originalSource = cms.InputTag("hltIter0IterL3MuonCtfWithMaterialTracksNoVtx")
)


process.hltIter0L3MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0GroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(False),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter0L3MuonPixelSeedsFromPixelTracks"),
    useHitsSplitting = cms.bool(False)
)


process.hltIter0L3MuonCkfTrackCandidatesNoVtx = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter0GroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(False),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx"),
    useHitsSplitting = cms.bool(False)
)


process.hltIter0L3MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0L3MuonCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0L3MuonCtfWithMaterialTracksNoVtx = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0L3MuonCkfTrackCandidatesNoVtx"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0L3MuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracksInRegionIter0L3Muon"),
    InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracksInRegionIter0L3MuonNoVtx"),
    InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0L3MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 0.003),
            d0err_par = cms.vdouble(0.001, 0.001, 0.001),
            dr_exp = cms.vint32(4, 4, 4),
            dr_par1 = cms.vdouble(3.40282346639e+38, 0.8, 0.8),
            dr_par2 = cms.vdouble(3.40282346639e+38, 0.6, 0.6)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 4),
            dz_par1 = cms.vdouble(3.40282346639e+38, 0.75, 0.75),
            dz_par2 = cms.vdouble(3.40282346639e+38, 0.5, 0.5)
        ),
        maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 3),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0L3MuonCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0L3MuonTrackCutClassifierNoVtx = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 0.003),
            d0err_par = cms.vdouble(0.001, 0.001, 0.001),
            dr_exp = cms.vint32(4, 4, 4),
            dr_par1 = cms.vdouble(3.40282346639e+38, 0.8, 0.8),
            dr_par2 = cms.vdouble(3.40282346639e+38, 0.6, 0.6)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 4),
            dz_par1 = cms.vdouble(3.40282346639e+38, 0.75, 0.75),
            dz_par2 = cms.vdouble(3.40282346639e+38, 0.5, 0.5)
        ),
        maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 3),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0L3MuonCtfWithMaterialTracksNoVtx"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0L3MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0L3MuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0L3MuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter0L3MuonCtfWithMaterialTracks")
)


process.hltIter0L3MuonTrackSelectionHighPurityNoVtx = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0L3MuonTrackCutClassifierNoVtx","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0L3MuonTrackCutClassifierNoVtx","QualityMasks"),
    originalSource = cms.InputTag("hltIter0L3MuonCtfWithMaterialTracksNoVtx")
)


process.hltIter0PFLowPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection = cms.InputTag("hltPixelTracks"),
    InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
    SeedCreatorPSet = cms.PSet(
        refToPSet_ = cms.string('HLTSeedFromProtoTracks')
    ),
    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    includeFourthHit = cms.bool(True),
    originHalfLength = cms.double(0.3),
    originRadius = cms.double(0.1),
    produceComplement = cms.bool(False),
    useEventsWithNoVertex = cms.bool(True),
    usePV = cms.bool(False),
    useProtoTrackKinematics = cms.bool(False)
)


process.hltIter0PFlowCkfTrackCandidates = cms.EDProducer("MkFitOutputConverter",
    batchSize = cms.int32(16),
    candMVASel = cms.bool(False),
    candWP = cms.double(0.0),
    doErrorRescale = cms.bool(True),
    mkFitEventOfHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitEventOfHits"),
    mkFitPixelHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits"),
    mkFitSeeds = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSeeds"),
    mkFitStripHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits"),
    propagatorAlong = cms.ESInputTag("","PropagatorWithMaterialParabolicMf"),
    propagatorOpposite = cms.ESInputTag("","PropagatorWithMaterialParabolicMfOpposite"),
    qualityMaxInvPt = cms.double(100.0),
    qualityMaxPosErr = cms.double(100.0),
    qualityMaxR = cms.double(120.0),
    qualityMaxZ = cms.double(280.0),
    qualityMinTheta = cms.double(0.01),
    qualitySignPt = cms.bool(True),
    seeds = cms.InputTag("hltIter0PFLowPixelSeedsFromPixelTracks"),
    tfDnnLabel = cms.string('trackSelectionTf'),
    tracks = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFit"),
    ttrhBuilder = cms.ESInputTag("","hltESPTTRHBWithTrackAngle")
)


process.hltIter0PFlowCkfTrackCandidatesMkFit = cms.EDProducer("MkFitProducer",
    backwardFitInCMSSW = cms.bool(False),
    buildingRoutine = cms.string('cloneEngine'),
    clustersToSkip = cms.InputTag(""),
    config = cms.ESInputTag("","hltESPIter0PFlowTrackCandidatesMkFitConfig"),
    eventOfHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitEventOfHits"),
    limitConcurrency = cms.untracked.bool(False),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    mkFitSilent = cms.untracked.bool(True),
    pixelHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits"),
    removeDuplicates = cms.bool(True),
    seedCleaning = cms.bool(True),
    seeds = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSeeds"),
    stripHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits")
)


process.hltIter0PFlowCkfTrackCandidatesMkFitEventOfHits = cms.EDProducer("MkFitEventOfHitsProducer",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    pixelHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits"),
    stripHits = cms.InputTag("hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits"),
    usePixelQualityDB = cms.bool(True),
    useStripStripQualityDB = cms.bool(True)
)


process.hltIter0PFlowCkfTrackCandidatesMkFitSeeds = cms.EDProducer("MkFitSeedConverter",
    maxNSeeds = cms.uint32(500000),
    seeds = cms.InputTag("hltIter0PFLowPixelSeedsFromPixelTracks"),
    ttrhBuilder = cms.ESInputTag("","hltESPTTRHBWithTrackAngle")
)


process.hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits = cms.EDProducer("MkFitSiPixelHitConverter",
    clusters = cms.InputTag("hltSiPixelClusters"),
    hits = cms.InputTag("hltSiPixelRecHits"),
    ttrhBuilder = cms.ESInputTag("","hltESPTTRHBWithTrackAngle")
)


process.hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits = cms.EDProducer("MkFitSiStripHitConverter",
    clusters = cms.InputTag("hltSiStripRawToClustersFacility"),
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    rphiHits = cms.InputTag("hltSiStripRecHits","rphiRecHit"),
    stereoHits = cms.InputTag("hltSiStripRecHits","stereoRecHit"),
    ttrhBuilder = cms.ESInputTag("","hltESPTTRHBWithTrackAngle")
)


process.hltIter0PFlowCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter0'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEvent"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter0PFlowCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter0PFlowTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 0.003),
            d0err_par = cms.vdouble(0.001, 0.001, 0.001),
            dr_exp = cms.vint32(4, 4, 4),
            dr_par1 = cms.vdouble(3.40282346639e+38, 0.6, 0.6),
            dr_par2 = cms.vdouble(3.40282346639e+38, 0.45, 0.45)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 4),
            dz_par1 = cms.vdouble(3.40282346639e+38, 0.6, 0.6),
            dz_par2 = cms.vdouble(3.40282346639e+38, 0.51, 0.51)
        ),
        maxChi2 = cms.vdouble(999.0, 25.0, 99.0),
        maxChi2n = cms.vdouble(1.2, 1.0, 999.0),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 3),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter0PFlowCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter0PFlowTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter0PFlowTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter0PFlowTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter0PFlowCtfWithMaterialTracks")
)


process.hltIter3IterL3FromL1MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTIter2GroupedCkfTrajectoryBuilderIT')
    ),
    TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(False),
    maxNSeeds = cms.uint32(100000),
    maxSeedsBeforeCleaning = cms.uint32(1000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(False),
    src = cms.InputTag("hltIter3IterL3FromL1MuonPixelSeedsFiltered"),
    useHitsSplitting = cms.bool(False)
)


process.hltIter3IterL3FromL1MuonClustersRefRemoval = cms.EDProducer("TrackClusterRemover",
    TrackQuality = cms.string('highPurity'),
    maxChi2 = cms.double(16.0),
    minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
    oldClusterRemovalInfo = cms.InputTag(""),
    overrideTrkQuals = cms.InputTag(""),
    pixelClusters = cms.InputTag("hltSiPixelClusters"),
    stripClusters = cms.InputTag("hltSiStripRawToClustersFacilityOnDemand"),
    trackClassifier = cms.InputTag("","QualityMasks"),
    trajectories = cms.InputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity")
)


process.hltIter3IterL3FromL1MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('hltIter3IterL3FromL1Muon'),
    Fitter = cms.string('hltESPFittingSmootherIT'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string(''),
    MeasurementTrackerEvent = cms.InputTag("hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent"),
    NavigationSchool = cms.string(''),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIter3IterL3FromL1MuonCkfTrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(True)
)


process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent = cms.EDProducer("MaskedMeasurementTrackerEventProducer",
    clustersToSkip = cms.InputTag("hltIter3IterL3FromL1MuonClustersRefRemoval"),
    phase2clustersToSkip = cms.InputTag(""),
    src = cms.InputTag("hltMeasurementTrackerEventOnDemand")
)


process.hltIter3IterL3FromL1MuonPixelClusterCheck = cms.EDProducer("ClusterCheckerEDProducer",
    ClusterCollectionLabel = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    DontCountDetsAboveNClusters = cms.uint32(0),
    MaxNumberOfPixelClusters = cms.uint32(40000),
    MaxNumberOfStripClusters = cms.uint32(50000),
    PixelClusterCollectionLabel = cms.InputTag("hltSiPixelClusters"),
    cut = cms.string(''),
    doClusterCheck = cms.bool(False),
    silentClusterCheck = cms.untracked.bool(False)
)


process.hltIter3IterL3FromL1MuonPixelHitDoublets = cms.EDProducer("HitPairEDProducer",
    clusterCheck = cms.InputTag("hltIter3IterL3FromL1MuonPixelClusterCheck"),
    layerPairs = cms.vuint32(0),
    maxElement = cms.uint32(0),
    maxElementTotal = cms.uint32(50000000),
    produceIntermediateHitDoublets = cms.bool(False),
    produceSeedingHitSets = cms.bool(True),
    putEmptyIfMaxElementReached = cms.bool(False),
    seedingLayers = cms.InputTag("hltIter3IterL3FromL1MuonPixelLayersAndRegions"),
    trackingRegions = cms.InputTag("hltIter3IterL3FromL1MuonTrackingRegions"),
    trackingRegionsSeedingLayers = cms.InputTag("")
)


process.hltIter3IterL3FromL1MuonPixelLayersAndRegions = cms.EDProducer("PixelInactiveAreaTrackingRegionsSeedingLayersProducer",
    BPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0027),
        hitErrorRZ = cms.double(0.006),
        skipClusters = cms.InputTag("hltIter3IterL3FromL1MuonClustersRefRemoval"),
        useErrorsFromParam = cms.bool(True)
    ),
    FPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0051),
        hitErrorRZ = cms.double(0.0036),
        skipClusters = cms.InputTag("hltIter3IterL3FromL1MuonClustersRefRemoval"),
        useErrorsFromParam = cms.bool(True)
    ),
    MTEC = cms.PSet(

    ),
    MTIB = cms.PSet(

    ),
    MTID = cms.PSet(

    ),
    MTOB = cms.PSet(

    ),
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        extraEta = cms.double(0.0),
        extraPhi = cms.double(0.0),
        maxNVertices = cms.int32(3),
        measurementTrackerName = cms.InputTag("hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent"),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        operationMode = cms.string('VerticesFixed'),
        originRadius = cms.double(0.015),
        precise = cms.bool(True),
        ptMin = cms.double(1.2),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
        whereToUseMeasurementTracker = cms.string('ForSiStrips'),
        zErrorBeamSpot = cms.double(15.0),
        zErrorVertex = cms.double(0.03)
    ),
    TEC = cms.PSet(

    ),
    TIB = cms.PSet(

    ),
    TID = cms.PSet(

    ),
    TOB = cms.PSet(

    ),
    badPixelFEDChannelCollectionLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    createPlottingFiles = cms.untracked.bool(False),
    debug = cms.untracked.bool(False),
    ignoreSingleFPixPanelModules = cms.bool(True),
    inactivePixelDetectorLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    layerList = cms.vstring(
        'BPix1+BPix2',
        'BPix1+BPix3',
        'BPix1+BPix4',
        'BPix2+BPix3',
        'BPix2+BPix4',
        'BPix3+BPix4',
        'BPix1+FPix1_pos',
        'BPix1+FPix1_neg',
        'BPix1+FPix2_pos',
        'BPix1+FPix2_neg',
        'BPix1+FPix3_pos',
        'BPix1+FPix3_neg',
        'BPix2+FPix1_pos',
        'BPix2+FPix1_neg',
        'BPix2+FPix2_pos',
        'BPix2+FPix2_neg',
        'BPix3+FPix1_pos',
        'BPix3+FPix1_neg',
        'FPix1_pos+FPix2_pos',
        'FPix1_neg+FPix2_neg',
        'FPix1_pos+FPix3_pos',
        'FPix1_neg+FPix3_neg',
        'FPix2_pos+FPix3_pos',
        'FPix2_neg+FPix3_neg'
    )
)


process.hltIter3IterL3FromL1MuonPixelSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsEDProducer",
    MinOneOverPtError = cms.double(1.0),
    OriginTransverseErrorMultiplier = cms.double(1.0),
    SeedComparitorPSet = cms.PSet(
        ComponentName = cms.string('none')
    ),
    SeedMomentumForBOFF = cms.double(5.0),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField = cms.string('ParabolicMf'),
    propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    seedingHitSets = cms.InputTag("hltIter3IterL3FromL1MuonPixelHitDoublets")
)


process.hltIter3IterL3FromL1MuonPixelSeedsFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
    L1Muon = cms.InputTag("hltGtStage2Digis","Muon"),
    L2Muon = cms.InputTag("hltL2MuonCandidates"),
    baseScore = cms.double(0.5),
    doSort = cms.bool(False),
    etaEdge = cms.double(1.2),
    isFromL1 = cms.bool(True),
    minL1Qual = cms.int32(7),
    mvaCutB = cms.double(0.1),
    mvaCutE = cms.double(0.1),
    mvaFileB = cms.FileInPath('RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter3FromL1_DoubletSeeds_barrel_v1.xml'),
    mvaFileE = cms.FileInPath('RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter3FromL1_DoubletSeeds_endcap_v1.xml'),
    mvaScaleMeanB = cms.vdouble(
        0.006826621711798213, 1.340471761359199e-05, 2.5827749083302998e-06, 0.00038329754175309627, -0.006327854398161656,
        0.0017211841076523692, 0.2760538806332439, -0.010429922003892818
    ),
    mvaScaleMeanE = cms.vdouble(
        0.0013243955281318262, 7.150658575633707e-06, 1.0493070182976e-05, -0.004802713888821372, -0.022186379498012398,
        0.0008335525228198972, 0.2915475574025415, -0.01200308471140653
    ),
    mvaScaleStdB = cms.vdouble(
        0.006225819995879627, 7.4048803387083885e-06, 3.6347963283736586e-06, 0.062213478665703675, 0.828854421408699,
        0.3714730344087147, 0.42155116686695293, 0.38566415759730355
    ),
    mvaScaleStdE = cms.vdouble(
        0.0013768261827517547, 7.80116971559064e-06, 8.819635719472336e-05, 0.27824938208607475, 1.798678366076454,
        0.16556388679148643, 0.48300543536161705, 0.401204958844809
    ),
    nSeedsMaxB = cms.int32(99999),
    nSeedsMaxE = cms.int32(99999),
    rejectAll = cms.bool(False),
    src = cms.InputTag("hltIter3IterL3FromL1MuonPixelSeeds")
)


process.hltIter3IterL3FromL1MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(False),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 0.003),
            d0err_par = cms.vdouble(0.001, 0.001, 0.001),
            dr_exp = cms.vint32(4, 4, 4),
            dr_par1 = cms.vdouble(3.40282346639e+38, 0.4, 0.4),
            dr_par2 = cms.vdouble(3.40282346639e+38, 0.3, 0.3)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 4),
            dz_par1 = cms.vdouble(3.40282346639e+38, 0.4, 0.4),
            dz_par2 = cms.vdouble(3.40282346639e+38, 0.35, 0.35)
        ),
        maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
        maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
        maxLostLayers = cms.vint32(1, 1, 1),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 3, 3),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIter3IterL3FromL1MuonCtfWithMaterialTracks"),
    vertices = cms.InputTag("hltTrimmedPixelVertices")
)


process.hltIter3IterL3FromL1MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIter3IterL3FromL1MuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIter3IterL3FromL1MuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIter3IterL3FromL1MuonCtfWithMaterialTracks")
)


process.hltIter3IterL3FromL1MuonTrackingRegions = cms.EDProducer("L1MuonSeededTrackingRegionsEDProducer",
    CentralBxOnly = cms.bool(True),
    L1MaxEta = cms.double(2.5),
    L1MinPt = cms.double(0.0),
    L1MinQuality = cms.uint32(7),
    Propagator = cms.string('SteppingHelixPropagatorAny'),
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEtas = cms.vdouble(0.175, 0.175, 0.175, 0.175),
        deltaPhis = cms.vdouble(0.5, 0.4, 0.3, 0.15),
        input = cms.InputTag("hltL1MuonsPt0"),
        maxNRegions = cms.int32(3),
        maxNVertices = cms.int32(3),
        measurementTrackerName = cms.InputTag("hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent"),
        mode = cms.string('VerticesFixed'),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        originRadius = cms.double(0.015),
        precise = cms.bool(True),
        ptMin = cms.double(1.2),
        ptRanges = cms.vdouble(0.0, 10.0, 15.0, 20.0, 1e+64),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
        whereToUseMeasurementTracker = cms.string('ForSiStrips'),
        zErrorBeamSpot = cms.double(15.0)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    SetMinPtBarrelTo = cms.double(3.5),
    SetMinPtEndcapTo = cms.double(1.0)
)


process.hltIterL3FromL1MuonPixelTracksTrackingRegions = cms.EDProducer("L1MuonSeededTrackingRegionsEDProducer",
    CentralBxOnly = cms.bool(True),
    L1MaxEta = cms.double(2.5),
    L1MinPt = cms.double(0.0),
    L1MinQuality = cms.uint32(7),
    Propagator = cms.string('SteppingHelixPropagatorAny'),
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEtas = cms.vdouble(0.35, 0.35, 0.35, 0.35),
        deltaPhis = cms.vdouble(1.0, 0.8, 0.6, 0.3),
        input = cms.InputTag("hltL1MuonsPt0"),
        maxNRegions = cms.int32(5),
        maxNVertices = cms.int32(1),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('BeamSpotSigma'),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        originRadius = cms.double(0.2),
        precise = cms.bool(True),
        ptMin = cms.double(0.0),
        ptRanges = cms.vdouble(0.0, 10.0, 15.0, 20.0, 1e+64),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("notUsed"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(24.2),
        zErrorVetex = cms.double(0.2)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    SetMinPtBarrelTo = cms.double(3.5),
    SetMinPtEndcapTo = cms.double(1.0)
)


process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx = cms.EDProducer("L1MuonSeededTrackingRegionsEDProducer",
    CentralBxOnly = cms.bool(True),
    L1MaxEta = cms.double(2.5),
    L1MinPt = cms.double(0.0),
    L1MinQuality = cms.uint32(7),
    Propagator = cms.string('SteppingHelixPropagatorAny'),
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEtas = cms.vdouble(0.35, 0.35, 0.35, 0.35),
        deltaPhis = cms.vdouble(1.0, 0.8, 0.6, 0.3),
        input = cms.InputTag("hltIterL3MuonL1MuonNoL2SelectorNoVtx"),
        maxNRegions = cms.int32(5),
        maxNVertices = cms.int32(1),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('BeamSpotSigma'),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        originRadius = cms.double(0.2),
        precise = cms.bool(True),
        ptMin = cms.double(0.0),
        ptRanges = cms.vdouble(0.0, 10.0, 15.0, 20.0, 1e+64),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("notUsed"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(24.2),
        zErrorVetex = cms.double(0.2)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    SetMinPtBarrelTo = cms.double(3.5),
    SetMinPtEndcapTo = cms.double(1.0)
)


process.hltIterL3GlbMuon = cms.EDProducer("L3MuonProducer",
    L3TrajBuilderParameters = cms.PSet(
        GlbRefitterParameters = cms.PSet(
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            Chi2CutCSC = cms.double(150.0),
            Chi2CutDT = cms.double(10.0),
            Chi2CutGEM = cms.double(1.0),
            Chi2CutRPC = cms.double(1.0),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            DYTthrs = cms.vint32(30, 15),
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            GEMRecHitLabel = cms.InputTag("hltGemRecHits"),
            HitThreshold = cms.int32(1),
            MuonHitsOption = cms.int32(1),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            PropDirForCosmics = cms.bool(False),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitFlag = cms.bool(True),
            RefitRPCHits = cms.bool(True),
            SkipStation = cms.int32(-1),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
            TrackerSkipSection = cms.int32(-1),
            TrackerSkipSystem = cms.int32(-1)
        ),
        GlobalMuonTrackMatcher = cms.PSet(
            Chi2Cut_1 = cms.double(50.0),
            Chi2Cut_2 = cms.double(50.0),
            Chi2Cut_3 = cms.double(200.0),
            DeltaDCut_1 = cms.double(40.0),
            DeltaDCut_2 = cms.double(10.0),
            DeltaDCut_3 = cms.double(15.0),
            DeltaRCut_1 = cms.double(0.1),
            DeltaRCut_2 = cms.double(0.2),
            DeltaRCut_3 = cms.double(1.0),
            Eta_threshold = cms.double(1.2),
            LocChi2Cut = cms.double(0.001),
            MinP = cms.double(2.5),
            MinPt = cms.double(1.0),
            Propagator = cms.string('hltESPSmartPropagator'),
            Pt_threshold1 = cms.double(0.0),
            Pt_threshold2 = cms.double(999999999.0),
            Quality_1 = cms.double(20.0),
            Quality_2 = cms.double(15.0),
            Quality_3 = cms.double(7.0)
        ),
        MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
        MuonTrackingRegionBuilder = cms.PSet(
            DeltaEta = cms.double(0.2),
            DeltaPhi = cms.double(0.15),
            DeltaR = cms.double(0.025),
            DeltaZ = cms.double(24.2),
            EtaR_UpperLimit_Par1 = cms.double(0.25),
            EtaR_UpperLimit_Par2 = cms.double(0.15),
            Eta_fixed = cms.bool(True),
            Eta_min = cms.double(0.1),
            MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
            OnDemand = cms.int32(-1),
            PhiR_UpperLimit_Par1 = cms.double(0.6),
            PhiR_UpperLimit_Par2 = cms.double(0.2),
            Phi_fixed = cms.bool(True),
            Phi_min = cms.double(0.1),
            Pt_fixed = cms.bool(False),
            Pt_min = cms.double(3.0),
            Rescale_Dz = cms.double(4.0),
            Rescale_eta = cms.double(3.0),
            Rescale_phi = cms.double(3.0),
            UseVertex = cms.bool(False),
            Z_fixed = cms.bool(False),
            beamSpot = cms.InputTag("hltOnlineBeamSpot"),
            input = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
            maxRegions = cms.int32(2),
            precise = cms.bool(True),
            vertexCollection = cms.InputTag("pixelVertices")
        ),
        PCut = cms.double(2.5),
        PtCut = cms.double(1.0),
        RefitRPCHits = cms.bool(True),
        ScaleTECxFactor = cms.double(-1.0),
        ScaleTECyFactor = cms.double(-1.0),
        TrackTransformer = cms.PSet(
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitRPCHits = cms.bool(True),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle')
        ),
        TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
        TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        tkTrajLabel = cms.InputTag("hltIterL3MuonAndMuonFromL1Merged"),
        tkTrajMaxChi2 = cms.double(9999.0),
        tkTrajMaxDXYBeamSpot = cms.double(9999.0),
        tkTrajUseVertex = cms.bool(False),
        tkTrajVertex = cms.InputTag("Notused")
    ),
    MuonCollectionLabel = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring(
            'hltESPSmartPropagatorAny',
            'SteppingHelixPropagatorAny',
            'hltESPSmartPropagator',
            'hltESPSteppingHelixPropagatorOpposite'
        ),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        DoSmoothing = cms.bool(True),
        MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
        MuonUpdatorAtVertexParameters = cms.PSet(
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
            MaxChi2 = cms.double(1000000.0),
            Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
        ),
        PutTkTrackIntoEvent = cms.untracked.bool(False),
        SmoothTkTrack = cms.untracked.bool(False),
        Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        VertexConstraint = cms.bool(False),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )
)


process.hltIterL3MuonAndMuonFromL1Merged = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIterL3MuonMerged", "hltIter03IterL3FromL1MuonMerged"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIterL3MuonMerged", "hltIter03IterL3FromL1MuonMerged"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltIterL3MuonAndMuonFromL1MergedNoVtx = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIterL3MuonMergedNoVtx", "hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIterL3MuonMergedNoVtx", "hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltIterL3MuonCandidates = cms.EDProducer("L3MuonCandidateProducerFromMuons",
    DisplacedReconstruction = cms.bool(False),
    InputObjects = cms.InputTag("hltIterL3Muons")
)


process.hltIterL3MuonCandidatesNoVtx = cms.EDProducer("L3MuonCandidateProducerFromMuons",
    DisplacedReconstruction = cms.bool(False),
    InputObjects = cms.InputTag("hltIterL3MuonsNoVtx")
)


process.hltIterL3MuonL1MuonNoL2SelectorNoVtx = cms.EDProducer("HLTL1MuonNoL2Selector",
    CentralBxOnly = cms.bool(True),
    InputObjects = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MaxEta = cms.double(5.0),
    L1MinPt = cms.double(-1.0),
    L1MinQuality = cms.uint32(7),
    L2CandTag = cms.InputTag("hltL2MuonCandidatesNoVtx"),
    SeedMapTag = cms.InputTag("hltL2Muons")
)


process.hltIterL3MuonMerged = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurity", "hltIter0IterL3MuonTrackSelectionHighPurity"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurity", "hltIter0IterL3MuonTrackSelectionHighPurity"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltIterL3MuonMergedNoVtx = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurityNoVtx", "hltIter0IterL3MuonTrackSelectionHighPurityNoVtx"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurityNoVtx", "hltIter0IterL3MuonTrackSelectionHighPurityNoVtx"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltIterL3MuonPixelTracksTrackingRegions = cms.EDProducer("MuonTrackingRegionByPtEDProducer",
    DeltaR = cms.double(0.025),
    DeltaZ = cms.double(24.2),
    MeasurementTrackerName = cms.InputTag(""),
    OnDemand = cms.int32(-1),
    Pt_fixed = cms.bool(True),
    Pt_min = cms.double(0.0),
    Rescale_Dz = cms.double(4.0),
    UseVertex = cms.bool(False),
    Z_fixed = cms.bool(True),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    deltaEtas = cms.vdouble(0.2, 0.2, 0.2),
    deltaPhis = cms.vdouble(0.75, 0.45, 0.225),
    input = cms.InputTag("hltL2SelectorForL3IO"),
    maxRegions = cms.int32(5),
    precise = cms.bool(True),
    ptRanges = cms.vdouble(0.0, 15.0, 20.0, 1e+64),
    vertexCollection = cms.InputTag("notUsed")
)


process.hltIterL3MuonPixelTracksTrackingRegionsNoVtx = cms.EDProducer("MuonTrackingRegionByPtEDProducer",
    DeltaR = cms.double(0.025),
    DeltaZ = cms.double(24.2),
    MeasurementTrackerName = cms.InputTag(""),
    OnDemand = cms.int32(-1),
    Pt_fixed = cms.bool(True),
    Pt_min = cms.double(0.0),
    Rescale_Dz = cms.double(4.0),
    UseVertex = cms.bool(False),
    Z_fixed = cms.bool(True),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    deltaEtas = cms.vdouble(0.2, 0.2, 0.2),
    deltaPhis = cms.vdouble(0.75, 0.45, 0.225),
    input = cms.InputTag("hltL2SelectorForL3IONoVtx"),
    maxRegions = cms.int32(5),
    precise = cms.bool(True),
    ptRanges = cms.vdouble(0.0, 15.0, 20.0, 1e+64),
    vertexCollection = cms.InputTag("notUsed")
)


process.hltIterL3MuonTracks = cms.EDProducer("HLTMuonTrackSelector",
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    copyTrajectories = cms.untracked.bool(False),
    muon = cms.InputTag("hltIterL3Muons"),
    originalMVAVals = cms.InputTag("none"),
    track = cms.InputTag("hltIterL3MuonAndMuonFromL1Merged")
)


process.hltIterL3Muons = cms.EDProducer("MuonIDFilterProducerForHLT",
    allowedTypeMask = cms.uint32(0),
    applyTriggerIdLoose = cms.bool(True),
    inputMuonCollection = cms.InputTag("hltIterL3MuonsNoID"),
    maxNormalizedChi2 = cms.double(9999.0),
    minNMuonHits = cms.int32(0),
    minNMuonStations = cms.int32(0),
    minNTrkLayers = cms.int32(0),
    minPixHits = cms.int32(0),
    minPixLayer = cms.int32(0),
    minPt = cms.double(0.0),
    minTrkHits = cms.int32(0),
    requiredTypeMask = cms.uint32(0),
    typeMuon = cms.uint32(0)
)


process.hltIterL3MuonsFromL2LinksCombination = cms.EDProducer("L3TrackLinksCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OI", "hltL3MuonsIterL3IO")
)


process.hltIterL3MuonsFromL2LinksCombinationNoVtx = cms.EDProducer("L3TrackLinksCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OINoVtx", "hltL3MuonsIterL3IONoVtx")
)


process.hltIterL3MuonsFromL2NoVtx = cms.EDProducer("L3TrackCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OINoVtx", "hltL3MuonsIterL3IONoVtx")
)


process.hltIterL3MuonsNoID = cms.EDProducer("MuonIdProducer",
    CaloExtractorPSet = cms.PSet(
        CenterConeOnCalIntersection = cms.bool(False),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DR_Veto_HO = cms.double(0.1),
        DepositInstanceLabels = cms.vstring(
            'ecal',
            'hcal',
            'ho'
        ),
        DepositLabel = cms.untracked.string('Cal'),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_EB = cms.double(0.025),
        Noise_EE = cms.double(0.1),
        Noise_HB = cms.double(0.2),
        Noise_HE = cms.double(0.2),
        Noise_HO = cms.double(0.2),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Threshold_HO = cms.double(0.5),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(1.0),
            dREcalPreselection = cms.double(1.0),
            dRHcal = cms.double(1.0),
            dRHcalPreselection = cms.double(1.0),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        ),
        UseRecHitsFlag = cms.bool(False)
    ),
    JetExtractorPSet = cms.PSet(
        ComponentName = cms.string('JetExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.1),
        ExcludeMuonVeto = cms.bool(True),
        JetCollectionLabel = cms.InputTag("Notused"),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold = cms.double(5.0),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(0.5),
            dREcalPreselection = cms.double(0.5),
            dRHcal = cms.double(0.5),
            dRHcalPreselection = cms.double(0.5),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        )
    ),
    MuonCaloCompatibility = cms.PSet(
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root'),
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root'),
        allSiPMHO = cms.bool(False),
        delta_eta = cms.double(0.02),
        delta_phi = cms.double(0.02)
    ),
    ShowerDigiFillerParameters = cms.PSet(
        cscDigiCollectionLabel = cms.InputTag("hltMuonCSCDigis","MuonCSCStripDigi"),
        digiMaxDistanceX = cms.double(25.0),
        dtDigiCollectionLabel = cms.InputTag("hltMuonDTDigis")
    ),
    TimingFillerParameters = cms.PSet(
        CSCTimingParameters = cms.PSet(
            CSCStripError = cms.double(7.0),
            CSCStripTimeOffset = cms.double(0.0),
            CSCTimeOffset = cms.double(0.0),
            CSCWireError = cms.double(8.6),
            CSCWireTimeOffset = cms.double(0.0),
            CSCsegments = cms.InputTag("hltCscSegments"),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(100.0),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseStripTime = cms.bool(True),
            UseWireTime = cms.bool(True),
            debug = cms.bool(False)
        ),
        DTTimingParameters = cms.PSet(
            DTTimeOffset = cms.double(2.7),
            DTsegments = cms.InputTag("hltDt4DSegments"),
            DoWireCorr = cms.bool(False),
            DropTheta = cms.bool(True),
            HitError = cms.double(6.0),
            HitsMin = cms.int32(5),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(10000.0),
            RequireBothProjections = cms.bool(False),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseSegmentT0 = cms.bool(False),
            debug = cms.bool(False)
        ),
        EcalEnergyCut = cms.double(0.4),
        ErrorCSC = cms.double(7.4),
        ErrorDT = cms.double(6.0),
        ErrorEB = cms.double(2.085),
        ErrorEE = cms.double(6.95),
        UseCSC = cms.bool(True),
        UseDT = cms.bool(True),
        UseECAL = cms.bool(True)
    ),
    TrackAssociatorParameters = cms.PSet(
        CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
        CaloTowerCollectionLabel = cms.InputTag("Notused"),
        DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
        EBRecHitCollectionLabel = cms.InputTag("Notused"),
        EERecHitCollectionLabel = cms.InputTag("Notused"),
        GEMSegmentCollectionLabel = cms.InputTag("hltGemSegments"),
        HBHERecHitCollectionLabel = cms.InputTag("Notused"),
        HORecHitCollectionLabel = cms.InputTag("Notused"),
        accountForTrajectoryChangeCalo = cms.bool(False),
        dREcal = cms.double(9999.0),
        dREcalPreselection = cms.double(0.05),
        dRHcal = cms.double(9999.0),
        dRHcalPreselection = cms.double(0.2),
        dRMuon = cms.double(9999.0),
        dRMuonPreselection = cms.double(0.2),
        dRPreshowerPreselection = cms.double(0.2),
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        propagateAllDirections = cms.bool(True),
        trajectoryUncertaintyTolerance = cms.double(-1.0),
        truthMatch = cms.bool(False),
        useCalo = cms.bool(False),
        useEcal = cms.bool(False),
        useGEM = cms.bool(True),
        useHO = cms.bool(False),
        useHcal = cms.bool(False),
        useMuon = cms.bool(True),
        usePreshower = cms.bool(False)
    ),
    TrackExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.01),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        Pt_Min = cms.double(-1.0),
        inputTrackCollection = cms.InputTag("hltIter03IterL3FromL1MuonMerged")
    ),
    TrackerKinkFinderParameters = cms.PSet(
        diagonalOnly = cms.bool(False),
        usePosition = cms.bool(False)
    ),
    addExtraSoftMuons = cms.bool(False),
    arbitrateTrackerMuons = cms.bool(True),
    arbitrationCleanerOptions = cms.PSet(
        ClusterDPhi = cms.double(0.6),
        ClusterDTheta = cms.double(0.02),
        Clustering = cms.bool(True),
        ME1a = cms.bool(True),
        Overlap = cms.bool(True),
        OverlapDPhi = cms.double(0.0786),
        OverlapDTheta = cms.double(0.02)
    ),
    debugWithTruthMatching = cms.bool(False),
    ecalDepositName = cms.string('ecal'),
    fillCaloCompatibility = cms.bool(False),
    fillEnergy = cms.bool(False),
    fillGlobalTrackQuality = cms.bool(False),
    fillGlobalTrackRefits = cms.bool(False),
    fillIsolation = cms.bool(False),
    fillMatching = cms.bool(True),
    fillShowerDigis = cms.bool(False),
    fillTrackerKink = cms.bool(False),
    globalTrackQualityInputTag = cms.InputTag(""),
    hcalDepositName = cms.string('hcal'),
    hoDepositName = cms.string('ho'),
    inputCollectionLabels = cms.VInputTag("hltIterL3MuonAndMuonFromL1Merged", "hltIterL3GlbMuon", "hltL2Muons:UpdatedAtVtx"),
    inputCollectionTypes = cms.vstring(
        'inner tracks',
        'links',
        'outer tracks'
    ),
    jetDepositName = cms.string('jets'),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    maxAbsEta = cms.double(3.0),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minCaloCompatibility = cms.double(0.6),
    minNumberOfMatches = cms.int32(1),
    minP = cms.double(0.0),
    minPCaloMuon = cms.double(1000000000.0),
    minPt = cms.double(2.0),
    ptThresholdToFillCandidateP4WithGlobalFit = cms.double(200.0),
    pvInputTag = cms.InputTag(""),
    runArbitrationCleaner = cms.bool(False),
    selectHighPurity = cms.bool(False),
    sigmaThresholdToFillCandidateP4WithGlobalFit = cms.double(2.0),
    storeCrossedHcalRecHits = cms.bool(False),
    trackDepositName = cms.string('tracker'),
    writeIsoDeposits = cms.bool(False)
)


process.hltIterL3MuonsNoVtx = cms.EDProducer("MuonIdProducer",
    CaloExtractorPSet = cms.PSet(
        CenterConeOnCalIntersection = cms.bool(False),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DR_Veto_HO = cms.double(0.1),
        DepositInstanceLabels = cms.vstring(
            'ecal',
            'hcal',
            'ho'
        ),
        DepositLabel = cms.untracked.string('Cal'),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_EB = cms.double(0.025),
        Noise_EE = cms.double(0.1),
        Noise_HB = cms.double(0.2),
        Noise_HE = cms.double(0.2),
        Noise_HO = cms.double(0.2),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Threshold_HO = cms.double(0.5),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(1.0),
            dREcalPreselection = cms.double(1.0),
            dRHcal = cms.double(1.0),
            dRHcalPreselection = cms.double(1.0),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        ),
        UseRecHitsFlag = cms.bool(False)
    ),
    JetExtractorPSet = cms.PSet(
        ComponentName = cms.string('JetExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.1),
        ExcludeMuonVeto = cms.bool(True),
        JetCollectionLabel = cms.InputTag("Notused"),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold = cms.double(5.0),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(0.5),
            dREcalPreselection = cms.double(0.5),
            dRHcal = cms.double(0.5),
            dRHcalPreselection = cms.double(0.5),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        )
    ),
    MuonCaloCompatibility = cms.PSet(
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root'),
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root'),
        allSiPMHO = cms.bool(False),
        delta_eta = cms.double(0.02),
        delta_phi = cms.double(0.02)
    ),
    ShowerDigiFillerParameters = cms.PSet(
        cscDigiCollectionLabel = cms.InputTag("hltMuonCSCDigis","MuonCSCStripDigi"),
        digiMaxDistanceX = cms.double(25.0),
        dtDigiCollectionLabel = cms.InputTag("hltMuonDTDigis")
    ),
    TimingFillerParameters = cms.PSet(
        CSCTimingParameters = cms.PSet(
            CSCStripError = cms.double(7.0),
            CSCStripTimeOffset = cms.double(0.0),
            CSCTimeOffset = cms.double(0.0),
            CSCWireError = cms.double(8.6),
            CSCWireTimeOffset = cms.double(0.0),
            CSCsegments = cms.InputTag("hltCscSegments"),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(100.0),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseStripTime = cms.bool(True),
            UseWireTime = cms.bool(True),
            debug = cms.bool(False)
        ),
        DTTimingParameters = cms.PSet(
            DTTimeOffset = cms.double(2.7),
            DTsegments = cms.InputTag("hltDt4DSegments"),
            DoWireCorr = cms.bool(False),
            DropTheta = cms.bool(True),
            HitError = cms.double(6.0),
            HitsMin = cms.int32(5),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(10000.0),
            RequireBothProjections = cms.bool(False),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseSegmentT0 = cms.bool(False),
            debug = cms.bool(False)
        ),
        EcalEnergyCut = cms.double(0.4),
        ErrorCSC = cms.double(7.4),
        ErrorDT = cms.double(6.0),
        ErrorEB = cms.double(2.085),
        ErrorEE = cms.double(6.95),
        UseCSC = cms.bool(True),
        UseDT = cms.bool(True),
        UseECAL = cms.bool(True)
    ),
    TrackAssociatorParameters = cms.PSet(
        CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
        CaloTowerCollectionLabel = cms.InputTag("Notused"),
        DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
        EBRecHitCollectionLabel = cms.InputTag("Notused"),
        EERecHitCollectionLabel = cms.InputTag("Notused"),
        HBHERecHitCollectionLabel = cms.InputTag("Notused"),
        HORecHitCollectionLabel = cms.InputTag("Notused"),
        accountForTrajectoryChangeCalo = cms.bool(False),
        dREcal = cms.double(9999.0),
        dREcalPreselection = cms.double(0.05),
        dRHcal = cms.double(9999.0),
        dRHcalPreselection = cms.double(0.2),
        dRMuon = cms.double(9999.0),
        dRMuonPreselection = cms.double(0.2),
        dRPreshowerPreselection = cms.double(0.2),
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        propagateAllDirections = cms.bool(True),
        trajectoryUncertaintyTolerance = cms.double(-1.0),
        truthMatch = cms.bool(False),
        useCalo = cms.bool(False),
        useEcal = cms.bool(False),
        useHO = cms.bool(False),
        useHcal = cms.bool(False),
        useMuon = cms.bool(True),
        usePreshower = cms.bool(False)
    ),
    TrackExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.01),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        Pt_Min = cms.double(-1.0),
        inputTrackCollection = cms.InputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx")
    ),
    TrackerKinkFinderParameters = cms.PSet(
        diagonalOnly = cms.bool(False),
        usePosition = cms.bool(False)
    ),
    addExtraSoftMuons = cms.bool(False),
    arbitrateTrackerMuons = cms.bool(True),
    arbitrationCleanerOptions = cms.PSet(
        ClusterDPhi = cms.double(0.6),
        ClusterDTheta = cms.double(0.02),
        Clustering = cms.bool(True),
        ME1a = cms.bool(True),
        Overlap = cms.bool(True),
        OverlapDPhi = cms.double(0.0786),
        OverlapDTheta = cms.double(0.02)
    ),
    debugWithTruthMatching = cms.bool(False),
    ecalDepositName = cms.string('ecal'),
    fillCaloCompatibility = cms.bool(False),
    fillEnergy = cms.bool(False),
    fillGlobalTrackQuality = cms.bool(False),
    fillGlobalTrackRefits = cms.bool(False),
    fillIsolation = cms.bool(False),
    fillMatching = cms.bool(True),
    fillShowerDigis = cms.bool(False),
    fillTrackerKink = cms.bool(False),
    globalTrackQualityInputTag = cms.InputTag(""),
    hcalDepositName = cms.string('hcal'),
    hoDepositName = cms.string('ho'),
    inputCollectionLabels = cms.VInputTag("hltIterL3MuonAndMuonFromL1MergedNoVtx", "hltL3MuonsIterL3LinksNoVtx"),
    inputCollectionTypes = cms.vstring(
        'inner tracks',
        'links'
    ),
    jetDepositName = cms.string('jets'),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    maxAbsEta = cms.double(3.0),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minCaloCompatibility = cms.double(0.6),
    minNumberOfMatches = cms.int32(1),
    minP = cms.double(0.0),
    minPCaloMuon = cms.double(1000000000.0),
    minPt = cms.double(8.0),
    ptThresholdToFillCandidateP4WithGlobalFit = cms.double(200.0),
    pvInputTag = cms.InputTag(""),
    runArbitrationCleaner = cms.bool(False),
    selectHighPurity = cms.bool(False),
    sigmaThresholdToFillCandidateP4WithGlobalFit = cms.double(2.0),
    storeCrossedHcalRecHits = cms.bool(False),
    trackDepositName = cms.string('tracker'),
    writeIsoDeposits = cms.bool(False)
)


process.hltIterL3OIL3MuonCandidates = cms.EDProducer("L3MuonCandidateProducer",
    InputLinksObjects = cms.InputTag("hltIterL3OIL3MuonsLinksCombination"),
    InputObjects = cms.InputTag("hltIterL3OIL3Muons"),
    MuonPtOption = cms.string('Tracker')
)


process.hltIterL3OIL3MuonCandidatesNoVtx = cms.EDProducer("L3MuonCandidateProducer",
    InputLinksObjects = cms.InputTag("hltIterL3OIL3MuonsLinksCombinationNoVtx"),
    InputObjects = cms.InputTag("hltIterL3OIL3MuonsNoVtx"),
    MuonPtOption = cms.string('Tracker')
)


process.hltIterL3OIL3Muons = cms.EDProducer("L3TrackCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OI")
)


process.hltIterL3OIL3MuonsLinksCombination = cms.EDProducer("L3TrackLinksCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OI")
)


process.hltIterL3OIL3MuonsLinksCombinationNoVtx = cms.EDProducer("L3TrackLinksCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OINoVtx")
)


process.hltIterL3OIL3MuonsNoVtx = cms.EDProducer("L3TrackCombiner",
    labels = cms.VInputTag("hltL3MuonsIterL3OINoVtx")
)


process.hltIterL3OIMuCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('iter10'),
    Fitter = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string('hltESPMeasurementTracker'),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    Propagator = cms.string('PropagatorWithMaterial'),
    SimpleMagneticField = cms.string(''),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIterL3OITrackCandidates"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(False)
)


process.hltIterL3OIMuCtfWithMaterialTracksNoVtx = cms.EDProducer("TrackProducer",
    AlgorithmName = cms.string('iter10'),
    Fitter = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK'),
    GeometricInnerState = cms.bool(True),
    MeasurementTracker = cms.string('hltESPMeasurementTracker'),
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    Propagator = cms.string('PropagatorWithMaterial'),
    SimpleMagneticField = cms.string(''),
    TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
    TrajectoryInEvent = cms.bool(False),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    clusterRemovalInfo = cms.InputTag(""),
    reMatchSplitHits = cms.bool(False),
    src = cms.InputTag("hltIterL3OITrackCandidatesNoVtx"),
    useHitsSplitting = cms.bool(False),
    usePropagatorForPCA = cms.bool(False),
    useSimpleMF = cms.bool(False)
)


process.hltIterL3OIMuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(True),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(10.0, 1.0, 0.4),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(4, 3, 2),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 5, 5),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracks"),
    vertices = cms.InputTag("Notused")
)


process.hltIterL3OIMuonTrackCutClassifierNoVtx = cms.EDProducer("TrackCutClassifier",
    beamspot = cms.InputTag("hltOnlineBeamSpot"),
    ignoreVertices = cms.bool(True),
    mva = cms.PSet(
        dr_par = cms.PSet(
            d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
            d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
            dr_exp = cms.vint32(4, 4, 2147483647),
            dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
        ),
        dz_par = cms.PSet(
            dz_exp = cms.vint32(4, 4, 2147483647),
            dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
            dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
        ),
        maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
        maxChi2n = cms.vdouble(10.0, 1.0, 0.4),
        maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
        maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
        maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
        maxLostLayers = cms.vint32(4, 3, 2),
        min3DLayers = cms.vint32(0, 0, 0),
        minLayers = cms.vint32(3, 5, 5),
        minNVtxTrk = cms.int32(3),
        minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
        minPixelHits = cms.vint32(0, 0, 0)
    ),
    qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
    src = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracksNoVtx"),
    vertices = cms.InputTag("Notused")
)


process.hltIterL3OIMuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIterL3OIMuonTrackCutClassifier","MVAValues"),
    originalQualVals = cms.InputTag("hltIterL3OIMuonTrackCutClassifier","QualityMasks"),
    originalSource = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracks")
)


process.hltIterL3OIMuonTrackSelectionHighPurityNoVtx = cms.EDProducer("TrackCollectionFilterCloner",
    copyExtras = cms.untracked.bool(True),
    copyTrajectories = cms.untracked.bool(False),
    minQuality = cms.string('highPurity'),
    originalMVAVals = cms.InputTag("hltIterL3OIMuonTrackCutClassifierNoVtx","MVAValues"),
    originalQualVals = cms.InputTag("hltIterL3OIMuonTrackCutClassifierNoVtx","QualityMasks"),
    originalSource = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracksNoVtx")
)


process.hltIterL3OISeedsFromL2Muons = cms.EDProducer("TSGForOIDNN",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    debug = cms.untracked.bool(False),
    dnnMetadataPath = cms.string('RecoMuon/TrackerSeedGenerator/data/OIseeding/DNNclassifier_Run3_metadata.json'),
    estimator = cms.string('hltESPChi2MeasurementEstimator100'),
    fixedErrorRescaleFactorForHitless = cms.double(2.0),
    getStrategyFromDNN = cms.bool(True),
    hitsToTry = cms.int32(1),
    layersToTry = cms.int32(2),
    maxEtaForTOB = cms.double(1.8),
    maxHitDoubletSeeds = cms.uint32(0),
    maxHitSeeds = cms.uint32(1),
    maxHitlessSeeds = cms.uint32(5),
    maxHitlessSeedsIP = cms.uint32(5),
    maxHitlessSeedsMuS = cms.uint32(0),
    maxSeeds = cms.uint32(20),
    minEtaForTEC = cms.double(0.7),
    propagatorName = cms.string('PropagatorWithMaterialParabolicMf'),
    src = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
    useRegressor = cms.bool(False)
)


process.hltIterL3OISeedsFromL2MuonsNoVtx = cms.EDProducer("TSGForOIFromL2",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    SF1 = cms.double(3.0),
    SF2 = cms.double(4.0),
    SF3 = cms.double(5.0),
    SF4 = cms.double(7.0),
    SF5 = cms.double(10.0),
    SF6 = cms.double(2.0),
    SFHd = cms.double(4.0),
    SFHld = cms.double(2.0),
    UseHitLessSeeds = cms.bool(True),
    adjustErrorsDynamicallyForHitless = cms.bool(True),
    adjustErrorsDynamicallyForHits = cms.bool(False),
    debug = cms.untracked.bool(False),
    displacedReco = cms.bool(False),
    estimator = cms.string('hltESPChi2MeasurementEstimator100'),
    eta1 = cms.double(0.2),
    eta2 = cms.double(0.3),
    eta3 = cms.double(1.0),
    eta4 = cms.double(1.2),
    eta5 = cms.double(1.6),
    eta6 = cms.double(1.4),
    eta7 = cms.double(2.1),
    fixedErrorRescaleFactorForHitless = cms.double(2.0),
    fixedErrorRescaleFactorForHits = cms.double(1.0),
    hitsToTry = cms.int32(1),
    layersToTry = cms.int32(2),
    maxEtaForTOB = cms.double(1.8),
    maxHitSeeds = cms.uint32(1),
    maxHitlessSeeds = cms.uint32(5),
    maxSeeds = cms.uint32(20),
    minEtaForTEC = cms.double(0.7),
    numL2ValidHitsCutAllEndcap = cms.uint32(30),
    numL2ValidHitsCutAllEta = cms.uint32(20),
    pT1 = cms.double(13.0),
    pT2 = cms.double(30.0),
    pT3 = cms.double(70.0),
    propagatorName = cms.string('PropagatorWithMaterialParabolicMf'),
    src = cms.InputTag("hltL2Muons"),
    tsosDiff1 = cms.double(0.2),
    tsosDiff2 = cms.double(0.02)
)


process.hltIterL3OITrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTPSetMuonCkfTrajectoryBuilder')
    ),
    TrajectoryCleaner = cms.string('muonSeededTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(False),
    maxNSeeds = cms.uint32(500000),
    maxSeedsBeforeCleaning = cms.uint32(5000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(True),
    src = cms.InputTag("hltIterL3OISeedsFromL2Muons"),
    useHitsSplitting = cms.bool(False)
)


process.hltIterL3OITrackCandidatesNoVtx = cms.EDProducer("CkfTrackCandidateMaker",
    MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEventOnDemand"),
    NavigationSchool = cms.string('SimpleNavigationSchool'),
    RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
    TrajectoryBuilderPSet = cms.PSet(
        refToPSet_ = cms.string('HLTPSetMuonCkfTrajectoryBuilder')
    ),
    TrajectoryCleaner = cms.string('muonSeededTrajectoryCleanerBySharedHits'),
    TransientInitialStateEstimatorParameters = cms.PSet(
        numberMeasurementsForFit = cms.int32(4),
        propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
        propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
    ),
    cleanTrajectoryAfterInOut = cms.bool(False),
    clustersToSkip = cms.InputTag(""),
    doSeedingRegionRebuilding = cms.bool(False),
    maxNSeeds = cms.uint32(500000),
    maxSeedsBeforeCleaning = cms.uint32(5000),
    numHitsForSeedCleaner = cms.int32(4),
    onlyPixelHitsForSeedCleaner = cms.bool(False),
    phase2clustersToSkip = cms.InputTag(""),
    reverseTrajectories = cms.bool(True),
    src = cms.InputTag("hltIterL3OISeedsFromL2MuonsNoVtx"),
    useHitsSplitting = cms.bool(False)
)


process.hltL1MuonsPt0 = cms.EDProducer("HLTL1TMuonSelector",
    CentralBxOnly = cms.bool(True),
    InputObjects = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MaxEta = cms.double(5.0),
    L1MinPt = cms.double(-1.0),
    L1MinQuality = cms.uint32(7)
)


process.hltL2MuonCandidates = cms.EDProducer("L2MuonCandidateProducer",
    InputObjects = cms.InputTag("hltL2Muons","UpdatedAtVtx")
)


process.hltL2MuonCandidatesNoVtx = cms.EDProducer("L2MuonCandidateProducer",
    InputObjects = cms.InputTag("hltL2Muons")
)


process.hltL2MuonSeeds = cms.EDProducer("L2MuonSeedGeneratorFromL1T",
    CentralBxOnly = cms.bool(True),
    EtaMatchingBins = cms.vdouble(0.0, 2.5),
    GMTReadoutCollection = cms.InputTag(""),
    InputObjects = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MaxEta = cms.double(2.5),
    L1MinPt = cms.double(0.0),
    L1MinQuality = cms.uint32(7),
    MatchDR = cms.vdouble(0.3),
    MatchType = cms.uint32(0),
    OfflineSeedLabel = cms.untracked.InputTag("hltL2OfflineMuonSeeds"),
    Propagator = cms.string('SteppingHelixPropagatorAny'),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny'),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    SetMinPtBarrelTo = cms.double(3.5),
    SetMinPtEndcapTo = cms.double(1.0),
    SortType = cms.uint32(0),
    UseOfflineSeed = cms.untracked.bool(True),
    UseUnassociatedL1 = cms.bool(False)
)


process.hltL2Muons = cms.EDProducer("L2MuonProducer",
    DoSeedRefit = cms.bool(False),
    InputObjects = cms.InputTag("hltL2MuonSeeds"),
    L2TrajBuilderParameters = cms.PSet(
        BWFilterParameters = cms.PSet(
            BWSeedType = cms.string('fromGenerator'),
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            EnableCSCMeasurement = cms.bool(True),
            EnableDTMeasurement = cms.bool(True),
            EnableGEMMeasurement = cms.bool(True),
            EnableRPCMeasurement = cms.bool(True),
            FitDirection = cms.string('outsideIn'),
            GEMRecSegmentLabel = cms.InputTag("hltGemRecHits"),
            MaxChi2 = cms.double(100.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                ExcludeRPCFromFit = cms.bool(False),
                Granularity = cms.int32(0),
                MaxChi2 = cms.double(25.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                UseInvalidHits = cms.bool(True)
            ),
            NumberOfSigma = cms.double(3.0),
            Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            RPCRecSegmentLabel = cms.InputTag("hltRpcRecHits")
        ),
        DoBackwardFilter = cms.bool(True),
        DoRefit = cms.bool(False),
        DoSeedRefit = cms.bool(False),
        FilterParameters = cms.PSet(
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            EnableCSCMeasurement = cms.bool(True),
            EnableDTMeasurement = cms.bool(True),
            EnableGEMMeasurement = cms.bool(True),
            EnableRPCMeasurement = cms.bool(True),
            FitDirection = cms.string('insideOut'),
            GEMRecSegmentLabel = cms.InputTag("hltGemRecHits"),
            MaxChi2 = cms.double(1000.0),
            MuonTrajectoryUpdatorParameters = cms.PSet(
                ExcludeRPCFromFit = cms.bool(False),
                Granularity = cms.int32(0),
                MaxChi2 = cms.double(25.0),
                RescaleError = cms.bool(False),
                RescaleErrorFactor = cms.double(100.0),
                UseInvalidHits = cms.bool(True)
            ),
            NumberOfSigma = cms.double(3.0),
            Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            RPCRecSegmentLabel = cms.InputTag("hltRpcRecHits")
        ),
        NavigationType = cms.string('Standard'),
        SeedPosition = cms.string('in'),
        SeedPropagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        SeedTransformerParameters = cms.PSet(
            Fitter = cms.string('hltESPKFFittingSmootherForL2Muon'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            NMinRecHits = cms.uint32(2),
            Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            RescaleError = cms.double(100.0),
            UseSubRecHits = cms.bool(False)
        )
    ),
    MuonTrajectoryBuilder = cms.string('Exhaustive'),
    SeedTransformerParameters = cms.PSet(
        Fitter = cms.string('hltESPKFFittingSmootherForL2Muon'),
        MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
        NMinRecHits = cms.uint32(2),
        Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        RescaleError = cms.double(100.0),
        UseSubRecHits = cms.bool(False)
    ),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring(
            'hltESPFastSteppingHelixPropagatorAny',
            'hltESPFastSteppingHelixPropagatorOpposite'
        ),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        DoSmoothing = cms.bool(False),
        MuonUpdatorAtVertexParameters = cms.PSet(
            BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
            MaxChi2 = cms.double(1000000.0),
            Propagator = cms.string('hltESPFastSteppingHelixPropagatorOpposite')
        ),
        Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        VertexConstraint = cms.bool(True),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )
)


process.hltL2OfflineMuonSeeds = cms.EDProducer("MuonSeedGenerator",
    CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
    CSC_01 = cms.vdouble(
        0.166, 0.0, 0.0, 0.031, 0.0,
        0.0
    ),
    CSC_01_1_scale = cms.vdouble(-1.915329, 0.0),
    CSC_02 = cms.vdouble(
        0.612, -0.207, 0.0, 0.067, -0.001,
        0.0
    ),
    CSC_03 = cms.vdouble(
        0.787, -0.338, 0.029, 0.101, -0.008,
        0.0
    ),
    CSC_12 = cms.vdouble(
        -0.161, 0.254, -0.047, 0.042, -0.007,
        0.0
    ),
    CSC_12_1_scale = cms.vdouble(-6.434242, 0.0),
    CSC_12_2_scale = cms.vdouble(-1.63622, 0.0),
    CSC_12_3_scale = cms.vdouble(-1.63622, 0.0),
    CSC_13 = cms.vdouble(
        0.901, -1.302, 0.533, 0.045, 0.005,
        0.0
    ),
    CSC_13_2_scale = cms.vdouble(-6.077936, 0.0),
    CSC_13_3_scale = cms.vdouble(-1.701268, 0.0),
    CSC_14 = cms.vdouble(
        0.606, -0.181, -0.002, 0.111, -0.003,
        0.0
    ),
    CSC_14_3_scale = cms.vdouble(-1.969563, 0.0),
    CSC_23 = cms.vdouble(
        -0.081, 0.113, -0.029, 0.015, 0.008,
        0.0
    ),
    CSC_23_1_scale = cms.vdouble(-19.084285, 0.0),
    CSC_23_2_scale = cms.vdouble(-6.079917, 0.0),
    CSC_24 = cms.vdouble(
        0.004, 0.021, -0.002, 0.053, 0.0,
        0.0
    ),
    CSC_24_1_scale = cms.vdouble(-6.055701, 0.0),
    CSC_34 = cms.vdouble(
        0.062, -0.067, 0.019, 0.021, 0.003,
        0.0
    ),
    CSC_34_1_scale = cms.vdouble(-11.520507, 0.0),
    DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
    DT_12 = cms.vdouble(
        0.183, 0.054, -0.087, 0.028, 0.002,
        0.0
    ),
    DT_12_1_scale = cms.vdouble(-3.692398, 0.0),
    DT_12_2_scale = cms.vdouble(-3.518165, 0.0),
    DT_13 = cms.vdouble(
        0.315, 0.068, -0.127, 0.051, -0.002,
        0.0
    ),
    DT_13_1_scale = cms.vdouble(-4.520923, 0.0),
    DT_13_2_scale = cms.vdouble(-4.257687, 0.0),
    DT_14 = cms.vdouble(
        0.359, 0.052, -0.107, 0.072, -0.004,
        0.0
    ),
    DT_14_1_scale = cms.vdouble(-5.644816, 0.0),
    DT_14_2_scale = cms.vdouble(-4.808546, 0.0),
    DT_23 = cms.vdouble(
        0.13, 0.023, -0.057, 0.028, 0.004,
        0.0
    ),
    DT_23_1_scale = cms.vdouble(-5.320346, 0.0),
    DT_23_2_scale = cms.vdouble(-5.117625, 0.0),
    DT_24 = cms.vdouble(
        0.176, 0.014, -0.051, 0.051, 0.003,
        0.0
    ),
    DT_24_1_scale = cms.vdouble(-7.490909, 0.0),
    DT_24_2_scale = cms.vdouble(-6.63094, 0.0),
    DT_34 = cms.vdouble(
        0.044, 0.004, -0.013, 0.029, 0.003,
        0.0
    ),
    DT_34_1_scale = cms.vdouble(-13.783765, 0.0),
    DT_34_2_scale = cms.vdouble(-11.901897, 0.0),
    EnableCSCMeasurement = cms.bool(True),
    EnableDTMeasurement = cms.bool(True),
    EnableME0Measurement = cms.bool(False),
    ME0RecSegmentLabel = cms.InputTag("me0Segments"),
    OL_1213 = cms.vdouble(
        0.96, -0.737, 0.0, 0.052, 0.0,
        0.0
    ),
    OL_1213_0_scale = cms.vdouble(-4.488158, 0.0),
    OL_1222 = cms.vdouble(
        0.848, -0.591, 0.0, 0.062, 0.0,
        0.0
    ),
    OL_1222_0_scale = cms.vdouble(-5.810449, 0.0),
    OL_1232 = cms.vdouble(
        0.184, 0.0, 0.0, 0.066, 0.0,
        0.0
    ),
    OL_1232_0_scale = cms.vdouble(-5.964634, 0.0),
    OL_2213 = cms.vdouble(
        0.117, 0.0, 0.0, 0.044, 0.0,
        0.0
    ),
    OL_2213_0_scale = cms.vdouble(-7.239789, 0.0),
    OL_2222 = cms.vdouble(
        0.107, 0.0, 0.0, 0.04, 0.0,
        0.0
    ),
    OL_2222_0_scale = cms.vdouble(-7.667231, 0.0),
    SMB_10 = cms.vdouble(
        1.387, -0.038, 0.0, 0.19, 0.0,
        0.0
    ),
    SMB_10_0_scale = cms.vdouble(2.448566, 0.0),
    SMB_11 = cms.vdouble(
        1.247, 0.72, -0.802, 0.229, -0.075,
        0.0
    ),
    SMB_11_0_scale = cms.vdouble(2.56363, 0.0),
    SMB_12 = cms.vdouble(
        2.128, -0.956, 0.0, 0.199, 0.0,
        0.0
    ),
    SMB_12_0_scale = cms.vdouble(2.283221, 0.0),
    SMB_20 = cms.vdouble(
        1.011, -0.052, 0.0, 0.188, 0.0,
        0.0
    ),
    SMB_20_0_scale = cms.vdouble(1.486168, 0.0),
    SMB_21 = cms.vdouble(
        1.043, -0.124, 0.0, 0.183, 0.0,
        0.0
    ),
    SMB_21_0_scale = cms.vdouble(1.58384, 0.0),
    SMB_22 = cms.vdouble(
        1.474, -0.758, 0.0, 0.185, 0.0,
        0.0
    ),
    SMB_22_0_scale = cms.vdouble(1.346681, 0.0),
    SMB_30 = cms.vdouble(
        0.505, -0.022, 0.0, 0.215, 0.0,
        0.0
    ),
    SMB_30_0_scale = cms.vdouble(-3.629838, 0.0),
    SMB_31 = cms.vdouble(
        0.549, -0.145, 0.0, 0.207, 0.0,
        0.0
    ),
    SMB_31_0_scale = cms.vdouble(-3.323768, 0.0),
    SMB_32 = cms.vdouble(
        0.67, -0.327, 0.0, 0.22, 0.0,
        0.0
    ),
    SMB_32_0_scale = cms.vdouble(-3.054156, 0.0),
    SME_11 = cms.vdouble(
        3.295, -1.527, 0.112, 0.378, 0.02,
        0.0
    ),
    SME_11_0_scale = cms.vdouble(1.325085, 0.0),
    SME_12 = cms.vdouble(
        0.102, 0.599, 0.0, 0.38, 0.0,
        0.0
    ),
    SME_12_0_scale = cms.vdouble(2.279181, 0.0),
    SME_13 = cms.vdouble(
        -1.286, 1.711, 0.0, 0.356, 0.0,
        0.0
    ),
    SME_13_0_scale = cms.vdouble(0.104905, 0.0),
    SME_21 = cms.vdouble(
        -0.529, 1.194, -0.358, 0.472, 0.086,
        0.0
    ),
    SME_21_0_scale = cms.vdouble(-0.040862, 0.0),
    SME_22 = cms.vdouble(
        -1.207, 1.491, -0.251, 0.189, 0.243,
        0.0
    ),
    SME_22_0_scale = cms.vdouble(-3.457901, 0.0),
    SME_31 = cms.vdouble(
        -1.594, 1.482, -0.317, 0.487, 0.097,
        0.0
    ),
    SME_32 = cms.vdouble(
        -0.901, 1.333, -0.47, 0.41, 0.073,
        0.0
    ),
    SME_41 = cms.vdouble(
        -0.003, 0.005, 0.005, 0.608, 0.076,
        0.0
    ),
    SME_42 = cms.vdouble(
        -0.003, 0.005, 0.005, 0.608, 0.076,
        0.0
    ),
    beamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    crackEtas = cms.vdouble(0.2, 1.6, 1.7),
    crackWindow = cms.double(0.04),
    deltaEtaCrackSearchWindow = cms.double(0.25),
    deltaEtaSearchWindow = cms.double(0.2),
    deltaPhiSearchWindow = cms.double(0.25),
    scaleDT = cms.bool(True)
)


process.hltL2SelectorForL3IO = cms.EDProducer("HLTMuonL2SelectorForL3IO",
    InputLinks = cms.InputTag("hltIterL3OIL3MuonsLinksCombination"),
    MaxNormalizedChi2 = cms.double(20.0),
    MaxPtDifference = cms.double(0.3),
    MinNhits = cms.int32(1),
    MinNmuonHits = cms.int32(1),
    applyL3Filters = cms.bool(False),
    l2Src = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
    l3OISrc = cms.InputTag("hltIterL3OIL3MuonCandidates")
)


process.hltL2SelectorForL3IONoVtx = cms.EDProducer("HLTMuonL2SelectorForL3IO",
    InputLinks = cms.InputTag("hltIterL3OIL3MuonsLinksCombinationNoVtx"),
    MaxNormalizedChi2 = cms.double(20.0),
    MaxPtDifference = cms.double(0.3),
    MinNhits = cms.int32(1),
    MinNmuonHits = cms.int32(1),
    applyL3Filters = cms.bool(False),
    l2Src = cms.InputTag("hltL2Muons"),
    l3OISrc = cms.InputTag("hltIterL3OIL3MuonCandidatesNoVtx")
)


process.hltL3MuonRelTrkIsolationVVL = cms.EDProducer("L3MuonCombinedRelativeIsolationProducer",
    CaloDepositsLabel = cms.InputTag("notUsed"),
    CaloExtractorPSet = cms.PSet(
        CaloTowerCollectionLabel = cms.InputTag("notUsed"),
        ComponentName = cms.string('CaloExtractor'),
        DR_Max = cms.double(0.3),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Vertex_Constraint_XY = cms.bool(False),
        Vertex_Constraint_Z = cms.bool(False),
        Weight_E = cms.double(1.0),
        Weight_H = cms.double(1.0)
    ),
    CutsPSet = cms.PSet(
        ComponentName = cms.string('SimpleCuts'),
        ConeSizes = cms.vdouble(0.3),
        EtaBounds = cms.vdouble(2.411),
        Thresholds = cms.vdouble(0.4),
        applyCutsORmaxNTracks = cms.bool(False),
        maxNTracks = cms.int32(-1)
    ),
    OutputMuIsoDeposits = cms.bool(True),
    TrackPt_Min = cms.double(-1.0),
    TrkExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('PixelTrackExtractor'),
        DR_Max = cms.double(0.3),
        DR_Veto = cms.double(0.01),
        DR_VetoPt = cms.double(0.025),
        DepositLabel = cms.untracked.string('PXLS'),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        PropagateTracksToRadius = cms.bool(False),
        PtVeto_Min = cms.double(2.0),
        Pt_Min = cms.double(-1.0),
        ReferenceRadius = cms.double(6.0),
        VetoLeadingTrack = cms.bool(False),
        inputTrackCollection = cms.InputTag("hltIter0L3MuonTrackSelectionHighPurity")
    ),
    UseCaloIso = cms.bool(False),
    UseRhoCorrectedCaloDeposits = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3MuonCandidates"),
    printDebug = cms.bool(False)
)


process.hltL3MuonsIterL3IO = cms.EDProducer("L3MuonProducer",
    L3TrajBuilderParameters = cms.PSet(
        GlbRefitterParameters = cms.PSet(
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            Chi2CutCSC = cms.double(150.0),
            Chi2CutDT = cms.double(10.0),
            Chi2CutGEM = cms.double(1.0),
            Chi2CutRPC = cms.double(1.0),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            DYTthrs = cms.vint32(30, 15),
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            GEMRecHitLabel = cms.InputTag("hltGemRecHits"),
            HitThreshold = cms.int32(1),
            MuonHitsOption = cms.int32(1),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            PropDirForCosmics = cms.bool(False),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitFlag = cms.bool(True),
            RefitRPCHits = cms.bool(True),
            SkipStation = cms.int32(-1),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
            TrackerSkipSection = cms.int32(-1),
            TrackerSkipSystem = cms.int32(-1)
        ),
        GlobalMuonTrackMatcher = cms.PSet(
            Chi2Cut_1 = cms.double(50.0),
            Chi2Cut_2 = cms.double(50.0),
            Chi2Cut_3 = cms.double(200.0),
            DeltaDCut_1 = cms.double(40.0),
            DeltaDCut_2 = cms.double(10.0),
            DeltaDCut_3 = cms.double(15.0),
            DeltaRCut_1 = cms.double(0.1),
            DeltaRCut_2 = cms.double(0.2),
            DeltaRCut_3 = cms.double(1.0),
            Eta_threshold = cms.double(1.2),
            LocChi2Cut = cms.double(0.001),
            MinP = cms.double(2.5),
            MinPt = cms.double(1.0),
            Propagator = cms.string('hltESPSmartPropagator'),
            Pt_threshold1 = cms.double(0.0),
            Pt_threshold2 = cms.double(999999999.0),
            Quality_1 = cms.double(20.0),
            Quality_2 = cms.double(15.0),
            Quality_3 = cms.double(7.0)
        ),
        MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
        MuonTrackingRegionBuilder = cms.PSet(
            DeltaEta = cms.double(0.04),
            DeltaPhi = cms.double(0.15),
            DeltaR = cms.double(0.025),
            DeltaZ = cms.double(24.2),
            EtaR_UpperLimit_Par1 = cms.double(0.25),
            EtaR_UpperLimit_Par2 = cms.double(0.15),
            Eta_fixed = cms.bool(True),
            Eta_min = cms.double(0.1),
            MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
            OnDemand = cms.int32(-1),
            PhiR_UpperLimit_Par1 = cms.double(0.6),
            PhiR_UpperLimit_Par2 = cms.double(0.2),
            Phi_fixed = cms.bool(True),
            Phi_min = cms.double(0.1),
            Pt_fixed = cms.bool(True),
            Pt_min = cms.double(3.0),
            Rescale_Dz = cms.double(4.0),
            Rescale_eta = cms.double(3.0),
            Rescale_phi = cms.double(3.0),
            UseVertex = cms.bool(False),
            Z_fixed = cms.bool(True),
            beamSpot = cms.InputTag("hltOnlineBeamSpot"),
            input = cms.InputTag("hltL2SelectorForL3IO"),
            maxRegions = cms.int32(2),
            precise = cms.bool(True),
            vertexCollection = cms.InputTag("pixelVertices")
        ),
        PCut = cms.double(2.5),
        PtCut = cms.double(1.0),
        RefitRPCHits = cms.bool(True),
        ScaleTECxFactor = cms.double(-1.0),
        ScaleTECyFactor = cms.double(-1.0),
        TrackTransformer = cms.PSet(
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitRPCHits = cms.bool(True),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle')
        ),
        TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
        TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        matchToSeeds = cms.bool(True),
        tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackSelectionHighPurity"),
        tkTrajMaxChi2 = cms.double(9999.0),
        tkTrajMaxDXYBeamSpot = cms.double(9999.0),
        tkTrajUseVertex = cms.bool(False),
        tkTrajVertex = cms.InputTag("hltTrimmedPixelVertices")
    ),
    MuonCollectionLabel = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring(
            'hltESPSmartPropagatorAny',
            'SteppingHelixPropagatorAny',
            'hltESPSmartPropagator',
            'hltESPSteppingHelixPropagatorOpposite'
        ),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        DoSmoothing = cms.bool(False),
        MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
        MuonUpdatorAtVertexParameters = cms.PSet(
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
            MaxChi2 = cms.double(1000000.0),
            Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
        ),
        PutTkTrackIntoEvent = cms.untracked.bool(False),
        SmoothTkTrack = cms.untracked.bool(False),
        Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        VertexConstraint = cms.bool(False),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )
)


process.hltL3MuonsIterL3IONoVtx = cms.EDProducer("L3MuonProducer",
    L3TrajBuilderParameters = cms.PSet(
        GlbRefitterParameters = cms.PSet(
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            Chi2CutCSC = cms.double(150.0),
            Chi2CutDT = cms.double(10.0),
            Chi2CutRPC = cms.double(1.0),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            DYTthrs = cms.vint32(30, 15),
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            HitThreshold = cms.int32(1),
            MuonHitsOption = cms.int32(1),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            PropDirForCosmics = cms.bool(False),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitFlag = cms.bool(True),
            RefitRPCHits = cms.bool(True),
            SkipStation = cms.int32(-1),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
            TrackerSkipSection = cms.int32(-1),
            TrackerSkipSystem = cms.int32(-1)
        ),
        GlobalMuonTrackMatcher = cms.PSet(
            Chi2Cut_1 = cms.double(50.0),
            Chi2Cut_2 = cms.double(50.0),
            Chi2Cut_3 = cms.double(200.0),
            DeltaDCut_1 = cms.double(40.0),
            DeltaDCut_2 = cms.double(10.0),
            DeltaDCut_3 = cms.double(15.0),
            DeltaRCut_1 = cms.double(0.1),
            DeltaRCut_2 = cms.double(0.2),
            DeltaRCut_3 = cms.double(1.0),
            Eta_threshold = cms.double(1.2),
            LocChi2Cut = cms.double(0.001),
            MinP = cms.double(2.5),
            MinPt = cms.double(1.0),
            Propagator = cms.string('hltESPSmartPropagator'),
            Pt_threshold1 = cms.double(0.0),
            Pt_threshold2 = cms.double(999999999.0),
            Quality_1 = cms.double(20.0),
            Quality_2 = cms.double(15.0),
            Quality_3 = cms.double(7.0)
        ),
        MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
        MuonTrackingRegionBuilder = cms.PSet(
            DeltaEta = cms.double(0.04),
            DeltaPhi = cms.double(0.15),
            DeltaR = cms.double(0.025),
            DeltaZ = cms.double(24.2),
            EtaR_UpperLimit_Par1 = cms.double(0.25),
            EtaR_UpperLimit_Par2 = cms.double(0.15),
            Eta_fixed = cms.bool(True),
            Eta_min = cms.double(0.1),
            MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
            OnDemand = cms.int32(-1),
            PhiR_UpperLimit_Par1 = cms.double(0.6),
            PhiR_UpperLimit_Par2 = cms.double(0.2),
            Phi_fixed = cms.bool(True),
            Phi_min = cms.double(0.1),
            Pt_fixed = cms.bool(True),
            Pt_min = cms.double(3.0),
            Rescale_Dz = cms.double(4.0),
            Rescale_eta = cms.double(3.0),
            Rescale_phi = cms.double(3.0),
            UseVertex = cms.bool(False),
            Z_fixed = cms.bool(True),
            beamSpot = cms.InputTag("hltOnlineBeamSpot"),
            input = cms.InputTag("hltL2SelectorForL3IONoVtx"),
            maxRegions = cms.int32(2),
            precise = cms.bool(True),
            vertexCollection = cms.InputTag("pixelVertices")
        ),
        PCut = cms.double(2.5),
        PtCut = cms.double(1.0),
        RefitRPCHits = cms.bool(True),
        ScaleTECxFactor = cms.double(-1.0),
        ScaleTECyFactor = cms.double(-1.0),
        TrackTransformer = cms.PSet(
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitRPCHits = cms.bool(True),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle')
        ),
        TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
        TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        matchToSeeds = cms.bool(True),
        tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackSelectionHighPurityNoVtx"),
        tkTrajMaxChi2 = cms.double(9999.0),
        tkTrajMaxDXYBeamSpot = cms.double(9999.0),
        tkTrajUseVertex = cms.bool(False),
        tkTrajVertex = cms.InputTag("hltTrimmedPixelVertices")
    ),
    MuonCollectionLabel = cms.InputTag("hltL2Muons"),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring(
            'hltESPSmartPropagatorAny',
            'SteppingHelixPropagatorAny',
            'hltESPSmartPropagator',
            'hltESPSteppingHelixPropagatorOpposite'
        ),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        DoSmoothing = cms.bool(False),
        MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
        MuonUpdatorAtVertexParameters = cms.PSet(
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
            MaxChi2 = cms.double(1000000.0),
            Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
        ),
        PutTkTrackIntoEvent = cms.untracked.bool(False),
        SmoothTkTrack = cms.untracked.bool(False),
        Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        VertexConstraint = cms.bool(False),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )
)


process.hltL3MuonsIterL3Links = cms.EDProducer("MuonLinksProducer",
    inputCollection = cms.InputTag("hltIterL3Muons")
)


process.hltL3MuonsIterL3LinksNoVtx = cms.EDProducer("MuonLinksProducerForHLT",
    InclusiveTrackerTrackCollection = cms.InputTag("hltIterL3MuonAndMuonFromL1MergedNoVtx"),
    LinkCollection = cms.InputTag("hltIterL3MuonsFromL2LinksCombinationNoVtx"),
    pMin = cms.double(2.5),
    ptMin = cms.double(2.5),
    shareHitFraction = cms.double(0.19)
)


process.hltL3MuonsIterL3OI = cms.EDProducer("L3MuonProducer",
    L3TrajBuilderParameters = cms.PSet(
        GlbRefitterParameters = cms.PSet(
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            Chi2CutCSC = cms.double(150.0),
            Chi2CutDT = cms.double(10.0),
            Chi2CutGEM = cms.double(1.0),
            Chi2CutRPC = cms.double(1.0),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            DYTthrs = cms.vint32(30, 15),
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            GEMRecHitLabel = cms.InputTag("hltGemRecHits"),
            HitThreshold = cms.int32(1),
            MuonHitsOption = cms.int32(1),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            PropDirForCosmics = cms.bool(False),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitFlag = cms.bool(True),
            RefitRPCHits = cms.bool(True),
            SkipStation = cms.int32(-1),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
            TrackerSkipSection = cms.int32(-1),
            TrackerSkipSystem = cms.int32(-1)
        ),
        GlobalMuonTrackMatcher = cms.PSet(
            Chi2Cut_1 = cms.double(50.0),
            Chi2Cut_2 = cms.double(50.0),
            Chi2Cut_3 = cms.double(200.0),
            DeltaDCut_1 = cms.double(40.0),
            DeltaDCut_2 = cms.double(10.0),
            DeltaDCut_3 = cms.double(15.0),
            DeltaRCut_1 = cms.double(0.1),
            DeltaRCut_2 = cms.double(0.2),
            DeltaRCut_3 = cms.double(1.0),
            Eta_threshold = cms.double(1.2),
            LocChi2Cut = cms.double(0.001),
            MinP = cms.double(2.5),
            MinPt = cms.double(1.0),
            Propagator = cms.string('hltESPSmartPropagator'),
            Pt_threshold1 = cms.double(0.0),
            Pt_threshold2 = cms.double(999999999.0),
            Quality_1 = cms.double(20.0),
            Quality_2 = cms.double(15.0),
            Quality_3 = cms.double(7.0)
        ),
        MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
        MuonTrackingRegionBuilder = cms.PSet(
            DeltaEta = cms.double(0.2),
            DeltaPhi = cms.double(0.15),
            DeltaR = cms.double(0.025),
            DeltaZ = cms.double(24.2),
            EtaR_UpperLimit_Par1 = cms.double(0.25),
            EtaR_UpperLimit_Par2 = cms.double(0.15),
            Eta_fixed = cms.bool(True),
            Eta_min = cms.double(0.1),
            MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
            OnDemand = cms.int32(-1),
            PhiR_UpperLimit_Par1 = cms.double(0.6),
            PhiR_UpperLimit_Par2 = cms.double(0.2),
            Phi_fixed = cms.bool(True),
            Phi_min = cms.double(0.1),
            Pt_fixed = cms.bool(False),
            Pt_min = cms.double(3.0),
            Rescale_Dz = cms.double(4.0),
            Rescale_eta = cms.double(3.0),
            Rescale_phi = cms.double(3.0),
            UseVertex = cms.bool(False),
            Z_fixed = cms.bool(False),
            beamSpot = cms.InputTag("hltOnlineBeamSpot"),
            input = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
            maxRegions = cms.int32(2),
            precise = cms.bool(True),
            vertexCollection = cms.InputTag("pixelVertices")
        ),
        PCut = cms.double(2.5),
        PtCut = cms.double(1.0),
        RefitRPCHits = cms.bool(True),
        ScaleTECxFactor = cms.double(-1.0),
        ScaleTECyFactor = cms.double(-1.0),
        TrackTransformer = cms.PSet(
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitRPCHits = cms.bool(True),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle')
        ),
        TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
        TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        tkTrajLabel = cms.InputTag("hltIterL3OIMuonTrackSelectionHighPurity"),
        tkTrajMaxChi2 = cms.double(9999.0),
        tkTrajMaxDXYBeamSpot = cms.double(9999.0),
        tkTrajUseVertex = cms.bool(False),
        tkTrajVertex = cms.InputTag("Notused")
    ),
    MuonCollectionLabel = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring(
            'hltESPSmartPropagatorAny',
            'SteppingHelixPropagatorAny',
            'hltESPSmartPropagator',
            'hltESPSteppingHelixPropagatorOpposite'
        ),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        DoSmoothing = cms.bool(True),
        MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
        MuonUpdatorAtVertexParameters = cms.PSet(
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
            MaxChi2 = cms.double(1000000.0),
            Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
        ),
        PutTkTrackIntoEvent = cms.untracked.bool(False),
        SmoothTkTrack = cms.untracked.bool(False),
        Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        VertexConstraint = cms.bool(False),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )
)


process.hltL3MuonsIterL3OINoVtx = cms.EDProducer("L3MuonProducer",
    L3TrajBuilderParameters = cms.PSet(
        GlbRefitterParameters = cms.PSet(
            CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
            Chi2CutCSC = cms.double(150.0),
            Chi2CutDT = cms.double(10.0),
            Chi2CutRPC = cms.double(1.0),
            DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
            DYTthrs = cms.vint32(30, 15),
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            HitThreshold = cms.int32(1),
            MuonHitsOption = cms.int32(1),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            PropDirForCosmics = cms.bool(False),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitFlag = cms.bool(True),
            RefitRPCHits = cms.bool(True),
            SkipStation = cms.int32(-1),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
            TrackerSkipSection = cms.int32(-1),
            TrackerSkipSystem = cms.int32(-1)
        ),
        GlobalMuonTrackMatcher = cms.PSet(
            Chi2Cut_1 = cms.double(50.0),
            Chi2Cut_2 = cms.double(50.0),
            Chi2Cut_3 = cms.double(200.0),
            DeltaDCut_1 = cms.double(40.0),
            DeltaDCut_2 = cms.double(10.0),
            DeltaDCut_3 = cms.double(15.0),
            DeltaRCut_1 = cms.double(0.1),
            DeltaRCut_2 = cms.double(0.2),
            DeltaRCut_3 = cms.double(1.0),
            Eta_threshold = cms.double(1.2),
            LocChi2Cut = cms.double(0.001),
            MinP = cms.double(2.5),
            MinPt = cms.double(1.0),
            Propagator = cms.string('hltESPSmartPropagator'),
            Pt_threshold1 = cms.double(0.0),
            Pt_threshold2 = cms.double(999999999.0),
            Quality_1 = cms.double(20.0),
            Quality_2 = cms.double(15.0),
            Quality_3 = cms.double(7.0)
        ),
        MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
        MuonTrackingRegionBuilder = cms.PSet(
            DeltaEta = cms.double(0.2),
            DeltaPhi = cms.double(0.15),
            DeltaR = cms.double(0.025),
            DeltaZ = cms.double(24.2),
            EtaR_UpperLimit_Par1 = cms.double(0.25),
            EtaR_UpperLimit_Par2 = cms.double(0.15),
            Eta_fixed = cms.bool(True),
            Eta_min = cms.double(0.1),
            MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
            OnDemand = cms.int32(-1),
            PhiR_UpperLimit_Par1 = cms.double(0.6),
            PhiR_UpperLimit_Par2 = cms.double(0.2),
            Phi_fixed = cms.bool(True),
            Phi_min = cms.double(0.1),
            Pt_fixed = cms.bool(False),
            Pt_min = cms.double(3.0),
            Rescale_Dz = cms.double(4.0),
            Rescale_eta = cms.double(3.0),
            Rescale_phi = cms.double(3.0),
            UseVertex = cms.bool(False),
            Z_fixed = cms.bool(False),
            beamSpot = cms.InputTag("hltOnlineBeamSpot"),
            input = cms.InputTag("hltL2Muons"),
            maxRegions = cms.int32(2),
            precise = cms.bool(True),
            vertexCollection = cms.InputTag("pixelVertices")
        ),
        PCut = cms.double(2.5),
        PtCut = cms.double(1.0),
        RefitRPCHits = cms.bool(True),
        ScaleTECxFactor = cms.double(-1.0),
        ScaleTECyFactor = cms.double(-1.0),
        TrackTransformer = cms.PSet(
            DoPredictionsOnly = cms.bool(False),
            Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            Propagator = cms.string('hltESPSmartPropagatorAny'),
            RefitDirection = cms.string('insideOut'),
            RefitRPCHits = cms.bool(True),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle')
        ),
        TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
        TrackerRecHitBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        tkTrajLabel = cms.InputTag("hltIterL3OIMuonTrackSelectionHighPurityNoVtx"),
        tkTrajMaxChi2 = cms.double(9999.0),
        tkTrajMaxDXYBeamSpot = cms.double(9999.0),
        tkTrajUseVertex = cms.bool(False),
        tkTrajVertex = cms.InputTag("Notused")
    ),
    MuonCollectionLabel = cms.InputTag("hltL2Muons"),
    ServiceParameters = cms.PSet(
        Propagators = cms.untracked.vstring(
            'hltESPSmartPropagatorAny',
            'SteppingHelixPropagatorAny',
            'hltESPSmartPropagator',
            'hltESPSteppingHelixPropagatorOpposite'
        ),
        RPCLayers = cms.bool(True),
        UseMuonNavigation = cms.untracked.bool(True)
    ),
    TrackLoaderParameters = cms.PSet(
        DoSmoothing = cms.bool(True),
        MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
        MuonUpdatorAtVertexParameters = cms.PSet(
            BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
            MaxChi2 = cms.double(1000000.0),
            Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
        ),
        PutTkTrackIntoEvent = cms.untracked.bool(False),
        SmoothTkTrack = cms.untracked.bool(False),
        Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        VertexConstraint = cms.bool(False),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )
)


process.hltLightPFTracks = cms.EDProducer("LightPFTrackProducer",
    TkColList = cms.VInputTag("hltPFMuonMerging"),
    TrackQuality = cms.string('none'),
    UseQuality = cms.bool(False)
)


process.hltMeasurementTrackerEvent = cms.EDProducer("MeasurementTrackerEventProducer",
    Phase2TrackerCluster1DProducer = cms.string(''),
    badPixelFEDChannelCollectionLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    inactivePixelDetectorLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    inactiveStripDetectorLabels = cms.VInputTag("hltSiStripExcludedFEDListProducer"),
    measurementTracker = cms.string('hltESPMeasurementTracker'),
    pixelCablingMapLabel = cms.string(''),
    pixelClusterProducer = cms.string('hltSiPixelClusters'),
    skipClusters = cms.InputTag(""),
    stripClusterProducer = cms.string('hltSiStripRawToClustersFacility'),
    switchOffPixelsIfEmpty = cms.bool(True),
    vectorHits = cms.InputTag(""),
    vectorHitsRej = cms.InputTag("")
)


process.hltMeasurementTrackerEventOnDemand = cms.EDProducer("MeasurementTrackerEventProducer",
    Phase2TrackerCluster1DProducer = cms.string(''),
    badPixelFEDChannelCollectionLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    inactivePixelDetectorLabels = cms.VInputTag("hltSiPixelDigiErrors"),
    inactiveStripDetectorLabels = cms.VInputTag("hltSiStripExcludedFEDListProducer"),
    measurementTracker = cms.string('hltESPMeasurementTracker'),
    pixelCablingMapLabel = cms.string(''),
    pixelClusterProducer = cms.string('hltSiPixelClusters'),
    skipClusters = cms.InputTag(""),
    stripClusterProducer = cms.string('hltSiStripRawToClustersFacilityOnDemand'),
    switchOffPixelsIfEmpty = cms.bool(True),
    vectorHits = cms.InputTag(""),
    vectorHitsRej = cms.InputTag("")
)


process.hltMergedTracks = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIter0PFlowTrackSelectionHighPurity", "hltDoubletRecoveryPFlowTrackSelectionHighPurity"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIter0PFlowTrackSelectionHighPurity", "hltDoubletRecoveryPFlowTrackSelectionHighPurity"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltMuonCSCDigis = cms.EDProducer("CSCDCCUnpacker",
    B904Setup = cms.untracked.bool(False),
    B904dmb = cms.untracked.int32(3),
    B904vmecrate = cms.untracked.int32(1),
    Debug = cms.untracked.bool(False),
    DisableMappingCheck = cms.untracked.bool(False),
    ErrorMask = cms.uint32(0),
    ExaminerMask = cms.uint32(535558134),
    FormatedEventDump = cms.untracked.bool(False),
    InputObjects = cms.InputTag("rawDataCollector"),
    PrintEventNumber = cms.untracked.bool(False),
    SuppressZeroLCT = cms.untracked.bool(True),
    UnpackStatusDigis = cms.bool(False),
    UseExaminer = cms.bool(True),
    UseFormatStatus = cms.bool(True),
    UseSelectiveUnpacking = cms.bool(True),
    VisualFEDInspect = cms.untracked.bool(False),
    VisualFEDShort = cms.untracked.bool(False),
    runDQM = cms.untracked.bool(False),
    useCSCShowers = cms.bool(False),
    useGEMs = cms.bool(False),
    useRPCs = cms.bool(False)
)


process.hltMuonDTDigis = cms.EDProducer("DTuROSRawToDigi",
    debug = cms.untracked.bool(False),
    inputLabel = cms.InputTag("rawDataCollector")
)


process.hltMuonEcalMFPFClusterIsoForMuons = cms.EDProducer("MuonHLTEcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doRhoCorrection = cms.bool(True),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.05),
    drVetoEndcap = cms.double(0.05),
    effectiveAreas = cms.vdouble(0.58, 0.35),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducer = cms.InputTag("hltParticleFlowClusterECALForMuonsMF"),
    recoCandidateProducer = cms.InputTag("hltIterL3MuonCandidates"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetECALMFForMuons"),
    rhoScale = cms.double(1.0)
)


process.hltMuonEcalMFPFClusterIsoForMuonsNoVtx = cms.EDProducer("MuonHLTEcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doRhoCorrection = cms.bool(True),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.05),
    drVetoEndcap = cms.double(0.05),
    effectiveAreas = cms.vdouble(0.35, 0.193),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducer = cms.InputTag("hltParticleFlowClusterECALForMuonsMFNoVtx"),
    recoCandidateProducer = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetECALMFForMuons"),
    rhoScale = cms.double(1.0)
)


process.hltMuonGEMDigis = cms.EDProducer("GEMRawToDigiModule",
    InputLabel = cms.InputTag("rawDataCollector"),
    fedIdEnd = cms.uint32(1478),
    fedIdStart = cms.uint32(1467),
    ge21Off = cms.bool(True),
    keepDAQStatus = cms.bool(False),
    readMultiBX = cms.bool(False),
    useDBEMap = cms.bool(True)
)


process.hltMuonHcalPFClusterIsoForMuonsNoVtx = cms.EDProducer("MuonHLTHcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doEffAreaCorrection = cms.bool(False),
    doRhoCorrection = cms.bool(True),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.1),
    drVetoEndcap = cms.double(0.1),
    effectiveAreas = cms.vdouble(0.11, 0.163),
    effectiveAreasCorr = cms.vdouble(0.0, 0.0),
    effectiveAreasThres = cms.vdouble(0.0, 0.0),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducerHCAL = cms.InputTag("hltParticleFlowClusterHCAL"),
    pfClusterProducerHFEM = cms.InputTag(""),
    pfClusterProducerHFHAD = cms.InputTag(""),
    recoCandidateProducer = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetAllCalo"),
    rhoScale = cms.double(1.0),
    useEt = cms.bool(True),
    useHF = cms.bool(False)
)


process.hltMuonHcalRegPFClusterIsoForMuons = cms.EDProducer("MuonHLTHcalPFClusterIsolationProducer",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    doEffAreaCorrection = cms.bool(True),
    doRhoCorrection = cms.bool(True),
    drMax = cms.double(0.3),
    drVetoBarrel = cms.double(0.1),
    drVetoEndcap = cms.double(0.1),
    effectiveAreas = cms.vdouble(0.227, 0.372),
    effectiveAreasCorr = cms.vdouble(0.594, 0.64),
    effectiveAreasThres = cms.vdouble(9.0, 9.0),
    energyBarrel = cms.double(0.0),
    energyEndcap = cms.double(0.0),
    etaStripBarrel = cms.double(0.0),
    etaStripEndcap = cms.double(0.0),
    pfClusterProducerHCAL = cms.InputTag("hltParticleFlowClusterHCAL"),
    pfClusterProducerHFEM = cms.InputTag(""),
    pfClusterProducerHFHAD = cms.InputTag(""),
    recoCandidateProducer = cms.InputTag("hltIterL3MuonCandidates"),
    rhoMax = cms.double(99999999.0),
    rhoProducer = cms.InputTag("hltFixedGridRhoFastjetHCAL"),
    rhoScale = cms.double(1.0),
    useEt = cms.bool(True),
    useHF = cms.bool(False)
)


process.hltMuonLinks = cms.EDProducer("MuonLinksProducerForHLT",
    InclusiveTrackerTrackCollection = cms.InputTag("hltPFMuonMerging"),
    LinkCollection = cms.InputTag("hltL3MuonsIterL3Links"),
    pMin = cms.double(2.5),
    ptMin = cms.double(2.5),
    shareHitFraction = cms.double(0.8)
)


process.hltMuonRPCDigis = cms.EDProducer("RPCDigiMerger",
    InputLabel = cms.InputTag("rawDataCollector"),
    bxMaxCPPF = cms.int32(2),
    bxMaxOMTF = cms.int32(4),
    bxMaxTwinMux = cms.int32(2),
    bxMinCPPF = cms.int32(-2),
    bxMinOMTF = cms.int32(-3),
    bxMinTwinMux = cms.int32(-2),
    inputTagCPPFDigis = cms.InputTag("hltMuonRPCDigisCPPF"),
    inputTagOMTFDigis = cms.InputTag("hltOmtfDigis"),
    inputTagSimRPCDigis = cms.InputTag(""),
    inputTagTwinMuxDigis = cms.InputTag("hltMuonRPCDigisTwinMux")
)


process.hltMuonRPCDigisCPPF = cms.EDProducer("RPCAMCRawToDigi",
    RPCAMCUnpacker = cms.string('RPCCPPFUnpacker'),
    RPCAMCUnpackerSettings = cms.PSet(
        bxMax = cms.int32(2),
        bxMin = cms.int32(-2),
        cppfDaqDelay = cms.int32(2),
        fillAMCCounters = cms.bool(True)
    ),
    calculateCRC = cms.bool(True),
    fillCounters = cms.bool(True),
    inputTag = cms.InputTag("rawDataCollector")
)


process.hltMuonRPCDigisTwinMux = cms.EDProducer("RPCTwinMuxRawToDigi",
    bxMax = cms.int32(2),
    bxMin = cms.int32(-2),
    calculateCRC = cms.bool(True),
    fillCounters = cms.bool(True),
    inputTag = cms.InputTag("rawDataCollector")
)


process.hltMuonTkRelIsolationCut0p09MapNoVtx = cms.EDProducer("L3MuonCombinedRelativeIsolationProducer",
    CaloDepositsLabel = cms.InputTag("notUsed"),
    CaloExtractorPSet = cms.PSet(
        CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
        ComponentName = cms.string('CaloExtractor'),
        DR_Max = cms.double(0.3),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Vertex_Constraint_XY = cms.bool(False),
        Vertex_Constraint_Z = cms.bool(False),
        Weight_E = cms.double(1.0),
        Weight_H = cms.double(1.0)
    ),
    CutsPSet = cms.PSet(
        ComponentName = cms.string('SimpleCuts'),
        ConeSizes = cms.vdouble(0.3),
        EtaBounds = cms.vdouble(2.411),
        Thresholds = cms.vdouble(0.09),
        applyCutsORmaxNTracks = cms.bool(False),
        maxNTracks = cms.int32(-1)
    ),
    OutputMuIsoDeposits = cms.bool(True),
    TrackPt_Min = cms.double(-1.0),
    TrkExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('PixelTrackExtractor'),
        DR_Max = cms.double(0.3),
        DR_Veto = cms.double(0.01),
        DR_VetoPt = cms.double(0.025),
        DepositLabel = cms.untracked.string('PXLS'),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        PropagateTracksToRadius = cms.bool(True),
        PtVeto_Min = cms.double(2.0),
        Pt_Min = cms.double(-1.0),
        ReferenceRadius = cms.double(6.0),
        VetoLeadingTrack = cms.bool(True),
        inputTrackCollection = cms.InputTag("hltIter0L3MuonTrackSelectionHighPurityNoVtx")
    ),
    UseCaloIso = cms.bool(False),
    UseRhoCorrectedCaloDeposits = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    printDebug = cms.bool(False)
)


process.hltMuonTkRelIsolationCut0p14Map = cms.EDProducer("L3MuonCombinedRelativeIsolationProducer",
    CaloDepositsLabel = cms.InputTag("notUsed"),
    CaloExtractorPSet = cms.PSet(
        CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
        ComponentName = cms.string('CaloExtractor'),
        DR_Max = cms.double(0.3),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DepositLabel = cms.untracked.string('EcalPlusHcal'),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Vertex_Constraint_XY = cms.bool(False),
        Vertex_Constraint_Z = cms.bool(False),
        Weight_E = cms.double(1.0),
        Weight_H = cms.double(1.0)
    ),
    CutsPSet = cms.PSet(
        ComponentName = cms.string('SimpleCuts'),
        ConeSizes = cms.vdouble(0.3),
        EtaBounds = cms.vdouble(2.411),
        Thresholds = cms.vdouble(0.14),
        applyCutsORmaxNTracks = cms.bool(False),
        maxNTracks = cms.int32(-1)
    ),
    OutputMuIsoDeposits = cms.bool(True),
    TrackPt_Min = cms.double(-1.0),
    TrkExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('PixelTrackExtractor'),
        DR_Max = cms.double(0.3),
        DR_Veto = cms.double(0.01),
        DR_VetoPt = cms.double(0.025),
        DepositLabel = cms.untracked.string('PXLS'),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        PropagateTracksToRadius = cms.bool(True),
        PtVeto_Min = cms.double(2.0),
        Pt_Min = cms.double(-1.0),
        ReferenceRadius = cms.double(6.0),
        VetoLeadingTrack = cms.bool(True),
        inputTrackCollection = cms.InputTag("hltIter0L3MuonTrackSelectionHighPurity")
    ),
    UseCaloIso = cms.bool(False),
    UseRhoCorrectedCaloDeposits = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3MuonCandidates"),
    printDebug = cms.bool(False)
)


process.hltMuons = cms.EDProducer("MuonIdProducer",
    CaloExtractorPSet = cms.PSet(
        CenterConeOnCalIntersection = cms.bool(False),
        ComponentName = cms.string('CaloExtractorByAssociator'),
        DR_Max = cms.double(1.0),
        DR_Veto_E = cms.double(0.07),
        DR_Veto_H = cms.double(0.1),
        DR_Veto_HO = cms.double(0.1),
        DepositInstanceLabels = cms.vstring(
            'ecal',
            'hcal',
            'ho'
        ),
        DepositLabel = cms.untracked.string('Cal'),
        NoiseTow_EB = cms.double(0.04),
        NoiseTow_EE = cms.double(0.15),
        Noise_EB = cms.double(0.025),
        Noise_EE = cms.double(0.1),
        Noise_HB = cms.double(0.2),
        Noise_HE = cms.double(0.2),
        Noise_HO = cms.double(0.2),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold_E = cms.double(0.2),
        Threshold_H = cms.double(0.5),
        Threshold_HO = cms.double(0.5),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
            EERecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
            HBHERecHitCollectionLabel = cms.InputTag("hltHbhereco"),
            HORecHitCollectionLabel = cms.InputTag("hltHoreco"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(1.0),
            dREcalPreselection = cms.double(1.0),
            dRHcal = cms.double(1.0),
            dRHcalPreselection = cms.double(1.0),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        ),
        UseRecHitsFlag = cms.bool(False)
    ),
    JetExtractorPSet = cms.PSet(
        ComponentName = cms.string('JetExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.1),
        ExcludeMuonVeto = cms.bool(True),
        JetCollectionLabel = cms.InputTag("hltAK4CaloJetsPFEt5"),
        PrintTimeReport = cms.untracked.bool(False),
        PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(False),
            UseMuonNavigation = cms.untracked.bool(False)
        ),
        Threshold = cms.double(5.0),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
            EERecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
            HBHERecHitCollectionLabel = cms.InputTag("hltHbhereco"),
            HORecHitCollectionLabel = cms.InputTag("hltHoreco"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(0.5),
            dREcalPreselection = cms.double(0.5),
            dRHcal = cms.double(0.5),
            dRHcalPreselection = cms.double(0.5),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(True),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(False),
            usePreshower = cms.bool(False)
        )
    ),
    MuonCaloCompatibility = cms.PSet(
        MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root'),
        PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root'),
        allSiPMHO = cms.bool(False),
        delta_eta = cms.double(0.02),
        delta_phi = cms.double(0.02)
    ),
    ShowerDigiFillerParameters = cms.PSet(
        cscDigiCollectionLabel = cms.InputTag("hltMuonCSCDigis","MuonCSCStripDigi"),
        digiMaxDistanceX = cms.double(25.0),
        dtDigiCollectionLabel = cms.InputTag("hltMuonDTDigis")
    ),
    TimingFillerParameters = cms.PSet(
        CSCTimingParameters = cms.PSet(
            CSCStripError = cms.double(7.0),
            CSCStripTimeOffset = cms.double(0.0),
            CSCTimeOffset = cms.double(0.0),
            CSCWireError = cms.double(8.6),
            CSCWireTimeOffset = cms.double(0.0),
            CSCsegments = cms.InputTag("hltCscSegments"),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(100.0),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseStripTime = cms.bool(True),
            UseWireTime = cms.bool(True),
            debug = cms.bool(False)
        ),
        DTTimingParameters = cms.PSet(
            DTTimeOffset = cms.double(2.7),
            DTsegments = cms.InputTag("hltDt4DSegments"),
            DoWireCorr = cms.bool(False),
            DropTheta = cms.bool(True),
            HitError = cms.double(6.0),
            HitsMin = cms.int32(5),
            MatchParameters = cms.PSet(
                CSCsegments = cms.InputTag("hltCscSegments"),
                DTradius = cms.double(0.01),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                TightMatchCSC = cms.bool(True),
                TightMatchDT = cms.bool(False)
            ),
            PruneCut = cms.double(10000.0),
            RequireBothProjections = cms.bool(False),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(True)
            ),
            UseSegmentT0 = cms.bool(False),
            debug = cms.bool(False)
        ),
        EcalEnergyCut = cms.double(0.4),
        ErrorCSC = cms.double(7.4),
        ErrorDT = cms.double(6.0),
        ErrorEB = cms.double(2.085),
        ErrorEE = cms.double(6.95),
        UseCSC = cms.bool(True),
        UseDT = cms.bool(True),
        UseECAL = cms.bool(True)
    ),
    TrackAssociatorParameters = cms.PSet(
        CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
        CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
        DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
        EBRecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        EERecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        HBHERecHitCollectionLabel = cms.InputTag("hltHbhereco"),
        HORecHitCollectionLabel = cms.InputTag("hltHoreco"),
        accountForTrajectoryChangeCalo = cms.bool(False),
        dREcal = cms.double(9999.0),
        dREcalPreselection = cms.double(0.05),
        dRHcal = cms.double(9999.0),
        dRHcalPreselection = cms.double(0.2),
        dRMuon = cms.double(9999.0),
        dRMuonPreselection = cms.double(0.2),
        dRPreshowerPreselection = cms.double(0.2),
        muonMaxDistanceSigmaX = cms.double(0.0),
        muonMaxDistanceSigmaY = cms.double(0.0),
        muonMaxDistanceX = cms.double(5.0),
        muonMaxDistanceY = cms.double(5.0),
        propagateAllDirections = cms.bool(True),
        trajectoryUncertaintyTolerance = cms.double(-1.0),
        truthMatch = cms.bool(False),
        useCalo = cms.bool(False),
        useEcal = cms.bool(True),
        useHO = cms.bool(True),
        useHcal = cms.bool(True),
        useMuon = cms.bool(True),
        usePreshower = cms.bool(False)
    ),
    TrackExtractorPSet = cms.PSet(
        BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        BeamlineOption = cms.string('BeamSpotFromEvent'),
        Chi2Ndof_Max = cms.double(1e+64),
        Chi2Prob_Min = cms.double(-1.0),
        ComponentName = cms.string('TrackExtractor'),
        DR_Max = cms.double(1.0),
        DR_Veto = cms.double(0.01),
        DepositLabel = cms.untracked.string(''),
        Diff_r = cms.double(0.1),
        Diff_z = cms.double(0.2),
        NHits_Min = cms.uint32(0),
        Pt_Min = cms.double(-1.0),
        inputTrackCollection = cms.InputTag("hltPFMuonMerging")
    ),
    TrackerKinkFinderParameters = cms.PSet(
        diagonalOnly = cms.bool(False),
        usePosition = cms.bool(False)
    ),
    addExtraSoftMuons = cms.bool(False),
    arbitrateTrackerMuons = cms.bool(False),
    arbitrationCleanerOptions = cms.PSet(
        ClusterDPhi = cms.double(0.6),
        ClusterDTheta = cms.double(0.02),
        Clustering = cms.bool(True),
        ME1a = cms.bool(True),
        Overlap = cms.bool(True),
        OverlapDPhi = cms.double(0.0786),
        OverlapDTheta = cms.double(0.02)
    ),
    debugWithTruthMatching = cms.bool(False),
    ecalDepositName = cms.string('ecal'),
    fillCaloCompatibility = cms.bool(True),
    fillEnergy = cms.bool(True),
    fillGlobalTrackQuality = cms.bool(False),
    fillGlobalTrackRefits = cms.bool(False),
    fillIsolation = cms.bool(True),
    fillMatching = cms.bool(True),
    fillShowerDigis = cms.bool(False),
    fillTrackerKink = cms.bool(False),
    globalTrackQualityInputTag = cms.InputTag(""),
    hcalDepositName = cms.string('hcal'),
    hoDepositName = cms.string('ho'),
    inputCollectionLabels = cms.VInputTag("hltPFMuonMerging", "hltMuonLinks", "hltL2Muons"),
    inputCollectionTypes = cms.vstring(
        'inner tracks',
        'links',
        'outer tracks'
    ),
    jetDepositName = cms.string('jets'),
    maxAbsDx = cms.double(3.0),
    maxAbsDy = cms.double(9999.0),
    maxAbsEta = cms.double(3.0),
    maxAbsPullX = cms.double(4.0),
    maxAbsPullY = cms.double(9999.0),
    minCaloCompatibility = cms.double(0.6),
    minNumberOfMatches = cms.int32(1),
    minP = cms.double(10.0),
    minPCaloMuon = cms.double(1000000000.0),
    minPt = cms.double(10.0),
    ptThresholdToFillCandidateP4WithGlobalFit = cms.double(200.0),
    pvInputTag = cms.InputTag(""),
    runArbitrationCleaner = cms.bool(False),
    selectHighPurity = cms.bool(False),
    sigmaThresholdToFillCandidateP4WithGlobalFit = cms.double(2.0),
    storeCrossedHcalRecHits = cms.bool(False),
    trackDepositName = cms.string('tracker'),
    writeIsoDeposits = cms.bool(False)
)


process.hltOmtfDigis = cms.EDProducer("OmtfUnpacker",
    inputLabel = cms.InputTag("rawDataCollector"),
    outputTag = cms.string(''),
    rpcConnectionFile = cms.string(''),
    skipCsc = cms.bool(False),
    skipDt = cms.bool(False),
    skipMuon = cms.bool(False),
    skipRpc = cms.bool(False),
    useRpcConnectionFile = cms.bool(False)
)


process.hltOnlineBeamSpot = cms.EDProducer("BeamSpotOnlineProducer",
    beamMode = cms.untracked.uint32(11),
    changeToCMSCoordinates = cms.bool(False),
    gtEvmLabel = cms.InputTag(""),
    maxRadius = cms.double(2.0),
    maxZ = cms.double(40.0),
    setSigmaZ = cms.double(0.0),
    sigmaXYThreshold = cms.double(4.0),
    sigmaZThreshold = cms.double(2.0),
    src = cms.InputTag(""),
    timeThreshold = cms.int32(48),
    useBSOnlineRecords = cms.bool(True)
)


process.hltOnlineBeamSpotDevice = cms.EDProducer("BeamSpotDeviceProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    src = cms.InputTag("hltOnlineBeamSpot")
)


process.hltOnlineMetaDataDigis = cms.EDProducer("OnlineMetaDataRawToDigi",
    onlineMetaDataInputLabel = cms.InputTag("rawDataCollector")
)


process.hltPFMETProducer = cms.EDProducer("PFMETProducer",
    alias = cms.string('hltPFMet'),
    applyWeight = cms.bool(False),
    calculateSignificance = cms.bool(False),
    globalThreshold = cms.double(0.0),
    parameters = cms.PSet(

    ),
    src = cms.InputTag("hltParticleFlow"),
    srcWeights = cms.InputTag("")
)


process.hltPFMuonMerging = cms.EDProducer("TrackListMerger",
    Epsilon = cms.double(-0.001),
    FoundHitBonus = cms.double(5.0),
    LostHitPenalty = cms.double(20.0),
    MaxNormalizedChisq = cms.double(1000.0),
    MinFound = cms.int32(3),
    MinPT = cms.double(0.05),
    ShareFrac = cms.double(0.19),
    TrackProducers = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracks"),
    allowFirstHitShare = cms.bool(True),
    copyExtras = cms.untracked.bool(True),
    copyMVA = cms.bool(False),
    hasSelector = cms.vint32(0, 0),
    indivShareFrac = cms.vdouble(1.0, 1.0),
    makeReKeyedSeeds = cms.untracked.bool(False),
    newQuality = cms.string('confirmed'),
    selectedTrackQuals = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracks"),
    setsToMerge = cms.VPSet(cms.PSet(
        pQual = cms.bool(False),
        tLists = cms.vint32(0, 1)
    )),
    trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
    writeOnlyTrkQuals = cms.bool(False)
)


process.hltParticleFlow = cms.EDProducer("PFProducer",
    GedElectronValueMap = cms.InputTag("gedGsfElectronsTmp"),
    GedPhotonValueMap = cms.InputTag("tmpGedPhotons","valMapPFEgammaCandToPhoton"),
    PFEGammaCandidates = cms.InputTag("particleFlowEGamma"),
    PFEGammaFiltersParameters = cms.PSet(
        electron_ecalDrivenHademPreselCut = cms.double(0.15),
        electron_iso_combIso_barrel = cms.double(10.0),
        electron_iso_combIso_endcap = cms.double(10.0),
        electron_iso_mva_barrel = cms.double(-0.1875),
        electron_iso_mva_endcap = cms.double(-0.1075),
        electron_iso_pt = cms.double(10.0),
        electron_maxElePtForOnlyMVAPresel = cms.double(50.0),
        electron_missinghits = cms.uint32(1),
        electron_noniso_mvaCut = cms.double(-0.1),
        electron_protectionsForBadHcal = cms.PSet(
            dEta = cms.vdouble(0.0064, 0.01264),
            dPhi = cms.vdouble(0.0547, 0.0394),
            eInvPInv = cms.vdouble(0.184, 0.0721),
            enableProtections = cms.bool(False),
            full5x5_sigmaIetaIeta = cms.vdouble(0.0106, 0.0387)
        ),
        electron_protectionsForJetMET = cms.PSet(
            maxDPhiIN = cms.double(0.1),
            maxE = cms.double(50.0),
            maxEcalEOverPRes = cms.double(0.2),
            maxEcalEOverP_1 = cms.double(0.5),
            maxEcalEOverP_2 = cms.double(0.2),
            maxEeleOverPout = cms.double(0.2),
            maxEeleOverPoutRes = cms.double(0.5),
            maxEleHcalEOverEcalE = cms.double(0.1),
            maxHcalE = cms.double(10.0),
            maxHcalEOverEcalE = cms.double(0.1),
            maxHcalEOverP = cms.double(1.0),
            maxNtracks = cms.double(3.0),
            maxTrackPOverEele = cms.double(1.0)
        ),
        photon_HoE = cms.double(0.05),
        photon_MinEt = cms.double(10.0),
        photon_SigmaiEtaiEta_barrel = cms.double(0.0125),
        photon_SigmaiEtaiEta_endcap = cms.double(0.034),
        photon_combIso = cms.double(10.0),
        photon_protectionsForBadHcal = cms.PSet(
            enableProtections = cms.bool(False),
            solidConeTrkIsoOffset = cms.double(10.0),
            solidConeTrkIsoSlope = cms.double(0.3)
        ),
        photon_protectionsForJetMET = cms.PSet(
            sumPtTrackIso = cms.double(4.0),
            sumPtTrackIsoSlope = cms.double(0.001)
        )
    ),
    PFHFCleaningParameters = cms.PSet(
        maxDeltaPhiPt = cms.double(7.0),
        maxSignificance = cms.double(2.5),
        minDeltaMet = cms.double(0.4),
        minHFCleaningPt = cms.double(5.0),
        minSignificance = cms.double(2.5),
        minSignificanceReduction = cms.double(1.4)
    ),
    PFMuonAlgoParameters = cms.PSet(

    ),
    blocks = cms.InputTag("hltParticleFlowBlock"),
    calibHF_a_EMHAD = cms.vdouble(
        1.42215, 1.00496, 0.68961, 0.81656, 0.98504,
        0.98504, 1.00802, 1.0593, 1.4576, 1.4576
    ),
    calibHF_a_EMonly = cms.vdouble(
        0.96945, 0.96701, 0.76309, 0.82268, 0.87583,
        0.89718, 0.98674, 1.4681, 1.458, 1.458
    ),
    calibHF_b_EMHAD = cms.vdouble(
        1.27541, 0.85361, 0.86333, 0.89091, 0.94348,
        0.94348, 0.9437, 1.0034, 1.0444, 1.0444
    ),
    calibHF_b_HADonly = cms.vdouble(
        1.27541, 0.85361, 0.86333, 0.89091, 0.94348,
        0.94348, 0.9437, 1.0034, 1.0444, 1.0444
    ),
    calibHF_eta_step = cms.vdouble(
        0.0, 2.9, 3.0, 3.2, 4.2,
        4.4, 4.6, 4.8, 5.2, 5.4
    ),
    calibHF_use = cms.bool(False),
    calibrationsLabel = cms.string('HLT'),
    cleanedHF = cms.VInputTag("hltParticleFlowRecHitHF:Cleaned", "hltParticleFlowClusterHF:Cleaned"),
    debug = cms.untracked.bool(False),
    dptRel_DispVtx = cms.double(10.0),
    egammaElectrons = cms.InputTag(""),
    factors_45 = cms.vdouble(10.0, 100.0),
    goodPixelTrackDeadHcal_chi2n = cms.double(2.0),
    goodPixelTrackDeadHcal_dxy = cms.double(0.02),
    goodPixelTrackDeadHcal_dz = cms.double(0.05),
    goodPixelTrackDeadHcal_maxLost3Hit = cms.int32(0),
    goodPixelTrackDeadHcal_maxLost4Hit = cms.int32(1),
    goodPixelTrackDeadHcal_maxPt = cms.double(50.0),
    goodPixelTrackDeadHcal_minEta = cms.double(2.3),
    goodPixelTrackDeadHcal_ptErrRel = cms.double(1.0),
    goodTrackDeadHcal_chi2n = cms.double(5.0),
    goodTrackDeadHcal_dxy = cms.double(0.5),
    goodTrackDeadHcal_layers = cms.uint32(4),
    goodTrackDeadHcal_ptErrRel = cms.double(0.2),
    goodTrackDeadHcal_validFr = cms.double(0.5),
    iCfgCandConnector = cms.PSet(
        bCalibPrimary = cms.bool(False),
        bCorrect = cms.bool(False),
        nuclCalibFactors = cms.vdouble(0.8, 0.15, 0.5, 0.5, 0.05)
    ),
    muon_ECAL = cms.vdouble(0.5, 0.5),
    muon_HCAL = cms.vdouble(3.0, 3.0),
    muon_HO = cms.vdouble(0.9, 0.9),
    muons = cms.InputTag("hltMuons"),
    nsigma_TRACK = cms.double(1.0),
    pf_nsigma_ECAL = cms.double(0.0),
    pf_nsigma_HCAL = cms.double(1.0),
    pf_nsigma_HFEM = cms.double(1.0),
    pf_nsigma_HFHAD = cms.double(1.0),
    postHFCleaning = cms.bool(False),
    postMuonCleaning = cms.bool(True),
    pt_Error = cms.double(1.0),
    rejectTracks_Bad = cms.bool(False),
    rejectTracks_Step45 = cms.bool(False),
    resolHF_square = cms.vdouble(7.834401, 0.012996, 0.0),
    useCalibrationsFromDB = cms.bool(True),
    useEGammaElectrons = cms.bool(False),
    useEGammaFilters = cms.bool(False),
    useHO = cms.bool(False),
    usePFConversions = cms.bool(False),
    usePFDecays = cms.bool(False),
    usePFNuclearInteractions = cms.bool(False),
    useProtectionsForJetMET = cms.bool(True),
    useVerticesForNeutral = cms.bool(True),
    verbose = cms.untracked.bool(False),
    vertexCollection = cms.InputTag("hltPixelVertices"),
    vetoEndcap = cms.bool(False)
)


process.hltParticleFlowBlock = cms.EDProducer("PFBlockProducer",
    debug = cms.untracked.bool(False),
    elementImporters = cms.VPSet(
        cms.PSet(
            DPtOverPtCuts_byTrackAlgo = cms.vdouble(
                0.5, 0.5, 0.5, 0.5, 0.5,
                0.5
            ),
            NHitCuts_byTrackAlgo = cms.vuint32(
                3, 3, 3, 3, 3,
                3
            ),
            cleanBadConvertedBrems = cms.bool(False),
            importerName = cms.string('GeneralTracksImporter'),
            muonMaxDPtOPt = cms.double(1.0),
            muonSrc = cms.InputTag("hltMuons"),
            source = cms.InputTag("hltLightPFTracks"),
            trackQuality = cms.string('highPurity'),
            useIterativeTracking = cms.bool(False),
            vetoEndcap = cms.bool(False)
        ),
        cms.PSet(
            BCtoPFCMap = cms.InputTag(""),
            importerName = cms.string('ECALClusterImporter'),
            source = cms.InputTag("hltParticleFlowClusterECALUnseeded")
        ),
        cms.PSet(
            importerName = cms.string('GenericClusterImporter'),
            source = cms.InputTag("hltParticleFlowClusterHCAL")
        ),
        cms.PSet(
            importerName = cms.string('GenericClusterImporter'),
            source = cms.InputTag("hltParticleFlowClusterHF")
        )
    ),
    linkDefinitions = cms.VPSet(
        cms.PSet(
            linkType = cms.string('TRACK:ECAL'),
            linkerName = cms.string('TrackAndECALLinker'),
            useKDTree = cms.bool(True)
        ),
        cms.PSet(
            linkType = cms.string('TRACK:HCAL'),
            linkerName = cms.string('TrackAndHCALLinker'),
            nMaxHcalLinksPerTrack = cms.int32(1),
            trajectoryLayerEntrance = cms.string('HCALEntrance'),
            trajectoryLayerExit = cms.string('HCALExit'),
            useKDTree = cms.bool(True)
        ),
        cms.PSet(
            linkType = cms.string('ECAL:HCAL'),
            linkerName = cms.string('ECALAndHCALLinker'),
            minAbsEtaEcal = cms.double(2.5),
            useKDTree = cms.bool(False)
        ),
        cms.PSet(
            linkType = cms.string('HFEM:HFHAD'),
            linkerName = cms.string('HFEMAndHFHADLinker'),
            useKDTree = cms.bool(False)
        )
    ),
    verbose = cms.untracked.bool(False)
)


process.hltParticleFlowClusterECALForMuonsMF = cms.EDProducer("CorrectedECALPFClusterProducer",
    energyCorrector = cms.PSet(
        applyCrackCorrections = cms.bool(False),
        applyMVACorrections = cms.bool(True),
        ebSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        eeSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        maxPtForMVAEvaluation = cms.double(300.0),
        recHitsEBLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        recHitsEELabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        srfAwareCorrection = cms.bool(True)
    ),
    inputECAL = cms.InputTag("hltParticleFlowClusterECALUncorrectedForMuonsMF"),
    inputPS = cms.InputTag("hltParticleFlowClusterPSForMuons"),
    minimumPSEnergy = cms.double(0.0),
    skipPS = cms.bool(False)
)


process.hltParticleFlowClusterECALForMuonsMFNoVtx = cms.EDProducer("CorrectedECALPFClusterProducer",
    energyCorrector = cms.PSet(
        applyCrackCorrections = cms.bool(False),
        applyMVACorrections = cms.bool(True),
        ebSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        eeSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        maxPtForMVAEvaluation = cms.double(300.0),
        recHitsEBLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        recHitsEELabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        srfAwareCorrection = cms.bool(True)
    ),
    inputECAL = cms.InputTag("hltParticleFlowClusterECALUncorrectedForMuonsMFNoVtx"),
    inputPS = cms.InputTag("hltParticleFlowClusterPSForMuonsNoVtx"),
    minimumPSEnergy = cms.double(0.0),
    skipPS = cms.bool(False)
)


process.hltParticleFlowClusterECALL1Seeded = cms.EDProducer("CorrectedECALPFClusterProducer",
    energyCorrector = cms.PSet(
        applyCrackCorrections = cms.bool(False),
        applyMVACorrections = cms.bool(True),
        ebSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        eeSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        maxPtForMVAEvaluation = cms.double(300.0),
        recHitsEBLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        recHitsEELabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        srfAwareCorrection = cms.bool(True)
    ),
    inputECAL = cms.InputTag("hltParticleFlowClusterECALUncorrectedL1Seeded"),
    inputPS = cms.InputTag("hltParticleFlowClusterPSL1Seeded"),
    minimumPSEnergy = cms.double(0.0),
    skipPS = cms.bool(False)
)


process.hltParticleFlowClusterECALUncorrectedForMuonsMF = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                gatheringThreshold = cms.double(0.08),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                gatheringThreshold = cms.double(0.3),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(True)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        allCellsPositionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(9),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        positionCalcForConvergence = cms.PSet(
            T0_EB = cms.double(7.4),
            T0_EE = cms.double(3.1),
            T0_ES = cms.double(1.2),
            W0 = cms.double(4.2),
            X0 = cms.double(0.89),
            algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
            minAllowedNormalization = cms.double(0.0),
            minFractionInCalc = cms.double(0.0)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                recHitEnergyNorm = cms.double(0.08)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                recHitEnergyNorm = cms.double(0.3)
            )
        ),
        showerSigma = cms.double(1.5),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(
        T0_EB = cms.double(7.4),
        T0_EE = cms.double(3.1),
        T0_ES = cms.double(1.2),
        W0 = cms.double(4.2),
        X0 = cms.double(0.89),
        algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
        minAllowedNormalization = cms.double(0.0),
        minFractionInCalc = cms.double(0.0)
    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitECALForMuonsMF"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(8),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                seedingThreshold = cms.double(0.6),
                seedingThresholdPt = cms.double(0.15)
            ),
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                seedingThreshold = cms.double(0.23),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterECALUncorrectedForMuonsMFNoVtx = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                gatheringThreshold = cms.double(0.08),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                gatheringThreshold = cms.double(0.3),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(True)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        allCellsPositionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(9),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        positionCalcForConvergence = cms.PSet(
            T0_EB = cms.double(7.4),
            T0_EE = cms.double(3.1),
            T0_ES = cms.double(1.2),
            W0 = cms.double(4.2),
            X0 = cms.double(0.89),
            algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
            minAllowedNormalization = cms.double(0.0),
            minFractionInCalc = cms.double(0.0)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                recHitEnergyNorm = cms.double(0.08)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                recHitEnergyNorm = cms.double(0.3)
            )
        ),
        showerSigma = cms.double(1.5),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(
        T0_EB = cms.double(7.4),
        T0_EE = cms.double(3.1),
        T0_ES = cms.double(1.2),
        W0 = cms.double(4.2),
        X0 = cms.double(0.89),
        algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
        minAllowedNormalization = cms.double(0.0),
        minFractionInCalc = cms.double(0.0)
    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitECALForMuonsMFNoVtx"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(8),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                seedingThreshold = cms.double(0.6),
                seedingThresholdPt = cms.double(0.15)
            ),
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                seedingThreshold = cms.double(0.23),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterECALUncorrectedL1Seeded = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                gatheringThreshold = cms.double(0.08),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                gatheringThreshold = cms.double(0.3),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(True)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        allCellsPositionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(9),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        positionCalcForConvergence = cms.PSet(
            T0_EB = cms.double(7.4),
            T0_EE = cms.double(3.1),
            T0_ES = cms.double(1.2),
            W0 = cms.double(4.2),
            X0 = cms.double(0.89),
            algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
            minAllowedNormalization = cms.double(0.0),
            minFractionInCalc = cms.double(0.0)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                recHitEnergyNorm = cms.double(0.08)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                recHitEnergyNorm = cms.double(0.3)
            )
        ),
        showerSigma = cms.double(1.5),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(
        T0_EB = cms.double(7.4),
        T0_EE = cms.double(3.1),
        T0_ES = cms.double(1.2),
        W0 = cms.double(4.2),
        X0 = cms.double(0.89),
        algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
        minAllowedNormalization = cms.double(0.0),
        minFractionInCalc = cms.double(0.0)
    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitECALL1Seeded"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(8),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                seedingThreshold = cms.double(0.6),
                seedingThresholdPt = cms.double(0.15)
            ),
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                seedingThreshold = cms.double(0.23),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterECALUncorrectedUnseeded = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                gatheringThreshold = cms.double(0.08),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                gatheringThreshold = cms.double(0.3),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(True)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        allCellsPositionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(0.08),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(9),
            timeResolutionCalcBarrel = cms.PSet(
                constantTerm = cms.double(0.428192),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0510871),
                noiseTerm = cms.double(1.10889),
                noiseTermLowE = cms.double(1.31883),
                threshHighE = cms.double(5.0),
                threshLowE = cms.double(0.5)
            ),
            timeResolutionCalcEndcap = cms.PSet(
                constantTerm = cms.double(0.0),
                constantTermLowE = cms.double(0.0),
                corrTermLowE = cms.double(0.0),
                noiseTerm = cms.double(5.72489999999),
                noiseTermLowE = cms.double(6.92683000001),
                threshHighE = cms.double(10.0),
                threshLowE = cms.double(1.0)
            )
        ),
        positionCalcForConvergence = cms.PSet(
            T0_EB = cms.double(7.4),
            T0_EE = cms.double(3.1),
            T0_ES = cms.double(1.2),
            W0 = cms.double(4.2),
            X0 = cms.double(0.89),
            algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
            minAllowedNormalization = cms.double(0.0),
            minFractionInCalc = cms.double(0.0)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                recHitEnergyNorm = cms.double(0.08)
            ),
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                recHitEnergyNorm = cms.double(0.3)
            )
        ),
        showerSigma = cms.double(1.5),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(
        T0_EB = cms.double(7.4),
        T0_EE = cms.double(3.1),
        T0_ES = cms.double(1.2),
        W0 = cms.double(4.2),
        X0 = cms.double(0.89),
        algoName = cms.string('ECAL2DPositionCalcWithDepthCorr'),
        minAllowedNormalization = cms.double(0.0),
        minFractionInCalc = cms.double(0.0)
    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitECALUnseeded"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(8),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('ECAL_ENDCAP'),
                seedingThreshold = cms.double(0.6),
                seedingThresholdPt = cms.double(0.15)
            ),
            cms.PSet(
                detector = cms.string('ECAL_BARREL'),
                seedingThreshold = cms.double(0.23),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterECALUnseeded = cms.EDProducer("CorrectedECALPFClusterProducer",
    energyCorrector = cms.PSet(
        applyCrackCorrections = cms.bool(False),
        applyMVACorrections = cms.bool(True),
        ebSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        eeSrFlagLabel = cms.InputTag("hltEcalDigisLegacy"),
        maxPtForMVAEvaluation = cms.double(300.0),
        recHitsEBLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        recHitsEELabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        srfAwareCorrection = cms.bool(True)
    ),
    inputECAL = cms.InputTag("hltParticleFlowClusterECALUncorrectedUnseeded"),
    inputPS = cms.InputTag("hltParticleFlowClusterPSUnseeded"),
    minimumPSEnergy = cms.double(0.0),
    skipPS = cms.bool(False)
)


process.hltParticleFlowClusterHBHE = cms.EDProducer("LegacyPFClusterProducer",
    PFRecHitsLabelIn = cms.InputTag("hltParticleFlowRecHitHBHESoA"),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        allCellsPositionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominatorByDetector = cms.VPSet(
                cms.PSet(
                    depths = cms.vint32(1, 2, 3, 4),
                    detector = cms.string('HCAL_BARREL1'),
                    logWeightDenominator = cms.vdouble(0.4, 0.3, 0.3, 0.3)
                ),
                cms.PSet(
                    depths = cms.vint32(
                        1, 2, 3, 4, 5,
                        6, 7
                    ),
                    detector = cms.string('HCAL_ENDCAP'),
                    logWeightDenominator = cms.vdouble(
                        0.1, 0.2, 0.2, 0.2, 0.2,
                        0.2, 0.2
                    )
                )
            ),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1)
        ),
        clusterTimeResFromSeed = cms.bool(False),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(5),
        maxNSigmaTime = cms.double(10.0),
        minChi2Prob = cms.double(0.0),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominatorByDetector = cms.VPSet(
                cms.PSet(
                    depths = cms.vint32(1, 2, 3, 4),
                    detector = cms.string('HCAL_BARREL1'),
                    logWeightDenominator = cms.vdouble(0.4, 0.3, 0.3, 0.3)
                ),
                cms.PSet(
                    depths = cms.vint32(
                        1, 2, 3, 4, 5,
                        6, 7
                    ),
                    detector = cms.string('HCAL_ENDCAP'),
                    logWeightDenominator = cms.vdouble(
                        0.1, 0.2, 0.2, 0.2, 0.2,
                        0.2, 0.2
                    )
                )
            ),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(5)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                depths = cms.vint32(1, 2, 3, 4),
                detector = cms.string('HCAL_BARREL1'),
                recHitEnergyNorm = cms.vdouble(0.4, 0.3, 0.3, 0.3)
            ),
            cms.PSet(
                depths = cms.vint32(
                    1, 2, 3, 4, 5,
                    6, 7
                ),
                detector = cms.string('HCAL_ENDCAP'),
                recHitEnergyNorm = cms.vdouble(
                    0.1, 0.2, 0.2, 0.2, 0.2,
                    0.2, 0.2
                )
            )
        ),
        showerSigma = cms.double(10.0),
        stoppingTolerance = cms.double(1e-08),
        timeResolutionCalcBarrel = cms.PSet(
            constantTerm = cms.double(2.82),
            constantTermLowE = cms.double(4.24),
            corrTermLowE = cms.double(0.0),
            noiseTerm = cms.double(21.86),
            noiseTermLowE = cms.double(8.0),
            threshHighE = cms.double(15.0),
            threshLowE = cms.double(6.0)
        ),
        timeResolutionCalcEndcap = cms.PSet(
            constantTerm = cms.double(2.82),
            constantTermLowE = cms.double(4.24),
            corrTermLowE = cms.double(0.0),
            noiseTerm = cms.double(21.86),
            noiseTermLowE = cms.double(8.0),
            threshHighE = cms.double(15.0),
            threshLowE = cms.double(6.0)
        ),
        timeSigmaEB = cms.double(10.0),
        timeSigmaEE = cms.double(10.0)
    ),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitHBHE"),
    src = cms.InputTag("hltParticleFlowClusterHBHESoA"),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterHBHESoA = cms.EDProducer("PFClusterSoAProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    initialClusteringStep = cms.PSet(
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('HCAL_BARREL1'),
                gatheringThreshold = cms.vdouble(0.1, 0.2, 0.3, 0.3)
            ),
            cms.PSet(
                detector = cms.string('HCAL_ENDCAP'),
                gatheringThreshold = cms.vdouble(
                    0.1, 0.2, 0.2, 0.2, 0.2,
                    0.2, 0.2
                )
            )
        )
    ),
    pfClusterBuilder = cms.PSet(
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(5),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('HCAL_BARREL1'),
                recHitEnergyNorm = cms.vdouble(0.1, 0.2, 0.3, 0.3)
            ),
            cms.PSet(
                detector = cms.string('HCAL_ENDCAP'),
                recHitEnergyNorm = cms.vdouble(
                    0.1, 0.2, 0.2, 0.2, 0.2,
                    0.2, 0.2
                )
            )
        ),
        showerSigma = cms.double(10.0),
        stoppingTolerance = cms.double(1e-08),
        timeResolutionCalcBarrel = cms.PSet(
            constantTerm = cms.double(2.82),
            constantTermLowE = cms.double(4.24),
            corrTermLowE = cms.double(0.0),
            noiseTerm = cms.double(21.86),
            noiseTermLowE = cms.double(8.0),
            threshHighE = cms.double(15.0),
            threshLowE = cms.double(6.0)
        ),
        timeResolutionCalcEndcap = cms.PSet(
            constantTerm = cms.double(2.82),
            constantTermLowE = cms.double(4.24),
            corrTermLowE = cms.double(0.0),
            noiseTerm = cms.double(21.86),
            noiseTermLowE = cms.double(8.0),
            threshHighE = cms.double(15.0),
            threshLowE = cms.double(6.0)
        )
    ),
    pfRecHits = cms.InputTag("hltParticleFlowRecHitHBHESoA"),
    seedFinder = cms.PSet(
        nNeighbours = cms.int32(4),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('HCAL_BARREL1'),
                seedingThreshold = cms.vdouble(0.125, 0.25, 0.35, 0.35),
                seedingThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('HCAL_ENDCAP'),
                seedingThreshold = cms.vdouble(
                    0.1375, 0.275, 0.275, 0.275, 0.275,
                    0.275, 0.275
                ),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    synchronise = cms.bool(False),
    topology = cms.ESInputTag("hltESPPFRecHitHCALTopology","")
)


process.hltParticleFlowClusterHCAL = cms.EDProducer("PFMultiDepthClusterProducer",
    clustersSource = cms.InputTag("hltParticleFlowClusterHBHE"),
    energyCorrector = cms.PSet(

    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('PFMultiDepthClusterizer'),
        allCellsPositionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominatorByDetector = cms.VPSet(
                cms.PSet(
                    depths = cms.vint32(1, 2, 3, 4),
                    detector = cms.string('HCAL_BARREL1'),
                    logWeightDenominator = cms.vdouble(0.4, 0.3, 0.3, 0.3)
                ),
                cms.PSet(
                    depths = cms.vint32(
                        1, 2, 3, 4, 5,
                        6, 7
                    ),
                    detector = cms.string('HCAL_ENDCAP'),
                    logWeightDenominator = cms.vdouble(
                        0.1, 0.2, 0.2, 0.2, 0.2,
                        0.2, 0.2
                    )
                )
            ),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1)
        ),
        minFractionToKeep = cms.double(1e-07),
        nSigmaEta = cms.double(2.0),
        nSigmaPhi = cms.double(2.0)
    ),
    positionReCalc = cms.PSet(

    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterHF = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DClusterForEachSeed'),
        thresholdsByDetector = cms.VPSet()
    ),
    pfClusterBuilder = cms.PSet(

    ),
    positionReCalc = cms.PSet(

    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitHF"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(0),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('HF_EM'),
                seedingThreshold = cms.double(1.4),
                seedingThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('HF_HAD'),
                seedingThreshold = cms.double(1.4),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterPSForMuons = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(False)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(6e-05),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                recHitEnergyNorm = cms.double(6e-05)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                recHitEnergyNorm = cms.double(6e-05)
            )
        ),
        showerSigma = cms.double(0.3),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(

    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitPSForMuons"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(4),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterPSForMuonsNoVtx = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(False)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(6e-05),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                recHitEnergyNorm = cms.double(6e-05)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                recHitEnergyNorm = cms.double(6e-05)
            )
        ),
        showerSigma = cms.double(0.3),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(

    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitPSForMuonsNoVtx"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(4),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterPSL1Seeded = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(False)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(6e-05),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                recHitEnergyNorm = cms.double(6e-05)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                recHitEnergyNorm = cms.double(6e-05)
            )
        ),
        showerSigma = cms.double(0.3),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(

    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitPSL1Seeded"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(4),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowClusterPSUnseeded = cms.EDProducer("PFClusterProducer",
    energyCorrector = cms.PSet(

    ),
    initialClusteringStep = cms.PSet(
        algoName = cms.string('Basic2DGenericTopoClusterizer'),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                gatheringThreshold = cms.double(6e-05),
                gatheringThresholdPt = cms.double(0.0)
            )
        ),
        useCornerCells = cms.bool(False)
    ),
    pfClusterBuilder = cms.PSet(
        algoName = cms.string('Basic2DGenericPFlowClusterizer'),
        excludeOtherSeeds = cms.bool(True),
        maxIterations = cms.uint32(50),
        minFracTot = cms.double(1e-20),
        minFractionToKeep = cms.double(1e-07),
        positionCalc = cms.PSet(
            algoName = cms.string('Basic2DGenericPFlowPositionCalc'),
            logWeightDenominator = cms.double(6e-05),
            minAllowedNormalization = cms.double(1e-09),
            minFractionInCalc = cms.double(1e-09),
            posCalcNCrystals = cms.int32(-1)
        ),
        recHitEnergyNorms = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                recHitEnergyNorm = cms.double(6e-05)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                recHitEnergyNorm = cms.double(6e-05)
            )
        ),
        showerSigma = cms.double(0.3),
        stoppingTolerance = cms.double(1e-08)
    ),
    positionReCalc = cms.PSet(

    ),
    recHitCleaners = cms.VPSet(),
    recHitsSource = cms.InputTag("hltParticleFlowRecHitPSUnseeded"),
    seedCleaners = cms.VPSet(),
    seedFinder = cms.PSet(
        algoName = cms.string('LocalMaximumSeedFinder'),
        nNeighbours = cms.int32(4),
        thresholdsByDetector = cms.VPSet(
            cms.PSet(
                detector = cms.string('PS1'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            ),
            cms.PSet(
                detector = cms.string('PS2'),
                seedingThreshold = cms.double(0.00012),
                seedingThresholdPt = cms.double(0.0)
            )
        )
    ),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltParticleFlowRecHitECALForMuonsMF = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        barrel = cms.PSet(

        ),
        endcap = cms.PSet(

        ),
        name = cms.string('PFRecHitECALNavigator')
    ),
    producers = cms.VPSet(
        cms.PSet(
            name = cms.string('PFEBRecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltRecHitInRegionForMuonsMF","EcalRegionalRecHitsEB")
        ),
        cms.PSet(
            name = cms.string('PFEERecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltRecHitInRegionForMuonsMF","EcalRegionalRecHitsEE")
        )
    )
)


process.hltParticleFlowRecHitECALForMuonsMFNoVtx = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        barrel = cms.PSet(

        ),
        endcap = cms.PSet(

        ),
        name = cms.string('PFRecHitECALNavigator')
    ),
    producers = cms.VPSet(
        cms.PSet(
            name = cms.string('PFEBRecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltRecHitInRegionForMuonsMFnoVtx","EcalRegionalRecHitsEB")
        ),
        cms.PSet(
            name = cms.string('PFEERecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltRecHitInRegionForMuonsMFnoVtx","EcalRegionalRecHitsEE")
        )
    )
)


process.hltParticleFlowRecHitECALL1Seeded = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        barrel = cms.PSet(

        ),
        endcap = cms.PSet(

        ),
        name = cms.string('PFRecHitECALNavigator')
    ),
    producers = cms.VPSet(
        cms.PSet(
            name = cms.string('PFEBRecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltRechitInRegionsECAL","EcalRecHitsEB")
        ),
        cms.PSet(
            name = cms.string('PFEERecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltRechitInRegionsECAL","EcalRecHitsEE")
        )
    )
)


process.hltParticleFlowRecHitECALUnseeded = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        barrel = cms.PSet(

        ),
        endcap = cms.PSet(

        ),
        name = cms.string('PFRecHitECALNavigator')
    ),
    producers = cms.VPSet(
        cms.PSet(
            name = cms.string('PFEBRecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltEcalRecHit","EcalRecHitsEB")
        ),
        cms.PSet(
            name = cms.string('PFEERecHitCreator'),
            qualityTests = cms.VPSet(
                cms.PSet(
                    applySelectionsToAllCrystals = cms.bool(True),
                    name = cms.string('PFRecHitQTestDBThreshold')
                ),
                cms.PSet(
                    cleaningThreshold = cms.double(2.0),
                    name = cms.string('PFRecHitQTestECAL'),
                    skipTTRecoveredHits = cms.bool(True),
                    timingCleaning = cms.bool(True),
                    topologicalCleaning = cms.bool(True)
                )
            ),
            srFlags = cms.InputTag(""),
            src = cms.InputTag("hltEcalRecHit","EcalRecHitsEE")
        )
    )
)


process.hltParticleFlowRecHitHBHE = cms.EDProducer("LegacyPFRecHitProducer",
    src = cms.InputTag("hltParticleFlowRecHitHBHESoA")
)


process.hltParticleFlowRecHitHBHESoA = cms.EDProducer("PFRecHitSoAProducerHCAL@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    producers = cms.VPSet(cms.PSet(
        params = cms.ESInputTag("hltESPPFRecHitHCALParams",""),
        src = cms.InputTag("hltHbheRecoSoA")
    )),
    synchronise = cms.untracked.bool(False),
    topology = cms.ESInputTag("hltESPPFRecHitHCALTopology","")
)


process.hltParticleFlowRecHitHF = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        hcalEnums = cms.vint32(4),
        name = cms.string('PFRecHitHCALDenseIdNavigator')
    ),
    producers = cms.VPSet(cms.PSet(
        EMDepthCorrection = cms.double(22.0),
        HADDepthCorrection = cms.double(25.0),
        HFCalib29 = cms.double(1.07),
        LongFibre_Cut = cms.double(120.0),
        LongFibre_Fraction = cms.double(0.1),
        ShortFibre_Cut = cms.double(60.0),
        ShortFibre_Fraction = cms.double(0.01),
        name = cms.string('PFHFRecHitCreator'),
        qualityTests = cms.VPSet(
            cms.PSet(
                cleaningThresholds = cms.vdouble(0.0, 120.0, 60.0),
                flags = cms.vstring(
                    'Standard',
                    'HFLong',
                    'HFShort'
                ),
                maxSeverities = cms.vint32(11, 9, 9),
                name = cms.string('PFRecHitQTestHCALChannel')
            ),
            cms.PSet(
                cuts = cms.VPSet(cms.PSet(
                    depth = cms.vint32(1, 2),
                    detectorEnum = cms.int32(4),
                    threshold = cms.vdouble(1.2, 1.8)
                )),
                name = cms.string('PFRecHitQTestHCALThresholdVsDepth'),
                usePFThresholdsFromDB = cms.bool(False)
            )
        ),
        src = cms.InputTag("hltHfreco"),
        thresh_HF = cms.double(0.4)
    ))
)


process.hltParticleFlowRecHitPSForMuons = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        name = cms.string('PFRecHitPreshowerNavigator')
    ),
    producers = cms.VPSet(cms.PSet(
        name = cms.string('PFPSRecHitCreator'),
        qualityTests = cms.VPSet(cms.PSet(
            name = cms.string('PFRecHitQTestThreshold'),
            threshold = cms.double(7e-06)
        )),
        src = cms.InputTag("hltRecHitInRegionForMuonsES","EcalRegionalRecHitsES")
    ))
)


process.hltParticleFlowRecHitPSForMuonsNoVtx = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        name = cms.string('PFRecHitPreshowerNavigator')
    ),
    producers = cms.VPSet(cms.PSet(
        name = cms.string('PFPSRecHitCreator'),
        qualityTests = cms.VPSet(cms.PSet(
            name = cms.string('PFRecHitQTestThreshold'),
            threshold = cms.double(7e-06)
        )),
        src = cms.InputTag("hltRecHitInRegionForMuonsESNoVtx","EcalRegionalRecHitsES")
    ))
)


process.hltParticleFlowRecHitPSL1Seeded = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        name = cms.string('PFRecHitPreshowerNavigator')
    ),
    producers = cms.VPSet(cms.PSet(
        name = cms.string('PFPSRecHitCreator'),
        qualityTests = cms.VPSet(cms.PSet(
            name = cms.string('PFRecHitQTestThreshold'),
            threshold = cms.double(7e-06)
        )),
        src = cms.InputTag("hltRechitInRegionsES","EcalRecHitsES")
    ))
)


process.hltParticleFlowRecHitPSUnseeded = cms.EDProducer("PFRecHitProducer",
    navigator = cms.PSet(
        name = cms.string('PFRecHitPreshowerNavigator')
    ),
    producers = cms.VPSet(cms.PSet(
        name = cms.string('PFPSRecHitCreator'),
        qualityTests = cms.VPSet(cms.PSet(
            name = cms.string('PFRecHitQTestThreshold'),
            threshold = cms.double(7e-06)
        )),
        src = cms.InputTag("hltEcalPreshowerRecHit","EcalRecHitsES")
    ))
)


process.hltParticleFlowSuperClusterECALL1Seeded = cms.EDProducer("PFECALSuperClusterProducer",
    BeamSpot = cms.InputTag("hltOnlineBeamSpot"),
    ClusteringType = cms.string('Mustache'),
    ESAssociation = cms.InputTag("hltParticleFlowClusterECALL1Seeded"),
    EnergyWeight = cms.string('Raw'),
    PFBasicClusterCollectionBarrel = cms.string('hltParticleFlowBasicClusterECALBarrel'),
    PFBasicClusterCollectionEndcap = cms.string('hltParticleFlowBasicClusterECALEndcap'),
    PFBasicClusterCollectionPreshower = cms.string('hltParticleFlowBasicClusterECALPreshower'),
    PFClusters = cms.InputTag("hltParticleFlowClusterECALL1Seeded"),
    PFSuperClusterCollectionBarrel = cms.string('hltParticleFlowSuperClusterECALBarrel'),
    PFSuperClusterCollectionEndcap = cms.string('hltParticleFlowSuperClusterECALEndcap'),
    PFSuperClusterCollectionEndcapWithPreshower = cms.string('hltParticleFlowSuperClusterECALEndcapWithPreshower'),
    applyCrackCorrections = cms.bool(False),
    barrelRecHits = cms.InputTag(""),
    doSatelliteClusterMerge = cms.bool(False),
    dropUnseedable = cms.bool(False),
    endcapRecHits = cms.InputTag(""),
    etawidth_SuperClusterBarrel = cms.double(0.04),
    etawidth_SuperClusterEndcap = cms.double(0.04),
    isOOTCollection = cms.bool(False),
    phiwidth_SuperClusterBarrel = cms.double(0.6),
    phiwidth_SuperClusterEndcap = cms.double(0.6),
    regressionConfig = cms.PSet(
        ecalRecHitsEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        ecalRecHitsEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        isHLT = cms.bool(True),
        regTrainedWithPS = cms.bool(True),
        regressionKeyEB = cms.string('pfscecal_EBCorrection_online'),
        regressionKeyEE = cms.string('pfscecal_EECorrection_online'),
        uncertaintyKeyEB = cms.string('pfscecal_EBUncertainty_online'),
        uncertaintyKeyEE = cms.string('pfscecal_EEUncertainty_online')
    ),
    satelliteClusterSeedThreshold = cms.double(50.0),
    satelliteMajorityFraction = cms.double(0.5),
    seedThresholdIsET = cms.bool(True),
    thresh_PFClusterBarrel = cms.double(0.5),
    thresh_PFClusterES = cms.double(0.5),
    thresh_PFClusterEndcap = cms.double(0.5),
    thresh_PFClusterSeedBarrel = cms.double(1.0),
    thresh_PFClusterSeedEndcap = cms.double(1.0),
    thresh_SCEt = cms.double(4.0),
    useDynamicDPhiWindow = cms.bool(True),
    useRegression = cms.bool(True),
    verbose = cms.untracked.bool(False)
)


process.hltParticleFlowSuperClusterECALUnseeded = cms.EDProducer("PFECALSuperClusterProducer",
    BeamSpot = cms.InputTag("hltOnlineBeamSpot"),
    ClusteringType = cms.string('Mustache'),
    ESAssociation = cms.InputTag("hltParticleFlowClusterECALUnseeded"),
    EnergyWeight = cms.string('Raw'),
    PFBasicClusterCollectionBarrel = cms.string('hltParticleFlowBasicClusterECALBarrel'),
    PFBasicClusterCollectionEndcap = cms.string('hltParticleFlowBasicClusterECALEndcap'),
    PFBasicClusterCollectionPreshower = cms.string('hltParticleFlowBasicClusterECALPreshower'),
    PFClusters = cms.InputTag("hltParticleFlowClusterECALUnseeded"),
    PFSuperClusterCollectionBarrel = cms.string('hltParticleFlowSuperClusterECALBarrel'),
    PFSuperClusterCollectionEndcap = cms.string('hltParticleFlowSuperClusterECALEndcap'),
    PFSuperClusterCollectionEndcapWithPreshower = cms.string('hltParticleFlowSuperClusterECALEndcapWithPreshower'),
    applyCrackCorrections = cms.bool(False),
    barrelRecHits = cms.InputTag(""),
    doSatelliteClusterMerge = cms.bool(False),
    dropUnseedable = cms.bool(False),
    endcapRecHits = cms.InputTag(""),
    etawidth_SuperClusterBarrel = cms.double(0.04),
    etawidth_SuperClusterEndcap = cms.double(0.04),
    isOOTCollection = cms.bool(False),
    phiwidth_SuperClusterBarrel = cms.double(0.6),
    phiwidth_SuperClusterEndcap = cms.double(0.6),
    regressionConfig = cms.PSet(
        ecalRecHitsEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
        ecalRecHitsEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
        isHLT = cms.bool(True),
        regTrainedWithPS = cms.bool(True),
        regressionKeyEB = cms.string('pfscecal_EBCorrection_online'),
        regressionKeyEE = cms.string('pfscecal_EECorrection_online'),
        uncertaintyKeyEB = cms.string('pfscecal_EBUncertainty_online'),
        uncertaintyKeyEE = cms.string('pfscecal_EEUncertainty_online')
    ),
    satelliteClusterSeedThreshold = cms.double(50.0),
    satelliteMajorityFraction = cms.double(0.5),
    seedThresholdIsET = cms.bool(True),
    thresh_PFClusterBarrel = cms.double(0.5),
    thresh_PFClusterES = cms.double(0.5),
    thresh_PFClusterEndcap = cms.double(0.5),
    thresh_PFClusterSeedBarrel = cms.double(1.0),
    thresh_PFClusterSeedEndcap = cms.double(1.0),
    thresh_SCEt = cms.double(4.0),
    useDynamicDPhiWindow = cms.bool(True),
    useRegression = cms.bool(True),
    verbose = cms.untracked.bool(False)
)


process.hltPixelLayerPairs = cms.EDProducer("SeedingLayersEDProducer",
    BPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0027),
        hitErrorRZ = cms.double(0.006),
        useErrorsFromParam = cms.bool(True)
    ),
    FPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0051),
        hitErrorRZ = cms.double(0.0036),
        useErrorsFromParam = cms.bool(True)
    ),
    MTEC = cms.PSet(

    ),
    MTIB = cms.PSet(

    ),
    MTID = cms.PSet(

    ),
    MTOB = cms.PSet(

    ),
    TEC = cms.PSet(

    ),
    TIB = cms.PSet(

    ),
    TID = cms.PSet(

    ),
    TOB = cms.PSet(

    ),
    layerList = cms.vstring(
        'BPix1+BPix2',
        'BPix1+BPix3',
        'BPix1+BPix4',
        'BPix2+BPix3',
        'BPix2+BPix4',
        'BPix3+BPix4',
        'FPix1_pos+FPix2_pos',
        'FPix1_pos+FPix3_pos',
        'FPix2_pos+FPix3_pos',
        'BPix1+FPix1_pos',
        'BPix1+FPix2_pos',
        'BPix1+FPix3_pos',
        'BPix2+FPix1_pos',
        'BPix2+FPix2_pos',
        'BPix2+FPix3_pos',
        'BPix3+FPix1_pos',
        'BPix3+FPix2_pos',
        'BPix3+FPix3_pos',
        'BPix4+FPix1_pos',
        'BPix4+FPix2_pos',
        'BPix4+FPix3_pos',
        'FPix1_neg+FPix2_neg',
        'FPix1_neg+FPix3_neg',
        'FPix2_neg+FPix3_neg',
        'BPix1+FPix1_neg',
        'BPix1+FPix2_neg',
        'BPix1+FPix3_neg',
        'BPix2+FPix1_neg',
        'BPix2+FPix2_neg',
        'BPix2+FPix3_neg',
        'BPix3+FPix1_neg',
        'BPix3+FPix2_neg',
        'BPix3+FPix3_neg',
        'BPix4+FPix1_neg',
        'BPix4+FPix2_neg',
        'BPix4+FPix3_neg'
    )
)


process.hltPixelLayerTriplets = cms.EDProducer("SeedingLayersEDProducer",
    BPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0027),
        hitErrorRZ = cms.double(0.006),
        useErrorsFromParam = cms.bool(True)
    ),
    FPix = cms.PSet(
        HitProducer = cms.string('hltSiPixelRecHits'),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        hitErrorRPhi = cms.double(0.0051),
        hitErrorRZ = cms.double(0.0036),
        useErrorsFromParam = cms.bool(True)
    ),
    MTEC = cms.PSet(

    ),
    MTIB = cms.PSet(

    ),
    MTID = cms.PSet(

    ),
    MTOB = cms.PSet(

    ),
    TEC = cms.PSet(

    ),
    TIB = cms.PSet(

    ),
    TID = cms.PSet(

    ),
    TOB = cms.PSet(

    ),
    layerList = cms.vstring(
        'BPix1+BPix2+BPix3',
        'BPix2+BPix3+BPix4',
        'BPix1+BPix3+BPix4',
        'BPix1+BPix2+BPix4',
        'BPix2+BPix3+FPix1_pos',
        'BPix2+BPix3+FPix1_neg',
        'BPix1+BPix2+FPix1_pos',
        'BPix1+BPix2+FPix1_neg',
        'BPix2+FPix1_pos+FPix2_pos',
        'BPix2+FPix1_neg+FPix2_neg',
        'BPix1+FPix1_pos+FPix2_pos',
        'BPix1+FPix1_neg+FPix2_neg',
        'FPix1_pos+FPix2_pos+FPix3_pos',
        'FPix1_neg+FPix2_neg+FPix3_neg',
        'BPix1+BPix3+FPix1_pos',
        'BPix1+BPix2+FPix2_pos',
        'BPix1+BPix3+FPix1_neg',
        'BPix1+BPix2+FPix2_neg',
        'BPix1+FPix2_neg+FPix3_neg',
        'BPix1+FPix1_neg+FPix3_neg',
        'BPix1+FPix2_pos+FPix3_pos',
        'BPix1+FPix1_pos+FPix3_pos'
    )
)


process.hltPixelTracks = cms.EDProducer("PixelTrackProducerFromSoAAlpakaPhase1",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    minNumberOfHits = cms.int32(0),
    minQuality = cms.string('loose'),
    pixelRecHitLegacySrc = cms.InputTag("hltSiPixelRecHits"),
    trackSrc = cms.InputTag("hltPixelTracksSoA")
)


process.hltPixelTracksInRegionIter0L3Muon = cms.EDProducer("TrackSelectorByRegion",
    produceMask = cms.bool(False),
    produceTrackCollection = cms.bool(True),
    regions = cms.InputTag("hltPixelTracksTrackingRegionsForSeedsL3Muon"),
    tracks = cms.InputTag("hltPixelTracks")
)


process.hltPixelTracksInRegionIter0L3MuonNoVtx = cms.EDProducer("TrackSelectorByRegion",
    produceMask = cms.bool(False),
    produceTrackCollection = cms.bool(True),
    regions = cms.InputTag("hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx"),
    tracks = cms.InputTag("hltPixelTracks")
)


process.hltPixelTracksInRegionL1 = cms.EDProducer("TrackSelectorByRegion",
    produceMask = cms.bool(False),
    produceTrackCollection = cms.bool(True),
    regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegions"),
    tracks = cms.InputTag("hltPixelTracks")
)


process.hltPixelTracksInRegionL1NoVtx = cms.EDProducer("TrackSelectorByRegion",
    produceMask = cms.bool(False),
    produceTrackCollection = cms.bool(True),
    regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx"),
    tracks = cms.InputTag("hltPixelTracks")
)


process.hltPixelTracksInRegionL2 = cms.EDProducer("TrackSelectorByRegion",
    produceMask = cms.bool(False),
    produceTrackCollection = cms.bool(True),
    regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegions"),
    tracks = cms.InputTag("hltPixelTracks")
)


process.hltPixelTracksInRegionL2NoVtx = cms.EDProducer("TrackSelectorByRegion",
    produceMask = cms.bool(False),
    produceTrackCollection = cms.bool(True),
    regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegionsNoVtx"),
    tracks = cms.InputTag("hltPixelTracks")
)


process.hltPixelTracksSoA = cms.EDProducer("CAHitNtupletAlpakaPhase1@alpaka",
    CAThetaCutBarrel = cms.double(0.00123302705499),
    CAThetaCutForward = cms.double(0.00355691321774),
    CPE = cms.string('PixelCPEFastParams'),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    cellPtCut = cms.double(0.5),
    cellZ0Cut = cms.double(12.0),
    dcaCutInnerTriplet = cms.double(0.0918113099491),
    dcaCutOuterTriplet = cms.double(0.420724617835),
    doClusterCut = cms.bool(True),
    doPtCut = cms.bool(True),
    doSharedHitCut = cms.bool(True),
    doZ0Cut = cms.bool(True),
    dupPassThrough = cms.bool(False),
    earlyFishbone = cms.bool(True),
    fillStatistics = cms.bool(False),
    fitNas4 = cms.bool(False),
    hardCurvCut = cms.double(0.0328407225),
    idealConditions = cms.bool(False),
    includeJumpingForwardDoublets = cms.bool(True),
    lateFishbone = cms.bool(False),
    maxNumberOfDoublets = cms.uint32(524288),
    minHitsForSharingCut = cms.uint32(10),
    minHitsPerNtuplet = cms.uint32(3),
    minYsizeB1 = cms.int32(1),
    minYsizeB2 = cms.int32(1),
    phiCuts = cms.vint32(
        965, 1241, 395, 698, 1058,
        1211, 348, 782, 1016, 810,
        463, 755, 694, 531, 770,
        471, 592, 750, 348
    ),
    pixelRecHitSrc = cms.InputTag("hltSiPixelRecHitsSoA"),
    ptmin = cms.double(0.9),
    trackQualityCuts = cms.PSet(
        chi2Coeff = cms.vdouble(0.9, 1.8),
        chi2MaxPt = cms.double(10.0),
        chi2Scale = cms.double(8.0),
        quadrupletMaxTip = cms.double(0.5),
        quadrupletMaxZip = cms.double(12.0),
        quadrupletMinPt = cms.double(0.3),
        tripletMaxTip = cms.double(0.3),
        tripletMaxZip = cms.double(12.0),
        tripletMinPt = cms.double(0.5)
    ),
    useRiemannFit = cms.bool(False),
    useSimpleTripletCleaner = cms.bool(True)
)


process.hltPixelTracksTrackingRegionsForSeedsL3Muon = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEta = cms.double(0.3),
        deltaPhi = cms.double(0.3),
        input = cms.InputTag("hltIterL3MuonCandidates"),
        maxNRegions = cms.int32(40),
        maxNVertices = cms.int32(4),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('VerticesFixed'),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        originRadius = cms.double(0.1),
        precise = cms.bool(True),
        ptMin = cms.double(0.3),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("hltPixelVertices"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(24.2),
        zErrorVetex = cms.double(0.2)
    )
)


process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEta = cms.double(0.3),
        deltaPhi = cms.double(0.3),
        input = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
        maxNRegions = cms.int32(40),
        maxNVertices = cms.int32(4),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('VerticesFixed'),
        nSigmaZBeamSpot = cms.double(4.0),
        nSigmaZVertex = cms.double(3.0),
        originRadius = cms.double(0.1),
        precise = cms.bool(True),
        ptMin = cms.double(0.3),
        searchOpt = cms.bool(False),
        vertexCollection = cms.InputTag("hltPixelVertices"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(24.2),
        zErrorVetex = cms.double(0.2)
    )
)


process.hltPixelVertices = cms.EDProducer("PixelVertexProducerFromSoAAlpaka",
    TrackCollection = cms.InputTag("hltPixelTracks"),
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    src = cms.InputTag("hltPixelVerticesSoA")
)


process.hltPixelVerticesSoA = cms.EDProducer("PixelVertexProducerAlpakaPhase1@alpaka",
    PtMax = cms.double(75.0),
    PtMin = cms.double(0.5),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    chi2max = cms.double(9.0),
    doSplitting = cms.bool(True),
    eps = cms.double(0.07),
    errmax = cms.double(0.01),
    maxVertices = cms.int32(256),
    minT = cms.int32(2),
    oneKernel = cms.bool(True),
    pixelTrackSrc = cms.InputTag("hltPixelTracksSoA"),
    useDBSCAN = cms.bool(False),
    useDensity = cms.bool(True),
    useIterative = cms.bool(False)
)


process.hltRecHitInRegionForMuonsES = cms.EDProducer("MuonHLTRechitInRegionsProducer",
    doIsolated = cms.bool(True),
    ecalhitLabels = cms.VInputTag("hltEcalPreshowerRecHit:EcalRecHitsES"),
    l1LowerThr = cms.double(0.0),
    l1LowerThrIgnoreIsolation = cms.double(100.0),
    l1TagIsolated = cms.InputTag("hltIterL3MuonCandidates"),
    l1TagNonIsolated = cms.InputTag("NotUsed"),
    l1UpperThr = cms.double(999.0),
    productLabels = cms.vstring('EcalRegionalRecHitsES'),
    regionEtaMargin = cms.double(0.4),
    regionPhiMargin = cms.double(0.4),
    useUncalib = cms.bool(False)
)


process.hltRecHitInRegionForMuonsESNoVtx = cms.EDProducer("MuonHLTRechitInRegionsProducer",
    doIsolated = cms.bool(True),
    ecalhitLabels = cms.VInputTag("hltEcalPreshowerRecHit:EcalRecHitsES"),
    l1LowerThr = cms.double(0.0),
    l1LowerThrIgnoreIsolation = cms.double(100.0),
    l1TagIsolated = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    l1TagNonIsolated = cms.InputTag("NotUsed"),
    l1UpperThr = cms.double(999.0),
    productLabels = cms.vstring('EcalRegionalRecHitsES'),
    regionEtaMargin = cms.double(0.4),
    regionPhiMargin = cms.double(0.4),
    useUncalib = cms.bool(False)
)


process.hltRecHitInRegionForMuonsMF = cms.EDProducer("MuonHLTRechitInRegionsProducer",
    doIsolated = cms.bool(True),
    ecalhitLabels = cms.VInputTag("hltEcalRecHit:EcalRecHitsEB", "hltEcalRecHit:EcalRecHitsEE"),
    l1LowerThr = cms.double(0.0),
    l1LowerThrIgnoreIsolation = cms.double(100.0),
    l1TagIsolated = cms.InputTag("hltIterL3MuonCandidates"),
    l1TagNonIsolated = cms.InputTag("NotUsed"),
    l1UpperThr = cms.double(999.0),
    productLabels = cms.vstring(
        'EcalRegionalRecHitsEB',
        'EcalRegionalRecHitsEE'
    ),
    regionEtaMargin = cms.double(0.4),
    regionPhiMargin = cms.double(0.4),
    useUncalib = cms.bool(False)
)


process.hltRecHitInRegionForMuonsMFnoVtx = cms.EDProducer("MuonHLTRechitInRegionsProducer",
    doIsolated = cms.bool(True),
    ecalhitLabels = cms.VInputTag("hltEcalRecHit:EcalRecHitsEB", "hltEcalRecHit:EcalRecHitsEE"),
    l1LowerThr = cms.double(0.0),
    l1LowerThrIgnoreIsolation = cms.double(100.0),
    l1TagIsolated = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    l1TagNonIsolated = cms.InputTag("NotUsed"),
    l1UpperThr = cms.double(999.0),
    productLabels = cms.vstring(
        'EcalRegionalRecHitsEB',
        'EcalRegionalRecHitsEE'
    ),
    regionEtaMargin = cms.double(0.4),
    regionPhiMargin = cms.double(0.4),
    useUncalib = cms.bool(False)
)


process.hltRechitInRegionsECAL = cms.EDProducer("HLTEcalRecHitInAllL1RegionsProducer",
    l1InputRegions = cms.VPSet(
        cms.PSet(
            inputColl = cms.InputTag("hltGtStage2Digis","EGamma"),
            maxEt = cms.double(999999.0),
            minEt = cms.double(5.0),
            regionEtaMargin = cms.double(0.9),
            regionPhiMargin = cms.double(1.2),
            type = cms.string('EGamma')
        ),
        cms.PSet(
            inputColl = cms.InputTag("hltGtStage2Digis","Jet"),
            maxEt = cms.double(999999.0),
            minEt = cms.double(170.0),
            regionEtaMargin = cms.double(0.9),
            regionPhiMargin = cms.double(1.2),
            type = cms.string('Jet')
        ),
        cms.PSet(
            inputColl = cms.InputTag("hltGtStage2Digis","Tau"),
            maxEt = cms.double(999999.0),
            minEt = cms.double(100.0),
            regionEtaMargin = cms.double(0.9),
            regionPhiMargin = cms.double(1.2),
            type = cms.string('Tau')
        )
    ),
    productLabels = cms.vstring(
        'EcalRecHitsEB',
        'EcalRecHitsEE'
    ),
    recHitLabels = cms.VInputTag("hltEcalRecHit:EcalRecHitsEB", "hltEcalRecHit:EcalRecHitsEE")
)


process.hltRechitInRegionsES = cms.EDProducer("HLTEcalRecHitInAllL1RegionsProducer",
    l1InputRegions = cms.VPSet(
        cms.PSet(
            inputColl = cms.InputTag("hltGtStage2Digis","EGamma"),
            maxEt = cms.double(999999.0),
            minEt = cms.double(5.0),
            regionEtaMargin = cms.double(0.9),
            regionPhiMargin = cms.double(1.2),
            type = cms.string('EGamma')
        ),
        cms.PSet(
            inputColl = cms.InputTag("hltGtStage2Digis","Jet"),
            maxEt = cms.double(999999.0),
            minEt = cms.double(170.0),
            regionEtaMargin = cms.double(0.9),
            regionPhiMargin = cms.double(1.2),
            type = cms.string('Jet')
        ),
        cms.PSet(
            inputColl = cms.InputTag("hltGtStage2Digis","Tau"),
            maxEt = cms.double(999999.0),
            minEt = cms.double(100.0),
            regionEtaMargin = cms.double(0.9),
            regionPhiMargin = cms.double(1.2),
            type = cms.string('Tau')
        )
    ),
    productLabels = cms.vstring('EcalRecHitsES'),
    recHitLabels = cms.VInputTag("hltEcalPreshowerRecHit:EcalRecHitsES")
)


process.hltRpcRecHits = cms.EDProducer("RPCRecHitProducer",
    deadSource = cms.string('File'),
    deadvecfile = cms.FileInPath('RecoLocalMuon/RPCRecHit/data/RPCDeadVec.dat'),
    maskSource = cms.string('File'),
    maskvecfile = cms.FileInPath('RecoLocalMuon/RPCRecHit/data/RPCMaskVec.dat'),
    recAlgo = cms.string('RPCRecHitStandardAlgo'),
    recAlgoConfig = cms.PSet(

    ),
    rpcDigiLabel = cms.InputTag("hltMuonRPCDigis")
)


process.hltScoutingEgammaPacker = cms.EDProducer("HLTScoutingEgammaProducer",
    DetaMap = cms.InputTag("hltEgammaGsfTrackVarsBestTrkUnseeded","DetaSeed"),
    DphiMap = cms.InputTag("hltEgammaGsfTrackVarsBestTrkUnseeded","Dphi"),
    EcalPFClusterIsoMap = cms.InputTag("hltEgammaEcalPFClusterIsoUnseeded"),
    EgammaCandidates = cms.InputTag("hltEgammaCandidatesUnseeded"),
    EgammaGsfTracks = cms.InputTag("hltEgammaGsfTracksUnseeded"),
    EleGsfTrackIsoMap = cms.InputTag("hltEgammaEleGsfTrackIsoUnseeded"),
    HcalPFClusterIsoMap = cms.InputTag("hltEgammaHcalPFClusterIsoUnseeded"),
    HoverEMap = cms.InputTag("hltEgammaHoverEUnseeded"),
    MissingHitsMap = cms.InputTag("hltEgammaGsfTrackVarsBestTrkUnseeded","MissingHits"),
    OneOEMinusOneOPMap = cms.InputTag("hltEgammaGsfTrackVarsBestTrkUnseeded","OneOESuperMinusOneOP"),
    SigmaIEtaIEtaMap = cms.InputTag("hltEgammaClusterShapeUnseeded","sigmaIEtaIEta5x5NoiseCleaned"),
    absEtaBinUpperEdges = cms.vdouble(1.479, 5.0),
    ecalRechitEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
    ecalRechitEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
    egammaEtaCut = cms.double(2.5),
    egammaHoverECut = cms.double(9999.0),
    egammaPtCut = cms.double(2.0),
    egammaSigmaIEtaIEtaCut = cms.vdouble(99999.0, 99999.0),
    fBremMap = cms.InputTag("hltEgammaGsfTrackVarsBestTrkUnseeded","fbrem"),
    mantissaPrecision = cms.int32(10),
    r9Map = cms.InputTag("hltEgammaR9IDUnseeded","r95x5"),
    rechitMatrixSize = cms.int32(10),
    rechitZeroSuppression = cms.bool(True),
    saveRecHitTiming = cms.bool(False)
)


process.hltScoutingMuonPackerNoVtx = cms.EDProducer("HLTScoutingMuonProducer",
    ChargedCandidates = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    EcalPFClusterIsoMap = cms.InputTag("hltMuonEcalMFPFClusterIsoForMuonsNoVtx"),
    HcalPFClusterIsoMap = cms.InputTag("hltMuonHcalPFClusterIsoForMuonsNoVtx"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3LinksNoVtx"),
    InputMuons = cms.InputTag("hltIterL3MuonsNoVtx"),
    TrackIsoMap = cms.InputTag("hltMuonTkRelIsolationCut0p09MapNoVtx","combinedRelativeIsoDeposits"),
    Tracks = cms.InputTag("hltIterL3MuonAndMuonFromL1MergedNoVtx"),
    displacedvertexCollection = cms.InputTag("hltDisplacedmumuVtxNoMatchingProducerNoVtx"),
    minVtxProbCut = cms.double(0.001),
    muonEtaCut = cms.double(2.4),
    muonPtCut = cms.double(0.0)
)


process.hltScoutingMuonPackerVtx = cms.EDProducer("HLTScoutingMuonProducer",
    ChargedCandidates = cms.InputTag("hltIterL3MuonCandidates"),
    EcalPFClusterIsoMap = cms.InputTag("hltMuonEcalMFPFClusterIsoForMuons"),
    HcalPFClusterIsoMap = cms.InputTag("hltMuonHcalRegPFClusterIsoForMuons"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    InputMuons = cms.InputTag("hltIterL3Muons"),
    TrackIsoMap = cms.InputTag("hltMuonTkRelIsolationCut0p14Map","combinedRelativeIsoDeposits"),
    Tracks = cms.InputTag("hltIterL3MuonAndMuonFromL1Merged"),
    displacedvertexCollection = cms.InputTag("hltDisplacedmumuVtxNoMatchingProducerVtx"),
    minVtxProbCut = cms.double(0.001),
    muonEtaCut = cms.double(2.4),
    muonPtCut = cms.double(0.0)
)


process.hltScoutingPFPacker = cms.EDProducer("HLTScoutingPFProducer",
    doCandIndsForJets = cms.bool(False),
    doCandidates = cms.bool(True),
    doJetTags = cms.bool(True),
    doMet = cms.bool(True),
    doTrackVars = cms.bool(True),
    mantissaPrecision = cms.int32(10),
    metCollection = cms.InputTag("hltPFMETProducer"),
    pfCandidateCollection = cms.InputTag("hltParticleFlow"),
    pfCandidateEtaCut = cms.double(3.0),
    pfCandidatePtCut = cms.double(0.6),
    pfJetCollection = cms.InputTag("hltAK4PFJets"),
    pfJetEtaCut = cms.double(5.0),
    pfJetPtCut = cms.double(20.0),
    pfJetTagCollection = cms.InputTag(""),
    relativeTrackVars = cms.bool(True),
    rho = cms.InputTag("hltFixedGridRhoFastjetAll"),
    vertexCollection = cms.InputTag("hltPixelVertices")
)


process.hltScoutingPrimaryVertexPacker = cms.EDProducer("HLTScoutingPrimaryVertexProducer",
    mantissaPrecision = cms.int32(10),
    vertexCollection = cms.InputTag("hltPixelVertices")
)


process.hltScoutingRecHitPacker = cms.EDProducer("HLTScoutingRecHitProducer",
    mantissaPrecision = cms.int32(10),
    minEnergyCleanedEB = cms.double(-1.0),
    minEnergyCleanedEE = cms.double(-1.0),
    minEnergyEB = cms.double(-1.0),
    minEnergyEE = cms.double(-1.0),
    minEnergyHBHE = cms.double(1.0),
    pfRecHitsECAL = cms.InputTag("hltParticleFlowRecHitECALUnseeded"),
    pfRecHitsECALCleaned = cms.InputTag("hltParticleFlowRecHitECALUnseeded","Cleaned"),
    pfRecHitsHBHE = cms.InputTag("hltParticleFlowRecHitHBHE")
)


process.hltScoutingTrackPacker = cms.EDProducer("HLTScoutingTrackProducer",
    OtherTracks = cms.InputTag("hltPFMuonMerging"),
    mantissaPrecision = cms.int32(10),
    ptMin = cms.double(1.0),
    vertexCollection = cms.InputTag("hltPixelVertices"),
    vtxMinDist = cms.double(999.0)
)


process.hltSiPixelClusters = cms.EDProducer("SiPixelDigisClustersFromSoAAlpakaPhase1",
    clusterThreshold_layer1 = cms.int32(2000),
    clusterThreshold_otherLayers = cms.int32(4000),
    produceDigis = cms.bool(False),
    src = cms.InputTag("hltSiPixelClustersSoA"),
    storeDigis = cms.bool(False)
)


process.hltSiPixelClustersSoA = cms.EDProducer("SiPixelRawToClusterPhase1@alpaka",
    CablingMapLabel = cms.string(''),
    DoDigiMorphing = cms.bool(False),
    IncludeErrors = cms.bool(True),
    InputLabel = cms.InputTag("rawDataCollector"),
    MaxFakesInModule = cms.uint32(2400),
    Regions = cms.PSet(

    ),
    UseQualityInfo = cms.bool(False),
    VCaltoElectronGain = cms.double(1.0),
    VCaltoElectronGain_L1 = cms.double(1.0),
    VCaltoElectronOffset = cms.double(0.0),
    VCaltoElectronOffset_L1 = cms.double(0.0),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    barrelRegions = cms.vstring(
        '1,1-12,1-2',
        '1,1-12,7-8',
        '2,1-28,1',
        '2,1-28,8'
    ),
    clusterThreshold_layer1 = cms.int32(2000),
    clusterThreshold_otherLayers = cms.int32(4000),
    endcapRegions = cms.vstring()
)


process.hltSiPixelDigiErrors = cms.EDProducer("SiPixelDigiErrorsFromSoAAlpaka",
    CablingMapLabel = cms.string(''),
    ErrorList = cms.vint32(29),
    UsePhase1 = cms.bool(True),
    UserErrorList = cms.vint32(40),
    digiErrorSoASrc = cms.InputTag("hltSiPixelClustersSoA"),
    fmtErrorsSoASrc = cms.InputTag("hltSiPixelClustersSoA")
)


process.hltSiPixelRecHits = cms.EDProducer("SiPixelRecHitFromSoAAlpakaPhase1",
    pixelRecHitSrc = cms.InputTag("hltSiPixelRecHitsSoA"),
    src = cms.InputTag("hltSiPixelClusters")
)


process.hltSiPixelRecHitsSoA = cms.EDProducer("SiPixelRecHitAlpakaPhase1@alpaka",
    CPE = cms.string('PixelCPEFastParams'),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    beamSpot = cms.InputTag("hltOnlineBeamSpotDevice"),
    src = cms.InputTag("hltSiPixelClustersSoA")
)


process.hltSiStripExcludedFEDListProducer = cms.EDProducer("SiStripExcludedFEDListProducer",
    ProductLabel = cms.InputTag("rawDataCollector")
)


process.hltSiStripRawToClustersFacility = cms.EDProducer("SiStripClusterizerFromRaw",
    Algorithms = cms.PSet(
        CommonModeNoiseSubtractionMode = cms.string('Median'),
        PedestalSubtractionFedMode = cms.bool(True),
        SiStripFedZeroSuppressionMode = cms.uint32(4),
        TruncateInSuppressor = cms.bool(True),
        Use10bitsTruncation = cms.bool(False),
        doAPVRestore = cms.bool(False),
        useCMMeanMap = cms.bool(False)
    ),
    Clusterizer = cms.PSet(
        Algorithm = cms.string('ThreeThresholdAlgorithm'),
        ChannelThreshold = cms.double(2.0),
        ClusterThreshold = cms.double(5.0),
        ConditionsLabel = cms.string(''),
        MaxAdjacentBad = cms.uint32(0),
        MaxClusterSize = cms.uint32(16),
        MaxSequentialBad = cms.uint32(1),
        MaxSequentialHoles = cms.uint32(0),
        RemoveApvShots = cms.bool(True),
        SeedThreshold = cms.double(3.0),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        setDetId = cms.bool(True)
    ),
    ConditionsLabel = cms.string(''),
    DoAPVEmulatorCheck = cms.bool(False),
    HybridZeroSuppressed = cms.bool(False),
    LegacyUnpacker = cms.bool(False),
    ProductLabel = cms.InputTag("rawDataCollector"),
    onDemand = cms.bool(False)
)


process.hltSiStripRawToClustersFacilityOnDemand = cms.EDProducer("SiStripClusterizerFromRaw",
    Algorithms = cms.PSet(
        CommonModeNoiseSubtractionMode = cms.string('Median'),
        PedestalSubtractionFedMode = cms.bool(True),
        SiStripFedZeroSuppressionMode = cms.uint32(4),
        TruncateInSuppressor = cms.bool(True),
        Use10bitsTruncation = cms.bool(False),
        doAPVRestore = cms.bool(False),
        useCMMeanMap = cms.bool(False)
    ),
    Clusterizer = cms.PSet(
        Algorithm = cms.string('ThreeThresholdAlgorithm'),
        ChannelThreshold = cms.double(2.0),
        ClusterThreshold = cms.double(5.0),
        ConditionsLabel = cms.string(''),
        MaxAdjacentBad = cms.uint32(0),
        MaxClusterSize = cms.uint32(16),
        MaxSequentialBad = cms.uint32(1),
        MaxSequentialHoles = cms.uint32(0),
        RemoveApvShots = cms.bool(True),
        SeedThreshold = cms.double(3.0),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        setDetId = cms.bool(True)
    ),
    ConditionsLabel = cms.string(''),
    DoAPVEmulatorCheck = cms.bool(False),
    HybridZeroSuppressed = cms.bool(False),
    LegacyUnpacker = cms.bool(False),
    ProductLabel = cms.InputTag("rawDataCollector"),
    onDemand = cms.bool(True)
)


process.hltSiStripRecHits = cms.EDProducer("SiStripRecHitConverter",
    ClusterProducer = cms.InputTag("hltSiStripRawToClustersFacility"),
    MaskBadAPVFibers = cms.bool(False),
    Matcher = cms.ESInputTag("SiStripRecHitMatcherESProducer","StandardMatcher"),
    StripCPE = cms.ESInputTag("hltESPStripCPEfromTrackAngle","hltESPStripCPEfromTrackAngle"),
    doMatching = cms.bool(False),
    matchedRecHits = cms.string('matchedRecHit'),
    rphiRecHits = cms.string('rphiRecHit'),
    siStripQualityLabel = cms.ESInputTag("",""),
    stereoRecHits = cms.string('stereoRecHit'),
    useSiStripQuality = cms.bool(False)
)


process.hltTowerMakerForAll = cms.EDProducer("CaloTowersCreator",
    AllowMissingInputs = cms.bool(False),
    EBGrid = cms.vdouble(),
    EBSumThreshold = cms.double(0.2),
    EBThreshold = cms.double(0.07),
    EBWeight = cms.double(1.0),
    EBWeights = cms.vdouble(),
    EEGrid = cms.vdouble(),
    EESumThreshold = cms.double(0.45),
    EEThreshold = cms.double(0.3),
    EEWeight = cms.double(1.0),
    EEWeights = cms.vdouble(),
    EcalRecHitSeveritiesToBeExcluded = cms.vstring(
        'kTime',
        'kWeird',
        'kBad'
    ),
    EcalRecHitThresh = cms.bool(True),
    EcalSeveritiesToBeUsedInBadTowers = cms.vstring(),
    EcutTower = cms.double(-1000.0),
    HBGrid = cms.vdouble(),
    HBThreshold = cms.double(0.3),
    HBThreshold1 = cms.double(0.4),
    HBThreshold2 = cms.double(0.3),
    HBWeight = cms.double(1.0),
    HBWeights = cms.vdouble(),
    HEDGrid = cms.vdouble(),
    HEDThreshold = cms.double(0.2),
    HEDThreshold1 = cms.double(0.1),
    HEDWeight = cms.double(1.0),
    HEDWeights = cms.vdouble(),
    HESGrid = cms.vdouble(),
    HESThreshold = cms.double(0.2),
    HESThreshold1 = cms.double(0.1),
    HESWeight = cms.double(1.0),
    HESWeights = cms.vdouble(),
    HF1Grid = cms.vdouble(),
    HF1Threshold = cms.double(0.5),
    HF1Weight = cms.double(1.0),
    HF1Weights = cms.vdouble(),
    HF2Grid = cms.vdouble(),
    HF2Threshold = cms.double(0.85),
    HF2Weight = cms.double(1.0),
    HF2Weights = cms.vdouble(),
    HOGrid = cms.vdouble(),
    HOThreshold0 = cms.double(3.5),
    HOThresholdMinus1 = cms.double(3.5),
    HOThresholdMinus2 = cms.double(3.5),
    HOThresholdPlus1 = cms.double(3.5),
    HOThresholdPlus2 = cms.double(3.5),
    HOWeight = cms.double(1e-99),
    HOWeights = cms.vdouble(),
    HcalAcceptSeverityLevel = cms.uint32(9),
    HcalAcceptSeverityLevelForRejectedHit = cms.uint32(9999),
    HcalPhase = cms.int32(1),
    HcalThreshold = cms.double(-1000.0),
    MomConstrMethod = cms.int32(1),
    MomEBDepth = cms.double(0.3),
    MomEEDepth = cms.double(0.0),
    MomHBDepth = cms.double(0.2),
    MomHEDepth = cms.double(0.4),
    UseEcalRecoveredHits = cms.bool(False),
    UseEtEBTreshold = cms.bool(False),
    UseEtEETreshold = cms.bool(False),
    UseHO = cms.bool(False),
    UseHcalRecoveredHits = cms.bool(False),
    UseRejectedHitsOnly = cms.bool(False),
    UseRejectedRecoveredEcalHits = cms.bool(False),
    UseRejectedRecoveredHcalHits = cms.bool(False),
    UseSymEBTreshold = cms.bool(False),
    UseSymEETreshold = cms.bool(False),
    ecalInputs = cms.VInputTag("hltEcalRecHit:EcalRecHitsEB", "hltEcalRecHit:EcalRecHitsEE"),
    hbheInput = cms.InputTag("hltHbhereco"),
    hfInput = cms.InputTag("hltHfreco"),
    hoInput = cms.InputTag("hltHoreco"),
    missingHcalRescaleFactorForEcal = cms.double(0.0),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltTriggerSummaryAOD = cms.EDProducer("TriggerSummaryProducerAOD",
    moduleLabelPatternsToMatch = cms.vstring('hlt*'),
    moduleLabelPatternsToSkip = cms.vstring(),
    processName = cms.string('@'),
    throw = cms.bool(False)
)


process.hltTriggerSummaryRAW = cms.EDProducer("TriggerSummaryProducerRAW",
    processName = cms.string('@')
)


process.hltTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
    PVcomparer = cms.PSet(
        refToPSet_ = cms.string('HLTPSetPvClusterComparerForIT')
    ),
    fractionSumPt2 = cms.double(0.3),
    maxVtx = cms.uint32(100),
    minSumPt2 = cms.double(0.0),
    src = cms.InputTag("hltPixelVertices")
)


process.packGtStage2 = cms.EDProducer("L1TDigiToRaw",
    CICADAScoreInputTag = cms.InputTag("unpackGtStage2","CICADAScore"),
    EGammaInputTag = cms.InputTag("unpackGtStage2","EGamma"),
    EtSumInputTag = cms.InputTag("unpackGtStage2","EtSum"),
    EtSumZDCInputTag = cms.InputTag("unpackGtStage2","EtSumZDC"),
    ExtInputTag = cms.InputTag("unpackGtStage2"),
    FWId = cms.uint32(4432),
    FedId = cms.int32(1404),
    GtInputTag = cms.InputTag("simGtStage2Digis"),
    JetInputTag = cms.InputTag("unpackGtStage2","Jet"),
    MuonInputTag = cms.InputTag("unpackGtStage2","Muon"),
    Setup = cms.string('stage2::GTSetup'),
    ShowerInputLabel = cms.InputTag("unpackGtStage2","MuonShower"),
    TauInputTag = cms.InputTag("unpackGtStage2","Tau"),
    lenSlinkHeader = cms.untracked.int32(8),
    lenSlinkTrailer = cms.untracked.int32(8)
)


process.rawDataCollector = cms.EDProducer("RawDataCollectorByLabel",
    RawCollectionList = cms.VInputTag("packGtStage2", cms.InputTag("rawDataCollector","","@skipCurrentProcess")),
    mightGet = cms.optional.untracked.vstring,
    verbose = cms.untracked.int32(0)
)


process.simGtExtFakeStage2Digis = cms.EDProducer("L1TExtCondProducer",
    bxFirst = cms.int32(-2),
    bxLast = cms.int32(2),
    setBptxAND = cms.bool(True),
    setBptxMinus = cms.bool(True),
    setBptxOR = cms.bool(True),
    setBptxPlus = cms.bool(True),
    tcdsRecordLabel = cms.InputTag("unpackTcds","tcdsRecord")
)


process.simGtStage2Digis = cms.EDProducer("L1TGlobalProducer",
    AlgoBlkInputTag = cms.InputTag("gtStage2Digis"),
    AlgorithmTriggersUnmasked = cms.bool(True),
    AlgorithmTriggersUnprescaled = cms.bool(True),
    CICADAInputTag = cms.InputTag("unpackGtStage2","CICADAScore"),
    EGammaInputTag = cms.InputTag("unpackGtStage2","EGamma"),
    EtSumInputTag = cms.InputTag("unpackGtStage2","EtSum"),
    EtSumZdcInputTag = cms.InputTag("unpackGtStage2","EtSumZDC"),
    ExtInputTag = cms.InputTag("unpackGtStage2"),
    GetPrescaleColumnFromData = cms.bool(False),
    JetInputTag = cms.InputTag("unpackGtStage2","Jet"),
    MuonInputTag = cms.InputTag("unpackGtStage2","Muon"),
    MuonShowerInputTag = cms.InputTag("unpackGtStage2","MuonShower"),
    RequireMenuToMatchAlgoBlkInput = cms.bool(False),
    TauInputTag = cms.InputTag("unpackGtStage2","Tau"),
    useMuonShowers = cms.bool(True)
)


process.unpackGtStage2 = cms.EDProducer("L1TRawToDigi",
    FedIds = cms.vint32(1404),
    InputLabel = cms.InputTag("rawDataCollector","","@skipCurrentProcess"),
    Setup = cms.string('stage2::GTSetup')
)


process.unpackTcds = cms.EDProducer("TcdsRawToDigi",
    InputLabel = cms.InputTag("rawDataCollector","","@skipCurrentProcess"),
    mightGet = cms.optional.untracked.vstring
)


process.hltAK4CaloJetsPFEt5 = cms.EDFilter("EtMinCaloJetSelector",
    etMin = cms.double(5.0),
    filter = cms.bool(False),
    src = cms.InputTag("hltAK4CaloJetsPF")
)


process.hltBoolEnd = cms.EDFilter("HLTBool",
    result = cms.bool(True)
)


process.hltBoolFalse = cms.EDFilter("HLTBool",
    result = cms.bool(False)
)


process.hltDatasetTestDataRaw = cms.EDFilter("TriggerResultsFilter",
    hltResults = cms.InputTag(""),
    l1tIgnoreMaskAndPrescale = cms.bool(False),
    l1tResults = cms.InputTag(""),
    throw = cms.bool(True),
    triggerConditions = cms.vstring('HLT_TestData_v1'),
    usePathStatus = cms.bool(True)
)


process.hltDatasetTestDataScouting = cms.EDFilter("TriggerResultsFilter",
    hltResults = cms.InputTag(""),
    l1tIgnoreMaskAndPrescale = cms.bool(False),
    l1tResults = cms.InputTag(""),
    throw = cms.bool(True),
    triggerConditions = cms.vstring('HLT_TestData_v1'),
    usePathStatus = cms.bool(True)
)


process.hltDiEG5TightIDMWEtUnseededFilter = cms.EDFilter("HLT1Photon",
    MaxEta = cms.double(1.479),
    MaxMass = cms.double(-1.0),
    MinE = cms.double(-1.0),
    MinEta = cms.double(-1.479),
    MinMass = cms.double(-1.0),
    MinN = cms.int32(2),
    MinPt = cms.double(5.0),
    inputTag = cms.InputTag("hltEgammaCandidatesUnseeded"),
    saveTags = cms.bool(True),
    triggerType = cms.int32(92)
)


process.hltDiMuon178RelTrkIsoVVLFiltered = cms.EDFilter("HLTMuonIsoFilter",
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    DepTag = cms.VInputTag("hltL3MuonRelTrkIsolationVVL"),
    IsolatorPSet = cms.PSet(

    ),
    MinN = cms.int32(2),
    PreviousCandTag = cms.InputTag("hltL3fL1DoubleMu155fPreFiltered8"),
    saveTags = cms.bool(True)
)


process.hltDiMuon178RelTrkIsoVVLFilteredDzFiltered0p2 = cms.EDFilter("HLT2MuonMuonDZ",
    MaxDZ = cms.double(0.2),
    MinDR = cms.double(0.001),
    MinN = cms.int32(1),
    MinPixHitsForDZ = cms.int32(0),
    checkSC = cms.bool(False),
    inputTag1 = cms.InputTag("hltDiMuon178RelTrkIsoVVLFiltered"),
    inputTag2 = cms.InputTag("hltDiMuon178RelTrkIsoVVLFiltered"),
    originTag1 = cms.VInputTag("hltIterL3MuonCandidates"),
    originTag2 = cms.VInputTag("hltIterL3MuonCandidates"),
    saveTags = cms.bool(True),
    triggerType1 = cms.int32(83),
    triggerType2 = cms.int32(83)
)


process.hltDoubleEG11CaloIdLClusterShapeFilter = cms.EDFilter("HLTEgammaGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltDoubleEG11CaloIdLEt11Filter"),
    doRhoCorrection = cms.bool(False),
    effectiveAreas = cms.vdouble(0.0, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(2),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag(""),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(-1.0),
    thrOverEEE = cms.vdouble(-1.0),
    thrRegularEB = cms.vdouble(0.014),
    thrRegularEE = cms.vdouble(0.035),
    useAbs = cms.bool(False),
    useEt = cms.bool(False),
    varTag = cms.InputTag("hltEgammaClusterShape","sigmaIEtaIEta5x5NoiseCleaned")
)


process.hltDoubleEG11CaloIdLEt11Filter = cms.EDFilter("HLTEgammaEtFilter",
    etcutEB = cms.double(11.0),
    etcutEE = cms.double(11.0),
    inputTag = cms.InputTag("hltEGL1DoubleIsoEG11Filter"),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    maxEtaCut = cms.double(2.1),
    minEtaCut = cms.double(-2.1),
    ncandcut = cms.int32(2),
    saveTags = cms.bool(True)
)


process.hltDoubleEG11CaloIdLHEFilter = cms.EDFilter("HLTEgammaGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltDoubleEG11CaloIdLClusterShapeFilter"),
    doRhoCorrection = cms.bool(False),
    effectiveAreas = cms.vdouble(0.0, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(2),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag(""),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(0.2),
    thrOverEEE = cms.vdouble(0.2),
    thrRegularEB = cms.vdouble(-1.0),
    thrRegularEE = cms.vdouble(-1.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(False),
    varTag = cms.InputTag("hltEgammaHoverE")
)


process.hltDoubleEGScoutingMonitorJPsiFilter = cms.EDFilter("HLTPMMassFilter",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    candTag = cms.InputTag("hltDoubleEG11CaloIdLHEFilter"),
    isElectron1 = cms.untracked.bool(False),
    isElectron2 = cms.untracked.bool(False),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lowerMassCut = cms.double(2.7),
    lowerdRCut = cms.double(0.0),
    nZcandcut = cms.int32(1),
    reqOppCharge = cms.untracked.bool(False),
    saveTags = cms.bool(True),
    upperMassCut = cms.double(3.5),
    upperdRCut = cms.double(9999.0)
)


process.hltDoubleEGScoutingMonitorZFilter = cms.EDFilter("HLTPMMassFilter",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    candTag = cms.InputTag("hltDoubleEG11CaloIdLHEFilter"),
    isElectron1 = cms.untracked.bool(False),
    isElectron2 = cms.untracked.bool(False),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lowerMassCut = cms.double(80.0),
    lowerdRCut = cms.double(0.0),
    nZcandcut = cms.int32(1),
    reqOppCharge = cms.untracked.bool(False),
    saveTags = cms.bool(True),
    upperMassCut = cms.double(100.0),
    upperdRCut = cms.double(9999.0)
)


process.hltDoubleMuScoutingMonitorJPsiL3Filtered = cms.EDFilter("HLTMuonDimuonL3Filter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    ChargeOpt = cms.int32(-1),
    CutCowboys = cms.bool(False),
    FastAccept = cms.bool(False),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fL1sL1DoubleMuonScouting"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxAcop = cms.double(999.0),
    MaxDCAMuMu = cms.double(0.5),
    MaxDr = cms.double(2.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxInvMass = cms.vdouble(3.5),
    MaxPtBalance = cms.double(999999.0),
    MaxPtMin = cms.vdouble(1e+125),
    MaxPtPair = cms.vdouble(1e+125),
    MaxRapidityPair = cms.double(999999.0),
    MinAcop = cms.double(-999.0),
    MinDiMuonDeltaR = cms.double(-1.0),
    MinInvMass = cms.vdouble(2.7),
    MinN = cms.int32(1),
    MinNhits = cms.int32(0),
    MinPtBalance = cms.double(-1.0),
    MinPtMax = cms.vdouble(0.0),
    MinPtMin = cms.vdouble(0.0),
    MinPtPair = cms.vdouble(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandIsL2 = cms.bool(True),
    PreviousCandTag = cms.InputTag("hltL2fL1sL1DoubleMuonScouting"),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    saveTags = cms.bool(True),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltDoubleMuScoutingMonitorZL3Filtered = cms.EDFilter("HLTMuonDimuonL3Filter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    ChargeOpt = cms.int32(-1),
    CutCowboys = cms.bool(False),
    FastAccept = cms.bool(False),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fL1sL1DoubleMuonScouting"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxAcop = cms.double(999.0),
    MaxDCAMuMu = cms.double(0.5),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxInvMass = cms.vdouble(100.0),
    MaxPtBalance = cms.double(999999.0),
    MaxPtMin = cms.vdouble(1e+125),
    MaxPtPair = cms.vdouble(1e+125),
    MaxRapidityPair = cms.double(999999.0),
    MinAcop = cms.double(-999.0),
    MinDiMuonDeltaR = cms.double(-1.0),
    MinInvMass = cms.vdouble(80.0),
    MinN = cms.int32(1),
    MinNhits = cms.int32(0),
    MinPtBalance = cms.double(-1.0),
    MinPtMax = cms.vdouble(0.0),
    MinPtMin = cms.vdouble(0.0),
    MinPtPair = cms.vdouble(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandIsL2 = cms.bool(True),
    PreviousCandTag = cms.InputTag("hltL2fL1sL1DoubleMuonScouting"),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    saveTags = cms.bool(True),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltDoubleMuonL3PreFilteredScoutingNoVtx = cms.EDFilter("HLTMuonL3PreFilter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidatesNoVtx"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3LinksNoVtx"),
    L1CandTag = cms.InputTag("hltL1fL1sL1DoubleMuonScouting"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxDXYBeamSpot = cms.double(9999.0),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxNormalizedChi2 = cms.double(9999.0),
    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
    MaxPtDifference = cms.double(9999.0),
    MinDXYBeamSpot = cms.double(-1.0),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(2),
    MinNhits = cms.int32(0),
    MinNmuonHits = cms.int32(0),
    MinPt = cms.double(0.0),
    MinTrackPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL2fL1sL1DoubleMuonScoutingNoVtx"),
    allowedTypeMask = cms.uint32(255),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3MuonsNoVtx"),
    minMuonHits = cms.int32(-1),
    minMuonStations = cms.int32(0),
    minTrkHits = cms.int32(-1),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    requireL3MuonTrajectorySeed = cms.bool(False),
    requiredTypeMask = cms.uint32(0),
    saveTags = cms.bool(True),
    trkMuonId = cms.uint32(0),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltDoubleMuonL3PreFilteredScoutingVtx = cms.EDFilter("HLTMuonL3PreFilter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fL1sL1DoubleMuonScouting"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxDXYBeamSpot = cms.double(9999.0),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxNormalizedChi2 = cms.double(9999.0),
    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
    MaxPtDifference = cms.double(9999.0),
    MinDXYBeamSpot = cms.double(-1.0),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(2),
    MinNhits = cms.int32(0),
    MinNmuonHits = cms.int32(0),
    MinPt = cms.double(0.0),
    MinTrackPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL2fL1sL1DoubleMuonScouting"),
    allowedTypeMask = cms.uint32(255),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    minMuonHits = cms.int32(-1),
    minMuonStations = cms.int32(0),
    minTrkHits = cms.int32(-1),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    requireL3MuonTrajectorySeed = cms.bool(False),
    requiredTypeMask = cms.uint32(0),
    saveTags = cms.bool(True),
    trkMuonId = cms.uint32(0),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltEG30EBTightIDTightIsoClusterShapeFilter = cms.EDFilter("HLTEgammaGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltEG30EBTightIDTightIsoEtFilter"),
    doRhoCorrection = cms.bool(False),
    effectiveAreas = cms.vdouble(0.0, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag(""),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(-1.0),
    thrOverEEE = cms.vdouble(-1.0),
    thrRegularEB = cms.vdouble(0.01),
    thrRegularEE = cms.vdouble(0.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(False),
    varTag = cms.InputTag("hltEgammaClusterShape","sigmaIEtaIEta5x5NoiseCleaned")
)


process.hltEG30EBTightIDTightIsoEtFilter = cms.EDFilter("HLTEgammaEtFilter",
    etcutEB = cms.double(30.0),
    etcutEE = cms.double(9999999.0),
    inputTag = cms.InputTag("hltEGL1SingleEGOrFilter"),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    maxEtaCut = cms.double(9999.0),
    minEtaCut = cms.double(-9999.0),
    ncandcut = cms.int32(1),
    saveTags = cms.bool(True)
)


process.hltEG30EBTightIDTightIsoHEFilter = cms.EDFilter("HLTEgammaGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltEG30EBTightIDTightIsoClusterShapeFilter"),
    doRhoCorrection = cms.bool(True),
    effectiveAreas = cms.vdouble(0.14, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(0.04),
    thrOverEEE = cms.vdouble(0.0),
    thrRegularEB = cms.vdouble(-1.0),
    thrRegularEE = cms.vdouble(-1.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(False),
    varTag = cms.InputTag("hltEgammaHoverE")
)


process.hltEG30EBTightIDTightIsoHcalIsoFilter = cms.EDFilter("HLTEgammaGenericQuadraticFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltEG30EBTightIDTightIsotEcalIsoFilter"),
    doRhoCorrection = cms.bool(True),
    effectiveAreas = cms.vdouble(0.3, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(0.0),
    thrOverE2EE = cms.vdouble(0.0),
    thrOverEEB = cms.vdouble(0.005),
    thrOverEEE = cms.vdouble(0.0),
    thrRegularEB = cms.vdouble(3.5),
    thrRegularEE = cms.vdouble(0.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(True),
    varTag = cms.InputTag("hltEgammaHcalPFClusterIso")
)


process.hltEG30EBTightIDTightIsoR9Filter = cms.EDFilter("HLTEgammaGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltEG30EBTightIDTightIsoHEFilter"),
    doRhoCorrection = cms.bool(False),
    effectiveAreas = cms.vdouble(0.0, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(False),
    ncandcut = cms.int32(0),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag(""),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(-1.0),
    thrOverEEE = cms.vdouble(-1.0),
    thrRegularEB = cms.vdouble(0.1),
    thrRegularEE = cms.vdouble(0.1),
    useAbs = cms.bool(False),
    useEt = cms.bool(False),
    varTag = cms.InputTag("hltEgammaR9ID")
)


process.hltEG30EBTightIDTightIsoTrackIsoFilter = cms.EDFilter("HLTEgammaGenericQuadraticFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltEG30EBTightIDTightIsoHcalIsoFilter"),
    doRhoCorrection = cms.bool(True),
    effectiveAreas = cms.vdouble(0.1, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(0.0),
    thrOverE2EE = cms.vdouble(0.0),
    thrOverEEB = cms.vdouble(0.01),
    thrOverEEE = cms.vdouble(0.01),
    thrRegularEB = cms.vdouble(0.0),
    thrRegularEE = cms.vdouble(0.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(True),
    varTag = cms.InputTag("hltEgammaHollowTrackIsoDr0p2")
)


process.hltEG30EBTightIDTightIsotEcalIsoFilter = cms.EDFilter("HLTEgammaGenericQuadraticFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltEG30EBTightIDTightIsoR9Filter"),
    doRhoCorrection = cms.bool(True),
    effectiveAreas = cms.vdouble(0.085, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltEgammaCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag("hltFixedGridRhoFastjetAllCaloForMuons"),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(0.0),
    thrOverE2EE = cms.vdouble(0.0),
    thrOverEEB = cms.vdouble(0.02),
    thrOverEEE = cms.vdouble(0.0),
    thrRegularEB = cms.vdouble(2.0),
    thrRegularEE = cms.vdouble(2.5),
    useAbs = cms.bool(False),
    useEt = cms.bool(True),
    varTag = cms.InputTag("hltEgammaEcalPFClusterIsoDr0p2")
)


process.hltEGL1DoubleIsoEG11Filter = cms.EDFilter("HLTEgammaL1TMatchFilterRegional",
    L1SeedFilterTag = cms.InputTag("hltL1sDSTRun3DoubleEGPFScoutingPixelTracking"),
    barrel_end = cms.double(1.4791),
    candIsolatedTag = cms.InputTag("hltEgammaCandidates"),
    candNonIsolatedTag = cms.InputTag(""),
    doIsolated = cms.bool(False),
    endcap_end = cms.double(2.65),
    l1CenJetsTag = cms.InputTag("hltGtStage2Digis","Jet"),
    l1IsolatedTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    l1NonIsolatedTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    l1TausTag = cms.InputTag("hltGtStage2Digis","Tau"),
    ncandcut = cms.int32(2),
    region_eta_size = cms.double(0.522),
    region_eta_size_ecap = cms.double(1.0),
    region_phi_size = cms.double(1.044),
    saveTags = cms.bool(True)
)


process.hltEGL1SingleEGOrFilter = cms.EDFilter("HLTEgammaL1TMatchFilterRegional",
    L1SeedFilterTag = cms.InputTag("hltL1sSingleEGor"),
    barrel_end = cms.double(1.4791),
    candIsolatedTag = cms.InputTag("hltEgammaCandidates"),
    candNonIsolatedTag = cms.InputTag(""),
    doIsolated = cms.bool(False),
    endcap_end = cms.double(2.65),
    l1CenJetsTag = cms.InputTag("hltGtStage2Digis","Jet"),
    l1IsolatedTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    l1NonIsolatedTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    l1TausTag = cms.InputTag("hltGtStage2Digis","Tau"),
    ncandcut = cms.int32(1),
    region_eta_size = cms.double(0.522),
    region_eta_size_ecap = cms.double(1.0),
    region_phi_size = cms.double(1.044),
    saveTags = cms.bool(True)
)


process.hltEgammaCandidatesWrapperUnseeded = cms.EDFilter("HLTEgammaTriggerFilterObjectWrapper",
    candIsolatedTag = cms.InputTag("hltEgammaCandidatesUnseeded"),
    candNonIsolatedTag = cms.InputTag(""),
    doIsolated = cms.bool(True),
    saveTags = cms.bool(True)
)


process.hltL1fForIterL3L1fL1sDoubleMu155L1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltL1MuonsPt0"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(1),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sDoubleMu155L1Filtered0"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1fForIterL3L1fL1sMu22L1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltL1MuonsPt0"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(1),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sMu22L1Filtered0"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1fForIterL3L1fL1sMuScoutingL1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltL1MuonsPt0"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(1),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sMuScoutingL1Filtered0"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1fL1sDoubleMu155L1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltGtStage2Digis","Muon"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(2),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1sDoubleMu125to157"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1fL1sL1DoubleMuonScouting = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltGtStage2Digis","Muon"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(2),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1sDSTRun3DoubleMuonPFScoutingPixelTracking"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1fL1sMu22L1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltGtStage2Digis","Muon"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(1),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1sSingleMu22"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1fL1sMuScoutingL1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    CandTag = cms.InputTag("hltGtStage2Digis","Muon"),
    CentralBxOnly = cms.bool(True),
    MaxDeltaR = cms.double(0.3),
    MaxEta = cms.double(2.5),
    MinN = cms.int32(1),
    MinPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1sSingleMuScouting"),
    SelectQualities = cms.vint32(),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3AXOLoosePFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_AXO_Loose'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3AXOMediumPFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_AXO_Medium'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3AXOTightPFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_AXO_Tight'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3AXOVLoosePFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_AXO_VLoose'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3AXOVTightPFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_AXO_VTight'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3CICADALoosePFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_CICADA_Loose'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3CICADAMediumPFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_CICADA_Medium'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3CICADATightPFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_CICADA_Tight'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3CICADAVLoosePFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_CICADA_VLoose'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3CICADAVTightPFScoutingTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_CICADA_VTight'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3DoubleEGPFScoutingPixelTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_DoubleEG_LooseIso16_LooseIso12_er1p5 OR L1_DoubleEG_LooseIso18_LooseIso12_er1p5 OR L1_DoubleEG_LooseIso20_LooseIso12_er1p5 OR L1_DoubleEG_LooseIso22_LooseIso12_er1p5 OR L1_DoubleEG15_11_er1p2_dR_Max0p6 OR L1_DoubleEG16_11_er1p2_dR_Max0p6 OR L1_DoubleEG17_11_er1p2_dR_Max0p6'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3DoubleMuonPFScoutingPixelTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_DoubleMu_12_5 OR L1_DoubleMu_15_7 OR L1_DoubleMu4p5er2p0_SQ_OS_Mass_Min7 OR L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18 OR L1_DoubleMu8_SQ OR L1_DoubleMu0er1p4_SQ_OS_dEta_Max1p2 OR L1_DoubleMu4er2p0_SQ_OS_dR_Max1p6 OR L1_DoubleMu5_SQ_OS_dR_Max1p6 OR L1_DoubleMu3er2p0_SQ_OS_dR_Max1p6 OR L1_DoubleMu0er1p5_SQ_OS_dEta_Max1p2 OR L1_DoubleMu0er1p4_OQ_OS_dEta_Max1p6 OR L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5 OR L1_DoubleMu0er1p4_SQ_OS_dR_Max1p4 OR L1_DoubleMu0er1p5_SQ_OS_dR_Max1p4 OR L1_DoubleMu4p5_SQ_OS_dR_Max1p2 OR L1_DoubleMu4_SQ_OS_dR_Max1p2 OR L1_DoubleMu0_Upt15_Upt7 OR L1_DoubleMu0_Upt6_IP_Min1_Upt4 OR L1_DoubleMu0_Upt6_SQ_er2p0 OR L1_DoubleMu0_Upt7_SQ_er2p0 OR L1_DoubleMu0_Upt8_SQ_er2p0 OR L1_DoubleMu0er2p0_SQ_dEta_Max1p6 OR L1_DoubleMu0er2p0_SQ_dEta_Max1p5'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDSTRun3JetHTPFScoutingPixelTracking = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_HTT200er OR L1_HTT255er OR L1_HTT280er OR L1_HTT320er OR L1_HTT360er OR L1_HTT400er OR L1_HTT450er OR L1_ETT2000 OR L1_SingleJet180 OR L1_SingleJet200 OR L1_DoubleJet30er2p5_Mass_Min250_dEta_Max1p5 OR L1_DoubleJet30er2p5_Mass_Min300_dEta_Max1p5 OR L1_DoubleJet30er2p5_Mass_Min330_dEta_Max1p5'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sDoubleMu125to157 = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_DoubleMu_12_5 OR L1_DoubleMu_15_7'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sSingleEGor = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_SingleLooseIsoEG26er2p5 OR L1_SingleLooseIsoEG26er1p5 OR L1_SingleLooseIsoEG28er2p5 OR L1_SingleLooseIsoEG28er2p1 OR L1_SingleLooseIsoEG28er1p5 OR L1_SingleLooseIsoEG30er2p5 OR L1_SingleLooseIsoEG30er1p5 OR L1_SingleEG26er2p5 OR L1_SingleEG38er2p5 OR L1_SingleEG40er2p5 OR L1_SingleEG42er2p5 OR L1_SingleEG45er2p5 OR L1_SingleEG60 OR L1_SingleEG34er2p5 OR L1_SingleEG36er2p5 OR L1_SingleIsoEG24er2p1 OR L1_SingleIsoEG26er2p1 OR L1_SingleIsoEG28er2p1 OR L1_SingleIsoEG30er2p1 OR L1_SingleIsoEG32er2p1 OR L1_SingleIsoEG26er2p5 OR L1_SingleIsoEG28er2p5 OR L1_SingleIsoEG30er2p5 OR L1_SingleIsoEG32er2p5 OR L1_SingleIsoEG34er2p5'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sSingleMu22 = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_SingleMu22'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sSingleMuScouting = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_SingleMu5_BMTF OR L1_SingleMu11_SQ14_BMTF OR L1_SingleMu13_SQ14_BMTF'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL1sZeroBias = cms.EDFilter("HLTL1TSeed",
    L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    L1EtSumZdcInputTag = cms.InputTag("hltGtStage2Digis","EtSumZDC"),
    L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    L1MuonShowerInputTag = cms.InputTag("hltGtStage2Digis","MuonShower"),
    L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    L1SeedsLogicalExpression = cms.string('L1_ZeroBias'),
    L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    saveTags = cms.bool(True)
)


process.hltL2fL1sDoubleMu155L1f0L2Filtered10OneMu = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
    AbsEtaBins = cms.vdouble(0.0),
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltL2MuonCandidates"),
    CutOnChambers = cms.bool(False),
    MatchToPreviousCand = cms.bool(True),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(0),
    MinNchambers = cms.vint32(0),
    MinNhits = cms.vint32(0),
    MinNstations = cms.vint32(0),
    MinPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sDoubleMu155L1Filtered0"),
    SeedMapTag = cms.InputTag("hltL2Muons"),
    saveTags = cms.bool(True)
)


process.hltL2fL1sL1DoubleMuonScouting = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
    AbsEtaBins = cms.vdouble(0.0),
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltL2MuonCandidates"),
    CutOnChambers = cms.bool(False),
    MatchToPreviousCand = cms.bool(True),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(0),
    MinNchambers = cms.vint32(0),
    MinNhits = cms.vint32(0),
    MinNstations = cms.vint32(0),
    MinPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sL1DoubleMuonScouting"),
    SeedMapTag = cms.InputTag("hltL2Muons"),
    saveTags = cms.bool(True)
)


process.hltL2fL1sL1DoubleMuonScoutingNoVtx = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
    AbsEtaBins = cms.vdouble(0.0),
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltL2MuonCandidatesNoVtx"),
    CutOnChambers = cms.bool(False),
    MatchToPreviousCand = cms.bool(True),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(0),
    MinNchambers = cms.vint32(0),
    MinNhits = cms.vint32(0),
    MinNstations = cms.vint32(0),
    MinPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sL1DoubleMuonScouting"),
    SeedMapTag = cms.InputTag("hltL2Muons"),
    saveTags = cms.bool(True)
)


process.hltL2fL1sMuScoutingL2Filtered0 = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
    AbsEtaBins = cms.vdouble(0.0),
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltL2MuonCandidates"),
    CutOnChambers = cms.bool(False),
    MatchToPreviousCand = cms.bool(True),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(0),
    MinNchambers = cms.vint32(0),
    MinNhits = cms.vint32(0),
    MinNstations = cms.vint32(0),
    MinPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sMuScoutingL1Filtered0"),
    SeedMapTag = cms.InputTag("hltL2Muons"),
    saveTags = cms.bool(True)
)


process.hltL2fL1sSingleMu22L1f0L2Filtered10Q = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
    AbsEtaBins = cms.vdouble(0.0),
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltL2MuonCandidates"),
    CutOnChambers = cms.bool(False),
    MatchToPreviousCand = cms.bool(True),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(0),
    MinNchambers = cms.vint32(0),
    MinNhits = cms.vint32(0),
    MinNstations = cms.vint32(0),
    MinPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sMu22L1Filtered0"),
    SeedMapTag = cms.InputTag("hltL2Muons"),
    saveTags = cms.bool(True)
)


process.hltL2pfL1sDoubleMu155L1f0L2PreFiltered0 = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
    AbsEtaBins = cms.vdouble(0.0),
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltL2MuonCandidates"),
    CutOnChambers = cms.bool(False),
    MatchToPreviousCand = cms.bool(True),
    MaxDr = cms.double(9999.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(0),
    MinNchambers = cms.vint32(0),
    MinNhits = cms.vint32(0),
    MinNstations = cms.vint32(0),
    MinPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL1fL1sDoubleMu155L1Filtered0"),
    SeedMapTag = cms.InputTag("hltL2Muons"),
    saveTags = cms.bool(True)
)


process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFiltered = cms.EDFilter("HLTMuonGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q"),
    doRhoCorrection = cms.bool(False),
    effectiveAreas = cms.vdouble(0.0, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltIterL3MuonCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag(""),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(0.14),
    thrOverEEE = cms.vdouble(0.1),
    thrRegularEB = cms.vdouble(-1.0),
    thrRegularEE = cms.vdouble(-1.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(True),
    varTag = cms.InputTag("hltMuonEcalMFPFClusterIsoForMuons")
)


process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFiltered = cms.EDFilter("HLTMuonGenericFilter",
    absEtaLowEdges = cms.vdouble(0.0, 1.479),
    candTag = cms.InputTag("hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFiltered"),
    doRhoCorrection = cms.bool(False),
    effectiveAreas = cms.vdouble(0.0, 0.0),
    energyLowEdges = cms.vdouble(0.0),
    l1EGCand = cms.InputTag("hltIterL3MuonCandidates"),
    lessThan = cms.bool(True),
    ncandcut = cms.int32(1),
    rhoMax = cms.double(99999999.0),
    rhoScale = cms.double(1.0),
    rhoTag = cms.InputTag(""),
    saveTags = cms.bool(True),
    thrOverE2EB = cms.vdouble(-1.0),
    thrOverE2EE = cms.vdouble(-1.0),
    thrOverEEB = cms.vdouble(0.177),
    thrOverEEE = cms.vdouble(0.24),
    thrRegularEB = cms.vdouble(-1.0),
    thrRegularEE = cms.vdouble(-1.0),
    useAbs = cms.bool(False),
    useEt = cms.bool(True),
    varTag = cms.InputTag("hltMuonHcalRegPFClusterIsoForMuons")
)


process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered = cms.EDFilter("HLTMuonIsoFilter",
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    DepTag = cms.VInputTag("hltMuonTkRelIsolationCut0p14Map"),
    IsolatorPSet = cms.PSet(

    ),
    MinN = cms.int32(1),
    PreviousCandTag = cms.InputTag("hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFiltered"),
    saveTags = cms.bool(True)
)


process.hltL3fL1DoubleMu155fFiltered17 = cms.EDFilter("HLTMuonL3PreFilter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fForIterL3L1fL1sDoubleMu155L1Filtered0"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxDXYBeamSpot = cms.double(9999.0),
    MaxDr = cms.double(2.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxNormalizedChi2 = cms.double(9999.0),
    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
    MaxPtDifference = cms.double(9999.0),
    MinDXYBeamSpot = cms.double(-1.0),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(1),
    MinNhits = cms.int32(0),
    MinNmuonHits = cms.int32(0),
    MinPt = cms.double(17.0),
    MinTrackPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL2fL1sDoubleMu155L1f0L2Filtered10OneMu"),
    allowedTypeMask = cms.uint32(255),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    minMuonHits = cms.int32(-1),
    minMuonStations = cms.int32(2),
    minTrkHits = cms.int32(-1),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    requireL3MuonTrajectorySeed = cms.bool(False),
    requiredTypeMask = cms.uint32(0),
    saveTags = cms.bool(True),
    trkMuonId = cms.uint32(0),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltL3fL1DoubleMu155fPreFiltered8 = cms.EDFilter("HLTMuonL3PreFilter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fForIterL3L1fL1sDoubleMu155L1Filtered0"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxDXYBeamSpot = cms.double(9999.0),
    MaxDr = cms.double(2.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxNormalizedChi2 = cms.double(9999.0),
    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
    MaxPtDifference = cms.double(9999.0),
    MinDXYBeamSpot = cms.double(-1.0),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(2),
    MinNhits = cms.int32(0),
    MinNmuonHits = cms.int32(0),
    MinPt = cms.double(8.0),
    MinTrackPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL2pfL1sDoubleMu155L1f0L2PreFiltered0"),
    allowedTypeMask = cms.uint32(255),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    minMuonHits = cms.int32(-1),
    minMuonStations = cms.int32(2),
    minTrkHits = cms.int32(-1),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    requireL3MuonTrajectorySeed = cms.bool(False),
    requiredTypeMask = cms.uint32(0),
    saveTags = cms.bool(True),
    trkMuonId = cms.uint32(0),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltL3fL1sMuScoutingL3Filtered0 = cms.EDFilter("HLTMuonL3PreFilter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fForIterL3L1fL1sMuScoutingL1Filtered0"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxDXYBeamSpot = cms.double(9999.0),
    MaxDr = cms.double(2.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(2.5),
    MaxNormalizedChi2 = cms.double(9999.0),
    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
    MaxPtDifference = cms.double(9999.0),
    MinDXYBeamSpot = cms.double(-1.0),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(1),
    MinNhits = cms.int32(0),
    MinNmuonHits = cms.int32(0),
    MinPt = cms.double(0.0),
    MinTrackPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL2fL1sMuScoutingL2Filtered0"),
    allowedTypeMask = cms.uint32(255),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    minMuonHits = cms.int32(-1),
    minMuonStations = cms.int32(2),
    minTrkHits = cms.int32(-1),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    requireL3MuonTrajectorySeed = cms.bool(False),
    requiredTypeMask = cms.uint32(0),
    saveTags = cms.bool(True),
    trkMuonId = cms.uint32(0),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q = cms.EDFilter("HLTMuonL3PreFilter",
    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
    L1CandTag = cms.InputTag("hltL1fForIterL3L1fL1sMu22L1Filtered0"),
    L1MatchingdR = cms.double(0.3),
    MatchToPreviousCand = cms.bool(True),
    MaxDXYBeamSpot = cms.double(9999.0),
    MaxDr = cms.double(2.0),
    MaxDz = cms.double(9999.0),
    MaxEta = cms.double(1e+99),
    MaxNormalizedChi2 = cms.double(9999.0),
    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
    MaxPtDifference = cms.double(9999.0),
    MinDXYBeamSpot = cms.double(-1.0),
    MinDr = cms.double(-1.0),
    MinDxySig = cms.double(-1.0),
    MinN = cms.int32(1),
    MinNhits = cms.int32(0),
    MinNmuonHits = cms.int32(0),
    MinPt = cms.double(24.0),
    MinTrackPt = cms.double(0.0),
    NSigmaPt = cms.double(0.0),
    PreviousCandTag = cms.InputTag("hltL2fL1sSingleMu22L1f0L2Filtered10Q"),
    allowedTypeMask = cms.uint32(255),
    cosmicPropagationHypothesis = cms.bool(False),
    fallbackToME1 = cms.bool(False),
    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
    minMuonHits = cms.int32(-1),
    minMuonStations = cms.int32(2),
    minTrkHits = cms.int32(-1),
    propagatorAlong = cms.ESInputTag("","hltESPSteppingHelixPropagatorAlong"),
    propagatorAny = cms.ESInputTag("","SteppingHelixPropagatorAny"),
    propagatorOpposite = cms.ESInputTag("","hltESPSteppingHelixPropagatorOpposite"),
    requireL3MuonTrajectorySeed = cms.bool(False),
    requiredTypeMask = cms.uint32(0),
    saveTags = cms.bool(True),
    trkMuonId = cms.uint32(0),
    useMB2InOverlap = cms.bool(False),
    useSimpleGeometry = cms.bool(True),
    useState = cms.string('atVertex'),
    useStation2 = cms.bool(True),
    useTrack = cms.string('tracker')
)


process.hltPreDSTPFScoutingAXOLoose = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingAXOMedium = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingAXOTight = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingAXOVLoose = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingAXOVTight = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingCICADALoose = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingCICADAMedium = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingCICADATight = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingCICADAVLoose = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingCICADAVTight = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleEG = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleEGMonitorJPsi = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleEGMonitorZ = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleMuonNoVtx = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleMuonVtx = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleMuonVtxMonitorJPsi = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingDoubleMuonVtxMonitorZ = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingJetHT = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingSingleMuon = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingSinglePhotonEB = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingSinglePhotonEBMonitorJPsi = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingSinglePhotonEBMonitorZ = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDSTPFScoutingZeroBias = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDatasetTestDataRaw = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreDatasetTestDataScouting = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreIsoMu24 = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreMu17TrkIsoVVLMu8TrkIsoVVLDZ = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltPreTestData = cms.EDFilter("HLTPrescaler",
    L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    offset = cms.uint32(0)
)


process.hltSinglePhotonEBScoutingMonitorJPsiFilter = cms.EDFilter("HLTPMMassFilter",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    candTag = cms.InputTag("hltDiEG5TightIDMWEtUnseededFilter"),
    isElectron1 = cms.untracked.bool(False),
    isElectron2 = cms.untracked.bool(False),
    l1EGCand = cms.InputTag("hltEgammaCandidatesUnseeded"),
    lowerMassCut = cms.double(2.7),
    lowerdRCut = cms.double(0.0),
    nZcandcut = cms.int32(1),
    reqOppCharge = cms.untracked.bool(False),
    saveTags = cms.bool(True),
    upperMassCut = cms.double(3.5),
    upperdRCut = cms.double(9999.0)
)


process.hltSinglePhotonEBScoutingMonitorZFilter = cms.EDFilter("HLTPMMassFilter",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    candTag = cms.InputTag("hltDiEG5TightIDMWEtUnseededFilter"),
    isElectron1 = cms.untracked.bool(False),
    isElectron2 = cms.untracked.bool(False),
    l1EGCand = cms.InputTag("hltEgammaCandidatesUnseeded"),
    lowerMassCut = cms.double(80.0),
    lowerdRCut = cms.double(0.0),
    nZcandcut = cms.int32(1),
    reqOppCharge = cms.untracked.bool(False),
    saveTags = cms.bool(True),
    upperMassCut = cms.double(100.0),
    upperdRCut = cms.double(9999.0)
)


process.hltTriggerType = cms.EDFilter("HLTTriggerTypeFilter",
    SelectedTriggerType = cms.int32(1)
)


process.dqmOutput = cms.OutputModule("DQMRootOutputModule",
    fileName = cms.untracked.string('DQMIO.root')
)


process.hltOutputLocalTestDataRaw = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('Dataset_TestDataRaw')
    ),
    compressionAlgorithm = cms.untracked.string('ZSTD'),
    compressionLevel = cms.untracked.int32(3),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RAW'),
        filterName = cms.untracked.string('')
    ),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('outputLocalTestDataRaw.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
        'keep edmTriggerResults_*_*_HLTX',
        'keep triggerTriggerEvent_*_*_HLTX'
    )
)


process.hltOutputLocalTestDataScouting = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('Dataset_TestDataScouting')
    ),
    compressionAlgorithm = cms.untracked.string('ZSTD'),
    compressionLevel = cms.untracked.int32(3),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RAW'),
        filterName = cms.untracked.string('')
    ),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('outputLocalTestDataScouting.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_hltFEDSelectorL1_*_*',
        'keep *_hltScoutingEgammaPacker_*_*',
        'keep *_hltScoutingMuonPackerNoVtx_*_*',
        'keep *_hltScoutingMuonPackerVtx_*_*',
        'keep *_hltScoutingPFPacker_*_*',
        'keep *_hltScoutingPrimaryVertexPacker_*_*',
        'keep *_hltScoutingRecHitPacker_*_*',
        'keep *_hltScoutingTrackPacker_*_*',
        'keep edmTriggerResults_*_*_*'
    )
)


process.DQMStore = cms.Service("DQMStore",
    MEsToSave = cms.untracked.vstring( (
        'Hcal/DigiTask/Occupancy/depth/depth1',
        'Hcal/DigiTask/Occupancy/depth/depth2',
        'Hcal/DigiTask/Occupancy/depth/depth3',
        'Hcal/DigiTask/Occupancy/depth/depth4',
        'Hcal/DigiTask/Occupancy/depth/depth5',
        'Hcal/DigiTask/Occupancy/depth/depth6',
        'Hcal/DigiTask/Occupancy/depth/depth7',
        'Hcal/DigiTask/Occupancy/depth/depthHO',
        'Hcal/DigiTask/OccupancyCut/depth/depth1',
        'Hcal/DigiTask/OccupancyCut/depth/depth2',
        'Hcal/DigiTask/OccupancyCut/depth/depth3',
        'Hcal/DigiTask/OccupancyCut/depth/depth4',
        'Hcal/DigiTask/OccupancyCut/depth/depth5',
        'Hcal/DigiTask/OccupancyCut/depth/depth6',
        'Hcal/DigiTask/OccupancyCut/depth/depth7',
        'Hcal/DigiTask/OccupancyCut/depth/depthHO',
        'EcalBarrel/EBOccupancyTask/EBOT digi occupancy',
        'EcalEndcap/EEOccupancyTask/EEOT digi occupancy EE -',
        'EcalEndcap/EEOccupancyTask/EEOT digi occupancy EE +',
        'EcalBarrel/EBOccupancyTask/EBOT DCC entries',
        'EcalEndcap/EEOccupancyTask/EEOT DCC entries',
        'Ecal/EventInfo/processedEvents',
        'PixelPhase1/Tracks/charge_PXBarrel',
        'PixelPhase1/Tracks/charge_PXForward',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_1',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_2',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_3',
        'PixelPhase1/Tracks/PXBarrel/charge_PXLayer_4',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_+1',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_+2',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_+3',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_-1',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_-2',
        'PixelPhase1/Tracks/PXForward/charge_PXDisk_-3',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_1',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_2',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_3',
        'PixelPhase1/Tracks/PXBarrel/size_PXLayer_4',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_+1',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_+2',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_+3',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_-1',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_-2',
        'PixelPhase1/Tracks/PXForward/size_PXDisk_-3',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm1',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm2',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm3',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalm4',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp1',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp2',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp3',
        'CSC/CSCOfflineMonitor/recHits/hRHGlobalp4',
        'GEM/RecHits/occ_xy_GE11-M-L1',
        'GEM/RecHits/occ_xy_GE11-M-L2',
        'GEM/RecHits/occ_xy_GE11-P-L1',
        'GEM/RecHits/occ_xy_GE11-P-L2',
        'GEM/Digis/occ_GE11-M-L1',
        'GEM/Digis/occ_GE11-M-L2',
        'GEM/Digis/occ_GE11-P-L1',
        'GEM/Digis/occ_GE11-P-L2',
        'HLT/Vertexing/hltPixelVertices/hltPixelVertices/goodvtxNbr',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_pt',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/mon_unMatched_pt',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_eta',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_hits',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_matched_pt',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_phi',
        'HLT/Tracking/ValidationWRTOffline/hltMergedWrtHighPurityPV/ref_pt',
        'HLT/Tracking/pixelTracks/GeneralProperties/Chi2Prob_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/Chi2oNDFVsEta_ImpactPoint_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/DeltaZToPVZoom_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/DistanceOfClosestApproachToPVVsPhi_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/DistanceOfClosestApproachToPVZoom_GenTk',
        'HLT/Tracking/pixelTracks/GeneralProperties/NumberOfTracks_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/Chi2Prob_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/Chi2oNDFVsEta_ImpactPoint_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/DeltaZToPVZoom_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/DistanceOfClosestApproachToPVVsPhi_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/DistanceOfClosestApproachToPVZoom_GenTk',
        'HLT/Tracking/tracks/GeneralProperties/NumberOfTracks_GenTk',
        'HLT/Tracking/tracks/LUMIanalysis/NumberEventsVsLUMI',
        'HLT/Tracking/tracks/PUmonitoring/NumberEventsVsGoodPVtx',
        'PixelPhase1/Tracks/num_clusters_ontrack_PXBarrel',
        'PixelPhase1/Tracks/num_clusters_ontrack_PXForward',
        'PixelPhase1/Tracks/clusterposition_zphi_ontrack',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_1',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_2',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_3',
        'PixelPhase1/Tracks/PXBarrel/clusterposition_zphi_ontrack_PXLayer_4',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_+1',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_+2',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_+3',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_-1',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_-2',
        'PixelPhase1/Tracks/PXForward/clusterposition_xy_ontrack_PXDisk_-3',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_1',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_2',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_3',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/digi_occupancy_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_4',
        'PixelPhase1/Phase1_MechanicalView/PXForward/digi_occupancy_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_1',
        'PixelPhase1/Phase1_MechanicalView/PXForward/digi_occupancy_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_2',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_1',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_2',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_3',
        'PixelPhase1/Phase1_MechanicalView/PXBarrel/clusters_per_SignedModuleCoord_per_SignedLadderCoord_PXLayer_4',
        'PixelPhase1/Phase1_MechanicalView/PXForward/clusters_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_1',
        'PixelPhase1/Phase1_MechanicalView/PXForward/clusters_per_SignedDiskCoord_per_SignedBladePanelCoord_PXRing_2',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/NormalizedHitResiduals_TEC__wheel__1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_2/NormalizedHitResiduals_TEC__wheel__2',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_3/NormalizedHitResiduals_TEC__wheel__3',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_4/NormalizedHitResiduals_TEC__wheel__4',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_5/NormalizedHitResiduals_TEC__wheel__5',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_6/NormalizedHitResiduals_TEC__wheel__6',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_7/NormalizedHitResiduals_TEC__wheel__7',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_8/NormalizedHitResiduals_TEC__wheel__8',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_9/NormalizedHitResiduals_TEC__wheel__9',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_1/NormalizedHitResiduals_TEC__wheel__1',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_2/NormalizedHitResiduals_TEC__wheel__2',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_3/NormalizedHitResiduals_TEC__wheel__3',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_4/NormalizedHitResiduals_TEC__wheel__4',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_5/NormalizedHitResiduals_TEC__wheel__5',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_6/NormalizedHitResiduals_TEC__wheel__6',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_7/NormalizedHitResiduals_TEC__wheel__7',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_8/NormalizedHitResiduals_TEC__wheel__8',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_9/NormalizedHitResiduals_TEC__wheel__9',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__2',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__3',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_4/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__4',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_5/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__5',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_6/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__6',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_7/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__7',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_8/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__8',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_9/Summary_ClusterStoNCorr__OnTrack__TEC__PLUS__wheel__9',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__1',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__2',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__3',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_4/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__4',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_5/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__5',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_6/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__6',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_7/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__7',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_8/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__8',
        'SiStrip/MechanicalView/TEC/MINUS/wheel_9/Summary_ClusterStoNCorr__OnTrack__TEC__MINUS__wheel__9',
        'SiStrip/MechanicalView/TIB/layer_1/NormalizedHitResiduals_TIB__Layer__1',
        'SiStrip/MechanicalView/TIB/layer_2/NormalizedHitResiduals_TIB__Layer__2',
        'SiStrip/MechanicalView/TIB/layer_3/NormalizedHitResiduals_TIB__Layer__3',
        'SiStrip/MechanicalView/TIB/layer_4/NormalizedHitResiduals_TIB__Layer__4',
        'SiStrip/MechanicalView/TIB/layer_1/Summary_ClusterStoNCorr__OnTrack__TIB__layer__1',
        'SiStrip/MechanicalView/TIB/layer_2/Summary_ClusterStoNCorr__OnTrack__TIB__layer__2',
        'SiStrip/MechanicalView/TIB/layer_3/Summary_ClusterStoNCorr__OnTrack__TIB__layer__3',
        'SiStrip/MechanicalView/TIB/layer_4/Summary_ClusterStoNCorr__OnTrack__TIB__layer__4',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/NormalizedHitResiduals_TID__wheel__1',
        'SiStrip/MechanicalView/TID/PLUS/wheel_2/NormalizedHitResiduals_TID__wheel__2',
        'SiStrip/MechanicalView/TID/PLUS/wheel_3/NormalizedHitResiduals_TID__wheel__3',
        'SiStrip/MechanicalView/TID/MINUS/wheel_1/NormalizedHitResiduals_TID__wheel__1',
        'SiStrip/MechanicalView/TID/MINUS/wheel_2/NormalizedHitResiduals_TID__wheel__2',
        'SiStrip/MechanicalView/TID/MINUS/wheel_3/NormalizedHitResiduals_TID__wheel__3',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TID__PLUS__wheel__1',
        'SiStrip/MechanicalView/TID/PLUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TID__PLUS__wheel__2',
        'SiStrip/MechanicalView/TID/PLUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TID__PLUS__wheel__3',
        'SiStrip/MechanicalView/TID/MINUS/wheel_1/Summary_ClusterStoNCorr__OnTrack__TID__MINUS__wheel__1',
        'SiStrip/MechanicalView/TID/MINUS/wheel_2/Summary_ClusterStoNCorr__OnTrack__TID__MINUS__wheel__2',
        'SiStrip/MechanicalView/TID/MINUS/wheel_3/Summary_ClusterStoNCorr__OnTrack__TID__MINUS__wheel__3',
        'SiStrip/MechanicalView/TOB/layer_1/NormalizedHitResiduals_TOB__Layer__1',
        'SiStrip/MechanicalView/TOB/layer_2/NormalizedHitResiduals_TOB__Layer__2',
        'SiStrip/MechanicalView/TOB/layer_3/NormalizedHitResiduals_TOB__Layer__3',
        'SiStrip/MechanicalView/TOB/layer_4/NormalizedHitResiduals_TOB__Layer__4',
        'SiStrip/MechanicalView/TOB/layer_5/NormalizedHitResiduals_TOB__Layer__5',
        'SiStrip/MechanicalView/TOB/layer_6/NormalizedHitResiduals_TOB__Layer__6',
        'SiStrip/MechanicalView/TOB/layer_1/Summary_ClusterStoNCorr__OnTrack__TOB__layer__1',
        'SiStrip/MechanicalView/TOB/layer_2/Summary_ClusterStoNCorr__OnTrack__TOB__layer__2',
        'SiStrip/MechanicalView/TOB/layer_3/Summary_ClusterStoNCorr__OnTrack__TOB__layer__3',
        'SiStrip/MechanicalView/TOB/layer_4/Summary_ClusterStoNCorr__OnTrack__TOB__layer__4',
        'SiStrip/MechanicalView/TOB/layer_5/Summary_ClusterStoNCorr__OnTrack__TOB__layer__5',
        'SiStrip/MechanicalView/TOB/layer_6/Summary_ClusterStoNCorr__OnTrack__TOB__layer__6',
        'SiStrip/MechanicalView/MainDiagonal Position',
        'SiStrip/MechanicalView/NumberOfClustersInPixel',
        'SiStrip/MechanicalView/NumberOfClustersInStrip',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/TkHMap_NumberOfDigi_TIDP_D1',
        'SiStrip/MechanicalView/TID/PLUS/wheel_1/TkHMap_NumberOfCluster_TIDP_D1',
        'SiStrip/MechanicalView/TIB/layer_1/TkHMap_NumberOfDigi_TIB_L1',
        'SiStrip/MechanicalView/TIB/layer_1/TkHMap_NumberOfCluster_TIB_L1',
        'SiStrip/MechanicalView/TOB/layer_1/TkHMap_NumberOfDigi_TOB_L1',
        'SiStrip/MechanicalView/TOB/layer_1/TkHMap_NumberOfCluster_TOB_L1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/TkHMap_NumberOfDigi_TECP_W1',
        'SiStrip/MechanicalView/TEC/PLUS/wheel_1/TkHMap_NumberOfCluster_TECP_W1',
        'Tracking/TrackParameters/generalTracks/LSanalysis/Chi2oNDF_lumiFlag_GenTk',
        'Tracking/TrackParameters/generalTracks/LSanalysis/NumberOfRecHitsPerTrack_lumiFlag_GenTk',
        'Tracking/TrackParameters/generalTracks/LSanalysis/NumberOfTracks_lumiFlag_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/SIPDxyToPV_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/SIPDzToPV_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/SIP3DToPV_GenTk',
        'Tracking/TrackParameters/generalTracks/HitProperties/NumberOfMissingOuterRecHitsPerTrack_GenTk',
        'Tracking/TrackParameters/generalTracks/HitProperties/NumberMORecHitsPerTrackVsPt_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEtaPhi_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/NumberOfTracks_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPt_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/Chi2oNDF_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackPhi_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackEta_ImpactPoint_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_Strip_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/HitProperties/NumberOfRecHitsPerTrack_Pixel_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBS_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBSdz_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBSVsPhi_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/DistanceOfClosestApproachToBSVsEta_GenTk',
        'Tracking/TrackParameters/highPurityTracks/pt_1/GeneralProperties/TrackQoverP_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/Quality_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/NumberofTracks_Hardvtx_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/NumberofTracks_PUvtx_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackPtHighpurity_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackPtTight_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackPtLoose_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaHighpurity_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaTight_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TrackEtaLoose_ImpactPoint_GenTk',
        'Tracking/PrimaryVertices/highPurityTracks/pt_0to1/offline/NumberOfGoodPVtx_offline',
        'Tracking/PrimaryVertices/highPurityTracks/pt_0to1/offline/GoodPVtxNumberOfTracks_offline',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/NumberofTracks_Hardvtx_PUvtx_GenTk',
        'Tracking/PrimaryVertices/highPurityTracks/pt_0to1/offline/FractionOfGoodPVtx_offline',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_Ratio_byFoldingmap_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_Ratio_byFoldingmap_op_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_RelativeDifference_byFoldingmap_ImpactPoint_GenTk',
        'Tracking/TrackParameters/generalTracks/GeneralProperties/TkEtaPhi_RelativeDifference_byFoldingmap_op_ImpactPoint_GenTk',
        'OfflinePV/offlinePrimaryVertices/tagVtxProb',
        'OfflinePV/offlinePrimaryVertices/tagType',
        'OfflinePV/Resolution/PV/pull_x',
        'OfflinePV/Resolution/PV/pull_y',
        'OfflinePV/Resolution/PV/pull_z',
        'OfflinePV/offlinePrimaryVertices/tagDiffX',
        'OfflinePV/offlinePrimaryVertices/tagDiffY',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_highPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_mediumPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/CHFrac_lowPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_highPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_highPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_mediumPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_mediumPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_lowPt_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/ChMultiplicity_lowPt_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Constituents',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Eta',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Eta_uncor',
        'JetMET/Jet/Cleanedak4PFJetsCHS/JetEnergyCorr',
        'JetMET/Jet/Cleanedak4PFJetsCHS/NJets',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Phi',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Phi_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Phi_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsCHS/Pt',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/PtJetMET/Jet/Cleanedak4PFJetsPuppi/Phi',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Phi_Barrel',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Phi_EndCap',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/JetEnergyCorr',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/NJets',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Eta',
        'JetMET/Jet/Cleanedak4PFJetsPuppi/Eta_uncor',
        'JetMET/MET/pfMETT1/Cleaned/METSig',
        'JetMET/vertices',
        'JetMET/HIJetValidation/akCs4PFJets/SumPFPt',
        'JetMET/HIJetValidation/akCs4PFJets/NJets',
        'JetMET/HIJetValidation/akCs4PFJets/NPFpart',
        'JetMET/HIJetValidation/akPu4CaloJets/SumCaloPt',
        'JetMET/HIJetValidation/akPu4CaloJets/NCalopart',
        'JetMET/HIJetValidation/akPu4CaloJets/NJets',
        'Muons/MuonRecoAnalyzer/GlbMuon_Glb_pt',
        'Muons/MuonRecoAnalyzer/GlbMuon_Glb_eta',
        'Muons/MuonRecoAnalyzer/GlbMuon_Glb_phi',
        'Muons/MuonRecoAnalyzer/Res_TkGlb_qOverlap',
        'Muons/diMuonHistograms/GlbGlbMuon_LM',
        'Muons/diMuonHistograms/GlbGlbMuon_HM',
        'Muons/Isolation/global/relPFIso_R03',
        'Muons/globalMuons/GeneralProperties/NumberOfMeanRecHitsPerTrack_glb',
        'Muons/standAloneMuonsUpdatedAtVtx/HitProperties/NumberOfValidRecHitsPerTrack_sta',
        'Muons/MuonRecoOneHLT/GlbMuon_Glb_pt',
        'Muons/MuonRecoOneHLT/GlbMuon_Glb_eta',
        'Egamma/Electrons/Ele5_TagAndProbe/ele0_vertexPt_barrel',
        'Egamma/Electrons/Ele5_TagAndProbe/ele1_vertexPt_endcaps',
        'Egamma/Electrons/Ele5_TagAndProbe/ele2_vertexEta',
        'Egamma/Electrons/Ele5_TagAndProbe/ele5_vertexZ',
        'Egamma/Electrons/Ele5_TagAndProbe/ele10_Eop_barrel',
        'Egamma/Electrons/Ele5_TagAndProbe/ele10_Eop_endcaps',
        'Egamma/Electrons/Ele5_TagAndProbe/ele101_etaEff',
        'Egamma/Electrons/Ele5_TagAndProbe/ele102_phiEff',
        'Egamma/Electrons/Ele5_TagAndProbe/ele201_mee_os'
     ) ),
    assertLegacySafe = cms.untracked.bool(False),
    enableMultiThread = cms.untracked.bool(True),
    onlineMode = cms.untracked.bool(False),
    saveByLumi = cms.untracked.bool(False),
    trackME = cms.untracked.string(''),
    verbose = cms.untracked.int32(0)
)


process.FastTimerService = cms.Service("FastTimerService",
    dqmLumiSectionsRange = cms.untracked.uint32(2500),
    dqmMemoryRange = cms.untracked.double(1000000.0),
    dqmMemoryResolution = cms.untracked.double(5000.0),
    dqmModuleMemoryRange = cms.untracked.double(100000.0),
    dqmModuleMemoryResolution = cms.untracked.double(500.0),
    dqmModuleTimeRange = cms.untracked.double(40.0),
    dqmModuleTimeResolution = cms.untracked.double(0.2),
    dqmPath = cms.untracked.string('HLT/TimerService'),
    dqmPathMemoryRange = cms.untracked.double(1000000.0),
    dqmPathMemoryResolution = cms.untracked.double(5000.0),
    dqmPathTimeRange = cms.untracked.double(100.0),
    dqmPathTimeResolution = cms.untracked.double(0.5),
    dqmTimeRange = cms.untracked.double(2000.0),
    dqmTimeResolution = cms.untracked.double(5.0),
    enableDQM = cms.untracked.bool(True),
    enableDQMTransitions = cms.untracked.bool(False),
    enableDQMbyLumiSection = cms.untracked.bool(True),
    enableDQMbyModule = cms.untracked.bool(False),
    enableDQMbyPath = cms.untracked.bool(False),
    enableDQMbyProcesses = cms.untracked.bool(True),
    jsonFileName = cms.untracked.string('resources.json'),
    printEventSummary = cms.untracked.bool(False),
    printJobSummary = cms.untracked.bool(True),
    printRunSummary = cms.untracked.bool(True),
    writeJSONSummary = cms.untracked.bool(False)
)


process.MessageLogger = cms.Service("MessageLogger",
    FastReport = cms.untracked.PSet(

    ),
    HLTrigReport = cms.untracked.PSet(

    ),
    L1GtTrigReport = cms.untracked.PSet(

    ),
    L1TGlobalSummary = cms.untracked.PSet(

    ),
    ThroughputService = cms.untracked.PSet(

    ),
    TriggerSummaryProducerAOD = cms.untracked.PSet(

    ),
    cerr = cms.untracked.PSet(
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkReport = cms.untracked.PSet(
            limit = cms.untracked.int32(0),
            reportEvery = cms.untracked.int32(1)
        ),
        FwkSummary = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000),
            reportEvery = cms.untracked.int32(1)
        ),
        INFO = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        Root_NoDictionary = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        enableStatistics = cms.untracked.bool(False),
        noTimeStamps = cms.untracked.bool(False),
        threshold = cms.untracked.string('INFO')
    ),
    debugModules = cms.untracked.vstring(),
    suppressDebug = cms.untracked.vstring(),
    suppressError = cms.untracked.vstring(
        'hltL3TkTracksFromL2IOHit',
        'hltL3TkTracksFromL2OIHit',
        'hltL3TkTracksFromL2OIState'
    ),
    suppressFwkInfo = cms.untracked.vstring(),
    suppressInfo = cms.untracked.vstring(),
    suppressWarning = cms.untracked.vstring(
        'hltL3MuonsIOHit',
        'hltL3MuonsOIHit',
        'hltL3MuonsOIState',
        'hltLightPFTracks',
        'hltPixelTracks',
        'hltPixelTracksForHighMult',
        'hltSiPixelClusters',
        'hltSiPixelDigis'
    )
)


process.ThroughputService = cms.Service("ThroughputService",
    dqmPath = cms.untracked.string('HLT/Throughput'),
    dqmPathByProcesses = cms.untracked.bool(True),
    enableDQM = cms.untracked.bool(True),
    eventRange = cms.untracked.uint32(10000),
    eventResolution = cms.untracked.uint32(1),
    printEventSummary = cms.untracked.bool(False),
    timeRange = cms.untracked.double(60000.0),
    timeResolution = cms.untracked.double(5.828)
)


process.ProcessAcceleratorAlpaka = ProcessAcceleratorAlpaka()


process.ProcessAcceleratorCUDA = ProcessAcceleratorCUDA()


process.ProcessAcceleratorROCm = ProcessAcceleratorROCm()


process.AnyDirectionAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    ComponentName = cms.string('AnyDirectionAnalyticalPropagator'),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('anyDirection'),
    SimpleMagneticField = cms.string(''),
    appendToDataLabel = cms.string('')
)


process.CSCChannelMapperESProducer = cms.ESProducer("CSCChannelMapperESProducer",
    AlgoName = cms.string('CSCChannelMapperPostls1')
)


process.CSCGeometryESModule = cms.ESProducer("CSCGeometryESModule",
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    debugV = cms.untracked.bool(False),
    fromDD4hep = cms.bool(False),
    fromDDD = cms.bool(False),
    useCentreTIOffsets = cms.bool(False),
    useGangedStripsInME1a = cms.bool(False),
    useOnlyWiresInME1a = cms.bool(False),
    useRealWireGeometry = cms.bool(True)
)


process.CSCIndexerESProducer = cms.ESProducer("CSCIndexerESProducer",
    AlgoName = cms.string('CSCIndexerPostls1')
)


process.CSCObjectMapESProducer = cms.ESProducer("CSCObjectMapESProducer",
    appendToDataLabel = cms.string('')
)


process.CaloGeometryBuilder = cms.ESProducer("CaloGeometryBuilder",
    SelectedCalos = cms.vstring(
        'HCAL',
        'ZDC',
        'EcalBarrel',
        'EcalEndcap',
        'EcalPreshower',
        'TOWER'
    )
)


process.CaloTopologyBuilder = cms.ESProducer("CaloTopologyBuilder")


process.CaloTowerConstituentsMapBuilder = cms.ESProducer("CaloTowerConstituentsMapBuilder",
    MapAuto = cms.untracked.bool(False),
    MapFile = cms.untracked.string('Geometry/CaloTopology/data/CaloTowerEEGeometric.map.gz'),
    SkipHE = cms.untracked.bool(False),
    appendToDataLabel = cms.string('')
)


process.CaloTowerGeometryFromDBEP = cms.ESProducer("CaloTowerGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.CaloTowerTopologyEP = cms.ESProducer("CaloTowerTopologyEP",
    appendToDataLabel = cms.string('')
)


process.CastorDbProducer = cms.ESProducer("CastorDbProducer",
    appendToDataLabel = cms.string(''),
    dump = cms.untracked.vstring()
)


process.ClusterShapeHitFilterESProducer = cms.ESProducer("ClusterShapeHitFilterESProducer",
    ComponentName = cms.string('ClusterShapeHitFilter'),
    PixelShapeFile = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_noL1.par'),
    PixelShapeFileL1 = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_loose.par'),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
    ),
    doPixelShapeCut = cms.bool(True),
    doStripShapeCut = cms.bool(True),
    isPhase2 = cms.bool(False)
)


process.DTGeometryESModule = cms.ESProducer("DTGeometryESModule",
    DDDetector = cms.ESInputTag("",""),
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    attribute = cms.string('MuStructure'),
    fromDD4hep = cms.bool(False),
    fromDDD = cms.bool(False),
    value = cms.string('MuonBarrelDT')
)


process.DTObjectMapESProducer = cms.ESProducer("DTObjectMapESProducer",
    appendToDataLabel = cms.string('')
)


process.EcalBarrelGeometryFromDBEP = cms.ESProducer("EcalBarrelGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalElectronicsMappingBuilder = cms.ESProducer("EcalElectronicsMappingBuilder")


process.EcalEndcapGeometryFromDBEP = cms.ESProducer("EcalEndcapGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.EcalLaserCorrectionService = cms.ESProducer("EcalLaserCorrectionService",
    appendToDataLabel = cms.string(''),
    maxExtrapolationTimeInSec = cms.uint32(0)
)


process.EcalPreshowerGeometryFromDBEP = cms.ESProducer("EcalPreshowerGeometryFromDBEP",
    applyAlignment = cms.bool(True)
)


process.GEMGeometryESModule = cms.ESProducer("GEMGeometryESModule",
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(False),
    fromDD4hep = cms.bool(False),
    fromDDD = cms.bool(False)
)


process.GlobalParameters = cms.ESProducer("StableParametersTrivialProducer",
    IfCaloEtaNumberBits = cms.uint32(4),
    IfMuEtaNumberBits = cms.uint32(6),
    NumberChips = cms.uint32(1),
    NumberConditionChips = cms.uint32(1),
    NumberL1CenJet = cms.uint32(4),
    NumberL1EGamma = cms.uint32(12),
    NumberL1ForJet = cms.uint32(4),
    NumberL1IsoEG = cms.uint32(4),
    NumberL1Jet = cms.uint32(12),
    NumberL1JetCounts = cms.uint32(12),
    NumberL1Mu = cms.uint32(4),
    NumberL1Muon = cms.uint32(8),
    NumberL1NoIsoEG = cms.uint32(4),
    NumberL1Tau = cms.uint32(12),
    NumberL1TauJet = cms.uint32(4),
    NumberPhysTriggers = cms.uint32(512),
    NumberPhysTriggersExtended = cms.uint32(64),
    NumberPsbBoards = cms.int32(7),
    NumberTechnicalTriggers = cms.uint32(64),
    OrderConditionChip = cms.vint32(1),
    OrderOfChip = cms.vint32(1),
    PinsOnChip = cms.uint32(512),
    PinsOnConditionChip = cms.uint32(512),
    TotalBxInEvent = cms.int32(5),
    UnitLength = cms.int32(8),
    WordLength = cms.int32(64),
    appendToDataLabel = cms.string('')
)


process.HcalGeometryFromDBEP = cms.ESProducer("HcalGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.HcalTopologyIdealEP = cms.ESProducer("HcalTopologyIdealEP",
    Exclude = cms.untracked.string(''),
    MergePosition = cms.untracked.bool(True),
    appendToDataLabel = cms.string('')
)


process.L1DTConfigFromDB = cms.ESProducer("DTConfigDBProducer",
    DTTPGMap = cms.untracked.PSet(
    **dict(
        [
            ("wh0st1se1" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se10" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se11" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se12" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se2" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se3" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se4" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se5" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se6" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se7" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se8" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st1se9" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh0st2se1" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se10" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se11" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se12" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se2" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se3" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se4" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se5" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se6" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se7" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se8" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st2se9" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh0st3se1" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se10" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se11" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se12" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se2" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se3" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se4" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se5" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se6" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se7" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se8" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st3se9" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh0st4se1" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh0st4se10" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("wh0st4se11" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("wh0st4se12" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("wh0st4se13" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("wh0st4se14" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("wh0st4se2" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh0st4se3" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh0st4se4" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("wh0st4se5" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh0st4se6" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh0st4se7" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh0st4se8" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("wh0st4se9" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("wh1st1se1" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se10" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se11" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se12" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se2" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se3" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se4" , cms.untracked.vint32(50, 48, 50, 13) ),
            ("wh1st1se5" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se6" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se7" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se8" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st1se9" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh1st2se1" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se10" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se11" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se12" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se2" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se3" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se4" , cms.untracked.vint32(60, 48, 60, 15) ),
            ("wh1st2se5" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se6" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se7" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se8" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st2se9" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh1st3se1" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se10" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se11" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se12" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se2" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se3" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se4" , cms.untracked.vint32(72, 48, 72, 18) ),
            ("wh1st3se5" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se6" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se7" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se8" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st3se9" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh1st4se1" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh1st4se10" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("wh1st4se11" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("wh1st4se12" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("wh1st4se13" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("wh1st4se14" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("wh1st4se2" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh1st4se3" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh1st4se4" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("wh1st4se5" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh1st4se6" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh1st4se7" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh1st4se8" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("wh1st4se9" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("wh2st1se1" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se10" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se11" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se12" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se2" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se3" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se4" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se5" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se6" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se7" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se8" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st1se9" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("wh2st2se1" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se10" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se11" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se12" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se2" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se3" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se4" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se5" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se6" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se7" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se8" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st2se9" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("wh2st3se1" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se10" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se11" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se12" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se2" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se3" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se4" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se5" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se6" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se7" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se8" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st3se9" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("wh2st4se1" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh2st4se10" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("wh2st4se11" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("wh2st4se12" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("wh2st4se13" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("wh2st4se14" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("wh2st4se2" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh2st4se3" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh2st4se4" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("wh2st4se5" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh2st4se6" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh2st4se7" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("wh2st4se8" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("wh2st4se9" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("whm1st1se1" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se10" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se11" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se12" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se2" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se3" , cms.untracked.vint32(50, 48, 50, 13) ),
            ("whm1st1se4" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se5" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se6" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se7" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se8" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st1se9" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm1st2se1" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se10" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se11" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se12" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se2" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se3" , cms.untracked.vint32(60, 48, 60, 15) ),
            ("whm1st2se4" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se5" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se6" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se7" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se8" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st2se9" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm1st3se1" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se10" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se11" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se12" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se2" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se3" , cms.untracked.vint32(72, 48, 72, 18) ),
            ("whm1st3se4" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se5" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se6" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se7" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se8" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st3se9" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm1st4se1" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm1st4se10" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("whm1st4se11" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("whm1st4se12" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("whm1st4se13" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("whm1st4se14" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("whm1st4se2" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm1st4se3" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm1st4se4" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("whm1st4se5" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm1st4se6" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm1st4se7" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm1st4se8" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("whm1st4se9" , cms.untracked.vint32(48, 0, 48, 12) ),
        ] +
        [
            ("whm2st1se1" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se10" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se11" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se12" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se2" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se3" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se4" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se5" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se6" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se7" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se8" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st1se9" , cms.untracked.vint32(50, 58, 50, 13) ),
            ("whm2st2se1" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se10" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se11" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se12" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se2" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se3" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se4" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se5" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se6" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se7" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se8" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st2se9" , cms.untracked.vint32(60, 58, 60, 15) ),
            ("whm2st3se1" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se10" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se11" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se12" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se2" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se3" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se4" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se5" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se6" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se7" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se8" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st3se9" , cms.untracked.vint32(72, 58, 72, 18) ),
            ("whm2st4se1" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm2st4se10" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("whm2st4se11" , cms.untracked.vint32(48, 0, 48, 12) ),
            ("whm2st4se12" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("whm2st4se13" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("whm2st4se14" , cms.untracked.vint32(60, 0, 60, 15) ),
            ("whm2st4se2" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm2st4se3" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm2st4se4" , cms.untracked.vint32(72, 0, 72, 18) ),
            ("whm2st4se5" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm2st4se6" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm2st4se7" , cms.untracked.vint32(96, 0, 96, 24) ),
            ("whm2st4se8" , cms.untracked.vint32(92, 0, 92, 23) ),
            ("whm2st4se9" , cms.untracked.vint32(48, 0, 48, 12) ),
            ]
        )
    ),
    DTTPGParameters = cms.PSet(
        Debug = cms.untracked.bool(False),
        SectCollParameters = cms.PSet(
            Debug = cms.untracked.bool(False),
            SCCSP1 = cms.int32(0),
            SCCSP2 = cms.int32(0),
            SCCSP3 = cms.int32(0),
            SCCSP4 = cms.int32(0),
            SCCSP5 = cms.int32(0),
            SCECF1 = cms.bool(False),
            SCECF2 = cms.bool(False),
            SCECF3 = cms.bool(False),
            SCECF4 = cms.bool(False)
        ),
        TUParameters = cms.PSet(
            BtiParameters = cms.PSet(
                AC1 = cms.int32(0),
                AC2 = cms.int32(3),
                ACH = cms.int32(1),
                ACL = cms.int32(2),
                CH = cms.int32(41),
                CL = cms.int32(22),
                DEAD = cms.int32(31),
                Debug = cms.untracked.int32(0),
                KACCTHETA = cms.int32(1),
                KMAX = cms.int32(64),
                LH = cms.int32(21),
                LL = cms.int32(2),
                LTS = cms.int32(3),
                PTMS0 = cms.int32(0),
                PTMS1 = cms.int32(0),
                PTMS10 = cms.int32(1),
                PTMS11 = cms.int32(1),
                PTMS12 = cms.int32(1),
                PTMS13 = cms.int32(1),
                PTMS14 = cms.int32(1),
                PTMS15 = cms.int32(1),
                PTMS16 = cms.int32(1),
                PTMS17 = cms.int32(1),
                PTMS18 = cms.int32(1),
                PTMS19 = cms.int32(1),
                PTMS2 = cms.int32(0),
                PTMS20 = cms.int32(1),
                PTMS21 = cms.int32(1),
                PTMS22 = cms.int32(1),
                PTMS23 = cms.int32(1),
                PTMS24 = cms.int32(1),
                PTMS25 = cms.int32(1),
                PTMS26 = cms.int32(1),
                PTMS27 = cms.int32(1),
                PTMS28 = cms.int32(1),
                PTMS29 = cms.int32(1),
                PTMS3 = cms.int32(0),
                PTMS30 = cms.int32(0),
                PTMS31 = cms.int32(0),
                PTMS4 = cms.int32(1),
                PTMS5 = cms.int32(1),
                PTMS6 = cms.int32(1),
                PTMS7 = cms.int32(1),
                PTMS8 = cms.int32(1),
                PTMS9 = cms.int32(1),
                RE43 = cms.int32(2),
                RH = cms.int32(61),
                RL = cms.int32(42),
                RON = cms.bool(True),
                SET = cms.int32(7),
                ST43 = cms.int32(42),
                WEN0 = cms.int32(1),
                WEN1 = cms.int32(1),
                WEN2 = cms.int32(1),
                WEN3 = cms.int32(1),
                WEN4 = cms.int32(1),
                WEN5 = cms.int32(1),
                WEN6 = cms.int32(1),
                WEN7 = cms.int32(1),
                WEN8 = cms.int32(1),
                XON = cms.bool(False)
            ),
            Debug = cms.untracked.bool(False),
            LutParameters = cms.PSet(
                BTIC = cms.untracked.int32(0),
                D = cms.untracked.double(0),
                Debug = cms.untracked.bool(False),
                WHEEL = cms.untracked.int32(-1),
                XCN = cms.untracked.double(0)
            ),
            TSPhiParameters = cms.PSet(
                Debug = cms.untracked.bool(False),
                TSMCCE1 = cms.bool(True),
                TSMCCE2 = cms.bool(False),
                TSMCCEC = cms.bool(False),
                TSMCGS1 = cms.bool(True),
                TSMCGS2 = cms.bool(True),
                TSMGS1 = cms.int32(1),
                TSMGS2 = cms.int32(1),
                TSMHSP = cms.int32(1),
                TSMHTE1 = cms.bool(True),
                TSMHTE2 = cms.bool(False),
                TSMHTEC = cms.bool(False),
                TSMMSK1 = cms.int32(312),
                TSMMSK2 = cms.int32(312),
                TSMNOE1 = cms.bool(True),
                TSMNOE2 = cms.bool(False),
                TSMNOEC = cms.bool(False),
                TSMWORD = cms.int32(255),
                TSSCCE1 = cms.bool(True),
                TSSCCE2 = cms.bool(False),
                TSSCCEC = cms.bool(False),
                TSSCGS1 = cms.bool(True),
                TSSCGS2 = cms.bool(True),
                TSSGS1 = cms.int32(1),
                TSSGS2 = cms.int32(1),
                TSSHTE1 = cms.bool(True),
                TSSHTE2 = cms.bool(False),
                TSSHTEC = cms.bool(False),
                TSSMSK1 = cms.int32(312),
                TSSMSK2 = cms.int32(312),
                TSSNOE1 = cms.bool(True),
                TSSNOE2 = cms.bool(False),
                TSSNOEC = cms.bool(False),
                TSTREN0 = cms.bool(True),
                TSTREN1 = cms.bool(True),
                TSTREN10 = cms.bool(True),
                TSTREN11 = cms.bool(True),
                TSTREN12 = cms.bool(True),
                TSTREN13 = cms.bool(True),
                TSTREN14 = cms.bool(True),
                TSTREN15 = cms.bool(True),
                TSTREN16 = cms.bool(True),
                TSTREN17 = cms.bool(True),
                TSTREN18 = cms.bool(True),
                TSTREN19 = cms.bool(True),
                TSTREN2 = cms.bool(True),
                TSTREN20 = cms.bool(True),
                TSTREN21 = cms.bool(True),
                TSTREN22 = cms.bool(True),
                TSTREN23 = cms.bool(True),
                TSTREN3 = cms.bool(True),
                TSTREN4 = cms.bool(True),
                TSTREN5 = cms.bool(True),
                TSTREN6 = cms.bool(True),
                TSTREN7 = cms.bool(True),
                TSTREN8 = cms.bool(True),
                TSTREN9 = cms.bool(True)
            ),
            TSThetaParameters = cms.PSet(
                Debug = cms.untracked.bool(False)
            ),
            TracoParameters = cms.PSet(
                BTIC = cms.int32(32),
                DD = cms.int32(18),
                Debug = cms.untracked.int32(0),
                FHISM = cms.int32(0),
                FHTMSK = cms.int32(0),
                FHTPRF = cms.int32(1),
                FLTMSK = cms.int32(1),
                FPRGCOMP = cms.int32(2),
                FSLMSK = cms.int32(0),
                IBTIOFF = cms.int32(0),
                KPRGCOM = cms.int32(255),
                KRAD = cms.int32(0),
                LTF = cms.int32(0),
                LTS = cms.int32(0),
                LVALIDIFH = cms.int32(0),
                REUSEI = cms.int32(1),
                REUSEO = cms.int32(1),
                SHISM = cms.int32(0),
                SHTMSK = cms.int32(0),
                SHTPRF = cms.int32(1),
                SLTMSK = cms.int32(1),
                SPRGCOMP = cms.int32(2),
                SSLMSK = cms.int32(0),
                TRGENB0 = cms.int32(1),
                TRGENB1 = cms.int32(1),
                TRGENB10 = cms.int32(1),
                TRGENB11 = cms.int32(1),
                TRGENB12 = cms.int32(1),
                TRGENB13 = cms.int32(1),
                TRGENB14 = cms.int32(1),
                TRGENB15 = cms.int32(1),
                TRGENB2 = cms.int32(1),
                TRGENB3 = cms.int32(1),
                TRGENB4 = cms.int32(1),
                TRGENB5 = cms.int32(1),
                TRGENB6 = cms.int32(1),
                TRGENB7 = cms.int32(1),
                TRGENB8 = cms.int32(1),
                TRGENB9 = cms.int32(1)
            )
        )
    ),
    TracoLutsFromDB = cms.bool(True),
    UseBtiAcceptParam = cms.bool(True),
    UseT0 = cms.bool(False),
    bxOffset = cms.int32(19),
    cfgConfig = cms.bool(False),
    debug = cms.bool(False),
    debugBti = cms.int32(0),
    debugDB = cms.bool(False),
    debugLUTs = cms.bool(False),
    debugPed = cms.bool(False),
    debugSC = cms.bool(False),
    debugTSP = cms.bool(False),
    debugTST = cms.bool(False),
    debugTU = cms.bool(False),
    debugTraco = cms.int32(0),
    finePhase = cms.double(25.0)
)


process.MaterialPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterial'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.MaterialPropagatorForHI = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialForHI'),
    Mass = cms.double(0.139),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.MaterialPropagatorParabolicMF = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialParabolicMf'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.OppositeMaterialPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialOpposite'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.OppositeMaterialPropagatorForHI = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialOppositeForHI'),
    Mass = cms.double(0.139),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.OppositeMaterialPropagatorParabolicMF = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.OppositePropagatorWithMaterialForMixedStep = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialForMixedStepOpposite'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(0.1),
    useRungeKutta = cms.bool(False)
)


process.ParametrizedMagneticFieldProducer = cms.ESProducer("AutoParametrizedMagneticFieldProducer",
    label = cms.untracked.string('ParabolicMf'),
    valueOverride = cms.int32(-1),
    version = cms.string('Parabolic')
)


process.PropagatorWithMaterialForLoopers = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialForLoopers'),
    Mass = cms.double(0.1396),
    MaxDPhi = cms.double(4.0),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.PropagatorWithMaterialForMixedStep = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('PropagatorWithMaterialForMixedStep'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string('ParabolicMf'),
    ptMin = cms.double(0.1),
    useRungeKutta = cms.bool(False)
)


process.RPCConeBuilder = cms.ESProducer("RPCConeBuilder",
    towerBeg = cms.int32(0),
    towerEnd = cms.int32(16)
)


process.RPCGeometryESModule = cms.ESProducer("RPCGeometryESModule",
    appendToDataLabel = cms.string(''),
    fromDD4hep = cms.untracked.bool(False),
    fromDDD = cms.untracked.bool(False)
)


process.SiPixelTemplateStoreESProducer = cms.ESProducer("SiPixelTemplateStoreESProducer",
    appendToDataLabel = cms.string('')
)


process.SiStripClusterizerConditionsESProducer = cms.ESProducer("SiStripClusterizerConditionsESProducer",
    Label = cms.string(''),
    QualityLabel = cms.string(''),
    appendToDataLabel = cms.string('')
)


process.SiStripGainESProducer = cms.ESProducer("SiStripGainESProducer",
    APVGain = cms.VPSet(
        cms.PSet(
            Label = cms.untracked.string(''),
            NormalizationFactor = cms.untracked.double(1.0),
            Record = cms.string('SiStripApvGainRcd')
        ),
        cms.PSet(
            Label = cms.untracked.string(''),
            NormalizationFactor = cms.untracked.double(1.0),
            Record = cms.string('SiStripApvGain2Rcd')
        )
    ),
    AutomaticNormalization = cms.bool(False),
    appendToDataLabel = cms.string(''),
    printDebug = cms.untracked.bool(False)
)


process.SiStripQualityESProducer = cms.ESProducer("SiStripQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(
        cms.PSet(
            record = cms.string('SiStripDetVOffRcd'),
            tag = cms.string('')
        ),
        cms.PSet(
            record = cms.string('SiStripDetCablingRcd'),
            tag = cms.string('')
        ),
        cms.PSet(
            record = cms.string('SiStripBadChannelRcd'),
            tag = cms.string('')
        ),
        cms.PSet(
            record = cms.string('SiStripBadFiberRcd'),
            tag = cms.string('')
        ),
        cms.PSet(
            record = cms.string('SiStripBadModuleRcd'),
            tag = cms.string('')
        )
    ),
    PrintDebugOutput = cms.bool(False),
    ReduceGranularity = cms.bool(False),
    ThresholdForReducedGranularity = cms.double(0.3),
    UseEmptyRunInfo = cms.bool(False),
    appendToDataLabel = cms.string('')
)


process.SiStripRecHitMatcherESProducer = cms.ESProducer("SiStripRecHitMatcherESProducer",
    ComponentName = cms.string('StandardMatcher'),
    NSigmaInside = cms.double(3.0),
    PreFilter = cms.bool(False)
)


process.SiStripRegionConnectivity = cms.ESProducer("SiStripRegionConnectivity",
    EtaDivisions = cms.untracked.uint32(20),
    EtaMax = cms.untracked.double(2.5),
    PhiDivisions = cms.untracked.uint32(20),
    appendToDataLabel = cms.string('')
)


process.SimpleSecondaryVertex3TrkComputer = cms.ESProducer("SimpleSecondaryVertexESProducer",
    appendToDataLabel = cms.string(''),
    minTracks = cms.uint32(3),
    minVertices = cms.uint32(1),
    unBoost = cms.bool(False),
    use3d = cms.bool(True),
    useSignificance = cms.bool(True)
)


process.SteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('SteppingHelixPropagatorAny'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    appendToDataLabel = cms.string(''),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False)
)


process.TrackerAdditionalParametersPerDetESModule = cms.ESProducer("TrackerAdditionalParametersPerDetESModule",
    appendToDataLabel = cms.string('')
)


process.TrackerDigiGeometryESModule = cms.ESProducer("TrackerDigiGeometryESModule",
    alignmentsLabel = cms.string(''),
    appendToDataLabel = cms.string(''),
    applyAlignment = cms.bool(True),
    fromDDD = cms.bool(False)
)


process.TrackerGeometricDetESModule = cms.ESProducer("TrackerGeometricDetESModule",
    appendToDataLabel = cms.string(''),
    fromDD4hep = cms.bool(False),
    fromDDD = cms.bool(False)
)


process.TransientTrackBuilderESProducer = cms.ESProducer("TransientTrackBuilderESProducer",
    ComponentName = cms.string('TransientTrackBuilder'),
    appendToDataLabel = cms.string('')
)


process.VolumeBasedMagneticFieldESProducer = cms.ESProducer("VolumeBasedMagneticFieldESProducerFromDB",
    debugBuilder = cms.untracked.bool(False),
    label = cms.untracked.string(''),
    valueOverride = cms.int32(-1)
)


process.ZdcGeometryFromDBEP = cms.ESProducer("ZdcGeometryFromDBEP",
    applyAlignment = cms.bool(False)
)


process.caloConfig = cms.ESProducer("L1TCaloConfigESProducer",
    fwVersionLayer2 = cms.uint32(3),
    l1Epoch = cms.string('Stage1')
)


process.caloDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('CaloDetIdAssociator'),
    etaBinSize = cms.double(0.087),
    hcalRegion = cms.int32(2),
    includeBadChambers = cms.bool(False),
    includeGEM = cms.bool(False),
    includeME0 = cms.bool(False),
    nEta = cms.int32(70),
    nPhi = cms.int32(72)
)


process.cosmicsNavigationSchoolESProducer = cms.ESProducer("NavigationSchoolESProducer",
    ComponentName = cms.string('CosmicNavigationSchool'),
    PluginName = cms.string(''),
    SimpleMagneticField = cms.string(''),
    appendToDataLabel = cms.string('')
)


process.ctppsGeometryESModule = cms.ESProducer("CTPPSGeometryESModule",
    appendToDataLabel = cms.string(''),
    buildMisalignedGeometry = cms.bool(False),
    compactViewTag = cms.string(''),
    dbTag = cms.string(''),
    fromDD4hep = cms.untracked.bool(False),
    fromPreprocessedDB = cms.untracked.bool(True),
    isRun2 = cms.bool(False),
    verbosity = cms.untracked.uint32(1)
)


process.ctppsInterpolatedOpticalFunctionsESSource = cms.ESProducer("CTPPSInterpolatedOpticalFunctionsESSource",
    appendToDataLabel = cms.string(''),
    lhcInfoLabel = cms.string(''),
    lhcInfoPerFillLabel = cms.string(''),
    lhcInfoPerLSLabel = cms.string(''),
    opticsLabel = cms.string(''),
    useNewLHCInfo = cms.bool(True)
)


process.ecalDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('EcalDetIdAssociator'),
    etaBinSize = cms.double(0.02),
    hcalRegion = cms.int32(2),
    includeBadChambers = cms.bool(False),
    includeGEM = cms.bool(False),
    includeME0 = cms.bool(False),
    nEta = cms.int32(300),
    nPhi = cms.int32(360)
)


process.ecalElectronicsMappingHostESProducer = cms.ESProducer("EcalElectronicsMappingHostESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.ecalMultifitConditionsHostESProducer = cms.ESProducer("EcalMultifitConditionsHostESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.ecalSeverityLevel = cms.ESProducer("EcalSeverityLevelESProducer",
    dbstatusMask = cms.PSet(
        kBad = cms.vstring(
            'kNonRespondingIsolated',
            'kDeadVFE',
            'kDeadFE',
            'kNoDataNoTP'
        ),
        kGood = cms.vstring('kOk'),
        kProblematic = cms.vstring(
            'kDAC',
            'kNoLaser',
            'kNoisy',
            'kNNoisy',
            'kNNNoisy',
            'kNNNNoisy',
            'kNNNNNoisy',
            'kFixedG6',
            'kFixedG1',
            'kFixedG0'
        ),
        kRecovered = cms.vstring(),
        kTime = cms.vstring(),
        kWeird = cms.vstring()
    ),
    flagMask = cms.PSet(
        kBad = cms.vstring(
            'kFaultyHardware',
            'kDead',
            'kKilled'
        ),
        kGood = cms.vstring('kGood'),
        kProblematic = cms.vstring(
            'kPoorReco',
            'kPoorCalib',
            'kNoisy',
            'kSaturated'
        ),
        kRecovered = cms.vstring(
            'kLeadingEdgeRecovered',
            'kTowerRecovered'
        ),
        kTime = cms.vstring('kOutOfTime'),
        kWeird = cms.vstring(
            'kWeird',
            'kDiWeird'
        )
    ),
    timeThresh = cms.double(2.0)
)


process.fakeTwinMuxParams = cms.ESProducer("L1TTwinMuxParamsESProducer",
    CorrectDTBxwRPC = cms.bool(True),
    dphiWindowBxShift = cms.uint32(9999),
    fwVersion = cms.uint32(1),
    useLowQDT = cms.bool(False),
    useOnlyDT = cms.bool(False),
    useOnlyRPC = cms.bool(False),
    useRpcBxForDtBelowQuality = cms.uint32(4),
    verbose = cms.bool(False)
)


process.hcalChannelPropertiesESProd = cms.ESProducer("HcalChannelPropertiesEP")


process.hcalDDDRecConstants = cms.ESProducer("HcalDDDRecConstantsESModule",
    appendToDataLabel = cms.string('')
)


process.hcalDDDSimConstants = cms.ESProducer("HcalDDDSimConstantsESModule",
    appendToDataLabel = cms.string('')
)


process.hcalDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('HcalDetIdAssociator'),
    etaBinSize = cms.double(0.087),
    hcalRegion = cms.int32(2),
    includeBadChambers = cms.bool(False),
    includeGEM = cms.bool(False),
    includeME0 = cms.bool(False),
    nEta = cms.int32(70),
    nPhi = cms.int32(72)
)


process.hcalMahiConditionsESProducer = cms.ESProducer("HcalMahiConditionsESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.hcalRecAlgos = cms.ESProducer("HcalRecAlgoESProducer",
    DropChannelStatusBits = cms.vstring(
        'HcalCellMask',
        'HcalCellOff',
        'HcalCellDead'
    ),
    RecoveredRecHitBits = cms.vstring(''),
    SeverityLevels = cms.VPSet(
        cms.PSet(
            ChannelStatus = cms.vstring(''),
            Level = cms.int32(0),
            RecHitFlags = cms.vstring('')
        ),
        cms.PSet(
            ChannelStatus = cms.vstring('HcalCellCaloTowerProb'),
            Level = cms.int32(1),
            RecHitFlags = cms.vstring('')
        ),
        cms.PSet(
            ChannelStatus = cms.vstring('HcalCellExcludeFromHBHENoiseSummary'),
            Level = cms.int32(5),
            RecHitFlags = cms.vstring(
                'HBHEIsolatedNoise',
                'HFAnomalousHit'
            )
        ),
        cms.PSet(
            ChannelStatus = cms.vstring(''),
            Level = cms.int32(8),
            RecHitFlags = cms.vstring(
                'HBHEHpdHitMultiplicity',
                'HBHESpikeNoise',
                'HBHETS4TS5Noise',
                'HBHEOOTPU',
                'HBHEFlatNoise',
                'HBHENegativeNoise'
            )
        ),
        cms.PSet(
            ChannelStatus = cms.vstring(''),
            Level = cms.int32(11),
            RecHitFlags = cms.vstring(
                'HFLongShort',
                'HFS8S1Ratio',
                'HFPET',
                'HFSignalAsymmetry'
            )
        ),
        cms.PSet(
            ChannelStatus = cms.vstring('HcalCellCaloTowerMask'),
            Level = cms.int32(12),
            RecHitFlags = cms.vstring()
        ),
        cms.PSet(
            ChannelStatus = cms.vstring('HcalCellHot'),
            Level = cms.int32(15),
            RecHitFlags = cms.vstring('')
        ),
        cms.PSet(
            ChannelStatus = cms.vstring(
                'HcalCellOff',
                'HcalCellDead'
            ),
            Level = cms.int32(20),
            RecHitFlags = cms.vstring('')
        )
    ),
    appendToDataLabel = cms.string(''),
    phase = cms.uint32(1)
)


process.hcalRecoParamWithPulseShapeESProducer = cms.ESProducer("HcalRecoParamWithPulseShapeESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.hcalSiPMCharacteristicsESProducer = cms.ESProducer("HcalSiPMCharacteristicsESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.hcal_db_producer = cms.ESProducer("HcalDbProducer")


process.hltBoostedDoubleSecondaryVertexAK8Computer = cms.ESProducer("CandidateBoostedDoubleSecondaryVertexESProducer",
    appendToDataLabel = cms.string(''),
    gbrForestLabel = cms.string(''),
    useAdaBoost = cms.bool(False),
    useCondDB = cms.bool(False),
    useGBRForest = cms.bool(True),
    weightFile = cms.FileInPath('RecoBTag/SecondaryVertex/data/BoostedDoubleSV_AK8_BDT_v4.weights.xml.gz')
)


process.hltCombinedSecondaryVertex = cms.ESProducer("CombinedSecondaryVertexESProducer",
    SoftLeptonFlip = cms.bool(False),
    appendToDataLabel = cms.string(''),
    calibrationRecord = cms.string(''),
    calibrationRecords = cms.vstring(
        'CombinedSVRecoVertex',
        'CombinedSVPseudoVertex',
        'CombinedSVNoVertex'
    ),
    categoryVariableName = cms.string('vertexCategory'),
    charmCut = cms.double(1.5),
    correctVertexMass = cms.bool(True),
    minimumTrackWeight = cms.double(0.5),
    pseudoMultiplicityMin = cms.uint32(2),
    pseudoVertexV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.05)
    ),
    recordLabel = cms.string('HLT'),
    trackFlip = cms.bool(False),
    trackMultiplicityMin = cms.uint32(3),
    trackPairV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.03)
    ),
    trackPseudoSelection = cms.PSet(
        jetDeltaRMax = cms.double(0.3),
        maxDecayLen = cms.double(5.0),
        maxDistToAxis = cms.double(0.07),
        normChi2Max = cms.double(99999.9),
        pixelHitsMin = cms.uint32(0),
        ptMin = cms.double(0.0),
        qualityClass = cms.string('any'),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(2.0),
        sip2dValMax = cms.double(99999.9),
        sip2dValMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        sip3dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        totalHitsMin = cms.uint32(0)
    ),
    trackSelection = cms.PSet(
        jetDeltaRMax = cms.double(0.3),
        maxDecayLen = cms.double(5.0),
        maxDistToAxis = cms.double(0.07),
        normChi2Max = cms.double(99999.9),
        pixelHitsMin = cms.uint32(0),
        ptMin = cms.double(0.0),
        qualityClass = cms.string('any'),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip2dValMax = cms.double(99999.9),
        sip2dValMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        sip3dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        totalHitsMin = cms.uint32(0)
    ),
    trackSort = cms.string('sip2dSig'),
    useCategories = cms.bool(True),
    useTrackWeights = cms.bool(True),
    vertexFlip = cms.bool(False)
)


process.hltCombinedSecondaryVertexV2 = cms.ESProducer("CombinedSecondaryVertexESProducer",
    SoftLeptonFlip = cms.bool(False),
    appendToDataLabel = cms.string(''),
    calibrationRecord = cms.string(''),
    calibrationRecords = cms.vstring(
        'CombinedSVIVFV2RecoVertex',
        'CombinedSVIVFV2PseudoVertex',
        'CombinedSVIVFV2NoVertex'
    ),
    categoryVariableName = cms.string('vertexCategory'),
    charmCut = cms.double(1.5),
    correctVertexMass = cms.bool(True),
    minimumTrackWeight = cms.double(0.5),
    pseudoMultiplicityMin = cms.uint32(2),
    pseudoVertexV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.05)
    ),
    recordLabel = cms.string('HLT'),
    trackFlip = cms.bool(False),
    trackMultiplicityMin = cms.uint32(3),
    trackPairV0Filter = cms.PSet(
        k0sMassWindow = cms.double(0.03)
    ),
    trackPseudoSelection = cms.PSet(
        a_dR = cms.double(-0.001053),
        a_pT = cms.double(0.005263),
        b_dR = cms.double(0.6263),
        b_pT = cms.double(0.3684),
        jetDeltaRMax = cms.double(0.3),
        maxDecayLen = cms.double(5.0),
        maxDistToAxis = cms.double(0.07),
        max_pT = cms.double(500.0),
        max_pT_dRcut = cms.double(0.1),
        max_pT_trackPTcut = cms.double(3.0),
        min_pT = cms.double(120.0),
        min_pT_dRcut = cms.double(0.5),
        normChi2Max = cms.double(99999.9),
        pixelHitsMin = cms.uint32(0),
        ptMin = cms.double(0.0),
        qualityClass = cms.string('any'),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(2.0),
        sip2dValMax = cms.double(99999.9),
        sip2dValMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        sip3dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        totalHitsMin = cms.uint32(0),
        useVariableJTA = cms.bool(False)
    ),
    trackSelection = cms.PSet(
        a_dR = cms.double(-0.001053),
        a_pT = cms.double(0.005263),
        b_dR = cms.double(0.6263),
        b_pT = cms.double(0.3684),
        jetDeltaRMax = cms.double(0.3),
        maxDecayLen = cms.double(5.0),
        maxDistToAxis = cms.double(0.07),
        max_pT = cms.double(500.0),
        max_pT_dRcut = cms.double(0.1),
        max_pT_trackPTcut = cms.double(3.0),
        min_pT = cms.double(120.0),
        min_pT_dRcut = cms.double(0.5),
        normChi2Max = cms.double(99999.9),
        pixelHitsMin = cms.uint32(0),
        ptMin = cms.double(0.0),
        qualityClass = cms.string('any'),
        sip2dSigMax = cms.double(99999.9),
        sip2dSigMin = cms.double(-99999.9),
        sip2dValMax = cms.double(99999.9),
        sip2dValMin = cms.double(-99999.9),
        sip3dSigMax = cms.double(99999.9),
        sip3dSigMin = cms.double(-99999.9),
        sip3dValMax = cms.double(99999.9),
        sip3dValMin = cms.double(-99999.9),
        totalHitsMin = cms.uint32(0),
        useVariableJTA = cms.bool(False)
    ),
    trackSort = cms.string('sip2dSig'),
    useCategories = cms.bool(True),
    useTrackWeights = cms.bool(True),
    vertexFlip = cms.bool(False)
)


process.hltDisplacedDijethltESPPromptTrackCountingESProducer = cms.ESProducer("PromptTrackCountingESProducer",
    appendToDataLabel = cms.string(''),
    deltaR = cms.double(-1.0),
    deltaRmin = cms.double(0.0),
    impactParameterType = cms.int32(1),
    maxImpactParameter = cms.double(0.1),
    maxImpactParameterSig = cms.double(999999.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(999999.0),
    nthTrack = cms.int32(-1),
    trackQualityClass = cms.string('any')
)


process.hltDisplacedDijethltESPTrackCounting2D1st = cms.ESProducer("TrackCountingESProducer",
    a_dR = cms.double(-0.001053),
    a_pT = cms.double(0.005263),
    appendToDataLabel = cms.string(''),
    b_dR = cms.double(0.6263),
    b_pT = cms.double(0.3684),
    deltaR = cms.double(-1.0),
    impactParameterType = cms.int32(1),
    max_pT = cms.double(500.0),
    max_pT_dRcut = cms.double(0.1),
    max_pT_trackPTcut = cms.double(3.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(9999999.0),
    min_pT = cms.double(120.0),
    min_pT_dRcut = cms.double(0.5),
    minimumImpactParameter = cms.double(0.05),
    nthTrack = cms.int32(1),
    trackQualityClass = cms.string('any'),
    useSignedImpactParameterSig = cms.bool(False),
    useVariableJTA = cms.bool(False)
)


process.hltDoubletRecoveryPFlowTrackCandidatesMkFitConfig = cms.ESProducer("MkFitIterationConfigESProducer",
    ComponentName = cms.string('hltDoubletRecoveryPFlowTrackCandidatesMkFitConfig'),
    appendToDataLabel = cms.string(''),
    config = cms.FileInPath('RecoTracker/MkFit/data/mkfit-phase1-hltdr.json'),
    maxClusterSize = cms.uint32(8),
    minPt = cms.double(0.7)
)


process.hltESChi2MeasurementEstimatorForP5 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESChi2MeasurementEstimatorForP5'),
    MaxChi2 = cms.double(100.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(100000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(4.0)
)


process.hltESFittingSmootherRKP5 = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    ComponentName = cms.string('hltESFittingSmootherRKP5'),
    EstimateCut = cms.double(20.0),
    Fitter = cms.string('hltESPRKTrajectoryFitter'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(0.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(4),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(True),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPRKTrajectorySmoother'),
    appendToDataLabel = cms.string('')
)


process.hltESPAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    ComponentName = cms.string('hltESPAnalyticalPropagator'),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    appendToDataLabel = cms.string('')
)


process.hltESPBwdAnalyticalPropagator = cms.ESProducer("AnalyticalPropagatorESProducer",
    ComponentName = cms.string('hltESPBwdAnalyticalPropagator'),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SimpleMagneticField = cms.string(''),
    appendToDataLabel = cms.string('')
)


process.hltESPBwdElectronPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('hltESPBwdElectronPropagator'),
    Mass = cms.double(0.000511),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.hltESPChi2ChargeLooseMeasurementEstimator16 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeLooseMeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPChi2ChargeMeasurementEstimator16 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPChi2ChargeMeasurementEstimator2000 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator2000'),
    MaxChi2 = cms.double(2000.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPChi2ChargeMeasurementEstimator30 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPChi2ChargeMeasurementEstimator9 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPChi2ChargeMeasurementEstimator9ForHI = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator9ForHI'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutForHI')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPChi2ChargeTightMeasurementEstimator16 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2ChargeTightMeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPChi2MeasurementEstimator100 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2MeasurementEstimator100'),
    MaxChi2 = cms.double(40.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(4.0)
)


process.hltESPChi2MeasurementEstimator16 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2MeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(3.0)
)


process.hltESPChi2MeasurementEstimator30 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2MeasurementEstimator30'),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(3.0)
)


process.hltESPChi2MeasurementEstimator9 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPChi2MeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(3.0)
)


process.hltESPCloseComponentsMerger5D = cms.ESProducer("CloseComponentsMergerESProducer5D",
    ComponentName = cms.string('hltESPCloseComponentsMerger5D'),
    DistanceMeasure = cms.string('hltESPKullbackLeiblerDistance5D'),
    MaxComponents = cms.int32(12),
    appendToDataLabel = cms.string('')
)


process.hltESPDetachedQuadStepChi2ChargeMeasurementEstimator9 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPDetachedQuadStepChi2ChargeMeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPDetachedQuadStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPDetachedQuadStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.13)
)


process.hltESPDetachedStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPDetachedStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.13)
)


process.hltESPDetachedTripletStepChi2ChargeMeasurementEstimator9 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPDetachedTripletStepChi2ChargeMeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPDetachedTripletStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPDetachedTripletStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.13)
)


process.hltESPDisplacedDijethltPromptTrackCountingESProducer = cms.ESProducer("PromptTrackCountingESProducer",
    appendToDataLabel = cms.string(''),
    deltaR = cms.double(-1.0),
    deltaRmin = cms.double(0.0),
    impactParameterType = cms.int32(1),
    maxImpactParameter = cms.double(0.1),
    maxImpactParameterSig = cms.double(999999.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(999999.0),
    nthTrack = cms.int32(-1),
    trackQualityClass = cms.string('any')
)


process.hltESPDisplacedDijethltPromptTrackCountingESProducerLong = cms.ESProducer("PromptTrackCountingESProducer",
    appendToDataLabel = cms.string(''),
    deltaR = cms.double(-1.0),
    deltaRmin = cms.double(0.0),
    impactParameterType = cms.int32(1),
    maxImpactParameter = cms.double(0.2),
    maxImpactParameterSig = cms.double(999999.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(999999.0),
    nthTrack = cms.int32(-1),
    trackQualityClass = cms.string('any')
)


process.hltESPDisplacedDijethltPromptTrackCountingESProducerShortSig5 = cms.ESProducer("PromptTrackCountingESProducer",
    appendToDataLabel = cms.string(''),
    deltaR = cms.double(-1.0),
    deltaRmin = cms.double(0.0),
    impactParameterType = cms.int32(1),
    maxImpactParameter = cms.double(0.05),
    maxImpactParameterSig = cms.double(5.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(999999.0),
    nthTrack = cms.int32(-1),
    trackQualityClass = cms.string('any')
)


process.hltESPDisplacedDijethltTrackCounting2D1st = cms.ESProducer("TrackCountingESProducer",
    a_dR = cms.double(-0.001053),
    a_pT = cms.double(0.005263),
    appendToDataLabel = cms.string(''),
    b_dR = cms.double(0.6263),
    b_pT = cms.double(0.3684),
    deltaR = cms.double(-1.0),
    impactParameterType = cms.int32(1),
    max_pT = cms.double(500.0),
    max_pT_dRcut = cms.double(0.1),
    max_pT_trackPTcut = cms.double(3.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(9999999.0),
    min_pT = cms.double(120.0),
    min_pT_dRcut = cms.double(0.5),
    minimumImpactParameter = cms.double(0.05),
    nthTrack = cms.int32(1),
    trackQualityClass = cms.string('any'),
    useSignedImpactParameterSig = cms.bool(False),
    useVariableJTA = cms.bool(False)
)


process.hltESPDisplacedDijethltTrackCounting2D1stLoose = cms.ESProducer("TrackCountingESProducer",
    a_dR = cms.double(-0.001053),
    a_pT = cms.double(0.005263),
    appendToDataLabel = cms.string(''),
    b_dR = cms.double(0.6263),
    b_pT = cms.double(0.3684),
    deltaR = cms.double(-1.0),
    impactParameterType = cms.int32(1),
    max_pT = cms.double(500.0),
    max_pT_dRcut = cms.double(0.1),
    max_pT_trackPTcut = cms.double(3.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(9999999.0),
    min_pT = cms.double(120.0),
    min_pT_dRcut = cms.double(0.5),
    minimumImpactParameter = cms.double(0.03),
    nthTrack = cms.int32(1),
    trackQualityClass = cms.string('any'),
    useSignedImpactParameterSig = cms.bool(False),
    useVariableJTA = cms.bool(False)
)


process.hltESPDisplacedDijethltTrackCounting2D2ndLong = cms.ESProducer("TrackCountingESProducer",
    a_dR = cms.double(-0.001053),
    a_pT = cms.double(0.005263),
    appendToDataLabel = cms.string(''),
    b_dR = cms.double(0.6263),
    b_pT = cms.double(0.3684),
    deltaR = cms.double(-1.0),
    impactParameterType = cms.int32(1),
    max_pT = cms.double(500.0),
    max_pT_dRcut = cms.double(0.1),
    max_pT_trackPTcut = cms.double(3.0),
    maximumDecayLength = cms.double(999999.0),
    maximumDistanceToJetAxis = cms.double(9999999.0),
    min_pT = cms.double(120.0),
    min_pT_dRcut = cms.double(0.5),
    minimumImpactParameter = cms.double(0.2),
    nthTrack = cms.int32(2),
    trackQualityClass = cms.string('any'),
    useSignedImpactParameterSig = cms.bool(True),
    useVariableJTA = cms.bool(False)
)


process.hltESPDummyDetLayerGeometry = cms.ESProducer("DetLayerGeometryESProducer",
    ComponentName = cms.string('hltESPDummyDetLayerGeometry'),
    appendToDataLabel = cms.string('')
)


process.hltESPEcalTrigTowerConstituentsMapBuilder = cms.ESProducer("EcalTrigTowerConstituentsMapBuilder",
    MapFile = cms.untracked.string('Geometry/EcalMapping/data/EndCap_TTMap.txt')
)


process.hltESPElectronMaterialEffects = cms.ESProducer("GsfMaterialEffectsESProducer",
    BetheHeitlerCorrection = cms.int32(2),
    BetheHeitlerParametrization = cms.string('BetheHeitler_cdfmom_nC6_O5.par'),
    ComponentName = cms.string('hltESPElectronMaterialEffects'),
    EnergyLossUpdator = cms.string('GsfBetheHeitlerUpdator'),
    Mass = cms.double(0.000511),
    MultipleScatteringUpdator = cms.string('MultipleScatteringUpdator')
)


process.hltESPFastSteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('anyDirection'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    appendToDataLabel = cms.string(''),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(True)
)


process.hltESPFastSteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPFastSteppingHelixPropagatorOpposite'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    appendToDataLabel = cms.string(''),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(True)
)


process.hltESPFittingSmootherIT = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(True),
    ComponentName = cms.string('hltESPFittingSmootherIT'),
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('hltESPTrajectoryFitterRK'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(3),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(True),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPTrajectorySmootherRK'),
    appendToDataLabel = cms.string('')
)


process.hltESPFittingSmootherRK = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    ComponentName = cms.string('hltESPFittingSmootherRK'),
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('hltESPTrajectoryFitterRK'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(5),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPTrajectorySmootherRK'),
    appendToDataLabel = cms.string('')
)


process.hltESPFlexibleKFFittingSmoother = cms.ESProducer("FlexibleKFFittingSmootherESProducer",
    ComponentName = cms.string('hltESPFlexibleKFFittingSmoother'),
    appendToDataLabel = cms.string(''),
    looperFitter = cms.string('hltESPKFFittingSmootherForLoopers'),
    standardFitter = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK')
)


process.hltESPFwdElectronPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('hltESPFwdElectronPropagator'),
    Mass = cms.double(0.000511),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(False)
)


process.hltESPGlobalDetLayerGeometry = cms.ESProducer("GlobalDetLayerGeometryESProducer",
    ComponentName = cms.string('hltESPGlobalDetLayerGeometry'),
    appendToDataLabel = cms.string('')
)


process.hltESPGlobalTrackingGeometryESProducer = cms.ESProducer("GlobalTrackingGeometryESProducer")


process.hltESPGsfElectronFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(True),
    ComponentName = cms.string('hltESPGsfElectronFittingSmoother'),
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('hltESPGsfTrajectoryFitter'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(5),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(True),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPGsfTrajectorySmoother'),
    appendToDataLabel = cms.string('')
)


process.hltESPGsfTrajectoryFitter = cms.ESProducer("GsfTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPGsfTrajectoryFitter'),
    GeometricalPropagator = cms.string('hltESPAnalyticalPropagator'),
    MaterialEffectsUpdator = cms.string('hltESPElectronMaterialEffects'),
    Merger = cms.string('hltESPCloseComponentsMerger5D'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    appendToDataLabel = cms.string('')
)


process.hltESPGsfTrajectorySmoother = cms.ESProducer("GsfTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPGsfTrajectorySmoother'),
    ErrorRescaling = cms.double(100.0),
    GeometricalPropagator = cms.string('hltESPBwdAnalyticalPropagator'),
    MaterialEffectsUpdator = cms.string('hltESPElectronMaterialEffects'),
    Merger = cms.string('hltESPCloseComponentsMerger5D'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    appendToDataLabel = cms.string('')
)


process.hltESPHighPtTripletStepChi2ChargeMeasurementEstimator30 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPHighPtTripletStepChi2ChargeMeasurementEstimator30'),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPInitialStepChi2ChargeMeasurementEstimator30 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPInitialStepChi2ChargeMeasurementEstimator30'),
    MaxChi2 = cms.double(30.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPInitialStepChi2MeasurementEstimator36 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPInitialStepChi2MeasurementEstimator36'),
    MaxChi2 = cms.double(36.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(3.0)
)


process.hltESPIter0PFlowTrackCandidatesMkFitConfig = cms.ESProducer("MkFitIterationConfigESProducer",
    ComponentName = cms.string('hltESPIter0PFlowTrackCandidatesMkFitConfig'),
    appendToDataLabel = cms.string(''),
    config = cms.FileInPath('RecoTracker/MkFit/data/mkfit-phase1-hltiter0.json'),
    maxClusterSize = cms.uint32(8),
    minPt = cms.double(0.0)
)


process.hltESPKFFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    ComponentName = cms.string('hltESPKFFittingSmoother'),
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('hltESPKFTrajectoryFitter'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(5),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPKFTrajectorySmoother'),
    appendToDataLabel = cms.string('')
)


process.hltESPKFFittingSmootherForL2Muon = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    ComponentName = cms.string('hltESPKFFittingSmootherForL2Muon'),
    EstimateCut = cms.double(-1.0),
    Fitter = cms.string('hltESPKFTrajectoryFitterForL2Muon'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(5),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPKFTrajectorySmootherForL2Muon'),
    appendToDataLabel = cms.string('')
)


process.hltESPKFFittingSmootherForLoopers = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(True),
    ComponentName = cms.string('hltESPKFFittingSmootherForLoopers'),
    EstimateCut = cms.double(20.0),
    Fitter = cms.string('hltESPKFTrajectoryFitterForLoopers'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-14.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(3),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(True),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPKFTrajectorySmootherForLoopers'),
    appendToDataLabel = cms.string('')
)


process.hltESPKFFittingSmootherWithOutliersRejectionAndRK = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(True),
    ComponentName = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK'),
    EstimateCut = cms.double(20.0),
    Fitter = cms.string('hltESPRKTrajectoryFitter'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-14.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(3),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(True),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPRKTrajectorySmoother'),
    appendToDataLabel = cms.string('')
)


process.hltESPKFTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPKFTrajectoryFitter'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)


process.hltESPKFTrajectoryFitterForL2Muon = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPKFTrajectoryFitterForL2Muon'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)


process.hltESPKFTrajectoryFitterForLoopers = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPKFTrajectoryFitterForLoopers'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialForLoopers'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)


process.hltESPKFTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPKFTrajectorySmoother'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3)
)


process.hltESPKFTrajectorySmootherForL2Muon = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPKFTrajectorySmootherForL2Muon'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPFastSteppingHelixPropagatorOpposite'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3)
)


process.hltESPKFTrajectorySmootherForLoopers = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPKFTrajectorySmootherForLoopers'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialForLoopers'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(3)
)


process.hltESPKFTrajectorySmootherForMuonTrackLoader = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPSmartPropagatorAnyOpposite'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(3)
)


process.hltESPKFUpdator = cms.ESProducer("KFUpdatorESProducer",
    ComponentName = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string('')
)


process.hltESPKullbackLeiblerDistance5D = cms.ESProducer("DistanceBetweenComponentsESProducer5D",
    ComponentName = cms.string('hltESPKullbackLeiblerDistance5D'),
    DistanceMeasure = cms.string('KullbackLeibler'),
    appendToDataLabel = cms.string('')
)


process.hltESPL3MuKFTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPL3MuKFTrajectoryFitter'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPSmartPropagatorAny'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)


process.hltESPLowPtQuadStepChi2ChargeMeasurementEstimator9 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPLowPtQuadStepChi2ChargeMeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPLowPtQuadStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPLowPtQuadStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.16)
)


process.hltESPLowPtStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPLowPtStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.16)
)


process.hltESPLowPtTripletStepChi2ChargeMeasurementEstimator9 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPLowPtTripletStepChi2ChargeMeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPLowPtTripletStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPLowPtTripletStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.16)
)


process.hltESPMeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
    ComponentName = cms.string('hltESPMeasurementTracker'),
    DebugPixelModuleQualityDB = cms.untracked.bool(False),
    DebugPixelROCQualityDB = cms.untracked.bool(False),
    DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
    DebugStripModuleQualityDB = cms.untracked.bool(False),
    DebugStripStripQualityDB = cms.untracked.bool(False),
    HitMatcher = cms.string('StandardMatcher'),
    MaskBadAPVFibers = cms.bool(True),
    Phase2StripCPE = cms.string(''),
    PixelCPE = cms.string('hltESPPixelCPEGeneric'),
    SiStripQualityLabel = cms.string(''),
    StripCPE = cms.string('hltESPStripCPEfromTrackAngle'),
    UsePixelModuleQualityDB = cms.bool(True),
    UsePixelROCQualityDB = cms.bool(True),
    UseStripAPVFiberQualityDB = cms.bool(True),
    UseStripModuleQualityDB = cms.bool(True),
    UseStripStripQualityDB = cms.bool(True),
    appendToDataLabel = cms.string(''),
    badStripCuts = cms.PSet(
        TEC = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        ),
        TIB = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        ),
        TID = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        ),
        TOB = cms.PSet(
            maxBad = cms.uint32(4),
            maxConsecutiveBad = cms.uint32(2)
        )
    )
)


process.hltESPMixedStepClusterShapeHitFilter = cms.ESProducer("ClusterShapeHitFilterESProducer",
    ComponentName = cms.string('hltESPMixedStepClusterShapeHitFilter'),
    PixelShapeFile = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_noL1.par'),
    PixelShapeFileL1 = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_loose.par'),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    doPixelShapeCut = cms.bool(True),
    doStripShapeCut = cms.bool(True),
    isPhase2 = cms.bool(False)
)


process.hltESPMixedStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPMixedStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.11)
)


process.hltESPMixedTripletStepChi2ChargeMeasurementEstimator16 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPMixedTripletStepChi2ChargeMeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPMixedTripletStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPMixedTripletStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.11)
)


process.hltESPMuonDetLayerGeometryESProducer = cms.ESProducer("MuonDetLayerGeometryESProducer")


process.hltESPMuonTransientTrackingRecHitBuilder = cms.ESProducer("MuonTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
    appendToDataLabel = cms.string('')
)


process.hltESPPFRecHitHCALParams = cms.ESProducer("PFRecHitHCALParamsESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string(''),
    energyThresholdsHB = cms.vdouble(0.1, 0.2, 0.3, 0.3),
    energyThresholdsHE = cms.vdouble(
        0.1, 0.2, 0.2, 0.2, 0.2,
        0.2, 0.2
    )
)


process.hltESPPFRecHitHCALTopology = cms.ESProducer("PFRecHitHCALTopologyESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string(''),
    usePFThresholdsFromDB = cms.bool(True)
)


process.hltESPPixelCPEFastParamsHIonPhase1 = cms.ESProducer("PixelCPEFastParamsESProducerAlpakaHIonPhase1@alpaka",
    Alpha2Order = cms.bool(True),
    ClusterProbComputationFlag = cms.int32(0),
    ComponentName = cms.string('PixelCPEFastParamsHIonPhase1'),
    EdgeClusterErrorX = cms.double(50.0),
    EdgeClusterErrorY = cms.double(85.0),
    LoadTemplatesFromDB = cms.bool(True),
    MagneticFieldRecord = cms.ESInputTag("",""),
    TruncatePixelCharge = cms.bool(True),
    UseErrorsFromTemplates = cms.bool(True),
    appendToDataLabel = cms.string(''),
    doLorentzFromAlignment = cms.bool(False),
    lAOffset = cms.double(0.0),
    lAWidthBPix = cms.double(0.0),
    lAWidthFPix = cms.double(0.0),
    useLAFromDB = cms.bool(True),
    useLAWidthFromDB = cms.bool(True),
    xerr_barrel_l1 = cms.vdouble(0.00115, 0.0012, 0.00088),
    xerr_barrel_l1_def = cms.double(0.0103),
    xerr_barrel_ln = cms.vdouble(0.00115, 0.0012, 0.00088),
    xerr_barrel_ln_def = cms.double(0.0103),
    xerr_endcap = cms.vdouble(0.002, 0.002),
    xerr_endcap_def = cms.double(0.002),
    yerr_barrel_l1 = cms.vdouble(
        0.00375, 0.0023, 0.0025, 0.0025, 0.0023,
        0.0023, 0.0021, 0.0021, 0.0024
    ),
    yerr_barrel_l1_def = cms.double(0.0021),
    yerr_barrel_ln = cms.vdouble(
        0.00375, 0.0023, 0.0025, 0.0025, 0.0023,
        0.0023, 0.0021, 0.0021, 0.0024
    ),
    yerr_barrel_ln_def = cms.double(0.0021),
    yerr_endcap = cms.vdouble(0.0021),
    yerr_endcap_def = cms.double(0.00075)
)


process.hltESPPixelCPEFastParamsPhase1 = cms.ESProducer("PixelCPEFastParamsESProducerAlpakaPhase1@alpaka",
    Alpha2Order = cms.bool(True),
    ClusterProbComputationFlag = cms.int32(0),
    ComponentName = cms.string('PixelCPEFastParams'),
    EdgeClusterErrorX = cms.double(50.0),
    EdgeClusterErrorY = cms.double(85.0),
    LoadTemplatesFromDB = cms.bool(True),
    MagneticFieldRecord = cms.ESInputTag("",""),
    TruncatePixelCharge = cms.bool(True),
    UseErrorsFromTemplates = cms.bool(True),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string(''),
    doLorentzFromAlignment = cms.bool(False),
    lAOffset = cms.double(0.0),
    lAWidthBPix = cms.double(0.0),
    lAWidthFPix = cms.double(0.0),
    useLAFromDB = cms.bool(True),
    useLAWidthFromDB = cms.bool(True),
    xerr_barrel_l1 = cms.vdouble(0.00115, 0.0012, 0.00088),
    xerr_barrel_l1_def = cms.double(0.0103),
    xerr_barrel_ln = cms.vdouble(0.00115, 0.0012, 0.00088),
    xerr_barrel_ln_def = cms.double(0.0103),
    xerr_endcap = cms.vdouble(0.002, 0.002),
    xerr_endcap_def = cms.double(0.002),
    yerr_barrel_l1 = cms.vdouble(
        0.00375, 0.0023, 0.0025, 0.0025, 0.0023,
        0.0023, 0.0021, 0.0021, 0.0024
    ),
    yerr_barrel_l1_def = cms.double(0.0021),
    yerr_barrel_ln = cms.vdouble(
        0.00375, 0.0023, 0.0025, 0.0025, 0.0023,
        0.0023, 0.0021, 0.0021, 0.0024
    ),
    yerr_barrel_ln_def = cms.double(0.0021),
    yerr_endcap = cms.vdouble(0.0021),
    yerr_endcap_def = cms.double(0.00075)
)


process.hltESPPixelCPEGeneric = cms.ESProducer("PixelCPEGenericESProducer",
    Alpha2Order = cms.bool(True),
    ClusterProbComputationFlag = cms.int32(0),
    ComponentName = cms.string('hltESPPixelCPEGeneric'),
    DoCosmics = cms.bool(False),
    EdgeClusterErrorX = cms.double(50.0),
    EdgeClusterErrorY = cms.double(85.0),
    IrradiationBiasCorrection = cms.bool(False),
    LoadTemplatesFromDB = cms.bool(True),
    MagneticFieldRecord = cms.ESInputTag("",""),
    NoTemplateErrorsWhenNoTrkAngles = cms.bool(False),
    SmallPitch = cms.bool(False),
    TruncatePixelCharge = cms.bool(True),
    UseErrorsFromTemplates = cms.bool(True),
    appendToDataLabel = cms.string(''),
    doLorentzFromAlignment = cms.bool(False),
    eff_charge_cut_highX = cms.double(1.0),
    eff_charge_cut_highY = cms.double(1.0),
    eff_charge_cut_lowX = cms.double(0.0),
    eff_charge_cut_lowY = cms.double(0.0),
    inflate_all_errors_no_trk_angle = cms.bool(False),
    inflate_errors = cms.bool(False),
    isPhase2 = cms.bool(False),
    lAOffset = cms.double(0.0),
    lAWidthBPix = cms.double(0.0),
    lAWidthFPix = cms.double(0.0),
    size_cutX = cms.double(3.0),
    size_cutY = cms.double(3.0),
    useLAFromDB = cms.bool(True),
    useLAWidthFromDB = cms.bool(False),
    xerr_barrel_l1 = cms.vdouble(0.00115, 0.0012, 0.00088),
    xerr_barrel_l1_def = cms.double(0.0103),
    xerr_barrel_ln = cms.vdouble(0.00115, 0.0012, 0.00088),
    xerr_barrel_ln_def = cms.double(0.0103),
    xerr_endcap = cms.vdouble(0.002, 0.002),
    xerr_endcap_def = cms.double(0.002),
    yerr_barrel_l1 = cms.vdouble(
        0.00375, 0.0023, 0.0025, 0.0025, 0.0023,
        0.0023, 0.0021, 0.0021, 0.0024
    ),
    yerr_barrel_l1_def = cms.double(0.0021),
    yerr_barrel_ln = cms.vdouble(
        0.00375, 0.0023, 0.0025, 0.0025, 0.0023,
        0.0023, 0.0021, 0.0021, 0.0024
    ),
    yerr_barrel_ln_def = cms.double(0.0021),
    yerr_endcap = cms.vdouble(0.0021),
    yerr_endcap_def = cms.double(0.00075)
)


process.hltESPPixelCPETemplateReco = cms.ESProducer("PixelCPETemplateRecoESProducer",
    Alpha2Order = cms.bool(True),
    ClusterProbComputationFlag = cms.int32(0),
    ComponentName = cms.string('hltESPPixelCPETemplateReco'),
    GoodEdgeAlgo = cms.bool(False),
    LoadTemplatesFromDB = cms.bool(True),
    UseClusterSplitter = cms.bool(False),
    appendToDataLabel = cms.string(''),
    barrelTemplateID = cms.int32(0),
    directoryWithTemplates = cms.int32(0),
    doLorentzFromAlignment = cms.bool(False),
    forwardTemplateID = cms.int32(0),
    lAOffset = cms.double(0.0),
    lAWidthBPix = cms.double(0.0),
    lAWidthFPix = cms.double(0.0),
    speed = cms.int32(-2),
    useLAFromDB = cms.bool(True),
    useLAWidthFromDB = cms.bool(True)
)


process.hltESPPixelLessStepChi2ChargeMeasurementEstimator16 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPPixelLessStepChi2ChargeMeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPPixelLessStepClusterShapeHitFilter = cms.ESProducer("ClusterShapeHitFilterESProducer",
    ComponentName = cms.string('hltESPPixelLessStepClusterShapeHitFilter'),
    PixelShapeFile = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_noL1.par'),
    PixelShapeFileL1 = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_loose.par'),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    doPixelShapeCut = cms.bool(True),
    doStripShapeCut = cms.bool(True),
    isPhase2 = cms.bool(False)
)


process.hltESPPixelLessStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPPixelLessStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.11)
)


process.hltESPPixelPairStepChi2ChargeMeasurementEstimator9 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPPixelPairStepChi2ChargeMeasurementEstimator9'),
    MaxChi2 = cms.double(9.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutLoose')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(15.0)
)


process.hltESPPixelPairStepChi2MeasurementEstimator25 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPPixelPairStepChi2MeasurementEstimator25'),
    MaxChi2 = cms.double(25.0),
    MaxDisplacement = cms.double(100.0),
    MaxSagitta = cms.double(-1.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(10.0),
    appendToDataLabel = cms.string(''),
    nSigma = cms.double(3.0)
)


process.hltESPPixelPairTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPPixelPairTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.19)
)


process.hltESPRKTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPRKTrajectoryFitter'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)


process.hltESPRKTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPRKTrajectorySmoother'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3)
)


process.hltESPRungeKuttaTrackerPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
    ComponentName = cms.string('hltESPRungeKuttaTrackerPropagator'),
    Mass = cms.double(0.105),
    MaxDPhi = cms.double(1.6),
    PropagationDirection = cms.string('alongMomentum'),
    SimpleMagneticField = cms.string(''),
    ptMin = cms.double(-1.0),
    useRungeKutta = cms.bool(True)
)


process.hltESPSiPixelCablingSoA = cms.ESProducer("SiPixelCablingSoAESProducer@alpaka",
    CablingMapLabel = cms.string(''),
    UseQualityInfo = cms.bool(False),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.hltESPSiPixelGainCalibrationForHLTSoA = cms.ESProducer("SiPixelGainCalibrationForHLTSoAESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    ),
    appendToDataLabel = cms.string('')
)


process.hltESPSmartPropagator = cms.ESProducer("SmartPropagatorESProducer",
    ComponentName = cms.string('hltESPSmartPropagator'),
    Epsilon = cms.double(5.0),
    MuonPropagator = cms.string('hltESPSteppingHelixPropagatorAlong'),
    PropagationDirection = cms.string('alongMomentum'),
    TrackerPropagator = cms.string('PropagatorWithMaterial'),
    appendToDataLabel = cms.string('')
)


process.hltESPSmartPropagatorAny = cms.ESProducer("SmartPropagatorESProducer",
    ComponentName = cms.string('hltESPSmartPropagatorAny'),
    Epsilon = cms.double(5.0),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('alongMomentum'),
    TrackerPropagator = cms.string('PropagatorWithMaterial'),
    appendToDataLabel = cms.string('')
)


process.hltESPSmartPropagatorAnyOpposite = cms.ESProducer("SmartPropagatorESProducer",
    ComponentName = cms.string('hltESPSmartPropagatorAnyOpposite'),
    Epsilon = cms.double(5.0),
    MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
    PropagationDirection = cms.string('oppositeToMomentum'),
    TrackerPropagator = cms.string('PropagatorWithMaterialOpposite'),
    appendToDataLabel = cms.string('')
)


process.hltESPSoftLeptonByDistance = cms.ESProducer("LeptonTaggerByDistanceESProducer",
    appendToDataLabel = cms.string(''),
    distance = cms.double(0.5)
)


process.hltESPSteppingHelixPropagatorAlong = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPSteppingHelixPropagatorAlong'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('alongMomentum'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    appendToDataLabel = cms.string(''),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False)
)


process.hltESPSteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
    ApplyRadX0Correction = cms.bool(True),
    AssumeNoMaterial = cms.bool(False),
    ComponentName = cms.string('hltESPSteppingHelixPropagatorOpposite'),
    NoErrorPropagation = cms.bool(False),
    PropagationDirection = cms.string('oppositeToMomentum'),
    SetVBFPointer = cms.bool(False),
    VBFName = cms.string('VolumeBasedMagneticField'),
    appendToDataLabel = cms.string(''),
    debug = cms.bool(False),
    endcapShiftInZNeg = cms.double(0.0),
    endcapShiftInZPos = cms.double(0.0),
    returnTangentPlane = cms.bool(True),
    sendLogWarning = cms.bool(False),
    useEndcapShiftsInZ = cms.bool(False),
    useInTeslaFromMagField = cms.bool(False),
    useIsYokeFlag = cms.bool(True),
    useMagVolumes = cms.bool(True),
    useMatVolumes = cms.bool(True),
    useTuningForL2Speed = cms.bool(False)
)


process.hltESPStripCPEfromTrackAngle = cms.ESProducer("StripCPEESProducer",
    ComponentName = cms.string('hltESPStripCPEfromTrackAngle'),
    ComponentType = cms.string('StripCPEfromTrackAngle'),
    parameters = cms.PSet(
        mLC_P0 = cms.double(-0.326),
        mLC_P1 = cms.double(0.618),
        mLC_P2 = cms.double(0.3),
        mTEC_P0 = cms.double(-1.885),
        mTEC_P1 = cms.double(0.471),
        mTIB_P0 = cms.double(-0.742),
        mTIB_P1 = cms.double(0.202),
        mTID_P0 = cms.double(-1.427),
        mTID_P1 = cms.double(0.433),
        mTOB_P0 = cms.double(-1.026),
        mTOB_P1 = cms.double(0.253),
        maxChgOneMIP = cms.double(6000.0),
        useLegacyError = cms.bool(False)
    )
)


process.hltESPTTRHBWithTrackAngle = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPTTRHBWithTrackAngle'),
    ComputeCoarseLocalPositionFromDisk = cms.bool(False),
    Matcher = cms.string('StandardMatcher'),
    Phase2StripCPE = cms.string(''),
    PixelCPE = cms.string('hltESPPixelCPEGeneric'),
    StripCPE = cms.string('hltESPStripCPEfromTrackAngle'),
    appendToDataLabel = cms.string('')
)


process.hltESPTTRHBuilderAngleAndTemplate = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPTTRHBuilderAngleAndTemplate'),
    ComputeCoarseLocalPositionFromDisk = cms.bool(False),
    Matcher = cms.string('StandardMatcher'),
    Phase2StripCPE = cms.string(''),
    PixelCPE = cms.string('hltESPPixelCPETemplateReco'),
    StripCPE = cms.string('hltESPStripCPEfromTrackAngle'),
    appendToDataLabel = cms.string('')
)


process.hltESPTTRHBuilderPixelOnly = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPTTRHBuilderPixelOnly'),
    ComputeCoarseLocalPositionFromDisk = cms.bool(False),
    Matcher = cms.string('StandardMatcher'),
    Phase2StripCPE = cms.string(''),
    PixelCPE = cms.string('hltESPPixelCPEGeneric'),
    StripCPE = cms.string('Fake'),
    appendToDataLabel = cms.string('')
)


process.hltESPTTRHBuilderWithoutAngle4PixelTriplets = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    ComponentName = cms.string('hltESPTTRHBuilderWithoutAngle4PixelTriplets'),
    ComputeCoarseLocalPositionFromDisk = cms.bool(False),
    Matcher = cms.string('StandardMatcher'),
    Phase2StripCPE = cms.string(''),
    PixelCPE = cms.string('hltESPPixelCPEGeneric'),
    StripCPE = cms.string('Fake'),
    appendToDataLabel = cms.string('')
)


process.hltESPTobTecStepChi2ChargeMeasurementEstimator16 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
    ComponentName = cms.string('hltESPTobTecStepChi2ChargeMeasurementEstimator16'),
    MaxChi2 = cms.double(16.0),
    MaxDisplacement = cms.double(0.5),
    MaxSagitta = cms.double(2.0),
    MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
    MinimalTolerance = cms.double(0.5),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    nSigma = cms.double(3.0),
    pTChargeCutThreshold = cms.double(-1.0)
)


process.hltESPTobTecStepClusterShapeHitFilter = cms.ESProducer("ClusterShapeHitFilterESProducer",
    ComponentName = cms.string('hltESPTobTecStepClusterShapeHitFilter'),
    PixelShapeFile = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_noL1.par'),
    PixelShapeFileL1 = cms.string('RecoTracker/PixelLowPtUtilities/data/pixelShapePhase1_loose.par'),
    appendToDataLabel = cms.string(''),
    clusterChargeCut = cms.PSet(
        refToPSet_ = cms.string('HLTSiStripClusterChargeCutTight')
    ),
    doPixelShapeCut = cms.bool(True),
    doStripShapeCut = cms.bool(True),
    isPhase2 = cms.bool(False)
)


process.hltESPTobTecStepFittingSmoother = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    ComponentName = cms.string('hltESPTobTecStepFitterSmoother'),
    EstimateCut = cms.double(30.0),
    Fitter = cms.string('hltESPTobTecStepRKFitter'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(7),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPTobTecStepRKSmoother'),
    appendToDataLabel = cms.string('')
)


process.hltESPTobTecStepFittingSmootherForLoopers = cms.ESProducer("KFFittingSmootherESProducer",
    BreakTrajWith2ConsecutiveMissing = cms.bool(False),
    ComponentName = cms.string('hltESPTobTecStepFitterSmootherForLoopers'),
    EstimateCut = cms.double(30.0),
    Fitter = cms.string('hltESPTobTecStepRKFitterForLoopers'),
    HighEtaSwitch = cms.double(5.0),
    LogPixelProbabilityCut = cms.double(-16.0),
    MaxFractionOutliers = cms.double(0.3),
    MaxNumberOfOutliers = cms.int32(3),
    MinDof = cms.int32(2),
    MinNumberOfHits = cms.int32(7),
    MinNumberOfHitsHighEta = cms.int32(5),
    NoInvalidHitsBeginEnd = cms.bool(False),
    NoOutliersBeginEnd = cms.bool(False),
    RejectTracks = cms.bool(True),
    Smoother = cms.string('hltESPTobTecStepRKSmootherForLoopers'),
    appendToDataLabel = cms.string('')
)


process.hltESPTobTecStepFlexibleKFFittingSmoother = cms.ESProducer("FlexibleKFFittingSmootherESProducer",
    ComponentName = cms.string('hltESPTobTecStepFlexibleKFFittingSmoother'),
    appendToDataLabel = cms.string(''),
    looperFitter = cms.string('hltESPTobTecStepFitterSmootherForLoopers'),
    standardFitter = cms.string('hltESPTobTecStepFitterSmoother')
)


process.hltESPTobTecStepRKTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPTobTecStepRKFitter'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(7)
)


process.hltESPTobTecStepRKTrajectoryFitterForLoopers = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPTobTecStepRKFitterForLoopers'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialForLoopers'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(7)
)


process.hltESPTobTecStepRKTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPTobTecStepRKSmoother'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialParabolicMf'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(7)
)


process.hltESPTobTecStepRKTrajectorySmootherForLoopers = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPTobTecStepRKSmootherForLoopers'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('PropagatorWithMaterialForLoopers'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(10.0),
    minHits = cms.int32(7)
)


process.hltESPTobTecStepTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPTobTecStepTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.09)
)


process.hltESPTrackAlgoPriorityOrder = cms.ESProducer("TrackAlgoPriorityOrderESProducer",
    ComponentName = cms.string('hltESPTrackAlgoPriorityOrder'),
    algoOrder = cms.vstring(),
    appendToDataLabel = cms.string('')
)


process.hltESPTrackSelectionTfCKF = cms.ESProducer("TfGraphDefProducer",
    ComponentName = cms.string('hltESPTrackSelectionTfCKF'),
    FileName = cms.FileInPath('RecoTracker/FinalTrackSelectors/data/TrackTfClassifier/CKF_Run3_12_5_0_pre5.pb'),
    appendToDataLabel = cms.string('')
)


process.hltESPTrackerRecoGeometryESProducer = cms.ESProducer("TrackerRecoGeometryESProducer",
    appendToDataLabel = cms.string(''),
    trackerGeometryLabel = cms.untracked.string(''),
    usePhase2Stacks = cms.bool(False)
)


process.hltESPTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(0.0),
    ValidHitBonus = cms.double(100.0),
    allowSharedFirstHit = cms.bool(False),
    fractionShared = cms.double(0.5)
)


process.hltESPTrajectoryCleanerBySharedHitsP5 = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('hltESPTrajectoryCleanerBySharedHitsP5'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(20.0),
    ValidHitBonus = cms.double(5.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.19)
)


process.hltESPTrajectoryFitterRK = cms.ESProducer("KFTrajectoryFitterESProducer",
    ComponentName = cms.string('hltESPTrajectoryFitterRK'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    minHits = cms.int32(3)
)


process.hltESPTrajectorySmootherRK = cms.ESProducer("KFTrajectorySmootherESProducer",
    ComponentName = cms.string('hltESPTrajectorySmootherRK'),
    Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
    Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
    RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
    Updator = cms.string('hltESPKFUpdator'),
    appendToDataLabel = cms.string(''),
    errorRescaling = cms.double(100.0),
    minHits = cms.int32(3)
)


process.hltPixelTracksCleanerBySharedHits = cms.ESProducer("PixelTrackCleanerBySharedHitsESProducer",
    ComponentName = cms.string('hltPixelTracksCleanerBySharedHits'),
    appendToDataLabel = cms.string(''),
    useQuadrupletAlgo = cms.bool(False)
)


process.hltTrackCleaner = cms.ESProducer("TrackCleanerESProducer",
    ComponentName = cms.string('hltTrackCleaner'),
    appendToDataLabel = cms.string('')
)


process.hoDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('HODetIdAssociator'),
    etaBinSize = cms.double(0.087),
    hcalRegion = cms.int32(2),
    includeBadChambers = cms.bool(False),
    includeGEM = cms.bool(False),
    includeME0 = cms.bool(False),
    nEta = cms.int32(30),
    nPhi = cms.int32(72)
)


process.mkFitGeometryESProducer = cms.ESProducer("MkFitGeometryESProducer",
    appendToDataLabel = cms.string('')
)


process.multipleScatteringParametrisationMakerESProducer = cms.ESProducer("MultipleScatteringParametrisationMakerESProducer",
    appendToDataLabel = cms.string('')
)


process.muonDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('MuonDetIdAssociator'),
    etaBinSize = cms.double(0.125),
    hcalRegion = cms.int32(2),
    includeBadChambers = cms.bool(True),
    includeGEM = cms.bool(True),
    includeME0 = cms.bool(False),
    nEta = cms.int32(48),
    nPhi = cms.int32(48)
)


process.muonSeededTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
    ComponentName = cms.string('muonSeededTrajectoryCleanerBySharedHits'),
    ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
    MissingHitPenalty = cms.double(1.0),
    ValidHitBonus = cms.double(1000.0),
    allowSharedFirstHit = cms.bool(True),
    fractionShared = cms.double(0.1)
)


process.navigationSchoolESProducer = cms.ESProducer("NavigationSchoolESProducer",
    ComponentName = cms.string('SimpleNavigationSchool'),
    PluginName = cms.string(''),
    SimpleMagneticField = cms.string('ParabolicMf'),
    appendToDataLabel = cms.string('')
)


process.preshowerDetIdAssociator = cms.ESProducer("DetIdAssociatorESProducer",
    ComponentName = cms.string('PreshowerDetIdAssociator'),
    etaBinSize = cms.double(0.1),
    hcalRegion = cms.int32(2),
    includeBadChambers = cms.bool(False),
    includeGEM = cms.bool(False),
    includeME0 = cms.bool(False),
    nEta = cms.int32(60),
    nPhi = cms.int32(30)
)


process.siPixelGainCalibrationForHLTGPU = cms.ESProducer("SiPixelGainCalibrationForHLTGPUESProducer",
    appendToDataLabel = cms.string('')
)


process.siPixelQualityESProducer = cms.ESProducer("SiPixelQualityESProducer",
    ListOfRecordToMerge = cms.VPSet(
        cms.PSet(
            record = cms.string('SiPixelQualityFromDbRcd'),
            tag = cms.string('')
        ),
        cms.PSet(
            record = cms.string('SiPixelDetVOffRcd'),
            tag = cms.string('')
        )
    ),
    appendToDataLabel = cms.string(''),
    siPixelQualityFromDbLabel = cms.string('')
)


process.siPixelROCsStatusAndMappingWrapperESProducer = cms.ESProducer("SiPixelROCsStatusAndMappingWrapperESProducer",
    CablingMapLabel = cms.string(''),
    ComponentName = cms.string(''),
    UseQualityInfo = cms.bool(False),
    appendToDataLabel = cms.string('')
)


process.siPixelTemplateDBObjectESProducer = cms.ESProducer("SiPixelTemplateDBObjectESProducer")


process.siStripBackPlaneCorrectionDepESProducer = cms.ESProducer("SiStripBackPlaneCorrectionDepESProducer",
    BackPlaneCorrectionDeconvMode = cms.PSet(
        label = cms.untracked.string('deconvolution'),
        record = cms.string('SiStripBackPlaneCorrectionRcd')
    ),
    BackPlaneCorrectionPeakMode = cms.PSet(
        label = cms.untracked.string('peak'),
        record = cms.string('SiStripBackPlaneCorrectionRcd')
    ),
    LatencyRecord = cms.PSet(
        label = cms.untracked.string(''),
        record = cms.string('SiStripLatencyRcd')
    )
)


process.siStripLorentzAngleDepESProducer = cms.ESProducer("SiStripLorentzAngleDepESProducer",
    LatencyRecord = cms.PSet(
        label = cms.untracked.string(''),
        record = cms.string('SiStripLatencyRcd')
    ),
    LorentzAngleDeconvMode = cms.PSet(
        label = cms.untracked.string('deconvolution'),
        record = cms.string('SiStripLorentzAngleRcd')
    ),
    LorentzAnglePeakMode = cms.PSet(
        label = cms.untracked.string('peak'),
        record = cms.string('SiStripLorentzAngleRcd')
    )
)


process.sistripconn = cms.ESProducer("SiStripConnectivity")


process.trackerTopology = cms.ESProducer("TrackerTopologyEP",
    appendToDataLabel = cms.string('')
)


process.zdcTopologyEP = cms.ESProducer("ZdcTopologyEP",
    appendToDataLabel = cms.string('')
)


process.CSCChannelMapperESSource = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('CSCChannelMapperRecord')
)


process.CSCINdexerESSource = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('CSCIndexerRecord')
)


process.CSCL1TPLookupTableEP = cms.ESSource("CSCL1TPLookupTableEP",
    esDiffToSlopeME11aFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11a_even_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11a_odd_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11a_even_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11a_odd_GEMlayer2.txt'
    ),
    esDiffToSlopeME11bFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11b_even_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11b_odd_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11b_even_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME11b_odd_GEMlayer2.txt'
    ),
    esDiffToSlopeME21Files = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME21_even_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME21_odd_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME21_even_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/BendingAngle/SlopeAmendment_ME21_odd_GEMlayer2.txt'
    ),
    gemCscSlopeCorrectionFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11a_even_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11b_even_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME21_even_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11a_odd_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11b_odd_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME21_odd_GEMlayer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11a_even_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11b_even_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME21_even_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11a_odd_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME11b_odd_GEMlayer2.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/ExtrapolationBySlope_ME21_odd_GEMlayer2.txt'
    ),
    gemCscSlopeCosiCorrectionFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/GEMCSCconsistentSlopeCorr_ME11a_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/GEMCSCconsistentSlopeCorr_ME11b_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/GEMCSCconsistentSlopeCorr_ME21_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/GEMCSCconsistentSlopeCorr_ME11a_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/GEMCSCconsistentSlopeCorr_ME11b_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/GEMCSCconsistentSlopeCorr_ME21_odd_layer1.txt'
    ),
    gemCscSlopeCosiFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_2to1_SlopeShift_ME11a_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_2to1_SlopeShift_ME11a_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_3to1_SlopeShift_ME11a_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_3to1_SlopeShift_ME11a_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_2to1_SlopeShift_ME11b_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_2to1_SlopeShift_ME11b_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_3to1_SlopeShift_ME11b_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_3to1_SlopeShift_ME11b_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_2to1_SlopeShift_ME21_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_2to1_SlopeShift_ME21_odd_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_3to1_SlopeShift_ME21_even_layer1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/SlopeCorrection/FacingChambers/CSCconsistency_3to1_SlopeShift_ME21_odd_layer1.txt'
    ),
    padToEsME11aFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_pad_es_ME1a_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_pad_es_ME1a_odd.txt'
    ),
    padToEsME11bFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_pad_es_ME1b_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_pad_es_ME1b_odd.txt'
    ),
    padToEsME21Files = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_pad_es_ME21_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_pad_es_ME21_odd.txt'
    ),
    positionLUTFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodePosOffsetLUT_pat0_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodePosOffsetLUT_pat1_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodePosOffsetLUT_pat2_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodePosOffsetLUT_pat3_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodePosOffsetLUT_pat4_v1.txt'
    ),
    rollToMaxWgME11Files = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_max_wg_ME11_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_max_wg_ME11_odd.txt'
    ),
    rollToMaxWgME21Files = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_max_wg_ME21_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_max_wg_ME21_odd.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l2_max_wg_ME21_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l2_max_wg_ME21_odd.txt'
    ),
    rollToMinWgME11Files = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_min_wg_ME11_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_min_wg_ME11_odd.txt'
    ),
    rollToMinWgME21Files = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_min_wg_ME21_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l1_min_wg_ME21_odd.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l2_min_wg_ME21_even.txt',
        'L1Trigger/CSCTriggerPrimitives/data/GEMCSC/CoordinateConversion/GEMCSCLUT_roll_l2_min_wg_ME21_odd.txt'
    ),
    slopeLUTFiles = cms.vstring(
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodeSlopeLUT_pat0_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodeSlopeLUT_pat1_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodeSlopeLUT_pat2_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodeSlopeLUT_pat3_v1.txt',
        'L1Trigger/CSCTriggerPrimitives/data/CCLUT/CSCComparatorCodeSlopeLUT_pat4_v1.txt'
    )
)


process.GlobalParametersRcdSource = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TGlobalParametersRcd')
)


process.GlobalTag = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('.'),
        messageLevel = cms.untracked.int32(0)
    ),
    DumpStat = cms.untracked.bool(False),
    JsonDumpFileName = cms.untracked.string(''),
    ReconnectEachRun = cms.untracked.bool(False),
    RefreshAlways = cms.untracked.bool(False),
    RefreshEachRun = cms.untracked.bool(False),
    RefreshOpenIOVs = cms.untracked.bool(False),
    appendToDataLabel = cms.string(''),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
    frontierKey = cms.untracked.string(''),
    globaltag = cms.string('150X_dataRun3_NGT_v2'),
    pfnPostfix = cms.untracked.string(''),
    pfnPrefix = cms.untracked.string(''),
    recordsToDebug = cms.untracked.vstring(),
    snapshotTime = cms.string(''),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('L1TUtmTriggerMenuRcd'),
        snapshotTime = cms.string('9999-12-31 23:59:59.000'),
        tag = cms.string('L1Menu_Collisions2025_v1_3_0_xml')
    ))
)


process.HcalTimeSlewEP = cms.ESSource("HcalTimeSlewEP",
    appendToDataLabel = cms.string('HBHE'),
    timeSlewParametersM2 = cms.VPSet(
        cms.PSet(
            slope = cms.double(-3.178648),
            tmax = cms.double(16.0),
            tzero = cms.double(23.960177)
        ),
        cms.PSet(
            slope = cms.double(-1.5610227),
            tmax = cms.double(10.0),
            tzero = cms.double(11.977461)
        ),
        cms.PSet(
            slope = cms.double(-1.075824),
            tmax = cms.double(6.25),
            tzero = cms.double(9.109694)
        )
    ),
    timeSlewParametersM3 = cms.VPSet(
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(12.2999),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-2.19142),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(0.0),
            tspar2_siPM = cms.double(0.0)
        ),
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(15.5),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-3.2),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(32.0),
            tspar2_siPM = cms.double(0.0)
        ),
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(12.2999),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-2.19142),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(0.0),
            tspar2_siPM = cms.double(0.0)
        ),
        cms.PSet(
            cap = cms.double(6.0),
            tspar0 = cms.double(12.2999),
            tspar0_siPM = cms.double(0.0),
            tspar1 = cms.double(-2.19142),
            tspar1_siPM = cms.double(0.0),
            tspar2 = cms.double(0.0),
            tspar2_siPM = cms.double(0.0)
        )
    )
)


process.HepPDTESSource = cms.ESSource("HepPDTESSource",
    pdtFileName = cms.FileInPath('SimGeneral/HepPDTESSource/data/pythiaparticle.tbl')
)


process.bmbtfParamsSource = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TMuonBarrelParamsRcd')
)


process.caloConfigSource = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TCaloConfigRcd')
)


process.eegeom = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalMappingRcd')
)


process.es_hardcode = cms.ESSource("HcalHardcodeCalibrations",
    fromDDD = cms.untracked.bool(False),
    toGet = cms.untracked.vstring('GainWidths')
)


process.hltESSBTagRecord = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('JetTagComputerRecord')
)


process.hltESSEcalSeverityLevel = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('EcalSeverityLevelAlgoRcd')
)


process.hltESSHcalSeverityLevel = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('HcalSeverityLevelComputerRcd')
)


process.hltESSPFRecHitHCALParamsRecord = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('PFRecHitHCALParamsRecord')
)


process.hltESSPFRecHitHCALTopologyRecord = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('PFRecHitHCALTopologyRecord')
)


process.hltESSTfGraphRecord = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('TfGraphRecord')
)


process.l1ugmtdb = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string(''),
        authenticationSystem = cms.untracked.int32(0),
        connectionTimeout = cms.untracked.int32(0),
        messageLevel = cms.untracked.int32(0),
        security = cms.untracked.string('')
    ),
    connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('L1TMuonGlobalParamsO2ORcd'),
        tag = cms.string('L1TMuonGlobalParamsPrototype_Stage2v0_hlt')
    ))
)


process.ppsPixelTopologyESSource = cms.ESSource("PPSPixelTopologyESSource",
    PitchSimX = cms.double(0.1),
    PitchSimY = cms.double(0.15),
    RunType = cms.string('Run3'),
    activeEdgeSigma = cms.double(0.02),
    appendToDataLabel = cms.string(''),
    deadEdgeWidth = cms.double(0.2),
    noOfPixelSimX = cms.int32(160),
    noOfPixelSimY = cms.int32(104),
    noOfPixels = cms.int32(16640),
    physActiveEdgeDist = cms.double(0.15),
    simXWidth = cms.double(16.6),
    simYWidth = cms.double(16.2),
    thickness = cms.double(0.23)
)


process.rpcconesrc = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1RPCConeBuilderRcd')
)


process.twinmuxParamsSource = cms.ESSource("EmptyESSource",
    firstValid = cms.vuint32(1),
    iovIsRunNotTime = cms.bool(True),
    recordName = cms.string('L1TTwinMuxParamsRcd')
)


process.SimL1TGlobalTask = cms.Task(process.simGtStage2Digis)


process.SimL1TechnicalTriggersTask = cms.Task(process.simGtExtFakeStage2Digis)


process.SimL1EmulatorTask = cms.Task(process.SimL1TGlobalTask, process.SimL1TechnicalTriggersTask, process.packGtStage2, process.rawDataCollector, process.unpackGtStage2, process.unpackTcds)


process.HLTL1UnpackerSequence = cms.Sequence(process.hltGtStage2Digis+process.hltGtStage2ObjectMap)


process.HLTBeamSpot = cms.Sequence(process.hltOnlineMetaDataDigis+process.hltOnlineBeamSpot)


process.HLTBeginSequence = cms.Sequence(process.hltTriggerType+process.HLTL1UnpackerSequence+process.HLTBeamSpot)


process.HLTMuonLocalRecoSequence = cms.Sequence(process.hltMuonDTDigis+process.hltDt1DRecHits+process.hltDt4DSegments+process.hltMuonCSCDigis+process.hltCsc2DRecHits+process.hltCscSegments+process.hltMuonRPCDigisCPPF+process.hltOmtfDigis+process.hltMuonRPCDigisTwinMux+process.hltMuonRPCDigis+process.hltRpcRecHits+process.hltMuonGEMDigis+process.hltGemRecHits+process.hltGemSegments)


process.HLTL2muonrecoNocandSequence = cms.Sequence(process.HLTMuonLocalRecoSequence+process.hltL2OfflineMuonSeeds+process.hltL2MuonSeeds+process.hltL2Muons)


process.HLTL2muonrecoSequenceNoVtx = cms.Sequence(process.HLTL2muonrecoNocandSequence+process.hltL2MuonCandidatesNoVtx)


process.HLTDoLocalPixelSequence = cms.Sequence(process.hltOnlineBeamSpotDevice+process.hltSiPixelClustersSoA+process.hltSiPixelClusters+process.hltSiPixelDigiErrors+process.hltSiPixelRecHitsSoA+process.hltSiPixelRecHits)


process.HLTDoLocalStripOnDemandSequence = cms.Sequence(process.hltSiStripExcludedFEDListProducer+process.hltSiStripRawToClustersFacilityOnDemand+process.hltMeasurementTrackerEventOnDemand)


process.HLTIterL3OImuonTkCandidateSequenceNoVtx = cms.Sequence(process.hltIterL3OISeedsFromL2MuonsNoVtx+process.hltIterL3OITrackCandidatesNoVtx+process.hltIterL3OIMuCtfWithMaterialTracksNoVtx+process.hltIterL3OIMuonTrackCutClassifierNoVtx+process.hltIterL3OIMuonTrackSelectionHighPurityNoVtx+process.hltL3MuonsIterL3OINoVtx)


process.HLTRecoPixelTracksSequence = cms.Sequence(process.hltPixelTracksSoA+process.hltPixelTracks)


process.HLTRecopixelvertexingSequence = cms.Sequence(process.HLTRecoPixelTracksSequence+process.hltPixelVerticesSoA+process.hltPixelVertices+process.hltTrimmedPixelVertices)


process.HLTIterL3MuonRecoPixelTracksSequenceNoVtx = cms.Sequence(process.HLTRecopixelvertexingSequence+process.hltIterL3MuonPixelTracksTrackingRegionsNoVtx+process.hltPixelTracksInRegionL2NoVtx)


process.HLTIterL3MuonRecopixelvertexingSequenceNoVtx = cms.Sequence(process.HLTIterL3MuonRecoPixelTracksSequenceNoVtx)


process.HLTIterativeTrackingIteration0ForIterL3MuonNoVtx = cms.Sequence(process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx+process.hltIter0IterL3MuonCkfTrackCandidatesNoVtx+process.hltIter0IterL3MuonCtfWithMaterialTracksNoVtx+process.hltIter0IterL3MuonTrackCutClassifierNoVtx+process.hltIter0IterL3MuonTrackSelectionHighPurityNoVtx)


process.HLTIterL3IOmuonTkCandidateSequenceNoVtx = cms.Sequence(process.HLTIterL3MuonRecopixelvertexingSequenceNoVtx+process.HLTIterativeTrackingIteration0ForIterL3MuonNoVtx+process.hltL3MuonsIterL3IONoVtx)


process.HLTIterL3OIAndIOFromL2muonTkCandidateSequenceNoVtx = cms.Sequence(process.HLTIterL3OImuonTkCandidateSequenceNoVtx+process.hltIterL3OIL3MuonsLinksCombinationNoVtx+process.hltIterL3OIL3MuonsNoVtx+process.hltIterL3OIL3MuonCandidatesNoVtx+process.hltL2SelectorForL3IONoVtx+process.HLTIterL3IOmuonTkCandidateSequenceNoVtx+process.hltIterL3MuonsFromL2LinksCombinationNoVtx+process.hltIterL3MuonsFromL2NoVtx)


process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx = cms.Sequence(process.HLTRecopixelvertexingSequence+process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx+process.hltPixelTracksInRegionL1NoVtx)


process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonNoVtx = cms.Sequence(process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx+process.hltIter0IterL3FromL1MuonCkfTrackCandidatesNoVtx+process.hltIter0IterL3FromL1MuonCtfWithMaterialTracksNoVtx+process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx+process.hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx)


process.HLTIterL3IOmuonFromL1TkCandidateSequenceNoVtx = cms.Sequence(process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx+process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonNoVtx)


process.HLTIterL3muonTkCandidateSequenceNoVtx = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTDoLocalStripOnDemandSequence+process.HLTIterL3OIAndIOFromL2muonTkCandidateSequenceNoVtx+process.hltIterL3MuonL1MuonNoL2SelectorNoVtx+process.HLTIterL3IOmuonFromL1TkCandidateSequenceNoVtx)


process.HLTL3muonrecoNocandSequenceNoVtx = cms.Sequence(process.HLTIterL3muonTkCandidateSequenceNoVtx+process.hltIterL3MuonMergedNoVtx+process.hltIterL3MuonAndMuonFromL1MergedNoVtx+process.hltL3MuonsIterL3LinksNoVtx+process.hltIterL3MuonsNoVtx)


process.HLTL3muonrecoSequenceNoVtx = cms.Sequence(process.HLTL3muonrecoNocandSequenceNoVtx+process.hltIterL3MuonCandidatesNoVtx)


process.HLTDoubleMuonScoutingNoVtx = cms.Sequence(process.hltL1fL1sL1DoubleMuonScouting+process.HLTL2muonrecoSequenceNoVtx+process.hltL2fL1sL1DoubleMuonScoutingNoVtx+process.HLTL3muonrecoSequenceNoVtx+process.hltDoubleMuonL3PreFilteredScoutingNoVtx)


process.HLTDoFullUnpackingEgammaEcalWithoutPreshowerSequence = cms.Sequence(process.hltEcalDigisLegacy+process.hltEcalDigisSoA+process.hltEcalDigis+process.hltEcalUncalibRecHitSoA+process.hltEcalUncalibRecHit+process.hltEcalDetIdToBeRecovered+process.hltEcalRecHit)


process.HLTDoLocalHcalSequence = cms.Sequence(process.hltHcalDigis+process.hltHcalDigisSoA+process.hltHbheRecoSoA+process.hltHbhereco+process.hltHfprereco+process.hltHfreco+process.hltHoreco)


process.HLTDoCaloSequencePF = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalWithoutPreshowerSequence+process.HLTDoLocalHcalSequence+process.hltTowerMakerForAll)


process.HLTAK4CaloJetsPrePFRecoSequence = cms.Sequence(process.HLTDoCaloSequencePF+process.hltAK4CaloJetsPF)


process.HLTPreAK4PFJetsRecoSequence = cms.Sequence(process.HLTAK4CaloJetsPrePFRecoSequence+process.hltAK4CaloJetsPFEt5)


process.HLTL2muonrecoSequence = cms.Sequence(process.HLTL2muonrecoNocandSequence+process.hltL2MuonCandidates)


process.HLTIterL3OImuonTkCandidateSequence = cms.Sequence(process.hltIterL3OISeedsFromL2Muons+process.hltIterL3OITrackCandidates+process.hltIterL3OIMuCtfWithMaterialTracks+process.hltIterL3OIMuonTrackCutClassifier+process.hltIterL3OIMuonTrackSelectionHighPurity+process.hltL3MuonsIterL3OI)


process.HLTIterL3MuonRecopixelvertexingSequence = cms.Sequence(process.HLTRecopixelvertexingSequence+process.hltIterL3MuonPixelTracksTrackingRegions+process.hltPixelTracksInRegionL2)


process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence(process.hltIter0IterL3MuonPixelSeedsFromPixelTracks+process.hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered+process.hltIter0IterL3MuonCkfTrackCandidates+process.hltIter0IterL3MuonCtfWithMaterialTracks+process.hltIter0IterL3MuonTrackCutClassifier+process.hltIter0IterL3MuonTrackSelectionHighPurity)


process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence(process.HLTIterL3MuonRecopixelvertexingSequence+process.HLTIterativeTrackingIteration0ForIterL3Muon+process.hltL3MuonsIterL3IO)


process.HLTIterL3OIAndIOFromL2muonTkCandidateSequence = cms.Sequence(process.HLTIterL3OImuonTkCandidateSequence+process.hltIterL3OIL3MuonsLinksCombination+process.hltIterL3OIL3Muons+process.hltIterL3OIL3MuonCandidates+process.hltL2SelectorForL3IO+process.HLTIterL3IOmuonTkCandidateSequence+process.hltIterL3MuonsFromL2LinksCombination)


process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon = cms.Sequence(process.HLTRecopixelvertexingSequence+process.hltIterL3FromL1MuonPixelTracksTrackingRegions+process.hltPixelTracksInRegionL1)


process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence(process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks+process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered+process.hltIter0IterL3FromL1MuonCkfTrackCandidates+process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks+process.hltIter0IterL3FromL1MuonTrackCutClassifier+process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity)


process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon = cms.Sequence(process.hltIter3IterL3FromL1MuonClustersRefRemoval+process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent+process.hltIter3IterL3FromL1MuonPixelLayersAndRegions+process.hltIter3IterL3FromL1MuonTrackingRegions+process.hltIter3IterL3FromL1MuonPixelClusterCheck+process.hltIter3IterL3FromL1MuonPixelHitDoublets+process.hltIter3IterL3FromL1MuonPixelSeeds+process.hltIter3IterL3FromL1MuonPixelSeedsFiltered+process.hltIter3IterL3FromL1MuonCkfTrackCandidates+process.hltIter3IterL3FromL1MuonCtfWithMaterialTracks+process.hltIter3IterL3FromL1MuonTrackCutClassifier+process.hltIter3IterL3FromL1MuonTrackSelectionHighPurity)


process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence(process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon+process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon+process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon)


process.HLTIterL3muonTkCandidateSequence = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTDoLocalStripOnDemandSequence+process.HLTIterL3OIAndIOFromL2muonTkCandidateSequence+process.hltL1MuonsPt0+process.HLTIterL3IOmuonFromL1TkCandidateSequence)


process.HLTL3muonrecoNocandSequence = cms.Sequence(process.HLTIterL3muonTkCandidateSequence+process.hltIter03IterL3FromL1MuonMerged+process.hltIterL3MuonMerged+process.hltIterL3MuonAndMuonFromL1Merged+process.hltIterL3GlbMuon+process.hltIterL3MuonsNoID+process.hltIterL3Muons+process.hltL3MuonsIterL3Links+process.hltIterL3MuonTracks)


process.HLTL3muonrecoSequence = cms.Sequence(process.HLTL3muonrecoNocandSequence+process.hltIterL3MuonCandidates)


process.HLTDoLocalStripSequence = cms.Sequence(process.hltSiStripExcludedFEDListProducer+process.hltSiStripRawToClustersFacility+process.hltMeasurementTrackerEvent)


process.HLTIterativeTrackingIteration0 = cms.Sequence(process.hltIter0PFLowPixelSeedsFromPixelTracks+process.hltIter0PFlowCkfTrackCandidatesMkFitSiPixelHits+process.hltSiStripRecHits+process.hltIter0PFlowCkfTrackCandidatesMkFitSiStripHits+process.hltIter0PFlowCkfTrackCandidatesMkFitEventOfHits+process.hltIter0PFlowCkfTrackCandidatesMkFitSeeds+process.hltIter0PFlowCkfTrackCandidatesMkFit+process.hltIter0PFlowCkfTrackCandidates+process.hltIter0PFlowCtfWithMaterialTracks+process.hltIter0PFlowTrackCutClassifier+process.hltIter0PFlowTrackSelectionHighPurity)


process.HLTIterativeTrackingDoubletRecovery = cms.Sequence(process.hltDoubletRecoveryClustersRefRemoval+process.hltDoubletRecoveryMaskedMeasurementTrackerEvent+process.hltDoubletRecoveryPixelLayersAndRegions+process.hltDoubletRecoveryPFlowPixelClusterCheck+process.hltDoubletRecoveryPFlowPixelHitDoublets+process.hltDoubletRecoveryPFlowPixelSeeds+process.hltDoubletRecoveryPFlowCkfTrackCandidatesMkFitSeeds+process.hltDoubletRecoveryPFlowCkfTrackCandidatesMkFit+process.hltDoubletRecoveryPFlowCkfTrackCandidates+process.hltDoubletRecoveryPFlowCtfWithMaterialTracks+process.hltDoubletRecoveryPFlowTrackCutClassifier+process.hltDoubletRecoveryPFlowTrackSelectionHighPurity)


process.HLTIterativeTrackingIter02 = cms.Sequence(process.HLTIterativeTrackingIteration0+process.HLTIterativeTrackingDoubletRecovery+process.hltMergedTracks)


process.HLTTrackReconstructionForPFNoMu = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTRecopixelvertexingSequence+process.HLTDoLocalStripSequence+process.HLTIterativeTrackingIter02)


process.HLTTrackReconstructionForPF = cms.Sequence(process.HLTTrackReconstructionForPFNoMu+process.hltPFMuonMerging+process.hltMuonLinks+process.hltMuons)


process.HLTPreshowerSequence = cms.Sequence(process.hltEcalPreshowerDigis+process.hltEcalPreshowerRecHit)


process.HLTPFHcalClustering = cms.Sequence(process.hltParticleFlowRecHitHBHESoA+process.hltParticleFlowRecHitHBHE+process.hltParticleFlowClusterHBHESoA+process.hltParticleFlowClusterHBHE+process.hltParticleFlowClusterHCAL)


process.HLTParticleFlowSequence = cms.Sequence(process.HLTPreshowerSequence+process.hltParticleFlowRecHitECALUnseeded+process.hltParticleFlowRecHitHF+process.hltParticleFlowRecHitPSUnseeded+process.hltParticleFlowClusterECALUncorrectedUnseeded+process.hltParticleFlowClusterPSUnseeded+process.hltParticleFlowClusterECALUnseeded+process.HLTPFHcalClustering+process.hltParticleFlowClusterHF+process.hltLightPFTracks+process.hltParticleFlowBlock+process.hltParticleFlow)


process.HLTAK4PFJetsReconstructionSequence = cms.Sequence(process.HLTL2muonrecoSequence+process.HLTL3muonrecoSequence+process.HLTTrackReconstructionForPF+process.HLTParticleFlowSequence+process.hltAK4PFJets+process.hltAK4PFJetsLooseID+process.hltAK4PFJetsTightID)


process.HLTAK4PFCorrectorProducersSequence = cms.Sequence(process.hltAK4PFFastJetCorrector+process.hltAK4PFRelativeCorrector+process.hltAK4PFAbsoluteCorrector+process.hltAK4PFResidualCorrector+process.hltAK4PFCorrector)


process.HLTAK4PFJetsCorrectionSequence = cms.Sequence(process.hltFixedGridRhoFastjetAll+process.HLTAK4PFCorrectorProducersSequence+process.hltAK4PFJetsCorrected+process.hltAK4PFJetsLooseIDCorrected+process.hltAK4PFJetsTightIDCorrected)


process.HLTAK4PFJetsSequence = cms.Sequence(process.HLTPreAK4PFJetsRecoSequence+process.HLTAK4PFJetsReconstructionSequence+process.HLTAK4PFJetsCorrectionSequence)


process.HLTDoFullUnpackingEgammaEcalSequence = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalWithoutPreshowerSequence+process.HLTPreshowerSequence)


process.HLTDoFullUnpackingEgammaEcalMFSequence = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalSequence)


process.HLTPFClusteringEcalMFForMuons = cms.Sequence(process.hltRecHitInRegionForMuonsMF+process.hltRecHitInRegionForMuonsES+process.hltParticleFlowRecHitECALForMuonsMF+process.hltParticleFlowRecHitPSForMuons+process.hltParticleFlowClusterECALUncorrectedForMuonsMF+process.hltParticleFlowClusterPSForMuons+process.hltParticleFlowClusterECALForMuonsMF)


process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalMFSequence+process.HLTDoLocalHcalSequence+process.hltFixedGridRhoFastjetECALMFForMuons+process.hltFixedGridRhoFastjetHCAL+process.HLTPFClusteringEcalMFForMuons+process.hltMuonEcalMFPFClusterIsoForMuons)


process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuons = cms.Sequence(process.HLTPFHcalClustering+process.hltMuonHcalRegPFClusterIsoForMuons)


process.HLTIterativeTrackingL3MuonIteration0 = cms.Sequence(process.hltPixelTracksTrackingRegionsForSeedsL3Muon+process.hltPixelTracksInRegionIter0L3Muon+process.hltIter0L3MuonPixelSeedsFromPixelTracks+process.hltIter0L3MuonCkfTrackCandidates+process.hltIter0L3MuonCtfWithMaterialTracks+process.hltIter0L3MuonTrackCutClassifier+process.hltIter0L3MuonTrackSelectionHighPurity)


process.HLTTrackReconstructionForIsoL3MuonIter02 = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTDoLocalStripOnDemandSequence+process.HLTIterativeTrackingL3MuonIteration0)


process.HLTMuIsolationSequence = cms.Sequence(process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons+process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuons+process.HLTTrackReconstructionForIsoL3MuonIter02+process.hltMuonTkRelIsolationCut0p14Map)


process.HLTPFClusteringForEgammaUnseeded = cms.Sequence(process.hltParticleFlowRecHitECALUnseeded+process.hltParticleFlowRecHitPSUnseeded+process.hltParticleFlowClusterPSUnseeded+process.hltParticleFlowClusterECALUncorrectedUnseeded+process.hltParticleFlowClusterECALUnseeded+process.hltParticleFlowSuperClusterECALUnseeded)


process.HLTFastJetForEgamma = cms.Sequence(process.hltFixedGridRhoFastjetAllCaloForMuons)


process.HLTElePixelMatchUnseededSequence = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTDoLocalStripOnDemandSequence+process.hltPixelLayerPairs+process.hltPixelLayerTriplets+process.hltEgammaHoverEUnseeded+process.hltEgammaSuperClustersToPixelMatchUnseeded+process.hltEleSeedsTrackingRegionsUnseeded+process.hltElePixelHitDoubletsUnseeded+process.hltElePixelHitDoubletsForTripletsUnseeded+process.hltElePixelHitTripletsUnseeded+process.hltElePixelSeedsDoubletsUnseeded+process.hltElePixelSeedsTripletsUnseeded+process.hltElePixelSeedsCombinedUnseeded+process.hltEgammaElectronPixelSeedsUnseeded+process.hltEgammaPixelMatchVarsUnseeded)


process.HLTGsfElectronBestTrkUnseededSequence = cms.Sequence(process.hltEgammaCkfTrackCandidatesForGSFUnseeded+process.hltEgammaGsfTracksUnseeded+process.hltEgammaGsfElectronsUnseeded+process.hltEgammaGsfTrackVarsBestTrkUnseeded)


process.HLTPFScoutingSequence = cms.Sequence(process.HLTAK4PFJetsSequence+process.hltFixedGridRhoFastjetAllCalo+process.hltPFMETProducer+process.HLTMuIsolationSequence+process.HLTDoFullUnpackingEgammaEcalSequence+process.HLTPFClusteringForEgammaUnseeded+process.hltEgammaCandidatesUnseeded+process.hltEgammaCandidatesWrapperUnseeded+process.hltEgammaClusterShapeUnseeded+process.HLTDoLocalHcalSequence+process.HLTFastJetForEgamma+process.hltEgammaHoverEUnseeded+process.hltEgammaEcalPFClusterIsoUnseeded+process.HLTPFHcalClustering+process.hltEgammaHcalPFClusterIsoUnseeded+process.HLTElePixelMatchUnseededSequence+process.HLTGsfElectronBestTrkUnseededSequence+process.hltEgammaEleGsfTrackIsoUnseeded)


process.HLTPFClusteringEcalMFForMuonsNoVtx = cms.Sequence(process.hltRecHitInRegionForMuonsMFnoVtx+process.hltRecHitInRegionForMuonsESNoVtx+process.hltParticleFlowRecHitECALForMuonsMFNoVtx+process.hltParticleFlowRecHitPSForMuonsNoVtx+process.hltParticleFlowClusterECALUncorrectedForMuonsMFNoVtx+process.hltParticleFlowClusterPSForMuonsNoVtx+process.hltParticleFlowClusterECALForMuonsMFNoVtx)


process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuonsNoVtx = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalMFSequence+process.HLTDoLocalHcalSequence+process.hltFixedGridRhoFastjetECALMFForMuons+process.hltFixedGridRhoFastjetHCAL+process.HLTPFClusteringEcalMFForMuonsNoVtx+process.hltMuonEcalMFPFClusterIsoForMuonsNoVtx)


process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuonsNoVtx = cms.Sequence(process.HLTPFHcalClustering+process.hltMuonHcalPFClusterIsoForMuonsNoVtx)


process.HLTIterativeTrackingL3MuonIteration0NoVtx = cms.Sequence(process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx+process.hltPixelTracksInRegionIter0L3MuonNoVtx+process.hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx+process.hltIter0L3MuonCkfTrackCandidatesNoVtx+process.hltIter0L3MuonCtfWithMaterialTracksNoVtx+process.hltIter0L3MuonTrackCutClassifierNoVtx+process.hltIter0L3MuonTrackSelectionHighPurityNoVtx)


process.HLTTrackReconstructionForIsoL3MuonIter02NoVtx = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTDoLocalStripOnDemandSequence+process.HLTIterativeTrackingL3MuonIteration0NoVtx)


process.HLTMuIsolationSequenceNoVtx = cms.Sequence(process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuonsNoVtx+process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuonsNoVtx+process.HLTTrackReconstructionForIsoL3MuonIter02NoVtx+process.hltMuonTkRelIsolationCut0p09MapNoVtx)


process.HLTPFScoutingPackingSequence = cms.Sequence(process.hltScoutingTrackPacker+process.hltScoutingPrimaryVertexPacker+process.hltScoutingPFPacker+process.hltScoutingMuonPackerNoVtx+process.hltScoutingMuonPackerVtx+process.hltScoutingEgammaPacker+process.hltScoutingRecHitPacker)


process.HLTPFScoutingTrackingSequence = cms.Sequence(process.HLTPFScoutingSequence+process.hltEgammaR9IDUnseeded+process.HLTL2muonrecoSequenceNoVtx+process.HLTL3muonrecoSequenceNoVtx+process.hltDisplacedmumuVtxNoMatchingProducerNoVtx+process.hltDisplacedmumuVtxNoMatchingProducerVtx+process.HLTMuIsolationSequenceNoVtx+process.hltFEDSelectorL1+process.HLTPFScoutingPackingSequence)


process.HLTEndSequence = cms.Sequence(process.hltBoolEnd)


process.HLTDoubleMuonScoutingVtx = cms.Sequence(process.hltL1fL1sL1DoubleMuonScouting+process.HLTL2muonrecoSequence+process.hltL2fL1sL1DoubleMuonScouting+process.HLTL3muonrecoSequence+process.hltDoubleMuonL3PreFilteredScoutingVtx)


process.HLTPFClusteringForEgamma = cms.Sequence(process.hltRechitInRegionsECAL+process.hltRechitInRegionsES+process.hltParticleFlowRecHitECALL1Seeded+process.hltParticleFlowRecHitPSL1Seeded+process.hltParticleFlowClusterPSL1Seeded+process.hltParticleFlowClusterECALUncorrectedL1Seeded+process.hltParticleFlowClusterECALL1Seeded+process.hltParticleFlowSuperClusterECALL1Seeded)


process.HLTDoubleEG11CaloIdLSequence = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalSequence+process.HLTPFClusteringForEgamma+process.hltEgammaCandidates+process.hltEGL1DoubleIsoEG11Filter+process.hltDoubleEG11CaloIdLEt11Filter+process.hltEgammaClusterShape+process.hltDoubleEG11CaloIdLClusterShapeFilter+process.HLTDoLocalHcalSequence+process.HLTFastJetForEgamma+process.hltEgammaHoverE+process.hltDoubleEG11CaloIdLHEFilter)


process.HLTTrackReconstructionForIsoForPhotons = cms.Sequence(process.HLTPreAK4PFJetsRecoSequence+process.HLTTrackReconstructionForPFNoMu)


process.HLTPhoton30EBTightIDTightIsoSequence = cms.Sequence(process.HLTDoFullUnpackingEgammaEcalSequence+process.HLTPFClusteringForEgamma+process.hltEgammaCandidates+process.hltEGL1SingleEGOrFilter+process.hltEG30EBTightIDTightIsoEtFilter+process.hltEgammaClusterShape+process.hltEG30EBTightIDTightIsoClusterShapeFilter+process.HLTDoLocalHcalSequence+process.HLTFastJetForEgamma+process.hltEgammaHoverE+process.hltEG30EBTightIDTightIsoHEFilter+process.hltEgammaR9ID+process.hltEG30EBTightIDTightIsoR9Filter+process.hltEgammaEcalPFClusterIsoDr0p2+process.hltEG30EBTightIDTightIsotEcalIsoFilter+process.HLTPFHcalClustering+process.hltEgammaHcalPFClusterIso+process.hltEG30EBTightIDTightIsoHcalIsoFilter+process.HLTTrackReconstructionForIsoForPhotons+process.hltEgammaHollowTrackIsoDr0p2+process.hltEG30EBTightIDTightIsoTrackIsoFilter)


process.HLTMu24IsolationSequence = cms.Sequence(process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons+process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFiltered+process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuons+process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFiltered+process.HLTTrackReconstructionForIsoL3MuonIter02+process.hltMuonTkRelIsolationCut0p14Map)


process.HLTL3muontrkisorecoSequence = cms.Sequence(process.HLTDoLocalPixelSequence+process.HLTDoLocalStripOnDemandSequence+process.HLTIterativeTrackingL3MuonIteration0)


process.HLTL3muontrkisovvlSequence = cms.Sequence(process.HLTL3muontrkisorecoSequence+process.hltL3MuonRelTrkIsolationVVL)


process.HLTBeginSequenceTestData = cms.Sequence(process.HLTL1UnpackerSequence)


process.HLTDatasetPathBeginSequence = cms.Sequence(process.hltGtStage2Digis)


process.SimL1Emulator = cms.Sequence(process.SimL1EmulatorTask)


process.DST_PFScouting_DoubleMuonNoVtx_v4 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleMuonPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleMuonNoVtx+process.HLTDoubleMuonScoutingNoVtx+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_DoubleMuonVtx_v4 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleMuonPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleMuonVtx+process.HLTDoubleMuonScoutingVtx+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_DoubleMuonVtxMonitorJPsi_v4 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleMuonPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleMuonVtxMonitorJPsi+process.HLTDoubleMuonScoutingVtx+process.hltDoubleMuScoutingMonitorJPsiL3Filtered+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_DoubleMuonVtxMonitorZ_v4 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleMuonPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleMuonVtxMonitorZ+process.HLTDoubleMuonScoutingVtx+process.hltDoubleMuScoutingMonitorZL3Filtered+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_DoubleEG_v10 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleEGPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleEG+process.HLTDoubleEG11CaloIdLSequence+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_DoubleEGMonitorJPsi_v1 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleEGPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleEGMonitorJPsi+process.HLTDoubleEG11CaloIdLSequence+process.hltDoubleEGScoutingMonitorJPsiFilter+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_DoubleEGMonitorZ_v1 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3DoubleEGPFScoutingPixelTracking+process.hltPreDSTPFScoutingDoubleEGMonitorZ+process.HLTDoubleEG11CaloIdLSequence+process.hltDoubleEGScoutingMonitorZFilter+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_SinglePhotonEBMonitorJPsi_v1 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sSingleEGor+process.hltPreDSTPFScoutingSinglePhotonEBMonitorJPsi+process.HLTPhoton30EBTightIDTightIsoSequence+process.HLTPFScoutingTrackingSequence+process.hltDiEG5TightIDMWEtUnseededFilter+process.hltSinglePhotonEBScoutingMonitorJPsiFilter+process.HLTEndSequence)


process.DST_PFScouting_SinglePhotonEBMonitorZ_v1 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sSingleEGor+process.hltPreDSTPFScoutingSinglePhotonEBMonitorZ+process.HLTPhoton30EBTightIDTightIsoSequence+process.HLTPFScoutingTrackingSequence+process.hltDiEG5TightIDMWEtUnseededFilter+process.hltSinglePhotonEBScoutingMonitorZFilter+process.HLTEndSequence)


process.DST_PFScouting_JetHT_v10 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3JetHTPFScoutingPixelTracking+process.hltPreDSTPFScoutingJetHT+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_AXOVLoose_v8 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3AXOVLoosePFScoutingTracking+process.hltPreDSTPFScoutingAXOVLoose+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_AXOLoose_v8 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3AXOLoosePFScoutingTracking+process.hltPreDSTPFScoutingAXOLoose+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_AXOMedium_v4 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3AXOMediumPFScoutingTracking+process.hltPreDSTPFScoutingAXOMedium+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_AXOTight_v10 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3AXOTightPFScoutingTracking+process.hltPreDSTPFScoutingAXOTight+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_AXOVTight_v8 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3AXOVTightPFScoutingTracking+process.hltPreDSTPFScoutingAXOVTight+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_CICADAVLoose_v6 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3CICADAVLoosePFScoutingTracking+process.hltPreDSTPFScoutingCICADAVLoose+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_CICADALoose_v6 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3CICADALoosePFScoutingTracking+process.hltPreDSTPFScoutingCICADALoose+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_CICADAMedium_v6 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3CICADAMediumPFScoutingTracking+process.hltPreDSTPFScoutingCICADAMedium+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_CICADATight_v6 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3CICADATightPFScoutingTracking+process.hltPreDSTPFScoutingCICADATight+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_CICADAVTight_v6 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDSTRun3CICADAVTightPFScoutingTracking+process.hltPreDSTPFScoutingCICADAVTight+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_SingleMuon_v10 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sSingleMuScouting+process.hltPreDSTPFScoutingSingleMuon+process.hltL1fL1sMuScoutingL1Filtered0+process.HLTL2muonrecoSequence+cms.ignore(process.hltL2fL1sMuScoutingL2Filtered0)+process.HLTL3muonrecoSequence+cms.ignore(process.hltL1fForIterL3L1fL1sMuScoutingL1Filtered0)+process.hltL3fL1sMuScoutingL3Filtered0+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_SinglePhotonEB_v7 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sSingleEGor+process.hltPreDSTPFScoutingSinglePhotonEB+process.HLTPhoton30EBTightIDTightIsoSequence+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.DST_PFScouting_ZeroBias_v8 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sZeroBias+process.hltPreDSTPFScoutingZeroBias+process.HLTPFScoutingTrackingSequence+process.HLTEndSequence)


process.HLT_IsoMu24_v29 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sSingleMu22+process.hltPreIsoMu24+process.hltL1fL1sMu22L1Filtered0+process.HLTL2muonrecoSequence+cms.ignore(process.hltL2fL1sSingleMu22L1f0L2Filtered10Q)+process.HLTL3muonrecoSequence+cms.ignore(process.hltL1fForIterL3L1fL1sMu22L1Filtered0)+process.hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q+process.HLTMu24IsolationSequence+process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered+process.HLTEndSequence)


process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v31 = cms.Path(process.SimL1Emulator+process.HLTBeginSequence+process.hltL1sDoubleMu125to157+process.hltPreMu17TrkIsoVVLMu8TrkIsoVVLDZ+process.hltL1fL1sDoubleMu155L1Filtered0+process.HLTL2muonrecoSequence+cms.ignore(process.hltL2pfL1sDoubleMu155L1f0L2PreFiltered0)+cms.ignore(process.hltL2fL1sDoubleMu155L1f0L2Filtered10OneMu)+process.HLTL3muonrecoSequence+cms.ignore(process.hltL1fForIterL3L1fL1sDoubleMu155L1Filtered0)+process.hltL3fL1DoubleMu155fPreFiltered8+process.hltL3fL1DoubleMu155fFiltered17+process.HLTL3muontrkisovvlSequence+process.hltDiMuon178RelTrkIsoVVLFiltered+process.hltDiMuon178RelTrkIsoVVLFilteredDzFiltered0p2+process.HLTEndSequence)


process.HLT_TestData_v1 = cms.Path(process.SimL1Emulator+process.HLTBeginSequenceTestData+process.hltPreTestData+process.HLTEndSequence)


process.HLTriggerFinalPath = cms.Path(process.SimL1Emulator+process.hltGtStage2Digis+process.hltTriggerSummaryAOD+process.hltTriggerSummaryRAW+process.hltBoolFalse)


process.Dataset_TestDataRaw = cms.Path(process.SimL1Emulator+process.HLTDatasetPathBeginSequence+process.hltDatasetTestDataRaw+process.hltPreDatasetTestDataRaw)


process.Dataset_TestDataScouting = cms.Path(process.SimL1Emulator+process.HLTDatasetPathBeginSequence+process.hltDatasetTestDataScouting+process.hltPreDatasetTestDataScouting)


process.LocalTestDataRawOutput = cms.EndPath(process.SimL1Emulator+process.hltOutputLocalTestDataRaw)


process.LocalTestDataScoutingOutput = cms.EndPath(process.SimL1Emulator+process.hltOutputLocalTestDataScouting)


process.DQMOutput = cms.EndPath(process.dqmOutput)


process.schedule = cms.Schedule(*[ process.DST_PFScouting_DoubleMuonNoVtx_v4, process.DST_PFScouting_DoubleMuonVtx_v4, process.DST_PFScouting_DoubleMuonVtxMonitorJPsi_v4, process.DST_PFScouting_DoubleMuonVtxMonitorZ_v4, process.DST_PFScouting_DoubleEG_v10, process.DST_PFScouting_DoubleEGMonitorJPsi_v1, process.DST_PFScouting_DoubleEGMonitorZ_v1, process.DST_PFScouting_SinglePhotonEBMonitorJPsi_v1, process.DST_PFScouting_SinglePhotonEBMonitorZ_v1, process.DST_PFScouting_JetHT_v10, process.DST_PFScouting_AXOVLoose_v8, process.DST_PFScouting_AXOLoose_v8, process.DST_PFScouting_AXOMedium_v4, process.DST_PFScouting_AXOTight_v10, process.DST_PFScouting_AXOVTight_v8, process.DST_PFScouting_CICADAVLoose_v6, process.DST_PFScouting_CICADALoose_v6, process.DST_PFScouting_CICADAMedium_v6, process.DST_PFScouting_CICADATight_v6, process.DST_PFScouting_CICADAVTight_v6, process.DST_PFScouting_SingleMuon_v10, process.DST_PFScouting_SinglePhotonEB_v7, process.DST_PFScouting_ZeroBias_v8, process.HLT_IsoMu24_v29, process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v31, process.HLT_TestData_v1, process.HLTriggerFinalPath, process.Dataset_TestDataRaw, process.Dataset_TestDataScouting, process.LocalTestDataRawOutput, process.LocalTestDataScoutingOutput, process.DQMOutput ])

