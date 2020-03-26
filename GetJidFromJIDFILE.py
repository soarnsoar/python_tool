def GetJidFromJIDFILE(jidpath):
    #1 job(s) submitted to cluster 3652292.
    f= open(jidpath,'r')

    lines=f.readlines()
    jid=""
    for line in lines:
        if "job(s) submitted to cluster" in line:
            jid=line.split('submitted to cluster')[1].replace('.','').replace('\n','').replace(' ','')
          
  
    f.close()

    #print jid
    return jid

#/cms/ldap_home/jhchoi/HWW_Analysis/slc7/For_Productionv6/jhchoi_workdir/jobs/NanoGardening__Run2017_102X_nAODv5_Full2017v6__HMSemilepFake2017/SingleMuon_Run2017C-Nano1June2019-v1____DATAl1loose2017v6__HMSemilepSkimJHv6_7_data/NanoGardening__Run2017_102X_nAODv5_Full2017v6__HMSemilepFake2017__SingleMuon_Run2017C-Nano1June2019-v1__part68____DATAl1loose2017v6__HMSemilepSkimJHv6_7_data.jid_1


if __name__ == '__main__':
    path="/cms/ldap_home/jhchoi/HWW_Analysis/slc7/For_Productionv6/jhchoi_workdir/jobs/NanoGardening__Run2017_102X_nAODv5_Full2017v6__HMSemilepFake2017/SingleMuon_Run2017C-Nano1June2019-v1____DATAl1loose2017v6__HMSemilepSkimJHv6_7_data/NanoGardening__Run2017_102X_nAODv5_Full2017v6__HMSemilepFake2017__SingleMuon_Run2017C-Nano1June2019-v1__part68____DATAl1loose2017v6__HMSemilepSkimJHv6_7_data.jid_1"
    GetJidFromJIDFILE(path)
