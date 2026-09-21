import sqlite3
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class NotificationRepository:
    """Repositorio de persistencia ligera para la auditoría de notificaciones FaaS."""

    def __init__(self, db_path: str = "notifications.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications_log (
                    id TEXT PRIMARY KEY,
                    event_id TEXT UNIQUE,
                    itinerary_id TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    message TEXT NOT NULL,
                    status TEXT NOT NULL,
                    sent_at TIMESTAMP NOT NULL
                )
            """)
            conn.commit()

    def save_notification(
        self,
        event_id: str,
        itinerary_id: str,
        recipient: str,
        channel: str,
        message: str,
        status: str = "SENT"
    ) -> bool:
        """Almacena la notificación garantizando idempotencia a través de event_id."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                notif_id = str(uuid.uuid4())
                now = datetime.utcnow().isoformat() + "Z"
                cursor.execute("""
                    INSERT INTO notifications_log (id, event_id, itinerary_id, recipient, channel, message, status, sent_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (notif_id, event_id, itinerary_id, recipient, channel, message, status, now))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                logger.warning(f"Event {event_id} already processed (idempotency caught duplicate).")
                return False

    def list_all(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notifications_log ORDER BY sent_at DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
