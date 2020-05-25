import ROOT
import math
ROOT.gROOT.SetBatch(True)
class HistoParser():
    def __init__(self,mydict):
        ####mydict####
        self.mydict=mydict
        ##mydict[grname]={cut,variables,FileName,samples}
        ##will define
        ##mydict[grname]['histo'][cut][variables][sample]=TH*D
        ##mydict[grname]['histo'][cut][variables]['Sum']=TH*D
        self.ReadHistos()

    def ReadHistos(self):
        for gr in self.mydict:
            self.mydict[gr]['histo']={}
            filename=self.mydict[gr]['FileName']
            f=ROOT.TFile.Open(filename)
            for cut in self.mydict[gr]['cuts']:
                self.mydict[gr]['histo'][cut]={}
                for variable in self.mydict[gr]['variables']:
                    self.mydict[gr]['histo'][cut][variable]={}
                    idx=0
                    integrals=0.
                    #self.mydict[gr]['histo'][cut][variable]['Sum']=
                    for sample in self.mydict[gr]['samples']:
                        #print '----cut=',cut,'variable',variable,'sample=',sample,'-----'
                        histopath=cut+'/'+variable+'/histo_'+sample
                        #print histopath
                        htemp=f.Get(cut+'/'+variable+'/histo_'+sample)
                        #print "type(htemp)",type(htemp)
                        self.mydict[gr]['histo'][cut][variable][sample]=htemp.Clone()
                        self.mydict[gr]['histo'][cut][variable][sample].SetDirectory(0)
                        #print "htemp.Integral()=",htemp.Integral()
                        #print "self.mydict[gr]['histo'][cut][variable][sample].Integral()",self.mydict[gr]['histo'][cut][variable][sample].Integral()
                        if idx==0:
                            self.mydict[gr]['histo'][cut][variable]['Sum']=htemp.Clone()
                            self.mydict[gr]['histo'][cut][variable]['Sum'].SetDirectory(0)
                        else:
                            self.mydict[gr]['histo'][cut][variable]['Sum'].Add(htemp)
                        integrals+=self.mydict[gr]['histo'][cut][variable][sample].Integral()
                        #print "sum one by one=",integrals
                        #print "integral sum histo=",self.mydict[gr]['histo'][cut][variable]['Sum'].Integral()
                        idx+=1
                        #print "type(self.mydict[gr]['histo'][cut][variable][sample])",type(self.mydict[gr]['histo'][cut][variable][sample])
                        #print "gr=",gr,'cut=',cut,'variable=',variable,'sample=',sample
                        #print "print type(mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['DATA'])=",type(mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['DATA'])
                    
            f.Close()
    def MakeEnvelopShape(self,envelopHistoName):
        for gr in self.mydict:
            for cut in self.mydict[gr]['cuts']:
                for variable in self.mydict[gr]['variables']:
                    ###For this cut, this variable
                    ###iterate each shape

                    Nbins=-1
                    for sample in self.mydict[gr]['samples']:
                        self.mydict[gr]['histo'][cut][variable]['envelopUp']=self.mydict[gr]['histo'][cut][variable][sample].Clone()
                        self.mydict[gr]['histo'][cut][variable]['envelopUp'].SetDirectory(0)
                        self.mydict[gr]['histo'][cut][variable]['envelopUp'].SetName(envelopHistoName+"Up")
                        self.mydict[gr]['histo'][cut][variable]['envelopUp'].SetTitle(envelopHistoName+"Up")

                        self.mydict[gr]['histo'][cut][variable]['envelopDown']=self.mydict[gr]['histo'][cut][variable][sample].Clone()
                        self.mydict[gr]['histo'][cut][variable]['envelopDown'].SetDirectory(0)
                        self.mydict[gr]['histo'][cut][variable]['envelopDown'].SetName(envelopHistoName+"Down")
                        self.mydict[gr]['histo'][cut][variable]['envelopDown'].SetTitle(envelopHistoName+"Down")
                        Nbins=self.mydict[gr]['histo'][cut][variable]['envelopUp'].GetNbinsX()
                        break ##only for the first sample to get Nbins
                    #print Nbins
                    for ibin in range(0,Nbins+1):
                        
                        ymax=self.mydict[gr]['histo'][cut][variable]['envelopDown'].GetBinContent(ibin)
                        ymaxerr=self.mydict[gr]['histo'][cut][variable]['envelopDown'].GetBinError(ibin)
                        ymin=self.mydict[gr]['histo'][cut][variable]['envelopDown'].GetBinContent(ibin)
                        yminerr=self.mydict[gr]['histo'][cut][variable]['envelopDown'].GetBinError(ibin)
                        for sample in self.mydict[gr]['samples']:
                            y=self.mydict[gr]['histo'][cut][variable][sample].GetBinContent(ibin)
                            yerr=self.mydict[gr]['histo'][cut][variable][sample].GetBinError(ibin)
                            if y >= ymax : 
                                ymax=y
                                ymaxerr=yerr
                            if y < ymin : 
                                ymin=y
                                yminerr=yerr
                        self.mydict[gr]['histo'][cut][variable]['envelopUp'].SetBinContent(ibin,ymax)
                        self.mydict[gr]['histo'][cut][variable]['envelopDown'].SetBinContent(ibin,ymin)
                        
    def MakeSymhessianAsShape(self,symhessianasHistoName):
        for gr in self.mydict:
            for cut in self.mydict[gr]['cuts']:
                for variable in self.mydict[gr]['variables']:
                    ###For this cut, this variable
                    ###iterate each shape

                    Nbins=-1
                    for sample in self.mydict[gr]['samples']:
                        self.mydict[gr]['histo'][cut][variable]['symhessianasUp']=self.mydict[gr]['histo'][cut][variable][sample].Clone()
                        self.mydict[gr]['histo'][cut][variable]['symhessianasUp'].SetDirectory(0)
                        self.mydict[gr]['histo'][cut][variable]['symhessianasUp'].SetName(symhessianasHistoName+"Up")
                        self.mydict[gr]['histo'][cut][variable]['symhessianasUp'].SetTitle(symhessianasHistoName+"Up")

                        self.mydict[gr]['histo'][cut][variable]['symhessianasDown']=self.mydict[gr]['histo'][cut][variable][sample].Clone()
                        self.mydict[gr]['histo'][cut][variable]['symhessianasDown'].SetDirectory(0)
                        self.mydict[gr]['histo'][cut][variable]['symhessianasDown'].SetName(symhessianasHistoName+"Down")
                        self.mydict[gr]['histo'][cut][variable]['symhessianasDown'].SetTitle(symhessianasHistoName+"Down")
                        Nbins=self.mydict[gr]['histo'][cut][variable]['symhessianasUp'].GetNbinsX()
                        break ##only for the first sample to get Nbins
                    #print Nbins
                    for ibin in range(0,Nbins+1):
                        
                        y0=self.mydict[gr]['histo'][cut][variable]['symhessianasDown'].GetBinContent(ibin)
                        y0err=self.mydict[gr]['histo'][cut][variable]['symhessianasDown'].GetBinError(ibin)
                        ##sigma = sqrt(sum[ (yi-y0)**2])
                        SumOfDiff2=0

                        Nsample=len(self.mydict[gr]['samples'])
                        for isample, sample in enumerate(self.mydict[gr]['samples']): ##Make symhessianas up/down
                            y=self.mydict[gr]['histo'][cut][variable][sample].GetBinContent(ibin)
                            yerr=self.mydict[gr]['histo'][cut][variable][sample].GetBinError(ibin)
                            if isample < Nsample-2:
                                SumOfDiff2+=(y-y0)**2
                            else: 
                                continue
                        ##alpha_s
                        plus_sample=self.mydict[gr]['samples'][-2]
                        yplus=self.mydict[gr]['histo'][cut][variable][plus_sample].GetBinContent(ibin)
                        minus_sample=self.mydict[gr]['samples'][-2]
                        yminus=self.mydict[gr]['histo'][cut][variable][minus_sample].GetBinContent(ibin)

                        sigma_as = 0.5*(yplus-yminus)
                        sigma=math.sqrt(SumOfDiff2 + sigma_as**2)
                        self.mydict[gr]['histo'][cut][variable]['symhessianasUp'].SetBinContent(ibin,y0+sigma)
                        self.mydict[gr]['histo'][cut][variable]['symhessianasDown'].SetBinContent(ibin,y0-sigma)

    def MakeRmsShape(self,rmsHistoName):
        for gr in self.mydict:
            for cut in self.mydict[gr]['cuts']:
                for variable in self.mydict[gr]['variables']:
                    ###For this cut, this variable
                    ###iterate each shape
                    Nbins=-1
                    for sample in self.mydict[gr]['samples']:
                        self.mydict[gr]['histo'][cut][variable]['rmsUp']=self.mydict[gr]['histo'][cut][variable][sample].Clone()
                        self.mydict[gr]['histo'][cut][variable]['rmsUp'].SetDirectory(0)
                        self.mydict[gr]['histo'][cut][variable]['rmsUp'].SetName(rmsHistoName+"Up")
                        self.mydict[gr]['histo'][cut][variable]['rmsUp'].SetTitle(rmsHistoName+"Up")

                        self.mydict[gr]['histo'][cut][variable]['rmsDown']=self.mydict[gr]['histo'][cut][variable][sample].Clone()
                        self.mydict[gr]['histo'][cut][variable]['rmsDown'].SetDirectory(0)
                        self.mydict[gr]['histo'][cut][variable]['rmsDown'].SetName(rmsHistoName+"Down")
                        self.mydict[gr]['histo'][cut][variable]['rmsDown'].SetTitle(rmsHistoName+"Down")
                        Nbins=self.mydict[gr]['histo'][cut][variable]['rmsUp'].GetNbinsX()
                        break ##only for the first sample to get Nbins
                    #print Nbins
                    for ibin in range(0,Nbins+1):

                        y0=self.mydict[gr]['histo'][cut][variable]['rmsDown'].GetBinContent(ibin)
                        y0err=self.mydict[gr]['histo'][cut][variable]['rmsDown'].GetBinError(ibin)
                        ##sigma = sqrt(sum[ (yi-y0)**2])
                        SumOfDiff2=0
                        for sample in self.mydict[gr]['samples']: ##Make rms up/down
                            y=self.mydict[gr]['histo'][cut][variable][sample].GetBinContent(ibin)
                            yerr=self.mydict[gr]['histo'][cut][variable][sample].GetBinError(ibin)
                            SumOfDiff2+=(y-y0)**2
                        sigma=math.sqrt(SumOfDiff2)



                        self.mydict[gr]['histo'][cut][variable]['rmsUp'].SetBinContent(ibin,y0+sigma)
                        self.mydict[gr]['histo'][cut][variable]['rmsDown'].SetBinContent(ibin,y0-sigma)
                       


            #print self.mydict[gr]['histo']
        #print type(mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['DATA'])
if __name__ == '__main__':
    mydict={
        'gr1':{
            'cuts':['eleCH__BoostedggF__SR__METOver40__PtOverM04'],
            'variables':['MEKD_Bst_C_0.003_M900'],
            'FileName':'rootFile_2017_Boosted_SKIM10_HMVar10_MEKDOPT/hadd.root',
            'samples':['DATA']
            
        }
    }
    test=HistoParser(mydict)
    c=ROOT.TCanvas()
    test.mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['DATA'].Draw()
    test.mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['Sum'].Draw()
    c.SaveAs('test.png')
    

