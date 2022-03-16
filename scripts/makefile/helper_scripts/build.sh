#!/usr/bin/env bash

ARCH=`arch`

FILE_PATH=$1


if [ "${ARCH}" == "arm64" ]; then
  docker buildx bake --file ${FILE_PATH} --set *.platform=linux/x86_64
else
  docker buildx bake --file ${FILE_PATH}
fi
