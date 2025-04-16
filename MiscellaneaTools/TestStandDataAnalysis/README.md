# TestStandDataAnalysis

```bash
cmsrel CMSSW_15_0_4
cd CMSSW_15_0_4/src/
cmsenv
scram b -j 8
wget https://raw.githubusercontent.com/mmusich/NGT-Task-3.4/refs/heads/main/TestStandDataAnalysis/testStand.sh .
./testStand.sh
wget https://raw.githubusercontent.com/sanuvarghese/L1PhysicsSkim/refs/heads/main/L1PhysicsFilter/test/cmsCondorData.py
cp -pr /tmp/x509up_u* .
edmConfigDump hltData.py > dump.py
python3 cmsCondorData.py dump.py $PWD /eos/cms/store/group/tsg-phase2/user/musich/test_out/ -p $PWD/x509up_u* -q espresso -n 20
condor_submit condor_cluster.sub
```