#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN:=localhost} \
TRAEFIK_TAG=${TRAEFIK_TAG=localhost} \
IMAGE_DOMAIN=${IMAGE_DOMAIN:=maronato} \
TAG=${TAG:=prod} \
docker-compose \
-f docker-compose.shared.admin.yml \
-f docker-compose.shared.networks.yml \
-f docker-compose.shared.base-images.yml \
-f docker-compose.shared.depends.yml \
-f docker-compose.shared.env.yml \
-f docker-compose.shared.volumes.yml \
-f docker-compose.deploy.command.yml \
-f docker-compose.deploy.images.yml \
-f docker-compose.deploy.build.yml \
-f docker-compose.deploy.labels.yml \
-f docker-compose.deploy.networks.yml \
-f docker-compose.deploy.ports.yml \
-f docker-compose.deploy.volumes-placement.yml \
-f docker-compose.deploy.stack.yml \
-f docker-compose.deploy.env.yml \
config > docker-stack-${TAG}.yml

DOMAIN=${DOMAIN:=localhost} \
TRAEFIK_TAG=${TRAEFIK_TAG=localhost} \
IMAGE_DOMAIN=${IMAGE_DOMAIN:=maronato} \
TAG=latest \
docker-compose \
-f docker-compose.shared.admin.yml \
-f docker-compose.shared.networks.yml \
-f docker-compose.shared.base-images.yml \
-f docker-compose.shared.depends.yml \
-f docker-compose.shared.env.yml \
-f docker-compose.shared.volumes.yml \
-f docker-compose.deploy.command.yml \
-f docker-compose.deploy.images.yml \
-f docker-compose.deploy.build.yml \
-f docker-compose.deploy.labels.yml \
-f docker-compose.deploy.networks.yml \
-f docker-compose.deploy.ports.yml \
-f docker-compose.deploy.volumes-placement.yml \
-f docker-compose.deploy.stack.yml \
-f docker-compose.deploy.env.yml \
config > docker-stack-latest.yml
