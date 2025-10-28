#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from transitions import Machine, State


class NGTLoopStep3(object):

    # Define some states.
    states = [
        State(name="NotRunning", on_enter="ResetTheMachine", on_exit="SetupNewRun"),
        State(name="WaitingForStep2Files", on_enter="AnnounceWaitingForStep2Files"),
        State(name="CheckingFilesForProcess", on_enter="CheckFilesForProcessing"),
        State(name="PreparingFiles", on_enter="ExecutePrepareFiles"),
        State(name="PreparingFinalFiles", on_enter="ExecutePrepareFinalFiles"),
        State(name="PreparingExpressJobs", on_enter="PrepareExpressJobs"),
        State(name="LaunchingExpressJobs", on_enter="LaunchExpressJobs"),
        State(name="CleanupState", on_enter="ExecuteCleanup"),
    ]

    # We check if a new run appeared, e.g. /tmp/ngt/run386925
    def NewRunAppeared(self):
        print("Checking if a new run appeared")
        path = Path(self.pathWhereFilesAppear)
        currentDirs = {p.name for p in path.iterdir() if p.is_dir()}
        newDirs = currentDirs - self.setOfRunsProcessed
        # Thiago: rig to run on 398600
        # newRuns = {p for p in newDirs if p.startswith("run")}
        newRuns = {p for p in newDirs if p.startswith("run398600")}
        foundNewRuns = not (not newRuns)  # Is this pythonic?
        if foundNewRuns:
            print("New runs found!")
            # What happens if we found more than one run?
            # We figure that out later...
            # Slice off the "run" substring at the beginning
            self.runNumber = (self.GetNextRun(newRuns))[3:]
            print(f"Run {self.runNumber} is available")
        else:
            print("No new runs...")

        return foundNewRuns

    # For now, we just take the earliest of the new runs
    def GetNextRun(self, newRuns):
        return sorted(newRuns, reverse=True)[0]

    def SetupNewRun(self):
        # Prepare the new run
        self.workingDir = "/tmp/ngt/run" + self.runNumber
        startTimeFilePath = Path(self.workingDir + "/runStart.log")
        if startTimeFilePath.exists():
            with open(startTimeFilePath, "r") as f:
                runStartLine = f.readline()
                self.startTime = datetime.fromisoformat(runStartLine)
        else:
            # Weird, how come we don't have a runStart.log?
            # Fine, we set the start time to now
            print("We didn't find a runStart.log file... setting run start to NOW")
            self.startTime = datetime.now(timezone.utc)

        print(f"Run {self.runNumber} detected, started at {self.startTime.isoformat()}")

    def AnnounceWaitingForStep2Files(self):
        print("I am WaitingForStep2Files...")

    def RunIsNotComplete(self):
        print("Is the run complete?")
        runEndedFile = Path(self.workingDir + "/runEnd.log")
        if runEndedFile.exists():
            print("The run is complete!")
        else:
            print("Not yet...")
        return not runEndedFile.exists()

    def StillHaveTime(self):
        now_utc = datetime.now(timezone.utc)
        diff = now_utc - self.startTime
        if diff.total_seconds() > self.timeoutInSeconds:
            print("Time ran out!")
            return False
        else:
            return True

    def CheckFilesForProcessing(self):
        print("I am in CheckFilesForProcessing...")
        # Do something to check if there are Files to process
        setOfFilesAvailable = self.GetSetOfAvailableFiles()
        self.setOfFilesObserved = self.setOfFilesObserved.union(setOfFilesAvailable)
        self.setOfFilesToProcess = setOfFilesAvailable - self.setOfFilesProcessed
        self.waitingFiles = len(self.setOfFilesToProcess) > 0
        print("New files to process:")
        print(self.setOfFilesToProcess)
        if len(self.setOfFilesToProcess) >= self.minimumFiles:
            self.enoughFiles = True
        else:
            self.enoughFiles = False

    # This function only looks at a given path and lists
    # all available files of the form "run*_step2.root".
    # Notice, however, that "available" here means
    # "the ROOT files are closed and ready to be used"!
    # So, we list files of the form
    # "run*_*ecalPedsStep2_job.txt". If we find those,
    # we lop off that suffix and substitute it for "step2.root"
    def GetSetOfAvailableFiles(self):
        # For this version, self.pathWhereFilesAppear is the same as
        # self.workingDir
        targetPath = self.workingDir
        suffixControlFiles = "ecalPedsStep2_job.txt"
        # We control the naming of these files, we know they're called like this
        setOfControlFiles = set(
            list(Path(targetPath).glob("run*_" + suffixControlFiles))
        )
        as_strings = {str(p) for p in setOfControlFiles}
        changed = {
            (
                s[: -len(suffixControlFiles)] + "step2.root"
                if s.endswith(suffixControlFiles)
                else s
            )
            for s in as_strings
        }
        setOfAvailableFiles = {Path(s) for s in changed}
        return setOfAvailableFiles

    def ExecutePrepareFiles(self):
        print("I am PreparingFiles")
        self.PrepareFilesForProcessing()

    def ExecutePrepareFinalFiles(self):
        print("I am PreparingFinalFiles")
        self.PrepareFilesForProcessing()
        # Since this is final files, they have to be enough!
        self.preparedFinalFiles = True

    def PrepareFilesForProcessing(self):
        print("I am in PrepareFilesForProcessing...")
        print("Will use the following Files:")
        # We add here an additional check: do these files all really exist?
        for fileToProcess in self.setOfFilesToProcess:
            if fileToProcess.exists():
                self.setOfExpressFiles.add(fileToProcess)

        # So here there's a subtlety: here, all files are processed,
        # but not are them are sutiable for Express
        # (e.g., because they don't exist)
        # So we keep track of the two different sets now
        print(self.setOfExpressFiles)

    def PrepareExpressJobs(self):
        print("I am in PrepareExpressjobs...")

        # We may arrive here without a self.setOfExpressFiles if
        # the run started and ended without producing Files.
        # In that case, nothing to do
        if not self.setOfExpressFiles:
            return

        # Here we should have some logic that prepares the Express jobs
        # Probably should have a call to cmsDriver
        # There are better ways to do this, but right now I just do it with a file

        # First make a particular subdir for us to run in
        alcaJobDir = Path(self.workingDir + "/apJob" + f"{self.alcaJobNumber:03}")
        alcaJobDir.mkdir(parents=True, exist_ok=True)
        os.chmod(alcaJobDir, 0o777)
        # Save it so that we can use it later
        self.jobDir = str(alcaJobDir)
        alcaJobFile = alcaJobDir / Path("ALCAOUTPUT.sh")

        # At this point, we already increase the self.alcaJobNumber
        self.alcaJobNumber += 1

        # Write the job file
        with alcaJobFile.open("w") as f:
            f.write("#!/bin/bash -ex\n\n")
            # First we go to the workingDir to setup CMSSW
            f.write(f"export $SCRAM_ARCH={self.scramArch}\n")
            f.write(f"cd {self.workingDir}/{self.cmsswVersion}/src\n")
            f.write("cmsenv\n")
            f.write("cd -\n\n")
            # Now we do the cmsDriver.py proper
            f.write(f"cmsDriver.py expressStep3 --conditions {self.globalTag} ")
            f.write(
                " -s ALCAOUTPUT:EcalTestPulsesRaw,ALCA:PromptCalibProdEcalPedestals "
                + "--datatier ALCARECO --eventcontent ALCARECO "
                + "--triggerResultsProcess RERECO "
                + "--nThreads 8 --nStreams 8 -n -1 "
            )
            # and we pass the list of files to process (self.setOfFilesToProcess)
            f.write("--filein ")
            # some massaging to go from PosixPath to string
            str_paths = {"file:" + str(p) for p in self.setOfExpressFiles}
            f.write(",".join(str_paths))
            # No need for fileout here
            # f.write(f" --fileout {outputFileName} --no_exec ")
            f.write(" --no_exec ")
            f.write(f"--python_filename run{self.runNumber}_ecalPedsALCAOUTPUT.py\n\n")
            # Some massaging to fix the source
            f.write(f"cat <<@EOF>> run{self.runNumber}_ecalPedsALCAOUTPUT.py\n")
            f.write(
                'process.ALCARECOEcalTestPulsesRaw.TriggerResultsTag = cms.InputTag("TriggerResults", "", "RERECO")\n'
            )
            f.write("@EOF\n\n")
            f.write(f"cmsRun run{self.runNumber}_ecalPedsALCAOUTPUT.py")

    def LaunchExpressJobs(self):
        print("I am in LaunchExpressJobs...")

        # Here we should launch the Express jobs
        # We use subprocess.Popen, since we don't want to hang waiting for this
        # to finish running. Some other loop will look at their output
        # FIXME: add monitoring...
        subprocess.Popen(
            ["bash", "ALCAOUTPUT.sh"],
            cwd=self.jobDir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Now we have to move the files we just processed
        # to self.setOfFilesProcessed
        # and clear self.setOfFilesToProcess
        # and setOfExpressFiles
        print("Launched jobs with:")
        print(self.setOfExpressFiles)
        self.setOfFilesProcessed = self.setOfFilesProcessed.union(
            self.setOfFilesToProcess
        )
        self.setOfFilesToProcess = set()
        self.setOfExpressFiles = set()

    def ThereAreFilesWaiting(self):
        if self.waitingFiles:
            print("++ There are Files waiting!")
        else:
            print("++ No Files waiting...")
        return self.waitingFiles

    def ThereAreEnoughFiles(self):
        if self.enoughFiles:
            print("++ Enough step2 files found!")
        else:
            print("++ Not enough step2 files...")
        return self.enoughFiles

    def WePreparedFinalFiles(self):
        return self.preparedFinalFiles

    def ExecuteCleanup(self):
        print("I am in ExecuteCleanup")
        if self.preparedFinalFiles:
            print("We prepared final files, will reset the machine...")
            # We actually have to reset the machine only when we go to NotRunning!

            # Make a log of everything that we did
            with open(self.workingDir + "/allStep2FilesProcessed.log", "w") as f:
                for Files in sorted(self.setOfFilesProcessed):
                    f.write(str(Files) + "\n")
            # Add the run we have just seen to our memory
            # If is easier to just add the "run" prefix here
            self.setOfRunsProcessed.add("run" + self.runNumber)
            print(self.setOfRunsProcessed)

    def ResetTheMachine(self):
        print("Machine reset!")
        self.runNumber = 0
        self.startTime = 0
        self.timeoutInSeconds = 99 * 60 * 60  # 8 hours
        self.minimumFiles = 1
        self.maximumFiles = 5
        self.requestMinimumFiles = True
        self.waitingFiles = False
        self.enoughFiles = False
        self.pathWhereFilesAppear = "/tmp/ngt/"
        self.workingDir = "/dev/null"
        self.jobDir = "/dev/null"
        self.alcaJobNumber = 0
        self.preparedFinalFiles = False

        # Read some configurations
        with open("/tmp/ngt/ngtParameters.jsn", "r") as f:
            config = json.load(f)
        self.scramArch = config["SCRAM_ARCH"]
        self.cmsswVersion = config["CMSSW_VERSION"]
        self.globalTag = config["GLOBAL_TAG"]

        self.setOfFilesObserved = set()
        self.setOfFilesToProcess = set()
        self.setOfExpressFiles = set()
        self.setOfFilesProcessed = set()
        self.setOfExpectedOutputs = set()

    def __init__(self, name):

        # No anonymous FSMs in my watch!
        self.name = name

        self.setOfRunsProcessed = set()
        self.ResetTheMachine()

        # Initialize the state machine
        self.machine = Machine(
            model=self, states=NGTLoopStep3.states, queued=True, initial="NotRunning"
        )

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # If we're not running, try to start running
        self.machine.add_transition(
            trigger="TryLookForRun",
            source="NotRunning",
            dest="WaitingForStep2Files",
            conditions="NewRunAppeared",
        )
        # Otherwise, do nothing
        self.machine.add_transition(
            trigger="TryLookForRun", source="NotRunning", dest=None
        )

        # During the loop, maybe we find out we are not running any more
        # In that case, we went through the "PreparingFinalFiles" state
        # So we need to check if that happened
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="CleanupState",
            dest="NotRunning",
            conditions="WePreparedFinalFiles",
        )
        # Otherwise, we go back to WaitingForStep2Files
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="CleanupState",
            dest="WaitingForStep2Files",
        )

        # This is the inner loop. We go from "WaitingForStep2Files"
        # to the "CheckingFilesForProcess", and from there we
        # will go to one of three states
        self.machine.add_transition(
            trigger="TryProcessFiles",
            source="WaitingForStep2Files",
            dest="CheckingFilesForProcess",
        )

        # If we have enough Files, we go to PreparingFiles
        self.machine.add_transition(
            trigger="ContinueAfterCheckFiles",
            source="CheckingFilesForProcess",
            dest="PreparingFiles",
            conditions=["ThereAreFilesWaiting", "ThereAreEnoughFiles"],
        )

        # If we don't have enough Files, but we are still running,
        # more Files will come. We go to WaitingForStep2Files,
        # but only if we still have time!
        self.machine.add_transition(
            trigger="ContinueAfterCheckFiles",
            source="CheckingFilesForProcess",
            dest="WaitingForStep2Files",
            conditions=["RunIsNotComplete", "StillHaveTime"],
        )

        # If we don't have enough Files, and we are not still running,
        # no more Files will come. We go to PreparingFinalFiles
        self.machine.add_transition(
            trigger="ContinueAfterCheckFiles",
            source="CheckingFilesForProcess",
            dest="PreparingFinalFiles",
        )

        # In any case, prepare the Express jobs
        self.machine.add_transition(
            trigger="TryPrepareALCAPROMPTJobs",
            source="PreparingFiles",
            dest="PreparingExpressJobs",
        )
        self.machine.add_transition(
            trigger="TryPrepareALCAPROMPTJobs",
            source="PreparingFinalFiles",
            dest="PreparingExpressJobs",
        )

        # And launch them!
        self.machine.add_transition(
            trigger="TryLaunchALCAPROMPTJobs",
            source="PreparingExpressJobs",
            dest="LaunchingExpressJobs",
        )
        self.machine.add_transition(
            trigger="ContinueToCleanup",
            source="LaunchingExpressJobs",
            dest="CleanupState",
        )

        # All other triggers take you from WaitingForStep2Files to WaitingForStep2Files if need be
        self.machine.add_transition(
            trigger="TryPrepareALCAPROMPTJobs",
            source="WaitingForStep2Files",
            dest="WaitingForStep2Files",
        )
        self.machine.add_transition(
            trigger="TryLaunchALCAPROMPTJobs",
            source="WaitingForStep2Files",
            dest="WaitingForStep2Files",
        )
        self.machine.add_transition(
            trigger="ContinueToCleanup",
            source="WaitingForStep2Files",
            dest="WaitingForStep2Files",
        )
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="WaitingForStep2Files",
            dest="WaitingForStep2Files",
        )


loop = NGTLoopStep3("Step3")

loop.state

while True:
    while loop.state == "NotRunning":
        time.sleep(1)  # Should be time.sleep(30) for deployment
        loop.TryLookForRun()

    while loop.state == "WaitingForStep2Files":
        loop.TryProcessFiles()
        time.sleep(1)
        loop.ContinueAfterCheckFiles()
        time.sleep(1)
        loop.TryPrepareALCAPROMPTJobs()
        time.sleep(1)
        loop.TryLaunchALCAPROMPTJobs()
        time.sleep(1)
        loop.ContinueToCleanup()
        time.sleep(1)
        loop.ContinueAfterCleanup()
        time.sleep(1)
