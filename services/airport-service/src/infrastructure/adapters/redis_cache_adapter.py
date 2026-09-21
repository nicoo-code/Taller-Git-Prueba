import logging
import time
from typing import Optional, Dict, Tuple
from src.domain.ports.cache_port import CachePort

logger = logging.getLogger(__name__)

class RedisCacheAdapter(CachePort):
    """Adaptador de caché que utiliza Redis asíncrono con fallback transparente en memoria."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self._redis_client = None
        self._in_memory_fallback: Dict[str, Tuple[str, float]] = {}

    async def _get_client(self):
        if self._redis_client is None:
            try:
                import redis.asyncio as aioredis
                self._redis_client = aioredis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=2.0
                )
            except Exception as e:
                logger.warning(f"Could not initialize Redis client, using in-memory cache: {e}")
        return self._redis_client

    async def get(self, key: str) -> Optional[str]:
        client = await self._get_client()
        if client:
            try:
                return await client.get(key)
            except Exception as e:
                logger.warning(f"Redis GET failed for key '{key}': {e}. Falling back to in-memory.")

        # Fallback en memoria
        if key in self._in_memory_fallback:
            val, expire_at = self._in_memory_fallback[key]
            if time.time() < expire_at:
                return val
            else:
                del self._in_memory_fallback[key]
        return None

    async def set(self, key: str, value: str, ttl_seconds: int = 3600) -> None:
        client = await self._get_client()
        if client:
            try:
                await client.set(key, value, ex=ttl_seconds)
                return
            except Exception as e:
                logger.warning(f"Redis SET failed for key '{key}': {e}. Falling back to in-memory.")

        # Fallback en memoria
        self._in_memory_fallback[key] = (value, time.time() + ttl_seconds)

    async def ping(self) -> bool:
        client = await self._get_client()
        if client:
            try:
                await client.ping()
                return True
            except Exception:
                return False
        return False
