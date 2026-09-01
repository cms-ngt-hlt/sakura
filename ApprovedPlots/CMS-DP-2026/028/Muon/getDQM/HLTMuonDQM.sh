#!/bin/bash -ex

EOS_DIR="/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/Muons/HLT"
FILE_PATTERN="*Raw.root"
INPUT_FILES=$(find "$EOS_DIR" -name "$FILE_PATTERN" | sort | sed 's|^|file:|' | paste -sd, -)

cmsRun DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py inputFiles="$INPUT_FILES" >& dqmclient_HLT.log
