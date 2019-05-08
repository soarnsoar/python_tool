import os
import commands

inputfile='Summer16_102X_nAODv4.py'

campaign='RunIISummer16NanoAODv4'


print "@@"+inputfile+"@@"

f=open(inputfile,'r')


lines=f.readlines()


Samples={}

commented_lines=[]

by_hand_list=[]


for line in lines:
    


    ###check unfinished samples###
    if "#Samples" in line:
        commented_lines.append(line)
        line=line.replace('#Samples','Samples')
        #getattr(foo,line)
        #print line
        #globals()['line']
        exec(line) ##define Samples dic 


f.close()



fnew=open(inputfile+"_new.py",'w')

for line in lines:

#print Samples

    if not "#Samples" in line:
        fnew.write(line)
        continue




    ##Check line
    for key in Samples:
        #Samples['WGJJ']
        if not "#Samples['"+key+"']" in line : continue

        ##the line corresponds to this key
        #print key
        old_datasetname=Samples[key]
        #print old_datasetname['nanoAOD']
        datasetname=old_datasetname['nanoAOD'].split('/')[1]
        #for typo
        if not old_datasetname['nanoAOD'].startswith('/'):
            datasetname=old_datasetname['nanoAOD'].split('/')[0]

        #print datasetname
    
        ##check das output 
        ##/GluGluHToWWTo2L2Nu_M125_13TeV_powheg_JHUgenv628_pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM
        search_phr=datasetname+"*/*"+campaign+"*/NANOAODSIM"
        #dasgoclient -query="dataset=/GGJets*/*Fall17*/MINI*"
        #print "####Checking-->>>"+datasetname
        dascheck='dasgoclient -query="dataset=/'+search_phr+'"'
        #print dascheck
        #a=os.system(dascheck).stdout
        #print str(a)
        #if str(a)!=str(0):
        #    print "-->"+a
        status, output = commands.getstatusoutput(dascheck)
        if not '/' in output:
            fnew.write(line)
            continue
                        
        nsample=len(output.split('\n'))
        if nsample==1:
            #print "##"+key+" has output nanoAODv4$$"
            #print output
            print key
            #print "length="+str(len(output.split('\n')))
            #Samples['WgStarLNuEE'] = {'nanoAOD' :'/WGstarToLNuEE_012Jets_13TeV-madgraph/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM'}
            towrite="Samples["+"'"+key+"'"+"] = {'nanoAOD' :'"+output+"']\n"
            fnew.write(towrite)
            ##in original file


        elif nsample>1:
            #print "!!!You should choose one of the sample and add it to new sample list python by hand"
            #print "##"+key
            by_hand_list.append("##"+key)
            #print output
            for output_i in output.split('\n'):
                towrite="Samples['"+"'"+key+"'"+"'] = {'nanoAOD' :'"+output_i+"']"
                by_hand_list.append(towrite)
                #print towrite
            fnew.write(line)

                        



fnew.close()


print "@@Write one of the samples for each process@@"
for byhand in by_hand_list:
    print byhand
