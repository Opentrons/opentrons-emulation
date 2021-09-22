#!/bin/bash
# This script will delete SocketCan network vcan0

if [ -z "${CAN_CHANNEL}" ]; then
  NETWORK="vcan0"
else
  NETWORK=${CAN_CHANNEL}
fi


sudo ip link delete $NETWORK 2> /dev/null
if [ $? == 1 ]; then
  echo "CAN Virtual Network \"$NETWORK\" does not exist"
  exit 1
fi

echo "CAN Virtual Network \"$NETWORK\" successfully removed"