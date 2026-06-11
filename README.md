# Financial Data Warehouse IT System

An end-to-end data architecture designed to acquire, process, store, and serve data securely and efficiently. This project encompasses automated data ingestion, robust SQL-based transformations using dbt, a relational data warehouse, and REST API.

## System architecture

This system follows a modular, multi-layer architecture:

* **Data Acquisition:** Python scripts extracting raw data from external sources.
* **Data Staging:** Local CSV files functioning as a lightweight staging layer.
* **Database:** PostgreSQL serving as the central Data Warehouse.
* **Data Transformation:** dbt (Data Build Tool) for building analytics-ready models from raw data.
* **Data Serving (API):** A containerized Python REST API (FastAPI) via Docker, including interactive Swagger UI documentation available at /docs.
[* **Data Visualization:** Tableau dashboards connecting directly to the transformed PostgreSQL schemas.]

## Prerequisites
This project assumes you have installed `docker` with `docker-compose` and have privileges to run `docker` commands.


## Installation

Clone the repository and enter created directory.
```
git clone https://github.com/vecel/fin-data-warehouse.git
cd fin-data-warehouse
```

Create enviroment files with your credentials (`.env.dev`, `.env.test`, `.env.prod` depending on the environment you want to run).
```
touch .env.dev
```

Paste environment variables to your `.env` file. Use your own values.
```
FRED_API_KEY=<api_key>
ALPHA_VANTAGE_API_KEY=<api_key>

POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database>
TABLEAU_USER_PASSWORD=<tableau_password>
```

Start the system using the environment manager script.
```
./start.sh dev up
```


## Tests
Start `test` environment.
```
./start.sh test up
```

To run load test against database open terminal window and run test script.
```
./tests/db/db_test.sh load
```

Or if you want to run stress.
```
./tests/db/db_test.sh stress
```

## Repository structure

* `/data-acquisition` - Python scripts and requirements for fetching data.
* `/data-loader` - Python scripts for automatic data loading to the database.
* `/staging` & `/cache` - Directories for temporary Parquet files for staging and caching (files ignored by git).
* `/data-processing` - dbt models, tests, and configurations.
* `/data-serving` - Python REST API source code (Fast API).
* `/data-visualization` - Streamlit application for data presentation and dashboards.
* `/deploy` - Infrastructure files including `docker-compose.yaml` and database init scripts.

[comment]: # (Add installation guide and automation with all required packages like docker, python etc.)

---

#### Work done
1. Data acqusition:
   - Container definition - Mateusz
   - Scheduler & writer - Mateusz
   - Fetchers: calendars, countries, tickers, fundamentals - Mateusz
   - Fetchers: news, quotes, fred - Olek
2. Data processing:
    - Dbt project setup - Mateusz
    - Container definition - Mateusz
    - Date dimension, exchange dimension - Mateusz
    - Tickers info staging, calendar staging - Mateusz
    - Fact tables - Olek
    - Macro indicator dimension - Olek
3. Data serving:
    - Container definition - Olek
    - API endpoints - Olek
4. Data visualization:
    - Container definition - Olek
    - Streamlit app - Olek
4. Deployment:
    - Docker compose definition & startup script - Mateusz
    - Separation for dev, test, prod enviroments & manage script - Olek
5. Other:
    - Project and repository structure - Mateusz
    - README - Mateusz & Olek
    - Load & stress tests - Mateusz
