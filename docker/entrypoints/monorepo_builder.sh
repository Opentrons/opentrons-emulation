#!/bin/bash
# Build all necessary wheels for running:
# Robot Server
# Smoothie Emulation
# Firmware Module Emulation
# CAN Server
# Emulator Proxy

# /dist will be loaded into a volume in local-monorepo-builder container
# All emulator containers needing the wheels will use that volume and bind it to /dist
(cd /opentrons/shared-data/python && monorepo_python setup.py -q bdist_wheel -d /dist/)
(cd /opentrons/api && monorepo_python setup.py -q bdist_wheel -d /dist/)
(cd /opentrons/notify-server && monorepo_python setup.py -q bdist_wheel -d /dist/)
(cd /opentrons/robot-server && monorepo_python setup.py -q bdist_wheel -d /dist/)
(cd /opentrons/hardware && monorepo_python setup.py -q bdist_wheel -d /dist/)
(cd /opentrons/server-utils && monorepo_python setup.py -q bdist_wheel -d /dist/)
