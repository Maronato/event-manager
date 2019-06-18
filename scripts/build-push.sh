#! /usr/bin/env bash

# Exit in case of error
set -e

TAG=${TAG:=latest} \
source ./scripts/build.sh

TAG=${TAG:=latest} \
source ./scripts/push.sh
