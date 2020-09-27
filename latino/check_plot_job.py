import os
import glob
import commands
import ROOT
import sys
import optparse
import glob
sys.path.insert(0, "python_tool/")
from CalMemoryUsage_condor import CalcMemory
from AddRequestMemory import AddRequestMemory #def AddRequestMemory(jds,memory)
from AddRequestDisk import AddRequestDisk
from AddRequestCPU import AddRequestCPU
CheckSocketErrorOpen=True
CheckSocketErrorClose=False
ResubMissingCheckPoint=True
AcceptEvictedJob=True
#TightCheck=True

######preDefined functions######
def check_file_das(JOBDIR,jobname):
    f=open(JOBDIR+'/'+jobname+'.py','r')
    lines=f.readlines()

    for line in lines:
        if 'files' in line and 'root:/' in line: ##if this line defines sample's path
            exec(line) ##then 'files' object is defined

    out=True
    f.close()
    for f in files:
        if not ROOT.TFile.Open(f):
            print "!Fail to open "+f
            out=False
    return out

def parse_name(name):
    info={}
    info['Production']=name.split('__')[1]
    info['Step']=name.split('__')[2]
    info['Sample']=name.split('__')[3]
    info['part']=name.split('__')[4]
    info['input_s']=''
    if len(name.split('____'))>1:
        #print "@@check input step@@"                                                                                                                         
        info['input_s']=name.split('____')[1]

    return info

def HasSocketError(errfile):
    if not os.path.isfile(errfile):
        
        return False
    f=open(errfile)
    lines=f.readlines()
    isFail=False
    for line in lines:
        if 'Error' in line and 'TNetXNGFile' in line:
            #if TightCheck:
            if not 'TNetXNGFile::Close' in line:
                isFail=True
                print "Error in TNetXNGFile"
                break
        if 'Error' in line and '<TNetXNGFile::Open>' in line: 
            if CheckSocketErrorOpen: 
                isFail=True
                print "socket open error->",errfile
                break
        if 'Error' in line and '<TNetXNGFile::Close>' in line:
            if CheckSocketErrorClose:
                print "socket close error->",errfile
                isFail=True
                break
    f.close()
    return isFail

def isTerminated(logfile,jid):##005 (3294050.000.000) 02/28 18:31:21 Job terminated.
    f=open(logfile)
    lines=f.readlines()
    isTerminated=False
    
    for line in lines:
        if 'Job terminated' in line and str(jid) in line:
            isTerminated=True
            break
        if 'Job was aborted by the user' in line and str(jid) in line:
            isTerminated=True
            break
        if 'reconnection failed' in line and str(jid) in line:
            isTerminated=True
    f.close()
    
    return isTerminated

def isZombie(name,jid):##005 (3294050.000.000) 02/28 18:31:21 Job terminated.
    if not ResubMissingCheckPoint:
        return False
    logfile=name+'.log'
    f=open(logfile)
    lines=f.readlines()
    isZombie=False
    ##--log file
    for line in lines:
        if 'Job was evicted' in line and str(jid) in line:
            print ">>Job was evicted"
            isZombie=True
        if 'Job executing on host' in line and str(jid) in line:
            print ">>job is restared"
            if AcceptEvictedJob:
                isZombie=False
            
    f.close()
    ##--errfile ##basket's WriteBuffer failed
    errfile=name+'.err'
    if os.path.isfile(errfile):
        if os.path.getsize(errfile)/1000000 > 10:
            isZombie=True
        else:
            #print "errfile exist"
            f=open(errfile)
            lines=f.readlines()
            for line in lines:
                if "WriteBuffer failed" in line:
                    print "[zombie]WriteBuffer failed"
                    isZombie=True
                    break
                if 'segmentation violation' in line:
                    print ">>segmentation violation"
                    isZombie=True
                    break
            f.close()
    return isZombie


