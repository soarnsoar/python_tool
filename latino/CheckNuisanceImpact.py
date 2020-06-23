
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-f", dest='histofile')
parser.add_argument("-p", dest='process')
parser.add_argument("-c", dest='cutname')
parser.add_argument("-v", dest='varname')
parser.add_argument("-n", dest='nuisance')
#parser.add_argument("-n", dest='shapename')                                                                                                                                      
args=parser.parse_args()

histofile=args.histofile
process=args.process
cutname=args.cutname
varname=args.varname
nuisance=args.nuisance

import ROOT


myfile=ROOT.TFile.Open(histofile)
path=cutname+'/'+varname+'/'+'histo_'+process
print path
myshape_nom=myfile.Get(path)
myshape_up=myfile.Get(path+'_'+nuisance+'Up')
myshape_down=myfile.Get(path+'_'+nuisance+'Down')

nom=myshape_nom.Integral()
up=myshape_up.Integral()
down=myshape_down.Integral()

myfile.Close()

#eleCH__BoostedGGF__SR__METOver40__PtOverM04___/Event/histo_

myerr= (abs(nom-up)+abs(nom-down))/2/nom
print nuisance,'->',myerr
