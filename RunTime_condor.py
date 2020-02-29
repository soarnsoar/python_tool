import glob
import sys
from datetime import datetime
def GetStartTime(line):
    #001 (3287776.000.000) 02/27 19:00:23 Job executing on host: <134.75.125.44:9618?addrs=134.75.125.44-9618+[2001-320-15-125-ca1f-66ff-fedb-5db9]-9618&noUDP&sock=25149_b35f_6>
    MMDDhhmmss=line.split('Job executing on host')[0].split(')')[1] ##02/27 19:00:23
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

def GetEndTime(line):
    #005 (3287776.000.000) 02/27 19:32:38 Job terminated.
    MMDDhhmmss=line.split('Job terminated')[0].split(')')[1] ##' 02/27 19:32:38 '
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



mydir=sys.argv[1] 
print "dir=",mydir
key=''
if len(sys.argv)>2:
    key=sys.argv[2]+'*'

loglist=glob.glob(mydir+'/*'+key+'.log')
print 'N log file=',len(loglist)

MaxRuntime=-1
MaxRuntimeFile=''
MinRuntime=9999999999999.
MinRuntimeFile=''
SumRuntime=0

for log in loglist:
    #print log
    ValidStart=False
    ValidEnd=False

    f=open(log,'r')
    lines=f.readlines()
    StartTime=0
    for line in lines:
        #22872  -  RuntimeUsage of job (MB)
        #166    RuntimeUsage of job (MB)
        if 'Job executing on host' in line:
            StartTime=GetStartTime(line)
            #print StartTime
            ValidStart=True
            #print "ValiStart"
        if 'Job terminated' in line:
            EndTime=GetEndTime(line)
            ValidEnd=True
            #print EndTime
            #print EndTime.year
            #print "ValidEnd"

    f.close()
    #print "ValidStart=",ValidStart
    #print "ValidEnd=",ValidEnd
    #print "ValiStart*ValidEnd=",ValiStart*ValidEnd
    #print "not(ValiStart*ValidEnd)=",not(ValiStart*ValidEnd)


    if not ValidStart : continue
    if not ValidEnd : continue
    #print "pass"
    if EndTime.year < StartTime.year:
        EndTime.year=EndTime.year+1
    thisRuntime=(EndTime-StartTime).seconds
    #print thisRuntime
    
    if thisRuntime>MaxRuntime: 
        MaxRuntime=thisRuntime
        MaxRuntimeFile=log
    if thisRuntime<MinRuntime:
        MinRuntime=thisRuntime
        MinRuntimeFile=log
    SumRuntime+=thisRuntime

    

print "Avg Runtime =", SumRuntime/len(loglist),"sec"
print "Max Runtime =", MaxRuntime, "sec"
print "Max Runtime File =", MaxRuntimeFile
print "Min Runtime =", MinRuntime, "sec"
print "Min Runtime File =", MinRuntimeFile
