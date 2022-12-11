#!/bin/bash

source .env
# build context variables
docker-compose -f client_api/docker/docker-compose.yml --env-file=.env down

docker-compose -f data_service/docker/docker-compose.yml --env-file=.env down

docker-compose -f ml_service/docker/docker-compose.yml --env-file=.env down
