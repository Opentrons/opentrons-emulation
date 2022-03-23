# Github Action Documentation

`opentrons-emulation` provides a Github Action for utilizing the functionality of the repository.

The single action provides different functionality through the `command` parameter. Valid commands are:

- `setup`
- `setup-break-cache`
- `setup-python-only`
- `run`
- `teardown`
- `yaml-sub`

| Command Name              | command             | input-file         | substitutions       | output-file-location | cache-break        |
|---------------------------|---------------------|--------------------|---------------------|----------------------|--------------------|
| `setup`                   | :heavy_check_mark:  | :heavy_check_mark: | :x:                 | :x:                  | :x:                |
| `setup-break-cache`       | :heavy_check_mark:  | :heavy_check_mark: | :x:                 | :x:                  | :heavy_check_mark: |
| `setup-break-python-only` | :heavy_check_mark:  | :heavy_check_mark: | :x:                 | :x:                  | :heavy_check_mark: |
| `run`                     | :heavy_check_mark:  | :heavy_check_mark: | :x:                 | :x:                  | :x:                |
| `teardown`                | :heavy_check_mark:  | :heavy_check_mark: | :x:                 | :x:                  | :x:                |
| `yaml-sub`                | :heavy_check_mark:  | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark:   | :x:                |

## setup

The setup command installs all Python dependencies, creates a configuration.json file, validates the passed
