from ROOT import TFile,TTree
import sys



def ConvertPath(INPUT):
    if "root://cms-xrdr.private.lo:2094" in INPUT:
        INPUT=INPUT.split('/xrd/')[1]
        INPUT='/xrootd/'+INPUT
        INPUT=INPUT.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','/xrootd_user/jhchoi/xrootd/Latino/HWWNano/')
    return INPUT

def BoolGetEnties(myTree):
    try:
        boolean=bool(myTree.GetEntries())
        #print myTree.GetEntries()
    #except ValueError:
    except AttributeError:
        boolean=False
    return boolean

def OpenFileInPyroot(INPUT):

    print INPUT
    INPUT=ConvertPath(INPUT)
    f=TFile(INPUT,'READ')
    myTree=f.Get("Runs")


    output=BoolGetEnties(myTree)
    #print output


    f.Close()

    del myTree
    del f
    return output

if __name__ == '__main__':
    INPUT=sys.argv[1]
    print "INPUT=",INPUT



    print OpenFileInPyroot(INPUT)
