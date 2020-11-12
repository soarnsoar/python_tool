import os
import glob
import commands
import ROOT
import sys
import argparse
from GetNJobs import GetNJobs
from CheckRunningJob import CheckRunningJob
import optparse
from LatinoAnalysis.Tools.userConfig  import *
scriptpath=os.path.realpath(__file__)
scriptpath=scriptpath.split(sys.argv[0].split('/')[-1])[0]
print 'scriptpath=',scriptpath
sys.path.insert(0, scriptpath+"../")
from CalMemoryUsage_condor import CalcMemory ##input = logpath+<logfile>.log
from AddRequestMemory import AddRequestMemory
from AddRequestDisk import AddRequestDisk
from AddRequestCPU import AddRequestCPU
from datetime import datetime
from LastModifiedTime import LastModifiedTime
from GetCondorSpace import GetCondorSpace
print "====Start check_nanoGardener_jobs.py===="
#JOB_DIR_SPLIT = ( jobDirSplit == True )
JOB_DIR_SPLIT=False

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option("-d","--remove_notstart",   dest="remove_notstart", help="Want to remove not started jobs")
parser.add_option("-u","--resub_notstartd",   dest="resub_notstarted", help="want to add not started samples to failed job list")
parser.add_option("-r","--resub_fail",   dest="resub_fail", help="want to resubmit failed jobs using condor_submit? (y/n)")
parser.add_option("-c","--change_workdir",   dest="chworkdir", help="want to change workdir from home to scratch?")
parser.add_option("-N","--nresub",   dest="Nresub", help="number of jobs for resub" )
parser.add_option("-p","--passzombie",   dest="passzombie", help="pass zombie scan step", default=False, action="store_true" )
parser.add_option("-s","--samplepy",   dest="Latino_samplepyArg", help="Latino_samplepy", default='', )

(options, args) = parser.parse_args()

USER=os.getenv('USER')

if options.remove_notstart:
    if options.remove_notstart!='y' and options.remove_notstart!='n':
        print "wrong argument for --rm,--remove_notstart"
        exit()

if options.resub_notstarted:
    if options.resub_notstarted!='y' and options.resub_notstarted!='n':
        print "wrong argument for -restart, --resub_notstartd"
        exit()
if options.resub_fail:
    if options.resub_fail!='y' and options.resub_fail!='n':
        print "wrong argument for -resub --resub_fail"
        exit()
if options.chworkdir:
    if options.chworkdir!='y' and options.chworkdir!='n':
        print "wrong argument for -chdir --change_workdir"
        exit()
if options.Nresub:
    if options.Nresub!='all':
        try:
            int(options.Nresub)
        except ValueError:
            print 'wrong argument for -N, --nresub' 
            exit()


#options.remove_notstart


#parser = argparse.ArgumentParser()

#parser.add_argument("--cleanjob", help="y or n")

#args = parser.parse_args()

#cleanjob=False
#if args.cleanjob:
#    cleanjob=True

######preDefined functions######
print "===predefine functions==="
#myfile="root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano//Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__HMSemilepSkimJH2017v6/nanoLatino_GluGluHToWWToLNuQQ_M1500__part0.root"
def CheckFileSize(myfile):
    f=ROOT.TFile.Open(myfile)
    Size=f.GetSize()/1024/1024
    #print Size
    f.Close()
    return Size


def GetUpdateTime(line):
    #001 (3287776.000.000) 02/27 19:00:23 Job executing on host: <134.75.125.44:9618?addrs=134.75.125.44-9618+[2001-320-15-125-ca1f-66ff-fedb-5db9]-9618&noUDP&sock=25149_b35f_6>
    MMDDhhmmss=line.split('Image size of job updated')[0].split(')')[1] ##02/27 19:00:23
    MMDDhhmmss=MMDDhhmmss.strip().split(' ')##['02/27', '19:00:23']
    MMDD=MMDDhhmmss[0]##02/27 
    MM=int(MMDD.split('/')[0])
    DD=int(MMDD.split('/')[1])
    hhmmss=MMDDhhmmss[1]
    hh=int(hhmmss.split(':')[0])
    mm=int(hhmmss.split(':')[1])
    ss=int(hhmmss.split(':')[2])


    this_datetime=datetime(2000,MM,DD,hh,mm,ss)
    return this_datetime

        
