#!/bin/bash -ex

# CMSSW_15_0_4

hltGetConfiguration /users/musich/tests/dev/CMSSW_15_0_0/NGT_DEMONSTRATOR/TestData/online/HLT/V1 \
            --globaltag 150X_dataRun3_Prompt_v1 \
            --data \
            --unprescale \
            --output all \
            --max-events 100 \
            --eras Run3_2024 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_0_0_xml \
            --input /store/data/Run2024I/EphemeralHLTPhysics0/RAW/v1/000/386/593/00000/91a08676-199e-404c-9957-f72772ef1354.root \
            > hltData.py

cmsRun hltData.py >& hltData.log
