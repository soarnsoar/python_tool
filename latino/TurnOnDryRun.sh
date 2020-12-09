echo "Turn on DryRun"

function condor_submit(){
    echo "DO NOT SUBMIT! DRY RUN"
}
export -f condor_submit
