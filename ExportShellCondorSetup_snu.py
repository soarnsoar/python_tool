#!/usr/bin/env python                                                                                                                                        
import optparse
import os
#export CMS_PATH=/cvmfs/cms.cern.ch
#source $CMS_PATH/cmsset_default.sh

def Export(WORKDIR,command,jobname,submit,ncpu,memory=False,nretry=3):
    command='('+command+')'
    os.system('mkdir -p '+WORKDIR)
    f=open(WORKDIR+'/run.sh','w')
    lines=[]
    
    lines.append("#!/bin/bash")
    #lines.append("export VO_CMS_SW_DIR="+os.getenv("VO_CMS_SW_DIR"))
    lines.append("export CMS_PATH=/cvmfs/cms.cern.ch")
    lines.append("source $CMS_PATH/cmsset_default.sh")
    lines.append("export SCRAM_ARCH="+os.getenv("SCRAM_ARCH"))
    #lines.append("source $VO_CMS_SW_DIR/cmsset_default.sh")
    lines.append("cd "+os.getenv("CMSSW_BASE"))
    lines.append("eval `scramv1 ru -sh`")
    lines.append('cd '+os.getcwd()+'/'+WORKDIR)
    #lines.append('python run.py &> run.log')
    #lines.append(command+'||myerr=$?')
    lines.append(command)
    lines.append('myerr=$?')
    #lines.append('if [ "$myerr"=="" ]')
    #lines.append('then')
    #lines.append('myerr=0')
    #lines.append('fi')
    lines.append('ntry=1')
    lines.append('echo "myerr=$myerr"')
    lines.append('while [ $myerr -ne 0 ]')
    lines.append('do')
    lines.append("ntry=`expr $ntry + 1`")
    #lines.append(command+'||myerr=$?')   
    lines.append(command)
    lines.append('myerr=$?')
    lines.append('echo ntry="$ntry"') 
    #lines.append('myerr=$?')
    lines.append('echo "myerr=$myerr"')


    lines.append('if [ $ntry -gt '+str(nretry)+' ]')
    lines.append('then')
    lines.append('break')
    lines.append('fi')
    lines.append('done')
    lines.append('echo "[ntry=$ntry]"')
    lines.append('if [ $myerr -eq 0 ]')
    lines.append('then')
    lines.append('mv '+os.getcwd()+'/'+WORKDIR+'/run.jid '+os.getcwd()+'/'+WORKDIR+'/run.done')
    lines.append('fi')
    #WORKDIR+'/run.jid
    for line in lines:
        f.write(line+'\n')
    
    f.close()
    os.system('chmod u+x '+WORKDIR+'/run.sh')
    ##--Jdsfile
    f=open(WORKDIR+'/run.jds','w')
    lines=[]
    lines.append('executable = '+os.getcwd()+'/'+WORKDIR+'/run.sh')
    lines.append('universe = vanilla')
    lines.append('output = '+os.getcwd()+'/'+WORKDIR+'/run.out')
    lines.append('error = '+os.getcwd()+'/'+WORKDIR+'/run.err')
    lines.append('log = '+os.getcwd()+'/'+WORKDIR+'/run.log')
    if memory:
        lines.append('request_memory = '+str(int(memory))+' MB \n')
    ncpu_criteria=int(memory/4096)+1
    if int(ncpu) < int(ncpu_criteria):
        ncpu=ncpu_criteria

    lines.append('request_cpus = '+str(ncpu))
    lines.append('accounting_group=group_cms')
    lines.append('JobBatchName='+jobname)

    lines.append('queue')
    for line in lines:
        f.write(line+'\n')
    f.close()
    if submit:
        submitcommand='condor_submit '+WORKDIR+'/run.jds > '+WORKDIR+'/run.jid'
        print submitcommand
        os.system(submitcommand)

if __name__ == '__main__':
   usage = 'usage: %prog [options]'
   parser = optparse.OptionParser(usage)
   parser.add_option("-c","--command",   dest="command", help="command to run")
   parser.add_option("-d","--workdir",   dest="workdir", help="workarea")
   parser.add_option("-n","--jobname",   dest="jobname", help="jobname")
   parser.add_option("-m","--ncpu",   dest="ncpu", help="number of multicores",default=1)
   parser.add_option("-s","--submit",   dest="submit",action="store_true", help="submit",default=False)
   parser.add_option("-r","--memory",   dest="memory", help="memory")
   (options, args) = parser.parse_args()

   command=options.command
   workdir=options.workdir
   jobname=options.jobname
   submit=options.submit
   ncpu=options.ncpu
   if options.memory:
       memory=int(options.memory)
   else:
       memory=-1
   Export(workdir,command,jobname,submit,ncpu,memory)

