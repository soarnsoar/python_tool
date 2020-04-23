import ROOT
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
                    #self.mydict[gr]['histo'][cut][variable]['Sum']=
                    for sample in self.mydict[gr]['samples']:
                        htemp=f.Get(cut+'/'+variable+'/histo_'+sample)
                        #print "type(htemp)",type(htemp)
                        self.mydict[gr]['histo'][cut][variable][sample]=htemp.Clone()
                        self.mydict[gr]['histo'][cut][variable][sample].SetDirectory(0)
                        if idx==0:
                            self.mydict[gr]['histo'][cut][variable]['Sum']=htemp.Clone()
                            self.mydict[gr]['histo'][cut][variable]['Sum'].SetDirectory(0)
                        else:
                            self.mydict[gr]['histo'][cut][variable]['Sum'].Add(htemp)

                        #print "type(self.mydict[gr]['histo'][cut][variable][sample])",type(self.mydict[gr]['histo'][cut][variable][sample])
                        #print "gr=",gr,'cut=',cut,'variable=',variable,'sample=',sample
                        #print "print type(mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['DATA'])=",type(mydict['gr1']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['MEKD_Bst_C_0.003_M900']['DATA'])
                    
            f.Close()
            

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
    

