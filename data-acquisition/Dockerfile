FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN groupadd -g 1000 acqu && \
    useradd -u 1000 -g 1000 acqu 
USER acqu
CMD ["python3", "/app/main.py"]