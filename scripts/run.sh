#!/bin/bash
./setup_can.sh
docker-compose -f ../docker-compose.yaml build
docker-compose -f ../docker-compose.yaml up
