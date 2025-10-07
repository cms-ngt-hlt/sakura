#!/bin/bash

cmsDriver.py step4 --conditions 150X_dataRun3_Express_v1 -s ALCAHARVEST:EcalPedestals \
--scenario pp --data --filein file:PromptCalibProdEcalPedestals.root -n -1 --no_exec
cmsRun step4_ALCAHARVEST.py
