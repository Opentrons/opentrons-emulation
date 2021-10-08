# opentrons-emulation

The `opentrons-emulation` repository contains software emulations of Opentron's various
pieces of hardware using [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

## Emulators

The following emulators are planned to be included:

| Hardware                                        | Emulation Level <sup>[1](#emulation-level)</sup> | Status               |
|-------------------------------------------------|----------------------------------------------------|----------------------|
| [OT-2](#ot-2)                                   | Driver                                             | Awaiting Development |
| [Single Container OT-3](#single-container-ot-3) | Firmware                                           | Awaiting Development |
| [Multi Container OT-3](#multi-container-ot-3)   | Firmware                                           | Work in Progress     |
| [Heater Shaker](#heater-shaker)                 | Firmware                                           | Work in Progress     |
| [Thermocycler](#thermocycler)                   | Firmware <sup>[2](#thermocycler-note)</sup>      | Awaiting Development |
| [Temp Deck](#temp-deck)                         | Driver                                             | Awaiting Development |
| [Mag Deck](#mag-deck)                           | Driver                                             | Awaiting Development |


### OT-2 

**Emulation Level:** Driver

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/)

Currently lives in the [opentrons respository](https://github.com/Opentrons/opentrons).
Needs to be pulled into this repository.

Using [SocketCan](https://en.wikipedia.org/wiki/SocketCAN) we are able to run a virtual OT-3
that behaves like the actual robot.

### Single Container OT-3

**Emulation Level:** Firmware

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/),
[Ubuntu](https://ubuntu.com/) <sup>[3](#ubuntu-requirement)</sup>

The single container OT-3 emulator will have all the firmware running on a single Ubuntu container.
They will be connected through a CAN network that is private to the container.

### Multi Container OT-3

**Emulation Level:** Firmware

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/),
[Ubuntu](https://ubuntu.com/) <sup>[[3]](#ubuntu-requirement)</sup>

The multi container OT-3 emulator will have all the firmware broken out into separate containers.
They will be connected through the host's CAN network.

**Development Images:**
* `ot3-firmware-echo-dev`

**Production Images:**
* `ot3-firmware-echo`

### Heater-Shaker

**Emulation Level:** Firmware

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/)

**Development Images:**
* `heater-shaker-dev`

**Production Images:**
* `heater-shaker`

### Thermocycler

**Emulation Level:** Driver

### Mag Deck

**Emulation Level:** Driver

### Temp Deck

**Emulation Level:** Driver

## Usage

Using this repository consists of 2 steps:

1. Creating Containers 
2. Building and running firmware inside containers

Currently, there are 2 different container configurations offered: `production` and `development`

### Production Configuration

The production configuration handles downloading the necessary source code and inserting
it into each container's Dockerfile. It also builds and runs the emulator inside each container.

### Development Configuration

The development configuration allows you to mount your source code into each of your
repositories. It also mounts the `entrypoint.sh` file into each container. This allows
you to have control over building and running your changes.

#### Environment File

You must specify an `.env` file. This file will configure your containers to your system. You will
have to specify the following variables. See `.env.default` file in this repo for an example.

`OT3_FIRMWARE_DIRECTORY`
* Used In - Development Configuration
* Description - Absolute path to your ot3-firmware source code 
* Example - `"${HOME}/Documents/repos/ot3-firmware"`

`OPENTRONS_MODULES_DIRECTORY`
* Used In - Development Configuration
* Description - Absolute path to your opentrons-modules source code
* Example - `"${HOME}/Documents/repos/opentrons-modules"`

`HEATER_SHAKER_SOCKET_HOST`
* Used In - Production Configuration
* Description - Host to connect socket to
* Example - `"127.0.0.1"`

`HEATER_SHAKER_SOCKET_PORT`
* Used In - Production Configuration
* Description - Port to connect socket to 
* Example - `"9999"`

### Creating System

To create systems use the `create_system.sh` script inside of the `scripts` directory.

#### Production System

To run a production system configuration run the base script.

`./create_system.sh --prod`

#### Development System

To run a development system configuration add the `--dev` option.

`./create_system.sh --dev`

#### Headless

Both Production and Development systems can be run in the background. 
To do this add the `--headless` option.

`./create_system.sh --dev --headless` -OR- `./create_system.sh --prod --headless`

#### Specifying Commit Sha

Production systems can be run from spefic commit shas that are on Github. 
To do this, specify `--ot3-firmware-sha` for ot3-firwamre or `--modules-sha` for opentrons-modules.

#### Example Commands

```shell
# Create a production system.
# Uses the latest commit from the master branch of both ot3-firmware and opentrons-modules
./run_emulation.sh

# Create same production system as above but run it in the background
./run_emulation.sh --headless

# Create production system, pull specific commit for ot3-firmware
./run_emulation.sh \
  --prod \
  --headless \
  --ot3-firmware-sha 7ec96029946054c9b6d55846bd5e909b55591adb

# Create production system, pull specific commit for opentrons-modules
./run_emulation.sh \
  --prod \
  --headless \
  --modules-sha 80f30ad3f99a7bbc22ec885371c592013a7cbe6c

# Create production system, pull specific commit for opentrons-modules and ot3-firmware
./run_emulation.sh \
  --prod \
  --headless \
  --ot3-firmware-sha 7ec96029946054c9b6d55846bd5e909b55591adb \
  --modules-sha 80f30ad3f99a7bbc22ec885371c592013a7cbe6c
  
# Create headless dev system. Will look at .env file for where to pull source code
./run_emulation.sh --dev
```

### Building and Running

Each container gets the `entrypoint.sh` script. This script supports both building and running
each container's respective software. To run this script directly you must do the following:

1. Open an interactive terminal in your container with `docker exec -it <container_name> bash`
2. Run `/entrypoint.sh build` or `entrypoint run <optional_args>...`

To avoid having to open an interactive terminal everytime you want to build the
scripts inside of `scripts/docker_convenience_scripts` have been provided. 

* Build - `./build.sh <container_name>`
* Run - `./run.sh <container_name> <optional_args>...`
* Build & Run - `./build_and_run.sh <container_name> <optional_args>...`

#### Heater Shaker Specific Run Args

When running the Heater-Shaker emulator you need to specify the runtime configuration. 
The emulator can either accept input from stdin or a socket. 

To run using stdin, execute the following command:

`./run.sh <heater-shaker-container> --stdin`

To run using a socket, execute the following command:

`./run.sh <heater-shaker-container> --socket "http://<your_host>:<your_port>"`

`./run.sh <heater-shaker-container> --socket "http://127.0.0.1:9999"`

## Github Action
This repository provides a Github Action to spin up the emulators in other repositories.
For an example, see [this action in ot3-firmware](https://github.com/Opentrons/ot3-firmware/blob/main/.github/workflows/run_emulation.yaml).

## Footnotes

### Emulation Level

**TL:DR** - Firmware level emulator more closely emulates a piece of hardware than driver level does. 

Emulators can either be at the `Driver` level or the `Firmware` level. Driver level emulators
cover the stack from driver level and up. Firmware level emulators cover the stack from firmware
level and up.

### Thermocycler Note

The thermocycler is in a "refresh" cycle to be updated to use a STM32 board. 
When that happens it can be emulated at the firmware level

### Ubuntu Requirement

For running either OT-3 a system running [Ubuntu](https://ubuntu.com/) is required.
This is due to the usage of the [SocketCan](https://en.wikipedia.org/wiki/SocketCAN) library
which is part of the Linux kernel.

To meet this requirement, you can also create a virtual machine installed on [VirtualBox](https://www.virtualbox.org/)
