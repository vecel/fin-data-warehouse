#!/bin/bash

mkdir cache
mkdir staging

chown -R 1000:1000 cache
chown -R 1000:1000 staging

docker compose -f deploy/compose.yaml up