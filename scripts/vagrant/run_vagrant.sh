#!/usr/bin/env bash
set -o nounset
set -o errexit
trap 'echo "Aborting due to errexit on line $LINENO. Exit code: $?" >&2' ERR
set -o errtrace
set -o pipefail
IFS=$'\n\t'
_ME="$(basename "${0}")"
_SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


# _exit_1()
#
# Usage:
#   _exit_1 <command>
#
# Description:
#   Exit with status 1 after executing the specified command with output
#   redirected to standard error. The command is expected to print a message
#   and should typically be either `echo`, `printf`, or `cat`.
_exit_1() {
  {
    printf "%s " "$(tput setaf 1)!$(tput sgr0)"
    "${@}"
  } 1>&2
  exit 1
}

# _warn()
#
# Usage:
#   _warn <command>
#
# Description:
#   Print the specified command with output redirected to standard error.
#   The command is expected to print a message and should typically be either
#   `echo`, `printf`, or `cat`.
_warn() {
  {
    printf "%s " "$(tput setaf 1)!$(tput sgr0)"
    "${@}"
  } 1>&2
}

###############################################################################
# Help
###############################################################################

_print_help() {
  cat <<HEREDOC
      _                 _
  ___(_)_ __ ___  _ __ | | ___
 / __| | '_ \` _ \\| '_ \\| |/ _ \\
 \\__ \\ | | | | | | |_) | |  __/
 |___/_|_| |_| |_| .__/|_|\\___|
                 |_|
Boilerplate for creating a simple bash script with some basic strictness
checks and help features.
Usage:
  ${_ME} install        Install Vagrant
  ${_ME} prod           Create production VM
  ${_ME} dev            Create development VM
  ${_ME} -h | --help    Print this help message
Options:
  -h --help  Show this screen.
HEREDOC
}

###############################################################################
# Program Functions
###############################################################################

_install_vagrant() {

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
    _exit_1 printf "Could not determine system. This script only works for Mac and Linux\\n"
  fi

  printf "... Installing vagrant-vbguest plugin ...\\n"
  vagrant plugin install vagrant-vbguest >> /dev/null

  if ! [ -f "${_SCRIPT_DIR}/Vagrantfile" ]; then
    printf "... Vagrantfile does not exist. Making copy of sample.Vagrantfile and naming it Vagrantfile ...\\n"
    cp "${_SCRIPT_DIR}/sample.Vagrantfile" Vagrantfile
    printf "\\nMake sure to update source code mount paths in Vagrantfile if you will be running VM in dev mode.\\n"
  fi

}

_setup_vm() {
  printf "Hello World"
}

_check_for_vagrantfile() {
  if ! [[ -f "${_SCRIPT_DIR}/Vagrantfile" ]]; then
    _exit_1 printf "Vagrantfile does not exist in vagrant directory. \\nDid you duplicate sample.Vagrantfile as Vagrantfile?\\n"
  fi
}

_bring_up_prod_vm() {
    _check_for_vagrantfile
    vagrant destroy prod -f
    vagrant up prod
}

_bring_up_prod_emulator() {
  vagrant ssh prod -c "/opentrons-emulation/scripts/run_emulation.sh --prod --headless"
}

_bring_up_dev_vm() {
    _check_for_vagrantfile
    vagrant destroy dev -f
    vagrant up dev
}

_bring_up_dev_emulator() {
  vagrant ssh dev -c "/opentrons-emulation/scripts/run_emulation.sh --dev --headless"
}

_set_default_env() {
  printf "Copying .env.vagrant to .env"
  cp "${_SCRIPT_DIR}/../../.env.vagrant" ${_SCRIPT_DIR}/../../.env
}

###############################################################################
# Main
###############################################################################

# _main()
#
# Usage:
#   _main [<options>] [<arguments>]
#
# Description:
#   Entry point for the program, handling basic option parsing and dispatching.
_main() {
  # Avoid complex option parsing when only one program option is expected.
  if [[ "${1:-}" =~ ^-h|--help$  ]]; then
    _print_help
    exit 0
  fi

  if [[ "$1"  = 'install' ]]; then
    if ! [[ -x "$(command -v vagrant)" ]]; then
      printf "Vagrant is not installed. Installing now\\n\n"
      _install_vagrant "$@"
    else
      printf "Vagrant already installed. Skipping installation\\n"
    fi

  elif [[ "$1"  = 'prod_vm' ]]; then
    _bring_up_prod_vm

  elif [[ "$1"  = 'dev_vm' ]]; then
    _bring_up_dev_vm

  elif [[ "$1"  = 'prod_em' ]]; then
    _bring_up_prod_emulator

  elif [[ "$1"  = 'dev_em' ]]; then
    _bring_up_dev_emulator

  elif [[ "$1"  = 'set_default_env' ]]; then
    _set_default_env
  fi


}

# Call `_main` after everything has been defined.
_main "$@"

# This file is based off of https://github.com/xwmx/bash-boilerplate/blob/master/bash-simple in https://github.com/xwmx/bash-boilerplate
# Below is the license for the repo
#The MIT License (MIT)
#
#Copyright (c) 2014 William Melody
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.