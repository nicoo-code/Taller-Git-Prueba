import os
from pydantic import BaseModel

class Settings(BaseModel):
    service_name: str = "notification-service"
    service_port: int = int(os.getenv("PORT", "8003"))
    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    db_path: str = os.getenv("NOTIFICATIONS_DB_PATH", "notifications.db")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
