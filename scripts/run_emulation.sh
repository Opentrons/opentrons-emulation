#!/usr/bin/env bash
#       _                 _
#   ___(_)_ __ ___  _ __ | | ___   _
#  / __| | '_ ` _ \| '_ \| |/ _ \_| |_
#  \__ \ | | | | | | |_) | |  __/_   _|
#  |___/_|_| |_| |_| .__/|_|\___| |_|
#                  |_|
#
# Boilerplate for creating a simple bash script with some basic strictness
# checks, help features, easy debug printing.
#
# Usage:
#   bash-simple-plus <options>...
#
# Depends on:
#  list
#  of
#  programs
#  expected
#  in
#  environment
#
# Bash Boilerplate: https://github.com/xwmx/bash-boilerplate
#
# Copyright (c) 2015 William Melody • hi@williammelody.com

# Notes #######################################################################

# Extensive descriptions are included for easy reference.
#
# Explicitness and clarity are generally preferable, especially since bash can
# be difficult to read. This leads to noisier, longer code, but should be
# easier to maintain. As a result, some general design preferences:
#
# - Use leading underscores on internal variable and function names in order
#   to avoid name collisions. For unintentionally global variables defined
#   without `local`, such as those defined outside of a function or
#   automatically through a `for` loop, prefix with double underscores.
# - Always use braces when referencing variables, preferring `${NAME}` instead
#   of `$NAME`. Braces are only required for variable references in some cases,
#   but the cognitive overhead involved in keeping track of which cases require
#   braces can be reduced by simply always using them.
# - Prefer `printf` over `echo`. For more information, see:
#   http://unix.stackexchange.com/a/65819
# - Prefer `$_explicit_variable_name` over names like `$var`.
# - Use the `#!/usr/bin/env bash` shebang in order to run the preferred
#   Bash version rather than hard-coding a `bash` executable path.
# - Prefer splitting statements across multiple lines rather than writing
#   one-liners.
# - Group related code into sections with large, easily scannable headers.
# - Describe behavior in comments as much as possible, assuming the reader is
#   a programmer familiar with the shell, but not necessarily experienced
#   writing shell scripts.

###############################################################################
# Strict Mode
###############################################################################

# Treat unset variables and parameters other than the special parameters ‘@’ or
# ‘*’ as an error when performing parameter expansion. An 'unbound variable'
# error message will be written to the standard error, and a non-interactive
# shell will exit.
#
# This requires using parameter expansion to test for unset variables.
#
# http://www.gnu.org/software/bash/manual/bashref.html#Shell-Parameter-Expansion
#
# The two approaches that are probably the most appropriate are:
#
# ${parameter:-word}
#   If parameter is unset or null, the expansion of word is substituted.
#   Otherwise, the value of parameter is substituted. In other words, "word"
#   acts as a default value when the value of "$parameter" is blank. If "word"
#   is not present, then the default is blank (essentially an empty string).
#
# ${parameter:?word}
#   If parameter is null or unset, the expansion of word (or a message to that
#   effect if word is not present) is written to the standard error and the
#   shell, if it is not interactive, exits. Otherwise, the value of parameter
#   is substituted.
#
# Examples
# ========
#
# Arrays:
#
#   ${some_array[@]:-}              # blank default value
#   ${some_array[*]:-}              # blank default value
#   ${some_array[0]:-}              # blank default value
#   ${some_array[0]:-default_value} # default value: the string 'default_value'
#
# Positional variables:
#
#   ${1:-alternative} # default value: the string 'alternative'
#   ${2:-}            # blank default value
#
# With an error message:
#
#   ${1:?'error message'}  # exit with 'error message' if variable is unbound
#
# Short form: set -u
set -o nounset

