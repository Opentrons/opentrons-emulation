# syntax=docker/dockerfile-upstream:master-labs
#############################################################
#                       LOCAL TARGETS                       #
#############################################################

# Targets for all development builds of emulators
# All source code should be bind-mounted in, so do not copy it in.
# entrypoint.sh should also be bind-mounted in so do not copy it in either
# Make sure to include the OPENTRONS_HARDWARE env variable

############################
# Hardware Local Emulators #
############################

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as heater-shaker-hardware
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as thermocycler-hardware
ENV OPENTRONS_HARDWARE "thermocycler-hardware"

# Do not use common-ot3-firmware as value for OPENTRONS_HARDWARE
# What will happen is the first container to finish building will move all the executables to their new file location
# and the rest of the containers will not be able to find them

# Instead specify the individual piece of firware as the hardware. This will cause only the container to only build
# and move firmware for itself. Eliminating the issue of them clobbering each other

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-pipettes-hardware
ENV OPENTRONS_HARDWARE "ot3-pipettes-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-head-hardware
ENV OPENTRONS_HARDWARE "ot3-head-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-gantry-x-hardware
ENV OPENTRONS_HARDWARE "ot3-gantry-x-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-gantry-y-hardware
ENV OPENTRONS_HARDWARE "ot3-gantry-y-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-bootloader-hardware
ENV OPENTRONS_HARDWARE "ot3-bootloader-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-gripper-hardware
ENV OPENTRONS_HARDWARE "ot3-gripper-hardware"

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH} as ot3-state-manager
ENV OPENTRONS_HARDWARE "ot3-state-manager"

############################
# Firmware Local Emulators #
############################

FROM ghcr.io/opentrons/python-base:latest as thermocycler-firmware
ENV OPENTRONS_HARDWARE "thermocycler-firmware"

FROM ghcr.io/opentrons/python-base:latest as heater-shaker-firmware
ENV OPENTRONS_HARDWARE "heater-shaker-firmware"

FROM ghcr.io/opentrons/python-base:latest as magdeck-firmware
ENV OPENTRONS_HARDWARE "magdeck-firmware"

FROM ghcr.io/opentrons/python-base:latest as tempdeck-firmware
ENV OPENTRONS_HARDWARE "tempdeck-firmware"

FROM ghcr.io/opentrons/python-base:latest as emulator-proxy
ENV OPENTRONS_HARDWARE "emulator-proxy"

FROM ghcr.io/opentrons/python-base:latest as robot-server
ENV OPENTRONS_HARDWARE "robot-server"

FROM ghcr.io/opentrons/python-base:latest as smoothie
ENV OPENTRONS_HARDWARE "smoothie"

FROM ghcr.io/opentrons/python-base:latest as can-server
ENV OPENTRONS_HARDWARE "can-server"





############################################### vvv PLEASE READ ME vvv #################################################
############################################### vvv PLEASE READ ME vvv #################################################
############################################### vvv PLEASE READ ME vvv #################################################

#                                                       Note:
# Configuration for local targets ends here. All following targets should either be remote targets or used to build
# remote targets. I am trying super hard to keep this file organized.

############################################### ^^^ PLEASE READ ME ^^^ #################################################
############################################### ^^^ PLEASE READ ME ^^^ #################################################
############################################### ^^^ PLEASE READ ME ^^^ #################################################





#############################################################
#                        REPO SOURCE                        #
#############################################################

# The following targets download source code, unpack it, and copy the entrypoint.sh file in.
# These should only be used for production targets.
# There should only be one repo builder target per source code repo being utlized.

# ot3-firmware-source:
#   * Based off of cpp-base
#   * Contains ot3-firmware source and entrypoint.sh

# opentrons-modules-source:
#   * Based off of cpp-base
#   * Contains modules source and entrypoint.sh

# opentrons-source:
#  * Based off of ghcr.io/opentrons/python-base:latest
#  * Contains opentrons source and entrypoint.sh

#######################
# ot3-firmware-source #
#######################

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH}:latest as ot3-firmware-source
ARG FIRMWARE_SOURCE_DOWNLOAD_LOCATION="https://github.com/Opentrons/ot3-firmware/archive/refs/heads/main.zip"
ARG OPENTRONS_SOURCE_DOWNLOAD_LOCATION="https://github.com/Opentrons/opentrons/archive/refs/heads/edge.zip"

ENV FIRMWARE_SOURCE_DOWNLOAD_LOCATION=$FIRMWARE_SOURCE_DOWNLOAD_LOCATION
ENV OPENTRONS_SOURCE_DOWNLOAD_LOCATION=$OPENTRONS_SOURCE_DOWNLOAD_LOCATION

ADD --keep-git-dir=true $FIRMWARE_SOURCE_DOWNLOAD_LOCATION /ot3-firmware
ADD --keep-git-dir=true $OPENTRONS_SOURCE_DOWNLOAD_LOCATION /opentrons

FROM ot3-firmware-source as ot3-firmware-builder
COPY entrypoints/ot3_firmware_builder.sh /build.sh
COPY scripts/selective_monorepo_builder.sh /selective_monorepo_builder.sh

##################
# modules-source #
##################

FROM ghcr.io/opentrons/cpp-base-${TARGETARCH}:latest as opentrons-modules-source
ARG MODULE_SOURCE_DOWNLOAD_LOCATION="https://github.com/Opentrons/opentrons-modules/archive/refs/heads/edge.zip"

ENV MODULE_SOURCE_DOWNLOAD_LOCATION=$MODULE_SOURCE_DOWNLOAD_LOCATION

ADD  --keep-git-dir=true $MODULE_SOURCE_DOWNLOAD_LOCATION /opentrons-modules.zip

RUN (cd / &&  \
    unzip -q opentrons-modules.zip && \
    rm -f opentrons-modules.zip && \
    mv opentrons-modules* opentrons-modules)


FROM opentrons-modules-source as opentrons-modules-builder
COPY entrypoints/opentrons_modules_builder.sh /build.sh


####################
# opentrons-source #
####################

FROM ghcr.io/opentrons/python-base:latest as opentrons-source

ARG OPENTRONS_SOURCE_DOWNLOAD_LOCATION="https://github.com/Opentrons/opentrons/archive/refs/heads/edge.zip"

ENV OPENTRONS_SOURCE_DOWNLOAD_LOCATION=$OPENTRONS_SOURCE_DOWNLOAD_LOCATION

ADD  --keep-git-dir=true $OPENTRONS_SOURCE_DOWNLOAD_LOCATION /opentrons.zip

RUN (cd / &&  \
    unzip -q opentrons.zip && \
    rm -f opentrons.zip && \
    mv opentrons* opentrons)


FROM opentrons-source as monorepo-builder
COPY entrypoints/monorepo_builder.sh /build.sh
COPY scripts/selective_monorepo_builder.sh /selective_monorepo_builder.sh
