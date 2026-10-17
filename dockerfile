FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["xvfb-run", "-a", "python", "customer_login.py"]
