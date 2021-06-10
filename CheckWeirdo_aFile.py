


import sys
import glob
import optparse

import ROOT
def Check_a_File(f):
    tfile=ROOT.TFile.Open(f)
    cutlist=tfile.GetListOfKeys()
    keylist=ROOT.gDirectory.GetList()                                                                                                                                                                       
    idx=0
    print "len(cutlist)",len(cutlist)
    for cut in cutlist:
        idx+=1
        print idx,'/',len(cutlist)


        cutname=cut.GetName()
        #print "key=",key                                                                                                                                                                                          #print 'dirname=',dirname                                                                                                                                                                             
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
                    print "!!!!! fail!!!!"
                    print cutname+'/'+variablename+'/'+hname
                    #flog.write(cutname+'/'+variablename+'/'+hname)

    print "[DONE]"
    tfile.Close()
    print "Fin. Close"




if __name__ == '__main__':
   usage = 'usage: %prog [options]'
   parser = optparse.OptionParser(usage)
   parser.add_option("-f","--filepath",   dest="filepath")
   (options, args) = parser.parse_args()

   f=options.filepath
   Check_a_File(f)
   #print "finish"