def GoToCPMode(pypath):
    f=open(pypath,'r')
    fnew=open(pypath+'_cpmode','w')
    lines=f.readlines()
    for line in lines:
        if 'root://cms-xrdr.private.lo:2094' in line:
            line=line.replace('root://cms-xrdr.private.lo:2094','/').replace('/xrd/','/xrootd/')
        fnew.write(line)
    f.close()
    fnew.close()
    os.system('cp '+pypath+'_cpmode'+' '+pypath)


def CalcNSub(logpath):
    #f=open(logpath)
    #lines=f.readlines()
    #nsub=0
    #for line in lines:
    #    if 'Job submitted from host' in line:
    #        nsub+=1
    #f.close()
    nsub=len(glob.glob(logpath+'*'))
    return nsub
    
    
def check_file_das(pypath):
    f=open(pypath,'r')
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
        
def ConvertXROOTDUSERpath(filepath):
    if "root://cms-xrdr.private.lo:2094" in filepath:

        filepath=filepath.split('/xrd/')[1]
        filepath='/xrootd/'+filepath
        filepath=filepath.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','/xrootd_user/jhchoi/xrootd/Latino/HWWNano/')

    return filepath

'''
def ConvertXROOTDpath(filepath):
    if "root://cms-xrdr.private.lo:2094" in filepath:

        filepath=filepath.split('/xrd/')[1]
        filepath='/xrootd/'+filepath
        filepath=filepath.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','/xrootd_user/jhchoi/xrootd/Latino/HWWNano/')

    return filepath
'''

def ConvertToXROOTDpath(filepath):
    if "root://cms-xrdr.private.lo:2094" in filepath:
        return filepath



    if "/xrootd_user/jhchoi/xrootd/Latino/HWWNano/" in filepath:

        filepath=filepath.replace('//','/').replace('/xrootd_user/jhchoi/xrootd/Latino/HWWNano/','root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano/')
    elif "/xrootd/store/user/jhchoi/Latino/HWWNano/" in filepath:
        filepath=filepath.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano/')
    return filepath

def TFileOpen(filepath):
    #filepath=ConvertXROOTDpath(filepath)
    
    filepath=ConvertToXROOTDpath(filepath)
    #print "[filepath in TFileOpen]",filepath
    ##if the file not exist
    #if not os.path.isfile(filepath):return False
    
    #print filepath
    f=ROOT.TFile.Open(filepath,'READ')
    if not bool(f):
        print filepath,'cannot be opened'
        return False
    IsZombie=bool(f.IsZombie())
    myTree=f.Get("Runs")

    try:
        boolean=bool(myTree.GetEntries())
    except AttributeError:
        boolean=False


    f.Close()

    del myTree
    del f
    
    return boolean and not IsZombie

def CheckInputZombie(pypath):
    output=False
    f=open(pypath)
    '''
    sourceFiles=[
    "root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano//Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__JESup//nanoLatino_DYJetsToLL_M-50_HT-100to200__part0.root"
    ]    
    '''    
    lines=f.readlines()
    READ=False
    LinesToRead=''
    for line in lines:
        if 'sourceFiles=' in line.strip():
            READ=True
        if READ:
            LinesToRead+=line
            if ']' in line:##end of sourceFiles
                READ=False
            
            



    f.close()
    

    FullSize=0
    exec(LinesToRead)
    for s in sourceFiles:
        if 'cms-xrd-global.cern.ch' in s:
            continue

        this_size=CheckFileSize(s)
        FullSize=float(this_size)
        isvalid=TFileOpen(ConvertToXROOTDpath(s))
        if not isvalid:
            print '[ZOMBIEInput]',ConvertToXROOTDpath(s)
            output=True
    #FullSize
    return output,FullSize

def CheckInputSize(pypath):
    output=False
    f=open(pypath)
    ''' 
    sourceFiles=[
    "root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano//Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__JESup//nanoLatino_DYJetsToLL_M-50_HT-100to200__part0.root"
    ]
    '''
    lines=f.readlines()
    READ=False
    LinesToRead=''
    for line in lines:
        if 'sourceFiles=' in line.strip():
            READ=True
        if READ:
            LinesToRead+=line
            if ']' in line:##end of sourceFiles
                READ=False

    f.close()


    FullSize=0
    exec(LinesToRead)
    for s in sourceFiles:
        if 'cms-xrd-global.cern.ch' in s:
            continue

        this_size=CheckFileSize(s)
        FullSize+=float(this_size)
        
    return FullSize


