import ROOT
import sys
import os


ROOT.gEnv.SetValue("TFile.Recover",0)
def ConvertPath(INPUT):
    if "root://cms-xrdr.private.lo:2094" in INPUT:
        INPUT=INPUT.split('/xrd/')[1]
        INPUT='/xrootd/'+INPUT
        USER=str(os.environ.get("USER"))
        print USER
        if USER=="jhchoi":
            INPUT=INPUT.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','/xrootd_user/jhchoi/xrootd/Latino/HWWNano/')
    return INPUT

def BoolGetEntries(myTree):
    try:
        boolean=bool(myTree.GetEntries())
        #print myTree.GetEntries()
    #except ValueError:
    except AttributeError:
        boolean=False
    return boolean

def OpenFileInPyroot(INPUT):
    
    #print INPUT
    INPUT=ConvertPath(INPUT)
    f=ROOT.TFile(INPUT,'READ')
    #print "bool(f.IsZombie())",bool(f.IsZombie())
    IsZombie=bool(f.IsZombie())
    myTree=f.Get("Runs")
    #print "bool(myTree)",bool(myTree)

    output=BoolGetEntries(myTree)
    #print output


    f.Close()

    del myTree
    del f
    return output and (not IsZombie)

if __name__ == '__main__':
    INPUT=sys.argv[1]
    print "INPUT=",INPUT



    print OpenFileInPyroot(INPUT)
