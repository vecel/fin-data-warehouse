#!/bin/bash
set -e

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

echo "Triggering SCD 2 change for 11 Bits"
echo "Current values in instrument_dim"
${PSQL} -c "\
    SELECT instrument_code, instrument_price_category, is_active_flag FROM dwh.instrument_dim
    WHERE instrument_code = '11B.WA'"

echo "Current raw price value"
${PSQL} -c "\
    SELECT symbol, \"currentPrice\" FROM raw.fundamentals
    WHERE symbol = '11B.WA'"

${PSQL} -c "\
    UPDATE raw.fundamentals
    SET \"currentPrice\" = 5.0 \
    WHERE symbol = '11B.WA'"

echo "Updated raw price value for 11B.WA"
${PSQL} -c "\
    SELECT symbol, \"currentPrice\" FROM raw.fundamentals
    WHERE symbol = '11B.WA'"

echo "Running dbt snapshot and model"

${COMPOSE} \
    run --rm --entrypoint dbt \
    dbt \
    snapshot

${COMPOSE} \
    run --rm --entrypoint dbt \
    dbt \
    run --select instrument_dim

echo "Updated 11B record in instrument_dim"

${PSQL} -c "\
    SELECT instrument_code, instrument_price_category, valid_from_date_id, valid_to_date_id, is_active_flag FROM dwh.instrument_dim
    WHERE instrument_code = '11B.WA'"
