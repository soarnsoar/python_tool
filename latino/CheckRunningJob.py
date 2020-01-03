import os
import subprocess


TotalJobFlag='Total for query:'


def CheckRunningJob(jid):
    #print 'jid=',jid
    USER=os.getenv('USER')

    if jid.replace(' ','')=='':
        print "[CheckRunningJob.py]no jid"
        return False
    
    proc=subprocess.Popen(['condor_q',jid],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    (stdout, stderr) = proc.communicate()

    #print stdout
    NJOBS=stdout.split(TotalJobFlag)[1].split('jobs')[0].replace(' ','')
    

    if NJOBS=='0':
        print "[CheckRunningJob.py] No Running jobs"
        return False
    else:
        return True

if __name__ == '__main__':
    a=CheckRunningJob('2358898')
    print a
