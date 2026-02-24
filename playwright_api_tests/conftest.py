import pytest
from pages.api_client import VehicleAPIClient
from pages.dashboard_page import DashboardPage

API_BASE_URL = "https://6pu7wjaw9d.execute-api.us-east-1.amazonaws.com/dev"

@pytest.fixture
def api_request(playwright):
    request = playwright.request.new_context()
    yield request 
    request.dispose()

@pytest.fixture
def api_url():
    return API_BASE_URL
    
@pytest.fixture
def api(api_request, api_url):
    return VehicleAPIClient(api_request, api_url)

@pytest.fixture
def valid_payload():
    return{
        "vehicle_id":"VH_VALID_001",
        "speed_kmh":80,
        "fuel_percent":45,
        "lat":5.6332,
        "lon":6.3423
    }

@pytest.fixture
def invalid_payload():
    return {
        "vehicle_id":1234,
        "speed_kmh":80,
        "fuel_percent":45,
        "lat":5.6332,
        "lon":6.3423
    }

@pytest.fixture
def speed_alert_payload():
    return{
        "vehicle_id":"VH_VALID_001",
        "speed_kmh":200,
        "fuel_percent":45,
        "lat":5.6332,
        "lon":6.3423
    }

@pytest.fixture
def fuel_alert_payload():
    return{
        "vehicle_id":"VH_VALID_001",
        "speed_kmh":80,
        "fuel_percent":4,
        "lat":5.6332,
        "lon":6.3423
    }

@pytest.fixture
def multiple_alert_payload():
    return{
        "vehicle_id":"VH_VALID_001",
        "speed_kmh":200,
        "fuel_percent":3,
        "lat":5.6332,
        "lon":6.3423
    }


@pytest.fixture
def dashboard(page):
    return DashboardPage(page)