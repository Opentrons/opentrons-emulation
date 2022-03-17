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

- `robot.source-location` - Absolute path to your `ot3-firmware` repo.
    - Example: `/home/derek-maggio/Documents/repos/ot3-firmware`
- `robot.robot-server-source-location` - Absolute path to your `opentrons` repo.
    - Example: `/home/derek-maggio/Documents/repos/opentrons`
- `robot.can-server-source-location` - Absolute path to your `opentrons` repo.
    - Example: `/home/derek-maggio/Documents/repos/opentrons`

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
make build file_path=./samples/team_specific_setups/ot3_firmware_development.yaml
```

> This may take 10 or more minutes on initial build.

### Run Emulation then Build and Start OT3 Firmware Emulators

1. From the root of the repo run the following command to start the containers.

```shell
make run-detached file_path=./samples/team_specific_setups/ot3_firmware_development.yaml
```

### Make Sure Emulation is Actually Working

1. Open 2 terminals
1. Run CAN monitoring script in the first terminal

```shell
make can-mon file_path=./samples/team_specific_setups/ot3_firmware_development.yaml
```

3. Run CAN communication script in the second terminal

```shell
make can-comm file_path=./samples/team_specific_setups/ot3_firmware_development.yaml
```

4. Select `device_info_request` then `broadcast`
1. You should see output in the `can-mon` terminal

### Rebuilding Changes

```shell
make restart file_path=./samples/team_specific_setups/ot3_firmware_development.yaml
```
