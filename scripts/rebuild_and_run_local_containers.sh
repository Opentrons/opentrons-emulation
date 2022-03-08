#!/usr/bin/env bash

CONTAINER_IDS=`docker-compose -f - ps -q`
for container_id in ${CONTAINER_IDS}; do
  docker container inspect --format '{{ .Mounts }}' ${container_id} | grep -q "entrypoint.sh"
  if [[ $? -eq 0 ]]; then
    docker exec ${container_id} bash -c "/entrypoint.sh stop"
    docker exec ${container_id} bash -c "/entrypoint.sh build" > /dev/null
    docker exec -d ${container_id} bash -c "/entrypoint.sh run"
  fi
done
