#!/bin/bash

HEADLESS="NO"

FIRMWARE_DIR_NAME="ot3"
FIRMWARE_REPO_NAME="ot3-firmware"
FIRMWARE_BRANCH="main"

MODULES_DIR_NAME="modules"
MODULES_REPO_NAME="opentrons-modules"
MODULES_BRANCH="edge"

usage() {
        cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [-d] [-f firmware-branch-name] [-m module-branch-name]

This script will create fully-automated Ubuntu 20.04 Focal Fossa installation media.

Available options:
-h, --help                      Print this help and exit
-f, --ot3-firmware-branch       Branch to pull OT-3 firmware from
-d, --detached                  Run system headless

EOF
        exit
}

while :; do
  case $1 in
    -h |-\?|--help) usage ;;
    -f | --ot3-firmware-branch) FIRMWARE_BRANCH="$2" ;;
    -d | --detached) HEADLESS="YES" ;;
    -m | --modules-branch-name) MODULES_BRANCH="$2" ;;
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

#./pull_from_repo.sh $FIRMWARE_REPO_NAME $FIRMWARE_BRANCH $FIRMWARE_DIR_NAME
#./pull_from_repo.sh $MODULES_REPO_NAME $MODULES_BRANCH $MODULES_DIR_NAME


../teardown_can.sh
../setup_can.sh
docker-compose -f ../../docker-compose.yaml rm -fs
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose -f ../../docker-compose.yaml build

if [ $HEADLESS == "YES" ]
then
  docker-compose -f ../../docker-compose.yaml up -d
else
  docker-compose -f ../../docker-compose.yaml up
fi


