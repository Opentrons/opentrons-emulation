#!/usr/bin/env bash

set -o nounset
set -o errexit
set -o errtrace
set -o pipefail

IFS=$'\n\t'

###############################################################################
# Environment
###############################################################################

# $_ME
#
# This program's basename.
_ME="$(basename "${0}")"

###############################################################################
# Debug
###############################################################################

# _debug()
#
# Usage:
#   _debug <command> <options>...
#
# Description:
#   Execute a command and print to standard error. The command is expected to
#   print a message and should typically be either `echo`, `printf`, or `cat`.
#
# Example:
#   _debug printf "Debug info. Variable: %s\\n" "$0"
__DEBUG_COUNTER=0
_debug() {
  if ((${_USE_DEBUG:-0}))
  then
    __DEBUG_COUNTER=$((__DEBUG_COUNTER+1))
    {
      # Prefix debug message with "bug (U+1F41B)"
      printf "🐛  %s " "${__DEBUG_COUNTER}"
      "${@}"
      printf "―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\\n"
    } 1>&2
  fi
}

###############################################################################
# Error Messages
###############################################################################

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

# _print_help()
#
# Usage:
#   _print_help
#
# Description:
#   Print the program help information.
_print_help() {
  cat <<HEREDOC

 __   __   ___      ___  __   __        __
/  \ |__) |__  |\ |  |  |__) /  \ |\ | /__\`
\__/ |    |___ | \|  |  |  \ \__/ | \| .__/

 ___                      ___    __
|__   |\/| |  | |     /\   |  | /  \ |\ |
|___  |  | \__/ |___ /~~\  |  | \__/ | \|


Script for bringing up emulated Opentrons hardware.

Usage:
  ${_ME} -h | --help
  ${_ME} --prod [--ot3-firmware-sha <sha>] [--modules-sha <sha>] [--headless]
  ${_ME} --dev [--headless]

Options:
  -h --help           Display this help information.
  --prod              Run as production system
  --dev               Run as development system
  --headless          Run system headless
  --ot3-firmware-sha  Full commit sha to base the ot3-firmware repo off of
  --modules-sha       Full commit sha to base the opentrons-modules repo off of
  -v --verbose        Show more output
HEREDOC
}

###############################################################################
# Parse Options
###############################################################################

# Initialize program option variables.
_PRINT_HELP=0
_USE_DEBUG=0

# Initialize additional expected option variables.
_HEADLESS=0
_DEV=0
_PROD=0
_VERBOSE=0
_SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
_COMPOSE_FILE_NAME=
_DEFAULT_OT3_FIRMWARE_DOWNLOAD_LOCATION="https://github.com/Opentrons/ot3-firmware/archive/refs/heads/main.zip"
_DEFAULT_MODULES_DOWNLOAD_LOCATION="https://github.com/Opentrons/opentrons-modules/archive/refs/heads/edge.zip"
_OT3_FIRMWARE=${_DEFAULT_OT3_FIRMWARE_DOWNLOAD_LOCATION}
_MODULES=${_DEFAULT_MODULES_DOWNLOAD_LOCATION}

# __get_option_value()
#
# Usage:
#   __get_option_value <option> <value>
#
# Description:
#  Given a flag (e.g., -e | --example) return the value or exit 1 if value
#  is blank or appears to be another option.
__get_option_value() {
  local __arg="${1:-}"
  local __val="${2:-}"

  if [[ -n "${__val:-}" ]] && [[ ! "${__val:-}" =~ ^- ]]
  then
    printf "%s\\n" "${__val}"
  else
    _exit_1 printf "%s requires a valid argument.\\n" "${__arg}"
  fi
}

while ((${#}))
do
  __arg="${1:-}"
  __val="${2:-}"

  case "${__arg}" in
    -h|--help)
      _PRINT_HELP=1
      ;;
    --debug)
      _USE_DEBUG=1
      ;;
    --headless)
      _HEADLESS=1
      ;;
    --dev)
      _DEV=1
      _COMPOSE_FILE_NAME="docker-compose-dev.yaml"
      ;;
    --prod)
      _PROD=1
      _COMPOSE_FILE_NAME="docker-compose.yaml"
      ;;
    --ot3-firmware-sha)
      _FIRMWARE_TEMP_VAL=$(__get_option_value "${__arg}" "${__val:-}")
      if ! [[ ${_FIRMWARE_TEMP_VAL} = "latest" ]]; then
        _OT3_FIRMWARE="https://github.com/Opentrons/ot3-firmware/archive/${_FIRMWARE_TEMP_VAL}.zip"
      fi
      shift
      ;;
    --modules-sha)
      _MODULES_TEMP_VAL=$(__get_option_value "${__arg}" "${__val:-}")
      if ! [[ $_MODULES_TEMP_VAL = "latest" ]]; then
        _MODULES="https://github.com/Opentrons/opentrons-modules/archive/${_MODULES_TEMP_VAL}.zip"
      fi
      shift
      ;;
    -v|--verbose)
      _VERBOSE=1
      ;;
    --endopts)
      # Terminate option parsing.
      break
      ;;
    -*)
      _exit_1 printf "Unexpected option: %s\\n" "${__arg}"
      ;;
  esac

  shift
done

###############################################################################
# Program Functions
###############################################################################

_use_debug() {
  _HEADLESS_DEBUG_MESSAGE="HEADLESS OPTION:"
  _DEV_DEBUG_MESSAGE="DEV OPTION: Running in"
  _OT3_FIRMWARE_DEBUG_MESSAGE="OT3_FIRMWARE: Pulling"
  _MODULES_DEBUG_MESSAGE="MODULES:"
  _VERBOSE_DEBUG_MESSAGE="VERBOSE: Running in"

  if (( _HEADLESS )); then
    _HEADLESS_DEBUG_MESSAGE="${_HEADLESS_DEBUG_MESSAGE} Running headless\\n"
  else
    _HEADLESS_DEBUG_MESSAGE="${_HEADLESS_DEBUG_MESSAGE} Running with logs printing to stdout\\n"
  fi

  if (( _DEV )); then
    _DEV_DEBUG_MESSAGE="${_DEV_DEBUG_MESSAGE} development mode\\n"
  else
    _DEV_DEBUG_MESSAGE="${_DEV_DEBUG_MESSAGE} production mode\\n"
  fi

  if (( _VERBOSE )); then
    _VERBOSE_DEBUG_MESSAGE="${_VERBOSE_DEBUG_MESSAGE} verbose mode\\n"
  else
    _VERBOSE_DEBUG_MESSAGE="${_VERBOSE_DEBUG_MESSAGE} quiet mode\\n"
  fi

  if [[ -n "${_OT3_FIRMWARE}" ]];  then
    _OT3_FIRMWARE_DEBUG_MESSAGE="${_OT3_FIRMWARE_DEBUG_MESSAGE} commit \"${_OT3_FIRMWARE}\" from ot3-firmware\\n"
  else
    _OT3_FIRMWARE_DEBUG_MESSAGE="${_OT3_FIRMWARE_DEBUG_MESSAGE} main from ot3-firmware\\n"
  fi

  if [[ -n "${_MODULES}" ]]; then
    _MODULES_DEBUG_MESSAGE="${_MODULES_DEBUG_MESSAGE} Pulling commit \"${_MODULES}\" from opentrons-modules\\n"
  else
    _MODULES_DEBUG_MESSAGE="${_MODULES_DEBUG_MESSAGE} Pulling edge from opentrons-modules\\n"
  fi
  _debug printf "${_HEADLESS_DEBUG_MESSAGE}"
  _debug printf "${_DEV_DEBUG_MESSAGE}"
  _debug printf "${_VERBOSE_DEBUG_MESSAGE}"
  _debug printf "${_OT3_FIRMWARE_DEBUG_MESSAGE}"
  _debug printf "${_MODULES_DEBUG_MESSAGE}"
}

_construct_build_command() {
  _BUILD_COMMAND="COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose --verbose -f ${_COMPOSE_FILE_PATH} build "

  if (( ! _VERBOSE )); then
    _BUILD_COMMAND="${_BUILD_COMMAND} --quiet"
  fi

  if [[ -n "${_OT3_FIRMWARE}" ]];  then
    _BUILD_COMMAND="${_BUILD_COMMAND} --build-arg FIRMWARE_SOURCE_DOWNLOAD_LOCATION=\"${_OT3_FIRMWARE}\""
  fi

  if [[ -n "${_MODULES}" ]]; then
    _BUILD_COMMAND="${_BUILD_COMMAND} --build-arg MODULE_SOURCE_DOWNLOAD_LOCATION=\"${_MODULES}\""
  fi

    if (( _VERBOSE )); then
      printf "BUILD COMMAND: ${_BUILD_COMMAND}\\n"
    fi
}

_teardown_can_network() {
  ${_SCRIPT_DIR}/teardown_can.sh
}

_setup_can_network() {
  ${_SCRIPT_DIR}/setup_can.sh
}

_remove_existing_docker_containers() {
  docker-compose -f ${_COMPOSE_FILE_PATH} rm -fs
}

_build_docker_images() {
  eval ${_BUILD_COMMAND}
}

_bring_up_docker_containers() {
  if (( _HEADLESS )); then
    docker-compose -f ${_COMPOSE_FILE_PATH} up -d
  else
    docker-compose -f ${_COMPOSE_FILE_PATH} up
  fi
}

_build_system() {
  _COMPOSE_FILE_PATH="${_SCRIPT_DIR}/../${_COMPOSE_FILE_NAME}"
  _construct_build_command
  _build_docker_images
  _teardown_can_network
  _setup_can_network
  _remove_existing_docker_containers
  _bring_up_docker_containers
}

###############################################################################
# Input Validation Functions
###############################################################################

_check_env_file_exists() {
    if [[ ! -f "${_SCRIPT_DIR}/../.env" ]]; then
          _exit_1 printf ".env file does not exist. \\nPlease copy .env.default to .env and modify fields\\n"
    fi
}

_check_env_file_different_from_default_env() {
    if cmp --silent -- "${_SCRIPT_DIR}/../.env" "${_SCRIPT_DIR}/../.env.default" ; then
      _warn printf ".env file and .env.default have the same content. \\nDid you update the values in .env to be valid?\\n\\n"
    fi
}

_check_for_print_help() {
    if (( _PRINT_HELP )); then
      _print_help
    fi
}

_check_prod_and_dev_not_both_specified() {
    if (( _PROD && _DEV )); then
      _exit_1 printf "Cannot specify --prod and --dev at the same time\\n"
    fi
}

_check_prod_or_dev_specified() {
    if [[ ${_PROD} -eq 0 && ${_DEV} -eq 0 ]]; then
      _exit_1 printf "Must specify either --prod or --dev\\n"
    fi
}

_check_commit_sha_not_specified_in_dev_mode() {
    if [[ ${_DEV} -eq 1 && ( -n "${_OT3_FIRMWARE}" || -n "${_MODULES}" ) ]]; then
      _exit_1 printf "Cannot specify --dev with either --ot3-firmware-sha or --modules-sha\\n"
    fi
}

_check_for_debug_mode() {
    if (( _USE_DEBUG )); then
      _use_debug
    fi
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
  _check_env_file_exists
  _check_env_file_different_from_default_env
  _check_for_print_help
  _check_prod_and_dev_not_both_specified
  _check_prod_or_dev_specified
  _check_commit_sha_not_specified_in_dev_mode
  _check_for_debug_mode
  _build_system "$@"

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