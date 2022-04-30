import json
import sys
import os
import ROOT
from numpy import array

class RebinningTool:
    def __init__(self,datacardpath,jsonpath):
        self.datacardpath=datacardpath
        self.jsonpath=jsonpath
        self.dict_H={}
    def GetHistoPath(self):
        f=open(self.datacardpath,'r')
        lines=f.readlines()
        for line in lines:
            line=line.split()
            if len(line)>1:
                if line[0]=='shapes' and line[1]=='*':
                    binname=line[2]
                    hpath=line[3]
                    self.dict_H[binname]=hpath
        #print self.dict_H
        f.close()
        self.GetMainDatacardDir()
    def GetMainDatacardDir(self):
        #self.datacardpath
        self.maindir='/'.join(self.datacardpath.split('/')[:-1])
        self.maindir+'/'
    def ParseJson(self):
        self.dict_ToRebin={}
        with open(self.jsonpath, "r") as st_json:
            self.data = json.load(st_json)
        if 'emptyBkgBin' in self.data:
            print self.data['emptyBkgBin']
            self.dict_ToRebin=self.data['emptyBkgBin']
        #print self.dict_ToRebin
    def doRebin(self):
        for binname in self.dict_ToRebin: 
            fpath= self.maindir+self.dict_H[binname]
            if os.path.isfile(fpath+'_backup') :
                print 'Re Use backup'
                os.system('cp '+fpath+'_backup '+fpath)
            else:
                os.system('cp '+fpath+' '+fpath+'_backup')
            binToRebin=self.dict_ToRebin[binname]
            print binToRebin
            self._Rebin(fpath,binToRebin)

    def restore_input(self):
        for binname in self.dict_ToRebin: 
            fpath= self.maindir+self.dict_H[binname]
            os.system('cp '+fpath+'_backup '+fpath)
            


    def _Rebin(self,fpath,binToRebin):
        tfile=ROOT.TFile.Open(fpath,'Update')
        ##---1)Read HistoList
        self.histokeylist=tfile.GetListOfKeys()
        self.histolist=[]
        for histokey in self.histokeylist:
            histoname=histokey.GetName()
            self.histolist.append(tfile.Get(histoname))
        ##---2)Get Old binning
        oldbinning=[]
        nbins=self.histolist[0].GetNbinsX()
        print 'nbins=',nbins
        for i in range(1,nbins+2):
            x=self.histolist[0].GetBinLowEdge(i)
            oldbinning.append(x)

        ##---3)Get New binning
        xToRemove=[]
        for i in binToRebin:
            x=self.histolist[0].GetBinLowEdge(i+1) ##Right Edge
            xToRemove.append(x)
        newbinning=[]
        for b in oldbinning:
            if b in xToRemove : continue
            newbinning.append(float(b))

        if not oldbinning[-1] in newbinning: ##if total range is changed -> recover
            newbinning.pop()
            newbinning.append(oldbinning[-1])
        print '[oldbinning]',oldbinning
        print '[newbinning]',newbinning
        ##---4)Do Rebinning
        for h in self.histolist:
            integral_before=h.Integral()
            h=h.Rebin(len(newbinning)-1, h.GetName(),array(newbinning))
            integral_after=h.Integral()
            if integral_before!=integral_after and (integral_after-integral_before)/integral_after > 0.00001:
                print '[!!!!Integral NOT Conserved]',h.GetName(),integral_before,integral_after,(integral_after-integral_before)
        ##---5)Write
        tfile.Write()
        
        tfile.Close()        
    def ReValidate(self):
        self.newjsonpath=self.jsonpath+'_new.json'
        os.system('ValidateDatacards.py '+self.datacardpath+' --jsonFile '+self.newjsonpath)
        newdata={}
        with open(self.newjsonpath, "r") as st_json:
            newdata = json.load(st_json)
        #print newdata
        if 'emptyBkgBin' in newdata:
            self.restore_input()
            return False
        else:
            return True

if __name__ == '__main__':
    #d='../../Datacards_2016/combine_hwwlnuqq_Resolved_900_2016__CUT_nocut.txt'
    #j='../../Datacards_2016/validation.json'
    d=sys.argv[1]
    j=sys.argv[2]
    rebin=RebinningTool(d,j)
    rebin.GetHistoPath()
    rebin.ParseJson()
    rebin.doRebin()
    if not rebin.ReValidate():
        print 1/0
