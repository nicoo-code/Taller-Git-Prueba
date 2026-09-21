# Backlog de Producto y Planificación Ágil (Jira Simulator)
## Proyecto: Sistema Distribuido de Itinerarios Personales (SDIP)

**Metodología:** Scrum / Kanban  
**Duración del Sprint:** 2 semanas  
**Herramienta de Gestión:** Jira Software Simulation  

---

## 1. Resumen de Épicas

| Clave | Nombre de la Épica | Descripción | Story Points Totales |
| :--- | :--- | :--- | :--- |
| **AIRP** | Catálogo de Aeropuertos y Visualización Geográfica | Consumo desacoplado de API Colombia, resiliencia y mapa Plotly JS. | 13 SP |
| **ITIN** | Gestión de Itinerarios y Comunicación Asíncrona | CRUD transaccional, validación HTTP y Transactional Outbox. | 13 SP |
| **OPS** | Notificaciones Serverless y Observabilidad Distribuida | Función reactiva FaaS en RabbitMQ, trazas Jaeger y CI/CD. | 13 SP |

---

## 2. Historias de Usuario Detalladas

### ÉPICA 1: Catálogo de Aeropuertos y Visualización Geográfica (AIRP)

#### US-01: Consumo y Adaptación de API Colombia mediante Patrón Adapter
- **Clave:** AIRP-01
- **Prioridad:** Alta (P1)
- **Story Points:** 5
- **Descripción:**
  *Como* desarrollador del sistema de itinerarios,  
  *quiero* consumir los datos de aeropuertos colombianos mediante una interfaz abstracta y un adaptador desacoplado,  
  *para que* el núcleo del dominio no dependa directamente de los cambios de esquema del proveedor externo `api-colombia.com`.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Obtención y mapeo exitoso de la lista de aeropuertos
    Dado que el servicio de aeropuertos invoca el puerto 'ExternalAirportPort'
    Cuando el adaptador 'ApiColombiaAdapter' consulta el endpoint 'https://api-colombia.com/api/v1/Airport'
    Entonces la respuesta JSON externa se transforma en instancias del modelo de dominio 'Airport'
    Y cada aeropuerto incluye id, nombre, código IATA, ciudad y coordenadas geográficas válidas.

  Escenario: Manejo de errores por aeropuerto inexistente
    Dado que se solicita un aeropuerto con el ID 99999 que no existe en el catálogo externo
    Cuando se ejecuta el caso de uso 'GetAirportByIdUseCase'
    Entonces el servicio retorna None
    Y la API REST responde con código de estado HTTP 404 Not Found.
  ```

---

#### US-02: Resiliencia con Circuit Breaker, Reintentos y Redis Cache
- **Clave:** AIRP-02
- **Prioridad:** Alta (P1)
- **Story Points:** 5
- **Descripción:**
  *Como* operador del sistema,  
  *quiero* que las consultas al catálogo de aeropuertos toleren caídas y demoras de la API externa mediante Circuit Breaker, reintentos con backoff exponencial y cache Redis,  
  *para que* el servicio mantenga alta disponibilidad y tiempos de respuesta inferiores a 15ms.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Apertura del circuito tras fallos repetidos
    Dado que la API externa de Colombia se encuentra fuera de servicio o presenta latencia superior a 3 segundos
    Cuando se registran 3 fallas consecutivas en las peticiones al adaptador
    Entonces el Circuit Breaker cambia su estado a 'OPEN'
    Y las peticiones subsecuentes son atendidas inmediatamente desde la memoria caché de Redis sin saturar la red externa.

  Escenario: Transición a Half-Open tras ventana de recuperación
    Dado que el Circuit Breaker ha permanecido en estado 'OPEN' durante 30 segundos
    Cuando ingresa una nueva solicitud de aeropuertos
    Entonces el circuito pasa a estado 'HALF-OPEN' permitiendo una única petición de prueba
    Y si la petición es exitosa, el circuito se restablece a estado 'CLOSED'.
  ```

---

