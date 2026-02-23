class TestPostTelemetry:

    def test_returns_200(self, api, valid_payload):
        response = api.post_telemetry(valid_payload)
        assert response.status == 200

    def test_returns_message(self,api, valid_payload):
        response = api.post_telemetry(valid_payload)
        data = response.json()
        assert data["message"] == "Telemetry stored"


    