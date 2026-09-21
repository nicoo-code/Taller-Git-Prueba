# ADR-004: Resiliencia con Circuit Breaker, Reintentos con Backoff Exponencial y Redis Cache

## Estado
Aceptado

## Contexto
El microservicio `airport-service` depende de un endpoint público de terceros (`https://api-colombia.com/api/v1/Airport`). Si esta API externa sufre degradación de servicio, latencias elevadas (>3 segundos) o caídas totales, el microservicio corre el riesgo de agotar sus hilos/conexiones de red (cascading failure), impactando directamente a `itinerary-service` y al frontend de los usuarios.

## Decisión
Se implementa una estrategia de resiliencia multicapa en el adaptador de API Colombia:
1. **Patrón Circuit Breaker:**
   - Máquina de estados con tres estados: `CLOSED`, `OPEN` y `HALF-OPEN`.
   - Umbral de falla: 3 errores consecutivos o timeouts (>3.0s).
   - Período de recuperación: 30 segundos en estado `OPEN` antes de permitir una petición de prueba en `HALF-OPEN`.
   - En estado `OPEN`, el circuito rechaza la llamada de inmediato o entrega datos seguros en memoria/cache en <5ms sin sobrecargar la red externa.
2. **Reintentos con Backoff Exponencial y Jitter:**
   - Hasta 3 reintentos con intervalo base de 0.5s multiplicado por $2^{\text{intento}}$ más un jitter aleatorio de 0 a 100ms para evitar tormentas de reintentos concurrentes.
3. **Caché en Memoria con Redis:**
   - La lista de aeropuertos se almacena en Redis con un TTL de 3600 segundos (1 hora), sirviendo como fallback inmediato y acelerador de rendimiento.

## Consecuencias
### Positivas:
- Alta disponibilidad y tolerancia a fallos: el sistema permanece funcional incluso durante la caída prolongada de API Colombia.
- Tiempos de respuesta óptimos (<15ms) en el 95% de las peticiones gracias al cache Redis.
- Falla rápida (*Fail-Fast*) que protege los recursos del servidor.

### Negativas / Mitigaciones:
- Riesgo de servir datos ligeramente desactualizados durante la ventana de caché (aceptable, dado que los aeropuertos son datos de referencia de cambio infrecuente).
