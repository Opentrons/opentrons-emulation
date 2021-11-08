# opentrons-emulation

The `opentrons-emulation` repository contains everything related to building and running
emulated hardware. Currently, it supports the following functionality

[**Emulation Creation**](#emulation-creation) - Create emulated hardware using [Docker](https://www.docker.com/) and 
[Docker Compose](https://docs.docker.com/compose/).

[**Virtual Machine Creation/Provisioning**](#virtual-machine-creation) - 
Create Virtual Machines inside [Virtual Box](https://www.virtualbox.org/) **(Needed for MacOS and Windows users)**

[**Docker Image Upload (Opentrons Employees Only)**](#docker-image-upload) - 
Upload Docker images to [AWS Elastic Container Registry](https://aws.amazon.com/ecr/)

The functionality can be accessed by using the `opentrons-emulation` executable in the root of the repository

## Required Software

### Running in Virtual Machine (MacOS, Windows, Linux)

- [Virtual Box](https://www.virtualbox.org/wiki/Downloads)

### Running Locally (Native Linux Only)

- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Vagrant](https://www.vagrantup.com/downloads)
- [AWS CLI (Opentrons Employees only)](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
  - Opentrons Employees - contact Global Infrastructure about setting up AWS account if you need push access

## Configuration File

The `opentrons-emulation` repository requires that you specify a `configuration.json` file in the root of the
repository. See `configuration_sample.json` for an example. 

**File Format**

- `global-settings` - global settings used by all functionality subsets in the repo
  - `default-folder-paths` - folder paths on your local system
    - `opentrons` - path to the `opentrons` mono repo
    - `ot3-firmware` - path to the `ot3-firmware` repo
    - `modules` - path to the `opentrons-modules` repo
- `emulation-settings` - settings that affect only emulation
  - `source-download-locations` - settings defining where to pull remote source code from
    - `heads` - where to download the latest version of repositories from. 
    (On Github, link can be found by copying the download link)
      - `opentrons` - link to the head of the `opentrons` mono repo
      - `ot3-firmware` - link to the head of the `ot3-firmware` repo
      - `modules` - link to the head of the `opentrons-modules` repo
    - `commits` - template for downloading a specific commit from repo. Use `{{commit-sha}}` variable
    as denote where to insert sha
      - `opentrons` - template for downloading specific commit from the `opentrons` mono repo
      - `ot3-firmware` - template for downloading specific commit from the `ot3-firmware` repo
      - `modules` - template for downloading specific commit from the `opentrons-modules` repo
  - `heater-shaker-settings` - settings pertaining to the Heater-Shaker module
    - `host` - url to socket connection at
    - `port` - port to access socket connection at
- `virtual-machine-settings`
  - `dev-vm-name` - the name for your development vm
  - `prod-vm-name` - the name for your production vm
  - `vm-memory` - the amount of memory in MB to allocate to each vm
  - `vm-cpus` - the number of cpus to allocate to each vm
  - `num-socket-can-networks` - the number of virtual SocketCan networks to create on VM startup


## Emulation Creation

The `emulation (em)` command allows for creating emulated hardware in 2 fashions: 
Production and Development modes

### Production Mode

When working in Production mode, the source for the emulated hardware is downloaded from Github and 
inserted into the Docker image during build time. 

This should be the default use case for any user that is not actively developing
against a container

**Options** 

The following options are supported when using Production mode

- `--dry-run` - Prints commands that will be executed internally by the CLI
- `--detached` - After building and running containers, return control flow to shell
- `--ot3-firmware-repo-sha` - Commit sha to download for `ot3-firmware` repository. Defaults 
to downloading the latest version from the repo
- `--opentrons-modules-repo-sha` - Commit sha to download for `opentrons-modules` repository. Defaults
to downloading the latest version from the repo
- `--opentrons-repo-sha` - Commit sha to download for `opentrons` repository. Defaults
to downloading the latest version from the repo

### Development Mode

When working in Development mode, the source for the emulated hardware is mounted into the container
at runtime. 

This use case is suitable for developers who are actively developing against a container

**Options** 

The following options are supported when using Development mode

- `--dry-run` - Prints commands that will be executed internally by the CLI
- `--detached` - After building and running containers, return control flow to shell
- `--ot3-firmware-repo-path` - Path on host system to `ot3-firmware` repo. Defaults to value provided in
`configuration.json`
- `--opentrons-modules-repo-path` - Path on host system to `opentrons-modules` repo. Defaults to value provided in
`configuration.json`
- `--opentrons-repo-path` - Path on host system to `opentrons` monorepo. Defaults to value provided in
`configuration.json`

### Examples Commands

#### (Production) Latest Versions

System with the latest version of all repos

`./opentrons-emulation emulation prod`

#### (Production) Specific Commit from Repo

Create production system with specific version of `ot3-firmware` repo and latest version of the others

`./opentrons-emulation emulation prod --ot3-firmware-repo-sha="afakereposha"`

#### (Development) Config File Defaults

Create development system with folders specified in `configuration.json` bind-mounted in

`./opentrons-emulation emulation dev`

#### (Production or Development) Detached System

Create production system running in detached mode

`./opentrons-emulation emulation prod --detached`

Create development system running in detached mode

`./opentrons-emulation emulation dev --detached`

#### (Production or Development) Dry Run

Print out commands that will be run internally by CLI to create system

`./opentrons-emulation emulation --dry-run prod`

### Emulators

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


#### OT-2 

**Emulation Level:** Driver

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/)

Currently lives in the [opentrons respository](https://github.com/Opentrons/opentrons).
Needs to be pulled into this repository.

Using [SocketCan](https://en.wikipedia.org/wiki/SocketCAN) we are able to run a virtual OT-3
that behaves like the actual robot.

---

#### Single Container OT-3

**Emulation Level:** Firmware

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/),
[Ubuntu](https://ubuntu.com/) <sup>[3](#ubuntu-requirement)</sup>

The single container OT-3 emulator will have all the firmware running on a single Ubuntu container.
They will be connected through a CAN network that is private to the container.

----

#### Multi Container OT-3

**Emulation Level:** Firmware

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/),
[Ubuntu](https://ubuntu.com/) <sup>[[3]](#ubuntu-requirement)</sup>

The multi container OT-3 emulator will have all the firmware broken out into separate containers.
They will be connected through the host's CAN network.

**Development Images:**
* `ot3-firmware-echo-dev`

**Production Images:**
* `ot3-firmware-echo`

----

#### Heater-Shaker

**Emulation Level:** Firmware

**Requirements:** [Docker](https://docs.docker.com/engine/install/ubuntu/), [Docker Compose](https://docs.docker.com/compose/install/)

**Development Images:**
* `heater-shaker-dev`

**Production Images:**
* `heater-shaker`

----

#### Thermocycler

**Emulation Level:** Driver

----

#### Mag Deck

**Emulation Level:** Driver

----

#### Temp Deck

**Emulation Level:** Driver

----

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
