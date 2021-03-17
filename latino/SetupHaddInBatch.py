import os
import optparse
import glob
class haddjob():

    def __init__(self,jobname,ncpu,targetdir):
        self.ncpu=ncpu
        self.targetdir=targetdir
        self.jobname=jobname
        self.CWD=os.getcwd()
        self.memory=self.GetDirSize(self.targetdir)/2
        self.workdir=self.CWD+"/workdirhadd_"+self.jobname
        self.JdsPath=self.workdir+'/'+'runhadd.jds'
        self.ExePath=self.workdir+'/'+'runhadd.sh'
        self.OutPath=self.workdir+'/'+'runhadd.out'
        self.ErrPath=self.workdir+'/'+'runhadd.err'
        self.LogPath=self.workdir+'/'+'runhadd.log'
        self.GetEnvs()
        self.SetJds()
        self.SetExe()

    def GetEnvs(self):
        self.SCRAM_ARCH=os.getenv("SCRAM_ARCH")
        self.VO_CMS_SW_DIR=os.getenv("VO_CMS_SW_DIR")
        self.CMSSW_BASE=os.getenv("CMSSW_BASE")
        #self.CWD=os.getcwd()
    def SetExe(self):
        self.exe=[]
        self.exe.append("#!/bin/bash")
        self.exe.append("export VO_CMS_SW_DIR="+self.VO_CMS_SW_DIR)
        self.exe.append("export SCRAM_ARCH="+self.SCRAM_ARCH)
        self.exe.append("source $VO_CMS_SW_DIR/cmsset_default.sh")
        self.exe.append("cd "+self.CMSSW_BASE)
        self.exe.append("eval `scramv1 ru -sh`")
        self.exe.append('cd '+self.targetdir)
        self.exe.append('(mkdir -p temp/;StartTime=$(date +%s);hadd -f -j '+str(self.ncpu)+' -d temp/ hadd.root *.root;EndTime=$(date +%s);echo "runtime : $(($EndTime - $StartTime)) sec";)>hadd.log')
    def SetJds(self):
        self.jds=[]
        self.jds.append('executable = '+self.ExePath)
        self.jds.append('universe = vanilla')
        self.jds.append('output = '+self.OutPath)
        self.jds.append('error = '+self.ErrPath)
        self.jds.append('log = '+self.LogPath)
        self.jds.append('request_cpus = '+str(int(self.ncpu/2)))
        self.jds.append('accounting_group=group_cms')
        self.jds.append('JobBatchName='+self.jobname)
        self.jds.append('request_memory = '+str(int(self.memory))+' MB \n')
        self.jds.append('queue')

    def ExportWorkspace(self):
        os.system('mkdir -p '+self.workdir)
        ###--Jds--###
        f=open(self.JdsPath,'w')
        for l in self.jds:
            f.write(l+'\n')
        f.close()
        ###--ExE--###
        f=open(self.ExePath,'w')
        for l in self.exe:
            f.write(l+'\n')
        f.close()

        os.system('chmod u+x '+self.ExePath )
        os.system('chmod u+x '+self.JdsPath )
    def Submit(self):
        os.chdir(self.workdir)
        command='condor_submit '+JdsPath+' &> '+JdsPath.replace('.jds','.jid')
        print command
        os.system(command)

    def GetDirSize(self,path):
        flist=glob.glob(path+'/plot*.root')
        mysize=0.
        for f in flist:
            mysize+=os.path.getsize(f)/1024/1024
        return mysize
        
if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option("-n","--ncpu",   dest="ncpu", help="# of cpus to use ")
    parser.add_option("-a","--jobname",   dest="jobname", help="jobname")
    parser.add_option("-t","--targetdir",   dest="targetdir", help="target directiry")
    

    (options, args) = parser.parse_args()
    
    ncpu=int(options.ncpu)
    jobname=options.jobname
    targetdir=options.targetdir
    ##    def __init__(self,jobname,ncpu,targetdir):
    #myjob=haddjob('test',5,os.getcwd()+'/filefortest')
    myjob=haddjob(jobname,ncpu,os.getcwd()+'/'+targetdir)
    myjob.ExportWorkspace()
