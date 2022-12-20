#!/bin/bash

if [ ! "$(docker network ls | grep sales-helper-network)" ]; then
  echo "Creating sales-helper-network network ..."
  docker network create sales-helper-network
else
  echo "sales-helper-network network exists."
fi

CURR_DIR=$(pwd)

source .env
# build context variables
docker-compose -f client_api/docker/docker-compose.yml --env-file=.env build --no-cache
docker-compose -f client_api/docker/docker-compose.yml --env-file=.env up -d

docker-compose -f data_service/docker/docker-compose.yml --env-file=.env build --no-cache
docker-compose -f data_service/docker/docker-compose.yml --env-file=.env up -d

docker-compose -f ml_service/docker/docker-compose.yml --env-file=.env build --no-cache
docker-compose -f ml_service/docker/docker-compose.yml --env-file=.env up -d