#### US-03: Visualización Interactiva en Mapa Geográfico con Plotly JS
- **Clave:** AIRP-03
- **Prioridad:** Media (P2)
- **Story Points:** 3
- **Descripción:**
  *Como* usuario planificador de viajes,  
  *quiero* visualizar todos los aeropuertos colombianos en un mapa interactivo renderizado con Plotly JS,  
  *para* identificar con facilidad las opciones de origen y destino de mi itinerario.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Renderizado cartográfico de aeropuertos
    Dado que el usuario carga la página principal del frontend
    Cuando el navegador consulta el endpoint '/api/v1/airports/map/plotly'
    Entonces el backend retorna la estructura scattergeo con latitudes, longitudes y etiquetas IATA
    Y Plotly JS dibuja el mapa de Colombia con los marcadores interactivos de los aeropuertos.
  ```

---

### ÉPICA 2: Gestión de Itinerarios y Comunicación Asíncrona (ITIN)

#### US-04: CRUD de Itinerarios y Validación HTTP con Airport Service
- **Clave:** ITIN-01
- **Prioridad:** Crítica (P0)
- **Story Points:** 5
- **Descripción:**
  *Como* pasajero del sistema,  
  *quiero* registrar, consultar y gestionar mis itinerarios de vuelo,  
  *para* asegurar que solo se creen reservas con aeropuertos de origen y destino reales y verificados.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Validación exitosa de aeropuertos antes de guardar itinerario
    Dado que el usuario envía una solicitud de itinerario con origen ID 1 y destino ID 5
    Cuando el servicio de itinerarios consulta al servicio de aeropuertos
    Entonces ambos aeropuertos son verificados como existentes (código 200 OK)
    Y el itinerario se persiste en la base de datos dentro de la misma transacción que el outbox
    Y la API responde con código HTTP 201 Created y el UUID generado.

  Escenario: Rechazo de itinerario por aeropuerto inexistente
    Dado que el usuario intenta crear un itinerario con un aeropuerto de destino ID 99999 inválido
    Cuando el servicio de itinerarios valida la existencia con el servicio de aeropuertos
    Entonces el servicio de aeropuertos responde 404 Not Found
    Y el itinerario es rechazado con código HTTP 400 Bad Request sin persistir ningún dato.
  ```

---

#### US-05: Implementación de Transactional Outbox para Evitar Double Write
- **Clave:** ITIN-02
- **Prioridad:** Crítica (P0)
- **Story Points:** 8
- **Descripción:**
  *Como* arquitecto de software,  
  *quiero* que la inserción del itinerario y el registro del evento de integración se ejecuten en una sola transacción atómica de base de datos relacional,  
  *para* eliminar el Double Write Problem y garantizar que nunca se pierda un evento de notificación hacia RabbitMQ.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Inserción atómica y publicación garantizada
    Dado que se procesa la creación de un itinerario válido
    Cuando se abre la transacción relacional en PostgreSQL
    Entonces se inserta la fila en 'itineraries' y simultáneamente el evento en 'outbox_events' con estado 'PENDING'
    Y tras el commit, el worker de relé 'OutboxRelayWorker' publica el mensaje en RabbitMQ
    Y el estado del evento en 'outbox_events' se actualiza a 'PUBLISHED'.
  ```

---

### ÉPICA 3: Notificaciones Serverless y Observabilidad Distribuida (OPS)

#### US-06: Procesamiento Reactivo de Notificaciones Serverless (FaaS)
- **Clave:** OPS-01
- **Prioridad:** Alta (P1)
- **Story Points:** 3
- **Descripción:**
  *Como* sistema de mensajería,  
  *quiero* ejecutar una función efímera reactiva (`SendNotificationFunction`) únicamente cuando llegue un evento `ItineraryCreatedEvent`,  
  *para* simular el despacho de confirmaciones y registrar la auditoría sin requerir servidores permanentes sobredimensionados.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Recepción y procesamiento reactivo del evento
    Dado que RabbitMQ encola un mensaje 'ItineraryCreatedEvent' en 'itinerary.notifications.queue'
    Cuando la función 'SendNotificationFunction' es invocada por el consumidor
    Entonces se deserializa el payload del itinerario
    Y se almacena el registro en la tabla de auditoría 'notifications_log' con estado 'SENT'.
  ```

---

#### US-07: Trazabilidad Distribuida con OpenTelemetry, Jaeger y Logs JSON
- **Clave:** OPS-02
- **Prioridad:** Alta (P1)
- **Story Points:** 5
- **Descripción:**
  *Como* ingeniero de operaciones,  
  *quiero* visualizar el flujo completo de cada solicitud a través de trazas distribuidas en Jaeger y consultar logs estructurados en JSON con correlation IDs (`trace_id` y `span_id`),  
  *para* diagnosticar latencias y fallas en cualquiera de los microservicios.

- **Criterios de Aceptación (Gherkin):**
  ```gherkin
  Escenario: Propagación de trazas de extremo a extremo
    Dado que un usuario realiza una petición POST al API Gateway
    Cuando la petición atraviesa el Gateway, llega a Itinerary Service y consulta a Airport Service
    Entonces el contexto W3C 'traceparent' se propaga entre todas las llamadas HTTP
    Y Jaeger registra el trace completo agrupando todos los spans de los microservicios
    Y cada línea de log en stdout contiene el mismo 'trace_id' en formato JSON.
  ```
