import ROOT
from copy import deepcopy

def Copy(f_i,f_o,histopath_list):
    tf_i=ROOT.TFile.Open(f_i)
    tf_o=ROOT.TFile.Open(f_o,"UPDATE")
    n=len(histopath_list)
    idx=0
    for histopath in histopath_list:
        idx+=1
        print idx,'/',n
        print histopath
        h=tf_i.Get(histopath).Clone()
        h.SetDirectory(0)
        dirpath='/'.join(histopath.split('/')[:-1])
        histoname=histopath.split('/')[-1]
        tf_o.cd(dirpath)
        tf_o.WriteObject(h,histoname)
    tf_i.Close()
    tf_o.Close()
def GetHistopathList(f_i,suffix):

    ret=[]
    tfile=ROOT.TFile.Open(f_i)
    cutlist=tfile.GetListOfKeys()
    for cut in cutlist:


        cutname=cut.GetName()
        tfile.cd(cutname)
        variablelist=ROOT.gDirectory.GetListOfKeys()    
        for variable in variablelist:
          variablename=variable.GetName()
          tfile.cd(cutname+'/'+variablename)
          histolist=ROOT.gDirectory.GetListOfKeys()
          for histo in histolist:
            histoname=histo.GetName()
            #print histoname
            fullpath='/'.join([cutname,variablename,histoname])
            #print fullpath
            if fullpath.endswith(suffix):ret.append(fullpath)
    tfile.Close()
    return ret
if __name__ == '__main__':
    import optparse
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option("-i", "--input", dest="f_i" , help="input")
    parser.add_option("-o", "--output", dest="f_o" , help="output")

    (options, args) = parser.parse_args()

    #year=options.year
    f_i=options.f_i
    f_o=options.f_o

    #f_i='../test_write_histo/Input/hadd.root'
    #f_o='../test_write_histo/Output/hadd.root'
    suffix='Up'
    #Copy(f_i,f_o,suffix)
    list_Up=deepcopy(GetHistopathList(f_i,suffix))
    suffix='Down'
    list_Down=deepcopy(GetHistopathList(f_i,suffix))
    histopath_list=list_Up+list_Down
    #histopath_list=[histopath_list[0],histopath_list[1]]
    Copy(f_i,f_o,histopath_list)

    
