import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for service in [
    "airport-service",
    "itinerary-service",
    "notification-service",
    "api-gateway",
]:
    svc_path = os.path.join(ROOT_DIR, "services", service)
    if svc_path not in sys.path:
        sys.path.insert(0, svc_path)