#def AddRequestMemory(jds,memory):
#    ToAdd='request_memory = '+str(int(memory))+'MB \n'
#    f=open(jds,'r')
#    fnew=open(jds+'_new','w')

#    lines=f.readlines()
#    for line in lines:
#        if 'queue' in line:
#            fnew.write(ToAdd)
#        fnew.write(line)

#    f.close()
#    fnew.close()
#    os.system('rm '+jds+'_new')
######END:preDefined functions######
print "===end of predefine functions==="


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
#Latino_samplepyArg=
if os.getenv('CMSSW_BASE')=='': 
    print "!!Need cmsenv!!"
    exit()
if options.Latino_samplepyArg=='':
    Latino_sampleDir=os.getenv('CMSSW_BASE')+'/src/LatinoAnalysis/NanoGardener/python/framework/samples/'
    #'/src/LatinoAnalysis/NanoGardener/python/framework/samples/'
    Latino_sampleFile=''
    if 'Summer16_102X_nAODv4' in JOBDIR:
        Latino_sampleFile='Summer16_102X_nAODv4.py'
    elif 'Summer16_102X_nAODv5' in JOBDIR:
        Latino_sampleFile='Summer16_102X_nAODv5.py'
    elif 'Summer16_102X_nAODv7' in JOBDIR:
        Latino_sampleFile='Summer16_102X_nAODv7.py'
    elif 'Run2016_102X_nAODv4' in JOBDIR:
        Latino_sampleFile='Run2016_102X_nAODv4.py'
    elif 'Run2016_102X_nAODv5' in JOBDIR:
        Latino_sampleFile='Run2016_102X_nAODv5.py'
    elif 'Run2016_102X_nAODv7' in JOBDIR:
        Latino_sampleFile='Run2016_102X_nAODv7.py'
    elif 'Fall2017_102X_nAODv4' in JOBDIR:
        Latino_sampleFile='fall17_102X_nAODv4.py'
    elif 'Fall2017_102X_nAODv5' in JOBDIR:
        Latino_sampleFile='fall17_102X_nAODv5.py'
    elif 'Fall2017_102X_nAODv5' in JOBDIR:
        Latino_sampleFile='fall17_102X_nAODv5.py'
    elif 'Fall2017_102X_nAODv7' in JOBDIR:
        Latino_sampleFile='fall17_102X_nAODv7.py'
    elif 'Run2017_102X_nAODv4' in JOBDIR:
        Latino_sampleFile='Run2017_102X_nAODv4.py'
    elif 'Run2017_102X_nAODv5' in JOBDIR:
        Latino_sampleFile='Run2017_102X_nAODv5.py'
    elif 'Run2017_102X_nAODv7' in JOBDIR:
        Latino_sampleFile='Run2017_102X_nAODv7.py'
    elif 'NanoGardening__Run2018_102X_nAODv4_14Dec' in JOBDIR:
        Latino_sampleFile='Run2018_102X_nAODv4_14Dec2018.py'
    elif 'NanoGardening__Autumn18_102X_nAODv4_GTv16' in JOBDIR:
        Latino_sampleFile='Autumn18_102X_nAODv4_v16.py'
    elif 'NanoGardening__Autumn18_102X_nAODv5_Full2018v5' in JOBDIR:
        Latino_sampleFile='Autumn18_102X_nAODv5.py'
    elif 'NanoGardening__Autumn18_102X_nAODv6_Full2018v6' in JOBDIR:
        Latino_sampleFile='Autumn18_102X_nAODv6.py'
    elif 'NanoGardening__Autumn18_102X_nAODv7_Full2018v7' in JOBDIR:
        Latino_sampleFile='Autumn18_102X_nAODv7.py'
    elif 'NanoGardening__Run2018_102X_nAODv5_Full2018v5' in JOBDIR:
        Latino_sampleFile='Run2018_102X_nAODv5.py'
    elif 'NanoGardening__Run2018_102X_nAODv6_Full2018v6' in JOBDIR:
        Latino_sampleFile='Run2018_102X_nAODv6.py'
    elif 'NanoGardening__Run2018_102X_nAODv7_Full2018v7' in JOBDIR:
        Latino_sampleFile='Run2018_102X_nAODv7.py'
    if Latino_sampleFile=='': 
        print "!!None matched sample python in Latino path!!"
        exit()

    
    sample_py=Latino_sampleDir+"/"+Latino_sampleFile
