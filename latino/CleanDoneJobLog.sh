DIRBASE='NanoGardening__'


while [ 1 ]




do
    N=0
    ARR_DIR=( $(ls -d ${DIRBASE}*/*/) )
    for DIR in ${ARR_DIR[@]};do
	continue
	echo "${DIR}"
    done



    for DIR in ${ARR_DIR[@]};do
	
	echo "$DIR"
	THISN=`ls ${DIR}/donelogs/*.log | wc -l`
	rm ${DIR}/donelogs/*.jid*
	rm ${DIR}/donelogs/*.log*
	rm ${DIR}/donelogs/*.err*
	rm ${DIR}/donelogs/*.out*
	rm ${DIR}/donelogs/*.done*
	rm ${DIR}/donelogs/*.jds*
	rm ${DIR}/donelogs/*.py*
	rm ${DIR}/donelogs/*.sh*
	rm ${DIR}/donelogs/*.root*
	echo "=========="
	date
	echo "Done N=$THISN"
	echo "=========="
	N=`expr $N + $THISN`

    done
    if [ $N -gt 0 ]
    then
	echo "$N jobs done!"
	echo "$N jobs done!" | /bin/mailx -s "$N jobs done!" "jhchoi.kisti@gmail.com"
    fi
	





    ARR_DIR=($(ls -d ${DIRBASE}*/*/ | grep -v donelogs))
    for DIR in ${ARR_DIR};do

	N=`ls ${DIR}/NanoGardening__* |grep -v donelogs | wc -l`	
        #if [ $N -eq 0 ]
        #then
        #    echo "No jobs to run"
        #    rm ${DIR}/*
        #    continue
        #fi                                                                                                                                                                       

    done
    echo "go to sleep"
    sleep 600
done
