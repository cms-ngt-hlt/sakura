#!/bin/bash


nums=$(grep -oP '/000/386/\K[0-9]+' fileList.txt | sort -u)
for num in $nums; do
  grep "/000/386/$num/" fileList.txt > "fileList_${num}.txt"
#  mkdir /eos/cms/store/group/tsg-phase2/user/jprendi/PrLC_Run2024I_386$num
#  mkdir /eos/cms/store/group/tsg-phase2/user/jprendi/Pr_Run2024I_386$num
  mkdir /eos/cms/store/group/tsg-phase2/user/jprendi/PrLCPed_Run2024I_386$num
  mkdir /eos/cms/store/group/tsg-phase2/user/jprendi/PrPed_Run2024I_386$num
  mkdir /eos/cms/store/group/tsg-phase2/user/jprendi/PrPrompt_Run2024I_386$num
done

nums=$(grep -oP '/000/386/\K[0-9]+' fileList.txt | sort -u)
for num in $nums; do
  grep "/000/386/$num/" fileList.txt > "fileList_${num}.txt"
done

