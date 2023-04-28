#!/bin/bash

# OPENTRONS_HARDWARE is an env variable that is passed to every container
OTHER_ARGS=`echo "${@:2}"`
case $OPENTRONS_HARDWARE in
  heater-shaker-hardware)
    pkill -f "/heater-shaker-simulator"
    bash -c "/heater-shaker-simulator $OTHER_ARGS"
    ;;
  thermocycler-hardware)
    pkill -f "/thermocycler-gen2-simulator"
    bash -c "/thermocycler-gen2-simulator $OTHER_ARGS"
    ;;
  ot3-pipettes-hardware)
    pkill -f "/executable/pipettes-simulator"
    /executable/pipettes-simulator
    ;;
  ot3-head-hardware)
    pkill -f "/executable/head-simulator"
    /executable/head-simulator
    ;;
  ot3-gantry-x-hardware)
    pkill -f "/executable/gantry-x-simulator"
    /executable/gantry-x-simulator
    ;;
  ot3-gantry-y-hardware)
    pkill -f "/executable/gantry-y-simulator"
    /executable/gantry-y-simulator
    ;;
  ot3-bootloader-hardware)
    pkill -f "/executable/bootloader-simulator"
    /executable/bootloader-simulator
    ;;
  ot3-gripper-hardware)
    pkill -f "/executable/gripper-simulator"
    /executable/gripper-simulator
    ;;
  ot3-state-manager)
    # 9999 is the hardcoded state manager port
    pkill -f "state_manager_python -m state_manager.state_manager"
    state_manager_python -m state_manager.state_manager --right-pipette P1000-multi-96 0.0.0.0 9999
    ;;
  thermocycler-firmware)
    pkill -f "run_module_emulator"
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator thermocycler $OTHER_ARGS"
    ;;
  heater-shaker-firmware)
    pkill -f "run_module_emulator"
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator heatershaker $OTHER_ARGS"
    ;;
  tempdeck-firmware)
    pkill -f "run_module_emulator"
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator tempdeck $OTHER_ARGS"
    ;;
  magdeck-firmware)
    pkill -f "run_module_emulator"
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_module_emulator magdeck $OTHER_ARGS"
    ;;
  robot-server)
    pkill -f "uvicorn"
    bash -c "uvicorn "robot_server:app" --host 0.0.0.0 --port 31950 --ws wsproto"
    ;;
  emulator-proxy)
    pkill -f "emulation.app"
    monorepo_python -m opentrons.hardware_control.emulation.app
    ;;
  smoothie)
    pkill -f "run_smoothie"
    bash -c "monorepo_python -m opentrons.hardware_control.emulation.scripts.run_smoothie"
    ;;
  can-server)
    pkill -f "sim_socket_can"
    bash -c "monorepo_python -m opentrons_hardware.scripts.sim_socket_can"
    ;;
  *)
    echo "Command ${OPENTRONS_HARDWARE} not found."
    exit 2
    ;;
esac
