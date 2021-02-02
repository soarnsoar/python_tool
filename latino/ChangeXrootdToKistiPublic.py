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




    os.system(python_path_new,python_path)

