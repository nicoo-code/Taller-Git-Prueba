# Script de Ejecución de Pruebas y Cobertura
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Ejecutando Suite de Pruebas Unitarias y de Integración" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$env:PYTHONPATH = "services/airport-service;services/itinerary-service;services/notification-service;services/api-gateway;."

python -m pytest tests/unit -v --cov=services/airport-service/src --cov=services/itinerary-service/src --cov=services/notification-service/src --cov-report=term --cov-report=xml:coverage.xml

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nTodas las pruebas pasaron exitosamente. Reporte de cobertura generado en coverage.xml." -ForegroundColor Green
} else {
    Write-Host "`nHubo fallas en las pruebas." -ForegroundColor Red
}
