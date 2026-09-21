import pytest
import uuid
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Agregar rutas de servicios al sys.path para soportar carpetas con guiones
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(ROOT_DIR, "services/airport-service"))
sys.path.insert(0, os.path.join(ROOT_DIR, "services/itinerary-service"))
sys.path.insert(0, os.path.join(ROOT_DIR, "services/notification-service"))

from src.infrastructure.adapters.api_colombia_adapter import ApiColombiaAdapter
from src.infrastructure.adapters.redis_cache_adapter import RedisCacheAdapter
from src.application.list_airports import ListAirportsUseCase
from src.application.get_airport_by_id import GetAirportByIdUseCase

from src.infrastructure.persistence.models import Base
from src.infrastructure.persistence.sqlalchemy_itinerary_repo import SqlAlchemyItineraryRepository
from src.application.create_itinerary import CreateItineraryUseCase
from src.domain.ports.airport_validator_port import AirportValidatorPort

from src.storage.notification_repository import NotificationRepository
from src.functions.send_notification_function import SendNotificationFunction

class LocalAirportValidator(AirportValidatorPort):
    def __init__(self, airport_uc: GetAirportByIdUseCase):
        self.airport_uc = airport_uc

    async def validate_airport_exists(self, airport_id: int) -> bool:
        airport = await self.airport_uc.execute(airport_id)
        return airport is not None

@pytest.mark.asyncio
async def test_full_distributed_flow_e2e(tmp_path):
    # 1. Configurar Airport Service
    cache_adapter = RedisCacheAdapter()
    api_adapter = ApiColombiaAdapter(max_retries=1)
    list_airports_uc = ListAirportsUseCase(external_port=api_adapter, cache_port=cache_adapter)
    get_airport_uc = GetAirportByIdUseCase(external_port=api_adapter, list_use_case=list_airports_uc)

    airports = await list_airports_uc.execute()
    assert len(airports) > 0, "Debe haber aeropuertos en el catálogo"
    origin = airports[0]
    dest = airports[1]

    # 2. Configurar Itinerary Service con BD SQLite temporal
    db_file = str(tmp_path / "e2e_itineraries.db")
    engine = create_engine(f"sqlite:///{db_file}", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionFactory = sessionmaker(bind=engine)
    itinerary_repo = SqlAlchemyItineraryRepository(session_factory=SessionFactory)

    validator = LocalAirportValidator(get_airport_uc)
    create_itin_uc = CreateItineraryUseCase(itinerary_repo=itinerary_repo, airport_validator=validator)

    # 3. Crear Itinerario (Validación síncrona + Transacción Atómica Outbox)
    departure_time = datetime.utcnow()
    new_itinerary = await create_itin_uc.execute(
        user_name="Usuario E2E",
        origin_airport_id=origin.id,
        destination_airport_id=dest.id,
        departure_date=departure_time,
        duration_minutes=50,
        trace_id="trace-e2e-12345"
    )

    assert new_itinerary.id is not None
    assert new_itinerary.status == "CREATED"

    # 4. Verificar que en la BD relacional se creó el evento PENDING en outbox_events
    pending_events = await itinerary_repo.get_pending_events(limit=10)
    assert len(pending_events) >= 1
    event = next(e for e in pending_events if str(e.aggregate_id) == str(new_itinerary.id))
    assert event.status == "PENDING"
    assert event.event_type == "ItineraryCreatedEvent"

    # 5. Simular Relé hacia el componente Serverless de Notificaciones
    notif_db = str(tmp_path / "e2e_notifications.db")
    notif_repo = NotificationRepository(db_path=notif_db)
    notif_func = SendNotificationFunction(repo=notif_repo)

    processed = await notif_func.execute(event.payload)
    assert processed is True

    # 6. Actualizar Outbox a PUBLISHED
    await itinerary_repo.mark_as_published(event.id)
    pending_after = await itinerary_repo.get_pending_events(limit=10)
    assert not any(str(e.id) == str(event.id) for e in pending_after)

    # 7. Verificar auditoría final en notification service
    logs = notif_repo.list_all()
    assert len(logs) == 1
    assert logs[0]["itinerary_id"] == str(new_itinerary.id)
    assert logs[0]["status"] == "SENT"
    assert "Usuario E2E" in logs[0]["recipient"]
