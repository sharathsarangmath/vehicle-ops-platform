# def test_GET_health_api(playwright):
#     request = playwright.request.new_context()
#     response = request.get("https://6pu7wjaw9d.execute-api.us-east-1.amazonaws.com/dev/health")

#     assert response.status == 200
#     json_data = response.json()
#     assert json_data["status"] == "healthy"
#     assert json_data["service"] == "vop-ingest-service"
#     print(json_data)
#     request.dispose()

# def test_GET_All_Vehicle_data(playwright):
#     request = playwright.request.new_context()
#     response = request.get("https://6pu7wjaw9d.execute-api.us-east-1.amazonaws.com/dev/telemetry")

#     assert response.status == 200
#     json_data = response.json()
#     print(json_data)
#     request.dispose()

import pytest

class TestHealth:

    def test_returns_200(self, api):
        response = api.get_health()
        assert response.status_code == 200

    def test_status_is_healthy(self, api):
        data = api.get_health().json()
        assert data["status"] == "healthy"

    def test_service_name_correct(self, api):
        data = api.get_health().json()
        assert data["service"] == "vop-ingest-service"

    def test_contains_timestamp(self, api):
        data = api.get_health().json()
        assert "timestamp" in data

    def test_response_time_under_2_seconds(self, api):
        response = api.get_health()
        assert response.elapsed.total_seconds() < 2


class TestGetAllTelemetry:

    def test_returns_200(self, api):
        response = api.get_all_telemetry()
        assert response.status_code == 200

    def test_contains_records_list(self, api):
        data = api.get_all_telemetry().json()
        assert "records" in data
        assert isinstance(data["records"], list)

    def test_contains_count(self, api):
        data = api.get_all_telemetry().json()
        assert "count" in data

    def test_count_matches_records_length(self, api):
        data = api.get_all_telemetry().json()
        assert data["count"] == len(data["records"])