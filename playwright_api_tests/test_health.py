class TestHealth:

    def test_returns_200(self, api):
        response = api.get_health()
        assert response.status == 200

    def test_status_is_healthy(self, api):
        response = api.get_health()
        data = response.json()
        assert data["status"] == "healthy"
        
        