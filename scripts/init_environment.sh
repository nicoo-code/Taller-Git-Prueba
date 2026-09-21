#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "Inicializando Sistema Distribuido de Itinerarios Personales"
echo "=========================================================="

if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker no está instalado o no está en el PATH."
    exit 1
fi

echo "Levantando contenedores con Docker Compose..."
docker compose up --build -d

echo "Esperando 10 segundos para inicialización de middleware..."
sleep 10

echo "Verificando estado de los servicios:"
docker compose ps

echo "=========================================================="
echo "URLs de Acceso:"
echo "  - Frontend / Web App:        http://localhost:8000"
echo "  - Airport Swagger API:       http://localhost:8001/docs"
echo "  - Itinerary Swagger API:     http://localhost:8002/docs"
echo "  - RabbitMQ Management UI:    http://localhost:15672 (guest/guest)"
echo "  - Jaeger Distributed Traces: http://localhost:16686"
echo "=========================================================="