def GetJid(jidfile):
    
    if not os.path.isfile(jidfile):
        jidfile=jidfile.replace('.jid','.done')
    if not os.path.isfile(jidfile):
        #print "Fail to Get jid of",jidfile
        return False
    f=open(jidfile)
    lines=f.readlines()##1 job(s) submitted to cluster 3294050.
    jid=False
    for line in lines:
        if "submitted to cluster" in line:
            
            jid=line.split('job(s) submitted to cluster')[1].replace('.','')
            
            jid=int(jid)
            break

    f.close()
    return jid
def CheckMemory(name):
    log=name+'.log'
    jds=name+'.jds'
    this_memory=CalcMemory(log)
    AddRequestMemory(jds,this_memory)
    if float(this_memory) > 5000:
        AddRequestCPU(jds,2)
    AddRequestDisk(jds,'2000')
######END:preDefined functions######

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)
parser.add_option("-d","--want_remove",   dest="want_remove", help="Want to remove not started jobs")
parser.add_option("-u","--want_resub_notstarted",   dest="want_resub_notstarted", help="want_resub_notstarted")
parser.add_option("-n","--want_resub_noDone",   dest="want_resub_noDone", help="want_resub_noDone")
parser.add_option("-r","--want_resub_fail",   dest="want_resub_fail", help="want_resub_fail")

(options, args) = parser.parse_args()

    



JOBDIR='mkShapes__semilep_XsecW'
MAINDIR=os.getcwd()

if len(sys.argv)>1:
    
    JOBDIR=sys.argv[1]
    print "@JOBDIR="+JOBDIR

###Setup#### 

FORMATS=['err','out','log','sh','jds','done']
####------####


HASMISSING=[]
NAMES=[]
for form1 in FORMATS:
    for form2 in FORMATS:
        if form1==form2 : continue
        FILES1=glob.glob(JOBDIR+"/**."+form1)
        FILENAMES1=[]
        for a in FILES1: FILENAMES1.append(a.split(form1)[0].strip('.')) 
        
        
        FILES2=glob.glob(JOBDIR+"/**."+form2)
        FILENAMES2=[]
        for a in FILES2: FILENAMES2.append(a.split(form2)[0].strip('.'))
        
        
        thislist=list(set(FILENAMES1)-set(FILENAMES2))
        HASMISSING+=thislist
        sumlist=list(set(FILENAMES1) | set(FILENAMES2))
        NAMES+=sumlist
HASMISSING=list(set(HASMISSING))
NAMES=list(set(NAMES))



##--Check logfiles---##
FAILS=[]
NOT_FINISHED=[]
SUCCESS=[]
NOT_STARTED=[]
NO_DONEFILE=[]
for name in NAMES:
    print "##--Running",name
    HasNoDone=False
    if not os.path.isfile(name+'.done'):
        NO_DONEFILE.append(name)
        HasNoDone=True
    jid=GetJid(name+'.jid')
    if not jid:
        NOT_STARTED.append(name)
        continue
    IsFail=HasSocketError(name+'.err')
    
    IsTerminated=isTerminated(name+'.log',jid)
    IsZombie=isZombie(name,jid)
    if IsTerminated and HasNoDone:
        print "--Fin But no Done file"
        CheckMemory(name)
        FAILS.append(name)
    if IsFail or IsZombie : FAILS.append(name)
    if not IsTerminated: NOT_FINISHED.append(name)
    if IsTerminated and not IsFail:SUCCESS.append(name)


print "---success--"
print len(SUCCESS),"/",len(NAMES)

print "---success but no DoneFile--"
SUCCESS_NODONE=list(set(SUCCESS).intersection(NO_DONEFILE))
print len(SUCCESS_NODONE),"/",len(NAMES)
for a in SUCCESS_NODONE:
    print a

print "--running  jobs--"
#print len(HASMISSING),"/",len(NAMES)
#for a in HASMISSING:

print len(NOT_FINISHED),"/",len(NAMES)
for a in NOT_FINISHED:
    print a

print "--not started  jobs--"
#print len(HASMISSING),"/",len(NAMES)
#for a in HASMISSING:

print len(NOT_STARTED),"/",len(NAMES)
for a in NOT_STARTED:
    print a

