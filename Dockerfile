#############################################################
#                           BASES                           #
#############################################################

# The following targets are what final image that the end user will use should be based off of

# ubuntu-base:
#   * Lowest level build target that all other targets are based off of
#   * Production targets should be based off of this to keep the images as small as possible

# cpp-base:
#   * Built on top of ubuntu-base
#   * Contains common packages that all ot3-firmware and module firmware require
#   * All firmware Development targets should be based off of this to ensure all packages required for building exist

# TODO: python-base
#   * Will be built on top of ubuntu-base
#   * All python level emulators will be based off of python-base
#   * Will contain all packages needed for building python emulators

###############
# ubuntu-base #
###############

FROM ubuntu:20.04 as ubuntu-base
# Only need to fill out these args, in CI builds to push images to AWS ECR.
# Don't bother when you are doing manual builds. It will break your cache and your
# build will take forever

ARG TRIGGER
ARG BUILD_DATE
ARG VCS_REF
ARG VCS_URL
ARG URL
ARG VENDOR
ARG DOCKER_CMD
ARG DESCRIPTION

LABEL opentrons-emulation.trigger=$TRIGGER
LABEL opentrons-emulation.build_date=$BUILD_DATE
LABEL opentrons-emulation.vcs_ref=$VCS_REF
LABEL opentons-emulation.vcs_url=$VCS_URL
LABEL opentons-emulation.url=$URL
LABEL opentons-emulation.vendor=$VENDOR
LABEL opentons-emulation.docker_cmd=$DOCKER_CMD
LABEL opentons-emulation.description=$DESCRIPTION

ENV DEBIAN_FRONTEND noninteractive

RUN rm -rf /var/lib/apt/lists/*
RUN echo "Updating apt" && apt-get update > /dev/null
RUN apt-get update \
    && apt-get install --no-install-recommends -y wget unzip

#############
# cpp-base #
#############

FROM ubuntu-base as cpp-base

RUN apt-get install \
    --no-install-recommends \
    -y \
    libgtest-dev \
    libboost-test-dev \
    build-essential \
    gcc-10 \
    g++-10 \
    libssl-dev \
    git \
    lsb-release \
    software-properties-common > /dev/null

RUN wget -q https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2-linux-x86_64.tar.gz && \
    tar -zxf cmake-3.21.2-linux-x86_64.tar.gz && \
    rm cmake-3.21.2-linux-x86_64.tar.gz && \
    mv cmake-3.21.2-linux-x86_64 cmake && \
    (cd /usr/bin/ && ln -s /cmake/bin/cmake cmake)

#############################################################
#                        REPO SOURCE                        #
#############################################################

# The following targets download source code, unpack it, and copy the entrypoint.sh file in.
# These should only be used for production targets.
# There should only be one repo builder target per source code repo being utlized.

# ot3-firmware-source:
#   * Based off of cpp-base
#   * Contains ot3-firmware source and entrypoint.sh

# modules-source:
#   * Based off of cpp-base
#   * Contains modules source and entrypoint.sh

# TODO: python-emulators-source
#  * Will be based off of python-base
#  * Will contain opentrons source and entrypoint.sh

#######################
# ot3-firmware-source #
#######################

FROM cpp-base as ot3-firmware-source
ARG FIRMWARE_SOURCE_DOWNLOAD_LOCATION
ADD $FIRMWARE_SOURCE_DOWNLOAD_LOCATION /ot3-firmware.zip
RUN (cd / &&  \
    unzip -q ot3-firmware.zip && \
    rm -f ot3-firmware.zip && \
    mv ot3-firmware* ot3-firmware)
COPY entrypoint.sh /entrypoint.sh

##################
# modules-source #
##################

FROM cpp-base as opentrons-modules-source
ARG MODULE_SOURCE_DOWNLOAD_LOCATION
ADD $MODULE_SOURCE_DOWNLOAD_LOCATION /opentrons-modules.zip
RUN (cd / &&  \
    unzip -q opentrons-modules.zip && \
    rm -f opentrons-modules.zip && \
    mv opentrons-modules* opentrons-modules)
COPY entrypoint.sh /entrypoint.sh

#############################################################
#                    EXECUTABLE BUILDERS                    #
#############################################################

# The following targets should build executables.
# There should be a 1 to 1 mapping of Executable Builder to Production Target
# The Exectuable Builder should build the executable file and the Production Target should copy over to itself
# Building separately from the Production Target to reduce image size

FROM ot3-firmware-source as ot3-echo-builder
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"
RUN /entrypoint.sh build

FROM opentrons-modules-source as heater-shaker-builder
ENV OPENTRONS_HARDWARE "heater-shaker"
RUN /entrypoint.sh build

#############################################################
#                    DEVELOPMENT TARGETS                    #
#############################################################

# Targets for all development builds of emulators
# All source code should be bind-mounted in so do not copy it in
# entrypoint.sh should also be bind-mounted in so do not copy it in either
# Make sure to include the OPENTRONS_HARDWARE env variable

FROM cpp-base as ot3-firmware-echo-dev
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"

FROM cpp-base as heater-shaker-dev
ENV OPENTRONS_HARDWARE "heater-shaker"

##############################################################
#                     PRODUCTION TARGETS                     #
##############################################################

# Targets for all production builds of emulators
# Each Production Target should have a corresponding Executable Builder target
# Each Production Target should copy the executable from the Executable Builder target
# Each Production Target should copy in entrypoint.sh
# Make sure to include the OPENTRONS_HARDWARE env variable


FROM ubuntu-base as ot3-firmware-echo
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"
COPY entrypoint.sh /entrypoint.sh
COPY --from=ot3-echo-builder /ot3-firmware/build-host/can/simulator/can-simulator /ot3-firmware/build-host/can/simulator/can-simulator
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as heater-shaker
ENV OPENTRONS_HARDWARE "heater-shaker"
COPY entrypoint.sh /entrypoint.sh
COPY --from=heater-shaker-builder /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator
ENTRYPOINT ["/entrypoint.sh", "run"]

