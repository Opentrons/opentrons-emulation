#!/usr/bin/env bash

ARCH=`arch`

FILE_PATH=$1

if [ "${ARCH}" == "x86_64" ]; then
  docker buildx bake --file ${FILE_PATH}
elif [ "${ARCH}" == "arm64" ]; then
  docker buildx bake --file ${FILE_PATH} --set *.platform=linux/x86_64
else
  echo "${ARCH} architecture not supported."
  exit 1
fi
