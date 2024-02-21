#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Set bin directory
BIN_DIR="$SCRIPT_DIR/../bin"

# Set download directory
DOWNLOAD_DIR="$BIN_DIR/mosquitto-source/downloads"

# Set build directory
BUILD_DIR="$BIN_DIR/mosquitto-source/build"

# Create directories if they do not exist
mkdir -p "$DOWNLOAD_DIR"
mkdir -p "$BUILD_DIR"

# Change to bin directory
cd "$BIN_DIR"

# Download and extract Mosquitto source
if [ ! -f "$DOWNLOAD_DIR/mosquitto-2.0.18.tar.gz" ]; then
    wget https://mosquitto.org/files/source/mosquitto-2.0.18.tar.gz -P "$DOWNLOAD_DIR"
fi

if [ -f "$DOWNLOAD_DIR/mosquitto-2.0.18.tar.gz" ]; then
    tar -xzf "$DOWNLOAD_DIR/mosquitto-2.0.18.tar.gz" -C "$BUILD_DIR"
    mv "$BUILD_DIR/mosquitto-2.0.18" "$BUILD_DIR/mosquitto"
else
    echo "Failed to download Mosquitto source file."
    exit 1
fi

# Check if the OS is Linux
if [[ "$(uname)" == "Linux" ]]; then
    # Install dependencies using apt
    sudo apt update
    sudo apt install -y build-essential libc-ares-dev libssl-dev libwebsockets-dev uuid-dev xsltproc wget libcjson-dev libpthread-stubs0-dev

    # Build Mosquitto
    cd "$BUILD_DIR/mosquitto"
    make -j$(nproc) WITH_WEBSOCKETS=yes WITH_DOCS=no binary
fi

# Check if the OS is macOS
if [[ "$(uname)" == "Darwin" ]]; then
    # Install dependencies using brew
    brew install cmake
    brew install openssl
    brew install libwebsockets
    brew install ossp-uuid
    brew install wget

    # Build Mosquitto
    cd "$BUILD_DIR/mosquitto"
    cmake -DCMAKE_MODULE_LINKER_FLAGS="-undefined dynamic_lookup" .
    WITH_WEBSOCKETS=yes WITH_DOCS=no cmake --build .
fi

    # Move mosquitto binary to bin directory
    mv "$BUILD_DIR/mosquitto/src/mosquitto" "$BIN_DIR"

    # Move mosquitto.conf to bin directory
    mv "$BUILD_DIR/mosquitto/mosquitto.conf" "$BIN_DIR"
