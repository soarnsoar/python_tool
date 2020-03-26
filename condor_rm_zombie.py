import os
import sys
scriptpath=os.path.realpath(__file__)
scriptpath=scriptpath.split(sys.argv[0].split('/')[-1])[0]
#print 'scriptpath=',scriptpath
sys.path.insert(0, scriptpath)
from GetJidFromJIDFILE import *

import glob

if __name__ == '__main__':
    dirpath = sys.argv[1]
    old_jids=glob.glob(dirpath+'/*.jid_*')
    print len(old_jids)
    for fjid in old_jids:
        jid=GetJidFromJIDFILE(fjid)
        #print '--',fjid
        if jid!="":
            #print jid 
            condor_rm = "condor_rm "+str(jid)
            #print condor_rm
            os.system(condor_rm)
