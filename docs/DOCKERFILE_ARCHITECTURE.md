# Dockerfile Architecture

The Dockerfile for `opentrons-emulation` is built with many stages to promote reusing shared resources and to maximize
cache usage when rebuilding images.

The final images can be 1 of 4 types:

- `hardware-local`
- `firmware-local`
- `hardware-remote`
- `firmware-remote`

### ubuntu-base

`ubuntu-base`, the lowest level image for `opentrons-emulation`, is based off of Ubuntu 20.04 and contains dependencies
required by all all images.

### cpp-base

`cpp-base` is built on top of `ubuntu-base` and contains dependencies for building our C++ firmware
inside [ot3-firmware](https://github.com/Opentrons/ot3-firmware) and
[opentrons-modules](https://github.com/Opentrons/opentrons-modules)

### python-base

`python-base` is build on top of `ubuntu-base` and contains dependencies for building our
[python monorepo](https://github.com/Opentrons/opentrons)

## Local Image Creation

```mermaid
stateDiagram-v2

ub: ubuntu-base
cpp: cpp-base
python: python-base
base_with_rebuild_script: base-with-rebuild-script
add_env_vars: local-image


state choose_source_base <<fork>>
state join <<join>>

[*] --> ub: Start with ubuntu-base
ub --> choose_source_base: Choose source base

choose_source_base --> cpp: If C++ source
choose_source_base --> python: If Python source

python --> join
cpp --> join

join --> base_with_rebuild_script: Add rebuild.sh as entrypoint

base_with_rebuild_script --> add_env_vars: Add env vars
add_env_vars --> [*]: Finished building
```

## Remote Image Creation

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
