### Emulation Commands

The following emulation commands require a `file_path` argument with a path to a valid emulation configuration file. Can
specify paths relative to `opentrons-emulation`. They are executed in the top-level directory of the repository.

#### Building System

**Description:** Use this command to build the necessary Docker images from your system. Docker images should be rebuilt
under the following conditions:

- If anything changes in your configuration file
- If you have an emulator using `remote` source type, `latest` source location, and there has been an update to the main
  branch of the source repo
- If the underlying Dockerfile changes

**Command:** `build`

**Example:** `make build file_path=./samples/yaml/ot2.yaml`

> Note: This repository supports building against `x86_64` and `arm64` type processors

#### Running System

**Description:** Use this command to bring up an emulated system.

**Command:** `make run file_path=./samples/yaml/ot2.yaml`

#### Viewing System Logs

**Description:** Use this command view the logs of a running emulation system.

**Command:** `make logs file_path=./samples/yaml/ot2.yaml`

#### Removing System

**Description:** Use this command to remove an emulated system.

**Command:** `make remove file_path=./samples/yaml/ot2.yaml`

#### Generate Compose File

**Description:** Use this command to generate the Docker Compose file that the system runs under the hood.

**Command:** `make generate-compose-file file_path=./samples/yaml/ot2.yaml`
