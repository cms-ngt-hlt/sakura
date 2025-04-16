#!/usr/bin/env python

import datetime,time
import os,sys
import string, re
import shlex, shutil, getpass
import subprocess
import configparser as ConfigParser
import json
from optparse import OptionParser

##############################################
def check_proxy():
##############################################
    """Check if GRID proxy has been initialized."""

    try:
        with open(os.devnull, "w") as dump:
            subprocess.check_call(["voms-proxy-info", "--exists"],
                                  stdout = dump, stderr = dump)
    except subprocess.CalledProcessError:
        return False
    return True

##############################################
def forward_proxy(rundir):
##############################################
    """Forward proxy to location visible from the batch system.
    Arguments:
    - `rundir`: directory for storing the forwarded proxy
    """

    if not check_proxy():
        print("Please create proxy via 'voms-proxy-init -voms cms -rfc'.")
        sys.exit(1)

    local_proxy = subprocess.check_output(["voms-proxy-info", "--path"]).strip()
    shutil.copyfile(local_proxy, os.path.join(rundir,".user_proxy"))

##############################################
def getCommandOutput(command):
##############################################
    """This function executes `command` and returns it output.
    Arguments:
    - `command`: Shell command to be invoked by this function.
    """
    child = os.popen(command)
    data = child.read()
    err = child.close()
    if err:
        print('%s failed w/ exit code %d' % (command, err))
    return data

##############################################
def write_HTCondor_submit_file(path, name, nruns, proxy_path=None):
##############################################
    """Writes 'job.submit' file in `path`.
    Arguments:
    - `path`: job directory
    - `script`: script to be executed
    - `proxy_path`: path to proxy (only used in case of requested proxy forward)
    """
        
    job_submit_template="""\
universe              = vanilla
executable            = {script:s}
output                = {jobm:s}/{out:s}.out
error                 = {jobm:s}/{out:s}.err
log                   = {jobm:s}/{out:s}.log
transfer_output_files = ""
+JobFlavour           = "{flavour:s}"
queue {njobs:s}
"""
    if proxy_path is not None:
        job_submit_template += """\
+x509userproxy        = "{proxy:s}"
"""
        
    job_submit_file = os.path.join(path, "job_"+name+".submit")
    with open(job_submit_file, "w") as f:
        f.write(job_submit_template.format(script = os.path.join(path,name+"_$(ProcId).sh"),
                                           out  = name+"_$(ProcId)",
                                           jobm = os.path.abspath(path),
                                           flavour = "tomorrow",
                                           njobs = str(nruns),
                                           proxy = proxy_path))

    return job_submit_file

##### method to parse the input file ################################

