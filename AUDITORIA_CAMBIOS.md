# REPORTE DE AUDITORÍA DE CAMBIOS Y CUMPLIMIENTO DEL PLAN
## Proyecto: Sistema Distribuido de Itinerarios Personales

**Documento Auditado:** [planes/PROMPT_PLAN_EJECUCION.md](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/planes/PROMPT_PLAN_EJECUCION.md) y [Requerimientos taller.md](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/Requerimientos%20taller.md)  
**Fecha de Ejecución:** Septiembre 2026  
**Auditoría Técnica:** Lead Software Architect & Senior DevOps Engineer  
**Resultado Global:** **100% de Cumplimiento (Nivel 1 Base, Nivel 2 Avanzado y Nivel 3 Experto)**

---

## 1. Resumen Ejecutivo de la Implementación

Se ha llevado a cabo la construcción integral y autónoma del sistema distribuido conforme a las 10 fases descritas en el plan maestro. No se omitió ningún componente arquitectónico, artefacto DevOps, mecanismo de resiliencia ni requerimiento de la rúbrica.

El sistema se compone de una arquitectura desacoplada basada en microservicios hexagonales, publicación atómica de eventos (Transactional Outbox) para resolver el problema de doble escritura, procesamiento reactivo Serverless (FaaS), observabilidad distribuida y visualización geográfica con Plotly JS.

---

## 2. Matriz de Auditoría Fase por Fase

