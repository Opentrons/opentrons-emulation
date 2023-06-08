#!/bin/bash

build_opentrons_modules() {
  (cd /opentrons-modules && cmake --preset=stm32-host-gcc10 .)
}

build_module_simulator() {
  (cd /opentrons-modules && cmake --build ./build-stm32-host -j $(expr $(nproc) - 1) --target $1)
}

echo "Building opentrons-modules"
build_opentrons_modules

echo "Building Heater-Shaker Module simulator"
build_module_simulator "heater-shaker-simulator"

echo "Building Thermocycler Module simulator"
build_module_simulator "thermocycler-gen2-simulator"

echo "Creating simulator directories (If needed)"
mkdir -p \
  /volumes/heater-shaker-executable \
  /volumes/thermocycler-executable

echo "Removing any existing simulators from simulator directories"
rm -f /volumes/heater-shaker-executable/*
rm -f /volumes/thermocycler-executable/*

echo "Copying built simulator files to simulator directories"
cp /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator /volumes/heater-shaker-executable/heater-shaker-simulator
cp /opentrons-modules/build-stm32-host/stm32-modules/thermocycler-gen2/simulator/thermocycler-gen2-simulator /volumes/thermocycler-executable/thermocycler-simulator
