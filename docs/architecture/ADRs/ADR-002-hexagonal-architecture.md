# ADR-002: Adopción de Arquitectura Hexagonal (Ports and Adapters)

## Estado
Aceptado

## Contexto
El sistema debe desacoplarse fuertemente de servicios externos (API Colombia), mecanismos de persistencia (PostgreSQL/SQLite) y proveedores de infraestructura (Redis, RabbitMQ). Es un requisito arquitectónico que las reglas de negocio e invariantes de dominio no queden contaminadas con detalles técnicos ni con bibliotecas de terceros.

## Decisión
Se estructura cada microservicio siguiendo la **Arquitectura Hexagonal (Puertos y Adaptadores)**:
1. **Capa de Dominio (`domain`):** Contiene entidades puras, objetos de valor y puertos (interfaces abstractas que declaran operaciones requeridas sin conocer la implementación).
2. **Capa de Aplicación (`application`):** Contiene casos de uso que orquestan las operaciones del negocio dependiendo únicamente de las abstracciones de los puertos.
3. **Capa de Infraestructura (`infrastructure`):** Contiene adaptadores primarios (controladores REST de FastAPI) y adaptadores secundarios (clientes HTTP, repositorios SQLAlchemy, cache Redis, mensajería RabbitMQ).

## Consecuencias
### Positivas:
- **Testabilidad total:** La lógica de negocio y los casos de uso pueden probarse unitariamente sustituyendo los adaptadores reales por fakes o mocks en memoria sin levantar infraestructura externa.
- **Intercambiabilidad:** Cambiar la base de datos o el proveedor externo no afecta las reglas de negocio.
- Cumplimiento riguroso del Principio de Inversión de Dependencias (DIP).

### Negativas / Mitigaciones:
- Mayor número de clases y capas de indirección (se mitiga con una estructura de directorios uniforme y estandarizada entre todos los microservicios).
