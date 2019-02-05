import argparse
parser = argparse.ArgumentParser()
####Set options###
parser.add_argument("--old", help="old phrase")
parser.add_argument("--new", help="new phrase")
parser.add_argument("--oldfile", help="old file")
parser.add_argument("--newfile", help="new file")

args = parser.parse_args()

if args.old:
    old = args.old
else:
    print "need --old argument"
    quit()
if args.new:
    new = args.new
else:
    print "need --new argument"
    quit()
if args.oldfile:
    oldfile= args.oldfile
else:
    print "need --oldfile argument"
    quit()
if args.newfile:
    newfile= args.newfile
else:
    print "need --newfile argument"
    quit()

######################

###Exe####
f = open(oldfile, 'r')
f_new = open(newfile,'w')
lines=f.readlines()
for line in lines:
    line=line.replace(old,new)
    f_new.write(line)


f_new.close()
f.close()
