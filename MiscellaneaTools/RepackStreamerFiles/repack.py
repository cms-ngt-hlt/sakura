import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.parseArguments()

process = cms.Process( 'REPACK' )

process.source = cms.Source("NewEventStreamFileReader", # T0 source (streamer .dat)
                                                     fileNames = cms.untracked.vstring(options.inputFiles))

process.output = cms.OutputModule( 'PoolOutputModule',
    fileName = cms.untracked.string( 'repacked.root' ),
    outputCommands = cms.untracked.vstring( 'keep *' )
)

process.endPath = cms.EndPath( process.output )


