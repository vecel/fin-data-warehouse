# Financial Data Warehouse IT System

An end-to-end data architecture designed to acquire, process, store, and serve data securely and efficiently. This project encompasses automated data ingestion, robust SQL-based transformations using dbt, a relational data warehouse, and REST API.

## System architecture

This system follows a modular, multi-layer architecture:

* **Data Acquisition:** Python scripts extracting raw data from external sources.
* **Data Staging:** Local CSV files functioning as a lightweight staging layer.
* **Database:** PostgreSQL serving as the central Data Warehouse.
* **Data Transformation:** dbt (Data Build Tool) for building analytics-ready models from raw data.
* **Data Serving (API):** A containerized Python REST API (FastAPI/Flask) via Docker.
[* **Data Visualization:** Tableau dashboards connecting directly to the transformed PostgreSQL schemas.]

## Repository structure

* `/data-acquisition` - Python scripts and requirements for fetching data.
* `/data-staging` - Directory for temporary CSV staging (files ignored by git).
* `/data-processing` - dbt models, tests, and configurations.
* `/api` - Python REST API source code and `Dockerfile`.
* `/deploy` - Infrastructure files including `docker-compose.yml` and database init scripts.
