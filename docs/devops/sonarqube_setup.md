# Configuración y Análisis Estático de Código con SonarQube

## 1. Visión General
SonarQube se utiliza como plataforma central de inspección continua de la calidad del código, detectando bugs, vulnerabilidades de seguridad, code smells y verificando el umbral de cobertura de pruebas unitarias.

## 2. Quality Gate Definido

| Métrica | Umbral Requerido | Justificación |
| :--- | :--- | :--- |
| **Cobertura de Código (Coverage)** | $\ge 80.0\%$ | Asegura que la lógica de negocio y adaptadores estén ampliamente cubiertos. |
| **Duplicación de Código** | $< 3.0\%$ | Evita redundancias de código en los servicios. |
| **Bugs** | 0 | Cero tolerancia a defectos lógicos en ramas productivas. |
| **Vulnerabilidades (Security)** | 0 | Prevención de riesgos de inyección y secretos en código. |
| **Code Smells (Maintainability)** | Rating A (Deuda técnica $< 5\%$) | Mantenibilidad a largo plazo y limpieza en capas hexagonales. |

---

## 3. Configuración del Proyecto (`sonar-project.properties`)

El archivo raíz `sonar-project.properties` define:
- Parámetros del proyecto: `sonar.projectKey=sistema-itinerarios-personales`.
- Fuentes analizadas: `services/`.
- Rutas de pruebas: `tests/`.
- Reporte de cobertura: `coverage.xml` (generado por `pytest-cov`).
- Exclusiones de código generado o migraciones: `**/alembic/**`, `**/venv/**`, `**/tests/**`.

---

## 4. Ejecución Local del Análisis

### Prerrequisitos:
- Docker instalado o SonarScanner local.
- Servidor SonarQube corriendo en `http://localhost:9000` (opcionalmente mediante Docker):
  ```bash
  docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
  ```

### Pasos de Ejecución:
1. Generar el reporte de cobertura de pruebas:
   ```bash
   pytest --cov=services --cov-report=xml:coverage.xml
   ```
2. Ejecutar el análisis con SonarScanner:
   ```bash
   sonar-scanner \
     -Dsonar.host.url=http://localhost:9000 \
     -Dsonar.token=<SONAR_TOKEN>
   ```
O ejecutar el script automatizado provisto en `scripts/run_sonar_scan.ps1` o `scripts/run_sonar_scan.sh`.
