DIR=$1
ALIAS=$2

TOTAL=`ls ${DIR}/*${ALIAS}*.sh*|wc -l`
DONE=`ls ${DIR}/*${ALIAS}*.done|wc -l`

echo "${ALIAS}--> ${DONE}/${TOTAL}"

