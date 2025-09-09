#!/bin/bash -ex

cmsDriver.py step4 --conditions 140X_dataRun3_Express_v3 -s ALCAHARVEST:BeamSpotByRun \
--scenario pp --data --filein file:PromptCalibProd.root -n -1
#cmsRun step4_ALCAHARVEST.py
