#!/usr/bin/env bash

CONTAINER_IDS=`docker-compose -f - ps -q`  # Get ids from generated compose file

for container_id in ${CONTAINER_IDS}; do
  # Load mounts from each container and check to see if they have entrypoint.sh mounted
  docker container inspect --format '{{ .Mounts }}' ${container_id} | grep -q "entrypoint.sh"

  # If they have it mounted (grep exited with 0) stop, build, then run
  if [[ $? -eq 0 ]]; then
    docker exec ${container_id} bash -c "/entrypoint.sh stop"
    docker exec ${container_id} bash -c "/entrypoint.sh build" > /dev/null
    docker exec -d ${container_id} bash -c "/entrypoint.sh run"
  fi
done
