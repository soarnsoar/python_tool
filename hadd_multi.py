#!/usr/bin/env python

##For time calc
import timeit
start = timeit.default_timer()


import sys
import os
import glob
import time

ncore=int(sys.argv[1])
os.system('mkdir -p hadd_temp')
##--clean remnants
for i_group in range(ncore):
    mergedFileDone='_temp_'+str(i_group)+'.done'
    mergedFile='_temp_'+str(i_group)+'.root'
    mergedFileLog='_temp_'+str(i_group)+'.log'
    os.system('mv '+mergedFileDone+' '+'hadd_temp/')
    os.system('mv '+mergedFile+' '+'hadd_temp/')
    os.system('mv '+mergedFileLog+' '+'hadd_temp/')



ListFile=glob.glob('plots*.root')
print "#files=",len(ListFile)
filedic={}

for i_group in range(ncore):
    filedic[i_group]=[]


##---assign files to each group 
for i, f in enumerate(ListFile):
    filedic[i%ncore].append(f)



for i_group in range(ncore):
    ##--For each group
    sourceFiles=''
    for f in filedic[i_group]:
        sourceFiles+=' '+str(f)
    mergedFile='_temp_'+str(i_group)+'.root'
    mergedFileDone='_temp_'+str(i_group)+'.done'
    mergedFileLog='_temp_'+str(i_group)+'.log'
    os.system('(echo "'+sourceFiles+'" &> filelist_'+str(i_group)+'.log;hadd -f '+mergedFile+' '+sourceFiles+' &> '+mergedFileLog+' ;touch '+mergedFileDone+')&'  )



while True:
    AllDone=True
    for i_group in range(ncore):
        print "##Check",i_group,'th file'
        mergedFileDone='_temp_'+str(i_group)+'.done'
        if not os.path.isfile(mergedFileDone):
            AllDone=False
            print mergedFileDone,'is not done yet'
            break
    if AllDone: break
    print "sleep 15 sec"
    time.sleep(15)
    

##--hadd tempfiles to
print "Hadd next step"
tempFiles=''
for i_group in range(ncore):
    mergedFile='_temp_'+str(i_group)+'.root'
    tempFiles+=' '+mergedFile
os.system('hadd -f hadd.root '+tempFiles+'&> hadd.log')

##--remove
for i_group in range(ncore):
    mergedFileDone='_temp_'+str(i_group)+'.done'
    mergedFile='_temp_'+str(i_group)+'.root'
    mergedFileLog='_temp_'+str(i_group)+'.log'
    os.system('mv '+mergedFileDone+' '+'hadd_temp/')
    os.system('mv '+mergedFile+' '+'hadd_temp/')
    os.system('mv '+mergedFileLog+' '+'hadd_temp/')


stop = timeit.default_timer()
print('Time: ', stop - start) 
os.system('echo '+str(stop - start)+'&> Runtime.log') 
