# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step4 --conditions 150X_dataRun3_Express_v1 -s ALCAHARVEST:EcalPedestals --scenario pp --data --filein file:PromptCalibProdEcalPedestals.root -n -1 --no_exec
import FWCore.ParameterSet.Config as cms



process = cms.Process('ALCAHARVEST')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.AlCaHarvesting_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:PromptCalibProdEcalPedestals.root'),
    processingMode = cms.untracked.string('RunsAndLumis'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring('ProductNotFound'),
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
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step4 nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
process.PoolDBOutputService.toPut.append(process.ALCAHARVESTEcalPedestals_dbOutput)
process.pclMetadataWriter.recordsToMap.append(process.ALCAHARVESTEcalPedestals_metadata)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_Express_v1', '')

# Path and EndPath definitions
process.ALCAHARVESTDQMSaveAndMetadataWriter = cms.Path(process.dqmSaver+process.pclMetadataWriter)
process.BeamSpotByLumi = cms.Path(process.ALCAHARVESTBeamSpotByLumi)
process.BeamSpotByRun = cms.Path(process.ALCAHARVESTBeamSpotByRun)
process.BeamSpotHPByLumi = cms.Path(process.ALCAHARVESTBeamSpotHPByLumi)
process.BeamSpotHPByRun = cms.Path(process.ALCAHARVESTBeamSpotHPByRun)
process.BeamSpotHPLowPUByLumi = cms.Path(process.ALCAHARVESTBeamSpotHPLowPUByLumi)
process.BeamSpotHPLowPUByRun = cms.Path(process.ALCAHARVESTBeamSpotHPLowPUByRun)
process.EcalPedestals = cms.Path(process.ALCAHARVESTEcalPedestals)
process.LumiPCC = cms.Path(process.ALCAHARVESTLumiPCC)
process.PPSAlignment = cms.Path(process.ALCAHARVESTPPSAlignment)
process.PPSDiamondSampicTimingCalibration = cms.Path(process.ALCAHARVESTPPSDiamondSampicTimingCalibration)
process.PPSTimingCalibration = cms.Path(process.ALCAHARVESTPPSTimingCalibration)
process.SiPixelAli = cms.Path(process.ALCAHARVESTSiPixelAli)
process.SiPixelAliHG = cms.Path(process.ALCAHARVESTSiPixelAliHG)
process.SiPixelAliHGCombined = cms.Path(process.ALCAHARVESTSiPixelAliHGCombined)
process.SiPixelAliHLTHGCombined = cms.Path(process.ALCAHARVESTSiPixelAliHLTHGCombined)
process.SiPixelLA = cms.Path(process.ALCAHARVESTSiPixelLorentzAngle)
process.SiPixelLAMCS = cms.Path(process.ALCAHARVESTSiPixelLorentzAngleMCS)
process.SiPixelQuality = cms.Path(process.dqmEnvSiPixelQuality+process.ALCAHARVESTSiPixelQuality)
process.SiStripGains = cms.Path(process.ALCAHARVESTSiStripGains)
process.SiStripGainsAAG = cms.Path(process.ALCAHARVESTSiStripGainsAAG)
process.SiStripHitEff = cms.Path(process.ALCAHARVESTSiStripHitEfficiency)
process.SiStripLA = cms.Path(process.ALCAHARVESTSiStripLorentzAngle)
process.SiStripQuality = cms.Path(process.ALCAHARVESTSiStripQuality)

# Schedule definition
process.schedule = cms.Schedule(process.EcalPedestals,process.ALCAHARVESTDQMSaveAndMetadataWriter)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)



# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
