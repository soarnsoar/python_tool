import os
import commands



####### Setting #########
##---Which list to check---##
inputfile='Summer16_102X_nAODv4.py'
#inputfile='fall17_102X_nAODv4.py'
#inputfile='Autumn18_102X_nAODv4_v16.py'


##---campaign string in DAS datasetname
campaign='RunIISummer16NanoAODv4'
#campaign='RunIIFall17NanoAODv4'
#campaign='RunIIAutumn18NanoAODv4'
#######End of Setting###########


print "@@"+inputfile+"@@"

f=open(inputfile,'r')

exec(f)

lines=f.readlines()


##updated sample list(dic) 
#Samples={}

##line in nAODv4 list python commented out. 
commented_lines=[]
##For ambigious case.
#by_hand_list=[]

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
#print Samples
#print "@@key list@@"
#for key in Samples:
#    print key



for key in Samples:
    if len(key.replace(' ',''))==0:
        continue
    if 'jhugen' in key.lower():
        print ""
        print key
        ##jhugen is in latino alias
        full_datasetname=Samples[key]
        if len(full_datasetname['nanoAOD'].split('/'))<2: continue
        datasetname=full_datasetname['nanoAOD'].split('/')[1]
        #print ""
        #print datasetname
        vjhugen_das=''

        for part in datasetname.split('_'):
            if 'jhugen' in part.lower() :
                #print '->datasetname in DAS='+part                                                                                                                          
                vjhugen_das=part.lower().replace('jhugen','').replace('v','')
        ##Check vJHUHen in latino sample alias##                                                                                                                             
        vjhugen_alias=''
        for part in key.split('_'):
            if 'jhugen' in part.lower() :
                #print '->datasetname in latino alias='+part                                                                                                                     
                vjhugen_alias=part.lower().replace('jhugen','').replace('v','')
                ##if the two versions are not matched##                                                                                                                              
        if vjhugen_das!=vjhugen_alias :
            print "!!!!!!!!!Version is not matched. Alias should be fixed!!!.."+vjhugen_alias+"->"+vjhugen_das
        else:
            print "->OK"
