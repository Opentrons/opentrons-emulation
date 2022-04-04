# Github Action Documentation

- [Github Action Documentation](#github-action-documentation)
  - [setup](#setup)
    - [Example](#example)
  - [setup-break-cache](#setup-break-cache)
    - [Example](#example-1)
  - [setup-python-only](#setup-python-only)
    - [Example](#example-2)
  - [run](#run)
    - [Example](#example-3)
  - [teardown](#teardown)
    - [Example](#example-4)

`opentrons-emulation` provides a Github Action for utilizing the functionality of the repository.

The single action provides different functionality through the `command` parameter. Valid commands are:

- `setup`
- `setup-break-cache`
- `setup-python-only`
- `run`
- `teardown`
- `yaml-sub`

| Command Name        | command            | input-file         | substitutions      | output-file-location | cache-break        |
| ------------------- | ------------------ | ------------------ | ------------------ | -------------------- | ------------------ |
| `setup`             | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                  | :x:                |
| `setup-break-cache` | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                  | :x:                |
| `setup-python-only` | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                  | :heavy_check_mark: |
| `run`               | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                  | :x:                |
| `teardown`          | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                  | :x:                |
| `yaml-sub`          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark:   | :x:                |

## setup

The `setup` command is a superset of the other setup commands. It performs the following functions:

- Installs all Python dependencies (calling to `setup-python-only`)
- Creates a configuration.json file
- Validates the passed input file has only remote `source-type` values
- Builds all Docker Images.

The Python dependencies are cached between runs.

### Example

```yaml
on: [ pull_request, push ]
jobs:
  setup-example:
    runs-on: "ubuntu-18.04"
    name: Setup Example
    steps:

      # You always have to check out the opentrons-emulation repo 
      - name: Checkout opentrons-emulation repository
        uses: actions/checkout@v3
        with:
          repository: Opentrons/opentrons-emulation

      - name: Setup opentrons-emulation project
        uses: Opentrons/opentrons-emulation@update-action-refs
          with:
            input-file: ${PWD}/samples/ot3/ot3_remote.yaml
            command: setup
```

## setup-break-cache

The `setup-break-cache` command works exactly the same as the `setup` command but runs without any caching. This can be
useful when something goes wrong with the `setup` action and you want to rerun everything without the cache.

### Example

```yaml
on: [ pull_request, push ]
jobs:
  setup-break-cache-example:
    runs-on: "ubuntu-18.04"
    name: Setup (Break Cache) Example
    steps:

      # You always have to check out the opentrons-emulation repo 
      - name: Checkout opentrons-emulation repository
        uses: actions/checkout@v3
        with:
          repository: Opentrons/opentrons-emulation
          ref: v2.1.0

      - name: Setup opentrons-emulation project
        uses: Opentrons/opentrons-emulation@v2.1.0
          with:
            input-file: ${PWD}/samples/ot3/ot3_remote.yaml
            command: setup-break-cache
```

## setup-python-only

The `setup-python-only` command only installs Python dependencies. Currently, this is only used internally by the
`yaml-sub` command.

### Example

```yaml
on: [ pull_request, push ]
jobs:
  setup-python-only-example:
    runs-on: "ubuntu-18.04"
    name: Setup (Python Only) Example
    steps:

      # You always have to check out the opentrons-emulation repo 
      - name: Checkout opentrons-emulation repository
        uses: actions/checkout@v3
        with:
          repository: Opentrons/opentrons-emulation
          ref: v2.1.0

      - name: Setup opentrons-emulation project
        uses: Opentrons/opentrons-emulation@v2.1.0
          with:
            command: setup-python-only
```

## run

The `run` command starts emulation Docker containers. It is required that you run `setup` or `setup-break-cache` before
running this command. After the `run` command is finished, you should the containers some time to finish starting.

### Example

```yaml
on: [ pull_request, push ]
jobs:
  run-example:
    runs-on: "ubuntu-18.04"
    name: Run Example
    steps:

      # You always have to check out the opentrons-emulation repo 
      - name: Checkout opentrons-emulation repository
        uses: actions/checkout@v3
        with:
          repository: Opentrons/opentrons-emulation
          ref: v2.1.0

      - name: Setup opentrons-emulation project
        uses: Opentrons/opentrons-emulation@v2.1.0
          with:
            input-file: ${PWD}/samples/ot3/ot3_remote.yaml
            command: setup

      - name: Run Emulation
        uses: Opentrons/opentrons-emulation@v2.1.0
        with:
          input-file: ${PWD}/samples/ot3_remote.yaml
          command: run

      - name: Give it some time to start up
        run: sleep 10s
```

## teardown

The `teardowm` command kills and removes any running emulation Docker containers. It is required that you run `setup`
or `setup-break-cache` before running this command.

### Example

```yaml
on: [ pull_request, push ]
jobs:
  teardown-example:
    runs-on: "ubuntu-18.04"
    name: Teardown Example
    steps:

      # You always have to check out the opentrons-emulation repo 
      - name: Checkout opentrons-emulation repository
        uses: actions/checkout@v3
        with:
          repository: Opentrons/opentrons-emulation
          ref: v2.1.0

      - name: Setup opentrons-emulation project
        uses: Opentrons/opentrons-emulation@v2.1.0
          with:
            input-file: ${PWD}/samples/ot3/ot3_remote.yaml
            command: setup

      - name: Run Emulation
        uses: Opentrons/opentrons-emulation@v2.1.0
        with:
          input-file: ${PWD}/samples/ot3_remote.yaml
          command: run

      - name: Give it some time to start up
        run: sleep 10s

      - name: Teardown Emulation
        uses: Opentrons/opentrons-emulation@v2.1.0
        with:
          input-file: ${PWD}/samples/ot3_remote.yaml
          command: teardown
```
