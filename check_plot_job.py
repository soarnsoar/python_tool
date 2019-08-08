import os
import glob
import commands
import ROOT
import sys
import datetime
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

######END:preDefined functions######


    



JOBDIR='mkShapes__semilep_XsecW'


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



for a in glob.glob(JOBDIR+"/*.jid"):
    a=a.split('.jid')[0]
    HASMISSING.append(a)




HASMISSING=list(set(HASMISSING))
NAMES=list(set(NAMES))



NOOUT=[]
print "--need to check following jobs--"
for a in HASMISSING:
    print a
    if os.path.isfile(a+'.out'):
        print "[out]",datetime.datetime.fromtimestamp(os.path.getmtime(a+'.out'))
        
    else:
        print "[out] No file"
        NOOUT.append(a)
    if os.path.isfile(a+'.err'):
        print "[err]",datetime.datetime.fromtimestamp(os.path.getmtime(a+'.err'))
    else:
        print "[err] No file"
    if os.path.isfile(a+'.log'):
        print "[log]",datetime.datetime.fromtimestamp(os.path.getmtime(a+'.log'))
    else:
        print "[log] No file"



ANSWERED=0
want_resub='n'
while ANSWERED==0:
    want_resub=raw_input('want to resubmit no outfile jobs using condor_submit? (y/n)')
    print(want_resub)
    if want_resub=='y' or want_resub=='n':
        ANSWERED=1


if want_resub=='n':
    exit()


for a in NOOUT:
    a=a.split('/')[-1]
    f=open(JOBDIR+'/'+a+'.jid')
    lines=f.readlines()
    jid=''
    njob=''
    for line in lines:
        if 'job(s) submitted to cluster' in line:
            jid=line.split('job(s) submitted to cluster')[1].strip()
            njob=line.split('job(s) submitted to cluster')[0].strip()

    if jid=='': print "!!Fail to get jobid of "+a
    for i in range(int(njob)):
        os.system('condor_rm '+jid+str(i) )




    curdir=os.getcwd()
    os.chdir(JOBDIR)
    os.system('rm '+a+'.err')
    os.system('rm '+a+'.out')
    os.system('rm '+a+'.log')
    os.system('rm '+a+'.jid')
    os.system('rm '+a+'.done')
    resubmit='condor_submit '+a+'.jds > '+a+'.jid'
    print resubmit
    os.system(resubmit)
    os.chdir(curdir)




ANSWERED=0
want_resub='n'
while ANSWERED==0:
    want_resub=raw_input('want to resubmit using condor_submit? (y/n)')
    print(want_resub)
    if want_resub=='y' or want_resub=='n':
        ANSWERED=1


if want_resub=='n':
    exit()


for a in HASMISSING:
    if a in NOOUT: continue
    a=a.split('/')[-1]
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




    curdir=os.getcwd()
    os.chdir(JOBDIR)
    os.system('rm '+a+'.err')
    os.system('rm '+a+'.out')
    os.system('rm '+a+'.log')
    os.system('rm '+a+'.jid')
    os.system('rm '+a+'.done')
    resubmit='condor_submit '+a+'.jds > '+a+'.jid'
    print resubmit
    os.system(resubmit)
    os.chdir(curdir)

