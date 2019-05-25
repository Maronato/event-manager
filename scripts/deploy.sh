#! /usr/bin/env sh

# Exit in case of error
set -e

STACK_NAME=${STACK_NAME:=em-stack}
TAG=${TAG:=latest}

docker stack deploy -c docker-stack-${TAG}.yml --with-registry-auth ${STACK_NAME}
