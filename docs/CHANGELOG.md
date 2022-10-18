# Opentrons Emulation Changelog

## v3.0.0 (2022-10-18)

### :rotating_light: Breaking Changes :rotating_light:

- All `robot` blocks of type `ot3` now require `opentrons-hardware-source-location` and
  `opentrons-hardware-source-type` fields.

### Bug Fixes

- Fix `load-container-names` Makefile command [\[PR #172\]](https://github.com/Opentrons/opentrons-emulation/pull/172)
- Fix not appending `local-network` to local network name when `system_unique_id`
  exists. [\[PR #185\]](https://github.com/Opentrons/opentrons-emulation/pull/185)
- Fix `can-mon` and `can-comm` Makefile
  commands [\[PR #197\]](https://github.com/Opentrons/opentrons-emulation/pull/197)
- Fix broken "Test Sample Files" Github Action [\[PR #200\]](https://github.com/Opentrons/opentrons-emulation/pull/200)
- Fix OT-3 gripper and pipette containers not starting due to `EEPROM_FILENAME` environment variable not being set
  [\[PR #185\]](https://github.com/Opentrons/opentrons-emulation/pull/185)
  [\[PR #204\]](https://github.com/Opentrons/opentrons-emulation/pull/204)

### Features

- Firmware Level Heater-Shaker Emulation [\[PR #173\]](https://github.com/Opentrons/opentrons-emulation/pull/173)
- Add `dev` Makefile commands that combine `bases_Dockerfile` and `Dockerfile` together to allow for testing changes in
  `bases_Dockerfile`
  . [\[PR #180\]](https://github.com/Opentrons/opentrons-emulation/pull/180) [\[DOCS\]](https://github.com/Opentrons/opentrons-emulation/tree/release-v3.0.0#how-to-modify-dockerfiles)
- Add compose file generation logs [\[PR #184\]](https://github.com/Opentrons/opentrons-emulation/pull/184)
  [\[PR #185\]](https://github.com/Opentrons/opentrons-emulation/pull/185)
  [\[PR #190\]](https://github.com/Opentrons/opentrons-emulation/pull/190)
  [\[PR #191\]](https://github.com/Opentrons/opentrons-emulation/pull/191)
  [\[DOCS\]](https://github.com/Opentrons/opentrons-emulation/blob/release-v3.0.0/README.md#debugging-docker-compose-file-generation)
- Add VSCode devcontainer support [\[PR #193\]](https://github.com/Opentrons/opentrons-emulation/pull/193)
  [\[PR #195\]](https://github.com/Opentrons/opentrons-emulation/pull/195) [\[DOCS\]](https://github.com/Opentrons/opentrons-emulation/blob/release-v3.0.0/README.md#development-container-devcontainer)
- Add support for [state manager in ot3-firmware](https://github.com/Opentrons/ot3-firmware/tree/main/state_manager)
  [\[PR #194\]](https://github.com/Opentrons/opentrons-emulation/pull/194)
- Add healthchecks to all emulation containers [\[PR #202\]](https://github.com/Opentrons/opentrons-emulation/pull/202)
- Add support for declaring environment variables on any emulation
  container [\[PR #203\]](https://github.com/Opentrons/opentrons-emulation/pull/203) [\[DOCS\]](https://github.com/Opentrons/opentrons-emulation/blob/release-v3.0.0/docs/EMULATION_CONFIGURATION_FILE_KEY_DEFINITIONS.md#specifying-custom-environment-variables)

### Chores

- Update Github Action OS's from Ubuntu 18.04 to Ubuntu
  20.04 [\[PR #175\]](https://github.com/Opentrons/opentrons-emulation/pull/175)
- Add `opentrons-hardware-source-type` and `opentrons-hardware-source-location` to necessary sample files.
  [\[PR #184\]](https://github.com/Opentrons/opentrons-emulation/pull/184)
  [\[PR #198\]](https://github.com/Opentrons/opentrons-emulation/pull/198)

### Refactor

- Switch to use [poetry](https://python-poetry.org/) for building instead of
  pipenv [\[PR #180\]](https://github.com/Opentrons/opentrons-emulation/pull/180)
- Refactor all calls to `pip` to call using `python` built into
  containers [\[PR #197\]](https://github.com/Opentrons/opentrons-emulation/pull/197)
- Symlink `python` and `python3` commands to version of python installed by Dockerfile.
  [\[PR #197\]](https://github.com/Opentrons/opentrons-emulation/pull/197)
- Make `cpp-base` inherit from `python-base` inside
  of `bases_Dockerfile` ([For state manager compatability](https://github.com/Opentrons/ot3-firmware/tree/main/state_manager))
  [\[PR #197\]](https://github.com/Opentrons/opentrons-emulation/pull/197)

______________________________________________________________________

## v2.3.2 (2022-07-08)

### Bug Fixes

- Update python dependency caching [\[PR #169\]](https://github.com/Opentrons/opentrons-emulation/pull/169)

### Features

- None

### Chores

- Update
  README [\[PR #166\]](https://github.com/Opentrons/opentrons-emulation/pull/166) [\[PR #170\]](https://github.com/Opentrons/opentrons-emulation/pull/170)

______________________________________________________________________

## v2.3.1 (2022-04-01)

### Bug Fixes

- Fix breaking caches in Github Actions [\[PR #162\]](https://github.com/Opentrons/opentrons-emulation/pull/162)

### Features

- None

### Chores

- Update pipenv and pyenv steps in README [\[PR #161\]](https://github.com/Opentrons/opentrons-emulation/pull/161)

______________________________________________________________________

## v2.3.0 (2022-04-01)

### Bug Fixes

- None

### Features

- Add image caching with Github Container
  Registry [\[PR #157\]](https://github.com/Opentrons/opentrons-emulation/pull/157)

### Chores

- None

______________________________________________________________________

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

______________________________________________________________________

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
