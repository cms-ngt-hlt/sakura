#!/bin/bash -ex

# cmsrel CMSSW_15_0_4_patch1 
# cd CMSSW_15_0_4_patch1/src
# cmsenv
# scram b

RUNNUMBER=386593
LUMISECTION=250

INPUTFILES="root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics1/RAW/v1/000/386/593/00000/9c067800-8618-4a0b-9a9d-bcfe833fc042.root root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics0/RAW/v1/000/386/593/00000/a79210d6-3442-4a75-95b2-670fc5f3e5b4.root root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics2/RAW/v1/000/386/593/00000/95bbef1b-9d8d-4a53-862c-32c94450bee2.root root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics3/RAW/v1/000/386/593/00000/cbec7838-61cc-4c46-8ad9-e2e0903e62c3.root root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics4/RAW/v1/000/386/593/00000/0bd73ec3-8d8b-4804-8ac3-c774a609049f.root root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics5/RAW/v1/000/386/593/00000/1a187ce0-0cc7-483f-b868-651a566e116a.root root://eoscms.cern.ch//store/data/Run2024I/EphemeralHLTPhysics6/RAW/v1/000/386/593/00000/e5a375b9-1abe-4a49-9d17-7f2fc6483135.root"

rm -rf run${RUNNUMBER}*

# run on 23000 events of LS 250, without event limits per input file
convertToRaw -l 23000 -r ${RUNNUMBER}:${LUMISECTION} -o . -- ${INPUTFILES}

tmpfile=$(mktemp)
hltConfigFromDB --configName /users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V3 > "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load("run${RUNNUMBER}_cff")
# to run without any HLT prescales
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = True
# # to run using the same HLT prescales as used online in LS 250
# process.PrescaleService.forceDefault = True

from HLTrigger.Configuration.common import *
def customizeHLTfor2024L1TMenu(process):
    seed_replacements = {

        'L1_SingleMu5_BMTF' : 'L1_AlwaysTrue',
        'L1_SingleMu13_SQ14_BMTF': 'L1_AlwaysTrue',

        'L1_AXO_Medium' : 'L1_AXO_Nominal',
        'L1_AXO_VVTight': 'L1_AlwaysTrue',
        'L1_AXO_VVVTight': 'L1_AlwaysTrue',

        'L1_CICADA_VVTight': 'L1_AlwaysTrue',
        'L1_CICADA_VVVTight': 'L1_AlwaysTrue',
        'L1_CICADA_VVVVTight': 'L1_AlwaysTrue',

        'L1_DoubleTau_Iso34_Iso26_er2p1_Jet55_RmOvlp_dR0p5': 'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5 OR L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5',
        'L1_DoubleTau_Iso38_Iso26_er2p1_Jet55_RmOvlp_dR0p5': 'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5 OR L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5',
        'L1_DoubleTau_Iso40_Iso26_er2p1_Jet55_RmOvlp_dR0p5': 'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5 OR L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5',

        'L1_DoubleEG15_11_er1p2_dR_Max0p6': 'L1_DoubleEG11_er1p2_dR_Max0p6',
        'L1_DoubleEG16_11_er1p2_dR_Max0p6': 'L1_DoubleEG11_er1p2_dR_Max0p6',
        'L1_DoubleEG17_11_er1p2_dR_Max0p6': 'L1_DoubleEG11_er1p2_dR_Max0p6',

        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min1000': 'L1_AlwaysTrue',
        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min1100': 'L1_AlwaysTrue',
        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min1200': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min700_IsoTau45er2p1_RmOvlp_dR0p5': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min800_IsoTau45er2p1_RmOvlp_dR0p5': 'L1_AlwaysTrue',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min750_DoubleJetCentral50': 'L1_AlwaysTrue',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min850_DoubleJetCentral50': 'L1_AlwaysTrue',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min950_DoubleJetCentral50': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min700_LooseIsoEG20er2p1_RmOvlp_dR0p2': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min800_LooseIsoEG20er2p1_RmOvlp_dR0p2': 'L1_AlwaysTrue',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min700_Mu3OQ': 'L1_AlwaysTrue',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min800_Mu3OQ': 'L1_AlwaysTrue',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min900_Mu3OQ': 'L1_AlwaysTrue',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min600_ETMHF65': 'L1_AlwaysTrue',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min700_ETMHF65': 'L1_AlwaysTrue',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min800_ETMHF65': 'L1_AlwaysTrue',
    }

    for module in filters_by_type(process, 'HLTL1TSeed'):
        l1Seed = module.L1SeedsLogicalExpression.value()
        if any(old_seed in l1Seed for old_seed in seed_replacements):
            for old_seed, new_seed in seed_replacements.items():
                l1Seed = l1Seed.replace(old_seed, new_seed)
            module.L1SeedsLogicalExpression = cms.string(l1Seed)

    return process

process = customizeHLTfor2024L1TMenu(process)    

@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

# remove input files to save space
rm -f run386593/run386593_ls0*_index*.*

# now cat the files and run the FRD conversion
cat run386593/run386593_ls0000_streamLocalTestDataRaw_pid3599953.ini run386593/run386593_ls0250_streamLocalTestDataRaw_pid3599953.dat > run386593_ls0250_streamLocalTestDataRaw_pid3599953.dat
cp -pr /afs/cern.ch/user/m/mzarucki/public/NGT/SAKURA/Demonstrator/test_convertStreamerToFRD.py .
cmsRun test_convertStreamerToFRD.py filePrepend=file: inputFiles=run386593_ls0250_streamLocalTestDataRaw_pid3599953.dat
