import glob


from OpenFileInPyroot import OpenFileInPyroot

BASEDIR='/xrootd_user/jhchoi/xrootd/Latino/HWWNano/'
#Production='Fall2017_102X_nAODv4_Full2017v5'
#Production='Summer16_102X_nAODv4_Full2016v5'
Production='Autumn18_102X_nAODv5_Full2018v5'
#Step='/MCl1loose2017v5__MCCorr2017v5*'
Step='/MCl1loose2018v5__MCCorr2018v5*'

THISDIR=BASEDIR+'/'+Production+'/'+Step+'/'

files=glob.glob(THISDIR+'/*.root')

ZOMBIE_LIST=[]
for f in files:

    IS_NOT_ZOMBIE=OpenFileInPyroot(f)
    #IS_NOT_ZOMBIE=False
    if not IS_NOT_ZOMBIE:
        ZOMBIE_LIST.append(f)


TASK_NAME=Production.replace('/','')+'_'+Step.replace('/','').replace('*','incl')

txt=open('log_'+TASK_NAME+'.txt','w')

print "---zombie--"
print len(ZOMBIE_LIST),'/',len(files)
for a in ZOMBIE_LIST:
    print a
    txt.write(a+'\n')

txt.close()

