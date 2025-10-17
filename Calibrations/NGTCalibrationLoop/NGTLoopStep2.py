#!/usr/bin/env python
# coding: utf-8

from transitions import Machine, State
import random
import time
from pathlib import Path
import subprocess
import re
import tempfile

class NGTLoopStep2(object):

    # Define some states.
    states = [
        State(
            name="NotRunning", on_enter="ResetTheMachine", on_exit="ExecuteRunStart"
        ),
        State(name="WaitingForLS", on_enter="AnnounceWaitingForLS"),
        State(name="CheckingLSForProcess", on_enter="CheckLSForProcessing"),
        State(name="PreparingLS", on_enter="ExecutePrepareLS"),
        State(name="PreparingFinalLS", on_enter="ExecutePrepareFinalLS"),
        State(name="PreparingExpressJobs", on_enter="PrepareExpressJobs"),
        State(name="LaunchingExpressJobs", on_enter="LaunchExpressJobs"),
        State(name="CleanupState", on_enter="ExecuteCleanup"),
    ]

    def ExecuteRunStart(self):
        runNumber = self.runNumber
        print(f"Run {runNumber} has started!")
        p = Path(f"/tmp/run{runNumber}")
        p.mkdir(parents=True, exist_ok=True)
        self.workingDir = str(p)

    def AnnounceWaitingForLS(self):
        print("I am WaitingForLS...")

    def AnnounceRunStop(self):
        print("The run stopped...")

    # FIXME: to be substituted with some code to check if DAQ is running    
    # Right now we have a dummy check!
    # Should also check if the run is good for runs (e.g. only pp run?)
    def DAQIsRunning(self):
        print("Testing if DAQ is running...")
        weAreRunning = Path("running.txt").exists()
        if weAreRunning:
            print("We are running!")
            self.runNumber = self.GetRunNumber()
        else:
            print("We are not running...")
        return weAreRunning

    # FIXME: Dummy
    def GetRunNumber(self):
        return 386925
    
    def CheckLSForProcessing(self):
        print("I am in CheckLSForProcessing...")
        ### This could be a Luigi task, for instance
        # Do something to check if there are LS to process
        listOfLSFilesAvailable = self.GetListOfAvailableFiles()
        self.setOfLSObserved = self.setOfLSObserved.union(listOfLSFilesAvailable)
        self.setOfLSToProcess = listOfLSFilesAvailable - self.setOfLSProcessed
        self.waitingLS = len(self.setOfLSToProcess) > 0
        print("New LSs to process:")
        print(self.setOfLSToProcess)
        if len(self.setOfLSToProcess) >= self.minimumLS:
            self.enoughLS = True
        else:
            self.enoughLS = False

    # This function only looks at a given path and lists all available
    # files of the form "run*_ls*.root". Could be made smarter if needed
    def GetListOfAvailableFiles(self):
        targetPath = self.pathWhereFilesAppear
        listOfAvailableFiles = set(list(Path(targetPath).glob("run*_ls*.root")))
        return listOfAvailableFiles
    
    def ExecutePrepareLS(self):
        print("I am PreparingLS") 
        self.PrepareLSForProcessing()

    def ExecutePrepareFinalLS(self):
        print("I am PreparingFinalLS") 
        self.PrepareLSForProcessing()
        # Since this is final LS, they have to be enough!
        self.preparedFinalLS = True
        
    def PrepareLSForProcessing(self):
        print("I am in PrepareLSForProcessing...")
        print("Will use the following LS:")
        print(self.setOfLSToProcess)
        
    def PrepareExpressJobs(self):
        print("I am in PrepareExpressjobs...")
        
        # Extract all LS numbers (as integers)
        str_paths = {"file:"+str(p) for p in self.setOfLSToProcess}
        ls_numbers = [
            int(re.search(r"ls(\d{4})", path).group(1))
            for path in str_paths
        ]

        # Compute min and max, then format back
        min_ls = min(ls_numbers)
        max_ls = max(ls_numbers)
        affix = f"LS{min_ls:04d}To{max_ls:04d}"
        
        # Here we should have some logic that prepares the Express jobs
        # Probably should have a call to cmsDriver
        # There are better ways to do this, but right now I just do it with a file

        with open(self.workingDir+"/cmsDriver.sh", "w") as f:
            # Do we actually need to set the environment like this every time?
            f.write("#!/bin/bash -ex\n\n")
            f.write("export $SCRAM_ARCH=el8_amd64_gcc12\n")
            f.write("cmsrel CMSSW_15_0_12\n")
            f.write("cd CMSSW_15_0_12/src\n")
            f.write("cmsenv\n")
            f.write("cd -\n\n")
            # Now we do the cmsDriver.py proper
            f.write("cmsDriver.py expressStep2 --conditions 150X_dataRun3_Express_v2 "+
                    "-s RAW2DIGI,RECO,ALCAPRODUCER:EcalTestPulsesRaw " +
                    "--datatier ALCARECO --eventcontent ALCARECO --data --process RERECO "+
                    "--scenario pp --era Run3 "+
                    "--nThreads 8 --nStreams 8 -n -1 ")
            # and we pass the list of LS to process (self.setOfLSToProcess)
            f.write("--filein ")
            # some massaging to go from PosixPath to string
            str_paths = {"file:"+str(p) for p in self.setOfLSToProcess}
            f.write(",".join(str_paths))
            f.write(f" --fileout file:run{self.runNumber}_{affix}_step2.root --no_exec ")
            f.write(f"--python_filename run{self.runNumber}_{affix}_ecalPedsStep1.py\n\n")
            f.write(f"cmsRun run{self.runNumber}_{affix}_ecalPedsStep1.py &\n")

        self.setOfExpressLS = self.setOfLSToProcess
        self.setOfLSToProcess = set()

    def LaunchExpressJobs(self):
        print("I am in LaunchExpressJobs...")

        # Here we should launch the Express jobs
        # We use subprocess.Popen, since we don't want to hang waiting for this
        # to finish running. Some other loop will look at their output
        subprocess.Popen(
            ["bash", "cmsDriver.sh"],
            cwd=self.workingDir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Now we have to move the LSs to self.setOfLSProcessed
        # and clear self.setOfLSToProcess

        print("Launched jobs with:")
        print(self.setOfExpressLS)
        self.setOfLSProcessed = self.setOfLSProcessed.union(self.setOfExpressLS)
        self.setOfLSToProcess = set()

    def ThereAreLSWaiting(self):
        if self.waitingLS:
            print("++ There are LS waiting!")
        else:
            print("++ No LS waiting...")
        return self.waitingLS

    def ThereAreEnoughLS(self):
        if self.enoughLS:
            print("++ Enough LS found!")
        else:
            print("++ Not enough LS...")
        return self.enoughLS

    def WePreparedFinalLS(self):
        return self.preparedFinalLS
    
    def ExecuteCleanup(self):
        print("I am in ExecuteCleanup")
        if self.preparedFinalLS:
            print("We prepared Final LS, resetting the machine...")
            ### We actually have to reset the machine when we go to not running!
            #self.ResetTheMachine()
            
    def ResetTheMachine(self):
        print("Machine reset!")
        self.runNumber = 0
        self.startTime = 0
        self.minimumLS = 3
        self.requestMinimumLS = True
        self.waitingLS = False
        self.enoughLS = False
        self.pathWhereFilesAppear = "/tmp/tomei/input/"
        self.workingDir = "/dev/null"
        self.preparedFinalLS = False
        
        self.setOfLSObserved = set()
        self.setOfLSToProcess = set()
        self.setOfExpressLS = set()
        self.setOfLSProcessed = set()       
        
    def __init__(self, name):

        # No anonymous FSMs in my watch!
        self.name = name
        self.ResetTheMachine()
        
        # Initialize the state machine
        self.machine = Machine(
            model=self, states=NGTLoopStep2.states, queued=True, initial="NotRunning"
        )

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # If we're not running, try to start running
        self.machine.add_transition(
            trigger="TryStartRun",
            source="NotRunning",
            dest="WaitingForLS",
            conditions="DAQIsRunning",
        )
        # Otherwise, do nothing
        self.machine.add_transition(
            trigger="TryStartRun", source="NotRunning", dest=None
        )
        
        # During the loop, maybe we find out we are not running any more
        # In that case, we went through the "PreparingFinalLS" state
        # So we need to check if that happened
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="CleanupState",
            dest="NotRunning",
            conditions="WePreparedFinalLS"
        )
        # Otherwise, we go back to WaitingForLS
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="CleanupState",
            dest="WaitingForLS"
        )

        # This is the inner loop. We go from "WaitingForLS"
        # to the "CheckingLSForProcess", and from there we
        # will go to one of three states
        self.machine.add_transition(
            trigger="TryProcessLS",
            source="WaitingForLS",
            dest="CheckingLSForProcess"
        )

        # If we have enough LS, we go to PreparingLS
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="PreparingLS",
            conditions=["ThereAreLSWaiting", "ThereAreEnoughLS"],
        )

        # If we don't have enough LS, but we are still running,
        # more LS will come. We go to WaitingForLS
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="WaitingForLS",
            conditions="DAQIsRunning"
        )
        
        # If we don't have enough LS, and we are not still running,
        # no more LS will come. We go to PreparingFinalLS
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="PreparingFinalLS"
        )

        # In any case, prepare the Express jobs
        self.machine.add_transition(
            trigger="TryPrepareExpressJobs",
            source="PreparingLS",
            dest="PreparingExpressJobs",
        )
        self.machine.add_transition(
            trigger="TryPrepareExpressJobs",
            source="PreparingFinalLS",
            dest="PreparingExpressJobs",
        )

        # And launch them!
        self.machine.add_transition(
            trigger="TryLaunchExpressJobs",
            source="PreparingExpressJobs",
            dest="LaunchingExpressJobs",
        )
        self.machine.add_transition(
            trigger="ContinueToCleanup",
            source="LaunchingExpressJobs",
            dest="CleanupState",
        )

        # All other triggers take you from WaitingForLS to WaitingForLS if need be
        self.machine.add_transition(
            trigger="TryPrepareExpressJobs",
            source="WaitingForLS",
            dest="WaitingForLS",
        )
        self.machine.add_transition(
            trigger="TryLaunchExpressJobs",
            source="WaitingForLS",
            dest="WaitingForLS",
        )
        self.machine.add_transition(
            trigger="ContinueToCleanup",
            source="WaitingForLS",
            dest="WaitingForLS",
        )
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="WaitingForLS",
            dest="WaitingForLS",
        )
        
loop = NGTLoopStep2("Thiago")

loop.state

while True:
    while loop.state == "NotRunning":
        time.sleep(1)
        loop.TryStartRun()

    while loop.state == "WaitingForLS":
        loop.TryProcessLS()
        time.sleep(1)
        loop.ContinueAfterCheckLS()
        time.sleep(1)
        loop.TryPrepareExpressJobs()
        time.sleep(1)
        loop.TryLaunchExpressJobs()
        time.sleep(1)
        loop.ContinueToCleanup()
        time.sleep(1)
        loop.ContinueAfterCleanup()
        time.sleep(1)

