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

From the root of the repo run Intel
`make em-build-amd64 file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml`
M1
`make em-build-arm64 file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml`

> This may take 10 or more minutes on initial build.

### Run Emulation then Build and Start OT3 Firmware Emulators

1. From the root of the repo run
    1. `make em-run-detached file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml`
    2. `make em-local-rebuild-firmware-only file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml`

> Note: This second step is necessary because we bound our source code into the emulators. It is up to the user to execute the build and run of any containers they have their local source bound into.*

> Note: We only built and ran the firmware emulators. This is intentional.

### Make Sure Emulation is Actually Working

Run the following command:

```shell
curl -s --location --request GET 'http://localhost:31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical
```

It should return to you a setup with heater-shaker, thermocycler, temperature, and magnetic modules.

### Change Something on the Robot Server

Now we want to verify that we can cascade changes from our local monorepo to the emulated robot server.

Change `displayName` on get_modules in `/opentrons/robot-server/robot_server/service/legacy/routers/modules.py`
to `BOOOOOOP`.

### Rebuild and Run

Run `make em-local-rebuild file_path=${PWD}/samples/team_specific_setups/ot3_firmware_development.yaml` to rebuild and
restart your dev server.

### Verify Changes Took Effect

Run the following command again:

```shell
curl -s --location --request GET 'http://localhost:31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical
```

It should return to you a setup with heater-shaker, thermocycler, temperature, and magnetic modules. Make sure the
displayName value changed.
