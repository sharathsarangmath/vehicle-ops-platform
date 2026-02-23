class TestAllVehicleAlerts: 
    
    def test_returns_200(self, api):
        response = api.get_all_vehicle_alerts()
        assert response.status == 200

    def test_contains_records_list(self, api):
        response = api.get_all_vehicle_alerts()
        data = response.json()
        assert "records" in data 
        assert isinstance(data["records"], list)

    def test_contains_count(self, api):
        response = api.get_all_vehicle_alerts()
        data = response.json()
        assert "count" in data