#!/bin/bash

set -e

source ../../.env

DB_SERVICE="db"
DB_USER="benchmark"           

CLIENTS=20
THREADS=4
TEST_DURATION=60

CONTAINER_ID=$(docker compose ps -q "${DB_SERVICE}" | head -n 1)
SQL_FILE="example_benchmark.sql"

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: The Docker Compose service '$DB_SERVICE' is not running."
    echo "Please start your containers using 'docker compose up' and try again."
    exit 1
fi

echo "Preparing SQL file for pgbench"
docker cp "${SQL_FILE}" "${CONTAINER_ID}:/tmp/${SQL_FILE}"

echo "Starting database load test with pgbench"
docker exec "${CONTAINER_ID}" \
    pgbench -n -c "${CLIENTS}" -j "${THREADS}" -T "${TEST_DURATION}" -U "${DB_USER}" -f  "/tmp/${SQL_FILE}" "${POSTGRES_DB}"

echo "Benchmark complete!"