# CPX Setup Instructions

Below are the instructions for settings up an OT-2 robot-server emulator with your own local source. Connected to it
will be a Heater-Shaker Module, Magnetic Module, Thermocycler Module, and Temperature Module.

### Initial Setup

Follow [these](https://github.com/Opentrons/opentrons-emulation/blob/main/README.md#initial-configuration) instructions.

### Modify CPX Config

Go into `samples/team_specific_setups/cpx_ot2.yaml` and replace the value for `robot.robot-server-source-location` with
a path to your mono repo.

### Build Docker Images

From the root of the repo run `make em-build-amd64 file_path=${PWD}/samples/team_specific_setups/cpx_ot2.yaml`.

This will take forever for the intial build, probably around 10 minutes.

### Run Emulation

From the root of the repo run `make em-run-detached file_path=${PWD}/samples/team_specific_setups/cpx_ot2.yaml`.

### Build and Start Robot Server

Run `docker exec -it ot2-with-all-modules-otie bash -c "/entrypoint.sh build && /entrypoint.sh run"` to build and start
your dev server.

*Note: This step is necessary because we bound our monorepo code into the robot-server emulator. It is up to*
*the user to execute the build and run of any containers they have their local source bound into.*

### Make Sure Emulation is Actually Working

Hit localhost:31950/modules in postman. It should return to you a setup with heater-shaker, thermocycler, temperature,
and magnetic modules.

### Change Something on the Robot Server

Now we want to verify that we can cascade changes from our local monorepo to the emulated robot server.

Change `displayName` on get_modules in `/opentrons/robot-server/robot_server/service/legacy/routers/modules.py`
to `BOOOOOOP`.

### Rebuild and Run

Run `docker exec -it ot2-with-all-modules-otie bash -c "/entrypoint.sh build && /entrypoint.sh run"` to rebuild and
restart your dev server.

### Verify Changes Took Effect

Hit localhost:31950/modules in postman again. Make sure the displayName value changed.
