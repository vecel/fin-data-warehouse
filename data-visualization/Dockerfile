FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir streamlit==1.32.0 requests==2.31.0 pandas==2.2.1 plotly==5.19.0
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]