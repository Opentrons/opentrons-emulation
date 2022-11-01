# Makefile Commands

`opentrons-emulation` supports a number of Makefile commands. Below are a description of their functionality.

> **Note:**
> Use `dev` commands when you have made changes to `bases_Dockerfile` and need to test them.

- [Generating Compose Files](#generating-compose-files)
  - [`generate-compose-file`](#-generate-compose-file-)
  - [`dev-generate-compose-file`](#-dev-generate-compose-file-)
- [Building Docker Images](#building-docker-images)
  - [`build`](#-build-)
  - [`build-print`](#-build-print-)
  - [`build-no-cache`](#-build-no-cache-)
  - [`build-print-no-cache`](#-build-print-no-cache-)
  - [`dev-build`](#-dev-build-)
  - [`dev-build-print`](#-dev-build-print-)
  - [`dev-build-no-cache`](#-dev-build-no-cache-)
  - [`dev-build-print-no-cache`](#-dev-build-print-no-cache-)
- [Running Emulation](#running-emulation)
  - [`run`](#-run-)
  - [`run-detached`](#-run-detached-)
  - [`dev-run`](#-dev-run-)
  - [`dev-run-detached`](#-dev-run-detached-)
- [Controlling Emulation](#controlling-emulation)
  - [`stop`](#-stop-)
  - [`start`](#-start-)
  - [`restart`](#-restart-)
  - [`remove`](#-remove-)
- [Logging](#logging)
  - [`logs`](#-logs-)
  - [`logs-tail`](#-logs-tail-)
- [Combination Commands](#combination-commands)
  - [`remove-build-run`](#-remove-build-run-)
  - [`remove-build-run-detached`](#-remove-build-run-detached-)
- [CAN Communication Commands (OT-3 Only)](#can-communication-commands--ot-3-only-)
  - [`can-comm`](#-can-comm-)
  - [`can-mon`](#-can-mon-)
- [Misc Commands](#misc-commands)
  - [`load-container-names`](#-load-container-names-)
  - [`check-remote-only`](#-check-remote-only-)
  - [`test-samples`](#-test-samples-)
  - [`push-docker-image-bases`](#-push-docker-image-bases-)
  - [`ot2`](#-ot2-)
  - [`ot3`](#-ot3-)
  - [`emulation-check`](#-emulation-check-)
- [emulation_system Project Commands](#emulation-system-project-commands)
  - [`setup`](#-setup-)
  - [`clean`](#-clean-)
  - [`teardown`](#-teardown-)
  - [`lint`](#-lint-)
  - [`format`](#-format-)
  - [`test`](#-test-)

<hr style="border:2px solid">

## Generating Compose Files

One of the main functions of `opentrons-emulation` is to dynamically build Docker Compose files.

### `generate-compose-file`

- Generates Docker-Compose file from passed configuration file and outputs it to stdout.

**Example:** `make generate-compose-file file_path=./samples/ot2/ot2_remote.yaml`

### `dev-generate-compose-file`

- Creates dev_Dockerfile, which combines `bases_Dockerfile` and `Dockerfile` into a single file.
- Generates Docker-Compose file from passed configuration file, with
  references to dev_Dockerfile and its targets
- Finally outputs it to stdout.

**Example:** `make dev-generate-compose-file file_path=./samples/ot2/ot2_remote.yaml`

<hr style="border:2px solid">

## Building Docker Images

> **Note 1:**
> This repository supports building against `x86_64` and `arm64` type processors

> **Note 2:** Docker images should be rebuilt under the following conditions:
>
> - If anything changes in your configuration file
> - If you have an emulator using `remote` source type, `latest` source location, and there has been an update to the
>   main branch of the source repo
> - If the underlying Dockerfile changes

### `build`

**Description:**

- Runs `generate-compose-file`. See [Generate Compose File](#generate-compose-file)
- Using generated compose file, builds necessary images
  using [docker buildx bake](https://docs.docker.com/engine/reference/commandline/buildx_bake/).

### `build-print`

**Description:**

- Same as [`build`](#-build-), but prints all output in plain text

**Example:** `make build-print file_path=./samples/ot2/ot2_remote.yaml`

### `build-no-cache`

**Description:**

- Same as [`build`](#-build-), but does not use Docker cache, and instead builds everything from scratch.

**Example:** `make build-no-cache file_path=./samples/ot2/ot2_remote.yaml`

### `build-print-no-cache`

**Description:**

- Same as [`build`](#-build-), but does not use Docker cache, and instead builds everything from scratch. Also prints
  all output in plain text.

**Example:** `make build-print-no-cache file_path=./samples/ot2/ot2_remote.yaml`

### `dev-build`

**Description:**

- Runs `dev-generate-compose-file`. See [Generate Compose File (Dev Mode)](#generate-compose-file--dev-mode-)
- Using generated development compose file, builds necessary images
  using [docker buildx bake](https://docs.docker.com/engine/reference/commandline/buildx_bake/).

**Example:** `make dev-build file_path=./samples/ot2/ot2_remote.yaml`

### `dev-build-print`

**Description:**

- Same as [`dev-build`](#-dev-build-), but prints all output in plain text

**Example:** `make dev-build-print file_path=./samples/ot2/ot2_remote.yaml`

### `dev-build-no-cache`

**Description:**

- Same as [`dev-build`](#-dev-build-), but does not use Docker cache, and instead builds everything from scratch.

**Example:** `make dev-build-no-cache file_path=./samples/ot2/ot2_remote.yaml`

### `dev-build-print-no-cache`

**Description:**

- Same as [`dev-build`](#-dev-build-), but does not use Docker cache, and instead builds everything from scratch. Also
  prints
  all output in plain text.

**Example:** `make dev-build-print-no-cache file_path=./samples/ot2/ot2_remote.yaml`

<hr style="border:2px solid">

## Running Emulation

### `run`

**Description:**

- Runs `generate-compose-file`. See [Generate Compose File](#generate-compose-file)
- Creates and starts Docker Containers from generated Docker-Compose file.
- Outputs logs to stdout.
- Stops and removes containers on exit of logs

**Example:** `make run file_path=./samples/ot2/ot2_remote.yaml`

### `run-detached`

**Description:**

- Same as [`run`](#-run-) but detaches logs from stdout and returns control of terminal

**Example:** `make run-detached file_path=./samples/ot2/ot2_remote.yaml`

### `dev-run`

**Description:**

- Runs `dev-generate-compose-file`. See [Generate Compose File (Dev Mode)](#generate-compose-file--dev-mode-)
- Creates and starts Docker Containers from generated Docker-Compose file.
- Outputs logs to stdout.
- Stops and removes containers on exit of logs

**Example:** `make dev-run file_path=./samples/ot2/ot2_remote.yaml`

### `dev-run-detached`

**Description:**

- Same as [`dev-run`](#-dev-run-) but detaches logs from stdout and returns control of terminal

**Example:** `make dev-run-detached file_path=./samples/ot2/ot2_remote.yaml`

<hr style="border:2px solid">

## Controlling Emulation

### `stop`

**Description:**

- Runs `generate-compose-file`. See [Generate Compose File](#generate-compose-file)
- Stops all running containers defined in generated compose file.

**Example:** `make stop file_path=./samples/ot3/ot3_remote.yaml`

### `start`

**Description:**

- Runs `generate-compose-file`. See [Generate Compose File](#generate-compose-file)
- Starts all stopped containers defined in generated compose file.

**Example:** `make start file_path=./samples/ot3/ot3_remote.yaml`

### `restart`

**Description:**

- Runs `generate-compose-file`. See [Generate Compose File](#generate-compose-file)
- Restarts all containers defined in generated compose file.

**Example:** `make restart file_path=./samples/ot3/ot3_remote.yaml`

### `remove`

**Description:**

- Runs `generate-compose-file`. See [Generate Compose File](#generate-compose-file)
- Kills all containers defined in generated compose file.
- Removes all containers defined in generated compose file.

**Example:** `make remove file_path=./samples/ot2/ot2_remote.yaml`

<hr style="border:2px solid">

## Logging

### `logs`

**Description:**

- Prints logs from all containers to stdout and follows current logs

**Example:** `make logs file_path=./samples/ot2/ot2_remote.yaml`

> **Warning:**
>
> This will print all logs since the start of your containers to stdout. This can be a whole whole whole lot.
>
> Piping to a file might be a good idea. `make logs file_path=./samples/ot2/ot2_remote.yaml > logs.txt`

### `logs-tail`

**Description:**

- Prints only the last n lines from the logs from all containers to stdout and follows current logs

**Example:** `make logs-tail file_path=./samples/ot2/ot2_remote.yaml number=100`

<hr style="border:2px solid">

## Combination Commands

### `remove-build-run`

**Description:**

- Runs `remove`. See [remove](#-remove-)
- Runs `build`. See [build](#-build-)
- Runs `run`. See [run](#-run-)

**Example:** `make remove-build-run file_path=./samples/ot2/ot2_remote.yaml`

### `remove-build-run-detached`

**Description:**

- Runs `remove`. See [remove](#-remove-)
- Runs `build`. See [build](#-build-)
- Runs `run-detached`. See [run-detached](#-run-detached-)

**Example:** `make remove-build-run file_path=./samples/ot2/ot2_remote.yaml`

<hr style="border:2px solid">

## CAN Communication Commands (OT-3 Only)

### `can-comm`

**Description:**

- Run can communication script against can_server

**Example:** `make can-comm file_path=./samples/ot3/ot3_remote.yaml`

### `can-mon`

**Description:**

- Run can monitor script against can_server

**Example:** `make can-mon file_path=./samples/ot3/ot3_remote.yaml`

<hr style="border:2px solid">

## Misc Commands

### `load-container-names`

**Description:**

- Return container names based off of passed filter

Acceptable filters are:

- `heater-shaker-module`
- `magnetic-module`
- `thermocycler-module`
- `temperature-module`
- `emulator-proxy`
- `smoothie`
- `can-server`
- `ot3-gantry-x`
- `ot3-gantry-y`
- `ot3-head`
- `ot3-pipettes`
- `modules`
- `firmware`
- `robot-server`
- `all`

**Example:** `make load-container-names file_path=./samples/ot2/ot2_remote.yaml filter=robot-server`

### `check-remote-only`

**Description:**

- Verifies that all source-types of configuration file are `remote`. Exits with error code 1, if not.

**Example:** `make check-remote-only file_path=./samples/ot3/ot3_remote.yaml`

### `test-samples`

**Description:**

- Runs generate_compose_file for all configuration files in samples

**Example:** `make test-samples`

### `push-docker-image-bases`

**Description:**

- Runs generate_compose_file for all configuration files in samples

**Example:** `make push-docker-image-bases branch_name=main`

### `ot2`

**Description:**

- One command to do all steps necessary to bring up an ot2 using the default code from GitHub.

**Examples:**

`make ot2`

`make ot2 OT2CONFIG=./samples/ot2/ot2_and_2_heater_shakers.yaml`

### `ot3`

**Description:**

- One command to do all steps necessary to bring up an ot3 using the default code from GitHub.

**Examples:**

`make ot3`

`make ot3 OT3CONFIG=./samples/ot3/ot3_remote.yaml`

### `emulation-check`

**Description:**

- Run a curl command to retrieve module information verifying that the emulation is running.

**Example:**
`make emulation-check`

<hr style="border:2px solid">

## emulation_system Project Commands

### `setup`

**Description:**

- Setup emulation_system project

**Example:** `make setup`

### `clean`

**Description:**

- Clean emulation_system project

**Example:** `make clean`

### `teardown`

**Description:**

- Teardown emulation_system project

**Example:** `make teardown`

### `lint`

**Description:**

- Confirm there are no formatting errors against Markdown files
- Run linting against emulation_system (mypy, isort, black, flake8)

**Example:** `make lint`

### `format`

**Description:**

- Run formatting against Markdown files
- Run formatting against emulation_system (isort, black)

**Example:** `make format`

### `test`

**Description:**

- Run all pytests in emulation_system project

**Example:** `make test`