def ConfigSectionMap(config, section):
    the_dict = {}
    options = config.options(section)
    for option in options:
        try:
            the_dict[option] = config.get(section, option)
            if the_dict[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            the_dict[option] = None
    return the_dict


###### method to create recursively directories on EOS #############
def mkdir_eos(out_path):
    print("creating",out_path)
    newpath='/'
    for dir in out_path.split('/'):
        newpath=os.path.join(newpath,dir)
        # do not issue mkdir from very top of the tree
        if newpath.find('test_out') > 0:
            command="/afs/cern.ch/project/eos/installation/cms/bin/eos.select mkdir "+newpath
            p = subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (out, err) = p.communicate()
            #print(out,err)
            p.wait()

    # now check that the directory exists
    command2="/afs/cern.ch/project/eos/installation/cms/bin/eos.select ls "+out_path
    p = subprocess.Popen(command2,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = p.communicate()
    p.wait()
    if p.returncode !=0:
        print(out)

def split(sequence, size):
##########################    
# aux generator function to split lists
# based on http://sandrotosi.blogspot.com/2011/04/python-group-list-in-sub-lists-of-n.html
# about generators see also http://stackoverflow.com/questions/231767/the-python-yield-keyword-explained
##########################
    for i in range(0, len(sequence), size):
        yield sequence[i:i+size] 

#############
class Job:
#############

    def __init__(self, job_number, job_id, job_name, GlobalTag, applyEXTRACOND, extraCondVect, CMSSW_dir ,the_dir):
###############################
        self.job_number= job_number
        self.job_id=job_id          
        self.job_name=job_name
        self.GlobalTag         = GlobalTag
        self.applyEXTRACOND    = applyEXTRACOND
        self.extraCondVect     = extraCondVect
    
        self.the_dir=the_dir
        self.CMSSW_dir=CMSSW_dir

        self.output_full_name=self.getOutputBaseName()+"_"+str(self.job_id)
        self.output_number_name=self.getOutputBaseName()+"_"+str(self.job_number)

        self.cfg_dir=None
        self.outputCfgName=None
        
        # LSF variables        
        self.LSF_dir=None
        self.BASH_dir=None
        self.output_LSF_name=None
        self.output_BASH_name=None

        self.lfn_list=list()      

    def __del__(self):
###############################
        del self.lfn_list

    def setEOSout(self,theEOSdir):    
###############################
        self.OUTDIR = theEOSdir
          
    def getOutputBaseName(self):
########################    
        return "myTest_"+self.job_name
        
    def getOutputBaseNameWithData(self):
########################    
        return "myTest_"+self.job_name+"_"+self.data

    def createTheCfgFile(self,lfn):
###############################
        
        # write the cfg file 
        self.cfg_dir = os.path.join(self.the_dir,"cfg")
        if not os.path.exists(self.cfg_dir):
            os.makedirs(self.cfg_dir)

        self.outputCfgName=self.output_full_name+"_cfg.py"
        fout=open(os.path.join(self.cfg_dir,self.outputCfgName),'w')

        ## Reco + TkAlCosmics0T AlCa Stream 
        template_cfg_file = os.path.join(self.the_dir,"NGT-Task-3.4","config.py")
        
        fin = open(template_cfg_file)

        for line in fin.readlines():
            if line.find("GLOBALTAG_TEMPLATE")!=-1:
                line=line.replace("GLOBALTAG_TEMPLATE",self.GlobalTag)     
            
            if 'True' in self.applyEXTRACOND:
                if 'APPEND OF EXTRA CONDITIONS' in line:
                    for element in self.extraCondVect :
                    #print element[0],element[1],element[2]
                        
                        fout.write(" \n")
                        fout.write("process.conditionsIn"+element[0]+"= CalibTracker.Configuration.Common.PoolDBESSource_cfi.poolDBESSource.clone( \n")
                        fout.write("     connect = cms.string('"+element[1]+"'), \n")
                        fout.write("     toGet = cms.VPSet(cms.PSet(record = cms.string('"+element[0]+"'), \n")
                        fout.write("                                tag = cms.string('"+element[2]+"') \n")
                        fout.write("                                ) \n")
                        fout.write("                       ) \n")
                        fout.write("     ) \n")
                        fout.write("process.prefer_conditionsIn"+element[0]+" = cms.ESPrefer(\"PoolDBESSource\", \"conditionsIn"+element[0]+"\") \n \n") 
                        
            if line.find("FILEINPUT_TEMPLATE")!=-1:
                lfn_with_quotes = map(lambda x: "\'"+x+"\'",lfn)                   
                #print "["+",".join(lfn_with_quotes)+"]"
                line=line.replace("FILEINPUT_TEMPLATE","["+",".join(lfn_with_quotes)+"]") 
            if line.find("OUTFILE_TEMPLATE")!=-1:
                line=line.replace("OUTFILE_TEMPLATE",self.output_full_name+".root")     
            fout.write(line)    
      
        fout.close()                
                          
    def createTheLSFFile(self):
###############################

       # directory to store the LSF to be submitted
        self.LSF_dir = os.path.join(self.the_dir,"LSF")
        if not os.path.exists(self.LSF_dir):
            os.makedirs(self.LSF_dir)

        self.output_LSF_name=self.output_full_name+".lsf"
        fout=open(os.path.join(self.LSF_dir,self.output_LSF_name),'w')
    
        job_name = self.output_full_name

        log_dir = os.path.join(self.the_dir,"log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        fout.write("#!/bin/sh \n") 
        fout.write("#BSUB -L /bin/sh\n")       
        fout.write("#BSUB -J "+job_name+"\n")
        fout.write("#BSUB -o "+os.path.join(log_dir,job_name+".log")+"\n")
        fout.write("#BSUB -q cmscaf1nd \n")
        fout.write("JobName="+job_name+" \n")
        fout.write("OUT_DIR="+self.OUTDIR+" \n")
        fout.write("LXBATCH_DIR=`pwd` \n") 
        fout.write("cd "+os.path.join(self.CMSSW_dir,"src")+" \n")
        fout.write("eval `scram runtime -sh` \n")
        fout.write("cd $LXBATCH_DIR \n") 
        fout.write("cmsRun "+os.path.join(self.cfg_dir,self.outputCfgName)+" \n")
        fout.write("ls -lh . \n")
        fout.write("for RootOutputFile in $(ls *root |grep myTest ); do xrdcp -f ${RootOutputFile}  ${OUT_DIR}/${RootOutputFile} ; done \n")
        fout.write("for TxtOutputFile in $(ls *txt ); do xrdcp -f ${TxtOutputFile}  ${OUT_DIR}/${TxtOutputFile} ; done \n")

        fout.close()

    def createTheBashFile(self):
###############################

       # directory to store the BASH to be submitted
        self.BASH_dir = os.path.join(self.the_dir,"BASH")
        if not os.path.exists(self.BASH_dir):
            os.makedirs(self.BASH_dir)

        self.output_BASH_name=self.output_number_name+".sh"
        fout=open(os.path.join(self.BASH_dir,self.output_BASH_name),'w')
    
        job_name = self.output_full_name

        log_dir = os.path.join(self.the_dir,"log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        fout.write("#!/bin/bash \n")
        #fout.write("export EOS_MGM_URL=root://eoscms.cern.ch \n")
        fout.write("JobName="+job_name+" \n")
        fout.write("export X509_USER_PROXY="+os.path.join(self.CMSSW_dir,"src")+"/.user_proxy \n")
        fout.write("echo  \"Job started at \" `date` \n")
        fout.write("CMSSW_DIR="+os.path.join(self.CMSSW_dir,"src")+" \n")
        fout.write("OUT_DIR="+self.OUTDIR+" \n")
        fout.write("LXBATCH_DIR=$PWD \n") 
        #fout.write("cd "+os.path.join(self.CMSSW_dir,"src")+" \n")
        fout.write("cd ${CMSSW_DIR} \n")
        fout.write("eval `scramv1 runtime -sh` \n")
        fout.write("echo \"batch dir: $LXBATCH_DIR release: $CMSSW_DIR release base: $CMSSW_RELEASE_BASE\" \n") 
        fout.write("cd $LXBATCH_DIR \n") 
        fout.write("cp "+os.path.join(self.cfg_dir,self.outputCfgName)+" . \n")
        fout.write("echo \"cmsRun "+self.outputCfgName+"\" \n")
        fout.write("cmsRun "+self.outputCfgName+" \n")
        fout.write("echo \"Content of working dir is \"`ls -lh` \n")
        #fout.write("less condor_exec.exe \n")
        fout.write("for RootOutputFile in $(ls *root ); do xrdcp -f ${RootOutputFile} root://eoscms/${OUT_DIR}/${RootOutputFile} ; done \n")
        #fout.write("mv ${JobName}.out ${CMSSW_DIR}/BASH \n")
        fout.write("echo  \"Job ended at \" `date` \n")
        fout.write("exit 0 \n")

        fout.close()

    def getOutputFileName(self):
############################################
        return os.path.join(self.OUTDIR,self.output_full_name+".root")
        
    def submit(self):
###############################        
        print("submit job", self.job_id)
        job_name = self.output_full_name
        submitcommand1 = "chmod u+x " + os.path.join(self.LSF_dir,self.output_LSF_name)
        child1  = os.system(submitcommand1)
        submitcommand2 = "bsub < "+os.path.join(self.LSF_dir,self.output_LSF_name)
        child2  = os.system(submitcommand2)

##############################################
def main():
##############################################

    # CMSSW section
    input_CMSSW_BASE = os.environ.get('CMSSW_BASE')
    AnalysisStep_dir = os.path.join(input_CMSSW_BASE,"src")
    lib_path = os.path.abspath(AnalysisStep_dir)
    sys.path.append(lib_path)

    ## check first there is a valid grid proxy
    forward_proxy(AnalysisStep_dir)

    ## N.B.: this is dediced here once and for all
    from all_files_cff import FilesSrc
    srcFiles        = [FilesSrc]

    desc="""This is a description of %prog."""
    parser = OptionParser(description=desc,version='%prog version 0.1')
    parser.add_option('-s','--submit',  help='job submitted', dest='submit', action='store_true', default=False)
    parser.add_option('-j','--jobname', help='task name', dest='taskname', action='store', default='')
    parser.add_option('-i','--input',help='set input configuration (overrides default)',dest='inputconfig',action='store',default=None)
    (opts, args) = parser.parse_args()

    now = datetime.datetime.now()
    #t = now.strftime("test_%Y_%m_%d_%H_%M_%S_DATA_ReReco_")
    t = "test_PromptGT_"
    t+=opts.taskname
    
    USER = os.environ.get('USER')
    eosdir=os.path.join("/eos/cms/store/group/tsg-phase2/user",USER,"test_out",t)
    if(opts.submit):
        mkdir_eos(eosdir)

    #### Initialize all the variables

    jobName         = None
    applyEXTRACOND  = None
    globalTag       = None
    extraCondVect   = None      
     
    ConfigFile = opts.inputconfig
    
    if ConfigFile is not None:

        print("********************************************************")
        print("* Parsing from input file:", ConfigFile," ")
        
        config = ConfigParser.ConfigParser()
        config.read(ConfigFile)

        #print(config.sections())

        # please notice: since in principle one wants to run on several different samples simultaneously,
        # all these inputs are vectors
        jobName          = [ConfigSectionMap(config,"Job")['jobname']+"_"+opts.taskname] 
        applyEXTRACOND   = [ConfigSectionMap(config,"Conditions")['applyextracond']]
        value            = ConfigSectionMap(config,"Conditions")['extracondvect']
        globalTag        = [ConfigSectionMap(config,"Conditions")['globaltag']]
        
        #print "apply:",applyEXTRACOND[0]," value:",value
        # some magic is need to write correctly the vector of vectors...
        if 'True' in applyEXTRACOND[0]:
            if "|" in value:
                bunch            = value.split('|')
                extraCondVect    = [[item.split(',') for item in bunch]]
            else:
                extraCondVect    = [[value.split(',')]]
        else:
            extraCondVect = [['None', 'None', 'None']]
    else :

        print("********************************************************")
        print("* Parsing from command line                            *")
        print("********************************************************")
          
        jobName         = ['MinBiasQCD_CSA14Ali_CSA14APE']      
        applyEXTRACOND  = ['False']
        extraCondVect   = [[('SiPixelTemplateDBObjectRcd','frontier://FrontierProd/CMS_COND_31X_PIXEL','SiPixelTemplates38T_2010_2011_mc'),
                            ('SiPixelQualityFromDBRcd','frontier://FrontierProd/CMS_COND_31X_PIXEL','SiPixelQuality_v20_mc')]]
     
    # start loop on samples

    # print some of the configuration
    
    print("********************************************************")
    print("* Configuration info *")
    print("********************************************************")
    print("- submitted   : ",opts.submit)
    print("- Jobname     : ",jobName)
    print("- GlobalTag   : ",globalTag)
    print("- extraCond?  : ",applyEXTRACOND)
    print("- conditions  : ",extraCondVect)                   
   
    for iConf in range(len(srcFiles)):

    # for hadd script
        scripts_dir = os.path.join(AnalysisStep_dir,"scripts")
        if not os.path.exists(scripts_dir):
            os.makedirs(scripts_dir)
        hadd_script_file = os.path.join(scripts_dir,jobName[iConf])
        fout = open(hadd_script_file,'w')

        output_file_list1=list()      
        output_file_list2=list()
        output_file_list2.append("hadd ")

        totalJobs=0          
        theBashDir=None
        theBaseName=None

        for jobN,theSrcFiles in enumerate(split(srcFiles[iConf],1)):
            #print jobN

            totalJobs=totalJobs+1
            aJob = Job(jobN,jobN,jobName[iConf], globalTag[iConf],applyEXTRACOND[iConf],extraCondVect[iConf],input_CMSSW_BASE,AnalysisStep_dir)
            
            aJob.setEOSout(eosdir)
            aJob.createTheCfgFile(theSrcFiles)
            aJob.createTheBashFile()

            output_file_list1.append("xrdcp "+aJob.getOutputFileName()+" . \n")

            if jobN == 0:
                theBashDir=aJob.BASH_dir
                theBaseName=aJob.getOutputBaseName()
                output_file_list2.append(aJob.getOutputBaseName()+".root ")
            output_file_list2.append(os.path.split(aJob.getOutputFileName())[1]+" ")    
   
            del aJob

        job_submit_file = write_HTCondor_submit_file(theBashDir,theBaseName,totalJobs,None)
        #os.path.join(self.CMSSW_dir,"src/.user_proxy"))

        if opts.submit:
            os.system("chmod u+x "+theBashDir+"/*.sh")
            submissionCommand = "condor_submit "+job_submit_file
            submissionOutput = getCommandOutput(submissionCommand)
            print(submissionOutput)

        fout.writelines(output_file_list1)
        fout.writelines(output_file_list2)

        fout.close()
        del output_file_list1
        
if __name__ == "__main__":        
    main()


   
