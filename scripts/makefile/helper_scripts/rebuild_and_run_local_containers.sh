#!/usr/bin/env bash
COMMAND=$1
VERBOSITY=$2

if [ "$COMMAND" != "build" ] && [ "$COMMAND" != "run" ] && [ "$COMMAND" != "stop" ]; then
  echo "Valid commands are \"build\", \"run\", and \"stop\""
  echo "You passed $COMMAND"
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command> <verbosity>"
  exit 1
fi

if [ "$VERBOSITY" != "loud" ] && [ "$VERBOSITY" != "quiet" ]; then
  echo "Valid vebosity values are \"quiet\" and \"loud\""
  echo "You passed $VERBOSITY"
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command> <verbosity>"
  exit 1
fi

shift 2
CONTAINER_NAMES="$@"

for container_name in ${CONTAINER_NAMES}; do

  echo "Running ${COMMAND} on ${container_name}"

  if [ "$VERBOSITY" == "loud" ]; then
    if [ "$COMMAND" == "run" ]; then
      docker exec -d ${container_name} bash -c "/entrypoint.sh run"
    else
      docker exec ${container_name} bash -c "/entrypoint.sh \"${COMMAND}\""
    fi
  else
    if [ "$COMMAND" == "run" ]; then
      docker exec -d ${container_name} bash -c "/entrypoint.sh run" > /dev/null
    else
      docker exec ${container_name} bash -c "/entrypoint.sh \"${COMMAND}\"" > /dev/null
    fi
  fi
  echo "Finished running ${COMMAND} on ${container_name}"
done
