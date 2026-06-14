#!/bin/bash
set -e

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: ./dwh_test.sh <path_to_sql_script> <model_name> [--preview]"
    exit 1
fi

SQL_INIT_FILE=$1
MODEL_NAME=$2
PREVIEW=$3
echo $PREVIEW
SQL_INIT_FILE_BASENAME=$(basename "${SQL_INIT_FILE}")

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR="${SCRIPT_DIR}/../../"
COMPOSE_DIR="${ROOT_DIR}/deploy/"

source "${ROOT_DIR}.env.test"

DB_SERVICE="db"
COMPOSE="docker compose -f ${COMPOSE_DIR}/compose.yaml -f ${COMPOSE_DIR}/compose.test.yaml"
PSQL="${COMPOSE} exec -e PGPASSWORD=${POSTGRES_PASSWORD} ${DB_SERVICE} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}"


echo "Checking for database container..."

CONTAINER_ID=$(${COMPOSE} ps -q "${DB_SERVICE}" | head -n 1)

if [ -z "$CONTAINER_ID" ]; then
    echo "Error: The Docker Compose service '$DB_SERVICE' is not running."
    echo "Please start your containers using 'docker compose up' and try again."
    exit 1
fi

echo "Database ready"
echo "Preparing end-to-end test..."

if [ ! -f "$SQL_INIT_FILE" ]; then
    echo "Error: SQL file '$SQL_INIT_FILE' not found!"
    exit 1
fi

${COMPOSE} cp "${SQL_INIT_FILE}" "${DB_SERVICE}:/tmp/${SQL_INIT_FILE_BASENAME}"
${PSQL} -f "/tmp/${SQL_INIT_FILE_BASENAME}"

echo "Ready for testing"

if [ "$PREVIEW" == "--preview" ]; then
    ${PSQL} -c "\
        select * \
        from dwh.${MODEL_NAME} \
        limit 10" 
fi

echo "Running dbt model"

${COMPOSE} \
    run --rm --entrypoint dbt \
    dbt \
    run --select $MODEL_NAME

if [ "$PREVIEW" == "--preview" ]; then
    ${PSQL} -c "\
        select * \
        from dwh.${MODEL_NAME} \
        limit 10"
fi
