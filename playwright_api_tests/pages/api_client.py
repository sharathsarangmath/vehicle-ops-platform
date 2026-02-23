class VehicleAPIClient:

    def __init__(self, request, api_url):
        self.request = request
        self.api_url = api_url

    def get_health(self):
        return self.request.get(f"{self.api_url}/health")

    def get_all_vehicle_data(self):
        return self.request.get(f"{self.api_url}/telemetry")

    def get_all_vehicle_alerts(self):
        return self.request.get(f"{self.api_url}/alerts")

    def post_telemetry(self, payload:dict):
        return self.request.post(f"{self.api_url}/telemetry", data=payload)
    