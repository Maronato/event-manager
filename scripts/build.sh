#! /usr/bin/env bash

# Exit in case of error
set -e

DOMAIN=${DOMAIN:=localhost} \
TRAEFIK_TAG=${TRAEFIK_TAG=localhost} \
IMAGE_DOMAIN=${IMAGE_DOMAIN:=maronato} \
TAG=${TAG:=prod} \
source ./scripts/generate-stack.sh

TAG=${TAG} \
DOCKER_BUILDKIT=1 \
IMAGE_DOMAIN=${IMAGE_DOMAIN} \
docker build app/ -f app/backend.dockerfile -t ${IMAGE_DOMAIN}/em-backend:${TAG} -t ${IMAGE_DOMAIN}/em-backend:latest --build-arg APP_ENV=prod

TAG=${TAG} \
DOCKER_BUILDKIT=1 \
IMAGE_DOMAIN=${IMAGE_DOMAIN} \
docker build app/ -f app/worker.dockerfile -t ${IMAGE_DOMAIN}/em-worker:${TAG} -t ${IMAGE_DOMAIN}/em-worker:latest --build-arg APP_ENV=prod

