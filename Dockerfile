###############
# UBUNTU BASE #
###############
# Lowest level build target that all other targets are based off of

FROM ubuntu:20.04 as ubuntu-base

ENV DEBIAN_FRONTEND noninteractive

RUN rm -rf /var/lib/apt/lists/*
RUN echo "Updating apt" && apt-get update > /dev/null
RUN apt-get install -y wget unzip

####################
# C++ MODULES BASE #
####################
# Contains common packages that all ot3-firmware and module firmware require

FROM ubuntu-base as cpp-base

RUN apt-get install -y \
    libgtest-dev \
    libboost-test-dev \
    build-essential \
    gcc-10 \
    g++-10 \
    libssl-dev \
    git \
    lsb-release \
    software-properties-common > /dev/null

# Install cmake
RUN wget -q https://github.com/Kitware/CMake/releases/download/v3.21.2/cmake-3.21.2-linux-x86_64.tar.gz && \
    tar -zxf cmake-3.21.2-linux-x86_64.tar.gz && \
    rm cmake-3.21.2-linux-x86_64.tar.gz && \
    mv cmake-3.21.2-linux-x86_64 cmake && \
    (cd /usr/bin/ && ln -s /cmake/bin/cmake cmake)

########################
# DEV FIRMWARE TARGETS #
########################
# Targets for all dev builds of emulators

FROM cpp-base as ot3-firmware-echo-dev
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"

FROM cpp-base as heater-shaker-dev
ENV OPENTRONS_HARDWARE "heater-shaker"

#########################
# PROD FIRMWARE TARGETS #
#########################
# Targets for all prod builds of emulators

FROM ot3-firmware-echo-dev as ot3-firmware-echo
ADD "https://github.com/Opentrons/ot3-firmware/archive/refs/heads/main.zip" /ot3-firmware.zip
RUN (cd / &&  \
    unzip -q ot3-firmware.zip && \
    rm -f ot3-firmware.zip && \
    mv ot3-firmware* ot3-firmware)
COPY entrypoint.sh /entrypoint.sh
RUN /entrypoint.sh build

FROM heater-shaker-dev as heater-shaker
ADD "https://github.com/Opentrons/opentrons-modules/archive/refs/heads/edge.zip" /opentrons-modules.zip
RUN (cd / &&  \
    unzip -q opentrons-modules.zip && \
    rm -f opentrons-modules.zip && \
    mv opentrons-modules* opentrons-modules)
COPY entrypoint.sh /entrypoint.sh
RUN /entrypoint.sh build
