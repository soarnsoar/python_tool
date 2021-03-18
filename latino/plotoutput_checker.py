import glob
import ROOT
def plotoutput_chekcer(filename,procname):
    
    filein=ROOT.TFile.Open(filename)
    cutlist=filein.GetListOfKeys()
    for cutkey in cutlist:
        cut=cutkey.GetName()
        filein.cd(cut)
        variablelist=ROOT.gDirectory.GetListOfKeys()
        for variablekey in variablelist:
            variable=variablekey.GetName()
            try:
                hcentral=filein.Get(cut+'/'+variable+'/histo_'+procname)
                hcentral.Integral()
            except:
                print '======',filename,procname,"is zombie========="
                print cut+'/'+variable+'/histo_'+proc
                filein.Close()
                return False
            
    filein.Close()
    return True

if __name__ == '__main__':
    import sys

    dirname=sys.argv[1]
    prefix='Combine_ALL_'
    filelist=glob.glob(dirname+'/plot*.root')
    
    zombielog=open('zombie__'+dirname.replace('/','_')+'.txt','w')
    #_ALL_TT.97.root
    
    for filename in filelist:
        print filename
        procname=filename.split(prefix)[1].split('.')[0]
        isfine=plotoutput_chekcer(filename,procname)
        if not isfine:
            zombielog.append(filename)

    zombielog.close()
