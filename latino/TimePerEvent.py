import glob, sys

def GetTimePerEventList(outfile):
    f=open(outfile,'r')
    lines=f.readlines()

    List_TPE=[] ##TimePerEvent
    List_TreeTime=[] ##        Time spent on tree input:
    List_FilterTime=[] ## [Event filter]:

    for line in lines:
        if 'Execution time' in line:
            tpe=float(line.lstrip('Execution time:').replace('ms/evt','').replace(' ',''))
            List_TPE.append(tpe)
        if 'Time spent on tree input:' in line:
            treetime=float(line.split('Time spent on tree input:')[1].split('ms/evt')[0].replace(' ',''))
            List_TreeTime.append(treetime)
        if '[Event filter]:' in line:
            FilterTime=float(line.split('[Event filter]:')[1].split('ms/evt')[0].replace(' ','')  )
    f.close()


    #SUM=sum(List_TPE)
    #AVG=SUM/len(List_TPE)

    #print AVG
    return List_TPE, List_TreeTime, List_FilterTime

if __name__ == '__main__':
    inputdir=sys.argv[1]
    key=''
    if len(sys.argv)>2:
        key=sys.argv[2]
    search=inputdir+'/*'+key+'*.out'
    search=search.replace('**','*')
    
    print "--Get List of files"
    outputlist=glob.glob(search)
    #outfile='mkShapes__2016__cms_scratch_jhchoi_AN_PLOT_v2_1_Resolved_HMFull_V13_RelW0.02_DeepAK8WP0p5_dMchi2Resolution_Combine__ALL__Wjets2j.7.9.out'
    print "len(outputlist)=",len(outputlist)
    print "--Gathering infos.."
    ListTPE=[]
    ListTreeTime=[]
    ListFilterTime=[]
    for outfile in outputlist:
        _List_TPE, _LIST_TreeTime, _List_FilterTime=GetTimePerEventList(outfile)
        ListTPE+=_List_TPE
        ListTreeTime+=_LIST_TreeTime
        ListFilterTime+=_List_FilterTime

    SUM_TPE=sum(ListTPE)
    AVG_TPE=SUM/len(ListTPE)

    SUM_TreeTime=sum(ListTreeTime)
    AVG_TreeTime=SUM/len(ListTreeTime)

    SUM_FilterTime=sum(ListFilterTime)
    AVG_FilterTime=SUM/len(ListFilterTime)

    print inputdir
    print key
    print 'TimePerEvent',AVG_TPE,'ms/evt'
    print 'Time-ReadingTree',AVG_TreeTime,'ms/evt'
    print 'Time-Filter',AVG_FilterTime,'ms/evt'
