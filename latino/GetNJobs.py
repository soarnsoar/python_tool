import os
import subprocess


TotalJobFlag='Total for query:'


def GetNJobs():
    USER=os.getenv('USER')
    proc=subprocess.Popen(['condor_q',USER],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    (stdout, stderr) = proc.communicate()
    #print 'stdout',stdout
    #print 'stderr',stderr
    NJOBS=stdout.split(TotalJobFlag)[1].split('jobs')[0].replace(' ','')
    #print NJOBS
    return int(NJOBS)
if __name__ == '__main__':
    GetNJobs()
