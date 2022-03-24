# Opentrons Emulation

Opentrons has various software emulations of their hardware. This repository defines a framework to dynamically connect
all these emulators together into systems.

- [Opentrons Emulation](#opentrons-emulation)
    - [What is an Emulator?](#what-is-an-emulator-)
    - [How do the Opentrons Emulators work?](#how-do-the-opentrons-emulators-work-)
    - [Supported Hardware](#supported-hardware)
    - [Required Software](#required-software)
    - [Initial Configuration](#initial-configuration)
    - [Quick Setup](#quick-setup)
        - [OT2 With All Modules](#ot2-with-all-modules)
        - [OT3](#ot3)
    - [Emulation Commands](#emulation-commands)
    - [Building Your Own Configuration Files](#building-your-own-configuration-files)
    - [Setting Up For Local Development](#setting-up-for-local-development)
        - [CPX Setup](#cpx-setup)
        - [OT3 Firmware Development Setup](#ot3-firmware-development-setup)
        - [Apps and UI Setup](#apps-and-ui-setup)
    - [Architecture Diagrams](#architecture-diagrams)

## What is an Emulator?

The simplest description is an emulator is a software model that stands in for a piece of hardware.

In practice, this software model should behave and respond the same way as the hardware it is standing in for. The
software that is connected to the emulator should not know the difference between an emulator and the actual hardware.
It should interact with the emulator in exactly the same manner that it interacts with the hardware.

## How do the Opentrons Emulators work?

The Opentrons emulators are implemented in one of two ways: by emulating at the firmware level or the hardware level.

Firmware Emulation replaces the firmware with a software model and the drivers interact with the model. Note that at
this level, the hardware is also theoretically emulated as well.

Hardware Emulation replaces the hardware itself with a software model and the firmware interacts with the model.

Each piece of hardware you emulate in your system will require you to specify whether you are using `firmware` level
emulation or `hardware` level emulation. See [emulation-level](#emulation-level) for a mapping of hardware to emulation
level.

## Supported Hardware

The following hardware is supported:

- OT2
- OT3
- Thermocycler Module
- Temperature Module
- Magnetic Module
- Heater Shaker Module

**Note: Since we are building from source code the hardware is whatever version the source is. Generally, this means the
latest version. Unless you load a really old version, but no guarantees that a super old version will actually work.**

## Required Software

Install the following software:

1. Docker
    1. [Mac Instructions](https://docs.docker.com/desktop/mac/install/)
        1. Make sure that you have rosetta installed if you are running on an M1 Mac, `softwareupdate --install-rosetta`
    1. [Linux Instructions](https://docs.docker.com/engine/install/#server)
1. Docker-Compose
    1. Mac Instructions: Installed when you install Docker
    1. [Linux Instructions](https://docs.docker.com/compose/install/)
1. [Install Python 3.10](https://www.python.org/downloads/)
   2\. use [pyenv](https://github.com/pyenv/pyenv)

<details>
   <summary>Pyenv Detailed Instructions</summary>

**Setup (Mac)**

1. Navigate to [pyenv docs](https://github.com/pyenv/pyenv)
    1. [Install pyenv using brew](https://github.com/pyenv/pyenv#homebrew-in-macos)
    1. Go to [Basic Github Checkout](https://github.com/pyenv/pyenv#basic-github-checkout) in the pyenv README
    1. Go to Step 2 `Configure your shell's enviornment for Pyenv`
    1. Scroll down to `For Zsh:` section.
    1. Run the `MacOS, if Pyenv is installed with Homebrew` instructions
    1. Restart your terminal
    1. Install [Python Build Dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
    1. Pyenv is now ready to use

**Setup (Linux)**

1. Navigate to [pyenv docs](https://github.com/pyenv/pyenv)
    1. Follow instructions for [Basic Github Checkout](https://github.com/pyenv/pyenv#basic-github-checkout) in the
       pyenv README
        1. In step 2, follow `For Bash` instructions
    1. Restart your terminal
    1. Install [Python Build Dependencies](https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
    1. Pyenv is now ready to use

**Installing Python**

1. Run `pyenv install --list` to get a list of all available Python versions.
    1. Choose the latest 3.10 version. For the purpose of this document we will say the latest version is `3.10.2`
    1. Run `pyenv install 3.10.2` to install Python
    1. Run `pyenv global 3.10.2`  to set the system version to 3.10.2
    1. Verify that you are running the correct Python version by running `pyenv version`
        1. It should say `3.10.2` (set by /something/something/something/pyenv/version)

**Troubleshooting**

_Problem_

When trying to run `pyenv install 3.10.x` you get

```bash
✘ Failed... Something went wrong... python-build: definition not found: 3.10.2
```

_Soulution_

You need to update pyenv. Follow [these](https://github.com/pyenv/pyenv#upgrading) instructions. Then try again.

</details>

4. [Pipenv Installed Globally](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)
    1. Run `python -m ensurepip --upgrade` to install pip
    1. Run `pip install pipenv` to install pipenv

## Initial Configuration

1. In the root of the repository, create to `configuration.json` from `configuration_sample.json`
    1. `cp configuration_sample.json configuration.json`
1. You can leave everything default.
    1. TODO: `global-settings`, `virtual-machine-settings`, and `aws-ecr-settings` will be removed in future releases
1. Run `make setup`

## Quick Setup

Now you have performed the initial configuration lets get an emulated system running.

### OT2 With All Modules

An OT2 with a Heater-Shaker Module, Temperature Module, Thermocycler Module, and a Magnetic Module

> Run the following commands from the root of the repo.

**Build the Docker Images**

```bash
make build file_path=samples/ot2/ot2_with_all_modules.yaml
```

**Start the Emulator**

```bash
make run-detached file_path=samples/ot2/ot2_with_all_modules.yaml
```

**Verify Emulation is Working**

Running the following curl command will hit the /modules endpoint. It should return a JSON describing the attached
modules.

```bash
curl -s --location --request GET 'http://localhost:31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical
```

**Remove Emulation**

```bash
make remove file_path=samples/ot2/ot2_with_all_modules.yaml
```

### OT3

An OT3

> Run the following commands from the root of the repo.

**Build the Docker Images**

```bash
make build file_path=samples/ot3/ot3_remote.yaml
```

**Start the Emulator**

```bash
`make run-detached file_path=samples/ot3/ot3_remote.yaml
```

**Verify Emulation is Working**

Open a CAN bus monitor in another terminal

```bash
make can-mon file_path=samples/ot3/ot3_remote.yaml
```

## Makefile Commands

Go to [MAKEFILE_COMMANDS.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/MAKEFILE_COMMANDS.md)

## Building Your Own Configuration Files

To run an emulated system you need to create an emulation system configuration file. This can either be a JSON file or a
YAML file. You can create a single robot and unlimited number of modules in a single configuration, although neither are
required.

The `samples` directory contains samples of YAML configurations.

If you want to create you own files go
to [EMULATION_CONFIGURATION_FILE_KEY_DEFINITIONS.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/EMULATION_CONFIGURATION_FILE_KEY_DEFINITIONS.md)
for definitions of all the options and examples of more complex setups.

## Setting Up For Local Development

### CPX Setup

Go to [CPX_SETUP.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/team_specific_setup/CPX_SETUP.md)

### OT3 Firmware Development Setup

Go
to [OT3_FIRMWARE_DEVELOPMENT_SETUP.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/team_specific_setup/OT3_FIRMWARE_DEVELOPMENT_SETUP.md)

### Apps and UI Setup

Go
to [APPS_AND_UI_SETUP.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/team_specific_setup/APPS_AND_UI_SETUP.md)

## Architecture Diagrams

For more information on how containers are connected to one another and how they communicated refer to
[ARCHITECTURE.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/ARCHITECTURE.md)

For information on the Docker build process refer
to [DOCKERFILE_ARCHITECTURE.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/DOCKERFILE_ARCHITECTURE.md)

## Github Action

For information on this repository's Github Action refer
to [GITHUB_ACTION_DOCS.md](https://github.com/Opentrons/opentrons-emulation/blob/main/docs/GITHUB_ACTION_DOCS.md)
