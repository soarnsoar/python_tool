#ARR_SYS=(ElepTup ElepTdo MupTup MupTdo METup METdo)
ARR_SYS=(ElepTup)

for sys in ${ARR_SYS[@]};do
    DIR=/xrootd_user/jhchoi/xrootd/Latino/HWWNano/Fall2017_102X_nAODv4_Full2017v5/MCl1loose2017v5__MCCorr2017v5__${sys}
    ARR_FILE=($(ls ${DIR}/*.root))
    for f in ${ARR_FILE[@]};do
	#echo $f
	python OpenFileInPyroot.py ${f}

    done

done
