from OpenFileInPyroot import *






if __name__ == '__main__':
    INPUT=sys.argv[1]
    f=open(INPUT,'r')
    lines=f.readlines()
    for line in lines:


        
        print line,'->',OpenFileInPyroot(line)


    f.close()
