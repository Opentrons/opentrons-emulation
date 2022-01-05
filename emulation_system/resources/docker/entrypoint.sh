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


build_ot3_simulator() {
      cd /ot3-firmware && \
      cmake --preset host-gcc10 && \
      cmake --build ./build-host --target $1
}

case $FULL_COMMAND in
  build-heater-shaker)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target heater-shaker-simulator
    )
    ;;
  run-heater-shaker)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator $OTHER_ARGS"
    ;;
  build-thermocycler)
    (
      cd /opentrons-modules && \
      cmake --preset=stm32-host-gcc10 . && \
      cmake --build ./build-stm32-host --target thermocycler-refresh-simulator
    )
    ;;
  run-thermocycler)
    bash -c "/opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator $OTHER_ARGS"
    ;;
  run-emulator-proxy)
    python3 -m opentrons.hardware_control.emulation.app
    ;;
  run-thermocycler-driver)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator thermocycler $OTHER_ARGS"
    ;;
  run-tempdeck-driver)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator tempdeck $OTHER_ARGS"
    ;;
  run-magdeck-driver)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_module_emulator magdeck $OTHER_ARGS"
    ;;
  run-robot-server)
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto --reload"
    ;;
  build-ot3-pipettes)
      build_ot3_simulator "pipettes_simulator"
    ;;
  build-ot3-head)
      build_ot3_simulator "head_simulator"
    ;;
  build-ot3-gantry-x)
      build_ot3_simulator "gantry_x_simulator"
    ;;
  build-ot3-gantry-y)
      build_ot3_simulator "gantry_y_simulator"
    ;;
  run-ot3-pipettes)
    /ot3-firmware/build-host/pipettes/simulator/pipettes_simulator
    ;;
  run-ot3-head)
    /ot3-firmware/build-host/head/simulator/head_simulator
    ;;
  run-ot3-gantry-x)
    /ot3-firmware/build-host/gantry/simulator/gantry_x_simulator
    ;;
  run-ot3-gantry-y)
    /ot3-firmware/build-host/gantry/simulator/gantry_y_simulator
    ;;
esac
