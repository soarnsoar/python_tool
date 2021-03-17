import os
import sys
import glob
def GetJid(jidfile):

    if not os.path.isfile(jidfile):
        jidfile=jidfile.replace('.jid','.done')
    if not os.path.isfile(jidfile):
        #print "Fail to Get jid of",jidfile
        return False,False
    f=open(jidfile)
    lines=f.readlines()##1 job(s) submitted to cluster 3294050.
    jid=False
    dryrun=False
    for line in lines:
        if "submitted to cluster" in line:

            jid=line.split('job(s) submitted to cluster')[1].replace('.','')

            jid=int(jid)
            break
        if 'DRY' in line:
            dryrun=True
            break
    f.close()
    return jid,dryrun


if __name__ == '__main__':
    ##---
    dirpath=sys.argv[1]
    key=sys.argv[2]
    myprio=sys.argv[3]

    print dirpath,key,myprio
    jidfiles=glob.glob(dirpath+'/*'+key+'*.jid')


    for jidfile in jidfiles:
        #condor_prio -p '+myprio+' '+jid
        jid,dryrun=GetJid(jidfile)
        if jid and not dryrun:
            increase='condor_prio -p '+myprio+' '+str(jid)
            print increase,jidfile
            os.system(increase)
