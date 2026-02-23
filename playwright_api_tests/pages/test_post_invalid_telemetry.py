class TestPostInvalidTelemetry:

    def test_returns_400(self,api,invalid_payload):
        response = api.post_telemetry(invalid_payload)
        assert response.status == 400