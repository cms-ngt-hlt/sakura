# Profiling PCL

In order to have a sound profiling of the throughput of the current RECO+ALCA step used in the Prompt Calibration Loop the following scripts are used.
- `createStep2Config.sh` : creates the configuration to run
- `timing.sh` : runs the timing / throughput jobs


# Recipe

In the scope of [CMSONS-16366](https://its.cern.ch/jira/browse/CMSONS-16366) the measurements were performed on a "Milan" node (2x AMD EPYC "Milan" 7763 processors).

In the specifics the chosen "Milan" node was `devfu-c2b03-44-01.cms`. Some useful information on how to setup the node to be able to run the measurement is [this twiki page](https://twiki.cern.ch/twiki/bin/viewauth/CMS/TriggerDevelopmentWithGPUs).


A `CMSSW` release >= than `CMSSW_15_0_14` is used, and the content of the following PRs is added by hand:
- https://github.com/cms-sw/cmssw/pull/48923
- https://github.com/cms-sw/cmssw/pull/48943

The former is need to make sure it is possible to run the `trackingIters01` in a Run-3 data-taking scenario, while the latter can be used to reduce the amount of duplicated modules in the configuration and reduce the timing of the `ALCAPROMPT` step

```
cmsrel CMSSW_15_0_14
cd CMSSW_15_0_14/src
git cms-addpkg RecoTracker/ConversionSeedGenerators
git cms-addpkg RecoTracker/FinalTrackSelectors
git cms-addpkg RecoTracker/IterativeTracking
git cms-addpkg Alignment/CommonAlignmentProducer
git cms-addpkg Calibration/TkAlCaRecoProducers
git remote add mmusich git@github.com:mmusich/cmssw.git; git fetch mmusich
git cherry-pick 12e9008f02559c454bf54c1aa4dd6c7226309c9c^..75cf61d9d13e7a0321ba057797a2536f8be59f84
git cherry-pick af2cf2560b5951a8f187116f7d8e73961927987d^..fff845e821156cfae8544845da865d00880f0f9d
git clone git@github.com:cms-ngt-hlt/sakura.git
scram b -j
cd sakura/Calibrations/Profiling

# note to see eos on the GPU dev machines you need to
# kinit $USER@CERN.CH

./createStep2Config.sh --PU 60 
./createStep2Config.sh --PU 60 --doTrimming
./timing.sh
```

-----
N.B.: the `timing.sh` script allows to configure the amount of jobs,streams and threads to run.

As `devfu-c2b03-44-01.cms` has 128 cores (with 256 logical threads), to have full machine occupancy we decided to run in the option 32 jobs, 8 streams, 8 threads. The option 64 jobs, 4 streams, 4 threads was also explored, but gave lower overall throughput.
 