FROM ubuntu:20.04 as base

ENV DEBIAN_FRONTEND noninteractive

RUN rm -rf /var/lib/apt/lists/*
RUN echo "Updating apt" && apt-get update > /dev/null
RUN apt-get install -y \
    libgtest-dev \
    libboost-test-dev \
    wget \
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

###################
# FIRMWARE BUILDS #
###################

FROM base as ot3-firmware-echo
ENV OPENTRONS_HARDWARE "ot3-firmware-echo"

FROM base as heater-shaker
ENV OPENTRONS_HARDWARE "heater-shaker"


