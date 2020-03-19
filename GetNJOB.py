import tempfile
import os
USER=os.getenv('USER')

tf = tempfile.NamedTemporaryFile()
thisfile=tf.name
#print thisfile
os.system('condor_q '+USER+' > '+thisfile)
f=open(thisfile,'r')
Ntotal='0'
lines1=f.readlines()
for line in lines1:
    if 'Total for query:' in line:
        Ntotal=line.split('Total for query:')[-1].split()[0]

f.close()
#os.system('rm '+thisfile)
print Ntotal
