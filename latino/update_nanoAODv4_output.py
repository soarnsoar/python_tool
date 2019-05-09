import os
import commands




##---Which list to check---##
#inputfile='Summer16_102X_nAODv4.py'
inputfile='fall17_102X_nAODv4.py'
#inputfile='Autumn18_102X_nAODv4_v16.py'



##---campaign string in DAS datasetname
##campaign=RunIISummer16NanoAODv4
campaign='RunIIFall17NanoAODv4'
#campaign='RunIIAutumn18NanoAODv4'


print "@@"+inputfile+"@@"

f=open(inputfile,'r')
lines=f.readlines()


##updated sample list(dic) 
Samples={}

##line in nAODv4 list python commented out. 
commented_lines=[]
##For ambigious case.
by_hand_list=[]

##--Collect commented lines--##
for line in lines:
    line_nospace=line.replace(" ","")
    #print line_nospace
    ###check unfinished samples###
    if "#Samples" in line_nospace:
        
        #print "+++commented"
        commented_lines.append(line)
        #line=line.replace('#','')
        ##---find 'samples' definition part of this line ---##

        for part in line_nospace.split("#"): 
            if part.startswith('Samples'):
                exec(part) ##define Samples dic 
            else : continue

f.close()
#print "@@key list@@"
#for key in Samples:
#    print key

fnew=open(inputfile+"_new.py",'w') ## new file for updated list -> check commented samples and fill datasetname if production is completed.
for line in lines:
    line_nospace=line.replace(" ","")
    ##Already has datasetname##
    if not "#Samples" in line_nospace:
        fnew.write(line)
        continue
    ###Private samples -> NOT in DAS###
    if 'private' in line.lower():
        fnew.write(line)
        continue
    if 'srmPrefix' in line:
        fnew.write(line)
        continue


    ##scan all unfinished sample and check whetehr this line corresponds to the sample 
    for key in Samples:
        if len(key.replace(' ',''))==0: continue
        if (not "#Samples['"+key+"']" in line_nospace) and (not '#Samples["'+key+'"]' in line_nospace) : continue
        full_datasetname=Samples[key]
        #print full_datasetname['nanoAOD']
        datasetname=key
        try:
            datasetname=full_datasetname['nanoAOD'].split('/')[1]
        except:
            print"!!No DAS datasetname in this sample="+key
        ##check das output
        search_phr=datasetname+"*/*"+campaign+"*/NANOAODSIM"
        #For example : 
        #dasgoclient -query="dataset=/GGJets*/*Fall17*/MINI*"
        #print "####Checking-->>>"+datasetname
        dascheck='dasgoclient -query="dataset=/'+search_phr+'"'
        #print dascheck
        #--get das output list
        status, output = commands.getstatusoutput(dascheck)
        if not '/' in output: ## if no output -> production is not finished yet
            fnew.write(line)
            continue
                        
        nsample=len(output.split('\n'))### the number of sample
        if nsample==1: ## only one corresponding sample
            print key+" updated :)"
            #Format#example#
            #Samples['WgStarLNuEE'] = {'nanoAOD' :'/WGstarToLNuEE_012Jets_13TeV-madgraph/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM'}
            towrite="Samples['"+key+"'] = {'nanoAOD' :'"+output+"'}\n"
            fnew.write(towrite)



        elif nsample>1:
            #print "!!!You should choose one of the sample and add it to new sample list python by hand"
            #print "##"+key
            by_hand_list.append("##"+key+" is updated##")
            #print output
            for output_i in output.split('\n'):
                towrite="Samples['"+key+"'] = {'nanoAOD' :'"+output_i+"'}"
                by_hand_list.append(towrite)
                #print towrite
            fnew.write(line)

                        



fnew.close()


print "@@Write one of the samples for each process@@"
for byhand in by_hand_list:
    print byhand
