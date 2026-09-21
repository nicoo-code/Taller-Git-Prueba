import asyncio
import logging
import sys
import json
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.infrastructure.config import settings
from src.infrastructure.persistence.models import Base
from src.infrastructure.persistence.sqlalchemy_itinerary_repo import SqlAlchemyItineraryRepository
from src.infrastructure.clients.airport_http_validator import AirportHttpValidator
from src.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from src.infrastructure.messaging.outbox_relay_worker import OutboxRelayWorker
from src.application.create_itinerary import CreateItineraryUseCase
from src.application.get_itinerary import GetItineraryUseCase, ListItinerariesUseCase, DeleteItineraryUseCase
from src.infrastructure.api.router import create_itinerary_router

# Logging Estructurado JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "service": settings.service_name,
            "message": record.getMessage(),
            "module": record.module,
            "trace_id": getattr(record, "trace_id", "00000000000000000000000000000000"),
            "span_id": getattr(record, "span_id", "0000000000000000")
        }
        return json.dumps(log_record)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO), handlers=[handler])
logger = logging.getLogger(settings.service_name)

# Configuración de Base de Datos
connect_args = {"check_same_thread": False} if "sqlite" in settings.database_url else {}
engine = create_engine(settings.database_url, connect_args=connect_args, echo=False)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Inicialización Hexagonal
itinerary_repo = SqlAlchemyItineraryRepository(session_factory=SessionFactory)
airport_validator = AirportHttpValidator(airport_service_url=settings.airport_service_url)
rabbitmq_publisher = RabbitMQPublisher(amqp_url=settings.rabbitmq_url)
outbox_worker = OutboxRelayWorker(outbox_repo=itinerary_repo, publisher=rabbitmq_publisher, poll_interval_seconds=1.0)

create_uc = CreateItineraryUseCase(itinerary_repo=itinerary_repo, airport_validator=airport_validator)
get_uc = GetItineraryUseCase(itinerary_repo=itinerary_repo)
list_uc = ListItinerariesUseCase(itinerary_repo=itinerary_repo)
delete_uc = DeleteItineraryUseCase(itinerary_repo=itinerary_repo)

worker_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global worker_task
    logger.info("Initializing Outbox Relay Worker and RabbitMQ connection...")
    try:
        await rabbitmq_publisher.connect()
    except Exception as e:
        logger.warning(f"RabbitMQ initial connection postponed: {e}")

    worker_task = asyncio.create_task(outbox_worker.start())
    yield
    logger.info("Shutting down Outbox Relay Worker...")
    outbox_worker.stop()
    if worker_task:
        worker_task.cancel()
    await rabbitmq_publisher.close()

app = FastAPI(
    title="Itinerary Microservice - Transactional Outbox & DDD",
    description="Microservicio para gestión de itinerarios personales con validación HTTP y garantía de consistencia con Outbox.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de Correlation ID
@app.middleware("http")
async def trace_and_log_middleware(request: Request, call_next):
    trace_parent = request.headers.get("traceparent")
    trace_id = "00000000000000000000000000000000"
    if trace_parent and "-" in trace_parent:
        parts = trace_parent.split("-")
        if len(parts) >= 2:
            trace_id = parts[1]

    request.state.trace_id = trace_id
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000

    extra = {"trace_id": trace_id}
    logger.info(
        f"{request.method} {request.url.path} - Status {response.status_code} ({duration_ms:.2f}ms)",
        extra=extra
    )
    return response

# OpenTelemetry opcional
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    FastAPIInstrumentor.instrument_app(app)
except Exception:
    pass

app.include_router(
    create_itinerary_router(
        create_uc=create_uc,
        get_uc=get_uc,
        list_uc=list_uc,
        delete_uc=delete_uc,
        session_factory=SessionFactory,
        worker_status_callback=lambda: outbox_worker._is_running
    )
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)
