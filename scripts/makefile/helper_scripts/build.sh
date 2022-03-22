#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

ARCH=`${SCRIPT_DIR}/get_untranslated_arch.sh`

FILE_PATH=$1


if [ "${ARCH}" == "arm64" ]; then
  # Platform is being set to linux/x86_64 because a requirement of M1 Mac is to use rosetta
  # Rosetta emulates a x86_64 architecture and then Docker uses that
  # Docker thinks it should be trying to build against an arm64 arch. So we have to override it.
  echo "On arm64 specifying platform in build command."
  docker buildx bake --file ${FILE_PATH} --progress=plain --set *.platform=linux/x86_64
else
  docker buildx bake --file ${FILE_PATH} --progress=plain
fi
