import os
import time

def LastModifiedTime(path):
    stat = os.stat(path)
    
    modtime= stat.st_mtime
    #modtime_form =time.ctime(stat.st_mtime)
    #mod_timestamp = datetime.datetime.fromtimestamp(path.getmtime(path))
    now=time.time()

    age=now-modtime
    return age

if __name__ == '__main__':
    a=LastModifiedTime('test')
    print a
