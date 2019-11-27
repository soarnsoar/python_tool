import sys

INPUT=sys.argv[1]


f=open(INPUT,'r')
fnew=open(INPUT+'__new__','w')


lines=f.readlines()
for line in lines:
    line=line.replace('.root','.root\n')
    fnew.write(line)

f.close()
fnew.close()
