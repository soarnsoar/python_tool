import datetime
begin_time = datetime.datetime.now()

##---
class dummy():##dummy
   def __init__(self):
       self.scriptname=''
       self.variablesFile=''
       self.cutsFile=''
       self.nuisancesFile=''
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
parser.add_argument("-s", dest='samplelist')
#parser.add_argument("-n", dest='shapename')
args=parser.parse_args()


#conf='configuration_Boosted.py'
#histofile='hadd.root'
conf=args.conf
histofile=args.histofile
samplelist=args.samplelist.split(',')

##--declare--##
variables={}
cuts={}

##---Read configuration---##
handle=open(conf,'r')
exec(handle)
handle.close()
opt.variablesFile=variablesFile
opt.cutsFile=cutsFile
opt.nuisancesFile=nuisancesFile
##--Read variablesFile--##
handle=open(variablesFile,'r')
exec(handle)
handle.close()
##--Read cutFile--##
handle=open(cutsFile,'r')
exec(handle)
handle.close()
##--Read samples--##
samples={}
handle=open(samplesFile,'r')
exec(handle)
handle.close()
##--Read nuisance--##
nuisances={}
handle=open(nuisancesFile,'r')
exec(handle)
handle.close()


##---END--##
print "[CombineMultiV.py] len(cuts)=",len(cuts)

#nuisances
#ListVar=['']
#for nui in nuisances:
##--nominal

this_dict={
   'nom':{
      'cuts':sorted(cuts),
      #'variables':['MEKD_Bst_C_0.003_M900'],                                                                                                                               
      'variables':sorted(variables),
      #'variables':[],                                                                                                                                                      
      'FileName':histofile,
      'samples':samplelist,
      #'samples':['WW'+nuis,'WWW'+nuis,'WWZ'+nuis,'WZ'+nuis,'WZZ'+nuis,'ZZZ'+nuis,'ZZ'+nuis]                                                                                
      #'samples':samplelist,
   }
}
histoana=HistoParser(this_dict)
for cut in sorted(cuts):
   for var in sorted(variables):
      for gr in this_dict:
         Nbins=histoana.mydict[gr]['histo'][cut][var]['Sum'].GetNbinsX()
         for i in range(0,Nbins+1):
            
            entry=histoana.mydict[gr]['histo'][cut][var]['Sum'].GetBinContent(i)
            if entry<0:entry=0
            
            error=math.sqrt(entry)
            if error==0:
               error=math.sqrt(3)
               histoana.mydict[gr]['histo'][cut][var]['Sum'].SetBinContent(i,entry)
               histoana.mydict[gr]['histo'][cut][var]['Sum'].SetBinError(i,error)

f=ROOT.TFile.Open(histofile,'UPDATE')

for cut in sorted(cuts):
   print cut
   #f.cd(cut)                                                                                                                                                               
   for var in sorted(variables):
      #if idx==0:                                                                                                                                                           
      #   print "init dir"                                                                                                                                                  
      #   ROOT.gDirectory.pwd()                                                                                                                                             
      #   print 'go to',cut,var                                                                                                                                             
      #   f.cd(cut+'/'+var)                                                                                                                                                 
      #   print "--current dir--"                                                                                                                                           
      #   ROOT.gDirectory.pwd()                                                                                                                                             
      #   ROOT.gDirectory.WriteObject(histoana.mydict['multiv']['histo'][cut][var]['Sum'],'histo_PseudoData')                                                               
      #   ROOT.gDirectory.ls()
      f.cd(cut+'/'+var)
      #idx+=1                                                                                                                                                               
      #initdir=ROOT.gDirectory.CurrentDirectory()                                                                                                                           
      #print "Shape histo_MultiV created"                                                                                                                                   
      for gr in histoana.mydict:
         histoana.mydict[gr]['histo'][cut][var]['Sum'].SetTitle('histo_MultiV')
         histoana.mydict[gr]['histo'][cut][var]['Sum'].SetName('histo_MultiV')
         ROOT.gDirectory.WriteObject(histoana.mydict[gr]['histo'][cut][var]['Sum'],'histo_MultiV')
         #f.cd(initdir)                                                                                                                                                     
         #f.cd('../')                                                                                                                                                       
         #f.cd('../')                                                                                                                                                       
