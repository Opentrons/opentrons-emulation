#!/bin/bash

# Abs path to this script. Returns the same thing regardless of where the script was
# executed from
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

HEADLESS_FLAG="NO"
DEV_FLAG="NO"
CUSTOM_OT3_FIRMWARE_FLAG="NO"
CUSTOM_MODULES_FLAG="NO"

PROD_DOCKER_COMPOSE_FILE_NAME="docker-compose.yaml"
DEV_DOCKER_COMPOSE_FILE_NAME="docker-compose-dev.yaml"

FIRMWARE_SOURCE_DOWNLOAD_LOCATION=""
MODULE_SOURCE_DOWNLOAD_LOCATION=""

usage() {
        cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [-h] [--detached] [--dev] [--ot3-firmware-sha full-commit-sha] [--modules-sha full-commit-sha]

This script will create an emulated system of opentrons hardware

Available Options:
  -h, --help                      Print this help and exit
  --detached, --headless          Run system headless
  --dev                           Run as development system

Production Options:
  --ot3-firmware-sha              Download ot3-firmware repo from passed commit sha
  --modules-sha                   Download opentrons modules repo from passed commit sha

EOF
        exit
}

while :; do
  case "${1-}" in
    -h |-\?|--help) usage ;;
    --detached | --headless) HEADLESS_FLAG="YES" ;;
    --dev) DEV_FLAG="YES";;
    --ot3-firmware-sha)
      CUSTOM_OT3_FIRMWARE_FLAG="YES"
      FIRMWARE_SOURCE_DOWNLOAD_LOCATION="https://github.com/Opentrons/ot3-firmware/archive/${2-}.zip"
      shift
      ;;
    --modules-sha)
      CUSTOM_MODULES_FLAG="YES"
      MODULE_SOURCE_DOWNLOAD_LOCATION="https://github.com/Opentrons/opentrons-modules/archive/${2-}.zip"
      shift
      ;;
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

if [[ "$DEV_FLAG" == "YES" && ("$CUSTOM_OT3_FIRMWARE_FLAG" == "YES" || "$CUSTOM_MODULES_FLAG" == "YES") ]]; then
  echo
  >&2 echo "ERROR: Cannot specify --dev with either --ot3-firmware-sha or --modules-sha"
  echo
  usage
  exit 1
fi

if [ "$DEV_FLAG" == "YES" ]; then
  DOCKER_COMPOSE_FILE_NAME="$DEV_DOCKER_COMPOSE_FILE_NAME"
else
  DOCKER_COMPOSE_FILE_NAME="$PROD_DOCKER_COMPOSE_FILE_NAME"
fi

COMPOSE_FILE_PATH="$SCRIPT_DIR/../$DOCKER_COMPOSE_FILE_NAME"

BUILD_COMMAND="COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose --verbose -f $COMPOSE_FILE_PATH build "

if [ "$CUSTOM_OT3_FIRMWARE_FLAG" == "YES" ]; then
  BUILD_COMMAND="$BUILD_COMMAND --build-arg FIRMWARE_SOURCE_DOWNLOAD_LOCATION=\"$FIRMWARE_SOURCE_DOWNLOAD_LOCATION\""
fi

if [ "$CUSTOM_MODULES_FLAG" == "YES" ]; then
  BUILD_COMMAND="$BUILD_COMMAND --build-arg MODULE_SOURCE_DOWNLOAD_LOCATION=\"$MODULE_SOURCE_DOWNLOAD_LOCATION\""
fi



echo $BUILD_COMMAND

$SCRIPT_DIR/teardown_can.sh
$SCRIPT_DIR/setup_can.sh
docker-compose -f $COMPOSE_FILE_PATH rm -fs
eval $BUILD_COMMAND

if [ "$HEADLESS_FLAG" == "YES" ]
then
  docker-compose -f $COMPOSE_FILE_PATH up -d
else
  docker-compose -f $COMPOSE_FILE_PATH up
fi


