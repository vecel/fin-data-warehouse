#!/bin/sh
set -e

dbt snapshot

echo "Running dbt models"
dbt run

echo "Done"