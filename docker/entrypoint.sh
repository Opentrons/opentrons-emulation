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

build_module_simulator() {
  cd /opentrons-modules && \
  cmake --preset=stm32-host-gcc10 . && \
  cmake --build ./build-stm32-host --target $1
}

# OPENTRONS_HARDWARE is an env variable that is passed to every container

FULL_COMMAND="$COMMAND"-"$OPENTRONS_HARDWARE"
OTHER_ARGS=`echo "${@:2}"`
echo "${FULL_COMMAND}"
case $FULL_COMMAND in

  # Hardware Level

  build-heater-shaker-hardware)
    build_module_simulator "heater-shaker-simulator"
    ;;
  build-thermocycler-hardware)
    build_module_simulator "thermocycler-refresh-simulator"
    ;;

  build-thermocycler-firmware|build-magdeck-firmware|build-tempdeck-firmware|build-emulator-proxy|build-robot-server|build-common-firmware|build-smoothie)
    (cd /opentrons/shared-data/python && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/api && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/notify-server && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/robot-server && python3 setup.py bdist_wheel -d /dist/)
    pip install /dist/*
    ;;

  build-common-ot3-firmware)
    cd /ot3-firmware && \
    cmake --preset host-gcc10 && \
    cmake --build --preset=simulators
    ;;

  run-heater-shaker-hardware)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator $OTHER_ARGS"
    ;;
  run-thermocycler-hardware)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator $OTHER_ARGS"
    ;;

  run-ot3-pipettes-hardware)
    /ot3-firmware/build-host/pipettes/simulator/pipettes-simulator
    ;;
  run-ot3-head-hardware)
    /ot3-firmware/build-host/head/simulator/head-simulator
    ;;
  run-ot3-gantry-x-hardware)
    /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator
    ;;
  run-ot3-gantry-y-hardware)
    /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator
    ;;

  # Firmware Level

  build-thermocycler-firmware|build-magdeck-firmware|build-tempdeck-firmware|build-emulator-proxy|build-robot-server|build-common-firmware)
    (cd /opentrons/shared-data/python && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/api && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/notify-server && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/robot-server && python3 setup.py bdist_wheel -d /dist/)
    pip install /dist/*
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
  run-smoothie)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_smoothie"
    ;;
  *)
    echo "Command ${FULL_COMMAND} not found."
    exit 2
    ;;
esac
