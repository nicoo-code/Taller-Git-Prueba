# Sistema de itinerarios personales

## Contexto del Proyecto

Se desea desarrollar un sistema de planificación de viajes que permita:

1. Consultar aeropuertos colombianos a través de la API pública API Colombia.
2. Mostrar la ubicación de los aeropuertos en un mapa interactivo usando Plotly JS.
3. Permitir que un usuario cree y gestione itinerarios de viaje.
4. Validar que los aeropuertos utilizados en un itinerario existan realmente.
5. Notificar la creación de itinerarios de forma asíncrona (event-driven).
6. Soportar la concurrencia, resiliencia y observabilidad típicas de un sistema distribuido real.

El sistema deberá estar desacoplado de la API externa mediante la aplicación del patrón Adapter.

---

### 1. Servicio de Aeropuertos (Airport Service) - ARQUITECTURA DE MICROSERVICIOS

**Responsable de:**
* Consumir la API pública API Colombia.
* Adaptar la respuesta externa a un modelo de dominio interno.
* Transformar los datos al formato requerido por Plotly.
* Exponer un endpoint REST para obtener información de aeropuertos por ID.
* Implementar tolerancia a fallos frente a problemas externos (circuit breaker, reintentos con espera exponencial, tiempo límite de espera) y memoria caché local en Redis.
* Cachear respuestas de la API externa en Redis para reducir llamadas repetidas.

Aquí debe implementarse formalmente el patrón Adapter, donde:
* La API externa actúa como Adapter.
* Se define una interfaz interna (Puerto).
* El Adapter traduce la estructura externa al modelo de dominio.
* El frontend solo conoce el formato adaptado.

El frontend debe mostrar al menos un aeropuerto en un mapa utilizando Plotly JS.

---

### 2. Servicio de Itinerarios (Itinerary Service) - ARQUITECTURA DE MICROSERVICIOS + BASADA EN EVENTOS

**Responsable de:**
* Persistir la información en base de datos (SQLite, PostgreSQL o MySQL).
* Gestionar errores adecuadamente.
* Implementar la gestión completa (crear, leer, actualizar, eliminar) de itinerarios guardados en su propia base de datos relacional (una base de datos por servicio).
* Validar la existencia de aeropuertos consultando de forma directa al Servicio de Aeropuertos (Nivel 1) o mediante copia local optimizada (Nivel 2/3).
* Garantizar el desacoplamiento mediante la publicación de un Evento de Integración en el gestor de mensajes aplicando el patrón de Buzón de Salida Transaccional (Transactional Outbox) para evitar la inconsistencia de datos por escritura doble.

Cada itinerario debe contener como mínimo:
* Nombre del usuario
* Aeropuerto de salida (ID)
* Aeropuerto de llegada (ID)
* Fecha de viaje
* Duración del viaje en minutos

Antes de guardar un itinerario, el sistema debe verificar que los aeropuertos existan, realizando una llamada HTTP al Airport Service.

---

### 3. Componente de Notificaciones y Procesamiento - SERVERLESS

En lugar de un servicio tradicional encendido de forma permanente, el procesamiento de notificaciones y analítica se ejecutará bajo el paradigma de Funciones como Servicio (Function-as-a-Service / FaaS) dentro del modelo sin servidor (Serverless).

**Responsable de:**
* **Función sin Servidor 1 (`SendNotificationFunction`):** Se activa de forma automática únicamente cuando el gestor de mensajes recibe el evento `ItineraryCreatedEvent`. Procesa la alerta, simula el envío de correo/registro y guarda el historial en su propia base de datos.
* **Función sin Servidor 2 opcional (`GenerateItineraryReportFunction`):** Función ejecutada bajo demanda para consolidar métricas de itinerarios sin sobrecargar los servicios principales.
* Se desplegará localmente usando herramientas de simulación de nube (LocalStack para AWS Lambda, Knative o OpenFaaS) dentro de la orquestación de contenedores.

---

### Infraestructura Compartida

#### API Gateway / BFF
* Punto único de entrada del sistema (Traefik, nginx o implementación en Python).
* Ruteo hacia los microservicios internos.
* Rate limiting básico.
* No debe contener lógica de negocio.
* Propaga el token JWT del usuario hacia los servicios internos (seguridad S2S).

