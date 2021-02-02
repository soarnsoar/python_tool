#root://cms-xrd-global.cern.ch
#root://xrootd-cms.infn.it
import os

def ChangeToKistiPublic(python_path):

    xrd_from='cms-xrdr.private.lo:2094'
    xrd_to='cms-xrdr.sdfarm.kr'

    f=open(python_path,'r')
    python_path_new=python_path+'_new'
    fnew=open(python_path_new,'w')
    lines=f.readlines()
    for line in lines:
        if xrd_from in line:
            line=line.replace(xrd_from,xrd_to)
        fnew.write(line)


    f.close()
    fnew.close()




    os.system('mv '+python_path+' '+python_path+'_old')
    os.system('mv '+python_path_new+' '+python_path)
    


ChangeToKistiPublic('mkShapes__2017__cms_scratch_jhchoi_FinalBinNum4_Resolved_HMFull_V13_RelW0.02_DeepAK8WP0p5_dMchi2Resolution_SR__ALL__ggH_hww1000_c10brn00.py')
