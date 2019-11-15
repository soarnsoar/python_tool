import os
import glob
import commands
import ROOT
import sys




######preDefined functions######
def check_file_das(JOBDIR,jobname):
    f=open(JOBDIR+'/'+jobname+'.py','r')
    lines=f.readlines()
    files=[]
    for line in lines:
        #if 'files' in line and 'root:/' in line: ##if this line defines sample's path
        #    exec(line) ##then 'files' object is defined
        if 'root://cms-xrd-global.cern.ch/' in line and '.root' in line:
            ftemp=line.split('root://cms-xrd-global.cern.ch/')[1]
            ftemp=ftemp.split('.root')[0]
            ftemp='root://cms-xrd-global.cern.ch/'+ftemp+'.root'
            files.append(ftemp)
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

def change_workdir(shfile):
    f=open(shfile,'r')
    fnew=open(shfile+'_new','w')
    lines=f.readlines()
    curdir=os.getcwd()
    print "curdir=",curdir
    for line in lines:
        #print "[DEBUG]",line
        if 'cd' in line and curdir in line.replace('//','/'):
            fnew.write('cd ${_CONDOR_SCRATCH_DIR}\n')
            print "!!change workdir From"+line+'====>'+'cd ${_CONDOR_SCRATCH_DIR}'
        else:
            fnew.write(line)

    f.close()
    fnew.close()
    os.system('mv '+shfile+'_new'+' '+shfile)
    os.system('chmod u+x '+shfile)
        




######END:preDefined functions######



JOBDIR=sys.argv[1]
print "@JOBDIR="+JOBDIR


TREEDIR='/xrootd/store/user/jhchoi/Latino/HWWNano/'
#JOBDIR='NanoGardening__Summer16_102X_nAODv4_Full2016v4'
#JOBDIR='NanoGardening__Run2016_102X_nAODv4_Full2016v4'
#JOBDIR='NanoGardening__Fall2017_102X_nAODv4_Full2017v4'
#JOBDIR='NanoGardening__Run2017_102X_nAODv4_Full2017v4'                                                                       
#JOBDIR='NanoGardening__Autumn18_102X_nAODv4_GTv16_Full2018v4'
#JOBDIR='NanoGardening__Autumn18_102X_nAODv4_GTv16_Full2018v4'
#JOBDIR='NanoGardening__Run2017_102X_nAODv4_Full2017v5'
#JOBDIR='NanoGardening__Fall2017_102X_nAODv4_Full2017v5'
#JOBDIR='NanoGardening__Run2016_102X_nAODv4_Full2016v5'
#JOBDIR='NanoGardening__Summer16_102X_nAODv4_Full2016v5'
#JOBDIR='NanoGardening__Autumn18_102X_nAODv5_Full2018v5'
#JOBDIR='NanoGardening__Autumn18_102X_nAODv5_Full2018v5'
#JOBDIR='NanoGardening__Run2018_102X_nAODv5_Full2018v5'
#JOBDIR='NanoGardening__Fall2017_102X_nAODv4_Full2017v5'
###Setup#### 
Latino_sampleDir=''
if os.getenv('CMSSW_BASE')=='': 
    print "!!Need cmsenv!!"
    exit()
else :
    Latino_sampleDir=os.getenv('CMSSW_BASE')+'/src/LatinoAnalysis/NanoGardener/python/framework/samples/'
Latino_sampleFile=''
if 'Summer16_102X_nAODv4' in JOBDIR:
    Latino_sampleFile='Summer16_102X_nAODv4.py'
elif 'Run2016_102X_nAODv4' in JOBDIR:
    Latino_sampleFile='Run2016_102X_nAODv4.py'
elif 'Fall2017_102X_nAODv4' in JOBDIR:
    Latino_sampleFile='fall17_102X_nAODv4.py'
elif 'Run2017_102X_nAODv4' in JOBDIR:
    Latino_sampleFile='Run2017_102X_nAODv4.py'
elif 'NanoGardening__Run2018_102X_nAODv4_14Dec' in JOBDIR:
    Latino_sampleFile='Run2018_102X_nAODv4_14Dec2018.py'
elif 'NanoGardening__Autumn18_102X_nAODv4_GTv16' in JOBDIR:
    Latino_sampleFile='Autumn18_102X_nAODv4_v16.py'
elif 'NanoGardening__Autumn18_102X_nAODv5_Full2018v5' in JOBDIR:
    Latino_sampleFile='Autumn18_102X_nAODv5.py'
