from GetNEntiresOfEventsTree import *
import glob
import time

##--Setup--##
DoTest=False



NominalDir="/xrootd_user/jhchoi/xrootd/Latino/HWWNano/Fall2017_102X_nAODv5_Full2017v6/MCl1loose2017v6__MCCorr2017v6__HMSemilepSkimJH2017v6_5/"

SysStep='ElepTup'
#####----####

##--defined
def ConvertToXROOTDpath(filepath):
    if "root://cms-xrdr.private.lo:2094" in filepath:
        return filepath
    if "/xrootd_user/jhchoi/xrootd/Latino/HWWNano/" in filepath:
        filepath=filepath.replace('//','/').replace('/xrootd_user/jhchoi/xrootd/Latino/HWWNano/','root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano/')
    elif "/xrootd/store/user/jhchoi/Latino/HWWNano/" in filepath:
        filepath=filepath.replace('//','/').replace('/xrootd/store/user/jhchoi/Latino/HWWNano/','root://cms-xrdr.private.lo:2094///xrd/store/user/jhchoi/Latino/HWWNano/')
    return filepath


##--End of defined

SysDir=NominalDir.rstrip('/')+'__'+SysStep+'/'


SysFileList=glob.glob(SysDir+'*.root')

fZombieList=open('zombie_'+SysStep+'.txt','w')
fNotMatchList=open('NotMatch_'+SysStep+'.txt','w')


idx=0
for sysfile in SysFileList:
    print idx,'/',len(SysFileList)
    fileroot=sysfile.split('/')[-1]

    NominalPath=NominalDir+'/'+fileroot
    NominalPath=ConvertToXROOTDpath(NominalPath)

    SysPath=SysDir+'/'+fileroot
    SysPath=ConvertToXROOTDpath(SysPath)

    Nnomi=GetNEntiresOfEventsTree(NominalPath)
    Nsys=GetNEntiresOfEventsTree(SysPath)
    if not bool(Nsys):
        print "--thisFile can have a problem or is a zombie--"
        print SysDir+'/'+fileroot
        fZombieList.write(SysDir+'/'+fileroot+'\n')
    else:

        if Nnomi!=Nsys:
            print "[NEEED RESUB], Entries not matched: (Nnomi,Nsys) =",Nnomi,Nsys
            print SysDir+'/'+fileroot
            fNotMatchList.write(SysDir+'/'+fileroot)+'\n'
    time.sleep(0.7)


    ##ForTest
    if DoTest:
        print fileroot
        print "Nnomi=",Nnomi
        print "Nsys=",Nsys
        break ##For Test
    idx+=1
fZombieList.close()
fNotMatchList.close()
