import sys
mydir=sys.argv[1]

import glob

flist=glob.glob(mydir+'/*.root')
ntotal=len(flist)
import ROOT
idx=0
jobname=mydir.replace('/','_')+'_Weirdo.txt'
flog=open(jobname,'w')
for f in flist:
    idx+=1
    #if idx>85:continue
    print idx,'/',ntotal
    print f

    for trial in range(1):
        print 'trial=',trial
        tfile=ROOT.TFile.Open(f)
        cutlist=tfile.GetListOfKeys()
        keylist=ROOT.gDirectory.GetList()                                                                                                                                                                       
        print "len(cutlist)",len(cutlist)
        for cut in cutlist:
            cutname=cut.GetName()
            #print "key=",key                                                                                                                                                                                     
            #print 'dirname=',dirname                                                                                                                                                                             
            tfile.cd(cutname)
            variablelist=ROOT.gDirectory.GetListOfKeys()
            for variable in variablelist:
                variablename=variable.GetName()
                tfile.cd(cutname+'/'+variablename)
                hlist=ROOT.gDirectory.GetListOfKeys()
                for h in hlist:
                    hname=h.GetName()
                    hobj=tfile.Get(cutname+'/'+variablename+'/'+hname)
                    try:
                        hobj.Integral()
                    except:
                        flog.write(cutname+'/'+variablename+'/'+hname)
        tfile.Close()
flog.close()