elif 'NanoGardening__Run2018_102X_nAODv5_Full2018v5' in JOBDIR:
    Latino_sampleFile='Run2018_102X_nAODv5.py'
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
LIST_NOT_STARTED={}
LIST_FAIL={}
LIST_ZOMBIE={}
for name in NAMES:
    #NanoGardening__Summer16_102X_nAODv4_Full2016v4/NanoGardening__Summer16_102X_nAODv4_Full2016v4__MCl1loose2016__TTZjets__part9
    #NanoGardening__Summer16_102X_nAODv4_Full2016v4__MCl1loose2016__TTZjets__part9
    #NanoGardening__Summer16_102X_nAODv4_Full2016v4__MCCorr2016__GluGluHToWWToLNuQQ_M4000__part18____MCl1loose2016
    #MCl1loose2016__MCCorr2016/
    name=name.split('/')[-1]
    name=name.strip('/')
    info=parse_name(name)
    #Production=name.split('__')[1]
    #Step=name.split('__')[2]
    #Sample=name.split('__')[3]
    #part=name.split('__')[4]
    #input_s=''
    #if len(name.split('____'))>1:
    #    #print "@@check input step@@"
    #    input_s=name.split('____')[1]
    Production=info['Production']
    Step=info['Step']
    Sample=info['Sample']
    part=info['part']
    input_s=info['input_s']
    #print "Production="+Production
    #print "Step="+Step
    #print "Sample="+Sample
    #print "part="+part
    #print "input_s="+input_s
    #path
    #/xrootd/store/user/jhchoi/Latino/HWWNano/Summer16_102X_nAODv4_Full2016v4/MCl1loose2016/nanoLatino_WZZ__part0.root
    if input_s=='':
        
        filepath=TREEDIR+'/'+Production+"/"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"
    else:
        filepath=TREEDIR+'/'+Production+"/"+input_s+"__"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"

    if os.path.isfile(filepath):
        if os.stat(filepath).st_size == 0:
            os.system('rm '+filepath.replace('/xrootd/store/user/jhchoi/','/xrootd_user/jhchoi/xrootd/'))
            os.system('xrdfs root://cms-xrdr.private.lo:2094 rm '+filepath.replace('/xrootd/','//xrd/'))
            print "0 size file!!!-->"+filepath



    if os.path.isfile(filepath):
        #print filepath
        LIST_COMPLETE[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part}    
    else:
        ##for this job##
        TERMINATED=False
        ZOMBIE=False
        STARTED=False
        logpath=JOBDIR+"/"+name+".log"
        errpath=JOBDIR+"/"+name+".err"
        outpath=JOBDIR+"/"+name+".out"
        jidpath=JOBDIR+"/"+name+".jid"
        donepath=JOBDIR+"/"+name+".done"
        if not os.path.isfile(logpath): os.system('touch '+logpath)
        if not os.path.isfile(jidpath): os.system('mv '+donepath+' '+jidpath)
        if not os.path.isfile(jidpath) and not os.path.isfile(donepath) : 
            LIST_NOT_STARTED[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
            continue
        jid=''
        f= open(jidpath)
        lines=f.readlines()

        for line in lines:
            if 'job(s) submitted to cluster' in line:
                jid=line.split('job(s) submitted to cluster')[1].strip()
                njob=line.split('job(s) submitted to cluster')[0].strip()
        #print "[jhchoi]JOBDIR="+jid
        f.close()
        
        f= open(logpath)
        lines=f.readlines()
        
        for line in lines:
            if 'Job terminated' in line and jid in line:TERMINATED=True
            if 'Job was aborted by the user' in line and jid in line: TERMINATED=True
            if 'Job disconnected, attempting to reconnect' in line and jid in line : ZOMBIE=True
        f.close()
        if not os.path.isfile(outpath): os.system('touch '+outpath)
        f=open(outpath)
        lines=f.readlines()
        for line in lines:
            if 'file probably overwritten: stopping reporting error messages' in line : ZOMBIE=True
            if 'Processed' in line and 'entries' in line and 'elapsed time' in line and 'kHz, avg speed' in line : STARTED=True
        f.close()
        if os.path.isfile(errpath):
            f=open(errpath)
            lines=f.readlines()
            for line in lines:
                if 'Error in <TFile::WriteBuffer>' in line : ZOMBIE=True
                if 'Error in <TBasket::Streamer>' in line : ZOMBIE=True
            f.close()


        if TERMINATED: LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
        elif ZOMBIE    : LIST_ZOMBIE[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
        elif not STARTED : LIST_NOT_STARTED[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
        else : LIST_RUNNING[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part,'input_s':input_s}
    

print "--Complete--"
for a in LIST_COMPLETE:
    print a
print "--Running--"
for a in LIST_RUNNING:
    print a
print "--NOT Started yet"
for a in LIST_NOT_STARTED:
    print a
print "--FAIL--"
for a in LIST_FAIL:
    print a
print "--ZOMBIE--"
for a in LIST_ZOMBIE:
    print a


print " --- kill zombie---"
for a in LIST_ZOMBIE:
    f=open(JOBDIR+'/'+a+'.jid')
    lines=f.readlines()
    jid=''
    njob=''
    for line in lines:
        if 'job(s) submitted to cluster' in line:
            jid=line.split('job(s) submitted to cluster')[1].strip()
            njob=line.split('job(s) submitted to cluster')[0].strip()

            if jid=='': print "!!Fail to get jobid of "+a
    #print 'jobid='+jid
    #print "njob="+njob
    
    for i in range(int(njob)):
        os.system('condor_rm '+jid+str(i) )



LIST_RESUB={}
LIST_RESUB.update(LIST_FAIL)
LIST_RESUB.update(LIST_ZOMBIE)

LIST_RESUB_SAMPLENAME=[]
print "---samples need resub ---"
for a in LIST_RESUB:
    #samplename=LIST_FAIL[a]['Sample']
    samplename=LIST_RESUB[a]['Sample']
    LIST_RESUB_SAMPLENAME.append(samplename)
    #print samplename                                                                                                                                         

LIST_RESUB_SAMPLENAME=list(set(LIST_RESUB_SAMPLENAME))
for a in LIST_RESUB_SAMPLENAME:
    print a

print "---Summary---"
print "COMPLETE="+str(len(LIST_COMPLETE))
print "RUNNING="+str(len(LIST_RUNNING))
print "NOT_STARTED="+str(len(LIST_NOT_STARTED))
print "FAIL="+str(len(LIST_FAIL))
print "ZOMBIE="+str(len(LIST_ZOMBIE))


LIST_FAIL_RESUB={}


ANSWERED=0
want_remove='n'
while ANSWERED==0:
    want_remove=raw_input('want to remove not started samples using condor_submit? (y/n)')
    print(want_remove)
    if want_remove=='y' or want_remove=='n':
        ANSWERED=1


if want_remove=='y':

    for a in LIST_NOT_STARTED:
        f=open(JOBDIR+'/'+a+'.jid')
        lines=f.readlines()
        jid=''
        njob=''
        for line in lines:
            if 'job(s) submitted to cluster' in line:
                jid=line.split('job(s) submitted to cluster')[1].strip()
                njob=line.split('job(s) submitted to cluster')[0].strip()

            if jid=='': print "!!Fail to get jobid of "+a
        #print 'jobid='+jid                                                                                                                                                           
        #print "njob="+njob                                                                                                                                                           

        for i in range(int(njob)):
            os.system('condor_rm '+jid+str(i) )


ANSWERED=0
want_resub='n'

while ANSWERED==0:
    want_resub=raw_input('want to ad not started samples to failed job list? (y/n)')
    print(want_resub)
    if want_resub=='y' or want_resub=='n':
        ANSWERED=1


if want_resub=='y':

    LIST_RESUB.update(LIST_NOT_STARTED)


ANSWERED=0
want_resub='n'
while ANSWERED==0:
    want_resub=raw_input('want to resubmit failed jobs using condor_submit? (y/n)')
    print(want_resub)
    if want_resub=='y' or want_resub=='n':
        ANSWERED=1


if want_resub=='n':
    print "Please resubmit using the Latino NanoGardener"
    exit()


ANSWERED=0
want_modify_workdir='n'
while ANSWERED==0:
    want_modify_workdir=raw_input('want to change workdir of failed jobs? (y/n)')
    print(want_modify_workdir)
    if want_modify_workdir=='y' or want_modify_workdir=='n':
        ANSWERED=1





print "-sample py ="+sample_py
exec open(sample_py).read()
for a in LIST_RESUB:
    
    samplename=LIST_RESUB[a]['Sample']
    print a
    #print "@@samplename="+samplename
    #print "LIST_FAIL[a]['input_s']="+LIST_FAIL[a]['input_s']
    if LIST_RESUB[a]['input_s']=='':
        dascheck='dasgoclient -timeout 5 -query="file dataset='+Samples[samplename]['nanoAOD']+'"'
        print "....."
        status, output = commands.getstatusoutput(dascheck)
        if not check_file_das(JOBDIR,a): 
            LIST_FAIL_RESUB[a]={'Production':LIST_RESUB[a]['Production'], 'Step':LIST_RESUB[a]['Step'], 'Sample':LIST_RESUB[a]['Sample'],'part':LIST_RESUB[a]['part']}
            continue
    #if '/store' in output: ## if file exists->resubmit
        #print "output="+output
    curdir=os.getcwd()
    os.chdir(JOBDIR)
    os.system('rm '+a+'.err')
    os.system('rm '+a+'.out')
    os.system('rm '+a+'.log')
    os.system('rm '+a+'.jid')

    if want_modify_workdir=='y':
        change_workdir(a+'.sh')
    resubmit='condor_submit '+a+'.jds > '+a+'.jid'
    print resubmit
    os.system(resubmit)
    os.chdir(curdir)
            
    print "--FIN.--"

print "--RESUB FAIL--"
for a in LIST_FAIL_RESUB:
    print a
    



