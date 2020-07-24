import sys
import os
#condor_q -global -all -global -all $1 -af:jh Owner RemoteHost CPUsUsage JobPrio JobBatchName|grep jhchoi
#3772591.0   jhchoi undefined                     undefined             0       NanoGardening__Summer16_102X_nAODv5_Full2016v6__METdo
def CondorRmBatchName(name):

    command="condor_rm -constraint 'JobBatchName == \""+name+"\"'"
    os.system(command)
    command="condor_rm -f -constraint 'JobBatchName == \""+name+"\"'"
    os.system(command)



if __name__ == '__main__':
    names=sys.argv[1]
    names=names.split(',')
    for name in names:
        CondorRmBatchName(name)
