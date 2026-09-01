#!/bin/bash 

cmsenv

RUNS=(593 509 594 604 642 661 553 668 661 672 673 679 693 446 477 478 505 508 554 592 605 614 615 616 617 618 629 640 630)

for RUN in "${RUNS[@]}"; do
echo "Processing run $RUN..."

INPUT_FILES=$(find /eos/cms/store/group/tsg-phase2/user/jprendi/PrLC_Run2024I_386${RUN}/ -type f -name  "output*.root" | paste -sd, -)

cmsRun DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py inputFiles=$INPUT_FILES >& dqmclient_LC_${RUN}.log
done
