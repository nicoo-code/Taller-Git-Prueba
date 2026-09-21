# Pull Request: Sistema Distribuido de Itinerarios Personales

## 1. Descripción del Cambio
<!-- Proporciona un resumen claro y conciso de los cambios introducidos en esta PR -->

## 2. Ticket de Jira Asociado
- **Ticket ID:** `[AIRP-XX / ITIN-XX / OPS-XX]`
- **Enlace:** [Link a Jira]

## 3. Tipo de Cambio
- [ ] `feat`: Nueva funcionalidad
- [ ] `fix`: Corrección de bug
- [ ] `refactor`: Refactorización de código
- [ ] `test`: Adición o mejora de pruebas
- [ ] `docs`: Modificación de documentación técnica o arquitectura
- [ ] `ci`: Cambios en pipeline CI/CD o scripts

## 4. Arquitectura y Componentes Afectados
- [ ] `services/airport-service` (Hexagonal, Adapter API Colombia, Circuit Breaker, Redis)
- [ ] `services/itinerary-service` (CRUD, Transactional Outbox, Validación HTTP, Alembic)
- [ ] `services/notification-service` (Serverless / FaaS Consumer RabbitMQ)
- [ ] `services/api-gateway` (Ruteo, Rate Limiting, JWT)
- [ ] `frontend` (Plotly JS Map)
- [ ] `docs/` (SAD, ADRs, Diagramas)

## 5. Checklist de Calidad Técnica
- [ ] Cumple con la Arquitectura Hexagonal y separación de capas (Dominio, Aplicación, Infraestructura).
- [ ] No acopla directamente el frontend a proveedores externos.
- [ ] Pruebas unitarias implementadas con cobertura $\ge 80\%$.
- [ ] Linters (`ruff`, `black`) ejecutados sin advertencias ni errores.
- [ ] Análisis de SonarQube verificado (Quality Gate en estado verde).
- [ ] Documentación OpenAPI/Swagger verificada en `/docs`.
- [ ] Se validaron los diagramas Mermaid si hubo cambios en la arquitectura.
- [ ] Se probó el levantamiento local mediante `docker-compose up --build`.
