import ROOT
import sys
import glob
#rf=sys.argv[1]
#
def Draw(rf):
    tfile=ROOT.TFile.Open(rf)
    BKG=[ 'DY', 'MultiBoson', 'Top','Wjets','QCD','WW','VH','qqWWqq','ggWW','ggH_hww','qqH_hww']

    yb=0
    for i,b in enumerate(BKG):
        if i==0:
            h=tfile.Get('histo_'+b).Clone()
        else:
            h.Add(tfile.Get('histo_'+b))
        yb+=tfile.Get('histo_'+b).Integral()

    hdata=tfile.Get('histo_Data')
    yd=tfile.Get('histo_Data').Integral()

    for i in range(1,h.GetNbinsX()+1):
        if h.GetBinContent(i)<=0:
            print "[NO Bkg Exp.]"
            print 'x->',h.GetBinLowEdge(i)
        print 'y->',h.GetBinContent(i)
    c=ROOT.TCanvas("c", "canvas", 800, 800)
    pad1=ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)
    pad1.SetGridx()
    pad1.Draw()
    pad1.cd()
    
    
    hdata.Draw()
    h.SetLineColor(2)
    h.Draw('same')
    
    hratio=hdata.Clone()
    hratio.Divide(h)
    c.cd()
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.2)
    pad2.SetGridx()
    pad2.Draw()
    pad2.cd()
    
    hratio.Draw()
    hratio.SetStats(0)
    hratio.SetTitle('')
    hratio.SetMaximum(2)
    hratio.SetMinimum(0)
    hratio.GetYaxis().SetLabelSize(0.1)
    hratio.GetXaxis().SetLabelSize(0.1)
    hratio.GetYaxis().SetNdivisions(505)







    pdfname='.root'.join(rf.split('.root')[:-1])
    pdfname+='.pdf'
    c.SaveAs(pdfname)
    tfile.Close()

    

    #print yb/yd
if __name__ == '__main__':
    search=sys.argv[1]
    rflist=glob.glob(search)
    for rf in rflist:
        Draw(rf)
