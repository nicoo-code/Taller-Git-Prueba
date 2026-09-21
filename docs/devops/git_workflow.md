# Estrategia de Ramas Git, Convenciones y Flujo DevOps

## 1. Estrategia de Ramificación (GitFlow / GitHub Flow)

El proyecto utiliza un modelo de ramas estructurado para garantizar la estabilidad del código en producción y facilitar el desarrollo concurrente:

```text
main (producción / tags semánticos v1.0.0)
  │
  └── develop (integración continua / staging)
        ├── feature/AIRP-01-api-colombia-adapter
        ├── feature/AIRP-02-circuit-breaker-redis
        ├── feature/ITIN-01-itinerary-crud-validation
        ├── feature/ITIN-02-transactional-outbox
        ├── feature/OPS-01-serverless-notifications
        └── fix/ITIN-03-validation-timeout-handling
```

### Ramas Principales:
- `main`: Código probado y estable en producción. Protegida contra pushes directos. Solo recibe merges mediante Pull Request aprobados desde `develop` o `hotfix/*`.
- `develop`: Rama de integración donde convergen las nuevas características validadas antes de la liberación.

### Ramas de Trabajo:
- `feature/<TICKET-JIRA>-<descripcion>`: Desarrollos nuevos. Ejemplo: `feature/AIRP-01-api-colombia-adapter`.
- `fix/<TICKET-JIRA>-<descripcion>`: Corrección de defectos en develop.
- `hotfix/<TICKET-JIRA>-<descripcion>`: Correcciones críticas directas sobre `main`.

---

## 2. Convención de Commits (Conventional Commits v1.0.0)

Todos los mensajes de commit deben seguir la estructura estándar:
```text
<tipo>(<alcance>): <descripción corta en imperativo>

[cuerpo opcional detallando el motivo del cambio]

[referencia al ticket de Jira o issues cerrados]
```

### Tipos Permitidos:
- `feat`: Nueva característica o funcionalidad.
- `fix`: Corrección de un defecto o bug.
- `docs`: Modificación o creación de documentación.
- `test`: Adición o refactorización de pruebas unitarias o de carga.
- `refactor`: Cambios en código que no corrigen bugs ni agregan funcionalidades.
- `ci`: Modificaciones en pipelines de CI/CD o herramientas de automatización.
- `chore`: Tareas auxiliares, dependencias o configuración de compilación.

### Ejemplos Válidos del Proyecto:
```bash
feat(airport): implement api colombia adapter with circuit breaker and redis cache
fix(itinerary): resolve double write problem using transactional outbox pattern
test(load): add k6 stress test suite for airport catalog queries
docs(sad): document 4+1 architecture model and ubiquitous language
ci(github): add multi-job pipeline with ruff, pytest, and docker build
```

---

## 3. Políticas de Pull Request (PR) y Quality Gates

Antes de fusionar cualquier cambio a `develop` o `main`, el Pull Request debe cumplir:
1. **Plantilla Diligenciada:** Se debe completar `.github/pull_request_template.md`.
2. **Revisión de Pares (Code Review):** Al menos 1 aprobación de un revisor técnico.
3. **Pipeline de CI Aprobado:**
   - Linter (`ruff`, `black`) sin violaciones de estilo.
   - 100% de las pruebas unitarias pasando exitosamente.
   - Cobertura de código superior al **80%**.
   - Quality Gate de **SonarQube** en verde (cero vulnerabilidades críticas, deuda técnica < 5%).
4. **Validación de Swagger y Contratos:** Endpoints verificados y esquemas Pydantic consistentes.
