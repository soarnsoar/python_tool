import sys
import ROOT
def GetNEntiresOfEventsTree(path):
    myfile=ROOT.TFile.Open(path)
    N=0
    try:
        N=myfile.Get("Events").GetEntries()
    except AttributeError:
        N=-1
    myfile.Close()
    return N

if __name__ == '__main__':
    filepath = sys.argv[1]
    N=GetNEntiresOfEventsTree(filepath)
    print N
