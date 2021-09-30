FROM ubuntu:20.04 as ubuntu-base

ENV DEBIAN_FRONTEND noninteractive

RUN rm -rf /var/lib/apt/lists/*
RUN echo "Updating apt" && apt-get update > /dev/null
RUN apt-get install -y wget unzip


####################
# C++ MODULES BASE #
####################

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

###############
# SOURCE CODE #
###############

FROM ubuntu-base as firmware-source
ADD "https://github.com/Opentrons/ot3-firmware/archive/refs/heads/main.zip" /ot3-firmware.zip
RUN (cd / &&  \
    unzip -q ot3-firmware.zip && \
    rm -f ot3-firmware.zip && \
    mv ot3-firmware* ot3-firmware)

FROM ubuntu-base as modules-source
ADD "https://github.com/Opentrons/opentrons-modules/archive/refs/heads/edge.zip" /opentrons-modules.zip

RUN (cd / &&  \
    unzip -q opentrons-modules.zip && \
    rm -f opentrons-modules.zip && \
    mv opentrons-modules* opentrons-modules)


#######################
# DEV FIRMWARE BUILDS #
#######################

FROM cpp-base as ot3-firmware-echo
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"

FROM cpp-base as heater-shaker
ENV OPENTRONS_HARDWARE "heater-shaker"

########################
# PROD FIRMWARE BUILDS #
########################

FROM ot3-firmware-echo as ot3-firmware-echo-prod
COPY --from=firmware-source /ot3-firmware/ /ot3-firmware/
#COPY entrypoint.sh /entrypoint.sh
#RUN /entrypoint.sh build

FROM heater-shaker as heater-shaker-prod
COPY --from=modules-source /opentrons-modules/ /opentrons-modules/
#COPY entrypoint.sh /entrypoint.sh
#RUN /entrypoint.sh build