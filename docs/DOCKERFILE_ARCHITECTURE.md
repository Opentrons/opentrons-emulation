# Dockerfile Architecture

The Dockerfile for `opentrons-emulation` is built with many stages to promote reusing shared resources and to maximize
cache usage when rebuilding images.

The final images can be 1 of 4 types:

- `hardware-local`
- `firmware-local`
- `hardware-remote`
- `firmware-remote`

`hardware` images emulate the physical hardware are based off of c++ firmware code

`firmware` images emulated the firmware and are based off of Python driver code

`local` images expect source code to be bound into the container at the Docker runtime

`remote` images download, build, and run source code at the Docker build time

## Local Image Creation Diagram

```mermaid
stateDiagram-v2

ubuntu_base: ubuntu-base
cpp_base: cpp-base
python_base: python-base
python_base_with_rebuild_script: python-base-with-rebuild-script
cpp_base_with_rebuild_script: cpp-base-with-rebuild-script
hardware_images: hardware-images
firmware_images: firmware-images


state choose_source_base <<choice>>

[*] --> ubuntu_base: Start with ubuntu-base
ubuntu_base --> choose_source_base: Choose source base

choose_source_base --> cpp_base: If hardware image
choose_source_base --> python_base: If firmware image

python_base --> python_base_with_rebuild_script: Add rebuild.sh as entrypoint
cpp_base --> cpp_base_with_rebuild_script: Add rebuild.sh as entrypoint

python_base_with_rebuild_script --> firmware_images: Set env vars
cpp_base_with_rebuild_script --> hardware_images: Set env vars

firmware_images --> [*]
hardware_images --> [*]


```

## Remote Image Creation Diagram

```mermaid
stateDiagram-v2
    direction TB
    
    [*] --> builder: Create builder stages

state builder{

    ubuntu_base: ubuntu-base
    cpp_base: cpp-base
    python_base: python-base
    
    opentrons_modules: opentrons-modules-source
    ot3_firmware: ot3-firmware-source
    opentrons: opentrons-source
    
    heater_shaker_builder: heater-shaker-builder
    thermocycler_builder: thermocycler-builder
    ot3_firmware_builder: ot3-firmware-builder
    python_emulator_builder: python-emulator-builder
    
    state choose_source_base <<choice>>
    state choose_cpp_source <<choice>>
    state choose_modules_builder <<choice>>
    
    [*] --> ubuntu_base: Start with ubuntu-base
    ubuntu_base --> choose_source_base: Choose source base
    choose_source_base --> python_base: If Python source
    python_base --> opentrons: Download opentrons
    opentrons --> python_emulator_builder: Create source code builder
    
    choose_source_base --> cpp_base: If C++ source
    cpp_base --> choose_cpp_source: Choose cpp source repo
    
    choose_cpp_source --> opentrons_modules: Download opentrons-modules
    opentrons_modules --> choose_modules_builder: Choose modules builder
    choose_modules_builder --> thermocycler_builder:  Create source code builder
    choose_modules_builder --> heater_shaker_builder:  Create source code builder
    
    choose_cpp_source --> ot3_firmware: Download ot3-firmware
    ot3_firmware --> ot3_firmware_builder: Create source code builder
}

    [*] --> ubuntu_base_outer: Start with ubuntu base
    
    ubuntu_base_outer: ubuntu-base
    firmware_common: firmware-common
    hardware_images: hardware-images
    firmware_images: firmware-images
    
    ubuntu_base_outer --> hardware_images
    ubuntu_base_outer --> firmware_common
    
    python_emulator_builder --> firmware_common: Copy built source code
    
    firmware_common --> firmware_images: - Run built source code\n- Set env vars
    
    thermocycler_builder --> hardware_images: - Copy built source code\n- Run built source code\n- Set env vars
    heater_shaker_builder --> hardware_images: - Copy built source code\n- Run built source code\n- Set env vars
    ot3_firmware_builder --> hardware_images: - Copy built source code\n- Run built source code\n- Set env vars
    
    firmware_images --> [*]
    hardware_images --> [*]
```
