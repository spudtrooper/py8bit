#!/bin/sh
#
# Run simple tests
#
set -e

rm -rf testoutput

scripts/run.sh -d testoutput --images testdata/picasso.jpg
scripts/run.sh -d testoutput --images testdata/picasso.jpg --pixel_size 25
scripts/run.sh -d testoutput --images testdata/picasso.jpg --pixel_size 100