#!/bin/bash
# This script will create a SocketCan network, vcan0

sudo ip link add dev vcan0 type vcan 2> /dev/null
if [ $? == 2 ]; then
  echo "CAN Virtual Network already exists"
  exit 1
fi

sudo ip link set up vcan0

if [ $? == 0 ]; then
  echo "CAN Virtual Network successfully created"
else
  echo "Error creating CAN Virtual Network"
fi

