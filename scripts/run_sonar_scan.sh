#!/usr/bin/env bash
set -e

SONAR_HOST="${1:-http://localhost:9000}"

echo "=========================================================="
echo "Ejecutando Análisis Estático con SonarQube"
echo "=========================================================="

if [ ! -f "coverage.xml" ]; then
    echo "Generando coverage.xml..."
    bash scripts/run_tests.sh
fi

if command -v sonar-scanner &> /dev/null; then
    sonar-scanner -Dsonar.host.url="$SONAR_HOST"
else
    echo "sonar-scanner CLI no encontrado. Ejecutando mediante contenedor Docker..."
    docker run --rm \
      --network host \
      -v "$(pwd):/usr/src" \
      sonarsource/sonar-scanner-cli \
      -Dsonar.host.url="$SONAR_HOST"
fi
