# Auto generated configuration file using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: expressStep2 --conditions 140X_dataRun3_Express_v3 -s RAW2DIGI,RECO,ALCAPRODUCER:SiStripPCLHistos+SiStripCalZeroBias+SiStripCalMinBias+SiStripCalMinBiasAAG+TkAlMinBias+SiPixelCalZeroBias+SiPixelCalSingleMuon+SiPixelCalSingleMuonTight+TkAlZMuMu --datatier ALCARECO --eventcontent ALCARECO --data --process RECO --scenario pp --era Run3 --customise Configuration/DataProcessing/RecoTLR.customiseExpress -n -1 --fileout file:step2.root --no_exec
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

jobNumber = 0
outputFileName = "file:output.root" # Cannot directly output to EOS
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(40000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)
eventsToSkip = jobNumber*40000

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0001_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0002_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0003_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0004_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0005_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0006_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0007_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0008_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0009_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0010_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0011_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0012_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0013_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0014_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0015_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0016_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0017_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0018_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0019_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0020_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0021_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0022_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0023_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0024_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0025_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0026_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0027_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0028_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0029_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0030_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0031_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0032_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0033_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0034_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0035_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0036_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0037_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0038_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0039_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0040_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0041_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0042_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0043_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0044_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0045_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0046_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0047_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0048_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0049_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0050_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0051_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0052_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0053_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0054_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0055_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0056_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0057_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0058_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0059_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0060_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0061_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0062_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0063_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0064_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0065_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0066_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0067_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0068_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0069_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0070_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0071_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0072_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0073_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0074_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0075_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0076_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0077_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0078_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0079_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0080_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0081_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0082_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0083_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0084_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0085_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0086_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0087_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0088_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0089_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0090_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0091_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0092_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0093_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0094_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0095_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0096_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0097_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0098_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0099_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0100_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0101_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0102_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0103_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0104_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0105_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0106_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0107_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0108_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0109_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0110_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0111_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0112_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0113_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0114_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0115_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0116_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0117_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0118_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0119_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0120_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0121_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0122_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0123_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0124_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0125_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0126_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0127_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0128_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0129_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0130_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0131_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0132_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0133_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0134_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0135_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0136_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0137_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0138_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0139_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0140_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0141_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0142_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0143_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0144_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0145_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0146_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0147_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0148_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0149_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0150_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0151_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0152_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0153_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0154_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0155_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0156_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0157_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0158_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0159_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0160_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0161_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0162_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0163_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0164_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0165_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0166_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0167_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0168_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0169_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0170_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0171_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0172_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0173_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0174_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0175_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0176_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0177_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0178_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0179_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0180_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0181_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0182_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0183_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0184_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0185_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0186_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0187_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0188_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0189_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0190_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0191_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0192_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0193_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0194_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0195_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0196_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0197_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0198_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0199_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0200_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0201_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0202_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0203_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0204_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0205_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0206_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0207_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0208_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0209_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0210_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0211_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0212_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0213_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0214_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0215_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0216_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0217_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0218_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0219_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0220_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0221_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0222_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0223_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0224_streamExpress_StorageManager.root",
        "/store/group/tsg-phase2/user/tomei/repacked/run386925/run386925_ls0225_streamExpress_StorageManager.root",
    ),
    secondaryFileNames = cms.untracked.vstring(),
    skipEvents = cms.untracked.uint32(eventsToSkip)
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
    fileName = cms.untracked.string(outputFileName),
    outputCommands = process.ALCARECOEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOTkAlMinBias_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOTkAlZMuMu_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiPixelCalSingleMuon_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiPixelCalSingleMuonTight_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiStripCalMinBias_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiStripCalMinBiasAAG_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiStripCalZeroBias_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiPixelCalZeroBias_noDrop.outputCommands)
process.ALCARECOEventContent.outputCommands.extend(process.OutALCARECOSiStripPCLHistos_noDrop.outputCommands)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '140X_dataRun3_Express_v3', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.ALCARECOoutput_step = cms.EndPath(process.ALCARECOoutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.pathALCARECOTkAlMinBias,process.pathALCARECOTkAlZMuMu,process.pathALCARECOSiPixelCalSingleMuon,process.pathALCARECOSiPixelCalSingleMuonTight,process.pathALCARECOSiStripCalMinBias,process.pathALCARECOSiStripCalMinBiasAAG,process.pathALCARECOSiStripCalZeroBias,process.pathALCARECOSiPixelCalZeroBias,process.pathALCARECOSiStripPCLHistos,process.endjob_step,process.ALCARECOoutput_step)
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

process.load('HLTrigger.Timer.FastTimerService_cfi')

process.FastTimerService.writeJSONSummary = True
process.FastTimerService.jsonFileName = "timing_tracking_upperbound_s2.json"

