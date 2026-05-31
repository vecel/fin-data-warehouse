FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "/app/main.py"]