import ROOT
import copy
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookHowToFit#Fitting_a_Breit_Wigner
##BW
#https://twiki.cern.ch/twiki/pub/CMSPublic/WorkBookHowToFit/BW.C.txt
def mybw(x,par):

  arg1 = 14.0/22.0 ## 2 over pi
  arg2 = par[1]*par[1]*par[2]*par[2] ##Gamma=par[1]  M=par[2]
  arg3 = ((x[0]*x[0]) - (par[2]*par[2]))*((x[0]*x[0]) - (par[2]*par[2]))
  arg4 = x[0]*x[0]*x[0]*x[0]*((par[1]*par[1])/(par[2]*par[2]))
  return par[0]*arg1*arg2/(arg3 + arg4);




def dofitbw(massMin,massMass):

    func=ROOT.TF1("mybw",mybw,massMin,massMax,3)
    func.SetParameter(0,1.0) ##
    func.SetParName(0,"const")
    func.SetParameter(2,5.0);
    func.SetParName(1,"sigma");
    func.SetParameter(1,80.0);
    func.SetParName(2,"mean");

def GetHisto(filepath,histopathlist):
  f=ROOT.TFile.Open(filepath)

  histolist=[]

  for histopath in histopathlist:

    htemp=f.Get(histopath)
    h=copy.deepcopy(htemp.Clone())
    histolist.append(h)

  newhisto=histolist[0].Clone()
  newhisto.SetDirectory(0)
  for histo in histolist[1:] :
    newhisto.Add(histo)
    

  _newhisto=copy.deepcopy(newhisto)
  f.Close()
  return _newhisto

def UseROOTmacro():

    ##--read histo
    filepath='hadd.root'
    cutname='__BoostedALL_TOP_NoMEKDCut'
    xname='HadronicW_mass'
    bkglist=['WW','Wjets','TT','SingleTop','MultiV']

    bkghistopathlist=[]
    for bkg in bkglist:
      path=cutname+'/'+xname+'/'+'histo_'+bkg
      bkghistopathlist.append(path)
    hbkg=GetHisto(filepath,bkghistopathlist)
    hbkg.SetTitle('hbkg')
    hbkg.SetName('hbkg')
    hdata=GetHisto(filepath,[cutname+'/'+xname+'/'+'histo_DATA'])

    ##--fitting function
    massMin=65.
    massMax=105.
    func=ROOT.TF1("mybw",mybw,massMin,massMax,3)
    func.SetParameter(0,1.0) ##
    func.SetParName(0,"const")
    func.SetParameter(2,5.0);
    func.SetParName(1,"sigma");
    func.SetParameter(1,80.0);
    func.SetParName(2,"mean");    
    
    c1=ROOT.TCanvas()

    hbkg.Fit("mybw","QR")
    c1.SaveAs('temp_bkg.pdf')

    hdata.Fit("mybw","QR")
    c1.SaveAs('temp_data.pdf')
    #f=ROOT.TFile.Open('hadd.root')
    #h=f.Get(cutname+'/'+x+)

def UseROOTFIT():


  ##--read histo
  filepath='hadd.root'
  cutname='__BoostedALL_TOP_NoMEKDCut'
  xname='HadronicW_mass'
  mclist=['WW','Wjets','TT','SingleTop','MultiV']
  
  mchistopathlist=[]
  for mc in mclist:
    path=cutname+'/'+xname+'/'+'histo_'+mc
    mchistopathlist.append(path)
  hmc=GetHisto(filepath,mchistopathlist)
  hmc.SetTitle('hmc')
  hmc.SetName('hmc')
  hdata=GetHisto(filepath,[cutname+'/'+xname+'/'+'histo_DATA'])


  #https://twiki.cern.ch/twiki/pub/CMSPublic/WorkBookHowToFit/RooFitMacro.C
  #https://www.nikhef.nl/~vcroft/GettingStartedWithRooFit.html
  hmin=65
  hmax=105
  x=ROOT.RooRealVar("x","x",hmin,hmax)
  l=ROOT.RooArgList(x)
  #  RooDataHist::RooDataHist(const char* name, const char* title, const RooArgList& vars, const TH1* hist, double initWgt = 1.) =>
  hfitdata=ROOT.RooDataHist("hdata","hdata",l,hdata) 
  hfitmc=ROOT.RooDataHist("hmc","hmc",l,hmc) 


  for hfit in [ [hfitdata,'data'], [hfitmc,'mc']]:
    frame = x.frame()    
    #hfitdata.plotOn(frame)
    #hfitdata.statOn(frame)
    hfit[0].plotOn(frame)
    hfit[0].statOn(frame)
    
    mean=ROOT.RooRealVar("mean","mean",85.782,65,105)
    width=ROOT.RooRealVar("width","width",16.3, 0.0, 120.0)
    sigma=ROOT.RooRealVar("sigma","sigma",16.3, 0.0, 120.0)
    gauss=ROOT.RooBreitWigner("gauss","gauss",x,mean,sigma) 
    
    #filtersdata=gauss.fitTo(hfitdata)
    #filtersmc=gauss.fitTo(hfitmc)
    filters=gauss.fitTo(hfit[0])
    gauss.plotOn(frame)
    gauss.paramOn(frame)
    c1=ROOT.TCanvas()
    frame.Draw()
    c1.SaveAs('roofit_'+hfit[1]+'.pdf')

if __name__ == '__main__':
  #--
  print "a"
  UseROOTFIT()
