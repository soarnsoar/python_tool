import sys
mydir=sys.argv[1]

import glob

flist=glob.glob(mydir+'/*.root')
ntotal=len(flist)
import ROOT
idx=0
for f in flist:
    print idx,'/',ntotal
    mytfile=ROOT.TFile.Open(f,'READ')
    iszombie=mytfile.IsZombie()

    if iszombie:
        print mytfile
    mytfile.Close()
    idx+=1
