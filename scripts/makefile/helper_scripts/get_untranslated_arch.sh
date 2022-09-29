#!/usr/bin/env bash

# Have to write this script because Mac M1 is confusing
# If you are running your shell on a mac in Rosetta, the arch command will return x86_64.
# This causes problems if you are trying to perform an action based on what the arch command returns

arch_name=$(uname -m)
os_name=$(uname)

if [[ ${os_name} == "Darwin" ]] && [[ ${arch_name} == "x86_64" ]] && [[ $(sysctl -in sysctl.proc_translated) == "1" ]]; then
    arch_name="arm64"
fi

echo ${arch_name}
