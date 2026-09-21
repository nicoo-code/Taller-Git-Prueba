#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "Ejecutando Suite de Pruebas Unitarias y de Integración"
echo "=========================================================="

export PYTHONPATH="services/airport-service:services/itinerary-service:services/notification-service:services/api-gateway:."

python3 -m pytest tests/unit -v --cov=services/airport-service/src --cov=services/itinerary-service/src --cov=services/notification-service/src --cov-report=term --cov-report=xml:coverage.xml

echo "Pruebas completadas. Cobertura generada en coverage.xml."
