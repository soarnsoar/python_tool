import glob, sys

def GetTimePerEventList(outfile):
    f=open(outfile,'r')
    lines=f.readlines()

    List_TPE=[] ##TimePerEvent

    for line in lines:
        if 'Execution time' in line:
            tpe=float(line.lstrip('Execution time:').replace('ms/evt','').replace(' ',''))
            List_TPE.append(tpe)
    f.close()


    #SUM=sum(List_TPE)
    #AVG=SUM/len(List_TPE)

    #print AVG
    return List_TPE

if __name__ == '__main__':
    inputdir=sys.argv[1]
    key=''
    if len(sys.argv)>2:
        key=sys.argv[2]
    search=inputdir+'/*'+key+'*.out'
    search=search.replace('**','*')
    outputlist=glob.glob(search)
    #outfile='mkShapes__2016__cms_scratch_jhchoi_AN_PLOT_v2_1_Resolved_HMFull_V13_RelW0.02_DeepAK8WP0p5_dMchi2Resolution_Combine__ALL__Wjets2j.7.9.out'
    List=[]
    for outfile in outputlist:
        List+=GetTimePerEvent(outfile)


    SUM=sum(List)
    AVG=SUM/len(List)

    print inputdir
    print key
    print AVG,'ms/evt'