f.Close()


##--nuisance
for nuis in nuisances:
   if nuisances[nuis]['type']=='shape':
      #:ListVar+=['_'+nuisances[nui]['name']+'Up', '_'+nuisances[nui]['name']+'Down']
      this_dict={
         'Up':{
            'cuts':sorted(cuts),
            #'variables':['MEKD_Bst_C_0.003_M900'],
            'variables':sorted(variables),
            #'variables':[],
            'FileName':histofile,
            'samples':[],
            #'samples':['WW'+nuis,'WWW'+nuis,'WWZ'+nuis,'WZ'+nuis,'WZZ'+nuis,'ZZZ'+nuis,'ZZ'+nuis]        
            #'samples':samplelist,
         },
         'Down':{
            'cuts':sorted(cuts),
            #'variables':['MEKD_Bst_C_0.003_M900'],
            'variables':sorted(variables),
            #'variables':[],
            'FileName':histofile,
            'samples':[],
            #'samples':['WW'+nuis,'WWW'+nuis,'WWZ'+nuis,'WZ'+nuis,'WZZ'+nuis,'ZZZ'+nuis,'ZZ'+nuis]        
            #'samples':samplelist,
         },
      }
      
      ###--Select samples
      #nuisances[nuis]['samples']
      for s in samplelist:
         if s in nuisances[nuis]['samples']:
            this_dict['Up']['samples'].append(s+"_"+nuisances[nuis]['name']+'Up')
            this_dict['Down']['samples'].append(s+"_"+nuisances[nuis]['name']+'Down')
         else:
            this_dict['Up']['samples'].append(s)
            this_dict['Down']['samples'].append(s)

      histoana=HistoParser(this_dict)
      #mysum=histoana.mydict['bkg']['histo']['eleCH__BoostedggF__SR__METOver40__PtOverM04']['Event']['Sum'].Integral()


      ##---Set staterr---##
      for cut in sorted(cuts):
         for var in sorted(variables):
            for gr in this_dict:
               Nbins=histoana.mydict[gr]['histo'][cut][var]['Sum'].GetNbinsX()
               for i in range(0,Nbins+1):
            
                  entry=histoana.mydict[gr]['histo'][cut][var]['Sum'].GetBinContent(i)
                  if entry<0:entry=0
               
                  error=math.sqrt(entry)
                  if error==0:
                     error=math.sqrt(3)
                     histoana.mydict[gr]['histo'][cut][var]['Sum'].SetBinContent(i,entry)
                     histoana.mydict[gr]['histo'][cut][var]['Sum'].SetBinError(i,error)
                  


      ##--End of Setbinerror--##

      
      f=ROOT.TFile.Open(histofile,'UPDATE')
      #f.ls()
      #idx=0
      for cut in sorted(cuts):
         print cut
         #f.cd(cut)
         for var in sorted(variables):      
            #if idx==0:
            #   print "init dir"
            #   ROOT.gDirectory.pwd()
            #   print 'go to',cut,var
            #   f.cd(cut+'/'+var)
            #   print "--current dir--"
            #   ROOT.gDirectory.pwd()
            #   ROOT.gDirectory.WriteObject(histoana.mydict['multiv']['histo'][cut][var]['Sum'],'histo_PseudoData')
            #   ROOT.gDirectory.ls()
            
            f.cd(cut+'/'+var)
            #idx+=1
            #initdir=ROOT.gDirectory.CurrentDirectory()
            #print "Shape histo_MultiV created"
            for gr in histoana.mydict:
               histoana.mydict[gr]['histo'][cut][var]['Sum'].SetTitle('histo_MultiV_'+nuis)
               histoana.mydict[gr]['histo'][cut][var]['Sum'].SetName('histo_MultiV_'+nuis)
               ROOT.gDirectory.WriteObject(histoana.mydict[gr]['histo'][cut][var]['Sum'],'histo_MultiV'+"_"+nuisances[nuis]['name']+gr)##gr=Up,Down
               #f.cd(initdir)
               #f.cd('../')
               #f.cd('../')
      f.Close()
print(datetime.datetime.now() - begin_time)
