#!/bin/sh
#
# Runs the main script
#
set -e

scripts=$(dirname $0)

python $scripts/../py8bit.py "$@"