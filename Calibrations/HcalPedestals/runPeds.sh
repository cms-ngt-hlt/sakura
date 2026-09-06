#!/bin/bash

# generate the hcal nanoAOD configuration
cmsDriver.py NANO \
	     -s RAW2DIGI,RECO,USER:DPGAnalysis/HcalNanoAOD/hcalNano_cff.hcalNanoTask \
	     --datatier NANOAOD \
	     --eventcontent NANOAOD \
	     --processName USER \
	     --nThreads 16 \
	     --filein /store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/007548c4-f2bb-4afe-a13f-7f6736cb8f19.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/3e318b5f-44cb-4330-b8a1-8397fecbd359.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/453f33a9-757f-47a6-95c7-02452711cd29.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/5cff7890-1174-4bd4-91ba-f95bac106076.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/8a4089df-4c9d-45a9-be82-c72fb38b3053.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/bb023468-ae78-4fed-9963-c56b1a083d5f.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/d27af202-36f9-42e4-aad2-244e4afc4848.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/d9ffdd68-7762-43c7-a931-50cae6a617b6.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/e39ee31d-ed04-4c25-b454-9463e2efd069.root,/store/group/tsg-phase2/user/tomei/TestEnablesEcalHcal/run403244/e5d55849-90f9-478e-88fd-7b36b2d4048f.root \
	     --fileout peds.root \
	     --conditions 160X_dataRun3_HLT_v1 \
	     -n 6000 \
	     --era Run3_2026 \
	     --customise DPGAnalysis/HcalNanoAOD/customiseHcalCalib_cff.customiseHcalCalib \
	     --python_filename test_global_cfg.py \
	     --no_exec

# execute the nanoAOD creation
cmsRun test_global_cfg.py

# download and compile the ROOT macro
wget https://gitlab.cern.ch/hcal_automation/pedestals/-/raw/master/digi_fromNano.cc
wget https://gitlab.cern.ch/hcal_automation/pedestals/-/raw/master/makefile
make

# generate the pedestals table
./nano_to_digi peds.root 403244

# convert to DB
wget https://raw.githubusercontent.com/HcalConditionsAutomatization/ConditionsValidation/08bfab92e10be6a375d11b7c7263411066f21fda/Tools/writetoSQL.csh
chmod +x writetoSQL.csh
./writetoSQL.csh 2026 Pedestals PedestalTable.txt Tag 403244 403244 Pedestals.db
