#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN:=localhost} \
TAG=${TAG:=prod-test} \
IMAGE_DOMAIN=${IMAGE_DOMAIN:=localhost} \
source ./scripts/build.sh

docker-compose \
-f compose/docker-compose.shared.admin.yml \
-f compose/docker-compose.shared.networks.yml \
-f compose/docker-compose.shared.base-images.yml \
-f compose/docker-compose.shared.depends.yml \
-f compose/docker-compose.shared.env.yml \
-f compose/docker-compose.shared.volumes.yml \
-f compose/docker-compose.deploy.command.yml \
-f compose/docker-compose.deploy.images.yml \
-f compose/docker-compose.deploy.build.yml \
-f compose/docker-compose.deploy.labels.yml \
-f compose/docker-compose.deploy.networks.yml \
-f compose/docker-compose.dev.ports.yml \
-f compose/docker-compose.deploy.volumes-placement.yml \
-f compose/docker-compose.deploy.stack.yml \
-f compose/docker-compose.test.env.yml \
config > docker-stack-${TAG}.yml

docker network rm proxy || true
docker swarm init || true
docker network create -d overlay --attachable proxy || true
TAG=${TAG:=prod} \
docker stack deploy -c docker-stack-${TAG}.yml --with-registry-auth em-stack
