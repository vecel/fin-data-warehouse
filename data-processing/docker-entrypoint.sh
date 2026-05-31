#!/bin/sh
set -e

echo "Running dbt models"
dbt run

echo "Done"