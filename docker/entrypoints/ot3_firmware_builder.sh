#!/bin/bash

# Build all simulators in ot3-firmware
# Create a directory for each simulator to live
# On local-ot3-firwmare-builder container create a volume for each simulator and bind each simulator directory to it
# On each OT-3 Firmware emulator container attach its respective volume

echo "Building ot3-firmware"

(
  cd /ot3-firmware && \
  cmake --preset host-gcc10 && \
  cmake --build ./build-host -j $(expr $(nproc) - 1)
)

echo "Creating simulator directories"

mkdir -p \
  /volumes/pipettes_volume \
  /volumes/head_volume \
  /volumes/gantry_x_volume \
  /volumes/gantry_y_volume \
  /volumes/gantry_y_volume \
  /volumes/bootloader_volume \
  /volumes/gripper_volume \
  /volumes/state_manager_venv

echo "Copying simulator files to simulator directories"

rm -f /volumes/pipettes_volume/pipettes-simulator
rm -f /volumes/head_volume/head-simulator
rm -f /volumes/gantry_x_volume/gantry-x-simulator
rm -f /volumes/gantry_y_volume/gantry-y-simulator
rm -f /volumes/bootloader_volume/bootloader-simulator
rm -f /volumes/gripper_volume/gripper-simulator
rm -rf /volumes/state_manager_venv/

cp /ot3-firmware/build-host/pipettes/simulator/pipettes-single-simulator /volumes/pipettes_volume/pipettes-simulator
cp /ot3-firmware/build-host/head/simulator/head-simulator /volumes/head_volume/head-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /volumes/gantry_x_volume/gantry-x-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /volumes/gantry_y_volume/gantry-y-simulator
cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /volumes/bootloader_volume/bootloader-simulator
cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /volumes/gripper_volume/gripper-simulator
cp -r /ot3-firmware/build-host/.venv /volumes/state_manager_venv/
