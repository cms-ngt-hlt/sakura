#!/usr/bin/env python3

import os, sys, imp, re, pprint, string
from optparse import OptionParser
import FWCore.ParameterSet.Config as cms

MYDIR=os.getcwd()

parser=OptionParser()
parser.add_option("-n",dest="nPerJob",type="int",default=1,help="NUMBER of files per job")
parser.add_option("-q","--flavour",dest="jobFlavour",type="str",default="workday",help="job FLAVOUR")
parser.add_option("-p","--proxy",dest="proxyPath",type="str",default="noproxy",help="Proxy path")
parser.add_option("--inputList", dest="inputList", type="str", default=None, help="Input file list")
parser.add_option("--outPrefix", dest="outPrefix", type="str", default="run", help="Prefix for run number")
# NEW: Dynamic tag (HLT, Prompt, NGT, etc.)
parser.add_option("--jobTag", dest="jobTag", type="str", default="TEST", help="Tag for output naming (HLT, Prompt, etc.)")

opts, args = parser.parse_args()

cfgFileName, cmsEnv, remoteDir = args[0], args[1], args[2]

# Directory setup
if os.path.exists('Jobs'): os.system('rm -rf Jobs')
os.system('mkdir Jobs')

# Load CMSSW process and file list
handle = open(cfgFileName, 'r')
cfo = imp.load_source("pycfg", cfgFileName, handle)
process = cfo.process
handle.close()

with open(opts.inputList, 'r') as f:
    file_paths = [line.strip() for line in f if line.strip()]

nFiles = len(file_paths)
nJobs = (nFiles // opts.nPerJob) + (1 if nFiles % opts.nPerJob > 0 else 0)

for i in range(0, nJobs):
    jobDir = f"{MYDIR}/Jobs/Job_{i}/"
    os.system(f'mkdir {jobDir}')

    with open(f"{jobDir}/sub_{i}.sh", 'w') as tmp_job:
        tmp_job.write("#!/bin/sh\n")
        if opts.proxyPath != "noproxy":
            tmp_job.write(f"export X509_USER_PROXY=$1\n")
        
        tmp_job.write(f"ulimit -v 5000000\ncd $TMPDIR\nmkdir Job_{i}\ncd Job_{i}\n")
        tmp_job.write(f"cd {cmsEnv}\neval `scramv1 runtime -sh`\ncd -\ncp -f {jobDir}* .\n")
        
        # Use a more resilient XRootD redirector if needed inside the run_cfg.py logic
        tmp_job.write("cmsRun run_cfg.py\n")
        
        # UNIVERSAL COPY LOGIC using jobTag
        for ftype in ["Raw", "Scouting"]:
            fname = f"outputLocalTestData{ftype}.root"
            outname = f"{opts.jobTag}_{opts.outPrefix}_job{i}_{ftype}.root"
            tmp_job.write(f"if [ -f {fname} ]; then\n  cp {fname} {remoteDir}/{outname}\nfi\n")
        
        tmp_job.write("rm -f *.root\n")
    
    os.system(f"chmod +x {jobDir}/sub_{i}.sh")
    process.source.fileNames = file_paths[i*opts.nPerJob : (i+1)*opts.nPerJob]
    with open(f"{jobDir}/run_cfg.py", 'w') as f: f.write(process.dumpPython())

# Create Condor JDL
condor_str = f"executable = $(filename)\n"
condor_str += f"arguments = {opts.proxyPath} $(filename) $(ClusterID) $(ProcId)\n" if opts.proxyPath != "noproxy" else "arguments = $(filename) $(ClusterID) $(ProcId)\n"
condor_str += "output = $Fp(filename)hlt.stdout\nerror = $Fp(filename)hlt.stderr\nlog = $Fp(filename)hlt.log\n"


condor_str += f'+JobFlavour = "{opts.jobFlavour}"\nqueue filename matching ({MYDIR}/Jobs/Job_*/*.sh)'

with open("condor_cluster.sub", "w") as f: f.write(condor_str)
