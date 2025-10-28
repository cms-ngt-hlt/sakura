#!/usr/bin/env python
# coding: utf-8

import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

from transitions import Machine, State
from omsapi import OMSAPI

CURRENT_RUN = ""
LAST_LS = None


class NGTLoopStep2(object):

    # Define some states.
    states = [
        State(name="NotRunning", on_enter="ResetTheMachine", on_exit="ExecuteRunStart"),
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
        print(f"Started processing run {runNumber}!")
        # We live in directory /tmp/ngt.
        p = Path(f"/tmp/ngt/run{runNumber}")
        p.mkdir(parents=True, exist_ok=True)
        os.chmod(p, 0o777)
        self.workingDir = str(p)
        # We assert the run start time for us as "now" in UTC
        with open(self.workingDir + "/runStart.log", "w") as f:
            f.write(datetime.now(timezone.utc).isoformat())

    def AnnounceWaitingForLS(self):
        print("I am WaitingForLS...")

    def AnnounceRunStop(self):
        print("The run stopped...")

    def LastLSRunNumber(self, runnum):
        omsapi = OMSAPI("https://cmsoms.cms/agg/api", "v1", cert_verify=False)
        q = omsapi.query("runs")
        q.filter("run_number", runnum)
        try:
            response = q.data().json()
        except Exception as e:
            print(f"Warning: OMS query for run {runnum} failed. Returning LS 0.")
            return 0
        run_info = response["data"][0]["attributes"]
        last_ls = run_info.get("last_lumisection_number")
        return int(last_ls)

    def LSavailable(self):
        availableFiles = self.GetListOfAvailableFiles()
        ls_numbers = set()
        for file_path in availableFiles:
            result = self.edmFileUtilCommand(file_path)
            for match in re.finditer(
                r"^\s*\d+\s+(\d+)\s+", result.stdout, re.MULTILINE
            ):
                ls_numbers.add(int(match.group(1)))
        max_ls = max(
            ls_numbers, default=0
        )  # default to 0 bc if there are none it will crash this function
        return max_ls

    def WeStillHaveTime(self):
        now_utc = datetime.now(timezone.utc)
        delta = now_utc - self.runStartTime
        if int(delta.total_seconds()) < int(self.maxLatchTime * 60 * 60):
            print(
                f"We still have time: {int(self.maxLatchTime * 60 * 60) - int(delta.total_seconds())} seconds"
            )
            print(delta.total_seconds())
        else:
            print("Time is up!")
        return delta.total_seconds() < (self.maxLatchTime * 60 * 60)

    def CalFuProcessed(self, run_number):

        # this whole omsapi block does not need to be repeated so often lol
        now_utc = datetime.now(timezone.utc)
        delta = now_utc - self.runStartTime
        hours_elapsed = delta.total_seconds() / 3600

        if not self.WeStillHaveTime():
            print(
                f"It has been {hours_elapsed} h since the run started, this exceeds the maximum latch time of {self.maxLatchTime} h."
            )
            return True
        else:
            print(
                f"We will spend {self.maxLatchTime-hours_elapsed:.1f} more hours in this run before proceeding to the next one."
            )

        ### Thiago: what does this do?
        LastLS_OMS = self.LastLSRunNumber(run_number)
        LastLS_available = self.LSavailable()
        return abs(int(LastLS_OMS) - int(LastLS_available)) <= int(LastLS_OMS * 0.04)

    def RunHasEndedAndFilesAreReady(self):
        if self.DAQIsRunning():
            return False
        if self.runNumber == 0:
            return False

        print(
            f"Run {self.runNumber} has ended. Checking if all files are available before going to next run..."
        )
        all_files_ready = self.CalFuProcessed(self.runNumber)

        if all_files_ready:
            print("All files available!")
        else:
            print(
                "Run ended, but we are still waiting for all the files to be processed"
            )
        return all_files_ready

    def DAQIsRunning(self):
        global CURRENT_RUN, LAST_LS
        print("Checking DAQ status via OMS...")
        omsapi = OMSAPI("https://cmsoms.cms/agg/api", "v1", cert_verify=False)

        if self.runNumber == 0:
            # ---
            # --- STATE 1: NOT LATCHED. Find the LATEST PROTONS run.
            # ---
            print("Currently NotRunning. Looking for the most recent PROTONS run...")
            q = omsapi.query("runs")

            # --- THIS IS THE NEW, MORE ROBUST FILTER ---
            q.filter("fill_type_runtime", "PROTONS")
            q.filter("l1_hlt_mode", "collisions2025")
            # --- END NEW FILTER ---

            # Sort by run number and get the top one
            q.sort("run_number", asc=False).paginate(page=1, per_page=1)
            response = q.data().json()

            if "data" not in response or not response["data"]:
                print("No PROTONS *collisions* runs found in OMS. Waiting.")
                return False  # Stay in NotRunning

            # This is the latest *collisions* run
            run_info = response["data"][0]["attributes"]
            run_number = run_info.get("run_number")
            run_type = run_info.get("l1_hlt_mode")  # We can just grab this for logging
            is_running = run_info.get("end_time") is None
            last_ls = run_info.get("last_lumisection_number")
            self.runStartTime = datetime.fromisoformat(
                run_info.get("start_time").replace("Z", "+00:00")
            )
            if not is_running and last_ls < self.minLSToProcess:
                print(
                    f"Found ended run {run_number}, but it's too short ({last_ls} LS). Skipping and waiting."
                )
                return False

            ### Thiago: Rig it to run over 398593
            # if(self.rigMe == True):
            #    run_number = "398593"
            #    run_type = "collisions2025"

            print(f"Found latest PROTONS run: {run_number} (type: {run_type})")

            # --- LATCH THE RUN ---
            self.runNumber = run_number
            # Set the globals
            LAST_LS = last_ls  # run_info.get("last_lumisection_number")

            run_str = str(self.runNumber)
            if len(run_str) == 6:
                CURRENT_RUN = f"{run_str[:3]}/{run_str[3:]}"
            else:
                CURRENT_RUN = run_str

            print(f"LATCHED run: {CURRENT_RUN}, last LS: {LAST_LS}")

            # Set the path for GetListOfAvailableFiles
            self.pathWhereFilesAppear = (
                "/eos/cms/tier0/store/data/Run2025G/TestEnablesEcalHcal/RAW/Express-v1/000/"
                + CURRENT_RUN
                + "/00000"
            )

            is_running = run_info.get("end_time") is None
            if is_running:
                # print("DAQ appears to be running!")
                print("Latching onto an ongoing collisions run.")
            else:
                # print("Latching onto a PROTONS run that has already ended.")
                print("Latching onto a collisions run that has already ended.")
            ## This return value tells TryStartRun whether to transition

            # we return true always bc either cases
            return True

        else:
            # ---
            # --- STATE 2: LATCHED. Check status of *our* run.
            # ---
            # (This part was already working perfectly and remains unchanged)

            print(
                f"Checking status of *our* latched run: {self.runNumber} ({CURRENT_RUN})"
            )

            # Query specifically for our run
            try:  # due to oms specific error recently
                q_our_run = omsapi.query("runs")
                q_our_run.filter("run_number", self.runNumber)
                response_our_run = q_our_run.data().json()
            except Exception as e:
                print(f"Error querying OMS API: {e}")
                return False

            if "data" not in response_our_run or not response_our_run["data"]:
                print(
                    f"Could not find info for *our* run {self.runNumber}. Assuming it ended."
                )
                return False  # Treat our run as finished

            our_run_info = response_our_run["data"][0]["attributes"]

            # Update the global LAST_LS to our run's last LS
            LAST_LS = our_run_info.get("last_lumisection_number")
            is_running = our_run_info.get("end_time") is None

            print(
                f"Our run {self.runNumber}: Last LS is {LAST_LS}. Running: {is_running}"
            )

            return is_running

    def NewRunAvailable(self):
        # We don't want to keep restarting the same run forever
        if self.runNumber != 0:
            end_log_path = Path(f"/tmp/ngt/run{self.runNumber}/runEnd.log")
            if end_log_path.exists():
                print("This is a run we have already treated. No point in restarting")
                return False
            else:  # If we don't find the file, IN PRINCIPLE, a new run exists
                print("Okay, in principle this is a new run!")
                return True
        else:
            # Again, IN PRINCIPLE, a new run exists
            return True

    def edmFileUtilCommand(self, filename):
        # for now it only works with one file, rewrite to also give out for several files..!
        cmd = ["edmFileUtil", "root://eoscms.cern.ch/" + filename, "--eventsInLumi"]
        output = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return output

    def GetRunNumber(self):
        availableFiles = self.GetListOfAvailableFiles()
        result = self.edmFileUtilCommand(availableFiles[0])
        match = re.search(r"^\s*(\d{6})\s+", result.stdout, re.MULTILINE)
        if not match:
            raise RuntimeError(
                f"Could not parse run number from edmFileUtil output:\n{result.stdout}"
            )
        runNumber = int(match.group(1))
        return runNumber

    def CheckLSForProcessing(self):
        print("I am in CheckLSForProcessing...")
        ### This could be a Luigi task, for instance
        # Do something to check if there are LS to process
        listOfLSFilesAvailable = set(self.GetListOfAvailableFiles())

        print("listOfLSFilesAvailable", [str(p) for p in listOfLSFilesAvailable])
        print(50 * "*")

        self.setOfLSObserved = self.setOfLSObserved.union(listOfLSFilesAvailable)
        self.setOfLSToProcess = listOfLSFilesAvailable - self.setOfLSProcessed

        # print("self.setOfLSToProcess",[str(p) for p in self.setOfLSToProcess])
        print(50 * "*")

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
        prefix = "root://eoscms.cern.ch/"

        if not self.pathWhereFilesAppear:
            print("Warning: pathWhereFilesAppear is not set. Cannot list files.")
            return []

        cmd = f"xrdfs {prefix} ls {self.pathWhereFilesAppear}"
        ## Thiago: rig to get only one file
        # if(self.rigMe == True):
        # cmd = "xrdfs root://eoscms.cern.ch/ ls /eos/cms/tier0/store/data/Run2025G/TestEnablesEcalHcal/RAW/Express-v1/000/398/600/00000/e03573bc-978e-4655-909a-15e45ab59a98.root"
        # cmd = "xrdfs root://eoscms.cern.ch ls /eos/cms/tier0/store/data/Run2025G/TestEnablesEcalHcal/RAW/Express-v1/000/398/593/00000/ef4a8d3d-100f-48bc-873e-8e73b0853ef6.root"
        all_files = (
            subprocess.run(cmd, shell=True, capture_output=True, text=True)
            .stdout.strip()
            .splitlines()
        )
        final_list = []
        for file in all_files:
            output = self.edmFileUtilCommand(file)
            if "ERR" in output.stdout:
                print(f"\n Following file won't be processed(skipping): {file}")
            else:
                final_list.append(file)
        return final_list

    def ExecutePrepareLS(self):
        print("I am PreparingLS")
        self.PrepareLSForProcessing()

    def ExecutePrepareFinalLS(self):
        print("I am PreparingFinalLS")
        self.PrepareLSForProcessing()
        self.preparedFinalLS = True

    def PrepareLSForProcessing(self):
        print("I am in PrepareLSForProcessing...")
        print("Will use the following LS:")
        print(self.setOfLSToProcess)

    def PrepareExpressJobs(self):
        print("I am in PrepareExpressjobs...")
        # We may arrive here without a self.setOfLSToProcess if
        # the run started and ended without producing LS.
        # In that case, nothing to do
        if not self.setOfLSToProcess:
            return

        # Thiago: new logic to avoid gigantic cmsRun jobs
        # if(len(self.setOfLSToProcess) > self.maximumFilesPerJob):
        #    as_a_list = sorted(self.setOfLSToProcess)
        #    topTargets = as_a_list[0:self.maximumFilesPerJob]
        #    self.setOfExpressLS = set(topTargets)
        # else:
        #    self.setOfExpressLS = self.setOfLSToProcess

        self.setOfExpressLS = self.setOfLSToProcess
        # Extract all LS numbers (as integers)
        str_paths = {"root://eoscms.cern.ch/" + str(p) for p in self.setOfExpressLS}

        ls_numbers = set()  # use a set to avoid duplicates

        for file_path in str_paths:
            print(file_path)
            cmd = ["edmFileUtil", f"{file_path}", "--eventsInLumi"]

            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            if result.returncode != 0:
                print(f"edmFileUtil failed for")  # {file_path}:\n{result.stderr}")
                continue

            # Find lumisection numbers -- second column in output table
            # Example line: "         398348            187           2268"
            for match in re.finditer(
                r"^\s*\d+\s+(\d+)\s+", result.stdout, re.MULTILINE
            ):
                ls_numbers.add(int(match.group(1)))

        # Convert to sorted list if you want
        ls_numbers = sorted(ls_numbers)

        print(f"Found {len(ls_numbers)} unique lumisections:")
        print(ls_numbers)

        # ls_numbers = [int(re.search(r"ls(\d{4})", path).group(1)) for path in str_paths]

        # Compute min and max, then format back
        min_ls = min(ls_numbers, default=None)
        max_ls = max(ls_numbers, default=None)
        affix = f"LS{min_ls:04d}To{max_ls:04d}"
        logFileName = f"run{self.runNumber}_{affix}_step2.log"
        outputFileName = f"run{self.runNumber}_{affix}_step2.root"

        # Here we should have some logic that prepares the Express jobs
        # Probably should have a call to cmsDriver
        # There are better ways to do this, but right now I just do it with a file
        with open(self.workingDir + "/cmsDriver.sh", "w") as f:
            # Do we actually need to set the environment like this every time?
            f.write("#!/bin/bash -ex\n\n")
            f.write(f"export $SCRAM_ARCH={self.scramArch}\n")
            f.write(f"cmsrel {self.cmsswVersion}\n")
            f.write(f"cd {self.cmsswVersion}/src\n")
            f.write("cmsenv\n")
            f.write("cd -\n\n")
            # Now we do the cmsDriver.py proper
            f.write(f"cmsDriver.py expressStep2 --conditions {self.globalTag} ")
            f.write(
                " -s RAW2DIGI,RECO,ALCAPRODUCER:EcalTestPulsesRaw "
                + "--datatier ALCARECO --eventcontent ALCARECO --data --process RERECO "
                + "--scenario pp --era Run3 "
                + "--nThreads 8 --nStreams 8 -n -1 "
            )
            # and we pass the list of LS to process (self.setOfLSToProcess)
            f.write("--filein ")
            # some massaging to go from PosixPath to string
            str_paths = {"root://eoscms.cern.ch/" + str(p) for p in self.setOfExpressLS}
            f.write(",".join(str_paths))
            f.write(f" --fileout file:{outputFileName} --no_exec ")
            f.write(
                f"--python_filename run{self.runNumber}_{affix}_ecalPedsStep2.py\n\n"
            )
            f.write(
                f"cmsRun run{self.runNumber}_{affix}_ecalPedsStep2.py > {logFileName} 2>&1\n"
            )
            f.write(f"touch run{self.runNumber}_{affix}_ecalPedsStep2_job.txt \n")

        self.setOfExpectedOutputs.add(self.workingDir + "/" + outputFileName)
        self.setOfLSToProcess = set()

    def LaunchExpressJobs(self):
        print("I am in LaunchExpressJobs...")

        # Here we should launch the Express jobs
        # We use subprocess.Popen, since we don't want to hang waiting for this
        # to finish running. Some other loop will look at their output
        # Notice: we only ACTUALLY launch the jobs if we are still treating this run!
        # If we find the magic file runEnd.log, we just do nothing!
        # We have to check this here because we don't want to continuously go through
        # launching jobs if we are forced to go through the PreparingFinalLS path
        end_log_path = Path(self.workingDir) / "runEnd.log"

        if not end_log_path.exists():
            subprocess.Popen(
                ["bash", "cmsDriver.sh"],
                cwd=self.workingDir,
                preexec_fn=os.setsid,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
            )

            # Now we have to move the LSs to self.setOfLSProcessed
            # and clear self.setOfLSToProcess
            print("Launched jobs with:")
            print(self.setOfExpressLS)

        # In any case we remove them from the list
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
        self.rigMe = False
        if self.preparedFinalLS:
            print("We prepared Final LS, will reset the machine...")
            # We actually have to reset the machine only when we go to NotRunning!

            # Announce that the run ended and setup the witness file
            print(
                f"Processing of run {self.runNumber} has ended. Creating empty runEnd.log..."
            )
            end_log_path = Path(self.workingDir) / "runEnd.log"
            end_log_path.touch()
            # Make a log of everything that we did
            with open(self.workingDir + "/allLSProcessed.log", "w") as f:
                for LS in sorted(self.setOfLSProcessed):
                    f.write(str(LS) + "\n")
            with open(self.workingDir + "/expectedOutputs.log", "w") as f:
                for output in self.setOfExpectedOutputs:
                    f.write("file:" + output + "\n")
            # And launch step3 (note: we do not actually launch it here, we just prepare this file)
            with open(self.workingDir + "/ALCAOUTPUT.sh", "w") as f:
                f.write("#!/bin/bash -ex\n\n")
                f.write(f"cd {self.cmsswVersion}/src\n")
                f.write("cmsenv\n")
                f.write("cd -\n\n")
                f.write(f"cmsDriver.py expressStep3 --conditions {self.globalTag} ")
                f.write(
                    " -s ALCAOUTPUT:EcalTestPulsesRaw,ALCA:PromptCalibProdEcalPedestals "
                    + "--datatier ALCARECO --eventcontent ALCARECO "
                    + "--triggerResultsProcess RERECO "
                    + "--nThreads 8 --nStreams 8 -n -1 "
                )
                # and we pass the list of files that we expected
                # FIXME: what if any of those cmsRuns failed?
                f.write("--filein ")
                str_paths = {p for p in sorted(self.setOfExpectedOutputs)}
                f.write(",".join(str_paths))
                f.write(" --no_exec ")
                f.write(
                    f"--python_filename run{self.runNumber}_ecalPedsALCAOUTPUT.py\n\n"
                )
                # Some massaging to fix the source
                f.write(f"cat <<@EOF>> run{self.runNumber}_ecalPedsALCAOUTPUT.py\n")
                f.write(
                    'process.ALCARECOEcalTestPulsesRaw.TriggerResultsTag = cms.InputTag("TriggerResults", "", "RERECO")\n'
                )
                f.write("@EOF\n\n")
                f.write(f"cmsRun run{self.runNumber}_ecalPedsALCAOUTPUT.py &\n")

    def ResetTheMachine(self):
        print("Machine reset!")
        self.runNumber = 0
        self.rigMe = False
        self.startTime = 0
        self.minimumLS = 1  # these variable names are a bit misleading as they are not minimumLS but minimum files availabe (same for the other ones ok)
        self.minLSToProcess = (
            50  # to avoid the continued processing of runs that do not have enough data
        )
        self.maximumFilesPerJob = 5
        self.maxLatchTime = 8  # due to 8 hours of buffering
        self.runStartTime = None
        self.waitingLS = False
        self.enoughLS = False
        self.pathWhereFilesAppear = (
            "/eos/cms/tier0/store/data/Run2025G/TestEnablesEcalHcal/RAW/Express-v1/000/"
            + CURRENT_RUN
            + "/00000"
        )
        print("self.pathWhereFilesAppear", self.pathWhereFilesAppear)
        self.workingDir = "/dev/null"
        self.preparedFinalLS = False
        # Read some configurations
        with open("/tmp/ngt/ngtParameters.jsn", "r") as f:
            config = json.load(f)
        self.scramArch = config["SCRAM_ARCH"]
        self.cmsswVersion = config["CMSSW_VERSION"]
        self.globalTag = config["GLOBAL_TAG"]

        self.setOfLSObserved = set()
        self.setOfLSToProcess = set()
        self.setOfExpressLS = set()
        self.setOfLSProcessed = set()
        self.setOfExpectedOutputs = set()

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
            conditions=["DAQIsRunning", "NewRunAvailable"],
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
            conditions="WePreparedFinalLS",
        )
        # Otherwise, we go back to WaitingForLS
        self.machine.add_transition(
            trigger="ContinueAfterCleanup", source="CleanupState", dest="WaitingForLS"
        )

        # This is the inner loop. We go from "WaitingForLS"
        # to the "CheckingLSForProcess", and from there we
        # will go to one of three states
        self.machine.add_transition(
            trigger="TryProcessLS", source="WaitingForLS", dest="CheckingLSForProcess"
        )

        # If time is up, that's it!
        # Go immediately to PreparingFinalLS to signal to Step3 that we are ready.
        # Notice: we will probably keep running over that run, and that is inneficient.
        # But we do the optimisation later.
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="PreparingFinalLS",
            unless=["WeStillHaveTime"],
        )

        # If we arrived here, we still have time... let's work leisurely.
        # If we have enough LS, process them immediately, we go to PreparingLS
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="PreparingLS",
            conditions=["ThereAreLSWaiting", "ThereAreEnoughLS"],
        )

        # If we don't have enough LS, and we are not still running,
        # no more LS will come. We go to PreparingFinalLS
        # if run is over and we have the files to be processed,
        # we go to PreparingFinalLS (so we can process whatever is left!)
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="PreparingFinalLS",
            # so only if run has ended *and* files are ready, and there is something to process
            conditions=["RunHasEndedAndFilesAreReady", "ThereAreLSWaiting"],
        )

        # i hope this fixes our issue of it needing to go onto another run once 8 hours have passed..
        ### Thiago: I think it didn't :(
        # self.machine.add_transition(
        #        trigger="ContinueAfterCheckLS",
        #        source="CheckingLSForProcess",
        #        dest="CleanupState",
        #        conditions="RunHasEndedAndFilesAreReady",
        #        unless="ThereAreLSWaiting" # Only fires if ThereAreLSWaiting is False
        #        )

        # If we don't have enough LS, but we are still running,
        # We go to WaitingForLS
        self.machine.add_transition(
            trigger="ContinueAfterCheckLS",
            source="CheckingLSForProcess",
            dest="WaitingForLS",
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


loop = NGTLoopStep2("Step2")
# loop.rigMe = True
# loop.maxLatchTime = 5.8
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
