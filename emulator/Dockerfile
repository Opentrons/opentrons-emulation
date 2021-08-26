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

WORKDIR /cmake-3.21.1

RUN ./bootstrap
RUN make
RUN make install

WORKDIR /
# This checks if there has been changes in the ot3 repo and if there has breaks the cache
ADD https://api.github.com/repos/opentrons/ot3-firmware/compare/main...HEAD /dev/null
RUN git clone https://github.com/Opentrons/ot3-firmware.git

WORKDIR /ot3-firmware

RUN cmake --preset host-gcc10
RUN cmake --build ./build-host --target can-simulator

FROM base as echo

WORKDIR /
COPY echo.sh echo.sh
CMD ["./echo.sh"]