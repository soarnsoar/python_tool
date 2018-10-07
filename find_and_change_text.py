filename='test.txt'
newfilename='newfile.txt'
old = 'aaa'
new = 'bbb'
f = open(filename, 'r')
newfile = open(newfilename,'w')
lines=f.readlines()
for line in lines:
    print line
#    if 'aaa' in line:
    line=line.replace(old,new)
    print line
    newfile.write(line)


newfile.close()
f.close()
