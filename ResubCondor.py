import sys
import glob
import os

class condorjob:
    def __init__(self,d):
        self.d=d
        self.jidfile=False
        self.donefile=False
        self.shfile=False
        self.pyfile=False
        self.jdsfile=False
        self.logfile=False
        self.errfile=False
        ###---
        self.IsTerminated=False
        self.IsFail=False
        self.jid=False

        if os.path.isfile(d+'/run.sh'): self.shfile=d+'/run.sh'
        if os.path.isfile(d+'/run.jid'): self.jidfile=d+'/run.jid'
        if os.path.isfile(d+'/run.done'): self.donefile=d+'/run.done'
        if os.path.isfile(d+'/run.py'): self.pyfile=d+'/run.py'
        if os.path.isfile(d+'/run.jds'): self.jdsfile=d+'/run.jds'
        if os.path.isfile(d+'/run.log'): self.logfile=d+'/run.log'
        if os.path.isfile(d+'/run.err'): self.errfile=d+'/run.err'

        self.Check()
        
    def Check(self):
        self.GetJid()
        self.CheckTerminated()
        self.CheckErrorfile()
        ##if terminated but no donefile->fail
        if self.IsTerminated and not self.donefile: self.IsFail=True
        
    def IsResub(self):
        if self.IsFail:
            return True
        else:
            return False
        
    def GetJid(self):
        if not self.jidfile:
            if self.donefile:
                self.jidfile=self.donefile
            else:
                self.IsFail=True
                self.jid=False

        f=open(self.jidfile)
        lines=f.readlines()##1 job(s) submitted to cluster 3294050.                                                                                                                                                                               
        self.jid=False
        for line in lines:
            if "submitted to cluster" in line:

                self.jid=line.split('job(s) submitted to cluster')[1].replace('.','')
                
                self.jid=int(self.jid)
                break
                
        f.close()
        
    def CheckTerminated(self):
        self.IsTerminated=False
        if not os.path.isfile(self.logfile):
            print "No log file, is terminated"
            self.IsTerminated=True
        f=open(self.logfile)
        lines=f.readlines()
        
        
        for line in lines:
            if 'Job terminated' in line and str(self.jid) in line:
                print "Job terminated"
                self.IsTerminated=True
                break
            if 'Job was aborted by the user' in line and str(self.jid) in line:
                print "Job was aborted by the user"
                self.IsTerminated=True
                break
            if 'reconnection failed' in line and str(self.jid) in line:
                print "reconnection failed"
                self.IsTerminated=True

            if 'Job executing on host' in line and str(self.jid) in line:
                print "Job executing on host -> reconnected"
                self.IsTerminated=False

        f.close()
        
    def CheckErrorfile(self):
        f=open(self.errfile)
        lines=f.readlines()
        self.IsFail=False
        for line in lines:
            if 'Server responded with an error' in line:
                self.IsFail=True
            if 'Error' in line and 'TNetXNGFile' in line:
                #if TightCheck:                                                                                                                                                                                                                   
                if not 'TNetXNGFile::Close' in line:
                    self.IsFail=True
                    print "Error in TNetXNGFile"
                    break
            #if 'Error' in line and '<TNetXNGFile::Open>' in line:
            #    if CheckSocketErrorOpen:
            #        self.IsFail=True
            #        print "socket open error->",self.errfile
            #        break
            if 'Error' in line and '<TNetXNGFile::Close>' in line:
                #if CheckSocketErrorClose:
                print "socket close error->",self.errfile
                self.IsFail=True
                break
            if 'Dictionary generation failed' in line :
                print "Dictionary generation failed"
                self.IsFail=True
            if 'Error' in line and '.pcm' in line:
                print "pcm error"
                self.IsFail=True
            if 'Failed to write out basket' in line:
                print "Failed to write out basket"
                #self.IsFail=True                                                                                                                                                                                                                      
            if 'No space left on device' in line:
                print "No space left on device"
                self.IsFail=True
            if 'Remote I/O error' in line:
                print "Remote I/O error"
                self.IsFail=True
            if 'Error: Parameters unset' in line:
                print 'Error: Parameters unset'
                self.IsFail=True
        f.close()

        
targetdir=sys.argv[1]
dirlist=glob.glob(targetdir+"/")

for d in dirlist:
    print d
    thisjob=condorjob(d)
    jid=thisjob.jid
    resub=thisjob.IsResub()

    if resub:
        print 'resub',d
        os.system('condor_rm '+str(jid))
        resub_command='condor_submit '+thisjob.jdsfile+" > "+thisjob.jidfile
        os.system(resub_command)

    elif thisjob.IsTerminated:
        print "done"

    else:
        print "running"
