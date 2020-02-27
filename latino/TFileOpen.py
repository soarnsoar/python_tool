import ROOT

def ConvertToXROOTDpath(filepath):
    if "root://cms-xrdr.private.lo:2094" in filepath:
        return filepath



    if "/xrootd_user/jhchoi/xrootd/Latino/HWWNano/" in filepath:

        filepath=filepath.replace('//','/').replace('/xrootd_user/jhchoi/xrootd/Latino/HWWNano/','root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano/')
    elif "/xrootd/store/user/jhchoi/Latino/HWWNano/" in filepath:
        filepath=filepath.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano/')
    return filepath


def TFileOpen(filepath):
    #filepath=ConvertXROOTDpath(filepath)                                                                                                                                         

    filepath=ConvertToXROOTDpath(filepath)
    #print "[filepath in TFileOpen]",filepath                                                                                                                                     
    ##if the file not exist                                                                                                                                                       
    #if not os.path.isfile(filepath):return False                                                                                                                                 

    #print filepath                                                                                                                                                               
    f=ROOT.TFile.Open(filepath,'READ')
    if not bool(f):
        print filepath,'cannot be opened'
        return False
    IsZombie=bool(f.IsZombie())
    myTree=f.Get("Runs")

    try:
        boolean=bool(myTree.GetEntries())
    except AttributeError:
        boolean=False


    f.Close()

    del myTree
    del f

    return boolean and not IsZombie
