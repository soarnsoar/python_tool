import glob
from OpenFileInPyroot import *

DIR="/xrootd/store/user/jhchoi/Latino/HWWNano/Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__Semilep2017__HMlnjjSelBWRew"

filelist=glob.glob(DIR+"/*.root")



list_fail=[]

for f in filelist:
  if not OpenFileInPyroot(f):
    #print OpenFileInPyroot(f)
    #print f
    list_fail.append(f)



print "-----FAIL-----"
for f in list_fail:
  print f
  
