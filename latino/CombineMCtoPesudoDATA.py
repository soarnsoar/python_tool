
##---
class dummy():##dummy
   def __init__(self):
       self.scriptname=''
       self.variablesFile=''
       self.cutsFile=''
opt=dummy()
##---



from array import array
import ROOT
ROOT.gROOT.SetBatch(True)
import sys
sys.path.insert(0, "python_tool/latino/")
import math
from HistoParser import HistoParser

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-c", dest='conf')
parser.add_argument("-f", dest='histofile')
args=parser.parse_args()


#conf='configuration_Boosted.py'
#histofile='hadd.root'
conf=args.conf
histofile=args.histofile

##--declare--##
variables={}
cuts={}

##---Read configuration---##
handle=open(conf,'r')
exec(handle)
handle.close()
##--Read variablesFile--##
handle=open(variablesFile,'r')
exec(handle)
handle.close()
##--Read cutFile--##
handle=open(cutsFile,'r')
exec(handle)
handle.close()
##---END--##


this_dict={
   'bkg':{
      'cuts':sorted(cuts),
      #'variables':['MEKD_Bst_C_0.003_M900'],
      'variables':sorted(variables),
      'FileName':histofile,
      'samples':['DY','QCD_EM','QCD_bcToE','WW','WWW','WWZ','WZ','WZZ','ZZZ','ZZ','Wjets0j','Wjets1j','Wjets2j','WpWmJJ_EWK_QCD_noHiggs','top',]        
   },
}
histoana=HistoParser(this_dict)
#mysum=histoana.mydict['bkg']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['Event']['Sum'].Integral()


##---Set staterr---##
for cut in sorted(cuts):
   for var in sorted(variables):
      Nbins=histoana.mydict['bkg']['histo'][cut][var]['Sum'].GetNbinsX()
      for i in range(0,Nbins+1):
         
         entry=histoana.mydict['bkg']['histo'][cut][var]['Sum'].GetBinContent(i)
         if entry<0:entry=0
         
         error=math.sqrt(entry)
         if error==0:
            error=math.sqrt(3)
         histoana.mydict['bkg']['histo'][cut][var]['Sum'].SetBinContent(i,entry)
         histoana.mydict['bkg']['histo'][cut][var]['Sum'].SetBinError(i,error)
      


##--End of Setbinerror--##


f=ROOT.TFile.Open(histofile,'UPDATE')
#f.ls()
#idx=0
for cut in sorted(cuts):
   #f.cd(cut)
   for var in sorted(variables):      
      #if idx==0:
      #   print "init dir"
      #   ROOT.gDirectory.pwd()
      #   print 'go to',cut,var
      #   f.cd(cut+'/'+var)
      #   print "--current dir--"
      #   ROOT.gDirectory.pwd()
      #   ROOT.gDirectory.WriteObject(histoana.mydict['bkg']['histo'][cut][var]['Sum'],'histo_PeudoData')
      #   ROOT.gDirectory.ls()

      f.cd(cut+'/'+var)
      #idx+=1
      #initdir=ROOT.gDirectory.CurrentDirectory()

      ROOT.gDirectory.WriteObject(histoana.mydict['bkg']['histo'][cut][var]['Sum'],'histo_PeudoData')
      #f.cd(initdir)
      #f.cd('../')
   #f.cd('../')
f.Close()
