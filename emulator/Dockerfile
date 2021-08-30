FROM ubuntu:20.04 as base

ENV DEBIAN_FRONTEND noninteractive
ARG CLONE_LOCATION=/tmp/ot3-firmware/

RUN rm -rf /var/lib/apt/lists/*
RUN apt-get update
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
    software-properties-common

# Install cmake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1.tar.gz && \
    tar -zxvf cmake-3.21.1.tar.gz
RUN (cd /cmake-3.21.1 && ./bootstrap)
RUN (cd /cmake-3.21.1 && make)
RUN (cd /cmake-3.21.1 && make install)

# Build firmware
ADD ./ot3-firmware/ /ot3-firmware/
RUN (cd ot3-firmware && cmake --preset host-gcc10)
RUN (cd ot3-firmware && cmake --build ./build-host --target can-simulator)

FROM base as echo

COPY echo.sh echo.sh
ENTRYPOINT ["/echo.sh"]