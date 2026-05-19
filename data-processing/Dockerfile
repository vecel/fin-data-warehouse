FROM ghcr.io/dbt-labs/dbt-postgres:1.9.0
WORKDIR /app
ENV DBT_PROFILES_DIR=.
COPY . .
CMD ["dbt", "run"]