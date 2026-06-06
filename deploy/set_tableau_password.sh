#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	ALTER USER tableau WITH PASSWORD '$TABLEAU_USER_PASSWORD'
EOSQL