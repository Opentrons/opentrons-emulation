#!/usr/bin/env bash

add-apt-repository ppa:deadsnakes/ppa
apt-get update
apt-get install -y \
  pipenv \
  make \
  build-essential \
  libssl-dev \
  zlib1g-dev \
  libbz2-dev \
  libreadline-dev \
  libsqlite3-dev \
  wget curl llvm \
  libncursesw5-dev \
  xz-utils tk-dev \
  libxml2-dev \
  libxmlsec1-dev \
  libffi-dev \
  liblzma-dev \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  linux-modules-extra-$(uname -r) \
  python3.7

(cd /usr/bin/ && ln -s /usr/bin/python3.7 python)
#(cd /home/vagrant/opentrons-emulation/emulation_system && sudo -u vagrant make setup)
