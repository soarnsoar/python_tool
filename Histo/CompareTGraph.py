import ROOT
import os
def CompareTGraph(graph_list,alias_list,xlabel,ylabel,xmin,xmax,ymin,ymax,savepath,setlogy=False):
    Ngr=len(graph_list)
    tcanvas = ROOT.TCanvas( 'tcanvas', 'comparison',1200,800)

    ##Set frame
    firstgr=graph_list[0]
    frame = ROOT.TH2F("frame","",firstgr.GetN(),xmin,xmax,100,ymin,ymax)
    frame.SetStats(0)
    frame.SetYTitle(ylabel)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetLabelSize(0.03)
    frame.SetXTitle(xlabel)
    frame.GetXaxis().SetTitleSize(0.035)
    frame.GetXaxis().SetLabelSize(0.03)
    frame.GetXaxis().SetTitleOffset(1.5)
    frame.Draw()
    ##Draw

    ##legend
    leg= ROOT.TLegend(0.5,0.75,0.95,0.94)
    leg.SetFillColor(0)
    leg.SetBorderSize(1)
    leg.SetTextFont(8)
    leg.SetTextSize(20)
    for idx in range(0,Ngr):
        graph_list[idx].Draw("l same")
        leg.AddEntry(graph_list[idx], alias_list[idx],"l")
    leg.Draw('same')
    dirpath='/'.join(savepath.replace('//','/').split('/')[:-1])
    os.system('mkdir -p '+dirpath)
    tcanvas.SetLogy(setlogy)
    tcanvas.SaveAs(savepath)

        
