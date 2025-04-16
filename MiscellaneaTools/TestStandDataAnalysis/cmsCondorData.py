#!/usr/bin/env python3

import os, sys,  imp, re, pprint, string
from optparse import OptionParser

# cms specific
import FWCore.ParameterSet.Config as cms

import time
import datetime
import os
import sys

MYDIR=os.getcwd()

#get inputs
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-n",dest="nPerJob",type="int",default=1,help="NUMBER of files processed per job",metavar="NUMBER")
parser.add_option("-q","--flavour",dest="jobFlavour",type="str",default="workday",help="job FLAVOUR",metavar="FLAVOUR")
parser.add_option("-p","--proxy",dest="proxyPath",type="str",default="noproxy",help="Proxy path")

opts, args = parser.parse_args()


help_text = '\n./cmsCondor.py <cfgFileName> <CMSSWrel> <remoteDir> -p <proxyPath> -n <nPerJob> -q <jobFlavour>'
help_text += '\n<cfgFileName> (mandatory) = name of your configuration file (e.g. hlt_config.py)'
help_text += '\n<CMSSWrel> (mandatory) = directory where the top of a CMSSW release is located'
help_text += '\n<remoteDir> (mandatory) = directory where the files will be transfered (e.g. on EOS)'
help_text += '\n<proxyPath> (optional) = location of your voms cms proxy. Note: keep your proxy in a private directory.'
help_text += '\n<nPerJob> (optional) = number of files processed per batch job (default=5)'
help_text += '\n<flavour> (optional) = job flavour (default=workday)\n'


cfgFileName = str(args[0])
cmsEnv = str(args[1])
remoteDir = str(args[2])

print('config file = %s'%cfgFileName)
print('CMSSWrel = %s'%cmsEnv)
print('proxy = %s'%opts.proxyPath)
print('remote directory = %s'%remoteDir)
print('job flavour = %s'%opts.jobFlavour)


#make directories for the jobs
try:
    os.system('rm -rf Jobs')
    os.system('mkdir Jobs')
except:
    print("err!")
    pass


sub_total = open("sub_total.jobb","w")


# load cfg script
handle = open(cfgFileName, 'r')
cfo = imp.load_source("pycfg", cfgFileName, handle)
process = cfo.process
handle.close()

# keep track of the original source
fullSource = process.source.clone()


nJobs = -1

try:
    process.source.fileNames
except:
    print('No input file. Exiting.')
    sys.exit(2)
else:
    print("Number of files in the source:",len(process.source.fileNames), ":")
    pprint.pprint(process.source.fileNames)
   
    nFiles = len(process.source.fileNames)
    nJobs = int(nFiles / opts.nPerJob)
    if (nJobs!=0 and (nFiles % opts.nPerJob) > 0) or nJobs==0:
        nJobs = nJobs + 1
      
    print("number of jobs to be created: ", nJobs)
    




k=0
loop_mark = opts.nPerJob
#make job scripts
for i in range(0, nJobs):
    #print 'total: %d/%d  ;  %.1f %% processed '%(j,my_sum,(100*float(j)/float(my_sum)))

    jobDir = MYDIR+'/Jobs/Job_%s/'%str(i)
    os.system('mkdir %s'%jobDir)

    tmp_jobname="sub_%s.sh"%(str(i))
    tmp_job=open(jobDir+tmp_jobname,'w')
    tmp_job.write("#!/bin/sh\n")
    if opts.proxyPath != "noproxy":
        tmp_job.write("export X509_USER_PROXY=$1\n")
        tmp_job.write("voms-proxy-info -all\n")
        tmp_job.write("voms-proxy-info -all -file $1\n")
    tmp_job.write("ulimit -v 5000000\n")
    tmp_job.write("cd $TMPDIR\n")
    tmp_job.write("mkdir Job_%s\n"%str(i))
    tmp_job.write("cd Job_%s\n"%str(i))
    tmp_job.write("cd %s\n"%(cmsEnv))
    tmp_job.write("eval `scramv1 runtime -sh`\n")
    tmp_job.write("cd -\n")
    tmp_job.write("cp -f %s* .\n"%(jobDir))
    tmp_job.write("cmsRun run_cfg.py\n")
    tmp_job.write("echo 'sending the file back'\n")
    tmp_job.write("cp outputLocalTestDataScouting.root %s/outputLocalTestDataScouting_%s.root\n"%(remoteDir, str(i)))
    tmp_job.write("rm outputLocalTestDataScouting.root \n")
    tmp_job.close()
    os.system("chmod +x %s"%(jobDir+tmp_jobname))

    print("preparing job number %s/%s"%(str(i), nJobs-1))

    iFileMin = i*opts.nPerJob
    iFileMax = (i+1)*opts.nPerJob
          
    process.source.fileNames = fullSource.fileNames[iFileMin:iFileMax]
          
    tmp_cfgFile = open(jobDir+'/run_cfg.py','w')
    tmp_cfgFile.write(process.dumpPython())
    tmp_cfgFile.close()
    


condor_str = "executable = $(filename)\n"
if opts.proxyPath != "noproxy":
    condor_str += "Proxy_path = %s\n"%opts.proxyPath
    condor_str += "arguments = $(Proxy_path) $Fp(filename) $(ClusterID) $(ProcId)\n"
else:
    condor_str += "arguments = $Fp(filename) $(ClusterID) $(ProcId)\n"
condor_str += "output = $Fp(filename)hlt.stdout\n"
condor_str += "error = $Fp(filename)hlt.stderr\n"
condor_str += "log = $Fp(filename)hlt.log\n"
condor_str += '+JobFlavour = "%s"\n'%opts.jobFlavour
condor_str += "queue filename matching ("+MYDIR+"/Jobs/Job_*/*.sh)"
condor_name = MYDIR+"/condor_cluster.sub"
condor_file = open(condor_name, "w")
condor_file.write(condor_str)
sub_total.write("condor_submit %s\n"%condor_name)
os.system("chmod +x sub_total.jobb")
