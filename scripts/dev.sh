#! /usr/bin/env bash

# Exit in case of error
set -e

DOCKER_BUILDKIT=1 docker build app/ -f app/backend.dockerfile -t localhost/em-backend:dev --build-arg APP_ENV=dev

DOCKER_BUILDKIT=1 docker build app/ -f app/worker.dockerfile -t localhost/em-worker:dev --build-arg APP_ENV=dev

docker network rm proxy || true
docker network create proxy || true
docker-compose -p em up
