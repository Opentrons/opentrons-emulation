#!/bin/sh -l

cp configuration_ci.json configuration.json
make check-remote-only file_path=compose/ot2_with_all_modules.yaml
make build file_path=compose/ot2_with_all_modules.yaml
make run file_path=compose/ot2_with_all_modules.yaml
