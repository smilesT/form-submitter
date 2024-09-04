FROM python:3.12-slim

# Curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir flask gunicorn

WORKDIR /app
