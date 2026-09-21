from typing import Dict, Any
from src.storage.notification_repository import NotificationRepository

class GenerateReportFunction:
    """Función Serverless ejecutada bajo demanda para consolidar métricas de notificaciones e itinerarios."""

    def __init__(self, repo: NotificationRepository):
        self.repo = repo

    def execute(self) -> Dict[str, Any]:
        logs = self.repo.list_all()
        total_sent = sum(1 for item in logs if item.get("status") == "SENT")
        channels = {}
        for item in logs:
            ch = item.get("channel", "UNKNOWN")
            channels[ch] = channels.get(ch, 0) + 1

        return {
            "total_notifications": len(logs),
            "total_sent": total_sent,
            "channels_breakdown": channels,
            "recent_events": logs[:10]
        }
