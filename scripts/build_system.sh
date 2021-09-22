#!/bin/bash

PULL_FIRMWARE="YES"
HEADLESS="NO"
PULL_FROM=""
while :; do
  case $1 in
    -h|-\?|--help)
      printf "Usage: \n./build_system.sh \n./build_system.sh --no-pull\n./build_system.sh --pull-from <commit_id>\n"
      exit
      ;;
    --no-pull)
      PULL_FIRMWARE="NO"
      ;;
    --pull-from)
      PULL_FROM="$2"
      ;;
    --headless)
      HEADLESS="YES"
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

# Grabs firmware and puts it where Docker can build it
if [ $PULL_FIRMWARE == "YES" ]
then
  if [ -z "$PULL_FROM" ]
  then
    echo "Pulling main from ot3-firmware"
    DOWNLOAD_PATH="https://github.com/Opentrons/ot3-firmware/archive/refs/heads/main.zip"
  else
    echo "Pulling commit $PULL_FROM from ot3-firmware"
    DOWNLOAD_PATH="https://github.com/Opentrons/ot3-firmware/archive/$PULL_FROM.zip"
  fi

  (
    cd ../emulator/ && \
    rm -rf ot3-firmware && \
    wget -q -O ot3-firmware.zip "$DOWNLOAD_PATH" && \
    unzip -q ot3-firmware.zip && \
    rm -f ot3-firmware.zip && \
    mv ot3-firmware* ot3-firmware
  )

fi
./teardown_can.sh
./setup_can.sh
docker-compose -f ../docker-compose.yaml rm -fs
docker-compose -f ../docker-compose.yaml build

if [ $HEADLESS == "YES" ]
then
  docker-compose -f ../docker-compose.yaml up -d
else
  docker-compose -f ../docker-compose.yaml up --abort-on-container-exit
fi


