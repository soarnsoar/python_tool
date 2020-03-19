import sys
import ROOT
def GetNEntiresOfEventsTree(path):
    myfile=ROOT.TFile.Open(path)
    N=myfile.Get("Events").GetEntries()
    myfile.Close()
    return N

if __name__ == '__main__':
    filepath = sys.argv[1]
    N=GetNEntiresOfEventsTree(filepath)
    print N
