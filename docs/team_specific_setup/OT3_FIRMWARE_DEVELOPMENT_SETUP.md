# OT3 Firmware Development Setup Instructions

Below are the instructions for settings up an OT-3 robot-server emulator with your own local source.

### Requirements

This configuration requires that you have [the opentrons repo](https://github.com/Opentrons/opentrons) and
[the ot3-firmware repo](https://github.com/Opentrons/ot3-firmware) downloaded locally to your system.

### Initial Setup

Follow [these](https://github.com/Opentrons/opentrons-emulation/blob/main/README.md#initial-configuration) instructions.

### Modify Configuration file

Go into `samples/team_specific_setups/ot3_firmware_development.yaml` and replace the following values with paths to the
**_TOP_** level of your repos:

* `robot.source-location` - Absolute path to your `ot3-firmware` repo.
    * Example: `/home/derek-maggio/Documents/repos/ot3-firmware`
* `robot.robot-server-source-location` - Absolute path to your `opentrons` repo.
    * Example: `/home/derek-maggio/Documents/repos/opentrons`
* `robot.can-server-source-location` - Absolute path to your `opentrons` repo.
    * Example: `/home/derek-maggio/Documents/repos/opentrons`

Your configuration should look something like the following:

```yaml
system-unique-id: ot3-only
robot:
  id: otie
  hardware: ot3
  source-type: local
  source-location: /home/derek-maggio/Documents/repos/ot3-firmware
  robot-server-source-type: local
  robot-server-source-location: /home/derek-maggio/Documents/repos/opentrons
  can-server-source-type: local
  can-server-source-location: /home/derek-maggio/Documents/repos/opentrons
  emulation-level: hardware
  exposed-port: 31950
```

### Build Docker Images

From the root of the repo run

```
Intel: make build-amd64 file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
Mac M1: make build-arm64 file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

> This may take 10 or more minutes on initial build.

### Run Emulation then Build and Start OT3 Firmware Emulators

1. From the root of the repo run the following command to start the containers.

```shell
make run-detached file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

2. Then run the following command to run builds inside containers with source code mounted into them.

```shell
make local-rebuild-all file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

> Note: This second step is necessary because we bound our source code into the emulators. It is up to the user to execute the build and run of any containers they have their local source bound into.

### Make Sure Emulation is Actually Working

Run the following command:

```shell
make can-comm file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml
```

This will run
the [can_comm.py](https://github.com/Opentrons/opentrons/blob/edge/hardware/opentrons_hardware/scripts/can_comm.py)
script. Run some commands to make sure communication is working correctly

### Change Something in the Firmware

Now we want to verify that we can cascade changes from our local monorepo to the emulated robot server.

Change `displayName` on get_modules in `/opentrons/robot-server/robot_server/service/legacy/routers/modules.py`
to `BOOOOOOP`.

### Rebuild and Run

Run `make local-rebuild-firmware file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml` to rebuild
and restart your dev server.

> Note: We are only rebuilding firmware here because we only made changes to the firmware.

### Verify Changes Took Effect

Run the following command again:

```shell
curl -s --location --request GET 'http://localhost:31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical
```

It should return to you a setup with heater-shaker, thermocycler, temperature, and magnetic modules. Make sure the
displayName value changed.
