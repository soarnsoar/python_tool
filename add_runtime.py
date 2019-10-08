import sys
import os

INPUT_SCRIPT=sys.argv[1]
fr=open(INPUT_SCRIPT,'r')
lines=fr.readlines()
os.system("mv "+INPUT_SCRIPT+" "+INPUT_SCRIPT+"_old")


fnew=open(INPUT_SCRIPT,'w')
fnew.write('StartTime=$(date +%s)\n')

for line in lines:
    if 'proxy-watcher -remove' in line: continue
    fnew.write(line)


fnew.write('''EndTime=$(date +%s)
echo $EndTime
echo "runtime : $(($EndTime - $StartTime)) sec"
echo -e "JOBDIR:${PWD}\nargs=$@\nruntime=$(($EndTime - $StartTime))\nScriptName=$BASH_SOURCE" | /bin/mailx -s "FINISHED JOB @ $HOSTNAME" $USER@cern.ch
''')

os.system('chmod u+x '+INPUT_SCRIPT)
