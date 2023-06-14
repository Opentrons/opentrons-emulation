#!/bin/bash

# Pass in a list of directories to build
# Each directory should have a Makefile with a `wheel` target
# The wheel will be copied to /dist

DIST_DIR=$1
shift 1

cd /opentrons || exit 1

for arg; do
    echo "Building /opentrons/$arg"
    make -C $arg python=monorepo_python wheel
    cp $arg/dist/*.whl $DIST_DIR
done
