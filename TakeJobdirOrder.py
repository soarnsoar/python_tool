from collections import OrderedDict
import os
import glob
def TakeJobdirOrder():
    
    os.system('condor_q jhchoi|grep jhchoi &> myjobs.txt')
    os.system("condor_q -global -all -global -all $1 -af:jh Owner RemoteHost CPUsUsage JobPrio JobBatchName|grep jhchoi &> condor_prio_info.txt")
    
    fprio=open('condor_prio_info.txt','r')
    lines=fprio.readlines()
    
    batchprios=OrderedDict()
    for line in lines:
        info=line.split()
        jid=info[0]
        prio=info[4]
        batchname=info[5]
        if batchname in batchprios: continue
        batchprios[batchname]=prio
            
    
    fprio.close()

    
    #f=open('myjobs.txt','r')
    #lines=f.readlines()
    #for line in lines:
    #    this_jobdir=line.split()[1]
    #    if not this_jobdir in jobdirs : jobdirs.append(this_jobdir)
    #f.close()
    
    priolist=sorted([(value,key) for (key,value) in batchprios.items()],reverse=True)
    jobdirs=[]
    for batchname in priolist:
        #print batch[1]
        jobdirs.append(batchname[1])
    

    normal_list=glob.glob('NanoGardening__*/')
    for mydir in normal_list:

        if mydir.replace('/','') in jobdirs: continue
        jobdirs.append(mydir)

    return jobdirs

if __name__ == '__main__':
    
    mylist=TakeJobdirOrder()
    for d in mylist:
        print d
