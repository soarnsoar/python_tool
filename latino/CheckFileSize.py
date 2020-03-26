import ROOT

#root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano//Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__HMSemilepSkimJH2017v6/nanoLatino_GluGluHToWWToLNuQQ_M1500__part0.root


myfile="root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano//Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__HMSemilepSkimJH2017v6/nanoLatino_GluGluHToWWToLNuQQ_M1500__part0.root"

f=ROOT.TFile.Open(myfile)
Size=f.GetSize()/1024/1024
print Size
