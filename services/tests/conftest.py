from dotenv import load_dotenv
import os
import pytest
from pages.api_client import VehicleAPIClient

# load env
load_dotenv()

#API URL
@pytest.fixture(scope="session")
def api_base_url():
    url=os.getenv("API_BASE_URL")
    print(f"Using API_BASE_URL: {url}")
    return url

# API Client
@pytest.fixture(scope="session")
def api(api_base_url):
    return VehicleAPIClient(api_base_url)

# ── AWS Clients ──────────────────────────────────────────
@pytest.fixture(scope="session")
def sqs_client():
    return boto3.client('sqs', region_name='us-east-1')

@pytest.fixture(scope="session")
def sqs_queue_url():
    return os.getenv("SQS_QUEUE_URL")

@pytest.fixture(scope="session")
def sqs_dlq_url():
    return os.getenv("SQS_DLQ_URL")

# ── Payloads ─────────────────────────────────────────────
@pytest.fixture
def valid_payload():
    """Normal data - no alerts expected"""
    return {
        "vehicle_id": "VH-TEST-001",
        "speed_kmh": 80,
        "fuel_percent": 50,
        "lat": 53.3498,
        "lon": -6.2603
    }

@pytest.fixture
def speed_alert_payload():
    """Speed over 120 - should trigger SPEED_ALERT"""
    return {
        "vehicle_id": "VH-SPEED-TEST",
        "speed_kmh": 150,
        "fuel_percent": 50,
        "lat": 53.3498,
        "lon": -6.2603
    }

@pytest.fixture
def fuel_alert_payload():
    """Fuel under 15 - should trigger LOW_FUEL_ALERT"""
    return {
        "vehicle_id": "VH-FUEL-TEST",
        "speed_kmh": 80,
        "fuel_percent": 5,
        "lat": 53.3498,
        "lon": -6.2603
    }

@pytest.fixture
def double_alert_payload():
    """Speed over 120 AND fuel under 15 - should trigger 2 alerts"""
    return {
        "vehicle_id": "VH-DOUBLE-ALERT",
        "speed_kmh": 150,
        "fuel_percent": 5,
        "lat": 53.3498,
        "lon": -6.2603
    }