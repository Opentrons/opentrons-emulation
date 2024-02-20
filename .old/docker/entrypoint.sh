#!/bin/bash

# OPENTRONS_HARDWARE is an env variable that is passed to every container
case $OPENTRONS_HARDWARE in
  heater-shaker-hardware)
    bash -c "/executable/heater-shaker-simulator $MODULE_ARGS"
    ;;
  thermocycler-hardware)
    bash -c "/executable/thermocycler-simulator $MODULE_ARGS"
    ;;
  ot3-pipettes-hardware)
    if [ -n "$SIMULATOR_NAME" ]; then
      bash -c "/executable/${SIMULATOR_NAME}"
    fi
    ;;
  ot3-head-hardware)
    /executable/head-simulator
    ;;
  ot3-gantry-x-hardware)
    /executable/gantry-x-simulator
    ;;
  ot3-gantry-y-hardware)
    /executable/gantry-y-simulator
    ;;
  ot3-bootloader-hardware)
    /executable/bootloader-simulator
    ;;
  ot3-gripper-hardware)
    /executable/gripper-simulator
    ;;
  ot3-state-manager)
    # 9999 is the hardcoded state manager port
    (
      cd /ot3-firmware/state_manager && \
      ../stm32-tools/poetry/bin/poetry run python3 -m state_manager.state_manager --right-pipette P1000-multi-96 0.0.0.0 9999
    )
    ;;
  thermocycler-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator thermocycler $MODULE_ARGS"
    ;;
  heater-shaker-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator heatershaker $MODULE_ARGS"
    ;;
  tempdeck-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator tempdeck $MODULE_ARGS"
    ;;
  magdeck-firmware)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator magdeck $MODULE_ARGS"
    ;;
  robot-server)
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto"
    ;;
  emulator-proxy)
    monorepo_python -m opentrons.hardware_control.emulation.app
    ;;
  smoothie)
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_smoothie"
    ;;
  can-server)
    bash -c "monorepo_python -m opentrons_hardware.scripts.sim_socket_can"
    ;;
  *)
    echo "Command ${OPENTRONS_HARDWARE} not found."
    exit 2
    ;;
esac
