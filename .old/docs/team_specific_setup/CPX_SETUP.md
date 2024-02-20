# CPX Setup Instructions

Below are the instructions for settings up an OT-2 robot-server emulator with your own local source. Connected to it
will be a Heater-Shaker Module, Magnetic Module, Thermocycler Module, and Temperature Module.

### Initial Setup

Follow [these](https://github.com/Opentrons/opentrons-emulation/blob/main/README.md#initial-configuration) instructions.

### Modify CPX Config

Go into `samples/team_specific_setups/cpx_ot2.yaml` and replace the value for `robot.robot-server-source-location` with
a path to your mono repo.

### Build Docker Images

From the root of the repo run
`make build file_path=./samples/team_specific_setups/cpx_ot2.yaml`

> This may take 10 or more minutes on initial build.

### Run Emulation then Build and Start Robot Server

From the root of the repo run

```bash
make run-detached file_path=./samples/team_specific_setups/cpx_ot2.yaml
```

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

Run `make restart file_path=./samples/team_specific_setups/cpx_ot2.yaml` to rebuild and restart your dev server.

### Verify Changes Took Effect

Run the following command again:

```shell
curl -s --location --request GET 'http://localhost:31950/modules' --header 'opentrons-version: *' | json_pp -json_opt pretty,canonical
```

It should return to you a setup with heater-shaker, thermocycler, temperature, and magnetic modules. Make sure the
displayName value changed.
