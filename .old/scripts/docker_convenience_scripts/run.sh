OTHER_ARGS=`echo "${@:2}"`
docker exec -it $1 /bin/bash -c "/entrypoint.sh run $OTHER_ARGS"