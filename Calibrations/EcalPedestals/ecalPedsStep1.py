# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: expressStep2 --conditions 150X_dataRun3_Express_v2 -s RAW2DIGI,RECO,ALCAPRODUCER:EcalTestPulsesRaw --datatier ALCARECO --eventcontent ALCARECO --data --process RERECO --scenario pp --era Run3 --nThreads 8 --nStreams 8 -n -1 --filein file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/08c7417b-a4d3-4004-a785-e38d9df48d5e.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/0ba3316e-fbd4-4767-9275-84cd1c5cee1f.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/0e227091-056b-47f7-b6b7-d31f623fc3f4.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/147152d7-c821-4e33-a180-c133c0270d22.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/1fb33687-b976-40cb-9aef-35baad55606d.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/203a09b3-daa9-4a59-a086-a61dcc4cf788.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/21d0637c-890b-4073-a873-de6d9af504c7.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/23fd734d-2c42-44aa-a7be-ed74bd2ce61a.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/2e91c812-816c-4d23-8eb8-c062fbbeda87.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/357b1b01-a697-4def-953b-728288fc5280.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/4c3d641f-cdeb-47fc-818b-bd17e273b113.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/503647f7-b2a3-4997-8a0d-c0bf8f708efa.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/551ff755-c2dd-4c91-9b63-ba1c28188b0d.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/6200c897-bb3f-45e2-8615-c91c8b97a433.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/8542ea44-46cb-482b-b44d-46f4815ca142.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/8918a4e7-e77d-4881-abd1-584d3c3910f7.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/a33837fd-e0d7-4c7f-a965-56ca7b4efb1a.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/ab47024b-ad0a-49e5-b4a8-ed6e545737a3.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/ae3f96da-43f6-4f70-a077-2831ee2e51b2.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/c5ec754e-c7da-40ce-b760-31664ddea76b.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/c7587d48-f502-40b2-8ad4-267afea870c8.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/d3aa42f7-b974-4643-b3b7-e22a7c04532f.root,file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/e37d178a-dd24-4083-8b0a-ecc34fb33bd7.root, --fileout file:step2.root --no_exec --python_filename ecalPedsStep1.py
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3

process = cms.Process('RERECO',Run3)

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

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/08c7417b-a4d3-4004-a785-e38d9df48d5e.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/0ba3316e-fbd4-4767-9275-84cd1c5cee1f.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/0e227091-056b-47f7-b6b7-d31f623fc3f4.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/147152d7-c821-4e33-a180-c133c0270d22.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/1fb33687-b976-40cb-9aef-35baad55606d.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/203a09b3-daa9-4a59-a086-a61dcc4cf788.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/21d0637c-890b-4073-a873-de6d9af504c7.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/23fd734d-2c42-44aa-a7be-ed74bd2ce61a.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/2e91c812-816c-4d23-8eb8-c062fbbeda87.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/357b1b01-a697-4def-953b-728288fc5280.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/4c3d641f-cdeb-47fc-818b-bd17e273b113.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/503647f7-b2a3-4997-8a0d-c0bf8f708efa.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/551ff755-c2dd-4c91-9b63-ba1c28188b0d.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/6200c897-bb3f-45e2-8615-c91c8b97a433.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/8542ea44-46cb-482b-b44d-46f4815ca142.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/8918a4e7-e77d-4881-abd1-584d3c3910f7.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/a33837fd-e0d7-4c7f-a965-56ca7b4efb1a.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/ab47024b-ad0a-49e5-b4a8-ed6e545737a3.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/ae3f96da-43f6-4f70-a077-2831ee2e51b2.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/c5ec754e-c7da-40ce-b760-31664ddea76b.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/c7587d48-f502-40b2-8ad4-267afea870c8.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/d3aa42f7-b974-4643-b3b7-e22a7c04532f.root',
        'file:/eos/cms/store/data/Run2025F/TestEnablesEcalHcal/RAW/Express-v1/000/397/621/00000/e37d178a-dd24-4083-8b0a-ecc34fb33bd7.root',
        ''
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

process.ALCARECOoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('ALCARECO'),
        filterName = cms.untracked.string('StreamALCACombined')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:step2.root'),
    outputCommands = process.ALCARECOEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOEcalTestPulsesRaw_noDrop.outputCommands)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_Express_v2', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.ALCARECOoutput_step = cms.EndPath(process.ALCARECOoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.pathALCARECOEcalTestPulsesRaw,process.endjob_step,process.ALCARECOoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

#Setup FWK for multithreaded
process.options.numberOfThreads = 8
process.options.numberOfStreams = 8



# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
process.load('HLTrigger.Timer.FastTimerService_cfi')
process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_ECALpeds.json"
