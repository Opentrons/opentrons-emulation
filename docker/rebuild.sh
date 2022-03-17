#!/usr/bin/env bash

rm /.build_finished
/entrypoint.sh build
touch /.build_finished
/entrypoint.sh run
