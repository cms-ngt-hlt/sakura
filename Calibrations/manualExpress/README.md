# Running Manual Express in HTCondor at CERN

## Standard setup

```
cmsrel CMSSW_14_0_18_patch1
cd CMSSW_14_0_18_patch1/src
cmsenv
```

## How it works

The submission has three scripts:

- `express.submit` is the HTCondor submission script. It submits N copies (18 by default) of `runExpress.sh` and passes the `$(ProcId)` to it as an argument. We have to be careful to use `MY.WantOS = "el8"` to select an EL8 environment. It is also useful to select as many CPUs as you're going to use in the `expressN.py` scripts (see below).
- `runExpress.sh` is the script that sets up environment and CMSSW for us to run, runs the correct `expressN.py`, and copies the output somewhere safe.
  - We should probably set CMSSW up from some more reasonable area than "Thiago's area in AFS".
  - Ditto for copying the `expressN.py` CMSSW scripts. Actually, this script should probably just copy a master script and do the modifications on the fly!
  - Probably more improvements could be done, but every improvement brings us closer to reinventing a horrible version of CRAB :)
- `express0.py` is the CMSSW job configuration file. It is the same one from https://github.com/cms-ngt-hlt/sakura/blob/main/Calibrations/test_upper_bounds.sh , with some extra flexibility to skip a given number of events
  - Again, we should probably pass the list of files to run over and the "events per job" parameter in a non-hardcoded way.

## Instructions to run

Coming Soon™ 
