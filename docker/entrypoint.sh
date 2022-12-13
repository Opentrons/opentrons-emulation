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

build_ot3_firmware_simulators()
  (
    cd /ot3-firmware && \
    cmake --preset host-gcc10 && \
    cmake --build --preset=simulators -j $(expr $(nproc) - 1)
  )

build_module_simulator() {
  (cd /opentrons-modules && cmake --preset=stm32-host-gcc10 . && cmake --build ./build-stm32-host -j $(expr $(nproc) - 1) --target $1)
}

build_ot3_firmware_single_simulator() {
  (
    cd /ot3-firmware && \
    cmake --preset host-gcc10 && \
    cmake --build ./build-host -j $(expr $(nproc) - 1) --target $1
    )
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
    build_module_simulator "thermocycler-gen2-simulator"
    cp /opentrons-modules/build-stm32-host/stm32-modules/thermocycler-gen2/simulator/thermocycler-gen2-simulator /thermocycler-gen2-simulator
    ;;

  # Will only use this for remote builds when we can control everything being built at once and then picking
  # and choosing which executeable is sent to which container
  build-common-ot3-firmware)
    build_ot3_firmware_simulators
    mkdir /executable
    cp /ot3-firmware/build-host/pipettes/simulator/pipettes-single-simulator /executable/pipettes-simulator
    cp /ot3-firmware/build-host/head/simulator/head-simulator /executable/head-simulator
    cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /executable/gantry-x-simulator
    cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /executable/gantry-y-simulator
    cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /executable/bootloader-simulator
    cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /executable/gripper-simulator
    ;;

  run-heater-shaker-hardware)
    bash -c "/heater-shaker-simulator $OTHER_ARGS"
    ;;
  run-thermocycler-hardware)
    bash -c "/thermocycler-gen2-simulator $OTHER_ARGS"
    ;;

  run-ot3-pipettes-hardware)
    /executable/pipettes-simulator
    ;;
  run-ot3-head-hardware)
    /executable/head-simulator
    ;;
  run-ot3-gantry-x-hardware)
    /executable/gantry-x-simulator
    ;;
  run-ot3-gantry-y-hardware)
    /executable/gantry-y-simulator
    ;;
  run-ot3-bootloader-hardware)
    /executable/bootloader-simulator
    ;;
  run-ot3-gripper-hardware)
    /executable/gripper-simulator
    ;;
  run-ot3-state-manager)
    # 9999 is the hardcoded state manager port
    (
      cd /ot3-firmware/state_manager && \
      ../stm32-tools/poetry/bin/poetry run python3 -m state_manager.state_manager --right-pipette P1000-multi-96 0.0.0.0 9999
    )
    ;;

  # Firmware Level

  build-thermocycler-firmware|build-heater-shaker-firmware|build-magdeck-firmware|build-tempdeck-firmware|build-emulator-proxy|build-robot-server|build-common-firmware|build-smoothie|build-can-server)
    monorepo_python -m pip uninstall --yes /dist/*
    (cd /opentrons/shared-data/python && monorepo_python setup.py bdist_wheel -d /dist/)
    (cd /opentrons/api && monorepo_python setup.py bdist_wheel -d /dist/)
    (cd /opentrons/notify-server && monorepo_python setup.py bdist_wheel -d /dist/)
    (cd /opentrons/robot-server && monorepo_python setup.py bdist_wheel -d /dist/)
    (cd /opentrons/hardware && monorepo_python setup.py bdist_wheel -d /dist/)
    monorepo_python -m pip install /dist/*
    ;;

  run-thermocycler-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator thermocycler $OTHER_ARGS"
    ;;
  run-heater-shaker-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator heatershaker $OTHER_ARGS"
    ;;
  run-tempdeck-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator tempdeck $OTHER_ARGS"
    ;;
  run-magdeck-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator magdeck $OTHER_ARGS"
    ;;
  run-robot-server)
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto"
    ;;
  run-emulator-proxy)
    monorepo_python -m opentrons.hardware_control.emulation.app
    ;;
  run-smoothie)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_smoothie"
    ;;
  run-can-server)
    bash -c "monorepo_python -m opentrons_hardware.scripts.sim_socket_can"
    ;;

  *)
    echo "Command ${FULL_COMMAND} not found."
    exit 2
    ;;
esac
