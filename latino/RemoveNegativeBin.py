import datetime
begin_time = datetime.datetime.now()





from array import array
import ROOT
ROOT.gROOT.SetBatch(True)
import sys
sys.path.insert(0, "python_tool/latino/")
import math
from HistoParser import HistoParser

import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-f", dest='histofile')


args=parser.parse_args()


histofile=args.histofile
import os
os.system('cp '+histofile+' '+histofile+'_backup')
#dict_htemp={}
f=ROOT.TFile.Open(histofile,'UPDATE')

for cut in ROOT.gDirectory.GetListOfKeys():
   if cut.IsFolder:
      f.cd(cut.GetName())
      for variable in ROOT.gDirectory.GetListOfKeys():
         if variable.IsFolder:
            f.cd(cut.GetName()+'/'+variable.GetName())
            for shape in ROOT.gDirectory.GetListOfKeys():
               shapepath=cut.GetName()+'/'+variable.GetName()+'/'+shape.GetName()
               if f.Get(shapepath):
                  print shapepath
                  thish = f.Get(shapepath)
                  htemp=thish.Clone()
                  Nbins= thish.GetNbinsX()
                  for ibin in range(0,Nbins+1):
                     y=thish.GetBinContent(ibin)
                     yerr=thish.GetBinError(ibin)
                     if y <0:
                        htemp.SetBinContent(ibin,0)
                  ##end of ibin
                  ROOT.gDirectory.WriteObject(htemp,shapepath)


      
#ROOT.gDirectory.WriteObject(,'')
f.Close()
print(datetime.datetime.now() - begin_time)
