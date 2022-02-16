# CPX Setup Instructions

Below are the instructions for settings up an OT-2 robot-server emulator with your own local source. Connected to it
will be a Heater-Shaker Module, Magnetic Module, Thermocycler Module, and Temperature Module.

1. Follow instructions in README for initial setup
2. Go into `samples/yaml/ot2_local_with_all_modules.yaml` and replace the value for `robot.robot-server-source-location`
   with a path to your mono repo
3. From the root of the repo run `make em-build-amd64 file_path=${PWD}/samples/yaml/ot2_local_with_all_modules.yaml`.
   This will take forever for the intial build, probably around 10 minutes.
4. From the root of the repo run `make em-run file_path=${PWD}/samples/yaml/ot2_local_with_all_modules.yaml`
5. Run `docker exec -it ot2-with-all-modules-otie bash -c "/entrypoint.sh build && /entrypoint.sh run"` to build and
   start your dev server
6. Hit localhost:31950/modules in postman
7. Change something to change the api in the mono repo. For instance I changed `displayName` on get_modules
   in `/opentrons/robot-server/robot_server/service/legacy/routers/modules.py` to `BOOOOOOP`
8. Run `docker exec -it ot2-with-all-modules-otie bash -c "/entrypoint.sh build && /entrypoint.sh run"` to rebuild and
   restart your dev server
9. Hit localhost:31950/modules in postman again
