FROM ubuntu:20.04 as builder

ENV DEBIAN_FRONTEND noninteractive

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
    software-properties-common \
    clang-12

# Setup clang
RUN cd /usr/bin && ln -s /lib/llvm-12/bin/clang clang

# Install cmake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1.tar.gz && \
    tar -zxvf cmake-3.21.1.tar.gz

WORKDIR /cmake-3.21.1

RUN ./bootstrap
RUN make
RUN make install

# Clone and build our firmware repo
WORKDIR /

RUN git clone https://github.com/Opentrons/ot3-firmware.git

WORKDIR /ot3-firmware

RUN gcc --version

RUN git checkout can-simulator-vcan # temporary
RUN git pull

RUN cmake --preset host
#RUN cmake --build ./build_host --target can-simulator