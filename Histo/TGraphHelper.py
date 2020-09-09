import ROOT
def TGraph_Maker(xlist,ylist):
    N=len(xlist)
    tgr  = ROOT.TGraph(N)
    tgr.SetLineWidth(2)

    for idx in range(0,N):
        x=xlist[idx]
        y=ylist[idx]
        tgr.SetPoint(idx,x,y)

    return tgr


def TGraphAsymmErrors_Maker(xlist,ylist,xerrl_list,xerrh_list,yerrl_list,yerrh_list):

    N=len(xlist)
    tgr  = ROOT.TGraphAsymmErrors(N)
    tgr.SetLineWidth(2)

    for idx in range(0,N):
        x=xlist[idx]
        y=ylist[idx]

        xerrl=xerrl_list[idx]
        xerrh=xerrh_list[idx]

        yerrl=yerrl_list[idx]
        yerrh=yerrh_list[idx]
        
        #tgr_cls_exp_pm1.SetPointError(i, 0, 0, values[4][i]-values[3][i], values[5][i]-values[4][i])
        #tgr_cls_exp_pm2.SetPointError(i, 0, 0, values[4][i]-values[2][i], values[6][i]-values[4][i])


        #SetPointError (Int_t i, Double_t exl, Double_t exh, Double_t eyl, Double_t eyh)

        tgr.SetPoint(idx,x,y)
        tgr.SetPointError(idx,xerrl,xerrh,yerrl,yerrh)

    return tgr

def DrawAndSave2Axis(tgrlist1,tgrnamelist1,tgrlist2,tgrnamelist2,yaxisname1,yaxisname2,savelist): #[RESULTDIR+'/'+'Significance_and_eff_'+v+'.png',RESULTDIR+'/'+'Significance_and_eff_'+v+'.pdf'])                                                                                                                                                                            
    ## Double axis                                                                                                                                                                                          
    #https://root-forum.cern.ch/t/tmultigraph-draw-options/6760                                                                                                                                             
    canvas=ROOT.TCanvas("c","multigraphs on same pad",200,10,700,500)
    pad1=ROOT.TPad("pad","",0,0,1,1)
    #pad2=ROOT.TPad()                                                                                                                                                                                       
    pad1.Draw()
    pad1.cd()

    mg1=ROOT.TMultiGraph()
    for _tgr in tgrlist1:
        mg1.Add(_tgr)
        
    mg1.Draw("AL")
    mg1.GetHistogram().GetYaxis().SetTitle(yaxisname1)
    mg1.GetHistogram().GetYaxis().SetTitleSize(0.03)
    mg1.GetHistogram().GetYaxis().SetLabelSize(0.03)
    mg1.GetHistogram().GetYaxis().SetLabelColor(1)
    #canvas.cd()                                                                                                                                                                                            
    pad2=ROOT.TPad("overlay","",0,0,1,1)
    pad2.SetFrameFillStyle(0)
    pad2.SetFillStyle(4000)
    pad2.Draw()
    pad2.cd()
    mg2=ROOT.TMultiGraph()
    for _tgr in tgrlist2:
        mg2.Add(_tgr)
    mg2.Draw("AL")

    mg2.GetHistogram().GetXaxis().SetLabelSize(0)
    mg2.GetHistogram().GetYaxis().SetLabelSize(0)
    mg2.GetHistogram().GetXaxis().SetTickLength(0)
    mg2.GetHistogram().GetYaxis().SetTickLength(0)

    xlist=[]
    ylist=[]
    for _tgr in tgrlist1+tgrlist2:
        xlist+=list(_tgr.GetX())
        ylist+=list(_tgr.GetY())
    xmax=max(xlist)*1.1
    ymin=min(ylist)*0.1
    ymax=max(ylist)*1.1
    yaxis2=ROOT.TGaxis(xmax,ymin,xmax,ymax,ymin,ymax,510,"+L")
    yaxis2.SetTitle(yaxisname2)
    yaxis2.SetLabelColor(1)
    yaxis2.SetLabelSize(0.03)
    yaxis2.SetTitleOffset(0.8)
    yaxis2.SetTitleSize(0.03)
    yaxis2.Draw('sames')

    #BestLine=ROOT.TLine(score_best_significance,ymin,score_best_significance,ymax    ) #x1y1x2y2                                                                                                            
    #BestLine.SetLineColor(1)
    #BestLine.SetLineStyle(2)
    #BestLine.Draw('sames')
    #_leg=ROOT.TLegend(0.1,0.8,0.28,0.9)                                                                                                                                                                    
    _leg=ROOT.TLegend(0.1,0.9,0.28,1.0) #x1y1x2y2                                                                                                                                                           
    #_leg2=ROOT.TLegend(0.4,   0.9,  0.9,  1.0) #x1y1x2y2                                                                                                                                                    

    for idx in range(0,len(tgrlist1)):

        _leg.AddEntry(tgrlist1[idx],tgrnamelist1[idx])
        
    for idx in range(0,len(tgrlist2)):
        _leg.AddEntry(tgrlist2[idx],tgrnamelist2[idx])


    _leg.Draw()
    #_leg2.AddEntry(BestLine,'Significance from '+str(float('%.3g'%nom_significance))+' to '+str(float('%.3g'%best_significance))+ '@'+str(float('%.3g'%score_best_significance)))
    for save in savelist:
        canvas.SaveAs(save)
