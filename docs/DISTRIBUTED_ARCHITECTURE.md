# Distributed Architecture Configuration Guide

This project supports a **distributed architecture** where different components can run on separate servers.

## Architecture Overview

```
┌─────────────────────┐
│   MLflow Server     │
│  (Tracking & Registry)│
│   Port: 5000        │
└──────────┬──────────┘
           │
           │ HTTP/HTTPS
           │
┌──────────┴──────────┐
│  Airflow Server     │
│ (Orchestration)     │
│   Port: 8080        │
└──────────┬──────────┘
           │
           │ HTTP/HTTPS
           │
┌──────────┴──────────┐
│   API Server        │
│ (Predictions)       │
│   Port: 8000        │
└─────────────────────┘
```

## Server 1: MLflow Tracking Server

### Setup
```bash
# Install MLflow
pip install mlflow

# Start MLflow server accessible from network
mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlartifacts
```

**Important**: Use `--host 0.0.0.0` to make it accessible from other servers.

### Configuration
- **Public URL**: `http://<mlflow-server-ip>:5000` or `https://mlflow.example.com`
- Ensure firewall allows port 5000
- For production, use proper authentication and HTTPS

---

## Server 2: Airflow Orchestration Server

### Setup
1. **Update `.env` file** in `airflow/` directory:
```env
# External Services
MLFLOW_TRACKING_URI=http://<mlflow-server-ip>:5000
AIRFLOW_PUBLIC_URL=http://<airflow-server-ip>:8080
```

2. **Start Airflow with Docker Compose**:
```bash
cd airflow/
docker compose down
docker compose build
docker compose up -d
```

### Configuration
- **Public URL**: `http://<airflow-server-ip>:8080` or `https://airflow.example.com`
- Ensure firewall allows port 8080
- Airflow containers will connect to MLflow using public URL
- API authentication is enabled (username: `airflow`, password: `airflow`)

### Verify Connectivity
```bash
# From Airflow container
docker exec airflow-airflow-scheduler-1 curl http://<mlflow-server-ip>:5000/health
```

---

## Server 3: API Prediction Server

### Setup
1. **Create `.env` file** in `deployment/` directory:
```env
# MLflow Server
MLFLOW_TRACKING_URI=http://<mlflow-server-ip>:5000

# Airflow Server
AIRFLOW_BASE_URL=http://<airflow-server-ip>:8080
AIRFLOW_USERNAME=airflow
AIRFLOW_PASSWORD=airflow

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

2. **Start API Server**:
```bash
cd deployment/
pip install -r requirements.txt
uvicorn api.v1.main:app --host 0.0.0.0 --port 8000
```

### Configuration
- **Public URL**: `http://<api-server-ip>:8000` or `https://api.example.com`
- Ensure firewall allows port 8000
- Connects to both MLflow and Airflow using public URLs

---

## Network Requirements

### Firewall Rules
- **MLflow Server**: Open port 5000 for incoming connections
- **Airflow Server**: Open port 8080 for incoming connections
- **API Server**: Open port 8000 for incoming connections

### DNS Configuration (Optional but Recommended)
Instead of IP addresses, use domain names:
- `mlflow.example.com` → MLflow server IP
- `airflow.example.com` → Airflow server IP
- `api.example.com` → API server IP

Update `.env` files with domain names instead of IPs.

---

## Security Considerations

### 1. HTTPS/TLS
Use a reverse proxy (Nginx, Traefik, or Caddy) for HTTPS:
```nginx
# Example Nginx config for MLflow
server {
    listen 443 ssl;
    server_name mlflow.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. Authentication
- **MLflow**: Add basic auth or integrate with identity provider
- **Airflow**: Already configured with basic auth (update credentials in production)
- **API Server**: Add JWT tokens or API keys for production

### 3. Network Isolation
- Use VPC/Private Network when possible
- Use VPN for cross-datacenter communication
- Implement rate limiting and DDoS protection

---

## Testing Connectivity

### From API Server to MLflow
```bash
curl http://<mlflow-server-ip>:5000/health
```

### From API Server to Airflow
```bash
curl -u airflow:airflow http://<airflow-server-ip>:8080/api/v1/health
```

### From Airflow to MLflow
```bash
docker exec airflow-airflow-scheduler-1 curl http://<mlflow-server-ip>:5000/health
```

---

## Troubleshooting

### Issue: Connection Refused
- **Check if service is running** on the target server
- **Verify firewall rules** allow the port
- **Test with telnet**: `telnet <server-ip> <port>`

### Issue: Connection Timeout
- **Check network connectivity** between servers
- **Verify security groups** (AWS/GCP/Azure)
- **Check if proxy is blocking** the connection

### Issue: DNS Resolution Failed
- **Use IP addresses** instead of domain names temporarily
- **Verify DNS records** are configured correctly
- **Check /etc/hosts** file for local resolution

---

## Environment Variables Reference

### Airflow `.env`
```env
MLFLOW_TRACKING_URI=<mlflow-url>
AIRFLOW_PUBLIC_URL=<airflow-url>
API_SERVER_URL=<api-url>
```

### Deployment `.env`
```env
MLFLOW_TRACKING_URI=<mlflow-url>
AIRFLOW_BASE_URL=<airflow-url>
AIRFLOW_USERNAME=airflow
AIRFLOW_PASSWORD=airflow
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Monitoring

### Health Check Endpoints
- MLflow: `http://<mlflow-url>/health`
- Airflow: `http://<airflow-url>/api/v1/health`
- API: `http://<api-url>/`

### Logs
- **MLflow**: Check terminal output or use logging service
- **Airflow**: `airflow/logs/` directory or web UI
- **API**: Check application logs

---

## Single Server Setup (Development)

For development/testing on a single machine:

```env
# All services on localhost
MLFLOW_TRACKING_URI=http://localhost:5000
AIRFLOW_BASE_URL=http://localhost:8080
API_SERVER_URL=http://localhost:8000
```

Start MLflow with `--host 0.0.0.0` even for local development to ensure Docker containers can access it.