print "---no DoneFile---"
print len(NO_DONEFILE),"/",len(NAMES)
for a in NO_DONEFILE:
    print a

print "--fail with error--"
print len(FAILS),"/",len(NAMES)
for a in FAILS:
    print a



RESUB=[]

ANSWERED=0
want_remove='n'
while ANSWERED==0:
    if options.want_remove:
        want_remove=options.want_remove
    else:
        want_remove=raw_input('want to remove not finished jobs? (y/n)')
    print(want_remove)
    if want_remove=='y' or want_remove=='n':
        ANSWERED=1
        if want_remove=='y':
            FAILS=list(set(FAILS+NOT_FINISHED))
    


ANSWERED=0
want_resub_notstarted='n'
while ANSWERED==0:
    if options.want_resub_notstarted:
        want_resub_notstarted=options.want_resub_notstarted
    else:
        want_resub_notstarted=raw_input('want to resubmit not started jobs using condor_submit? (y/n)')
    print(want_resub_notstarted)
    if want_resub_notstarted=='y' or want_resub_notstarted=='n':
        ANSWERED=1
        if want_resub_notstarted=='y':
            RESUB=RESUB+NOT_STARTED
            #want_resub='y'

ANSWERED=0
want_resub_noDone='n'
while ANSWERED==0:
    if options.want_resub_noDone:
        want_resub_noDone=options.want_resub_noDone
    else:
        want_resub_noDone=raw_input('want to resubmit  jobs without donefile using condor_submit? (y/n)')
    print(want_resub_noDone)
    if want_resub_noDone=='y' or want_resub_noDone=='n':
        ANSWERED=1
        if want_resub_noDone=='y':
            RESUB=RESUB+NO_DONEFILE
            print "add nodonfiles to resublist"
            #want_resub='y'


ANSWERED=0
want_resub_fail='n'
while ANSWERED==0:
    if options.want_resub_fail:
        want_resub_fail=options.want_resub_fail
    else:
        want_resub_fail=raw_input('want to resubmit failed jobs using condor_submit? (y/n)')
    print(want_resub_fail)
    if want_resub_fail=='y' or want_resub_fail=='n':
        ANSWERED=1
        if want_resub_fail=='y' :
            RESUB=RESUB+FAILS
            #want_resub='y'



#if want_resub=='n':
#    exit()

#if want_remove=='n':
#    exit()


def do_condor_rm(jidfile):
    f=open(jidfile)
    lines=f.readlines()
    jid=''
    njob=''
    for line in lines:
        if 'job(s) submitted to cluster' in line:
            jid=line.split('job(s) submitted to cluster')[1].strip()
            njob=line.split('job(s) submitted to cluster')[0].strip()

    f.close()
    if jid=='': 
        print "!!Fail to get jobid of "+a
        return False
    



    for i in range(int(njob)):
 
        os.system('condor_rm '+jid+str(i) )
        #print "condor_rm ",jid+'.'+str(i)
print "nFAILS=",len(FAILS)

for a in FAILS:
    RemoveJob=True
    os.chdir(MAINDIR)
    #a=a.split('/')[-1]
    #jidfile=JOBDIR+'/'+a+'.jid'
    jidfile=MAINDIR+'/'+a+'.jid'
    if not os.path.isfile(jidfile):
        jidfile=jidfile.replace('.jid','.done')
    if not os.path.isfile(jidfile):
        RemoveJob=False
    
    if RemoveJob:do_condor_rm(jidfile)

print "RESUB=",len(RESUB)
for a in list(set(RESUB)):
    #a=a.split('/')[-1]

    curdir=os.getcwd()
    #os.chdir(JOBDIR)
    os.chdir(MAINDIR)
    Nsub=len(glob.glob(a+'.log*'))
    for form in ['err','out','log','done','jid']:
        if os.path.isfile(a+'.'+form):  os.system('mv '+a+'.'+form+' '+a+'.'+form+'_'+str(Nsub) )
    resubmit='condor_submit '+a+'.jds > '+a+'.jid'
    

    print resubmit
    os.system(resubmit)
    os.chdir(curdir)

