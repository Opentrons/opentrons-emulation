#!/bin/sh -l

cp /main_emulation/configuration_ci.json configuration.json
make check-remote-only file_path=/main_emulation/simple_robot/ot2_with_all_modules.yaml
make build file_path=/main_emulation/simple_robot/ot2_with_all_modules.yaml
make run file_path=/main_emulation/simple_robot/ot2_with_all_modules.yaml
