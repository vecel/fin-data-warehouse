#!/bin/sh
set -e

echo "=== Waiting for the Loader to perform the initial data load ==="

python3 -c "
import psycopg2
import time
import os
import sys

conn_str = f\"host={os.getenv('POSTGRES_HOST')} dbname={os.getenv('POSTGRES_DB')} user={os.getenv('POSTGRES_USER')} password={os.getenv('POSTGRES_PASSWORD')} port=5432\"

while True:
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(\"SELECT COUNT(*) FROM raw._timestamps;\")
        count = cursor.fetchone()[0]
        if count >= 4:
            print(f'Success: Loader populated {count} source tables. Launching dbt.')
            conn.close()
            break
        conn.close()
    except Exception as e:
        pass
    print('Source data in the raw schema is not ready yet. Waiting 5 seconds...')
    time.sleep(5)
"

echo "Running dbt snapshots"
dbt snapshot

echo "Running dbt models"
dbt run

echo "Transformations completed successfully "