#!/bin/bash

# Build all simulators in ot3-firmware
# Create a directory for each simulator to live
# On local-ot3-firwmare-builder container create a volume for each simulator and bind each simulator directory to it
# On each OT-3 Firmware emulator container attach its respective volume

echo "Building ot3-firmware"
(
  cd /ot3-firmware && \
  cmake --preset host-gcc10
)

echo "Building subsystem simulator files"
(
  cd /ot3-firmware && \
  cmake --build ./build-host -j $(expr $(nproc) - 1)
)

echo "Building ot3-firmware State Manager"
(
  cd /ot3-firmware && \
  cmake --build --preset tests --target state-manager-build
)


echo "Creating directories (If needed)"
mkdir -p \
  /volumes/bootloader-executable \
  /volumes/gantry-x-executable \
  /volumes/gantry-y-executable \
  /volumes/gripper-executable \
  /volumes/gripper-eeprom \
  /volumes/head-executable \
  /volumes/left-pipette-executable \
  /volumes/left-pipette-eeprom \
  /volumes/right-pipette-executable \
  /volumes/right-pipette-eeprom \
  /volumes/state-manager-dist \
  /volumes/state-manager-venv 

echo "Removing any files from directories"
rm -f /volumes/bootloader-executable/*
rm -f /volumes/gantry-x-executable/*
rm -f /volumes/gantry-y-executable/*
rm -f /volumes/gripper-executable/*
rm -f /volumes/gripper-eeprom/*
rm -f /volumes/head-executable/*
rm -f /volumes/left-pipette-executable/*
rm -f /volumes/left-pipette-eeprom/*
rm -f /volumes/right-pipette-executable/*
rm -f /volumes/right-pipette-eeprom/*
rm -rf /volumes/state-manager-dist/*
rm -rf /volumes/state-manager-venv/*

echo "Copying built simulator files to simulator directories"
cp -r /ot3-firmware/build-host/.venv/* /volumes/state-manager-venv/
cp -r /ot3-firmware/build-host/pipettes/simulator/*-simulator /volumes/left-pipette-executable/
cp -r /ot3-firmware/build-host/pipettes/simulator/*-simulator /volumes/right-pipette-executable/
cp -r /ot3-firmware/state_manager/dist/* /volumes/state-manager-dist/
cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /volumes/bootloader-executable/bootloader-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /volumes/gantry-x-executable/gantry-x-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /volumes/gantry-y-executable/gantry-y-simulator
cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /volumes/gripper-executable/gripper-simulator
cp /ot3-firmware/build-host/head/simulator/head-simulator /volumes/head-executable/head-simulator

mkdir -p /opentrons_hardware_dist
/selective_monorepo_builder.sh "/opentrons_hardware_dist" "shared-data/python" "api" "notify-server" "hardware"
monorepo_python -m pip install --force-reinstall /opentrons_hardware_dist/*
monorepo_python -m opentrons_hardware.scripts.emulation_pipette_provision