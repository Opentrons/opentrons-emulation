FROM ubuntu:20.04 as builder

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
RUN git clone https://github.com/Opentrons/ot3-firmware.git

WORKDIR /ot3-firmware

RUN git checkout cmake-changes # temporary
RUN cmake --preset host-gcc10
RUN cmake --build ./build-host --target can-simulator

FROM builder as echo

WORKDIR /
COPY echo.sh echo.sh
CMD ["./echo.sh"]