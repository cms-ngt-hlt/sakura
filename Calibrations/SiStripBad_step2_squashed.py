# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: expressStep2 --conditions 140X_dataRun3_Express_v3 -s RAW2DIGI,RECO:trackerlocalreco,ALCA:SiStripCalZeroBias+SiStripPCLHistos+PromptCalibProdSiStrip --datatier ALCARECO --eventcontent ALCARECO --data --process RECO --scenario pp --era Run3 --customise Configuration/DataProcessing/RecoTLR.customiseExpress -n -1 --filein file:repacked_0.root,file:repacked_1.root,file:repacked_10.root,file:repacked_11.root,file:repacked_12.root,file:repacked_13.root,file:repacked_14.root,file:repacked_15.root,file:repacked_16.root,file:repacked_17.root,file:repacked_18.root,file:repacked_19.root,file:repacked_2.root,file:repacked_20.root,file:repacked_3.root,file:repacked_4.root,file:repacked_5.root,file:repacked_6.root,file:repacked_7.root,file:repacked_8.root,file:repacked_9.root --fileout file:step2.root --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3


process = cms.Process('RECO',Run3)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')
process.load('Configuration.StandardSequences.AlCaRecoStreams_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('HLTrigger.Timer.FastTimerService_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:repacked_0.root',
        'file:repacked_1.root',
        'file:repacked_10.root',
        'file:repacked_11.root',
        'file:repacked_12.root',
        'file:repacked_13.root',
        'file:repacked_14.root',
        'file:repacked_15.root',
        'file:repacked_16.root',
        'file:repacked_17.root',
        'file:repacked_18.root',
        'file:repacked_19.root',
        'file:repacked_2.root',
        'file:repacked_20.root',
        'file:repacked_3.root',
        'file:repacked_4.root',
        'file:repacked_5.root',
        'file:repacked_6.root',
        'file:repacked_7.root',
        'file:repacked_8.root',
        'file:repacked_9.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
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
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('expressStep2 nevts:-1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition
process.ALCARECOStreamPromptCalibProdSiStrip = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pathALCARECOPromptCalibProdSiStrip')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('PromptCalibProdSiStrip')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('PromptCalibProdSiStrip.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_MEtoEDMConvertSiStrip_*_*'
    )
)
process.ALCARECOStreamSiStripCalZeroBias = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pathALCARECOSiStripCalZeroBias')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('SiStripCalZeroBias')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('SiStripCalZeroBias.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_ALCARECOSiStripCalZeroBias_*_*',
        'keep *_calZeroBiasClusters_*_*',
        'keep L1AcceptBunchCrossings_*_*_*',
        'keep *_TriggerResults_*_*'
    )
)
process.ALCARECOStreamSiStripPCLHistos = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('pathALCARECOSiStripPCLHistos')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('SiStripPCLHistos')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('SiStripPCLHistos.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_MEtoEDMConvertSiStrip_*_*'
    )
)

# Other statements
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiStripCalZeroBias_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOPromptCalibProdSiStrip_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiStripPCLHistos_noDrop.outputCommands)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '140X_dataRun3_Express_v3', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.trackerlocalreco)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.ALCARECOStreamPromptCalibProdSiStripOutPath = cms.EndPath(process.ALCARECOStreamPromptCalibProdSiStrip)
process.ALCARECOStreamSiStripCalZeroBiasOutPath = cms.EndPath(process.ALCARECOStreamSiStripCalZeroBias)
process.ALCARECOStreamSiStripPCLHistosOutPath = cms.EndPath(process.ALCARECOStreamSiStripPCLHistos)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.pathALCARECOSiStripCalZeroBias,process.pathALCARECOPromptCalibProdSiStrip,process.pathALCARECOSiStripPCLHistos,process.endjob_step,process.ALCARECOStreamPromptCalibProdSiStripOutPath,process.ALCARECOStreamSiStripCalZeroBiasOutPath,process.ALCARECOStreamSiStripPCLHistosOutPath)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from Configuration.DataProcessing.RecoTLR
from Configuration.DataProcessing.RecoTLR import customiseExpress 

#call to customisation function customiseExpress imported from Configuration.DataProcessing.RecoTLR
process = customiseExpress(process)

# End of customisation functions


# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

process.options.numberOfStreams = 8
process.options.numberOfThreads = 8


process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_squashed_v1.json"
