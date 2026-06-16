# Instructions ?

KEEP IN MIND !! Everything is hardcoded. This is just documentation of the steps *I* took to get to the files. :)

The jobs were submitted within `CMSSW_15_0_17`. Generate a proxy à la:
```
voms-proxy-init --voms cms --valid 168:00
```
^ and store the resulting proxy wherever convenient.

The following scripts are to be run:
```
./generateFileListPerRun.sh
./EGammaFullHLT.sh
./submit_all.sh
```

and then check status of the jobs a lot with `condor_q`.

The files I obtained can be found in:
```
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/NGT
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/HLT
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/Prompt
```
as well as the resulting job folders stored at:
```
/eos/cms/store/group/tsg-phase2/user/jprendi/NERD25/MoreStats/EGammas/JobSubmissions
```
and you have the files :-)
