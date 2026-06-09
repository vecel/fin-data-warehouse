FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir dbt-postgres==1.8.0
COPY packages.yml dbt_project.yml .
RUN dbt deps
COPY . .
RUN chmod +x docker-entrypoint.sh && \
    useradd dbtuser && \
    chown -R dbtuser:dbtuser /app
USER dbtuser
ENTRYPOINT ["/app/docker-entrypoint.sh"]