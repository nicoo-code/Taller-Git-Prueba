import random
from datetime import datetime, timedelta
from locust import HttpUser, task, between

class SystemLoadUser(HttpUser):
    wait_time = between(1, 2.5)

    @task(3)
    def view_airports_catalog(self):
        self.client.get("/api/v1/airports", name="/api/v1/airports")

    @task(2)
    def view_plotly_map(self):
        self.client.get("/api/v1/airports/map/plotly", name="/api/v1/airports/map/plotly")

    @task(1)
    def create_itinerary(self):
        origin = random.choice([1, 9, 12, 18])
        dest = random.choice([5, 15, 22, 25])
        future_date = (datetime.utcnow() + timedelta(days=random.randint(1, 30))).isoformat() + "Z"

        payload = {
            "user_name": f"LocustPassenger_{random.randint(100, 999)}",
            "origin_airport_id": origin,
            "destination_airport_id": dest,
            "departure_date": future_date,
            "duration_minutes": random.choice([45, 60, 90, 120])
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer locust-token"
        }

        self.client.post("/api/v1/itineraries", json=payload, headers=headers, name="/api/v1/itineraries")

    @task(2)
    def list_itineraries(self):
        self.client.get("/api/v1/itineraries", name="/api/v1/itineraries [GET]")
