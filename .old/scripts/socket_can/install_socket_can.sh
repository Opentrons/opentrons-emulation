#!/usr/bin/env bash

sudo apt-get install linux-modules-extra-$(uname -r)
sudo modprobe vcan