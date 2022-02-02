#!/usr/bin/env bash

modprobe vcan

NUM_SOCKET_CAN_NETWORKS=$(expr $NUM_SOCKET_CAN_NETWORKS - 1)

for i in $(seq 0 $NUM_SOCKET_CAN_NETWORKS); do
  ip link add dev vcan${i} type vcan fd on
  ip link set up vcan${i}
done