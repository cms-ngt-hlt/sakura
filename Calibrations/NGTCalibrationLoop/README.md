# NGT Calibration Loop

(Alpha version, just the first part of the loop (Express reconstruction) works.

## Prerequisites

The `transitions` package. Install it with `pip` or `conda`. You can install it locally with
```
pip3 install --user transitions
```

## Overview

The loop is modeled as a finite state machine (FSM). It has the following states
- "NotRunning"
- "WaitingForLS"
- "CheckingLSForProcess"
- "PreparingLS"
- "PreparingFinalLS"
- "PreparingExpressJobs"
- "LaunchingExpressJobs"
- "CleanupState"

Currently, it is set to run the ECALPedestals.

## Fast instructions

In `ngtcalfu-c2b03-43-01`:
```
source /opt/offline/cmsset_default.sh
cmsrel CMSSW_15_0_14
cd CMSSW_15_0_14_patch4/src
cmsenv
# Follow the setup to be able to use pip in the online machines
git clone git@github.com:cms-ngt-hlt/sakura.git
# I don't know how to use pip in the online machines,
# so we use the github repo directly
git clone git@github.com:pytransitions/transitions.git
cd transitions
python3 setup.py install --user
cd ..
cd sakura/Calibrations/NGTCalibrationLoop
mkdir /tmp/ngt/
cp ngtParameters.jsn /tmp/ngt/ngtParameters.jsn 
python3 NGTLoopStep2.py  
```

then in other terminal, go to `NGTCalibrationLoop` directory again and
```
touch running.txt
```

and then check in the first window that we detected the "run start". Finally, simulate the lumisections appearing with
```
for i in `ls /tmp/tomei/staging/`; do sleep 23; ln -s /tmp/tomei/staging/"$i" /tmp/tomei/input/"$i"; done
```

The whole output should appear in `/tmp/ngt/run396925/`
    
## Explanation

The loop starts in "NotRunning"; it expects its configuration to appear in `/tmp/ngt/ngtParameters.jsn` It expects a file "running.txt" to appear in the working directory to signal the fact that we are running, and "lumisections" to appear in tha directory `self.pathWhereFilesAppear`. By default it is set to `/tmp/tomei/input/`; Those lumisections have to be files of the form `run*_ls*.root`. In the calibration nodes, you can simulate their appearance with:
```
for i in `ls /tmp/tomei/staging/`; do sleep 23; ln -s /tmp/tomei/staging/"$i" /tmp/tomei/input/"$i"; done
```
(you have to clean up the lumisections yourself afterwards).

When we detect the file appearing (FIXME: should have a real way to detect the run starting, and to get the real run number to make the working directory `self.workingDir`), we mark the beginning of run time and move to the "WaitingForLS" state. In that state, we continuously move to "CheckingLSForProcess" and there are three options:
- We have LS waiting and they are enough to launch a job (FIXME: should be careful to not send jobs with too many LSs -- try to use `self.maximumLS` to address that.). In that case, we move to "PreparingLS".
- We have LS waiting but they are not enough to launch a job - this includes zero LS. We check if we are still running: if we are, we just go back to "WaitingForLS".
- We have not enough LS (as above), but we are not running anymore - so we have to launch a final job with whatever we have (FIXME: how does this work with being careful not to send jobs with too many LSs above?). In that case we move to "PreparingFinalLS"

In both cases, we move to "PreparingExpressJobs". This is where we remove LS from list of LS to be processed and add them to the list of LS that will go to the next job (FIXME: here we should tailor both the size and the TARGET of the job - remember that we have two nodes, so maybe we should do something to pick running in one or the other?). After that we move to "LaunchingExpressJobs".

Finally, we move to the "CleanupState". Here, if we came through the "PreparingFinalLS" state, that means that we just launched the last of the Express jobs. We write two log files: `allLSProcessed.log` with the name of all LS processed, and `expectedOutputs.log` with the name of all expected "step2" files. These are of the form "runXXXXXX_LSAAAAToBBBB_step2.root". We write a final script `ALCAOUTPUT.sh` that should run the step3 (FIXME: maybe this logic should belong to the next loop?). All of that is in the working directory, that currently is hardcoded as `/tmp/ngt/run386925/` (FIXME: should write it dinamically according to the run number).
        
## TODO
 - Address all the FIXMEs above
 - Implement some kind of infrastructure such that the loop is always running (maybe give control to it to `systemd`?)
 - Implement the second part of the loop
