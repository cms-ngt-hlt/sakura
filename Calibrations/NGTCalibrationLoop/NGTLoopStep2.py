#!/usr/bin/env python
# coding: utf-8

# In[1]:


from transitions import Machine, State
import random
import time
from pathlib import Path


# In[2]:


class NGTLoopStep2(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = [
        State(
            name="NotRunning", on_enter="AnnounceRunStop", on_exit="AnnounceRunStart"
        ),
        State(name="Running", on_enter="AnnounceRunning"),
        State(name="CheckingLSForProcess", on_enter="CheckLSForProcessing"),
        State(name="PreparingExpressJobs", on_enter="PrepareExpressJobs"),
        State(name="LaunchingExpressJobs", on_enter="LaunchExpressJobs"),
        State(name="CheckingForRunFinish"),
        State(name="PreparingALCAOUTPUT"),
        State(name="LaunchingALCAOUTPUT"),
    ]

    def AnnounceRunStart(self):
        runNumber = self.runNumber
        print(f"Run {runNumber} has started!")

    def AnnounceRunning(self):
        print("I am in Running...")

    def AnnounceRunStop(self):
        print("The run stopped...")

    def DAQIsRunning(self):
        print("Testing if DAQ is running...")
        weAreRunning = Path("running.txt").exists()
        if weAreRunning:
            print("Yes, since the file exists!")
            self.runNumber = 386925
        else:
            print("No, the file is missing...")
        return weAreRunning

    def CheckLSForProcessing(self):
        print("I am in CheckLSForProcessing...")
        ### This could be a Luigi task, for instance
        # Do something to check if there are LS to process
        listOfLSFilesAvailable = set(list(Path(".").glob("ls*.txt")))
        self.setOfLSObserved = self.setOfLSObserved.union(listOfLSFilesAvailable)
        self.setOfLSToProcess = listOfLSFilesAvailable - self.setOfLSProcessed
        self.waitingLS = len(self.setOfLSToProcess) > 0
        print("New LSs to process:")
        print(self.setOfLSToProcess)

        # Do something to check if the LSs are enough
        print(len(self.setOfLSToProcess))
        if len(self.setOfLSToProcess) >= self.minimumLS or not self.DAQIsRunning():
            ### If the DAQ is not running we are not getting any more LS, so we just go with these
            self.enoughLS = True
        else:
            self.enoughLS = False

    def PrepareLSForProcessing(self):
        print("I am in PrepareLSForProcessing...")
        print("Will use the following LS:")
        print(self.setOfLSToProcess)
        # Here we could do something interesting,

    def PrepareExpressJobs(self):
        print("I am in PrepareExpressjobs...")
        self.PrepareLSForProcessing()
        # Here we should have some logic that prepares the Express jobsm
        # Probably should have a call to cmsDriver
        self.setOfExpressLS = self.setOfLSToProcess
        self.setOfLSToProcess = set()

    def LaunchExpressJobs(self):
        print("I am in LaunchExpressJobs...")
        # Here we should launch the Express jobs
        # Some other loop will look at their output
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

    def __init__(self, name):

        # No anonymous FSMs in my watch!
        self.name = name
        self.runNumber = 0
        self.startTime = 0
        self.minimumLS = 3
        self.requestMinimumLS = True
        self.waitingLS = False
        self.enoughLS = False

        # What have we accomplished today?
        self.setOfLSObserved = set()
        self.setOfLSToProcess = set()
        self.setOfExpressLS = set()
        self.setOfLSProcessed = set()

        # Initialize the state machine
        self.machine = Machine(
            model=self, states=NGTLoopStep2.states, queued=True, initial="NotRunning"
        )

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.
        self.machine.add_transition(
            trigger="TryStartRun",
            source="NotRunning",
            dest="Running",
            conditions="DAQIsRunning",
        )
        self.machine.add_transition(
            trigger="TryStartRun", source="NotRunning", dest=None
        )
        self.machine.add_transition(
            trigger="TryStopRun", source="Running", dest="NotRunning"
        )

        self.machine.add_transition(
            trigger="TryProcessLS", source="Running", dest="CheckingLSForProcess"
        )

        self.machine.add_transition(
            trigger="TryPrepareExpressJobs",
            source="*",
            dest="PreparingExpressJobs",
            conditions=["ThereAreLSWaiting", "ThereAreEnoughLS"],
        )
        ###  If there are no LS waiting or not enough LS, the transition above will not trigger.
        ### So we have to use the next one, and go back to running
        self.machine.add_transition(
            trigger="TryPrepareExpressJobs", source="*", dest="Running"
        )

        self.machine.add_transition(
            trigger="TryLaunchExpressJobs",
            source="PreparingExpressJobs",
            dest="LaunchingExpressJobs",
        )
        ### If we didn't prepare the jobs, we have to go back and try to prepare them
        self.machine.add_transition(
            trigger="TryLaunchExpressJobs", source="*", dest="PreparingExpressJobs"
        )

        self.machine.add_transition(
            trigger="ContinueAfterLaunchingExpress",
            source="LaunchingExpressJobs",
            dest="Running",
            conditions="DAQIsRunning",
        )
        ###  If DAQ is not running, the transition above will not trigger.
        ### So we will check if there are (final) LS waiting and send jobs.
        self.machine.add_transition(
            trigger="ContinueAfterLaunchingExpress",
            source="LaunchingExpressJobs",
            dest="PreparingExpressJobs",
            conditions="ThereAreLSWaiting",
        )

        ### If this triggers, might

        ### If we are running but there are no LS yet,
        ### just go back to 'Running', inconditionally.
        ### The loop continues from there
        ### The "DAQIsRunning" condition is self-consistent
        self.machine.add_transition(
            trigger="ContinueAfterLaunchingExpress", source="*", dest="Running"
        )


# In[3]:


loop = NGTLoopStep2("Thiago")


# In[4]:


loop.state


# In[5]:


while True:
    while loop.state == "NotRunning":
        time.sleep(1)
        loop.TryStartRun()

    while loop.state == "Running":
        loop.TryProcessLS()
        time.sleep(1)
        loop.TryPrepareExpressJobs()
        time.sleep(1)
        loop.TryLaunchExpressJobs()
        time.sleep(1)
        loop.ContinueAfterLaunchingExpress()
        time.sleep(1)

    loop.to_NotRunning()
