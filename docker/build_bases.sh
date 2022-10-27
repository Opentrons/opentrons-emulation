#!/usr/bin/env bash

if [ $# -lt 1 ]; then
  echo "Must provide \"branch_name\""
  echo "Usage: $(basename "${BASH_SOURCE[0]}") <branch_name>"
  exit 1
fi

BRANCH_NAME=$1

if [[ "${BRANCH_NAME}" =~ release-v.* ]]; then
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target ubuntu-base-amd64 \
  --platform=linux/amd64 \
  --tag ghcr.io/opentrons/ubuntu-base-amd64:latest \
  --tag ghcr.io/opentrons/ubuntu-base-amd64:${BRANCH_NAME} \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target ubuntu-base-arm64 \
  --platform=linux/arm64 \
  --tag ghcr.io/opentrons/ubuntu-base-arm64:latest \
  --tag ghcr.io/opentrons/ubuntu-base-arm64:${BRANCH_NAME} \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target cpp-base-amd64 \
  --platform=linux/amd64 \
  --tag ghcr.io/opentrons/cpp-base-amd64:latest \
  --tag ghcr.io/opentrons/cpp-base-amd64:${BRANCH_NAME} \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target cpp-base-arm64 \
  --platform=linux/arm64 \
  --tag ghcr.io/opentrons/cpp-base-arm64:latest \
  --tag ghcr.io/opentrons/cpp-base-arm64:${BRANCH_NAME} \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target python-base \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/python-base:latest \
  --tag ghcr.io/opentrons/python-base:${BRANCH_NAME} \
  .
else
    docker buildx build \
    --push \
  --file ./bases_Dockerfile \
  --target ubuntu-base-amd64 \
  --platform=linux/amd64 \
  --tag ghcr.io/opentrons/ubuntu-base-amd64:latest \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target ubuntu-base-arm64 \
  --platform=linux/arm64 \
  --tag ghcr.io/opentrons/ubuntu-base-arm64:latest \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target cpp-base-amd64 \
  --platform=linux/amd64 \
  --tag ghcr.io/opentrons/cpp-base-amd64:latest \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target cpp-base-arm64 \
  --platform=linux/arm64 \
  --tag ghcr.io/opentrons/cpp-base-arm64:latest \
  .
  docker buildx build \
  --push \
  --file ./bases_Dockerfile \
  --target python-base \
  --platform=linux/amd64,linux/arm64 \
  --tag ghcr.io/opentrons/python-base:latest \
  .
fi
