import json
import logging
from typing import Dict, Any
from src.storage.notification_repository import NotificationRepository

logger = logging.getLogger("notification-function")

class SendNotificationFunction:
    """
    Función FaaS reactiva (Serverless).
    Se activa única y exclusivamente ante la recepción de ItineraryCreatedEvent.
    """

    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    async def execute(self, event_data: Dict[str, Any]) -> bool:
        """Punto de entrada de ejecución de la función sin servidor."""
        event_id = event_data.get("event_id")
        event_type = event_data.get("event_type")
        trace_id = event_data.get("trace_id", "00000000000000000000000000000000")
        data = event_data.get("data", {})

        if event_type != "ItineraryCreatedEvent" or not data:
            logger.warning(f"Ignored unknown or invalid event type: {event_type}")
            return False

        itinerary_id = data.get("itinerary_id")
        user_name = data.get("user_name")
        origin_id = data.get("origin_airport_id")
        dest_id = data.get("destination_airport_id")
        departure_date = data.get("departure_date")
        duration = data.get("duration_minutes")

        # Simular despacho de notificación (Email / SMS)
        message = (
            f"Estimado(a) {user_name}, su itinerario de viaje [{itinerary_id}] ha sido confirmado. "
            f"Ruta: Aeropuerto {origin_id} -> Aeropuerto {dest_id}. "
            f"Fecha de salida: {departure_date}. Duración estimada: {duration} minutos."
        )

        logger.info(
            f"[FaaS] Dispatching simulated email notification to '{user_name}': {message}",
            extra={"trace_id": trace_id}
        )

        # Almacenar en auditoría
        saved = self.repo.save_notification(
            event_id=event_id,
            itinerary_id=itinerary_id,
            recipient=user_name,
            channel="EMAIL",
            message=message,
            status="SENT"
        )

        return saved