else:
    sample_py=options.Latino_samplepyArg

VETO_KEYWORDS=[]
TAG=[]


FORMATS=['err','out','log','sh','jds']
####------####


HASMISSING=[]
NAMES=[]
for form1 in FORMATS:
    for form2 in FORMATS:
        if form1==form2 : continue
        FILES1=[]
        
        FILES1=glob.glob(JOBDIR+"/*."+form1)
        
        FILENAMES1=[]
        for a in FILES1: FILENAMES1.append(a.split(form1)[0].strip('.')) 
        
        FILES2=[]
        
        FILES2=glob.glob(JOBDIR+"/*."+form2)
        
        FILENAMES2=[]
        for a in FILES2: FILENAMES2.append(a.split(form2)[0].strip('.'))
        
        
        thislist=list(set(FILENAMES1)-set(FILENAMES2))
        HASMISSING+=thislist
        sumlist=list(set(FILENAMES1) | set(FILENAMES2))
        NAMES+=sumlist
HASMISSING=list(set(HASMISSING))
NAMES=list(set(NAMES))

print "len(HASMISSING)=",len(HASMISSING)
print "len(NAMES)=",len(NAMES)

print "--need to check following jobs--"
for a in HASMISSING:
    print a


print "--check output--"

os.system('mkdir -p '+JOBDIR+'/donelogs/')

LIST_COMPLETE={}
LIST_RUNNING={}
LIST_NOT_STARTED={}
LIST_FAIL={}
LIST_ZOMBIE={}
LIST_ZOMBIEINPUT={}
LIST_OVER2RESUB={}

print "@@Remove zombie files"
for name in NAMES:
    if options.passzombie:continue
    name=name.split('/')[-1]
    name=name.strip('/')
    info=parse_name(name)
    Production=info['Production']
    Step=info['Step']
    Sample=info['Sample']
    part=info['part']
    input_s=info['input_s']







    if input_s=='':

        filepath=TREEDIR+'/'+Production+"/"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"
    else:
        filepath=TREEDIR+'/'+Production+"/"+input_s+"__"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"

    #if os.path.isfile(filepath) :
    if not TFileOpen(filepath):
        print "0 size file OR Zombie!!!-->"+filepath
        #if USER=='jhchoi':
        #    os.system('rm '+filepath.replace('/xrootd/store/user/jhchoi/','/xrootd_user/jhchoi/xrootd/'))
        #else:
        os.system('xrdfs root://cms-xrdr.private.lo:2094 rm '+ConvertToXROOTDpath(filepath).replace('root://cms-xrdr.private.lo:2094',''))
            



print "@@FIN. ZOMBIE SCAN@@"
idx=0
print "@@Total N=",len(NAMES)







for name in NAMES:
    print "@@Checking->",idx,')',name
    idx=idx+1
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


    #Check if it's dryrun
    jidpath=JOBDIR+"/"+name+".jid"
    jdspath=JOBDIR+"/"+name+".jds"
    pypath=JOBDIR+"/"+name+".py"
    if os.path.isfile(jidpath): ##NOT submitted, need resubmission
        f= open(jidpath)
        lines=f.readlines()
        DRYRUN=False
        for line in lines:
            if 'job(s) submitted to cluster' in line:
                jid=line.split('job(s) submitted to cluster')[1].strip()
                njob=line.split('job(s) submitted to cluster')[0].strip()
            if 'DO NOT SUBMIT! DRY RUN' in line: ##not started . need to force to start it
                DRYRUN=True
        f.close()
        if DRYRUN:
            filesize=CheckInputSize(pypath)
            if filesize > 500:
                AddRequestCPU(jdspath,3)
                print "[MEMORY INCREASE] filesize = ",filesize
                if filesize < 1000:
                    AddRequestMemory(jdspath,float(filesize*10))
                    
                else:
                    AddRequestMemory(jdspath,float(10000))

                #print "a"
                print "[jhchoi]Add requst disk"
                AddRequestDisk(jdspath,'5G')
            print "DRYRUN!"
            TERMINATED=True
            LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
            continue





    if input_s=='':
        
        filepath=TREEDIR+'/'+Production+"/"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"
    else:
        filepath=TREEDIR+'/'+Production+"/"+input_s+"__"+Step+"/"+"nanoLatino_"+Sample+"__"+part+".root"
    
    if not TFileOpen(filepath):
        print "0 size file OR Zombie!!!-->"+filepath
        os.system('xrdfs root://cms-xrdr.private.lo:2094 rm '+ConvertToXROOTDpath(filepath).replace('root://cms-xrdr.private.lo:2094',''))

        
       



