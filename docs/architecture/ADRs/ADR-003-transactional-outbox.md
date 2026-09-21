# ADR-003: Implementación del Patrón Transactional Outbox para Evitar el Double Write Problem

## Estado
Aceptado

## Contexto
En `itinerary-service`, la creación de un itinerario requiere tanto la persistencia relacional en la base de datos como la emisión de un evento de integración (`ItineraryCreatedEvent`) hacia RabbitMQ para que el componente Serverless lo procese. Si el servicio guarda en base de datos e intenta publicar en RabbitMQ, una caída del broker o de la red en ese instante dejaría el itinerario guardado pero la notificación nunca emitida (inconsistencia de datos). Por el contrario, si se publica primero y la transacción en la base de datos falla, se emitiría una notificación fantasma.

## Decisión
Se implementa el patrón **Transactional Outbox**:
1. Dentro de la **misma transacción atómica ACID** de base de datos se almacena el registro en la tabla `itineraries` y el evento en la tabla `outbox_events` con estado `PENDING`.
2. Un proceso en segundo plano (`outbox_relay_worker`) consulta los eventos pendientes (`status = 'PENDING'`), los publica a RabbitMQ y actualiza su estado a `PUBLISHED` con la marca de tiempo de despacho.
3. Se implementa confirmación de publicación (Publisher Confirms) para garantizar entrega de tipo *at-least-once*.

## Consecuencias
### Positivas:
- Se elimina completamente el problema de doble escritura (*Double Write Problem*).
- La API responde de forma inmediata al cliente sin quedar bloqueada por latencias o fallas temporales del broker de mensajería.
- Se mantiene consistencia eventual garantizada entre el almacenamiento transaccional y los consumidores asíncronos.

### Negativas / Mitigaciones:
- Requiere un worker en segundo plano y ligera latencia adicional en la entrega del mensaje (completamente despreciable, inferior a 1 segundo).
- Consumo *at-least-once* exige idempotencia en los consumidores finales (el consumidor FaaS valida la unicidad del `event_id`).
