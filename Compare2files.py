


import sys
import glob
import optparse

import ROOT
def Check_a_File(f):
    tfile=ROOT.TFile.Open(f)
    cutlist=tfile.GetListOfKeys()
    keylist=ROOT.gDirectory.GetList()                                                                                                                                                                       
    pathlist=[]
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
                pathlist.append(cutname+'/'+variablename+'/'+hname)
                try:
                    hobj.Integral()
                except:
                    print "!!!!! fail!!!!"
                    print cutname+'/'+variablename+'/'+hname
                    #flog.write(cutname+'/'+variablename+'/'+hname)

    print "[DONE]"
    tfile.Close()
    print "Fin. Close"


    return pathlist



def Compare(filepath1,filepath2,pathlist):##
    tf1=ROOT.TFile.Open(filepath1)
    tf2=ROOT.TFile.Open(filepath2)
    for path in pathlist:
        h1=tf1.Get(path)
        h2=tf1.Get(path)
        N= h1.GetNbinsX()
        for i in range(N):
            y1=h1.GetBinContent(i)
            y2=h2.GetBinContent(i)
            if y1!=y2:
                print path,i
            
if __name__ == '__main__':
   usage = 'usage: %prog [options]'
   parser = optparse.OptionParser(usage)
   parser.add_option("-a","--file1",   dest="filepath1")
   parser.add_option("-b","--file2",   dest="filepath2")
   (options, args) = parser.parse_args()

   f=options.filepath1
   pathlist=Check_a_File(f)
   #print "finish"
   Compare(filepath1,filepath2,pathlist)
