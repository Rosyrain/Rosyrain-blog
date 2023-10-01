TIME_OUT=10
BOOL=false
i=0
while [ ! $BOOL ] && [ "$i" -lt "$TIME_OUT" ]
do
    let i+=1
    echo $i
    sleep 1
done