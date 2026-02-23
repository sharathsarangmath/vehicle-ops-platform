import requests


class VehicleAPIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def get_health(self):
        return self.session.get(f"{self.base_url}/health")

    def post_telemetry(self, payload: dict):
        return self.session.post(
            f"{self.base_url}/telemetry",
            json=payload
        )

    def post_telemetry_raw(self, data: str):
        return self.session.post(
            f"{self.base_url}/telemetry",
            data=data,
            headers={"Content-Type": "application/json"}
        )

    def get_all_telemetry(self):
        return self.session.get(f"{self.base_url}/telemetry")

    def get_alerts(self):
        return self.session.get(f"{self.base_url}/alerts")

    def get_no_alerts(self):
        return self.session.get(
            f"{self.base_url}/telemetry/no-alerts"
        )

    def get_vehicle(self, vehicle_id: str):
        return self.session.get(
            f"{self.base_url}/vehicle/{vehicle_id}"
        )

    def get_vehicle_alerts(self, vehicle_id: str):
        return self.session.get(
            f"{self.base_url}/vehicle/{vehicle_id}/alerts"
        )

    def get_unknown_route(self):
        return self.session.get(
            f"{self.base_url}/doesnotexist"
        )