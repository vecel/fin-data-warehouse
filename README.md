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

## Prerequisites
This project assumes you have installed `docker` with `docker-compose` and have privileges to run `docker` commands.


## Installation

Clone the repository and enter created directory.
```
git clone https://github.com/vecel/fin-data-warehouse.git
cd fin-data-warehouse
```

Create `.env` file with postgres database credentials.
```
cd deploy/
touch .env
```

Paste environment variables to `.env` file. Use your own values.
```
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database>
```

Run `docker compose`.
```
docker compose up
```

[comment]: # (Add guide to create .env inside data-acquisition)
[comment]: # (After running docker compose up root owns data-staging directory. You won't have access to it unless you change directory ownership)

## Repository structure

* `/data-acquisition` - Python scripts and requirements for fetching data.
* `/data-staging` - Directory for temporary CSV staging (files ignored by git).
* `/data-processing` - dbt models, tests, and configurations.
* `/api` - Python REST API source code.
* `/deploy` - Infrastructure files including `docker-compose.yml` and database init scripts.

[comment]: # (Add installation guide and automation with all required packages like docker, python etc.)
