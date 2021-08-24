#!/bin/bash
./scripts/setup_can.sh
docker-compose build
docker-compose up
