
DIRLIST=($(ls -d NanoGardening__*/*/))


for dir in ${DIRLIST[@]};do
    echo "${dir}"
    python python_tool/condor_rm_zombie.py  ${dir}
done
