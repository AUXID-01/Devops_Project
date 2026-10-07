FROM python:3.11-slim

# Create a non-root user
RUN adduser --disabled-password --gecos '' bugboard

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership and switch user
RUN chown -R bugboard:bugboard /app
USER bugboard

# Run command will be specified in docker-compose
