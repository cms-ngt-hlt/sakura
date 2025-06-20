# Convert the streamer (.dat) files into FRD (.raw) DAQ format
#
# usage: cmsRun convertStreamerToRaw.py \
#           inputFiles=/store/path/file.root[,/store/path/file.root,...] \
#           runNumber=NNNNNN \
#           [lumiNumber=NNNN] \
#           [eventsPerFile=100] \
#           [eventsPerLumi=11650] \
#           [rawDataCollection=rawDataCollector] \
#           [outputPath=output_directory]
#
# The output files will appear as output_directory/runNNNNNN/runNNNNNN_lumiNNNN_indexNNNNNN.raw .

import sys, os
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')

options.register('runNumber', 
                 0, # 1 is for MC
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Run number")

options.register('numThreads', 
                 1,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of threads")

options.register('numStreams',
                 0,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Number of CMSSW streams")

#options.register('lumiNumber',
#                 None,
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.int,
#                 "Luminosity section number to use")

#options.register('eventsPerLumi',
#                 11650,
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.int,
#                 "Number of events in the given luminosity section to process")

options.register('eventsPerFile',
                 100,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Split the output into files with at most this number of events")

options.register('rawDataCollection',
                 'rawDataCollector', # regular pp data
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "FEDRawDataCollection to be repacked into RAW format")

options.register ('frdFileVersion',
                  1,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.int,          # string, int, or float
                  "Generate raw files with FRD file header with version 1 or separate JSON files with 0")

#options.register('buBaseDir', '/fff/BU0', # default value
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.string,
#                 "BU base directory")

#options.register('dataDir', '/fff/BU0/ramdisk', # default value (on standalone FU)
#                 VarParsing.VarParsing.multiplicity.singleton,
#                 VarParsing.VarParsing.varType.string,
#                 "BU data write directory")

options.register('outputPath',
                 os.getcwd(),
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Output directory for the FED RAW data files")

options.parseArguments()

process = cms.Process("FAKE")

process.options.numberOfThreads = options.numThreads
process.options.numberOfStreams = options.numStreams

noConcurrentLumiBlocks = process.options.numberOfStreams > 1
noConcurrentLumiBlocks |= (process.options.numberOfStreams == 0 and process.options.numberOfThreads > 1)
if noConcurrentLumiBlocks:
    process.options.numberOfConcurrentLuminosityBlocks = 1

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(options.maxEvents)
)

process.MessageLogger = cms.Service("MessageLogger",
  destinations = cms.untracked.vstring('cout'),
  cout = cms.untracked.PSet(threshold = cms.untracked.string('WARNING'))
)

process.source = cms.Source("NewEventStreamFileReader", # T0 source (streamer .dat)
  fileNames = cms.untracked.vstring(options.inputFiles)
)

# DAQ source:
#  - The input data is converted into the FRD (FED Raw Data) format
#    using the EvFDaqDirector service and the RawStreamFileWriterForBU output module
#  - The new DAQ file broker (file locking schema) is enabled (EvFDaqDirector.useFileBroker = True)
#    via the DAQ patch (hltDAQPatch.py) and ran using the bufu_filebroker systemd service

process.EvFDaqDirector = cms.Service("EvFDaqDirector",
  runNumber = cms.untracked.uint32(options.runNumber),
  baseDir = cms.untracked.string(options.outputPath),
  buBaseDir = cms.untracked.string(options.outputPath),
  directorIsBU = cms.untracked.bool(True),
  useFileBroker = cms.untracked.bool(False), # NOTE: no need for file broker
  fileBrokerHost = cms.untracked.string("")
  #hltSourceDirectory = cms.untracked.string("/tmp/hlt/"), # HLTD picks up HLT configuration and fffParameters.jsn from hltSourceDirectory (copied by newHiltonMenu.py)
)

process.out = cms.OutputModule("RawStreamFileWriterForBU", # DAQ FRD (.raw)
  source = cms.InputTag(options.rawDataCollection), # default: "rawDataCollector"
  numEventsPerFile = cms.uint32(options.eventsPerFile),
  frdVersion = cms.uint32(6),
  frdFileVersion = cms.uint32(options.frdFileVersion) # default: 1
)

process.endpath = cms.EndPath(process.out)
