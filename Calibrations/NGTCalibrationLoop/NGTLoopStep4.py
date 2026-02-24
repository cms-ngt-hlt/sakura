#!/usr/bin/env python
# coding: utf-8

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
from transitions import Machine, State

os.environ["COND_AUTH_PATH"] = os.path.expanduser("/nfshome0/sakura")
print("COND_AUTH_PATH set to:", os.environ["COND_AUTH_PATH"])
logging.info("COND_AUTH_PATH set to:", os.environ["COND_AUTH_PATH"])

parser = argparse.ArgumentParser(
    description="Runs step4 of our calibration loop of a given calibration workflow."
)
parser.add_argument(
    "-c",
    "--calibration",
    type=str,
    help="Calibration workflow to process: e.g. SiStripBad or EcalPedestals.",
    required=True,
    choices=["SiStripBad", "EcalPedestals"],
)
args = parser.parse_args()


class NGTLoopStep4(object):
    # Define some states.
    states = [
        State(name="NotRunning", on_enter="ResetTheMachine", on_exit="SetupNewRun"),
        State(name="WaitingForFiles", on_enter="AnnounceWaitingForFiles"),
        State(name="CheckingFilesForProcess", on_enter="CheckFilesForProcessing"),
        State(name="PreparingFiles", on_enter="ExecutePrepareFiles"),
        State(name="PreparingFinalFiles", on_enter="ExecutePrepareFinalFiles"),
        State(name="PreparingHarvestingJobs", on_enter="PrepareHarvestingJobs"),
        State(name="LaunchingHarvestingJobs", on_enter="LaunchHarvestingJobs"),
        State(name="CleanupState", on_enter="ExecuteCleanup"),
    ]

    # We check if a new run appeared, e.g. /tmp/ngt/run386925
    def NewRunAppeared(self):
        print("Checking if a new run appeared")
        logging.info("Checking if a new run appeared")
        path = Path(self.pathWhereFilesAppear)
        currentDirs = {p.name for p in path.iterdir() if p.is_dir()}
        newDirs = currentDirs - self.setOfRunsProcessed
        newRuns = {p for p in newDirs if p.startswith("run")}
        # Thiago: rig to run on 398600
        # newRuns = {p for p in newDirs if p.startswith("run398600")}
        foundNewRuns = bool(newRuns)
        if foundNewRuns:
            print("New runs found!")
            logging.info("New runs found!")
            # What happens if we found more than one run?
            # We figure that out later...
            # Slice off the "run" substring at the beginning
            self.runNumber = (self.GetNextRun(newRuns))[3:]
            print(f"Run {self.runNumber} is available")
            logging.info(f"Run {self.runNumber} is available")
        else:
            print("No new runs...")
            logging.info("No new runs...")

        return foundNewRuns

    # For now, we just take the earliest of the new runs
    def GetNextRun(self, newRuns):
        return sorted(newRuns)[0]

    def SetupNewRun(self):
        # Prepare the new run
        self.workingDir = self.pathWhereFilesAppear + "/run" + self.runNumber
        startTimeFilePath = Path(self.workingDir + "/runStart.log")
        if startTimeFilePath.exists():
            with open(startTimeFilePath, "r", encoding="utf-8") as f:
                runStartLine = f.readline()
                self.startTime = datetime.fromisoformat(runStartLine)
        else:
            # Weird, how come we don't have a runStart.log?
            # Fine, we set the start time to now
            print("We didn't find a runStart.log file... setting run start to NOW")
            logging.info(
                "We didn't find a runStart.log file... setting run start to NOW"
            )
            self.startTime = datetime.now(timezone.utc)

        print(f"Run {self.runNumber} detected, started at {self.startTime.isoformat()}")
        logging.info(
            f"Run {self.runNumber} detected, started at {self.startTime.isoformat()}"
        )

    def AnnounceWaitingForFiles(self):
        print("I am WaitingForFiles...")
        logging.info("I am WaitingForFiles...")

    def RunIsNotComplete(self):
        print("Is the run complete?")
        logging.info("Is the run complete?")
        runEndedFile = Path(self.workingDir + "/runEnd.log")
        if runEndedFile.exists():
            print("The run is complete!")
            logging.info("The run is complete!")
        else:
            print("Not yet...")
            logging.info("Not yet...")
        return not runEndedFile.exists()

    def StillHaveTime(self):
        now_utc = datetime.now(timezone.utc)
        diff = now_utc - self.startTime
        if diff.total_seconds() > self.timeoutInSeconds:
            print("Time ran out!")
            logging.info("Time ran out!")
            return False
        return True

    def CheckFilesForProcessing(self):
        print("I am in CheckFilesForProcessing...")
        logging.info("I am in CheckFilesForProcessing...")
        # Do something to check if there are Files to process
        setOfFilesAvailable = self.GetSetOfAvailableFiles()
        self.setOfFilesObserved = self.setOfFilesObserved.union(setOfFilesAvailable)
        self.setOfFilesToProcess = setOfFilesAvailable - self.setOfFilesProcessed
        self.waitingFiles = len(self.setOfFilesToProcess) > 0
        # Unlike in step2 or step3, here we want to process ALL files together again
        # every time a new appears. So we want self.setOfFilesToProcess to be
        # equal to setOfFilesAvailable.
        self.setOfFilesToProcess = setOfFilesAvailable
        print("New files to process:")
        logging.info("New files to process:")
        print(self.setOfFilesToProcess)
        logging.info(self.setOfFilesToProcess)
        if len(self.setOfFilesToProcess) >= self.minimumFiles:
            self.enoughFiles = True
        else:
            self.enoughFiles = False

    # This function only looks at a given path and lists
    # all available files of the form "PromptCalibProdEcalPedestals.root".
    # Notice, however, that "available" here means
    # "the ROOT files are closed and ready to be used"!
    # So, we list files of the form
    # "ecalPedsStep3_job.txt". If we find those,
    # we lop off that suffix and substitute it for "PromptCalibProdEcalPedestals.root"
    def GetSetOfAvailableFiles(self):
        # For this version, self.pathWhereFilesAppear is the same as
        # self.workingDir
        targetPath = Path(self.workingDir)
        conf = self.calib_config["step_4_config"]
        controlName = conf["step_3_witness_suffix"]
        targetName = conf["step_3_root_filename"]
        setOfControlFiles = set(targetPath.rglob(controlName))
        setOfAvailableFiles = set()
        as_strings = {str(p) for p in setOfControlFiles}
        changed = {
            s[: -len(controlName)] + targetName if s.endswith(controlName) else s
            for s in as_strings
        }
        setOfAvailableFiles = {Path(s) for s in changed}

        return setOfAvailableFiles

    def ExecutePrepareFiles(self):
        print("I am PreparingFiles")
        logging.info("I am PreparingFiles")
        self.PrepareFilesForProcessing()

    def ExecutePrepareFinalFiles(self):
        print("I am PreparingFinalFiles")
        logging.info("I am PreparingFinalFiles")
        self.PrepareFilesForProcessing()
        # Since this is final files, they have to be enough!
        self.preparedFinalFiles = True

    def PrepareFilesForProcessing(self):
        print("I am in PrepareFilesForProcessing...")
        logging.info("I am in PrepareFilesForProcessing...")
        print("Will use the following Files:")
        logging.info("Will use the following Files:")
        # We add here an additional check: do these files all really exist?
        for fileToProcess in self.setOfFilesToProcess:
            if fileToProcess.exists():
                self.setOfInputFiles.add(fileToProcess)

        # So here there's a subtlety: here, all files are processed,
        # but not are them are suitable for Harvesting
        # (e.g., because they don't exist)
        # So we keep track of the two different sets now
        print(self.setOfInputFiles)
        logging.info(self.setOfInputFiles)

    def PrepareHarvestingJobs(self):
        print("I am in PrepareHarvestingjobs...")
        logging.info("I am in PrepareHarvestingjobs...")

        # We may arrive here without a self.setOfInputFiles if
        # the run started and ended without producing Files.
        # In that case, nothing to do
        if not self.setOfInputFiles:
            return

        # Here we should have some logic that prepares the Harvesting jobs
        # Probably should have a call to cmsDriver
        # There are better ways to do this, but right now I just do it with a file

        # First make a particular subdir for us to run in
        alcaJobDir = Path(self.workingDir + "/harvestJob" + f"{self.alcaJobNumber:03}")
        alcaJobDir.mkdir(parents=True, exist_ok=True)
        os.chmod(alcaJobDir, 0o777)
        # Save it so that we can use it later
        self.jobDir = str(alcaJobDir)
        alcaJobFile = alcaJobDir / Path("HARVESTING.sh")

        # At this point, we already increase the self.alcaJobNumber
        self.alcaJobNumber += 1

        conf_step4 = self.calib_config["step_4_config"]
        conf_driver = conf_step4["cms_driver"]
        conf_upload = conf_step4["upload_metadata"]

        # Write the metadata for the upload
        metadata = {
            "destinationDatabase": conf_upload["destinationDatabase"],
            "destinationTags": conf_upload["destinationTags"],
            "inputTag": conf_upload["inputTag"],
            "since": self.runNumber,
            "userText": conf_upload["userText"],
        }
        metadataFile = alcaJobDir / Path(conf_step4["metadata_filename"])
        with open(metadataFile, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        # Write the job file
        python_filename = (
            f"run{self.runNumber}{conf_driver['python_filename_affix']}.py"
        )
        str_paths = ",".join("file:" + str(p) for p in self.setOfInputFiles)
        python_config_mods = "\n".join(conf_driver["python_config_mods"])
        final_db_name = conf_step4["final_db_name"]
        metadata_file = conf_step4["metadata_filename"]

        with alcaJobFile.open("w") as f:
            f.write(
                f"""#!/bin/bash -ex

export $SCRAM_ARCH={self.scramArch}
cd {self.CMSSWPath}/{self.cmsswVersion}/src
cmsenv
cd -

cmsDriver.py expressStep4 --conditions {self.globalTag} \\
-s {conf_driver["step"]} --scenario {conf_driver["scenario"]} --data \\
--filein {str_paths} -n -1 --no_exec --python_filename {python_filename}

cat <<@EOF>> {python_filename}
{python_config_mods}
@EOF

cmsRun {python_filename}

if [ -f "promptCalibConditions.db" ]; then echo "DB file exists!"; else echo "DB file missing"; fi
mv promptCalibConditions.db {final_db_name}
        if [ -f "{metadata_file}" ]; then echo "Metadata file exists!"; \
else echo "Metadata file missing"; fi
uploadConditions.py {final_db_name}

"""
            )

    def LaunchHarvestingJobs(self):
        print("I am in LaunchHarvestingJobs...")
        logging.info("I am in LaunchHarvestingJobs...")

        # Here we should launch the Harvesting jobs
        # We use subprocess.Popen, since we don't want to hang waiting for this
        # to finish running. Some other loop will look at their output
        if self.jobDir != "/dev/null" and len(self.setOfInputFiles) != 0:
            with open(self.jobDir + "/stdout.log", "w", encoding="utf-8") as out:
                with open(self.jobDir + "/stderr.log", "w", encoding="utf-8") as err:
                    subprocess.Popen(
                        ["bash", "HARVESTING.sh"],
                        cwd=self.jobDir,
                        stdout=out,
                        stderr=err,
                        preexec_fn=os.setsid,  # Unix-only; detaches session
                        close_fds=True,
                    )
        else:
            print("WARNING: not launching Harvesting jobs!")
            logging.info("WARNING: not launching Harvesting jobs!")

        # Now we have to move the files we just processed
        # to self.setOfFilesProcessed
        # and clear self.setOfFilesToProcess
        # and setOfInputFiles
        print("Launched jobs with:")
        logging.info("Launched jobs with:")
        print(self.setOfInputFiles)
        logging.info(self.setOfInputFiles)
        self.setOfFilesProcessed = self.setOfFilesProcessed.union(
            self.setOfFilesToProcess
        )
        self.setOfFilesToProcess = set()
        self.setOfInputFiles = set()

    def ThereAreFilesWaiting(self):
        if self.waitingFiles:
            print("++ There are Files waiting!")
            logging.info("++ There are Files waiting!")
        else:
            print("++ No Files waiting...")
            logging.info("++ No Files waiting...")
        return self.waitingFiles

    def ThereAreEnoughFiles(self):
        if self.enoughFiles:
            print("++ Enough input files found!")
            logging.info("++ Enough input files found!")
        else:
            print("++ Not enough input files...")
            logging.info("++ Not enough input files...")
        return self.enoughFiles

    def WePreparedFinalFiles(self):
        return self.preparedFinalFiles

    def ExecuteCleanup(self):
        print("I am in ExecuteCleanup")
        logging.info("I am in ExecuteCleanup")
        if self.preparedFinalFiles:
            print("We prepared final files, will reset the machine...")
            logging.info("We prepared final files, will reset the machine...")
            # We actually have to reset the machine only when we go to NotRunning!

            # Make a log of everything that we did
            with open(self.workingDir + "/allStep3FilesProcessed.log", "w", encoding="utf-8") as f:
                for Files in sorted(self.setOfFilesProcessed):
                    f.write(str(Files) + "\n")
            # Add the run we have just seen to our memory
            # If is easier to just add the "run" prefix here
            self.setOfRunsProcessed.add("run" + self.runNumber)
            print(self.setOfRunsProcessed)
            logging.info(self.setOfRunsProcessed)

    def ResetTheMachine(self):
        print("Machine reset!")
        logging.info("Machine reset!")
        self.runNumber = 0
        self.startTime = 0
        self.timeoutInSeconds = 8 * 60 * 60  # 8 hours
        self.minimumFiles = 1
        self.waitingFiles = False
        self.enoughFiles = False
        self.pathWhereFilesAppear = "/tmp/ngt/"
        self.workingDir = "/dev/null"
        self.jobDir = "/dev/null"
        self.alcaJobNumber = 0
        self.preparedFinalFiles = False
        calibration_config_path = (
            f"/tmp/ngt/calibrationYAML/{self.calibration_name}.yaml"
        )
        with open(calibration_config_path, "r", encoding="utf-8") as f:
            self.calib_config = yaml.safe_load(f)
        self.CMSSWPath = self.calib_config["step_4_config"]["cmssw_base_path"]

        # Read some configurations
        with open(f"{self.pathWhereFilesAppear}/ngtParameters.jsn", "r", encoding="utf-8") as f:
            config = json.load(f)
        self.scramArch = config["SCRAM_ARCH"]
        self.cmsswVersion = config["CMSSW_VERSION"]
        self.globalTag = config["GLOBAL_TAG"]

        self.setOfFilesObserved = set()
        self.setOfFilesToProcess = set()
        self.setOfInputFiles = set()
        self.setOfFilesProcessed = set()
        self.setOfExpectedOutputs = set()

    def __init__(self, name):

        # No anonymous FSMs in my watch!
        self.name = name
        self.calibration_name = args.calibration
        print(f"We are processing {self.calibration_name}.")
        logging.info(f"We are processing {self.calibration_name}.")
        self.setOfRunsProcessed = set()
        self.ResetTheMachine()

        # Initialize the state machine
        self.machine = Machine(
            model=self, states=NGTLoopStep4.states, queued=True, initial="NotRunning"
        )

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # If we're not running, try to start running
        self.machine.add_transition(
            trigger="TryLookForRun",
            source="NotRunning",
            dest="WaitingForFiles",
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
        # Otherwise, we go back to WaitingForFiles
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="CleanupState",
            dest="WaitingForFiles",
        )

        # This is the inner loop. We go from "WaitingForFiles"
        # to the "CheckingFilesForProcess", and from there we
        # will go to one of three states
        self.machine.add_transition(
            trigger="TryProcessFiles",
            source="WaitingForFiles",
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
        # more Files will come. We go to WaitingForFiles,
        # but only if we still have time!
        self.machine.add_transition(
            trigger="ContinueAfterCheckFiles",
            source="CheckingFilesForProcess",
            dest="WaitingForFiles",
            conditions=["RunIsNotComplete", "StillHaveTime"],
        )

        # If we don't have enough Files, and we are not still running,
        # no more Files will come. We go to PreparingFinalFiles
        self.machine.add_transition(
            trigger="ContinueAfterCheckFiles",
            source="CheckingFilesForProcess",
            dest="PreparingFinalFiles",
        )

        # In any case, prepare the Harvesting jobs
        self.machine.add_transition(
            trigger="TryPrepareHarvestingJobs",
            source="PreparingFiles",
            dest="PreparingHarvestingJobs",
        )
        self.machine.add_transition(
            trigger="TryPrepareHarvestingJobs",
            source="PreparingFinalFiles",
            dest="PreparingHarvestingJobs",
        )

        # And launch them!
        self.machine.add_transition(
            trigger="TryLaunchHarvestingJobs",
            source="PreparingHarvestingJobs",
            dest="LaunchingHarvestingJobs",
        )
        self.machine.add_transition(
            trigger="ContinueToCleanup",
            source="LaunchingHarvestingJobs",
            dest="CleanupState",
        )

        # All other triggers take you from WaitingForFiles to WaitingForFiles if need be
        self.machine.add_transition(
            trigger="TryPrepareHarvestingJobs",
            source="WaitingForFiles",
            dest="WaitingForFiles",
        )
        self.machine.add_transition(
            trigger="TryLaunchHarvestingJobs",
            source="WaitingForFiles",
            dest="WaitingForFiles",
        )
        self.machine.add_transition(
            trigger="ContinueToCleanup",
            source="WaitingForFiles",
            dest="WaitingForFiles",
        )
        self.machine.add_transition(
            trigger="ContinueAfterCleanup",
            source="WaitingForFiles",
            dest="WaitingForFiles",
        )


# --- NEW LOGGING SETUP ---
# Create /tmp/ngt if it doesn't exist, so we can write the log file
Path("/tmp/ngt").mkdir(parents=True, exist_ok=True)

# Get the main logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Capture everything at logger level

# Create formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# 1. ALL MESSAGES - Complete history
all_handler = logging.FileHandler("/tmp/ngt/NGTLoopStep4_ALL.log")
all_handler.setLevel(logging.DEBUG)
all_handler.setFormatter(formatter)
logger.addHandler(all_handler)

# 2. INFO ONLY
info_handler = logging.FileHandler("/tmp/ngt/NGTLoopStep4_INFO.log")
info_handler.setLevel(logging.INFO)
info_handler.addFilter(lambda record: record.levelno == logging.INFO)  # ONLY info
info_handler.setFormatter(formatter)
logger.addHandler(info_handler)

# 3. WARNING ONLY
warning_handler = logging.FileHandler("/tmp/ngt/NGTLoopStep4_WARNING.log")
warning_handler.setLevel(logging.WARNING)
warning_handler.addFilter(
    lambda record: record.levelno == logging.WARNING
)  # ONLY warnings
warning_handler.setFormatter(formatter)
logger.addHandler(warning_handler)

# 4. ERROR ONLY
error_handler = logging.FileHandler("/tmp/ngt/NGTLoopStep4_ERROR.log")
error_handler.setLevel(logging.ERROR)
error_handler.addFilter(lambda record: record.levelno == logging.ERROR)  # ONLY errors
error_handler.setFormatter(formatter)
logger.addHandler(error_handler)

# 5. CRITICAL ONLY
critical_handler = logging.FileHandler("/tmp/ngt/NGTLoopStep4_CRITICAL.log")
critical_handler.setLevel(logging.CRITICAL)
critical_handler.addFilter(
    lambda record: record.levelno == logging.CRITICAL
)  # ONLY critical
critical_handler.setFormatter(formatter)
logger.addHandler(critical_handler)

# 6. Screen output (stderr) - warnings and above
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Optional: Add a simple startup message to verify logging is working
logging.info("Logging initialized - writing to split log files")
logging.warning("Warning-level logging active")
# --- END OF ENHANCED LOGGING SETUP ---

loop = NGTLoopStep4("Step4")

loop.state

SLEEP_TIME = 60

while True:
    while loop.state == "NotRunning":
        time.sleep(
            SLEEP_TIME
        )  # Should be close to 60 for deployment, close to 1 for testing
        loop.TryLookForRun()

    while loop.state == "WaitingForFiles":
        loop.TryProcessFiles()
        time.sleep(SLEEP_TIME)
        loop.ContinueAfterCheckFiles()
        time.sleep(SLEEP_TIME)
        loop.TryPrepareHarvestingJobs()
        time.sleep(SLEEP_TIME)
        loop.TryLaunchHarvestingJobs()
        time.sleep(SLEEP_TIME)
        loop.ContinueToCleanup()
        time.sleep(SLEEP_TIME)
        loop.ContinueAfterCleanup()
        time.sleep(SLEEP_TIME)
