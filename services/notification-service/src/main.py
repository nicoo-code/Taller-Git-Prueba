import asyncio
import logging
import sys
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config import settings
from src.storage.notification_repository import NotificationRepository
from src.functions.send_notification_function import SendNotificationFunction
from src.functions.generate_report_function import GenerateReportFunction
from src.consumers.rabbitmq_event_consumer import RabbitMQEventConsumer

# Logging Estructurado JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "service": settings.service_name,
            "message": record.getMessage(),
            "module": record.module,
            "trace_id": getattr(record, "trace_id", "00000000000000000000000000000000")
        }
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO), handlers=[handler])
logger = logging.getLogger(settings.service_name)

# Inicialización de dependencias
repo = NotificationRepository(db_path=settings.db_path)
send_func = SendNotificationFunction(repo=repo)
report_func = GenerateReportFunction(repo=repo)
consumer = RabbitMQEventConsumer(amqp_url=settings.rabbitmq_url, notification_func=send_func)

consumer_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global consumer_task
    logger.info("Starting Serverless Notification Event Consumer...")
    consumer_task = asyncio.create_task(consumer.start())
    yield
    logger.info("Stopping Serverless Notification Event Consumer...")
    consumer.stop()
    if consumer_task:
        consumer_task.cancel()

app = FastAPI(
    title="Notification Microservice (Serverless / FaaS)",
    description="Componente reactivo para procesamiento asíncrono de eventos de itinerarios y reportes bajo demanda.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health():
    return {
        "status": "UP",
        "service": "notification-service",
        "consumer_active": consumer._is_running
    }

@app.get("/api/v1/notifications/report")
async def get_report():
    """Función serverless ejecutada bajo demanda para consolidar reportes."""
    return report_func.execute()

@app.get("/api/v1/notifications/logs")
async def get_logs():
    return repo.list_all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
