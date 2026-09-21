from abc import ABC, abstractmethod
from typing import Optional

class CachePort(ABC):
    """Puerto abstracto para el mecanismo de almacenamiento en caché de alto rendimiento."""

    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """Recupera un valor de la memoria caché por su clave."""
        pass

    @abstractmethod
    async def set(self, key: str, value: str, ttl_seconds: int = 3600) -> None:
        """Almacena un valor serializado en caché con un tiempo de vida (TTL) determinado."""
        pass
