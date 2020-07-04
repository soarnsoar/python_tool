import sys
import os
#condor_q -global -all -global -all $1 -af:jh Owner RemoteHost CPUsUsage JobPrio JobBatchName|grep jhchoi
#3772591.0   jhchoi undefined                     undefined             0       NanoGardening__Summer16_102X_nAODv5_Full2016v6__METdo
def CondorIncreasePrioUsingBatchName(name,myprio):
    command='condor_q -global -all -global -all $1 -af:jh Owner RemoteHost CPUsUsage JobPrio JobBatchName|grep jhchoi'
    os.system(command+ ' &> joblist.txt')
    f=open('joblist.txt','r')
    lines=f.readlines()

    name=name.split(',')

    for line in lines:
        info=line.split()
        jid=info[0]
        prio=info[4]
        batchname=info[5]
        #print jid,prio,batchname
        if batchname in name:
            increase='condor_prio -p '+myprio+' '+jid
            print increase
            os.system(increase)
            #break

    f.close()


if __name__ == '__main__':
    name=sys.argv[1]
    myprio=sys.argv[2]
    CondorIncreasePrioUsingBatchName(name,myprio)
