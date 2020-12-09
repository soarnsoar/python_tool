DIRBASE='mkShapes__'


while [ 1 ]
do
    StartTime=$(date +%s)
    ARR_DIR=($(ls -d ${DIRBASE}*/))
    echo "======LIST of Directories======="
    for DIR in ${ARR_DIR[@]};do
        echo ${DIR}
    done



    for DIR in ${ARR_DIR[@]};do
	
	python python_tool/latino/check_plot_job.py ${DIR} --want_remove n --want_resub_notstarted n --want_resub_noDone n --want_resub_fail y --nmaxjob=1000

    done


    while [ 1 ]
    do
        ##To avoid too frequenct checking
        EndTime=$(date +%s)
        IterTime=$(($EndTime - $StartTime))

        if [ $IterTime -lt 300 ]
        then
            echo "CURRENT IterTime=$IterTime"
            echo "Sleep 100 sec until IterTime is over 300"
            sleep 100
        else
            break
        fi

    done


done
