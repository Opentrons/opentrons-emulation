# Apps and UI Setup Instructions

Below are the instructions for settings up an OT-2 robot-server emulator. Connected to it will be a Heater-Shaker
Module, Magnetic Module, Thermocycler Module, and Temperature Module.

### Initial Setup

Follow [these](https://github.com/Opentrons/opentrons-emulation/blob/main/README.md#initial-configuration) instructions.

### Modify CPX Config

Go into `samples/ot2/ot2_will_all_modules.yaml` and replace the value for `robot.robot-server-source-location` with a
path to your mono repo.

### Build Docker Images

From the root of the repo run
`make build file_path=./samples/ot2/ot2_will_all_modules.yaml`

> This may take 10 or more minutes on initial build.

### Run Emulation

1. From the root of the repo run
   1. `make run-detached file_path=./samples/ot2/ot2_will_all_modules.yaml`

### Make Sure Emulation is Actually Working

Run the following command:

```shell
curl -s --location --request GET 'http://localhost:31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical
```

It should return to you a setup with heater-shaker, thermocycler, temperature, and magnetic modules.
