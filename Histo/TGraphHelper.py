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
