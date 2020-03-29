#/dev/mapper/rootvg-cms_condor                                                                                                      212G   31G  171G  16% /cms_condor

import os


def GetCondorSpace():

    os.system('df > df.txt')
    f=open('df.txt','r')
    lines=f.readlines()
    
    space=''
    
    for line in lines:
        if '/cms_condor' in line:
            #print line
            space = float(line.split()[3])/1024./1024.
            
    f.close()
    #print space
    return space
if __name__ == '__main__':
    a=GetCondorSpace()
    print a

