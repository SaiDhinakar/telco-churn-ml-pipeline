# Deployment Guide

## Docker Deployment

### Initial Build and Run

For the first deployment, build the Docker image:
```bash
docker-compose up --build
```

### Running the Service

Start the ML API service in detached mode:
```bash
docker-compose up -d
```

### Stopping the Service

Stop the ML API service:
```bash
docker-compose down
```