#### Broker de Mensajería
* RabbitMQ o Kafka para la comunicación asíncrona entre Itinerary Service y Notification Service.
* Cola o tópico dedicado a eventos de itinerarios.
* Su contrato debe documentarse con AsyncAPI.

#### Cache (opcional)
* Redis en el Airport Service para cachear las respuestas de la API externa y reducir llamadas repetidas.

#### Observabilidad (opcional)
* OpenTelemetry + Jaeger para trazabilidad distribuida entre microservicios.
* Logs estructurados en JSON con correlation ID (`trace_id` / `span_id`).
* Prometheus + Grafana para métricas y alertas de los servicios.

---

## Requisitos Técnicos Obligatorios

El proyecto deberá cumplir como mínimo con los siguientes requisitos:
* Uso de microservicios en el lenguaje de su elección (se recomienda Python).
* Implementación real del patrón Adapter.
* Separación por capas (dominio, infraestructura, API — Arquitectura Hexagonal).
* Definición explícita de Contextos Delimitados y Lenguaje Ubicuo (DDD).
* Comunicación HTTP entre microservicios.
* Comunicación asíncrona mediante broker de mensajería.
* Base de datos relacional (una por servicio).
* Migraciones de base de datos versionadas (Alembic, Flyway o Liquibase) en cada servicio.
* Uso de modelos Pydantic (caso Python o su equivalente en el lenguaje seleccionado).
* Manejo adecuado de errores HTTP.
* Documentación automática Swagger funcional en cada microservicio.
* Frontend básico que consuma el Airport Service y muestre el mapa.
* Uso de Docker y docker-compose para orquestar el sistema completo.

### Requisitos Arquitectónicos
Se evaluará especialmente:
* Correcta separación de responsabilidades.
* Uso de tecnologías recomendadas en el marco DevOps.
* Uso de interfaces o clases abstractas para definir contratos.
* No acoplar directamente el frontend a la API externa.
* No mezclar lógica de negocio con lógica de infraestructura.
* Organización clara del proyecto.
* Uso de Docker.

---

## Integración de las 3 Arquitecturas

| Arquitectura | Dónde se aplica | Cómo se demuestra en la práctica |
| :--- | :--- | :--- |
| **1. Microservicios** | Servicio de Aeropuertos y Servicio de Itinerarios | Servicios independientes, con bases de datos aisladas, desplegados por separado y comunicados vía HTTP/gRPC. |
| **2. Basada en Eventos** | Servicio de Itinerarios $\rightarrow$ Gestor de Mensajes | Publicación asíncrona del evento de creación mediante el patrón de Buzón de Salida Transaccional y contratos AsyncAPI. |
| **3. Sin Servidor (Serverless)** | Procesamiento de Notificaciones y Reportes | Funciones efímeras que se ejecutan únicamente al recibir eventos del gestor de mensajes, sin mantener servidores encendidos todo el tiempo. |

---

## Rúbrica de Evaluación

El reto se califica por niveles acumulativos. Para obtener la nota máxima se deben completar los tres niveles.

### Nivel 1 — Base (obligatorio)

| Criterio | Descripción |
| :--- | :--- |
| **Patrón Adapter** | Implementación formal con Puerto/Adapter y traducción al modelo de dominio. |
| **Arquitectura Hexagonal** | Separación clara en dominio, infraestructura y API en cada servicio. |
| **DDD básico** | Contextos delimitados y lenguaje ubicuo documentados en el README. |
| **CRUD de itinerarios** | CRUD completo con validación de aeropuertos vía HTTP. |
| **Base de datos relacional** | Persistencia funcional (al menos Itinerary Service). |
| **Migraciones de BD** | Migraciones versionadas (Alembic/Flyway) dentro de cada servicio. |
| **Swagger** | Documentación automática funcional en cada servicio. |
| **Manejo de errores** | Códigos HTTP correctos y respuestas consistentes. |
| **Logs estructurados** | Logs JSON con correlation ID (`trace_id`/`span_id`) en todos los servicios. |
| **Frontend con Plotly** | Mapa interactivo consumiendo el Airport Service. |
| **Docker + docker-compose** | Sistema completo orquestado (servicios + base de datos + frontend). |
| **README y diagramas** | Arquitectura, componentes, clases, relacional, patrón Adapter, contextos delimitados. |

