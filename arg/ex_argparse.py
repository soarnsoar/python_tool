import argparse
parser = argparse.ArgumentParser(description='input argument')
parser.add_argument('-n', dest='name', default="NONAME", help="name")
parser.add_argument('-d', dest='directory', default="NODIR", help="directory")
parser.add_argument('-l', dest='islogx', action='store_true', default=False, help="set x axis to log scale")
args = parser.parse_args()

name=args.name
directory=args.directory
islogx=args.islogx


print 'name',name
print 'directory',directory
print 'islogx',islogx
