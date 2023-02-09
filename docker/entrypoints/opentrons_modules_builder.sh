#!/bin/bash

build_module_simulator() {
  (cd /opentrons-modules && cmake --preset=stm32-host-gcc10 . && cmake --build ./build-stm32-host -j $(expr $(nproc) - 1) --target $1)
}

build_module_simulator "heater-shaker-simulator"
build_module_simulator "thermocycler-gen2-simulator"

mkdir -p \
  /volumes/heater_shaker_volume \
  /volumes/thermocycler_volume

cp /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator /volumes/heater_shaker_volume/heater-shaker-simulator
cp /opentrons-modules/build-stm32-host/stm32-modules/thermocycler-gen2/simulator/thermocycler-gen2-simulator /volumes/thermocycler_volume/thermocycler-simulator
