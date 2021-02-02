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


def GetNJobsByName(key):
    USER=os.getenv('USER')
    #command=['condor_q',USER,"-constraint", "'"+"regexp("+'"'+key+"*"+'"'+", JobBatchName, \"i\")"+"'"]
    
    #print ' '.join(command)
    #proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    #(stdout, stderr) = proc.communicate()
    #print 'stdout',stdout
    #print 'stderr',stderr
    f=os.popen('condor_q '+USER+' -constraint '+"'"+"regexp("+'"'+key+"*"+'"'+", JobBatchName, \"i\")"+"'")
    lines=f.readlines()
    NJOBS=-1
    for line in lines:
        #print line
        if TotalJobFlag in line:
            NJOBS=line.split(TotalJobFlag)[1].split('jobs')[0].replace(' ','')
    #NJOBS=stdout.split(TotalJobFlag)[1].split('jobs')[0].replace(' ','')
    #print NJOBS
    return int(NJOBS)
if __name__ == '__main__':
    #N=GetNJobs()
    N=GetNJobsByName('mkShap')
    print N