#    if os.path.isfile(filepath):
    #if ROOT.TFile.Open(filepath):

    logpath=JOBDIR+"/"+name+".log"
    errpath=JOBDIR+"/"+name+".err"
    outpath=JOBDIR+"/"+name+".out"
    jidpath=JOBDIR+"/"+name+".jid"
    pypath=JOBDIR+"/"+name+".py"
    shpath=JOBDIR+"/"+name+".sh"
    jdspath=JOBDIR+"/"+name+".jds"
    donepath=JOBDIR+"/"+name+".done"
    

    

    if TFileOpen(filepath):
        #print filepath
        LIST_COMPLETE[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part}
        


        print "[jhchoi]mv done logs and remaing root files -> ",name
        #os.system('mv '+logpath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+logpath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(logpath) : os.system('mv '+logpath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+pypath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+pypath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(pypath) :os.system('mv '+pypath+'* '+JOBDIR+'/donelogs/')
        print 'mv '+shpath+'* '+JOBDIR+'/donelogs/'
        #os.system('mv '+shpath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        if os.path.isfile(shpath) :os.system('mv '+shpath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+jdspath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+jdspath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(jdspath) :os.system('mv '+jdspath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+errpath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+errpath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(errpath) :os.system('mv '+errpath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+outpath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+outpath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(outpath) :os.system('mv '+outpath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+jidpath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+jidpath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(jidpath) :os.system('mv '+jidpath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+donepath+'* '+JOBDIR+'/donelogs/ &> /dev/null')
        print 'mv '+donepath+'* '+JOBDIR+'/donelogs/'
        if os.path.isfile(donepath) :os.system('mv '+donepath+'* '+JOBDIR+'/donelogs/')
        #os.system('mv '+JOBDIR+'/'+'*'+Sample+'*'+part+'*.root '+JOBDIR+'/donelogs &> /dev/null')
        print 'mv '+JOBDIR+'/'+'*'+Sample+'*'+part+'*.root '+JOBDIR+'/donelogs/'
        if len(glob.glob(JOBDIR+'/'+'*'+Sample+'*'+part+'*.root'))!=0 : os.system('mv '+JOBDIR+'/'+'*'+Sample+'*'+part+'*.root '+JOBDIR+'/donelogs/')
        #rm_rfile='rm '+JOBDIR+'/'+'*'+Sample+'*'+part+'*.root'
        #os.system(rm_rfile)
        print "[jhchoi]mv done logs and remaing root files [DONE]"
    else:
        if os.path.isfile(errpath):
    
            if os.path.getsize(errpath) > 1024.*1024.: ##if over 1MB err
                print "err file size is over 1MB"
                LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
                os.system('rm '+errpath)
                continue
        ##for this job##
        TERMINATED=False
        ZOMBIEINPUT=False
        ZOMBIE=False
        STARTED=False

        ##Check if input is zombie
        #if open(pypath):
        if os.path.isfile(pypath):
            #CheckInputZombie(pypath)
            IsInputZombie,filesize=CheckInputZombie(pypath)
            if IsInputZombie==True and input_s!='':
                ZOMBIEINPUT=True

            
            if filesize > 500:
                print "add cpu 2"
                AddRequestCPU(jdspath,3)
                print "[MEMORY INCREASE] filesize = ",filesize
                if filesize < 1000:
                    AddRequestMemory(jdspath,float(filesize*10))
                else:
                    AddRequestMemory(jdspath,float(10000))
                
                #print "a"
                print "[jhchoi]Add requst disk"
                AddRequestDisk(jdspath,'5G')
        #if not os.path.isfile(logpath): os.system('touch '+logpath)
        if not os.path.isfile(jidpath): os.system('mv '+donepath+' '+jidpath)
        #if (not os.path.isfile(jidpath) and not os.path.isfile(donepath)):
        #    #print "os.path.isfile(jidpath)",os.path.isfile(jidpath)
        #    #print 'jidpath',jidpath
        #    LIST_NOT_STARTED[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
        #    continue
        
        
        nsubmission=CalcNSub(logpath)
        if nsubmission>2:
            print "NSUB=",nsubmission
            LIST_OVER2RESUB[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
            #os.system('touch '+logpath+str(nsubmission))
            #os.system('cp '+errpath+' '+errpath+str(nsubmission))
            #print "[jhchoi]Go To CPMode"
            #GoToCPMode(pypath)
        jid=''
        if not os.path.isfile(jidpath): ##NOT submitted, need resubmission
            print "No jid file. FAIL"
            LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
            continue
        f= open(jidpath)
        lines=f.readlines()
        DRYRUN=False
        for line in lines:
            if 'job(s) submitted to cluster' in line:
                jid=line.split('job(s) submitted to cluster')[1].strip()
                njob=line.split('job(s) submitted to cluster')[0].strip()
            if 'DO NOT SUBMIT! DRY RUN' in line: ##not started . need to force to start it
                DRYRUN=True
        #print "[jhchoi]JOBDIR="+jid
        f.close()
        #print 'jid=',jid
        if DRYRUN:
            print "DRYRUN!"
            TERMINATED=True
            LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
            continue
        #CheckFileSize
        if os.path.isfile(logpath):
            f=open(logpath)
            lines=f.readlines()
        
            job_started=False
            last_update=''
            for line in lines:
                if str(jid) in line and 'Job executing on host' in line:
                    job_started=True
                    STARTED=True
                if 'Image size of job updated' in line:
                    last_update=line
                if 'Job terminated' in line and jid in line:
                    print "[.log]Job terminated"
                    TERMINATED=True
                    break
                if 'Job was aborted by the user' in line and jid in line: 
                    print "[.log]Job was aborted by the user"
                    TERMINATED=True
                    break
                if 'Job disconnected, attempting to reconnect' in line and jid in line : 
                    print "[logZOMBIE]Job disconnected, attempting to reconnect"
                    ZOMBIE=True
                    #break
                if 'Job was evicted' in line and jid in line : 
                    print "[logZOMBIE]Job was evicted"
                    ZOMBIE=True
                    #break

                if 'Job executing on host' in line and str(jid) in line:
                    print ">>job is restared"
                    ZOMBIE=False

                if 'Job was held' in line and jid in line:
                    print "[log hold]Job was held"
            ##if job is excuted
            #if last_update!="":
            #    updatetime=GetUpdateTime(last_update)
            #    currenttime=datetime.now()
            #    currenttime=currenttime.replace(year=2000)
            #    if currenttime.year < updatetime.year:
            #        currenttime.year=currenttime.year+1
            #    pendingtime=(currenttime-updatetime).seconds
            #    print "PENDINGTIME=",pendingtime
            #    if pendingtime > 3600:
            #        print "[ZOMBIE!!!]in log file, pending time is too large"
            #        ZOMBIE=True
            #    #this_datetime=datetime(2000,MM,DD,hh,mm,ss)
            f.close()
        if os.path.isfile(outpath):         
            f=open(outpath)
            lines=f.readlines()
            for line in lines:
                if 'file probably overwritten: stopping reporting error messages' in line : 
                    print "[out zombie]file probably overwritten: stopping reporting error messages"
                    ZOMBIE=True
                    break
                if 'Processed' in line and 'entries' in line and 'elapsed time' in line and 'kHz, avg speed' in line : STARTED=True
            f.close()
        if os.path.isfile(errpath):
            f=open(errpath)
            lines=f.readlines()
            for line in lines:
                if 'Error in <TFile::WriteBuffer>' in line : ZOMBIE=True
                if 'SysError in <TFile::ReadBuffer>: error reading from file' in line : 
                    print "[err ZOMBIE]SysError in <TFile::ReadBuffer>: error reading from file"
                    ZOMBIE=True
                    break
                #if 'Error in <TBasket::Streamer>' in line : ZOMBIE=True
                if 'There was a crash' in line : 
                    print "[err ZOMBIE]There was a crash"
                    ZOMBIE=True
                    break
                if 'Error in' in line: 
                    print "[err zombie]Error in"
                    ZOMBIE=True
                    break
                if 'Error R__unzip_header' in line : 
                    print "[err zombie]Error R__unzip_header"
                    ZOMBIE=True
                    break
                if '[ERROR]' in line:
                    print "[err zombie] [ERROR]flag"
                    ZOMBIE=True
                    break
            f.close()

        ##--Check last modification time
        pendingtime=-1
        for mypath in [logpath,errpath,outpath,jidpath]:
            if os.path.isfile(mypath):
                if pendingtime == -1: pendingtime=999999
                this_modtime=LastModifiedTime(mypath)
                print mypath
                print 'this_modtime=',this_modtime
                if this_modtime < pendingtime:
                    pendingtime = this_modtime 
        
        print "[PENDING TIME]",pendingtime
        if pendingtime > 3600 and STARTED:
            print "[PENDINGTIME ]MORE THAN 1hour"
            #ZOMBIE = True
        #pendingtime= (LastModifiedTime(logpath), LastModifiedTime(errpath), LastModifiedTime(outpath))


        if ZOMBIEINPUT : LIST_ZOMBIEINPUT[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
        elif TERMINATED: LIST_FAIL[name]={'Production':Production, 'Step':Step, 'Sample':Sample,'part':part, 'input_s':input_s}
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
print "--ZOMBIEINPUT--"
for a in LIST_ZOMBIEINPUT:
    print a

print " --- kill zombie---"
LIST_KILL={}
LIST_KILL.update(LIST_ZOMBIE)
LIST_KILL.update(LIST_FAIL)
for a in LIST_KILL:

    

    donepath=JOBDIR+'/'+a+'.done'
    jidpath=JOBDIR+'/'+a+'.jid'



    if os.path.isfile(donepath) : os.system('mv '+donepath+' '+jidpath)
    if not os.path.isfile(jidpath):continue
    f=open(jidpath)
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
    if njob=='':continue
    for i in range(int(njob)):
        command='condor_rm '+jid+str(i)
        print command
        os.system(command )
    

LIST_RESUB={}
LIST_RESUB.update(LIST_FAIL)
LIST_RESUB.update(LIST_ZOMBIE)

LIST_RESUB_SAMPLENAME=[]
print "---samples need resub ---"
for a in LIST_RESUB:
    #samplename=LIST_FAIL[a]['Sample']
    samplename=LIST_RESUB[a]['Sample']
    LIST_RESUB_SAMPLENAME.append(samplename)

    Sample=LIST_RESUB[a]['Sample']
    part=LIST_RESUB[a]['part']
    print "@Clean up remaining root files"
    rm_rfile='rm '+JOBDIR+'/'+'*'+Sample+'*'+part+'*.root'
    if len(glob.glob(JOBDIR+'/'+'*'+Sample+'*'+part+'*.root'))!=0:
        os.system(rm_rfile)

    #print samplename                                                                                                                                         

print "---LIST_OVER2RESUB---"
for a in LIST_OVER2RESUB:
    print a

LIST_RESUB_SAMPLENAME=list(set(LIST_RESUB_SAMPLENAME))
print "----LIST RESUB SAMPLES---"
for a in LIST_RESUB_SAMPLENAME:
    print a

print "---Summary---"
print "COMPLETE="+str(len(LIST_COMPLETE))
print "RUNNING="+str(len(LIST_RUNNING))
print "NOT_STARTED="+str(len(LIST_NOT_STARTED))
print "FAIL="+str(len(LIST_FAIL))
print "ZOMBIE="+str(len(LIST_ZOMBIE))
print "ZOMBIEINPUT="+str(len(LIST_ZOMBIEINPUT))

#if cleanjob : 
#    exit()

LIST_FAIL_RESUB={}


ANSWERED=0
want_remove='n'
##if answered by option
if options.remove_notstart:
    ANSWERED=1
    want_remove=options.remove_notstart
    print 'want to remove not started samples using condor_submit?->',want_remove
while ANSWERED==0:
    
    want_remove=raw_input('want to remove not started samples using condor_submit? (y/n)')
    print(want_remove)
    if want_remove=='y' or want_remove=='n':
        ANSWERED=1


if want_remove=='y':

    for a in LIST_NOT_STARTED:
        jidpath=JOBDIR+'/'+a+'.jid'
        
        f=open(jidpath)
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
            command='condor_rm '+jid+str(i) 
            print command
            os.system(command)


ANSWERED=0
want_resub='n'
##if answered by option
if options.resub_notstarted:
    ANSWERED=1
    want_resub=options.resub_notstarted
    print "want to add not started samples to failed job list?",want_resub
while ANSWERED==0:

    want_resub=raw_input('want to add not started samples to failed job list? (y/n)')
    print(want_resub)
    if want_resub=='y' or want_resub=='n':
        ANSWERED=1


if want_resub=='y':

    LIST_RESUB.update(LIST_NOT_STARTED)


ANSWERED=0
want_resub='n'
##if answered by option
if options.resub_fail:
    ANSWERED=1
    want_resub=options.resub_fail
    print "want to resubmit failed jobs using condor_submit?->",want_resub
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
##if answered by option
if options.chworkdir:
    ANSWERED=1
    want_modify_workdir=options.chworkdir
    print 'want to change workdir of failed jobs?',want_modify_workdir 
while ANSWERED==0:

    want_modify_workdir=raw_input('want to change workdir of failed jobs? (y/n)')
    print(want_modify_workdir)
    if want_modify_workdir=='y' or want_modify_workdir=='n':
        ANSWERED=1

ANSWERED=0
Nresub='all'
#if answered by option
if options.Nresub:
    ANSWERED=1
    Nresub=options.Nresub
    print 'number of Max resub jobs?->',Nresub 
while ANSWERED==0:

    Nresub=raw_input('number of resub jobs? (all / number of my submissions on queue(int))')
    print(Nresub)
    if Nresub=='all':
        ANSWERED=1
    else:
        try: 
            int(Nresub)
            ANSWERED=1
        except ValueError:
            ANSWERED=0


#CondorSpace=GetCondorSpace()
#if CondorSpace >70: ## more than 70G
print "[CONDOR SPACE] forece to WORK @ CONDOR SCRATCH"
want_modify_workdir='y'
##Get Nmyjob on queue

Nmyjob=GetNJobs()
print "##MY current njobs=",Nmyjob
print "-sample py ="+sample_py
exec open(sample_py).read()
idx_resub=0
total_resub=0
if Nresub=='all':
    total_resub=len(LIST_RESUB)
else:
    total_resub=max(0,int(Nresub)-int(Nmyjob))

print "Number of Resubmission===>",total_resub
#LIST_RESUB=list(set(LIST_RESUB))
print "len(LIST_RESUB)=",len(LIST_RESUB)


for a in LIST_RESUB:

    if idx_resub>=total_resub:
        break    
    samplename=LIST_RESUB[a]['Sample']
    print a
    #print "@@samplename="+samplename
    #print "LIST_FAIL[a]['input_s']="+LIST_FAIL[a]['input_s']
    if LIST_RESUB[a]['input_s']=='':
        dascheck='dasgoclient -timeout 5 -query="file dataset='+Samples[samplename]['nanoAOD']+'"'
        print "....."
        status, output = commands.getstatusoutput(dascheck)
        pypath=JOBDIR+'/'+a+'.py'
        
        if not check_file_das(pypath): 
            LIST_FAIL_RESUB[a]={'Production':LIST_RESUB[a]['Production'], 'Step':LIST_RESUB[a]['Step'], 'Sample':LIST_RESUB[a]['Sample'],'part':LIST_RESUB[a]['part']}
            
            continue
    #if '/store' in output: ## if file exists->resubmit
        #print "output="+output
    curdir=os.getcwd()
    
    os.chdir(JOBDIR)


    #this_memory = 0
    #print "logpath->",a+'.log'
    #if os.path.isfile(a+'.log') : 
    #    this_memory=CalcMemory(a+'.log')##inMB
    #    print "[MEMORY USAGE CHECK]",this_memory,"MB"
    #if this_memory > 2900:
    #    print "[JOB]Over 1000MB Memory, add request memory to jds"
    #    AddRequestMemory(a+'.jds')



    idx=len(glob.glob(a+'.log*'))
    if os.path.isfile(a+'.err') : os.system('mv '+a+'.err '+a+'.err_'+str(idx))
    if os.path.isfile(a+'.out') : os.system('mv '+a+'.out '+a+'.out_'+str(idx))
    if os.path.isfile(a+'.log') : os.system('mv '+a+'.log '+a+'.log_'+str(idx))
    if os.path.isfile(a+'.jid') : os.system('mv '+a+'.jid '+a+'.jid_'+str(idx))
    
    #if want_modify_workdir=='y': ##off this option. this is default
        #change_workdir(a+'.sh')

    resubmit='condor_submit '+a+'.jds > '+a+'.jid'
    print resubmit
    os.system(resubmit)
    idx_resub+=1
    os.chdir(curdir)
    
    print "--FIN.--"

print "Total Resubmt Result=",idx_resub

print "--RESUB FAIL--"
for a in LIST_FAIL_RESUB:
    print a
    



