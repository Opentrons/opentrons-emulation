# Opentrons Emulation Release Notes

## v2.3.3 (2022-08-12)

### Bug Fixes

- Fix load-container-names Makefile command [\[PR #172\]](https://github.com/Opentrons/opentrons-emulation/pull/172)

### Features

- Firmware Level Heater-Shaker Emulation [\[PR #173\]](https://github.com/Opentrons/opentrons-emulation/pull/173)

### Chores

- None

## v2.3.2 (2022-07-08)

### Bug Fixes

- Update python dependency caching [\[PR #169\]](https://github.com/Opentrons/opentrons-emulation/pull/169)

### Features

- None

### Chores

- Update
  README [\[PR #166\]](https://github.com/Opentrons/opentrons-emulation/pull/166) [\[PR #170\]](https://github.com/Opentrons/opentrons-emulation/pull/170)

## v2.3.1 (2022-04-01)

### Bug Fixes

- Fix breaking caches in Github Actions [\[PR #162\]](https://github.com/Opentrons/opentrons-emulation/pull/162)

### Features

- None

### Chores

- Update pipenv and pyenv steps in README [\[PR #161\]](https://github.com/Opentrons/opentrons-emulation/pull/161)

## v2.3.0 (2022-04-01)

### Bug Fixes

- None

### Features

- Add image caching with Github Container
  Registry [\[PR #157\]](https://github.com/Opentrons/opentrons-emulation/pull/157)

### Chores

- None

## v2.2.0 (2022-03-29)

### Bug Fixes

- Fix Github cache invalidation when there are changes only to Makefile
  [\[PR #146\]](https://github.com/Opentrons/opentrons-emulation/pull/146)
- Fix broken README link
  [\[PR #143\]](https://github.com/Opentrons/opentrons-emulation/pull/143)
  [\[PR #145\]](https://github.com/Opentrons/opentrons-emulation/pull/145)

### Features

- Add bootloader to OT3 emulation [\[PR #130\]](https://github.com/Opentrons/opentrons-emulation/pull/130)
- Add gripper to OT3 emulation [\[PR #132\]](https://github.com/Opentrons/opentrons-emulation/pull/132)
- Add nightly OT3 integration testing against emulation
  [\[PR #131\]](https://github.com/Opentrons/opentrons-emulation/pull/131)
  [\[PR #133\]](https://github.com/Opentrons/opentrons-emulation/pull/133)
  [\[PR #134\]](https://github.com/Opentrons/opentrons-emulation/pull/134)
  [\[PR #139\]](https://github.com/Opentrons/opentrons-emulation/pull/139)
  [\[PR #151\]](https://github.com/Opentrons/opentrons-emulation/pull/151)
- Run cmake multithreaded to speed up build time
  [\[PR #153\]](https://github.com/Opentrons/opentrons-emulation/pull/153)
  [\[PR #141\]](https://github.com/Opentrons/opentrons-emulation/pull/141)

### Chores

- Handle new pipette paths for OT3 [\[PR #135\]](https://github.com/Opentrons/opentrons-emulation/pull/135)
- Update pipenv
  [\[PR #136\]](https://github.com/Opentrons/opentrons-emulation/pull/136)
  [\[PR #142\]](https://github.com/Opentrons/opentrons-emulation/pull/142)
- Add Dockerfile architecture diagram [\[PR #138\]](https://github.com/Opentrons/opentrons-emulation/pull/138)
- Add Github Action usage docs [\[PR #140\]](https://github.com/Opentrons/opentrons-emulation/pull/140)
- Update Github Action filtering to only run when necessary
  [\[PR #144\]](https://github.com/Opentrons/opentrons-emulation/pull/144)
  [\[PR #147\]](https://github.com/Opentrons/opentrons-emulation/pull/147)
  [\[PR #148\]](https://github.com/Opentrons/opentrons-emulation/pull/148)
- Add status badges to README [\[PR #150\]](https://github.com/Opentrons/opentrons-emulation/pull/150)
- Add release workflow documentation [\[PR #150\]](https://github.com/Opentrons/opentrons-emulation/pull/152)
- Add Thermocycler Gen2 support [\[PR #154\]](https://github.com/Opentrons/opentrons-emulation/pull/152)

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
