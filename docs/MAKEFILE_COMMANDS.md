# Makefile Commands

`opentrons-emulation` supports a number of Makefile commands. Below are a description of their functionality.

## Emulation Control Commands

### Generate Compose File

**Description:** Generates Docker-Compose file from passed configuration file and outputs it to stdout.

**Command:** `generate-compose-file`

**Example:** `make generate-compose-file file_path=./samples/ot2/ot2_remote.yaml`

### Build System

**Description:** Builds generated Docker-Compose file's necessary images using docker buildx

**Command:** `build`

**Example:** `make build file_path=./samples/ot2/ot2_remote.yaml`

> **Note 1:**
> This repository supports building against `x86_64` and `arm64` type processors

> **Note 2:** Docker images should be rebuilt under the following conditions:
>
> - If anything changes in your configuration file
> - If you have an emulator using `remote` source type, `latest` source location, and there has been an update to the main branch of the source repo
> - If the underlying Dockerfile changes

### Run System (Attach Logs to STDOUT)

**Description:**

- Creates and starts Docker Containers from generated Docker-Compose file.
- Outputs logs to stdout.
- Stops and removes containers on exit of logs

**Command:** `run`

**Example:** `make run file_path=./samples/ot2/ot2_remote.yaml`

### Run System (Detach Logs)

**Description:**

- Creates and starts Docker Containers from generated Docker-Compose file.
- Detaches logs from stdout and returns control of terminal

**Command:** `run-detached`

**Example:** `make run-detached file_path=./samples/ot2/ot2_remote.yaml`

### Removing System

**Description:** Removes containers from generated Docker-Compose file

**Command:** `remove`

**Example:** `make remove file_path=./samples/ot2/ot2_remote.yaml`

### Remove-Build-Run (Attach Logs to STDOUT)

**Description:**

- Removes, rebuilds, and runs generated Docker-Compose file
- Outputs logs to stdout
- Stops and removes containers on exit of logs

**Command:** `remove-build-run`

**Example:** `make remove-build-run file_path=./samples/ot2/ot2_remote.yaml`

### Remove-Build-Run (Detach Logs)

**Description:**

- Removes, rebuilds, and runs generated Docker-Compose file
- Detaches logs from stdout and returns control of terminal

**Command:** `remove-build-run-detached`

**Example:** `make remove-build-run-detached file_path=./samples/ot2/ot2_remote.yaml`

### Restart System (Rebuild Mounted Code)

**Description:**

- Restarts all containers from generated Docker-Compose file
- Use this command to rebuild code if you have containers that have locally bound code

**Command:** `restart`

**Example:** `make restart file_path=./samples/ot2/ot2_local.yaml`

### Viewing System Logs

**Description:**  Prints logs from all containers to stdout and follows current logs

**Command:** `logs`

**Example:** `make logs file_path=./samples/ot2/ot2_remote.yaml`

> **Warning:**
>
> This will print all logs since the start of your containers to stdout. This can be a whole whole whole lot.
>
> Piping to a file might be a good idea. `make logs file_path=./samples/ot2/ot2_remote.yaml > logs.txt`

### Viewing System Logs (Tailed)

**Description:** Prints only the last n lines from the logs from all containers to stdout and follows current logs

**Command:** `logs-tail`

**Example:** `make logs-tail file_path=./samples/ot2/ot2_remote.yaml number=100`

### Load Container Names

**Description:** Return container names based off of passed filter

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

**Command:** `load-container-names`

**Example:** `make load-container-names file_path=./samples/ot2/ot2_remote.yaml filter=robot-server`

______________________________________________________________________

## CAN Communication Commands (OT3 Only)

### CAN Communication (OT3 Only)

**Description:** Run can communication script against can_server

**Commands:** `can-comm`

**Example:** `make can-comm file_path=./samples/ot3/ot3_remote.yaml`

### CAN Monitor (OT3 Only)

**Description:** Run can monitor script against can_server

**Commands:** `can-mon`

**Example:** `make can-mon file_path=./samples/ot3/ot3_remote.yaml`

______________________________________________________________________

## CI Commands

### Check Remote Only

**Description:** Verifies that all source-types of configuration file are `remote`. Exits with error code 1, if not.

**Commands:** `check-remote-only`

**Example:** `make check-remote-only file_path=./samples/ot3/ot3_remote.yaml`

### Test Samples

**Description:** Runs generate_compose_file for all configuration files in samples

**Commands:** `test-samples`

**Example:** `make test-samples`

## emulation_system Commands

### Setup

**Description:** Setup emulation_system project

**Commands:** `setup`

**Example:** `make setup`

### Clean

**Description:** Clean emulation_system project

**Commands:** `clean`

**Example:** `make clean`

### Teardown

**Description:** Teardown emulation_system project

**Commands:** `teardown`

**Example:** `make teardown`

### Lint

**Description:**

- Confirm there are no formatting errors against Markdown files
- Run linting against emulation_system (mypy, isort, black, flake8)

**Commands:** `lint`

**Example:** `make lint`

### Format

**Description:**

- Run formatting against Markdown files
- Run formatting against emulation_system (isort, black)

**Commands:** `format`

**Example:** `make format`

### Test

**Description:** Run all pytests in emulation_system project

**Commands:** `test`

**Example:** `make test`
