# Max Stuff
Here I am going to upload al the important files & scripts from my openlab internship. Pls do not merge yet!

![Schematic overview of the evaluation pipeline](NGT_eval_pipeline.svg "NGT Evaluation Pipeline")


## Running the pipeline
Make sure you have a compatible CMSSW version. We are using **CMSSW_16_0_8**. 
0. run `cmsenv`.
1. run `bash ./01_make_config.sh`. Now you should have a `configs/hltDataDump.py` file 
2. run the following commands. Remember, you have to run them once for every <tag> (`HLT`, `Prompt`, `NGT`):
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
3.  Usually, not all jobs will finish without crashing right away. This is why the `03_check.py` script exists. Run: 
    ```python3 03_check.py --tag <tag>```
    This will give you for each <tag> a:
    * `check_report_<tag>.md` - this will give you an overview about all the status of all jobs
    * `resubmit_<tag>.txt` - filelist for all the paths for the jobs that have to be resubmitted
    * `condor_resubmit_<tag>.sub - HTCondor submission file for all the jobs that crashed
    run:
    ```condor_submit condor_resubmit_<tag>.sub```,
    wait until the jobs are finished and repeat step 3. until all jobs are OK. 
