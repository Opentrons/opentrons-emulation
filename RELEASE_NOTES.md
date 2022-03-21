# Opentrons Emulation Release Notes

## v2.1.0 (2022-03-21)

### Bug Fixes

- Fix issue where Docker Images were not building on M1 Mac when running shell in Rosetta
- Fix issue where specifying custom pipettes was not working

### Features

- Add helper CAN Commands to Makefile
- Add automatic building and running to containers with mounted source code
- Add ability to trigger local container rebuilds on with restarting docker containers
- Add ability to specify relative paths
- Generalize build command to support `x86_64` and `arm64` with same command

### Chores

- Add run filters to Github Actions, to prevent unnecessary runs
- Simplify Makefile command naming
- Add Markdown formatter
- Add documentation for the following
  - Clarify python setup documentation
  - Add OT2 Architecture documentation
  - Add Build Artifact Named Volume Architecture documentation
  - Add usage docs for OT3 Firmware development
  - Add usage docs for Apps and UI development
