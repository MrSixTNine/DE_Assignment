#!/bin/bash

# Pull Docker images
docker pull postgres:alpine
docker pull dbgate/dbgate:alpine

# Create Docker volumes
docker volume create dbgate_data

# Import Volumes of DBGate
docker run --rm \
  -v $(pwd)/dbgate_data.tar.gz:/backup/dbgate_data.tar.gz \
  -v dbgate_data:/data \
  busybox \
  sh -c "tar xvf /backup/dbgate_data.tar.gz -C /data"

# Build the Docker image
docker build -t my-python-app .

# Run Docker containers
docker-compose up --build
