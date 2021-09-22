#!/bin/bash
# This script will create a SocketCan network, vcan0

if [[ "$#" -eq 1 ]]; then
  NETWORK=$1
elif [ -z "${CAN_CHANNEL}" ]; then
  NETWORK="vcan0"
else
  NETWORK=${CAN_CHANNEL}
fi



sudo ip link add dev $NETWORK type vcan fd on
if [ $? == 2 ]; then
  echo "CAN Virtual Network \"$NETWORK\" already exists"
  exit 1
fi

sudo ip link set up $NETWORK

if [ $? == 0 ]; then
  echo "CAN Virtual Network \"$NETWORK\" successfully created"
else
  echo "Error creating CAN Virtual Network \"$NETWORK\""
fi

