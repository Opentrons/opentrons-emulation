#!/usr/bin/env bash

arch_name=$(uname -m)
if [[ ${arch_name} == "x86_64" ]]; then
  arch_to_use="amd64"
else
  arch_to_use="arm64"
fi

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
MODDED_BASES_DOCKERFILE=`sed \
  -e "s;ubuntu-base;ubuntu-base-dev;g" \
  -e "s;python-base;python-base-dev;g" \
  -e "s;cpp-base;cpp-base-dev;g" \
  ${SCRIPT_DIR}/../../docker/bases_Dockerfile`

MODDED_DOCKERFILE=`sed \
  -e 's;ghcr.io/opentrons/ubuntu-base-${TARGETARCH}:latest;ubuntu-base-dev-'${arch_to_use}';g' \
  -e 's;ghcr.io/opentrons/cpp-base-${TARGETARCH}:latest;cpp-base-dev-'${arch_to_use}';g' \
  -e "s;ghcr.io/opentrons/python-base:latest;python-base-dev;g" \
  -e "s;ghcr.io/opentrons/cpp-base:latest;cpp-base-dev;g" \
  ${SCRIPT_DIR}/../../docker/Dockerfile`

printf "${MODDED_BASES_DOCKERFILE}\n\n${MODDED_DOCKERFILE}" > ${SCRIPT_DIR}/../../docker/dev_Dockerfile
