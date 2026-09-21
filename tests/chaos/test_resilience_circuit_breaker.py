#!/usr/bin/env python
"""
Demostración Automatizada de Resiliencia: Circuit Breaker ante Falla Controlada.
Este script evidencia cómo el sistema tolera la caída o degradación extrema de la API externa
de Colombia, protegiendo los recursos y respondiendo mediante fallback en < 5ms.
"""

import asyncio
import os
import sys
import time

# Ajustar PYTHONPATH
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../services/airport-service")
    ),
)

from src.infrastructure.adapters.api_colombia_adapter import ApiColombiaAdapter
from src.infrastructure.adapters.circuit_breaker import CircuitBreaker, CircuitState


async def run_resilience_demo():
    print("=" * 70)
    print("DEMOSTRACIÓN DE RESILIENCIA: CIRCUIT BREAKER ANTE FALLA CONTROLADA")
    print("=" * 70)

    # 1. Configurar adaptador apuntando a endpoint inaccesible con Circuit Breaker estricto
    cb = CircuitBreaker(
        failure_threshold=3, recovery_timeout=2.0, name="ChaosTestBreaker"
    )
    adapter = ApiColombiaAdapter(
        base_url="http://10.255.255.1:9999/unreachable-endpoint",  # IP no enrutable para simular timeout
        circuit_breaker=cb,
        timeout=0.1,  # 100ms timeout para la prueba
        max_retries=1,
    )

    print(f"\n[PASO 1] Estado Inicial del Circuito: {cb.state.value}")
    assert cb.state == CircuitState.CLOSED, "El circuito debe iniciar CLOSED"

    # 2. Provocar fallas controladas consecutivas
    print("\n[PASO 2] Inyectando fallas de red hacia el proveedor externo...")
    for i in range(1, 4):
        t0 = time.time()
        airports = await adapter.get_all_airports()
        elapsed = (time.time() - t0) * 1000
        print(
            f"  -> Intento #{i}: Fallo registrado. Tiempo: {elapsed:.2f}ms. Fallas acumuladas: {cb.failure_count}/{cb.failure_threshold}"
        )

    print("\n[PASO 3] Verificando apertura del circuito...")
    print(f"  -> Estado actual del Circuito: {cb.state.value}")
    assert (
        cb.state == CircuitState.OPEN
    ), "El circuito debió dispararse a OPEN tras 3 fallos"
    print("  [OK] ¡El Circuit Breaker se ha ABIERTO con éxito!")

    # 3. Demostración de Fail-Fast y Fallback en estado OPEN
    print("\n[PASO 4] Evaluando comportamiento Fail-Fast en estado OPEN...")
    times = []
    for i in range(1, 6):
        t0 = time.time()
        airports = await adapter.get_all_airports()
        elapsed = (time.time() - t0) * 1000
        times.append(elapsed)
        print(
            f"  -> Petición #{i} (Circuito OPEN): Retornó {len(airports)} aeropuertos de fallback en {elapsed:.3f}ms"
        )

    avg_time = sum(times) / len(times)
    print(
        f"\n  [EVIDENCIA] Tiempo promedio de respuesta en OPEN: {avg_time:.3f}ms (Menos de 5ms)"
    )
    assert (
        avg_time < 5.0
    ), f"El tiempo promedio debe ser menor a 5ms, obtenido: {avg_time}ms"

    # 4. Probar recuperación a HALF-OPEN
    print("\n[PASO 5] Esperando ventana de recuperación (2.0 segundos)...")
    await asyncio.sleep(2.1)

    print("  -> Evaluando transición de prueba...")
    # Ejecutamos una llamada que forzará HALF-OPEN
    # Al fallar nuevamente regresará a OPEN
    airports = await adapter.get_all_airports()
    print(
        f"  -> Estado posterior a prueba: {cb.state.value} (Retornó fallback sin saturar)"
    )

    print("\n" + "=" * 70)
    print("RESULTADO DE LA PRUEBA: EXITOSA. RESILIENCIA VERIFICADA.")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_resilience_demo())
