# Max Stuff
Here I am going to upload al the important files & scripts from my openlab internship. Pls do not merge yet!

![Schematic overview of the evaluation pipeline](NGT_eval_pipeline.svg "NGT Evaluation Pipeline")


## Running the pipeline
Make sure you have a compatible CMSSW version. We are using **CMSSW_16_0_8**. 

0. Run `cmsenv`.

1. Run `bash ./01_make_config.sh`. Now you should have a `configs/hltDataDump.py` file.

2. Run the following commands. Remember, you have to run them once for every <tag> (`HLT`, `Prompt`, `NGT`):
    ```python3 02_submit.py --tag <tag>```
    this should give you: 
    ```condor_<tag>.sub```
    You have to submit these files manually to HTCondor. But before: 
    * run `vomsi` (or equivalently, `voms-proxy-init --voms cms --valid 168:00`)
    * cp your proxy file in current directory
    * run this command: `module load lxbatch/eossubmit`
    Now run:
    ```condor_submit condor_<tag>.sub```
    You can view the status of your jobs with `condor_q`. Let them rest for a few hours until they are all marked as "Done".

3. Usually, not all jobs will finish without crashing right away. This is why the `03_check.py` script exists. Run: 
    ```python3 03_check.py --tag <tag>```
    This will give you for each <tag> a:
    * `check_report_<tag>.md` - this will give you an overview about all the status of all jobs
    * `resubmit_<tag>.txt` - filelist for all the paths for the jobs that have to be resubmitted
    * `condor_resubmit_<tag>.sub` - HTCondor submission file for all the jobs that crashed
    run:
    ```condor_submit condor_resubmit_<tag>.sub```,
    wait until the jobs are finished and repeat step 3. until all jobs are OK (or the number of crashes stays at least stable) 

4. Now we run the DQM. Since this takes a while, it is recommended to run it in tmux. For this, you have to run `mtmux` (or equivalently, `systemctl --user start tmux.service`). If no tags or streamsi (e.g. `DQMTestDataScouting `, or `LocalTestDataRaw`) are specified via the flags, all tags and streams are run. The command looks like this: 
```tmux new -d -s DQM_scouting 'source /cvmfs/cms.cern.ch/cmsset_default.sh && cmsenv && bash 04_run_dqm.sh --stream DQMTestDataScouting 2>&1 | tee dqm_master.log;exec bash'```

















