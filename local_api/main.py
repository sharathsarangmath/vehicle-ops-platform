from fastapi import FastAPI
from datetime import datetime
from kafka import KafkaProducer
import json
import os

app = FastAPI()

def get_producer():
    return KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

@app.get("/health")
def health():
    status = os.getenv("APP_STATUS", "healthy")
    return {
        "status": status.upper(),
        "service": "vop-local-api",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/telemetry")
def post_telemetry(payload: dict):
    try:
        producer = get_producer()
        producer.send('vehicle-telemetry', payload)
        producer.flush()
        return {
            "message": "Telemetry sent to Kafka",
            "vehicle_id": payload.get("vehicle_id"),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/vehicles")
def get_vehicles():
    return {
        "vehicles": [
            {"id": "VH-001", "speed": 80, "fuel": 50},
            {"id": "VH-002", "speed": 150, "fuel": 5},
        ]
    }