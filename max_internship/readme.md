# Max Stuff
Here I am going to upload al the important files & scripts from my openlab internship. Pls do not merge yet!
Snapshot time is not handled correctly yet. 

![Schematic overview of the evaluation pipeline](NGT_eval_pipeline.svg "NGT Evaluation Pipeline")


## Running the pipeline
Make sure you have a compatible CMSSW version. We are using **CMSSW_16_0_8**. 
0. run `cmsenv`.
1. run `bash ./01_make_config.sh`. Now you should have a `configs/hltDataDump.py` file 
2. run 
    ```
    python3 02_submit.py --tag HLT
    python3 02_submit.py --tag Prompt
    python3 02_submit.py --tag NGT
    ```
    this should give you three files: 
    ```
    condor_HLT.sub
    condor_Prompt.sub
    condor_NGT.sub
    ```
    You have to submit these files manually to HTCondor. But before: 
    * run `vomsi`
    * cp your proxy file in current directory
    * run this: `module load lxbatch/eossubmit`
    Now run:
    ```
    condor_submit condor_HLT.sub
    condor_submit condor_Prompt.sub
    condor_submit condor_NGT.sub
    ```
    You can view the status of your jobs with `condor_q`. Let them rest for a few hours until they are all marked as "Done".