# Exit immediately if a pipeline returns non-zero.
#
# NOTE: This can cause unexpected behavior. When using `read -rd ''` with a
# heredoc, the exit status is non-zero, even though there isn't an error, and
# this setting then causes the script to exit. `read -rd ''` is synonymous with
# `read -d $'\0'`, which means `read` until it finds a `NUL` byte, but it
# reaches the end of the heredoc without finding one and exits with status `1`.
#
# Two ways to `read` with heredocs and `set -e`:
#
# 1. set +e / set -e again:
#
#     set +e
#     read -rd '' variable <<HEREDOC
#     HEREDOC
#     set -e
#
# 2. Use `<<HEREDOC || true:`
#
#     read -rd '' variable <<HEREDOC || true
#     HEREDOC
#
# More information:
#
# https://www.mail-archive.com/bug-bash@gnu.org/msg12170.html
#
# Short form: set -e
set -o errexit

# Allow the above trap be inherited by all functions in the script.
#
# Short form: set -E
set -o errtrace

# Return value of a pipeline is the value of the last (rightmost) command to
# exit with a non-zero status, or zero if all commands in the pipeline exit
# successfully.
set -o pipefail

# Set $IFS to only newline and tab.
#
# http://www.dwheeler.com/essays/filenames-in-shell.html
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
HEREDOC
}

###############################################################################
# Options
#
# NOTE: The `getops` builtin command only parses short options and BSD `getopt`
# does not support long arguments (GNU `getopt` does), so the most portable
# and clear way to parse options is often to just use a `while` loop.
#
# For a pure bash `getopt` function, try pure-getopt:
#   https://github.com/agriffis/pure-getopt
#
# More info:
#   http://wiki.bash-hackers.org/scripting/posparams
#   http://www.gnu.org/software/libc/manual/html_node/Argument-Syntax.html
#   http://stackoverflow.com/a/14203146
#   http://stackoverflow.com/a/7948533
#   https://stackoverflow.com/a/12026302
#   https://stackoverflow.com/a/402410
###############################################################################

# Parse Options ###############################################################

# Initialize program option variables.
_PRINT_HELP=0
_USE_DEBUG=0

# Initialize additional expected option variables.
_HEADLESS=0
_DEV=0
_PROD=0
_SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
_COMPOSE_FILE_NAME=
_OT3_FIRMWARE=
_MODULES=

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
      _OT3_FIRMWARE="https://github.com/Opentrons/ot3-firmware/archive/$(__get_option_value "${__arg}" "${__val:-}").zip"
      shift
      ;;
    --modules-sha)
      _MODULES="https://github.com/Opentrons/opentrons-modules/archive/$(__get_option_value "${__arg}" "${__val:-}").zip"
      shift
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
  _debug printf "${_OT3_FIRMWARE_DEBUG_MESSAGE}"
  _debug printf "${_MODULES_DEBUG_MESSAGE}"
}

_construct_build_command() {
  _BUILD_COMMAND="COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose --verbose -f ${_COMPOSE_FILE_PATH} build "

  if [[ -n "${_OT3_FIRMWARE}" ]];  then
    _BUILD_COMMAND="${_BUILD_COMMAND} --build-arg FIRMWARE_SOURCE_DOWNLOAD_LOCATION=\"${_OT3_FIRMWARE}\""
  fi

  if [[ -n "${_MODULES}" ]]; then
    _BUILD_COMMAND="${_BUILD_COMMAND} --build-arg MODULE_SOURCE_DOWNLOAD_LOCATION=\"${_MODULES}\""
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
  _teardown_can_network
  _setup_can_network
  _remove_existing_docker_containers
  _bring_up_docker_containers
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
  if (( _USE_DEBUG )); then
    _use_debug
  fi
  if (( _PRINT_HELP )); then
    _print_help
  elif (( _PROD && _DEV )); then
    _exit_1 printf "Cannot specify --prod and --dev at the same time\\n"
  elif [[ ${_DEV} == 1 && ( -n "${_OT3_FIRMWARE}" || -n "${_MODULES}" ) ]]; then
    _exit_1 printf "Cannot specify --dev with either --ot3-firmware-sha or --modules-sha\\n"
  else
    _build_system "$@"
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