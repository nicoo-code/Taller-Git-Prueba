import pytest
import uuid
import os
from src.storage.notification_repository import NotificationRepository
from src.functions.send_notification_function import SendNotificationFunction
from src.functions.generate_report_function import GenerateReportFunction

@pytest.fixture
def temp_db(tmp_path):
    db_file = str(tmp_path / "test_notifications.db")
    return db_file

@pytest.mark.asyncio
async def test_send_notification_function_and_idempotency(temp_db):
    repo = NotificationRepository(db_path=temp_db)
    func = SendNotificationFunction(repo)

    event_id = str(uuid.uuid4())
    itinerary_id = str(uuid.uuid4())
    event_payload = {
        "event_id": event_id,
        "event_type": "ItineraryCreatedEvent",
        "trace_id": "trace-987654",
        "data": {
            "itinerary_id": itinerary_id,
            "user_name": "Maria Rodriguez",
            "origin_airport_id": 1,
            "destination_airport_id": 12,
            "departure_date": "2026-11-01T10:00:00Z",
            "duration_minutes": 75
        }
    }

    # 1. Primer despacho debe tener éxito
    success = await func.execute(event_payload)
    assert success is True

    # 2. Verificar que se persistió en la BD
    logs = repo.list_all()
    assert len(logs) == 1
    assert logs[0]["event_id"] == event_id
    assert logs[0]["recipient"] == "Maria Rodriguez"
    assert logs[0]["status"] == "SENT"

    # 3. Segundo despacho con el mismo event_id debe detectar duplicado (idempotencia)
    duplicate_success = await func.execute(event_payload)
    assert duplicate_success is False
    assert len(repo.list_all()) == 1

def test_generate_report_function(temp_db):
    repo = NotificationRepository(db_path=temp_db)
    repo.save_notification("ev-1", "it-1", "User A", "EMAIL", "Test 1", "SENT")
    repo.save_notification("ev-2", "it-2", "User B", "EMAIL", "Test 2", "SENT")

    report_func = GenerateReportFunction(repo)
    report = report_func.execute()

    assert report["total_notifications"] == 2
    assert report["total_sent"] == 2
    assert report["channels_breakdown"]["EMAIL"] == 2