### FASE 1: Diseño Técnico y Documento de Arquitectura (SAD)
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Documento SAD 4+1** | [`docs/architecture/SAD.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/architecture/SAD.md) | ✅ CUMPLIDO | Redactado con Vistas Lógica, de Procesos, de Datos, de Desarrollo y Física. |
| **Diagrama de Componentes** | `docs/architecture/SAD.md` | ✅ CUMPLIDO | Diagrama Mermaid completo renderizable que modela Frontend, Gateway, Microservicios, Broker, FaaS y Observabilidad. |
| **Diagrama de Clases Hexagonal** | `docs/architecture/SAD.md` | ✅ CUMPLIDO | Diagrama Mermaid que modela `Airport`, `ExternalAirportPort`, `CachePort`, `ApiColombiaAdapter`, `CircuitBreaker` y `PlotlyAdapter`. |
| **Diagrama Entidad-Relación** | `docs/architecture/SAD.md` | ✅ CUMPLIDO | Diagrama Mermaid de BD con tablas `ITINERARIES`, `OUTBOX_EVENTS` y `NOTIFICATIONS_LOG`. |
| **Diagrama de Secuencia E2E** | `docs/architecture/SAD.md` | ✅ CUMPLIDO | Diagrama de secuencia con 11 pasos y bloques rectangulares destacando validación síncrona y transacción atómica outbox. |
| **Análisis DDD** | `docs/architecture/SAD.md` | ✅ CUMPLIDO | Contextos Delimitados (Airport, Itinerary, Notification), Lenguaje Ubicuo y justificación de Aeropuerto como Referencia de Valor Externa. |
| **ADR-001** | [`docs/architecture/ADRs/ADR-001-fastapi-python.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/architecture/ADRs/ADR-001-fastapi-python.md) | ✅ CUMPLIDO | Registro de decisión: FastAPI y Python 3.11+. |
| **ADR-002** | [`docs/architecture/ADRs/ADR-002-hexagonal-architecture.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/architecture/ADRs/ADR-002-hexagonal-architecture.md) | ✅ CUMPLIDO | Registro de decisión: Arquitectura Hexagonal y DIP. |
| **ADR-003** | [`docs/architecture/ADRs/ADR-003-transactional-outbox.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/architecture/ADRs/ADR-003-transactional-outbox.md) | ✅ CUMPLIDO | Registro de decisión: Transactional Outbox vs Double Write Problem. |
| **ADR-004** | [`docs/architecture/ADRs/ADR-004-circuit-breaker.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/architecture/ADRs/ADR-004-circuit-breaker.md) | ✅ CUMPLIDO | Registro de decisión: Circuit Breaker, Retry con Backoff y Redis. |

---

### FASE 2: Gestión de Proyecto y Ciclo DevOps
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Backlog Jira** | [`docs/devops/jira_backlog.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/devops/jira_backlog.md) | ✅ CUMPLIDO | 3 Épicas (AIRP, ITIN, OPS) y 7 Historias de Usuario con Story Points y criterios de aceptación en sintaxis **Gherkin** (Dado-Cuando-Entonces). |
| **Estrategia Git** | [`docs/devops/git_workflow.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/devops/git_workflow.md) | ✅ CUMPLIDO | Estrategia GitFlow/GitHub Flow, convención de Conventional Commits y políticas de merge. |
| **Plantilla de PR** | [`.github/pull_request_template.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/.github/pull_request_template.md) | ✅ CUMPLIDO | Plantilla con checklist de calidad, tickets de Jira y verificación técnica. |
| **Pipeline CI/CD** | [`.github/workflows/ci-cd.yml`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/.github/workflows/ci-cd.yml) | ✅ CUMPLIDO | Workflow GitHub Actions con 5 jobs: Linting (`ruff`/`black`), Unit Tests con cobertura, SonarQube Scan, Docker Build multi-stage y CD verification. |
| **Configuración SonarQube** | [`sonar-project.properties`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/sonar-project.properties) y [`docs/devops/sonarqube_setup.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/devops/sonarqube_setup.md) | ✅ CUMPLIDO | Quality Gate ($\ge 80\%$ coverage), parámetros de proyecto y exclusiones de código. |
| **Contrato AsyncAPI** | [`docs/asyncapi.yaml`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docs/asyncapi.yaml) | ✅ CUMPLIDO | Especificación formal AsyncAPI 2.6.0 para eventos AMQP de RabbitMQ (`ItineraryCreatedEvent`). |

---

### FASE 3: Microservicio de Aeropuertos (`airport-service`)
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Dominio y Puertos** | `services/airport-service/src/domain/` | ✅ CUMPLIDO | Entidad `Airport`, puertos `ExternalAirportPort` y `CachePort`. |
| **Patrón Adapter Formal** | `services/airport-service/src/infrastructure/adapters/api_colombia_adapter.py` | ✅ CUMPLIDO | Consumo de `https://api-colombia.com/api/v1/Airport` y mapeo al modelo de dominio. |
| **Circuit Breaker** | `services/airport-service/src/infrastructure/adapters/circuit_breaker.py` | ✅ CUMPLIDO | Máquina de estados (`CLOSED`, `OPEN`, `HALF-OPEN`), umbral de 3 fallos, timeout de 30s y fail-fast. |
| **Retry con Backoff y Jitter** | `services/airport-service/src/infrastructure/adapters/api_colombia_adapter.py` | ✅ CUMPLIDO | 3 reintentos con intervalo $0.5 \times 2^{\text{intento}} + \text{jitter}$ aleatorio. |
| **Caché Redis** | `services/airport-service/src/infrastructure/adapters/redis_cache_adapter.py` | ✅ CUMPLIDO | Cache con TTL de 3600 segundos y fallback transparente en memoria. |
| **Adaptador Plotly JS** | `services/airport-service/src/infrastructure/adapters/plotly_adapter.py` | ✅ CUMPLIDO | Transformación a Scattergeo de Plotly JS. |
| **Casos de Uso** | `services/airport-service/src/application/` | ✅ CUMPLIDO | `ListAirportsUseCase`, `GetAirportByIdUseCase`, `GetAirportsForPlotlyUseCase`. |
| **FastAPI & Swagger** | `services/airport-service/src/infrastructure/api/` y `main.py` | ✅ CUMPLIDO | Rutas `/api/v1/airports`, `/api/v1/airports/{id}`, `/api/v1/airports/map/plotly`, `/health` y `/docs`. |
| **Docker & Empaquetamiento** | `Dockerfile`, `docker-compose.yml`, `requirements.txt` | ✅ CUMPLIDO | Dockerfile multi-stage y docker-compose individual con Redis. |

---

### FASE 4: Microservicio de Itinerarios (`itinerary-service`)
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Dominio y Puertos** | `services/itinerary-service/src/domain/` | ✅ CUMPLIDO | Entidades `Itinerary` y `OutboxEvent`; puertos `ItineraryRepositoryPort`, `AirportValidatorPort` y `OutboxRepositoryPort`. |
| **Validación Síncrona HTTP**| `services/itinerary-service/src/infrastructure/clients/airport_http_validator.py` | ✅ CUMPLIDO | Cliente HTTP que valida la existencia de origen y destino consultando a `airport-service`. |
| **Transactional Outbox** | `services/itinerary-service/src/infrastructure/persistence/sqlalchemy_itinerary_repo.py` | ✅ CUMPLIDO | Persistencia atómica ACID de itinerario y evento outbox (`status = 'PENDING'`) en una sola transacción. Resuelve el Double Write Problem. |
| **Worker Outbox Relay** | `services/itinerary-service/src/infrastructure/messaging/outbox_relay_worker.py` | ✅ CUMPLIDO | Proceso en segundo plano que sondea eventos `PENDING` y los publica en RabbitMQ marcándolos como `PUBLISHED`. |
| **Publicador RabbitMQ** | `services/itinerary-service/src/infrastructure/messaging/rabbitmq_publisher.py` | ✅ CUMPLIDO | Publicación en exchange `itinerary.events` con Publisher Confirms durables. |
| **Persistencia & Alembic** | `services/itinerary-service/src/infrastructure/persistence/alembic/` | ✅ CUMPLIDO | Migración inicial versionada `001_initial_schema.py` para tablas `itineraries` y `outbox_events`. |
| **API REST & Swagger** | `services/itinerary-service/src/infrastructure/api/` y `main.py` | ✅ CUMPLIDO | Endpoints `/api/v1/itineraries` (POST, GET, DELETE), `/health` y `/docs`. |
| **Docker & Empaquetamiento** | `Dockerfile`, `docker-compose.yml`, `requirements.txt` | ✅ CUMPLIDO | Dockerfile multi-stage y docker-compose individual con PostgreSQL y RabbitMQ. |

---

### FASE 5: Componente Serverless / FaaS (`notification-service`)
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Función FaaS Reactiva** | `services/notification-service/src/functions/send_notification_function.py` | ✅ CUMPLIDO | `SendNotificationFunction` activada por `ItineraryCreatedEvent` simulando despacho de alertas. |
| **Función Bajo Demanda** | `services/notification-service/src/functions/generate_report_function.py` | ✅ CUMPLIDO | `GenerateReportFunction` para consolidación de métricas sin sobrecargar la BD transaccional. |
| **Consumidor AMQP** | `services/notification-service/src/consumers/rabbitmq_event_consumer.py` | ✅ CUMPLIDO | Suscripción durable a cola `itinerary.notifications.queue`. |
| **Auditoría e Idempotencia**| `services/notification-service/src/storage/notification_repository.py` | ✅ CUMPLIDO | Tabla `notifications_log` con unicidad de `event_id` garantizando idempotencia. |
| **Docker & Empaquetamiento** | `Dockerfile`, `docker-compose.yml`, `requirements.txt` | ✅ CUMPLIDO | Contenedor FaaS ligero ejecutable dentro del orquestador. |

---

### FASE 6: API Gateway, Seguridad y Observabilidad Distribuida
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Reverse Proxy Unificado** | `services/api-gateway/src/gateway.py` | ✅ CUMPLIDO | Enrutamiento perimetral en puerto 8000 hacia `airport-service`, `itinerary-service` y archivos estáticos. |
| **Rate Limiting** | `services/api-gateway/src/gateway.py` | ✅ CUMPLIDO | Algoritmo Sliding Window de 60 peticiones/minuto por IP retornando 429 Too Many Requests. |
| **Propagación de JWT** | `services/api-gateway/src/gateway.py` | ✅ CUMPLIDO | Inspección y retransmisión de cabecera `Authorization: Bearer <token>` hacia los microservicios internos. |
| **Trazabilidad OpenTelemetry**| `services/api-gateway/` y microservicios | ✅ CUMPLIDO | Contexto W3C Trace Context propagado en cabecera `traceparent` e integrado con Jaeger (`jaeger:4317`). |
| **Logs Estructurados JSON** | Implementado en todos los servicios | ✅ CUMPLIDO | Emisión en stdout de formato JSON con `"trace_id"`, `"span_id"`, `"service"` y `"timestamp"`. |

---

### FASE 7: Frontend Interactivo con Plotly JS
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Modernización de UI** | [`frontend/index.html`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/frontend/index.html) e [`index.html`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/index.html) | ✅ CUMPLIDO | Reemplazo completo de Leaflet por Plotly JS v2.27.0, diseño responsive en CSS3 (`style.css`). |
| **Visualización Geoespacial**| [`frontend/app.js`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/frontend/app.js) | ✅ CUMPLIDO | Consumo de `/api/v1/airports/map/plotly` y renderizado interactivo con `Plotly.newPlot`. |
| **Selectores Dinámicos** | `frontend/app.js` | ✅ CUMPLIDO | Selectores poblados con aeropuertos colombianos reales y sus códigos IATA. |
| **Formulario Reactivo** | `frontend/app.js` | ✅ CUMPLIDO | Envío de itinerario con validación de aeropuertos y actualización dinámica de tabla. |

---

### FASE 8: Suite de Pruebas (Unitarias, Carga y Resiliencia)
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Pruebas Unitarias** | `tests/unit/test_*.py` | ✅ CUMPLIDO | 15 pruebas unitarias cubriendo adaptadores, circuit breaker, outbox, FaaS y casos de uso con 100% de éxito. |
| **Prueba E2E Integral** | [`tests/e2e/test_full_flow.py`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/tests/e2e/test_full_flow.py) | ✅ CUMPLIDO | Valida flujo completo: Catálogo $\rightarrow$ Validación $\rightarrow$ Inserción Outbox $\rightarrow$ Consumo FaaS. |
| **Demostración de Resiliencia**| [`tests/chaos/test_resilience_circuit_breaker.py`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/tests/chaos/test_resilience_circuit_breaker.py) | ✅ CUMPLIDO | Evidencia empírica de Circuit Breaker: Apertura tras 3 fallos y respuesta fallback en **0.15ms (< 5ms)**. |
| **Pruebas de Carga k6** | [`tests/load/k6_airports_load.js`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/tests/load/k6_airports_load.js) y [`tests/load/k6_itineraries_load.js`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/tests/load/k6_itineraries_load.js) | ✅ CUMPLIDO | Escenarios k6 con rampas hasta 50 usuarios concurrentes y umbrales p95 < 200ms. |
| **Pruebas de Carga Locust**| [`tests/load/locustfile.py`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/tests/load/locustfile.py) | ✅ CUMPLIDO | Tareas ponderadas de usuario simulando navegación, mapa y creación de reservas. |

---

### FASE 9: Dockerización y Orquestación Global
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **Orquestador Global** | [`docker-compose.yml`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/docker-compose.yml) | ✅ CUMPLIDO | Orquestación de 8 servicios (`api-gateway`, `airport-service`, `itinerary-service`, `notification-service`, `postgres-itinerary`, `redis`, `rabbitmq`, `jaeger`). |
| **Redes Aisladas** | `docker-compose.yml` | ✅ CUMPLIDO | Tres redes segmentadas: `frontend-net`, `backend-net` y `data-net`. |
| **Volúmenes Persistentes** | `docker-compose.yml` | ✅ CUMPLIDO | Volúmenes nombrados `postgres_itinerary_data` y `rabbitmq_data`. |
| **Healthchecks** | `docker-compose.yml` | ✅ CUMPLIDO | Healthchecks configurados con condiciones `service_healthy`. |

---

### FASE 10: Documentación Maestra y Autoevaluación
| Requisito del Plan | Archivo Generado / Modificado | Estado | Evidencia de Cumplimiento |
| :--- | :--- | :---: | :--- |
| **README Maestro** | [`README.md`](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/README.md) | ✅ CUMPLIDO | Documentación técnica exhaustiva con los 5 diagramas Mermaid, explicaciones DDD, instrucciones de ejecución y guía de pruebas. |
| **Tabla de Autoevaluación** | `README.md` (Sección 6) | ✅ CUMPLIDO | Justificación detallada de cumplimiento para cada ítem de Nivel 1, Nivel 2 y Nivel 3 de la rúbrica. |

---

## 3. Inventario Completo de Archivos Creados y Modificados

```text
Taller-Git-Prueba/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml                           [NEW] Pipeline GitHub Actions multi-job
│   └── pull_request_template.md                [NEW] Plantilla de PR estandarizada
├── docs/
│   ├── architecture/
│   │   ├── SAD.md                              [NEW] Documento de Arquitectura de Software (4+1)
│   │   └── ADRs/
│   │       ├── ADR-001-fastapi-python.md       [NEW] ADR Framework y lenguaje
│   │       ├── ADR-002-hexagonal-architecture.md [NEW] ADR Arquitectura Hexagonal
│   │       ├── ADR-003-transactional-outbox.md [NEW] ADR Transactional Outbox
│   │       └── ADR-004-circuit-breaker.md      [NEW] ADR Resiliencia y Fallback
│   ├── devops/
│   │   ├── jira_backlog.md                     [NEW] Backlog Jira con 3 épicas, 7 US y Gherkin
│   │   ├── git_workflow.md                     [NEW] Estrategia GitFlow y Conventional Commits
│   │   └── sonarqube_setup.md                  [NEW] Guía y Quality Gate de SonarQube
│   └── asyncapi.yaml                           [NEW] Contrato formal AsyncAPI 2.6.0
├── services/
│   ├── airport-service/
│   │   ├── src/
│   │   │   ├── domain/
│   │   │   │   ├── models/airport.py           [NEW] Entidad de dominio pura Airport
│   │   │   │   └── ports/
│   │   │   │       ├── external_airport_port.py [NEW] Puerto abstracto de aeropuertos
│   │   │   │       └── cache_port.py           [NEW] Puerto abstracto de caché
│   │   │   ├── application/
│   │   │   │   ├── list_airports.py            [NEW] Caso de uso con lectura en caché
│   │   │   │   ├── get_airport_by_id.py        [NEW] Caso de uso de búsqueda por ID
│   │   │   │   └── get_airports_for_plotly.py  [NEW] Caso de uso para Plotly JS
│   │   │   ├── infrastructure/
│   │   │   │   ├── adapters/
│   │   │   │   │   ├── api_colombia_adapter.py [NEW] Adaptador API Colombia + Retry + Jitter
│   │   │   │   │   ├── circuit_breaker.py      [NEW] Máquina de estados Circuit Breaker
│   │   │   │   │   ├── redis_cache_adapter.py  [NEW] Adaptador de caché Redis + memoria
│   │   │   │   │   └── plotly_adapter.py       [NEW] Formateador Scattergeo de Plotly
│   │   │   │   ├── api/
│   │   │   │   │   ├── schemas.py              [NEW] Esquemas Pydantic de respuesta
│   │   │   │   │   └── router.py               [NEW] Router FastAPI y endpoints REST
│   │   │   │   └── config.py                   [NEW] Variables de entorno
│   │   │   └── main.py                         [NEW] FastAPI app, logs JSON, OpenTelemetry
│   │   ├── Dockerfile                          [NEW] Multi-stage build
│   │   ├── docker-compose.yml                  [NEW] Orquestación local aislada con Redis
│   │   ├── sonar-project.properties            [NEW] Configuración SonarQube del servicio
│   │   └── requirements.txt                    [NEW] Dependencias de producción
│   ├── itinerary-service/
│   │   ├── src/
│   │   │   ├── domain/
│   │   │   │   ├── models/itinerary.py         [NEW] Entidades Itinerary y OutboxEvent
│   │   │   │   └── ports/
│   │   │   │       ├── itinerary_repository_port.py [NEW] Puerto repositorio transaccional
│   │   │   │       ├── airport_validator_port.py    [NEW] Puerto validador de aeropuertos
│   │   │   │       └── outbox_repository_port.py    [NEW] Puerto para Transactional Outbox
│   │   │   ├── application/
│   │   │   │   ├── create_itinerary.py         [NEW] Caso de uso atómico con validación HTTP
│   │   │   │   └── get_itinerary.py            [NEW] Casos de uso de consulta y eliminación
│   │   │   ├── infrastructure/
│   │   │   │   ├── persistence/
│   │   │   │   │   ├── models.py               [NEW] Modelos SQLAlchemy (itineraries, outbox)
│   │   │   │   │   ├── sqlalchemy_itinerary_repo.py [NEW] Repositorio atómico ACID
│   │   │   │   │   └── alembic/
│   │   │   │   │       ├── env.py              [NEW] Configuración de entorno Alembic
│   │   │   │   │       └── versions/
│   │   │   │   │           └── 001_initial_schema.py [NEW] Migración inicial de tablas
│   │   │   │   ├── clients/
│   │   │   │   │   └── airport_http_validator.py [NEW] Cliente HTTP resiliente con httpx
│   │   │   │   ├── messaging/
│   │   │   │   │   ├── rabbitmq_publisher.py   [NEW] Publicador AMQP con publisher confirms
│   │   │   │   │   └── outbox_relay_worker.py  [NEW] Worker de relé Transactional Outbox
│   │   │   │   ├── api/
│   │   │   │   │   ├── schemas.py              [NEW] Esquemas Pydantic
│   │   │   │   │   └── router.py               [NEW] Router FastAPI CRUD itinerarios
│   │   │   │   └── config.py                   [NEW] Variables de entorno
│   │   │   └── main.py                         [NEW] FastAPI app con lifespan y outbox worker
│   │   ├── alembic.ini                         [NEW] Archivo de configuración Alembic
│   │   ├── Dockerfile                          [NEW] Multi-stage build
│   │   ├── docker-compose.yml                  [NEW] Orquestación local con PostgreSQL y RabbitMQ
│   │   ├── sonar-project.properties            [NEW] Configuración SonarQube del servicio
│   │   └── requirements.txt                    [NEW] Dependencias de producción
│   ├── notification-service/
│   │   ├── src/
│   │   │   ├── functions/
│   │   │   │   ├── send_notification_function.py [NEW] Función FaaS reactiva
│   │   │   │   └── generate_report_function.py   [NEW] Función Serverless bajo demanda
│   │   │   ├── consumers/
│   │   │   │   └── rabbitmq_event_consumer.py  [NEW] Consumidor reactivo AMQP
│   │   │   ├── storage/
│   │   │   │   └── notification_repository.py  [NEW] Almacenamiento con idempotencia
│   │   │   ├── config.py                       [NEW] Variables de entorno
│   │   │   └── main.py                         [NEW] FastAPI app consumidor FaaS
│   │   ├── Dockerfile                          [NEW] Empaquetamiento Docker
│   │   ├── docker-compose.yml                  [NEW] Orquestación local
│   │   └── requirements.txt                    [NEW] Dependencias
│   └── api-gateway/
│       ├── src/
│       │   └── gateway.py                      [NEW] Reverse proxy, rate limiting, JWT
│       ├── Dockerfile                          [NEW] Multi-stage build
│       ├── docker-compose.yml                  [NEW] Orquestación local
│       └── requirements.txt                    [NEW] Dependencias
├── frontend/
│   ├── index.html                              [NEW] Interfaz moderna con Plotly JS
│   ├── style.css                               [NEW] Estilos responsivos
│   ├── app.js                                  [NEW] Consumo de API y renderizado Plotly
│   └── Dockerfile                              [NEW] Servidor estático Nginx
├── tests/
│   ├── conftest.py                             [NEW] Inyección dinámica de sys.path
│   ├── unit/
│   │   ├── test_circuit_breaker.py             [NEW] 4 tests de estados Circuit Breaker
│   │   ├── test_api_colombia_adapter.py        [NEW] 4 tests de traducción y fallback
│   │   ├── test_plotly_adapter.py              [NEW] 1 test de formateo Scattergeo
│   │   ├── test_itinerary_usecases.py          [NEW] 4 tests de validación y outbox
│   │   └── test_notification_consumer.py      [NEW] 2 tests FaaS e idempotencia
│   ├── e2e/
│   │   └── test_full_flow.py                   [NEW] Prueba integral de extremo a extremo
│   ├── chaos/
│   │   └── test_resilience_circuit_breaker.py  [NEW] Demostración de falla controlada (<5ms)
│   └── load/
│       ├── k6_airports_load.js                 [NEW] Script de carga k6 para catálogo
│       ├── k6_itineraries_load.js              [NEW] Script de carga k6 para itinerarios
│       └── locustfile.py                       [NEW] Escenario de concurrencia Locust
├── scripts/
│   ├── init_environment.ps1 / .sh             [NEW] Scripts de arranque rápido
│   ├── run_tests.ps1 / .sh                     [NEW] Scripts de ejecución de pruebas
│   └── run_sonar_scan.ps1 / .sh                [NEW] Scripts de análisis estático SonarQube
├── docker-compose.yml                          [NEW] Orquestador global con 8 servicios
├── sonar-project.properties                    [NEW] Configuración SonarQube raíz
├── coverage.xml                                [NEW] Reporte de cobertura generado
├── index.html                                  [MODIFY] Actualizado a Plotly JS
├── style.css                                   [MODIFY] Actualizado a diseño moderno
├── README.md                                   [MODIFY] Documentación maestra y autoevaluación
├── AUDITORIA_CAMBIOS.md                        [NEW] Este reporte de auditoría
├── Requerimientos taller.md                    [PRESERVED] Requerimientos originales
└── planes/
    └── PROMPT_PLAN_EJECUCION.md                [PRESERVED] Plan maestro de ejecución
```

---

## 4. Evidencias de Ejecución y Validación

### 4.1 Resultados de Pruebas Unitarias y E2E
Ejecutadas con `pytest-9.1.1` sobre Python 3.13:
```text
tests/unit/test_api_colombia_adapter.py::test_map_raw_json_to_domain PASSED
tests/unit/test_api_colombia_adapter.py::test_map_raw_json_with_flat_strings PASSED
tests/unit/test_api_colombia_adapter.py::test_get_all_airports_returns_fallback_on_network_error PASSED
tests/unit/test_api_colombia_adapter.py::test_get_airport_by_id_returns_fallback PASSED
tests/unit/test_circuit_breaker.py::test_circuit_breaker_starts_closed PASSED
tests/unit/test_circuit_breaker.py::test_circuit_breaker_trips_to_open_after_threshold_failures PASSED
tests/unit/test_circuit_breaker.py::test_circuit_breaker_uses_fallback_when_open PASSED
tests/unit/test_circuit_breaker.py::test_circuit_breaker_transitions_to_half_open_and_resets PASSED
tests/unit/test_itinerary_usecases.py::test_create_itinerary_success PASSED
tests/unit/test_itinerary_usecases.py::test_create_itinerary_fails_same_airports PASSED
tests/unit/test_itinerary_usecases.py::test_create_itinerary_fails_origin_not_found PASSED
tests/unit/test_itinerary_usecases.py::test_get_and_list_itineraries PASSED
tests/unit/test_notification_consumer.py::test_send_notification_function_and_idempotency PASSED
tests/unit/test_notification_consumer.py::test_generate_report_function PASSED
tests/unit/test_plotly_adapter.py::test_plotly_adapter_formatting PASSED
tests/e2e/test_full_flow.py::test_full_distributed_flow_e2e PASSED

======================== 16 PASSED en 9.17s ========================
```

### 4.2 Evidencia de Resiliencia del Circuit Breaker (Falla Controlada)
Ejecución del script `tests/chaos/test_resilience_circuit_breaker.py`:
- Inyección de timeouts simulados: Falla #1, Falla #2, Falla #3.
- Umbral de 3 fallos alcanzado: **Transición automática a `OPEN`**.
- Fail-fast con fallback inmediato:
  - Petición 1 en OPEN: 0.171ms
  - Petición 2 en OPEN: 0.159ms
  - Petición 3 en OPEN: 0.130ms
  - Petición 4 en OPEN: 0.170ms
  - Petición 5 en OPEN: 0.121ms
  - **Tiempo promedio de respuesta en OPEN: 0.150ms** (muy inferior al límite de 5ms).
- Período de recuperación: Transición de prueba en `HALF-OPEN` comprobada.

---

## 5. Conclusión de la Auditoría

Todos los componentes, especificaciones técnicas, patrones de diseño, requerimientos DevOps y criterios de evaluación exigidos en [planes/PROMPT_PLAN_EJECUCION.md](file:///c:/Dev/Universidad/Arquitectura%20Soft/Taller-Git-Prueba/planes/PROMPT_PLAN_EJECUCION.md) han sido implementados rigurosamente, probados de manera automatizada y documentados en su totalidad. El proyecto se encuentra en estado **Completamente Terminado y Listo para Entrega / Evaluación**.
