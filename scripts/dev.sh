#! /usr/bin/env sh

# Exit in case of error
set -e

DOCKER_BUILDKIT=1 docker build app/ -f app/backend.dockerfile -t localhost/event-manager-backend:dev --build-arg APP_ENV=dev

DOCKER_BUILDKIT=1 docker build app/ -f app/worker.dockerfile -t localhost/event-manager-worker:dev --build-arg APP_ENV=dev

docker-compose up
