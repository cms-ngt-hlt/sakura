 #!/bin/sh

if [[ ${#} -lt 2 ]]
then
    echo "Usage: ${0} <intervalcheck> <program> [<output>]"
    exit 1
fi

INTERVAL=${1}
PROGRAM=${2}

if [[ ${#} -eq 3 ]]
then
    OUTPUT=${3}
    rm -f ${OUTPUT}
    touch ${OUTPUT}
else
    OUTPUT=/dev/stdout
fi

while true
do
    LOGHEADER="checking '${PROGRAM}': $(date)"
    echo ${LOGHEADER}
    MEMORY=$(ps -u ${USER} -o rss,cmd -ww | \
        awk -v program="${PROGRAM}" '$2 ~ program {print}' | \
        egrep -v 'grep|memory' | awk '{print $1}')
    if [[ ${MEMORY} == "" ]]
    then
        break
    fi
    #echo "${LOGHEADER} >> rss: ${MEMORY}" >> ${OUTPUT}
    echo "${MEMORY}" >> $OUTPUT

    sleep ${INTERVAL}
done
