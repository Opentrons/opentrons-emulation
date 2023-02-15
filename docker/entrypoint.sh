#!/bin/bash

OTHER_ARGS=`echo "${@:2}"`

# OPENTRONS_HARDWARE is an env variable that is passed to every container
case $OPENTRONS_HARDWARE in

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
    echo "Command ${OPENTRONS_HARDWARE} not found."
    exit 2
    ;;
esac
