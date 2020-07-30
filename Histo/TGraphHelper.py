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
