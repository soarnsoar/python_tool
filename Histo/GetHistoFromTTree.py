import ROOT

def GetHistoFromTTree(filelist,TreeName,X,Selection):
    ####-------^___^--------####
    ##--Design :

    ##--input : arguments above
    ##--return th1d object with setdirectory(0)

    ROOT.gROOT.SetBatch(True)##--No display


    MYCHAIN = ROOT.TChain(TreeName)
    for myf in filelist:
        MYCHAIN.Add(myf)


    MYCHAIN.Draw(X,Selection) ##Draw formula with input selection
    htemp=ROOT.gPad.GetPrimitive("htemp")
    htemp.SetDirectory(0)

    return htemp

if __name__ == '__main__':
    filelist=['/cms/ldap_home/jhchoi/temp/nanoLatino_VBFHToWWToLNuQQ_M1000__part0.root']
    myhisto=GetHistoFromTTree(filelist,'Events','Lepton_pt','1')
    c1=ROOT.TCanvas()
    myhisto.Draw()
    c1.SaveAs('test.pdf')
