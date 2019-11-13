import ROOT
import sys

INPUT=sys.argv[1]
print "INPUT=",INPUT

ROOT.TFile.Open(INPUT)
