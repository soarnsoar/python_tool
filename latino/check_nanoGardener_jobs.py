import os
import glob
import commands
import ROOT


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

######END:preDefined functions######




TREEDIR='/xrootd/store/user/jhchoi/Latino/HWWNano/'
#JOBDIR='NanoGardening__Summer16_102X_nAODv4_Full2016v4'
#JOBDIR='NanoGardening__Run2016_102X_nAODv4_Full2016v4'
JOBDIR='NanoGardening__Fall2017_102X_nAODv4_Full2017v4'
#JOBDIR='NanoGardening__Run2017_102X_nAODv4_Full2017v4'                                                                       


###Setup#### 
Latino_sampleDir=''
if os.getenv('CMSSW_BASE')=='': 
    print "!!Need cmsenv!!"
    exit()
else :
    Latino_sampleDir=os.getenv('CMSSW_BASE')+'/src/LatinoAnalysis/NanoGardener/python/framework/samples/'
Latino_sampleFile=''
if 'Summer16_102X_nAODv4_Full2016v4' in JOBDIR:
    Latino_sampleFile='Summer16_102X_nAODv4.py'
elif 'Run2016_102X_nAODv4_Full2016v4' in JOBDIR:
    Latino_sampleFile='Run2016_102X_nAODv4.py'
elif 'Fall2017_102X_nAODv4_Full2017v4' in JOBDIR:
    Latino_sampleFile='fall17_102X_nAODv4.py'
elif 'Run2017_102X_nAODv4_Full2017v4' in JOBDIR:
    Latino_sampleFile='Run2017_102X_nAODv4.py'

if Latino_sampleFile=='': 
    print "!!None matched sample python in Latino path!!"
    exit()

sample_py=Latino_sampleDir+"/"+Latino_sampleFile


VETO_KEYWORDS=[]
TAG=[]


FORMATS=['err','out','log','sh','jds']
####------####


HASMISSING=[]
NAMES=[]
for form1 in FORMATS:
    for form2 in FORMATS:
        if form1==form2 : continue
        FILES1=glob.glob(JOBDIR+"/*."+form1)
        FILENAMES1=[]
        for a in FILES1: FILENAMES1.append(a.split(form1)[0].strip('.')) 
        
        
        FILES2=glob.glob(JOBDIR+"/*."+form2)
        FILENAMES2=[]
        for a in FILES2: FILENAMES2.append(a.split(form2)[0].strip('.'))
        
        
        thislist=list(set(FILENAMES1)-set(FILENAMES2))
        HASMISSING+=thislist
        sumlist=list(set(FILENAMES1) | set(FILENAMES2))
        NAMES+=sumlist
HASMISSING=list(set(HASMISSING))
NAMES=list(set(NAMES))

print "--need to check following jobs--"
for a in HASMISSING:
    print a


print "--check output--"

LIST_COMPLETE={}
LIST_RUNNING={}
LIST_FAIL={}
LIST_ZOMBIE={}
for name in NAMES:
    #NanoGardening__Summer16_102X_nAODv4_Full2016v4/NanoGardening__Summer16_102X_nAODv4_Full2016v4__MCl1loose2016__TTZjets__part9


    name=name.split('/')[-1]
    name=name.strip('/')
    
    Production=name.split('__')[1]
    Step=name.split('__')[2]
    Sample=name.split('__')[3]
    part=name.split('__')[4]
    

    #path
    #/xrootd/store/user/jhchoi/Latino/HWWNano/Summer16_102X_nAODv4_Full2016v4/MCl1loose2016/nanoLatino_WZZ__part0.root
    filepath=TREEDIR+'/'+Production+"/"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"

    if os.path.isfile(filepath):
        LIST_COMPLETE[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part}
    else:
        ##for this job##
        TERMINATED=False
        ZOMBIE=False
        logpath=JOBDIR+"/"+name+".log"
        outpath=JOBDIR+"/"+name+".out"
        if not os.path.isfile(logpath): os.system('touch '+logpath)
        f= open(logpath)
        lines=f.readlines()
        for line in lines:
            if 'Job terminated' in line:TERMINATED=True
            if 'Job was aborted by the user' in line: TERMINATED=True
        f.close()
        if not os.path.isfile(outpath): os.system('touch '+outpath)
        f=open(outpath)
        lines=f.readlines()
        for line in lines:
            if 'file probably overwritten: stopping reporting error messages' in line : ZOMBIE=True
        

        if TERMINATED: LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part}
        elif ZOMBIE    : LIST_ZOMBIE[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part}
        else : LIST_RUNNING[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part}


print "--Running--"
for a in LIST_RUNNING:
    print a
print "--FAIL--"
for a in LIST_FAIL:
    print a
print "--ZOMBIE--"
for a in LIST_ZOMBIE:
    print a

LIST_FAIL_RESUB={}

print "--check @ lxplus --"
print "-sample py ="+sample_py
exec open(sample_py).read()
for a in LIST_FAIL:
    
    samplename=LIST_FAIL[a]['Sample']
    print "@@samplename="+samplename
    dascheck='dasgoclient -timeout 5 -query="file dataset='+Samples[samplename]['nanoAOD']+'"'
    print "....."
    status, output = commands.getstatusoutput(dascheck)
    if check_file_das(JOBDIR,a):
    #if '/store' in output: ## if file exists->resubmit
        #print "output="+output
        curdir=os.getcwd()
        os.chdir(JOBDIR)
        os.system('rm '+a+'.err')
        os.system('rm '+a+'.out')
        os.system('rm '+a+'.log')
        os.system('rm '+a+'.jid')
        resubmit='condor_submit '+a+'.jds > '+a+'.jid'
        print resubmit
        os.system(resubmit)
        os.chdir(curdir)
    else:
        LIST_FAIL_RESUB[a]={'Production':LIST_FAIL[a]['Production'], 'Step':LIST_FAIL[a]['Step'], 'Sample':LIST_FAIL[a]['Sample'],'part':LIST_FAIL[a]['part']}
    print "--FIN.--"

print "--RESUB FAIL--"
for a in LIST_FAIL_RESUB:
    print a
    



