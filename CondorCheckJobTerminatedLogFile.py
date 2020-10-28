####-------
##-> Define function to check condor log file if there's terminated line.


#########    ( example )   005 (8535919.000.000) 10/28 20:40:45 Job terminated.

def CondorCheckJobTerminatedLogFile(logpath,jid):
    Terminated=False
    f=open(logpath,'r')
    lines=f.readlines()
    for line in lines:
        if str(jid) in line and 'Job terminated' in line: Terminated=True

    f.close()
    return Terminated
