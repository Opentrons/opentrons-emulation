#!/usr/bin/env bash

ARCH=`arch`

FILE_PATH=$1


if [ "${ARCH}" == "arm64" ]; then
  # Platform is being set to linux/x86_64 because a requirement of M1 Mac is to use rosetta
  # Rosetta emulates a x86_64 architecture and then Docker uses that
  # Docker thinks it should be trying to build against an arm64 arch. So we have to override it.
  docker buildx bake --file ${FILE_PATH} --set *.platform=linux/x86_64
else
  docker buildx bake --file ${FILE_PATH}
fi
