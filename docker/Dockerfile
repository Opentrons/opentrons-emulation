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

# python-base:
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
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && \
    apt-get install \
    --no-install-recommends \
    -y \
    libgtest-dev \
    libboost-test-dev \
    gcc-10 \
    g++-10 \
    lsb-release \
    python3.7 \
    python3.7-venv \
    > /dev/null
RUN (cd /usr/bin/ && ln -s /usr/bin/python3.7 python)
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
#                       LOCAL TARGETS                       #
#############################################################

# Targets for all development builds of emulators
# All source code should be bind-mounted in, so do not copy it in.
# entrypoint.sh should also be bind-mounted in so do not copy it in either
# Make sure to include the OPENTRONS_HARDWARE env variable

FROM cpp-base as local-cpp-base
COPY run.sh /run.sh
ENTRYPOINT ["/run.sh"]

FROM python-base as local-python-base
COPY run.sh /run.sh
ENTRYPOINT ["/run.sh"]

############################
# Hardware Local Emulators #
############################

FROM local-cpp-base as heater-shaker-hardware-local
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"

FROM local-cpp-base as thermocycler-hardware-local
ENV OPENTRONS_HARDWARE "thermocycler-hardware"

FROM local-cpp-base as ot3-pipettes-hardware-local
ENV OPENTRONS_HARDWARE "ot3-pipettes-hardware"

FROM local-cpp-base as ot3-head-hardware-local
ENV OPENTRONS_HARDWARE "ot3-head-hardware"

FROM local-cpp-base as ot3-gantry-x-hardware-local
ENV OPENTRONS_HARDWARE "ot3-gantry-x-hardware"

FROM local-cpp-base as ot3-gantry-y-hardware-local
ENV OPENTRONS_HARDWARE "ot3-gantry-y-hardware"

############################
# Firmware Local Emulators #
############################

FROM local-python-base as thermocycler-firmware-local
ENV OPENTRONS_HARDWARE "thermocycler-firmware"

FROM local-python-base as magdeck-firmware-local
ENV OPENTRONS_HARDWARE "magdeck-firmware"

FROM local-python-base as tempdeck-firmware-local
ENV OPENTRONS_HARDWARE "tempdeck-firmware"

FROM local-python-base as emulator-proxy-local
ENV OPENTRONS_HARDWARE "emulator-proxy"

FROM local-python-base as robot-server-local
ENV OPENTRONS_HARDWARE "robot-server"

FROM local-python-base as smoothie-local
ENV OPENTRONS_HARDWARE "smoothie"

FROM local-python-base as can-server-local
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
#  * Based off of python-base
#  * Contains opentrons source and entrypoint.sh

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
# The Exectuable Builder should build the executable file and the Production Target should copy over the executable file
# from the executable builder target
# Building separately from the Production Target to reduce image size

FROM opentrons-modules-source as heater-shaker-builder
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"
RUN /entrypoint.sh build

FROM opentrons-modules-source as thermocycler-builder
ENV OPENTRONS_HARDWARE "thermocycler-hardware"
RUN /entrypoint.sh build

FROM opentrons-source as python-emulator-builder
ENV OPENTRONS_HARDWARE "common-firmware"
RUN /entrypoint.sh build

FROM ot3-firmware-source as ot3-firmware-builder
ENV OPENTRONS_HARDWARE "common-ot3-firmware"
RUN /entrypoint.sh build

##################
# Firmware Common #
##################

# Added this firmware-common image because all firmware level emulator images are based off of
# the opentrons monorepo, it's just a different command that is ran for each.

FROM python-base as firmware-common
RUN mkdir /dist
COPY --from=python-emulator-builder /dist/* /dist/
RUN pip install /dist/*

##############################################################
#                       REMOTE TARGETS                       #
##############################################################

# Targets for all remote builds of emulators
# Make sure to include the OPENTRONS_HARDWARE env variable
# Each Remote Target should copy in entrypoint.sh

#############################
# Hardware Remote Emulators #
#############################

# These emulators run C++ firmware code and emulate the hardware
# Each Hardware Production Target should copy the executable from the Executable Builder target
# Each Hardware Production Target should have a corresponding Executable Builder target

FROM ubuntu-base as ot3-pipettes-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-pipettes-hardware"
COPY --from=ot3-firmware-builder /pipettes-simulator /pipettes-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as ot3-head-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-head-hardware"
COPY --from=ot3-firmware-builder /head-simulator /head-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as ot3-gantry-x-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-gantry-x-hardware"
COPY --from=ot3-firmware-builder /gantry-x-simulator /gantry-x-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as ot3-gantry-y-hardware-remote
ENV OPENTRONS_HARDWARE "ot3-gantry-y-hardware"
COPY --from=ot3-firmware-builder /gantry-y-simulator /gantry-y-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as heater-shaker-hardware-remote
ENV OPENTRONS_HARDWARE "heater-shaker-hardware"
COPY --from=heater-shaker-builder /heater-shaker-simulator /heater-shaker-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM ubuntu-base as thermocycler-hardware-remote
ENV OPENTRONS_HARDWARE "thermocycler-hardware"
COPY --from=thermocycler-builder /thermocycler-refresh-simulator /thermocycler-refresh-simulator
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

#################################
# Firmware Production Emulators #
#################################

# There emulators run python driver code and emulator the firmware
# All Firmware level emulators should be based off of firmware-common

FROM firmware-common as thermocycler-firmware-remote
ENV OPENTRONS_HARDWARE "thermocycler-firmware"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as magdeck-firmware-remote
ENV OPENTRONS_HARDWARE "magdeck-firmware"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as tempdeck-firmware-remote
ENV OPENTRONS_HARDWARE "tempdeck-firmware"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as emulator-proxy-remote
ENV OPENTRONS_HARDWARE "emulator-proxy"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as robot-server-remote
ENV OPENTRONS_HARDWARE "robot-server"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as smoothie-remote
ENV OPENTRONS_HARDWARE "smoothie"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]

FROM firmware-common as can-server-remote
ENV OPENTRONS_HARDWARE "can-server"
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh", "run"]
