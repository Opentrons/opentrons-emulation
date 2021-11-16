#!/usr/bin/env bash

if [[ `uname -s` = "Linux" ]]; then
  printf "... Getting vagrant gpg key ...\\n"
  curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
  printf "... Adding vagrant repository ...\\n"
  sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main" >> /dev/null
  printf "... Installing vagrant ...\\n"
  sudo apt-get update >> /dev/null
  sudo apt-get install vagrant >> /dev/null

elif [[ "$(uname -s)" = 'Darwin' ]]; then
  printf "... Installing vagrant ...\\n"
  brew install vagrant

else
  printf "Could not determine system. This script only works for Mac and Linux\\n"
  exit 1
fi

printf "... Installing vagrant-vbguest plugin ...\\n"
vagrant plugin install vagrant-vbguest >> /dev/null