#! /usr/bin/env bash

# Exit in case of error
set -e

TAG=${TAG:=latest}

docker-compose -f docker-stack-${TAG}.yml push
