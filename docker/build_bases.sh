#!/usr/bin/env bash
docker buildx build --file ./bases_Dockerfile --target ubuntu-base --push --tag ghcr.io/opentrons/ubuntu-base:latest .
docker buildx build --file ./bases_Dockerfile --target cpp-base --push --tag ghcr.io/opentrons/cpp-base:latest .
docker buildx build --file ./bases_Dockerfile --target python-base --push --tag ghcr.io/opentrons/python-base:latest .
