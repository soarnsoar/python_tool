import os
def AddRequestCPU(jds,cpu):
    ToAdd='request_cpus = '+str(int(cpu))+' \n'
    f=open(jds,'r')
    fnew=open(jds+'_new','w')

    lines=f.readlines()
    for line in lines:
        if ToAdd in line:continue ##already added
        if 'queue' in line:
            
            if not ToAdd in line:  fnew.write(ToAdd)
        fnew.write(line)

    f.close()
    fnew.close()
    os.system('mv '+jds+'_new'+' '+jds)
    #os.system('rm '+jds+'_new')
if __name__ == '__main__':
    AddRequestCPU("NanoGardening__Fall2017_102X_nAODv5_Full2017v6__METdo__WJetsToLNu-1J__part13____MCl1loose2017v6__MCCorr2017v6__HMSemilepSkimJH2017v6_5.jds","1000")
