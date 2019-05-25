OK=1
LINES=0

STACK_NAME=${STACK_NAME:=em-stack}

for line in $(docker stack services ${STACK_NAME} |awk 'NR>1{print $4}'); do
    LINES=$((LINES + 1))
    A="$(cut -d'/' -f1 <<<"$line")"
    B="$(cut -d'/' -f2 <<<"$line")"
    if (( A < B )); then
        OK=0
    fi
done

if (( OK == 1 )) && (( LINES > 0 )); then
    echo "OK"
else
    echo "Some services are down"
fi
