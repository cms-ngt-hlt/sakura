### How to run the modifications
## Environment
To set up the area and get Marco's branch:

```
cmsrel CMSSW_15_0_13_patch2
cd CMSSW_15_0_13_patch2/src
cmsenv
git cms-merge-topic mmusich:fix_trackingIters01_Run3
scram b -j 

```

## Get payloads
Here the recipe to use the scripts
# AlcaProducer
To get the AlcaProducer steps, using step2.sh:
```
./step2.sh
```
which as an output will give `step2.root` and `expressStep2_RAW2DIGI_RECO_ALCAPRODUCER.py` (which is the file that will is executed within the bash script.

# AlcaOutput
One can simply use the script again:
```
./step3.sh
```
which as an output will give `step3_ALCAOUTPUT_ALCA.py` (which is executed within the script) and one it's executed, it will give out several `*.root` and `*.dat`. `PromptCalibProd.root` is related to BeamSpot while `SiStripQualit.root` and `PromptCalibProdSiStrip.root` is related to SiStripQuality.

# AlcaHarvest
This last step produces the `.db`-files from which we can read the payloads from ! 

```
./step4.sh 
```
and to see the payloads:

```
conddb --db promptCalibConditions.db list SiStripBadStrip_pcl
```

To do the same thing with the beamspot, we use
```
`./step4_BS.sh
conddb --db promptCalibConditions.db list BeamSpotObject_ByRun
```
and it will print out the payloads ! :)

In case you want to check what you have already harvested on, one can run:
```
conddb --db promptCalibConditions.db listTags
```