### Nivel 2 — Avanzado

| Criterio | Descripción |
| :--- | :--- |
| **Circuit Breaker** | Resiliencia ante fallas de la API externa (timeout, fallback). |
| **Retry con Backoff** | Reintentos con exponential backoff y jitter. |
| **Cache Redis** | Cache funcional en el Airport Service con invalidación. |
| **API Gateway** | Punto único de entrada con ruteo, rate limiting y propagación de JWT. |
| **Notification Service** | Tercer microservicio consumiendo eventos del broker. |
| **Broker de mensajería** | RabbitMQ o Kafka funcionando con eventos de itinerarios. |
| **AsyncAPI** | Documentación YAML/JSON del contrato asíncrono (eventos, tópicos/colas, protocolos). |
| **Trazas distribuidas** | OpenTelemetry + Jaeger mostrando un request completo entre servicios. |
| **Propagación de JWT** | Protección de endpoints y propagación del token a servicios internos. |
| **Pruebas E2E** | Suite E2E con Testcontainers que verifica el flujo completo y lo destruye. |
| **Demostración de resiliencia** | Evidencia de falla controlada: tumbar la API externa y mostrar circuit breaker en acción. |

### Nivel 3 — Experto (bonus)

| Criterio | Descripción |
| :--- | :--- |
| **Transactional Outbox** | Tabla outbox en la misma transacción + worker/CDC para publicación garantizada de eventos. |
| **Consistencia distribuida** | Resolución explícita del Double Write Problem documentada en el README. |
| **gRPC** | Comunicación interna Itinerary $\leftrightarrow$ Airport mediante gRPC/Protobuf. |
| **Seguridad S2S** | mTLS con Service Mesh (Istio/Linkerd) u OAuth2 Client Credentials. |
| **Vault / Config Server** | Secretos y configuración obtenidos dinámicamente al arrancar. |
| **Chaos Engineering** | Inyección de fallos (Chaos Mesh o Toxiproxy): latencia, caída de paquetes, CPU al 100%. |
| **Bulkhead** | Aislamiento de hilos/conexiones para llamadas externas vs. BD local. |
| **Alerting** | Alertas de Prometheus (circuit breaker abierto, dead letters en RabbitMQ, etc.). |
| **CI/CD** | Pipeline en GitHub Actions (build, test, push, deploy). |
| **Kubernetes** | Despliegue con deployments, services y probes de readiness/liveness. |
| **Contract Testing** | Pruebas de contrato (Pact) entre consumidores y el Airport Service. |
| **API versioning** | Versionado y paginación en endpoints expuestos. |

---

## Entregables

Los estudiantes deberán entregar:

1. Código fuente completo en repositorio Git.
2. Archivo **README** explicando:
   * Arquitectura utilizada
   * Diagrama de componentes
   * Diagrama de clases
   * Diagrama relacional
   * Diagrama de secuencia (frontend $\rightarrow$ gateway $\rightarrow$ itinerary $\rightarrow$ airport)
   * Diagrama de despliegue (docker-compose / Kubernetes)
   * Contextos Delimitados y Lenguaje Ubicuo (DDD)
   * Decisión sobre el Agregado Aeropuerto (referencia de valor vs. agregado completo)
   * Diferencia entre eventos de dominio e integración
   * Explicación del patrón Adapter implementado
   * Explicación del flujo asíncrono de notificaciones
   * Explicación de cómo se resolvió el Double Write Problem (si aplica Nivel 3)
   * Instrucciones para ejecutar el proyecto
3. Evidencia de funcionamiento (capturas o video corto), incluyendo:
   * Mapa Plotly con aeropuertos.
   * Creación de un itinerario y notificación generada.
   * Captura de una traza distribuida en Jaeger (si aplica Nivel 2).
   * Demostración de falla controlada con circuit breaker (si aplica Nivel 2).
   * Captura de alertas de Prometheus y/o resultados de chaos engineering (si aplica Nivel 3).
4. Base de datos funcional.
5. Diagrama simple de arquitectura.
6. Tabla de autoevaluación indicando qué niveles cumplió y por qué.