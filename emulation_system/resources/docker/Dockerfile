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
    && apt-get install \
       --no-install-recommends \
       -y \
      wget \
      unzip \
      software-properties-common \
      build-essential \
      curl \
      git \
      libssl-dev \
      && rm -rf /var/lib/apt/lists/*

############
# cpp-base #
############

FROM ubuntu-base as cpp-base

RUN apt-get update && \
    apt-get install \
    --no-install-recommends \
    -y \
    libgtest-dev \
    libboost-test-dev \
    gcc-10 \
    g++-10 \
    lsb-release  > /dev/null

RUN wget -q https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2-linux-x86_64.tar.gz && \
    tar -zxf cmake-3.21.2-linux-x86_64.tar.gz && \
    rm cmake-3.21.2-linux-x86_64.tar.gz && \
    mv cmake-3.21.2-linux-x86_64 cmake && \
    (cd /usr/bin/ && ln -s /cmake/bin/cmake cmake)

###############
# python-base #
###############

FROM ubuntu-base as python-base

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
    apt-get install -y \
    pipenv \
    python3.7 \
    libudev-dev \
    libsystemd-dev \
    python3-dev \
    pkgconf \
    libpython3.7-dev \
    pip

RUN (cd /usr/bin/ && ln -s /usr/bin/python3.7 python)

ENV NODE_VERSION 14
ENV OT_PYTHON "/usr/bin/python3.7"

RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash -
RUN apt-get install -y nodejs && npm install --global yarn

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
#  * Use OPENTRONS_SOURCE_DOWNLOAD_LOCATION for build arg

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

####################
# opentrons-source #
####################

FROM python-base as opentrons-source
ARG OPENTRONS_SOURCE_DOWNLOAD_LOCATION
ADD $OPENTRONS_SOURCE_DOWNLOAD_LOCATION /opentrons.zip
RUN (cd / &&  \
    unzip -q opentrons.zip && \
    rm -f opentrons.zip && \
    mv opentrons* opentrons)
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

FROM opentrons-modules-source as thermocycler-builder
ENV OPENTRONS_HARDWARE "thermocycler"
RUN /entrypoint.sh build

FROM opentrons-source as driver-builder
RUN \
	(cd /opentrons/shared-data/python && python3 setup.py bdist_wheel -d /dist/) && \
    (cd /opentrons/api && python3 setup.py bdist_wheel -d /dist/) && \
    (cd /opentrons/notify-server && python3 setup.py bdist_wheel -d /dist/) && \
    (cd /opentrons/robot-server && python3 setup.py bdist_wheel -d /dist/)


#################
# Driver Common #
#################

# Added this driver-common image because all driver level emulator images are based off of
# the same source code build, it's just a different command that is ran for each.

FROM python-base as driver-common
RUN mkdir /dist
COPY --from=driver-builder /dist/* /dist/
RUN pip install /dist/*

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

FROM cpp-base as thermocycler-dev
ENV OPENTRONS_HARDWARE "thermocycler"

FROM python-base as tempdeck-driver-dev
ENV OPENTRONS_HARDWARE "tempdeck-driver"

FROM python-base as magdeck-driver-dev
ENV OPENTRONS_HARDWARE "magdeck-driver"

FROM python-base as thermocycler-driver-dev
ENV OPENTRONS_HARDWARE "thermocycler-driver"

FROM python-base as emulator-proxy-dev
ENV OPENTRONS_HARDWARE "emulator-proxy"

##############################################################
#                     PRODUCTION TARGETS                     #
##############################################################

# Targets for all production builds of emulators
# Make sure to include the OPENTRONS_HARDWARE env variable
# Each Production Target should copy in entrypoint.sh

#################################
# Firmware Production Emulators #
#################################

# Each Firmware Production Target should copy the executable from the Executable Builder target
# Each Firmware Production Target should have a corresponding Executable Builder target

FROM ubuntu-base as ot3-firmware-echo-prod
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"
COPY --from=ot3-echo-builder /ot3-firmware/build-host/can/simulator/can-simulator /ot3-firmware/build-host/can/simulator/can-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as heater-shaker-prod
ENV OPENTRONS_HARDWARE "heater-shaker"
COPY --from=heater-shaker-builder /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator /opentrons-modules/build-stm32-host/stm32-modules/heater-shaker/simulator/heater-shaker-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as thermocycler-prod
ENV OPENTRONS_HARDWARE "thermocycler"
COPY --from=thermocycler-builder /opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator /opentrons-modules/build-stm32-host/stm32-modules/thermocycler-refresh/simulator/thermocycler-refresh-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]


###############################
# Driver Production Emulators #
###############################

# All driver level emulators should be based off of driver-common

FROM driver-common as emulator-proxy-prod
ENV OPENTRONS_HARDWARE "emulator-proxy"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM driver-common as thermocycler-driver-prod
ENV OPENTRONS_HARDWARE "thermocycler-driver"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM driver-common as magdeck-driver-prod
ENV OPENTRONS_HARDWARE "magdeck-driver"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM driver-common as tempdeck-driver-prod
ENV OPENTRONS_HARDWARE "tempdeck-driver"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

