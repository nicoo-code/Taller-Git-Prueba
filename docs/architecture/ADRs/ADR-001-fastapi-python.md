# ADR-001: Selección de FastAPI y Python 3.11+ para los Microservicios

## Estado
Aceptado

## Contexto
El sistema requiere construir microservicios independientes y asíncronos para la gestión de itinerarios, integración de aeropuertos y procesamiento reactivo. Es necesario contar con un framework moderno que proporcione alto rendimiento en operaciones I/O concurrentes (comunicación HTTP y mensajería AMQP), generación automática de documentación interactiva OpenAPI (Swagger) y tipado estricto con Pydantic.

## Decisión
Se adopta **FastAPI** sobre Python 3.11+ como el framework estándar para los microservicios (`airport-service`, `itinerary-service` y `api-gateway`).

## Consecuencias
### Positivas:
- Soporte nativo de concurrencia asíncrona (`async`/`await`), reduciendo la sobrecarga de hilos y mejorando los tiempos de respuesta.
- Documentación OpenAPI/Swagger autogenerada e interactiva accesible sin esfuerzo adicional en `/docs`.
- Validación de esquemas y contratos de entrada/salida de alto rendimiento mediante Pydantic v2.
- Ecosistema maduro de librerías para observabilidad (OpenTelemetry), bases de datos (SQLAlchemy 2.0 / Alembic) y clientes HTTP (`httpx`).

### Negativas / Mitigaciones:
- Requiere cuidado en la gestión de librerías sincrónicas bloqueantes para evitar degradar el event loop de asyncio (se mitiga empleando `httpx.AsyncClient` y conexiones asíncronas de base de datos o threadpools dedicados).
