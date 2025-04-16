import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from FWCore.ParameterSet.Types import PSet

options = VarParsing.VarParsing('analysis')

#options.register('runNumber', 386593, # 1 is for MC
options.register('runNumber', 389891, # 1 is for MC
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Run number")

#options.register('numThreads', 1,
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.int,
#                 "Number of threads")
#
#options.register('numStreams', 0,
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.int,
#                 "Number of CMSSW streams")

options.register('buBaseDir', './tmp/BU0', # '/fff/BU0', # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "BU base directory")

options.register('dataDir', './tmp', # '/fff/BU0/ramdisk', # default value (on standalone FU)
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "BU data write directory")

options.register('sourceLabel', 'rawDataCollector', # default value (regular pp data)
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "FEDRawDataCollection label")

options.register ('frdFileVersion',
                  1,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Generate raw files with FRD file header with version 1 or separate JSON files with 0")

# DQM Input options
#options.register('runInputDir',
#                 '/tmp',
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.string,
#                 "Directory where the DQM files will appear.")
#
#options.register('eventsPerLS',
#                 35,
#                  VarParsing.VarParsing.multiplicity.singleton,
#                  VarParsing.VarParsing.varType.int,          # string, int, or float
#                  "Max LS to generate (0 to disable limit)")                 
#
#options.register ('maxLS',
#                  2,
#                  VarParsing.VarParsing.multiplicity.singleton,
#                  VarParsing.VarParsing.varType.int,          # string, int, or float
#                  "Max LS to generate (0 to disable limit)")


options.setDefault('maxEvents', -1)

options.parseArguments()

process = cms.Process("TESTCONVERSION")

#process.options.numberOfThreads = options.numThreads
#process.options.numberOfStreams = options.numStreams
#
#noConcurrentLumiBlocks = process.options.numberOfStreams > 1
#noConcurrentLumiBlocks |= (process.options.numberOfStreams == 0 and process.options.numberOfThreads > 1)
#if noConcurrentLumiBlocks:
#    process.options.numberOfConcurrentLuminosityBlocks = 1

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(options.maxEvents)
)

process.MessageLogger = cms.Service("MessageLogger",
  destinations = cms.untracked.vstring('cout'),
cout = cms.untracked.PSet(threshold = cms.untracked.string('INFO'))
)

#process.MessageLogger = cms.Service("MessageLogger",
#  destinations = cms.untracked.vstring( 'cout' ),
#  cout = cms.untracked.PSet(
#    FwkReport = cms.untracked.PSet(
#      reportEvery = cms.untracked.int32(-1),
#      optionalPSet = cms.untracked.bool(True),
##      limit = cms.untracked.int32(10000000)
#    ),
#    threshold = cms.untracked.string( "INFO" ),
#  ),
#)

process.source = cms.Source("NewEventStreamFileReader", # T0 source (streamer .dat)
  fileNames = cms.untracked.vstring(options.inputFiles)
)

#process.source = cms.Source("DQMStreamerReader", # DQM source (streamer .dat)
#        runNumber = cms.untracked.uint32(options.runNumber),
#        runInputDir = cms.untracked.string(options.runInputDir),
#        streamLabel = cms.untracked.string('streamDQM'),
#        scanOnce = cms.untracked.bool(True),
#        minEventsPerLumi = cms.untracked.int32(1),
#        delayMillis = cms.untracked.uint32(500),
#        nextLumiTimeoutMillis = cms.untracked.int32(0),
#        skipFirstLumis = cms.untracked.bool(False),
#        deleteDatFiles = cms.untracked.bool(False),
#        endOfRunKills  = cms.untracked.bool(False),
#        inputFileTransitionsEachEvent = cms.untracked.bool(False),
#        SelectEvents = cms.untracked.vstring("HLT*Mu*","HLT_*Physics*")

# DAQ source:
#  - The input data is converted into the FRD (FED Raw Data) format
#    using the EvFDaqDirector service and the RawStreamFileWriterForBU output module
#  - The new DAQ file broker (file locking schema) is enabled (EvFDaqDirector.useFileBroker = True)
#    via the DAQ patch (hltDAQPatch.py) and ran using the bufu_filebroker systemd service

process.EvFDaqDirector = cms.Service("EvFDaqDirector",
  runNumber = cms.untracked.uint32(options.runNumber),
  baseDir = cms.untracked.string(options.dataDir),
  buBaseDir = cms.untracked.string(options.buBaseDir),
  directorIsBU = cms.untracked.bool(True),
  useFileBroker = cms.untracked.bool(False), # NOTE: no need for file broker?
  fileBrokerHost = cms.untracked.string("")
  #hltSourceDirectory = cms.untracked.string("/tmp/hlt/"), # HLTD picks up HLT configuration and fffParameters.jsn from hltSourceDirectory (copied by newHiltonMenu.py)
)

process.out = cms.OutputModule("RawStreamFileWriterForBU", # DAQ FRD (.raw)
  source = cms.InputTag(options.sourceLabel), # default = "rawDataCollector"
  numEventsPerFile = cms.uint32(100),
  frdVersion = cms.uint32(6),
  frdFileVersion = cms.uint32(options.frdFileVersion) # default = 1
)

#process.a = cms.EDAnalyzer("ExceptionGenerator",
#  defaultAction = cms.untracked.int32(0),
#  defaultQualifier = cms.untracked.int32(10)
#)
#
#process.p = cms.Path(process.a)

process.endpath = cms.EndPath(process.out)

##make a list of all the EventIDs that were seen by the previous job,
## given the filter is semi-random we do not know which of these will
## be the actual first event written
#rn = options.runNumber
#transitions = [cms.EventID(rn,0,0)]
#evid = 1
#for lumi in range(1, options.maxLS+1):
#    transitions.append(cms.EventID(rn,lumi,0))
#    for ev in range(0, options.eventsPerLS):
#        transitions.append(cms.EventID(rn,lumi,evid))
#        evid += 1
#    transitions.append(cms.EventID(rn,lumi,0)) #end lumi
#transitions.append(cms.EventID(rn,0,0)) #end run
#
#
##only see 1 event as process.source.minEventsPerLumi == 1
#process.test = cms.EDAnalyzer("RunLumiEventChecker",
#                              eventSequence = cms.untracked.VEventID(*transitions),
#                              unorderedEvents = cms.untracked.bool(True),
#                              minNumberOfEvents = cms.untracked.uint32(1+2+2),
#                              maxNumberOfEvents = cms.untracked.uint32(1+2+2)
#)
#if options.eventsPerLS == 0:
#    process.test.eventSequence = []
#    process.test.minNumberOfEvents = 0
#    process.test.maxNumberOfEvents = 0
#
#process.p = cms.Path(process.test)
