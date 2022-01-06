#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Must provide \"command\""
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command>"
  exit 1
fi

COMMAND=$1

if [ "$COMMAND" != "build" ] && [ "$COMMAND" != "run" ]; then
  echo "Valid commands are \"build\" and \"run\""
  echo "You passed $COMMAND"
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command>"
  exit 1
fi

# OPENTRONS_HARDWARE is an env variable that is passed to every container

FULL_COMMAND="$COMMAND"-"$OPENTRONS_HARDWARE"
OTHER_ARGS=`echo "${@:2}"`
echo "${FULL_COMMAND}"
case $FULL_COMMAND in
  build-heater-shaker-hardware)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target heater-shaker-simulator
    )
    ;;
  build-ot3-echo-hardware)
    (
      cd /ot3-firmware && \
      cmake --preset host-gcc10 && \
      cmake --build ./build-host --target can-simulator
    )
    ;;
  build-thermocycler-hardware)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target thermocycler-refresh-simulator
    )
    ;;
  build-thermocycler-firmware|build-magdeck-firmware|build-tempdeck-firmware|build-emulator-proxy|build-robot-server|build-common-firmware)
    (cd /opentrons/shared-data/python && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/api && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/notify-server && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/robot-server && python3 setup.py bdist_wheel -d /dist/)
    pip install /dist/*
    ;;
  run-heater-shaker-hardware)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator $OTHER_ARGS"
    ;;
  run-thermocycler-hardware)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator $OTHER_ARGS"
    ;;
  run-ot3-echo-hardware)
    /ot3-firmware/build-host/can/simulator/can-simulator
    ;;
  run-thermocycler-firmware)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator thermocycler $OTHER_ARGS"
    ;;
  run-tempdeck-firmware)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator tempdeck $OTHER_ARGS"
    ;;
  run-magdeck-firmware)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator magdeck $OTHER_ARGS"
    ;;
  run-robot-server)
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto --reload"
    ;;
  run-emulator-proxy)
    python3 -m opentrons.hardware_control.emulation.app
    ;;

  *)
    echo "Command ${FULL_COMMAND} not found."
    exit 2
    ;;
esac
