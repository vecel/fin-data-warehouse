#!/bin/sh
set -e

echo "Running dbt seed"
dbt seed

echo "Running dbt models"
dbt run

echo "Done"