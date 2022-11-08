#!/bin/bash

(
  cd /ot3-firmware && \
  cmake --preset host-gcc10 && \
  cmake --build ./build-host -j $(expr $(nproc) - 1)
)

mkdir -p \
  /volumes/pipettes_volume \
  /volumes/head_volume \
  /volumes/gantry_x_volume \
  /volumes/gantry_y_volume \
  /volumes/gantry_y_volume \
  /volumes/bootloader_volume \
  /volumes/gripper_volume

cp /ot3-firmware/build-host/pipettes/simulator/pipettes-single-simulator /volumes/pipettes_volume/pipettes-simulator
cp /ot3-firmware/build-host/head/simulator/head-simulator /volumes/head_volume/head-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-x-simulator /volumes/gantry_x_volume/gantry-x-simulator
cp /ot3-firmware/build-host/gantry/simulator/gantry-y-simulator /volumes/gantry_y_volume/gantry-y-simulator
cp /ot3-firmware/build-host/bootloader/simulator/bootloader-simulator /volumes/bootloader_volume/bootloader-simulator
cp /ot3-firmware/build-host/gripper/simulator/gripper-simulator /volumes/gripper_volume/gripper-simulator
