#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN:=localhost} \
IMAGE_DOMAIN=${IMAGE_DOMAIN:=maronato} \
TAG=${TAG:=prod} \
EMAIL=${EMAIL:=gustavomaronato@gmail.com} \
USERNAME=${USENAME:=admin} \
HASHED_PASSWORD=${HASHED_PASSWORD:='$apr1$kbyKlDk8$JiUTxXytJQl1OBoqtrY0t.'} \
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
-f compose/docker-compose.deploy.ports.yml \
-f compose/docker-compose.deploy.volumes-placement.yml \
-f compose/docker-compose.deploy.stack.yml \
-f compose/docker-compose.deploy.env.yml \
config > docker-stack-${TAG}.yml

DOMAIN=${DOMAIN:=localhost} \
IMAGE_DOMAIN=${IMAGE_DOMAIN:=maronato} \
TAG=latest \
EMAIL=${EMAIL:=gustavomaronato@gmail.com} \
USERNAME=${USENAME:=admin} \
HASHED_PASSWORD=${HASHED_PASSWORD:=$apr1$kbyKlDk8$JiUTxXytJQl1OBoqtrY0t.} \
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
-f compose/docker-compose.deploy.ports.yml \
-f compose/docker-compose.deploy.volumes-placement.yml \
-f compose/docker-compose.deploy.stack.yml \
-f compose/docker-compose.deploy.env.yml \
config > docker-stack-latest.yml
