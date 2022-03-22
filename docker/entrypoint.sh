#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Must provide \"command\""
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command>"
  exit 1
fi

COMMAND=$1

if [ "$COMMAND" != "build" ] && [ "$COMMAND" != "run" ] && [ "$COMMAND" != "stop" ]; then
  echo "Valid commands are \"build\", \"run\", and \"stop\""
  echo "You passed $COMMAND"
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <command>"
  exit 1
fi

build_ot3_firmware_simulators()
  (cd /ot3-firmware && cmake --preset host-gcc10 && cmake --build --preset=simulators)

build_module_simulator() {
  (cd /opentrons-modules && cmake --preset=stm32-host-gcc10 . && cmake --build ./build-stm32-host --target $1)
}

build_ot3_firmware_single_simulator() {
  (cd /ot3-firmware && cmake --preset host-gcc10 && cmake --build ./build-host --target $1)
}

kill_process() {
  if [[ "$COMMAND" != "stop" ]]; then
    echo "Cannot run kill_process outside of the stop command."
    exit 1
  fi
  pkill -9 -f ${1:?error, must pass parameter to kill_process}
}

# OPENTRONS_HARDWARE is an env variable that is passed to every container

FULL_COMMAND="$COMMAND"-"$OPENTRONS_HARDWARE"
OTHER_ARGS=`echo "${@:2}"`
echo "${FULL_COMMAND}"
case $FULL_COMMAND in

  # Hardware Level

  build-heater-shaker-hardware)
    build_module_simulator "heater-shaker-simulator"
    cp /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator /heater-shaker-simulator
    ;;
  build-thermocycler-hardware)
    build_module_simulator "thermocycler-refresh-simulator"
    cp /opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator /thermocycler-refresh-simulator
    ;;

  # Will only use this for remote builds when we can control everything being built at once and then picking
  # and choosing which executeable is sent to which container
  build-common-ot3-firmware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/pipettes/simulator/pipettes-single-simulator /pipettes-simulator
    cp /ot3-firmware/build-host/head/simulator/head-simulator /head-simulator
    cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /gantry-x-simulator
    cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /gantry-y-simulator
    cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /bootloader-simulator
    cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /gripper-simulator
    ;;

  # TODO: Figure out why below ot3 builders are failing if I build just the single simulator and not all of them.

  build-ot3-gantry-x-hardware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /gantry-x-simulator
    ;;

  build-ot3-gantry-y-hardware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /gantry-y-simulator
    ;;

  build-ot3-head-hardware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/head/simulator/head-simulator /head-simulator
    ;;

  build-ot3-pipettes-hardware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/pipettes/simulator/pipettes-single-simulator /pipettes-simulator
    ;;

  build-ot3-bootloader-hardware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /bootloader-simulator
    ;;

  build-ot3-gripper-hardware)
    build_ot3_firmware_simulators
    cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /gripper-simulator
    ;;

  run-heater-shaker-hardware)
    bash -c "/heater-shaker-simulator $OTHER_ARGS"
    ;;
  run-thermocycler-hardware)
    bash -c "/thermocycler-refresh-simulator $OTHER_ARGS"
    ;;

  run-ot3-pipettes-hardware)
    /pipettes-simulator
    ;;
  run-ot3-head-hardware)
    /head-simulator
    ;;
  run-ot3-gantry-x-hardware)
    /gantry-x-simulator
    ;;
  run-ot3-gantry-y-hardware)
    /gantry-y-simulator
    ;;
  run-ot3-bootloader-hardware)
    /bootloader-simulator
    ;;
  run-ot3-gripper-hardware)
    /gripper-simulator
    ;;

  stop-ot3-gantry-y-hardware|stop-heater-shaker-hardware|stop-thermocycler-hardware|stop-ot3-pipettes-hardware|stop-ot3-head-hardware|stop-ot3-gantry-x-hardware)
    kill_process $OPENTRONS_HARDWARE
    ;;

  # Firmware Level

  build-thermocycler-firmware|build-magdeck-firmware|build-tempdeck-firmware|build-emulator-proxy|build-robot-server|build-common-firmware|build-smoothie|build-can-server)
    pip uninstall --yes /dist/*
    (cd /opentrons/shared-data/python && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/api && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/notify-server && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/robot-server && python3 setup.py bdist_wheel -d /dist/)
    (cd /opentrons/hardware && python3 setup.py bdist_wheel -d /dist/)
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
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto"
    ;;
  run-emulator-proxy)
    python3 -m opentrons.hardware_control.emulation.app
    ;;
  run-smoothie)
    bash -c "python3 -m opentrons.hardware_control.emulation.scripts.run_smoothie"
    ;;
  run-can-server)
    bash -c "python3 -m opentrons_hardware.scripts.sim_socket_can"
    ;;

  stop-thermocycler-firmware|stop-tempdeck-firmware|stop-magdeck-firmware)
    kill_process opentrons.hardware_control.emulation.scripts.run_module_emulator
    ;;
  stop-emulator-proxy)
    kill_process opentrons.hardware_control.emulation.app
    ;;
  stop-robot-server)
    kill_process /usr/local/bin/uvicorn
    ;;
  stop-smoothie)
    kill_process opentrons.hardware_control.emulation.script
    ;;
  stop-can-server)
    kill_process opentrons_hardware.script
    ;;

  *)
    echo "Command ${FULL_COMMAND} not found."
    exit 2
    ;;
esac
