#!/bin/bash

HEADLESS="NO"
DOCKER_COMPOSE_FILE_NAME="docker-compose.yaml"
FIRMWARE_DIR_NAME="ot3"
FIRMWARE_REPO_NAME="ot3-firmware"
FIRMWARE_BRANCH="main"
MODULES_DIR_NAME="modules"
MODULES_REPO_NAME="opentrons-modules"
MODULES_BRANCH="edge"
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"



usage() {
        cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [-d] [--dev]

This script will create fully-automated Ubuntu 20.04 Focal Fossa installation media.

Available options:
-h, --help                      Print this help and exit
-d, --detached                  Run system headless
--dev                           Run as development system

EOF
        exit
}

while :; do
  case $1 in
    -h |-\?|--help) usage ;;
    -d | --detached) HEADLESS="YES" ;;
    --dev) DOCKER_COMPOSE_FILE_NAME="docker-compose-dev.yaml" ;;
    --)
      shift
      break
      ;;
    -?*)
      printf 'ERROR: Unknown option: %s\nExiting...\n' "$1" >&2
      exit 1
      ;;
    *)
      break
  esac
  shift
done

$SCRIPT_DIR/teardown_can.sh
$SCRIPT_DIR/setup_can.sh
docker-compose -f $SCRIPT_DIR/../$DOCKER_COMPOSE_FILE_NAME rm -fs
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f $SCRIPT_DIR/../$DOCKER_COMPOSE_FILE_NAME build

if [ $HEADLESS == "YES" ]
then
  docker-compose -f $SCRIPT_DIR/../$DOCKER_COMPOSE_FILE_NAME up -d
else
  docker-compose -f $SCRIPT_DIR/../$DOCKER_COMPOSE_FILE_NAME up
fi


