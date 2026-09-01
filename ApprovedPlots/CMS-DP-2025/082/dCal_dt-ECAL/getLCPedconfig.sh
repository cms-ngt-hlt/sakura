#!/bin/bash -ex

    hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V80 \
       --globaltag 150X_dataRun3_HLT_v1 \
       --data \
       --unprescale \
       --output minimal \
       --max-events -1 \
       --eras Run3_2024 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_1_1_xml \
        --input " " \
       > hltDataLCPed.py


cat <<@EOF >> hltDataLCPed.py

process.GlobalTag.toGet.append(
  cms.PSet(record = cms.string("EcalPedestalsRcd"),
           tag = cms.string("EcalPedestals_prompt"),
           connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
          )
)


process.GlobalTag.toGet.append(
  cms.PSet(record = cms.string("EcalLaserAPDPNRatiosRcd"),
           tag = cms.string("EcalLaserAPDPNRatios_prompt_v3"),
           connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
          )
)

process.hltOutputMinimal.outputCommands = [
    'drop *',
    'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_HLTX',
    'keep edmTriggerResults_*_*_HLTX',
    'keep triggerTriggerEvent_*_*_HLTX' 
]


process.options.numberOfThreads = 1

@EOF

edmConfigDump hltDataLCPed.py > dumpLCPed.py
rm hltDataLCPed.py
