DIRBASE='NanoGardening__'







while [ 1 ]
do
    ARR_DIR=($(ls -d ${DIRBASE}*/*/ | grep -v donelogs))

    echo "======LIST of Directories======="
    for DIR in ${ARR_DIR[@]};do
	echo ${DIR}

    done

    idx=0
    for DIR in ${ARR_DIR[@]};do

	if [ $idx -gt 300 ]
	then
	    break
	fi


	N=`ls ${DIR}/NanoGardening__* |grep -v donelogs | wc -l`
	if [ $N -eq 0 ]
	then
	    echo "No jobs to run"
	#    rm ${DIR}/*
	    continue
	fi
	python python_tool/latino/check_nanoGardener_jobs.py ${DIR} -d n -u n -r y -c n -N 800

	idx=`expr $idx + 1`
    done
    #break
#sleep 1000
done
    
    
