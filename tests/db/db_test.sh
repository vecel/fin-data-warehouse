#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 {load|stress}"
    exit 1
fi

MODE=$1

case "$MODE" in
    load)
        echo "Initializing LOAD test"
        CLIENTS=20
        THREADS=4
        TEST_DURATION=60
        ;;
    stress)
        echo "Initializing STRESS test"
        CLIENTS=60
        THREADS=4
        TEST_DURATION=60
        ;;
    *)
        echo "Error: Invalid mode '$MODE'."
        echo "Usage: $0 {load|stress}"
        exit 1
        ;;
esac

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
COMPOSE_DIR="${SCRIPT_DIR}/../../deploy/"

source "${SCRIPT_DIR}/../../.env.test"

DB_SERVICE="db"
DB_USER="benchmark"           

CONTAINER_ID=$(docker compose -f "${COMPOSE_DIR}"/compose.yaml -f "${COMPOSE_DIR}"/compose.test.yaml ps -q "${DB_SERVICE}" | head -n 1)
SQL_FILE="quote_benchmark.sql"
SQL_FILE_PATH="${SCRIPT_DIR}/${SQL_FILE}"

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: The Docker Compose service '$DB_SERVICE' is not running."
    echo "Please start your containers using 'docker compose up' and try again."
    exit 1
fi

echo "Preparing SQL file for pgbench"
docker cp "${SQL_FILE_PATH}" "${CONTAINER_ID}:/tmp/${SQL_FILE}"

echo "Starting database load test with pgbench"
docker exec "${CONTAINER_ID}" \
    pgbench -n -c "${CLIENTS}" -j "${THREADS}" -T "${TEST_DURATION}" -U "${DB_USER}" -f  "/tmp/${SQL_FILE}" "${POSTGRES_DB}"

echo "Benchmark complete!"