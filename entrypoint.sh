usage() {
        cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") <command>

command               What command you want to execute (build, run)

Available options:
-h, --help              Print this help and exit

EOF
        exit
}


if [ $# -ne 1 ]; then
  echo "Must provide arg \"command\""
  usage
fi

COMMAND=$1

if [ "$COMMAND" != "build" ] && [ "$COMMAND" != "run" ]; then
  echo "Valid commands are \"build\" and \"run\""
  echo "You passed $COMMAND"
  usage
fi

FULL_COMMAND="$COMMAND"-"$OPENTRONS_HARDWARE"

case $FULL_COMMAND in
  build-heater-shaker)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target heater-shaker-simulator
    )
    ;;
  run-heater-shaker)
    /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator
    ;;
  build-ot3-firmware-echo)
    (
      cd ot3-firmware && \
      cmake --preset host-gcc10 && \
      cmake --build ./build-host --target can-simulator
    )
    ;;
  run-ot3-firmware-echo)
    /ot3-firmware/build-host/can/simulator/can-simulator
    ;;
esac