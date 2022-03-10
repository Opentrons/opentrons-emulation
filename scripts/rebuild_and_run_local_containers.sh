#!/usr/bin/env bash
CONTAINER_IDS=`docker-compose -f - ps -q`  # Get ids from generated compose file
date
for container_id in ${CONTAINER_IDS}; do
  # Load mounts from each container and check to see if they have entrypoint.sh mounted
  docker container inspect --format '{{ .Mounts }}' ${container_id} | grep -q "entrypoint.sh"
  IS_LOCAL=$?
  docker container inspect --format '{{ .Mounts }}' ${container_id} | grep -q "ot3-firmware"
  IS_FIRMWARE=$?
  CONTAINER_NAME=`docker container inspect --format '{{ .Name }}' ${container_id} | cut -c2-`

  # If they have it mounted (grep exited with 0) stop, build, then run
  if { [ "$IS_LOCAL" -eq 0 ] && [ -z "$2" ]; } || { [ "$IS_LOCAL" -eq 0 ] && [ "$2" == "firmware" ] && [ "$IS_FIRMWARE" -eq 0 ]; } then
    echo "${CONTAINER_NAME}"
    echo "Stopping -> ${CONTAINER_NAME}"
    docker exec ${container_id} bash -c "/entrypoint.sh stop" > /dev/null
    echo "Building ${CONTAINER_NAME}"
    if [[ "$1" == "quiet" ]]; then
      docker exec ${container_id} bash -c "/entrypoint.sh build" > /dev/null
    else
      docker exec ${container_id} bash -c "/entrypoint.sh build"
    fi
    echo "Running ${CONTAINER_NAME}"
    docker exec -d ${container_id} bash -c "/entrypoint.sh run"
  fi
done
date
