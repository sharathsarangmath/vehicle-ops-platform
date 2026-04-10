# Vehicle Operations Platform (VOP)

A cloud-native vehicle telemetry platform built to demonstrate 
senior QA engineering skills across AWS, Docker, Kafka, and Kubernetes.

[![VOP CI Pipeline](https://github.com/sharathsarangmath/vehicle-ops-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/sharathsarangmath/vehicle-ops-platform/actions/workflows/ci.yml)

## Architecture
```
Postman/Tests → API Gateway → Lambda → SQS → DynamoDB
                                 ↓
                              Kafka Topic
                                 ↓
                           Consumer Service
```

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud API | AWS Lambda, API Gateway |
| Queue | AWS SQS, Kafka |
| Database | AWS DynamoDB |
| Local API | FastAPI |
| Containers | Docker, Docker Compose |
| Orchestration | Kubernetes (minikube) |
| CI/CD | GitHub Actions |
| Testing | Pytest, Playwright, POM |

## Services

| Endpoint | Method | Description |
|---|---|---|
| /health | GET | Health check |
| /telemetry | POST | Submit vehicle data |
| /telemetry | GET | Get all records |
| /alerts | GET | Get alert records |
| /telemetry/no-alerts | GET | Get clean records |
| /vehicle/{id} | GET | Get vehicle records |
| /vehicle/{id}/alerts | GET | Get vehicle alerts |

## Alert Thresholds
```
Speed > 120 km/h  → SPEED_ALERT
Fuel < 15%        → LOW_FUEL_ALERT
```

## Running Locally

### With Docker Compose
```bash
docker-compose up --build
```

### Test the API
```bash
curl http://localhost:8000/health
```

### Run Tests
```bash
cd playwright_api_tests
pytest -v
```

## Kubernetes
```bash
# Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check pods
kubectl get pods

# Access app
minikube service vop-api-service --url
```

## CI/CD

Every push to main branch:
1. Runs Playwright API tests
2. Builds Docker image
3. Reports pass or fail

## Debugging Experience

Real AWS bugs debugged during development:
- Region mismatch (eu-west-1 vs us-east-1)
- DynamoDB float to Decimal conversion
- Lambda timeout (3s → 30s)
- CORS configuration
- Kafka NoBrokersAvailable
