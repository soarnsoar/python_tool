DIRBASE='NanoGardening__'







while [ 1 ]
do



    StartTime=$(date +%s)

    ARR_DIR=($(ls -d ${DIRBASE}*/*/ | grep -v donelogs))

    echo "======LIST of Directories======="
    for DIR in ${ARR_DIR[@]};do
	echo ${DIR}

    done

    idx=0
    for DIR in ${ARR_DIR[@]};do
	
	EndTime=$(date +%s)
	IterTime=$(($EndTime - $StartTime)) ## time for one iteration
	
	if [ $IterTime -gt 5000 ]
	then
	    break
	fi


	N=`ls ${DIR}/NanoGardening__*.sh|grep -v log_|grep -v err_|grep -v out_ | grep -v jid_ |grep -v donelogs | wc -l`
	if [ $N -eq 0 ]
	then
	    echo "No jobs to run"
	    rm -rf ${DIR}
	    continue
	fi

	date
	echo "IterTime=""$IterTime"
	echo "Directory index=""${idx}"
	echo "N jobs=$N"
	echo "Directory="${DIR}
	python python_tool/latino/check_nanoGardener_jobs.py ${DIR} -d n -u n -r y -c n -N 800

	idx=`expr $idx + 1`
    done
    
    while [ 1 ] 
    do
	##To avoid too frequenct checking
	EndTime=$(date +%s)
	IterTime=$(($EndTime - $StartTime))
	
	if [ $IterTime -lt 600 ]
	then
	    echo "CURRENT IterTime=$IterTime"
	    echo "Sleep 100 sec until IterTime is over 600"
	    sleep 100
	else
	    break
	fi

    done
    #break
#sleep 1000
done
    
    
