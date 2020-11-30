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

  dict_info={}
  for hfit in [ [hfitdata,'data'], [hfitmc,'mc']]:
    frame = x.frame()    
    #hfitdata.plotOn(frame)
    #hfitdata.statOn(frame)
    hfit[0].plotOn(frame)
    hfit[0].statOn(frame)
    
    #s4=hfit[0].GetListOfFunctions().FindObject("stats")
    
    #s4.SetX1NDC(0.78)
    #s4.SetX2NDC(0.98)
    #s4.SetY1NDC(0.48)
    #s4.SetY2NDC(0.18)
    mean=ROOT.RooRealVar("mean","mean",85.782,65,105)
    width=ROOT.RooRealVar("width","width",2.085, 2.085-1*0.042, 2.085+1*0.042) ##decay width
    sigma=ROOT.RooRealVar("sigma","sigma",8, 5, 10.0) ##detector
    #gauss=ROOT.RooBreitWigner("gauss","gauss",x,mean,sigma) 
    gauss=ROOT.RooVoigtian("gauss","gauss",x,mean,width,sigma) 
    
    #filtersdata=gauss.fitTo(hfitdata)
    #filtersmc=gauss.fitTo(hfitmc)
    filters=gauss.fitTo(hfit[0])
    gauss.plotOn(frame,ROOT.RooFit.Layout(0.65,0.99,0.8))
    gauss.paramOn(frame,ROOT.RooFit.Layout(0.65))

    #print mean.getValV()

    ##---store infos
    _mean=mean.getValV()
    _width=width.getValV()
    _sigma=sigma.getValV()

    _mean_up=_mean+mean.getErrorHi()
    _mean_down=_mean+mean.getErrorLo()

    _width_up=_width+width.getErrorHi()
    _width_down=_width+width.getErrorLo()

    _sigma_up=_sigma+sigma.getErrorHi()
    _sigma_down=_sigma+sigma.getErrorLo()

    dict_info[hfit[1]]={
      'mean':_mean,
      'width':_width,
      'sigma':_sigma,


      'mean_up':_mean_up,
      'mean_down':_mean_down,

      'width_up':_width_up,
      'width_down':_width_down,

      'sigma_up':_sigma_up,
      'sigma_down':_sigma_down,
      
    }

    #mean.Print()
    #width.Print()
    #sigma.Print()

    c1=ROOT.TCanvas()
    frame.SetTitle(hfit[1])
    frame.Draw()
    c1.SaveAs('roofit_'+hfit[1]+'.pdf')

  ##--JMS,JMR
  dict_info['jms']=dict_info['data']['mean']/dict_info['mc']['mean']
  dict_info['jmr']=dict_info['data']['sigma']/dict_info['mc']['sigma']

  

  ##--save info
  f=open('fit_info.py','w')
  f.write(str(dict_info))
  f.close()

if __name__ == '__main__':
  #--
  print "a"
  UseROOTFIT()
