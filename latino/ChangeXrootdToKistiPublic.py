#root://cms-xrd-global.cern.ch
#root://xrootd-cms.infn.it
import os

def ChangeToInfn(python_path):

    xrd_from='root://cms-xrd-global.cern.ch'
    xrd_to='root://xrootd-cms.infn.it'

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

