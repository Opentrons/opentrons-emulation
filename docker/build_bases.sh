#!/usr/bin/env bash

if [ $# -lt 1 ]; then
  echo "Must provide \"branch_name\""
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <branch_name>"
  exit 1
fi

BRANCH_NAME=$1

if [[ "${BRANCH_NAME}" =~ release-v.* ]]; then
  docker buildx build \
  --file ./bases_Dockerfile \
  --target ubuntu-base \
  --push \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/ubuntu-base:latest \
  --tag ghcr.io/opentrons/ubuntu-base:${BRANCH_NAME} \
  .
  docker buildx build \
  --file ./bases_Dockerfile \
  --target cpp-base \
  --push \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/cpp-base:latest \
  --tag ghcr.io/opentrons/cpp-base:${BRANCH_NAME} \
  .
  docker buildx build \
  --file ./bases_Dockerfile \
  --target python-base \
  --push \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/python-base:latest \
  --tag ghcr.io/opentrons/python-base:${BRANCH_NAME} \
  .
else
  docker buildx build \
  --file ./bases_Dockerfile \
  --target ubuntu-base \
  --push \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/ubuntu-base:latest .
  docker buildx build \
  --file ./bases_Dockerfile \
  --target cpp-base \
  --push \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/cpp-base:latest .
  docker buildx build \
  --file ./bases_Dockerfile \
  --target python-base \
  --push \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/python-base:latest .
fi
