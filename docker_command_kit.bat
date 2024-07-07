@echo off

REM Pull Docker images
docker pull postgres:alpine
docker pull dbgate/dbgate:alpine

REM Create Docker volumes
docker volume create dbgate_data

REM Import Volumes of DBGate
docker run --rm `
  -v %cd%\dbgate_data.tar.gz:/backup/dbgate_data.tar.gz `
  -v dbgate_data:/data `
  busybox `
  sh -c "tar xvf /backup/dbgate_data.tar.gz -C /data"

REM Build the Docker image
docker build -t my-python-app .

REM Run Docker containers
docker-compose up --build


