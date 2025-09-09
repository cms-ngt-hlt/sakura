#!/bin/bash -ex

cmsDriver.py step4 --conditions 140X_dataRun3_Express_v3 -s ALCAHARVEST:SiStripQuality \
--scenario pp --data --filein file:PromptCalibProdSiStrip.root -n -1
#cmsRun step4_ALCAHARVEST.py
