# Script de Inicialización Rápida del Entorno Local
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Inicializando Sistema Distribuido de Itinerarios Personales" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verificar Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker no está instalado o no está en el PATH." -ForegroundColor Red
    exit 1
}

# 2. Levantar todos los servicios con docker compose
Write-Host "`nLevantando contenedores con Docker Compose..." -ForegroundColor Yellow
docker compose up --build -d

# 3. Esperar a que los servicios estén listos
Write-Host "`nEsperando 10 segundos para inicialización de middleware..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# 4. Mostrar estado de salud
Write-Host "`nVerificando estado de los servicios:" -ForegroundColor Green
docker compose ps

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "URLs de Acceso:" -ForegroundColor Green
Write-Host "  - Frontend / Web App:        http://localhost:8000" -ForegroundColor White
Write-Host "  - Airport Swagger API:       http://localhost:8001/docs" -ForegroundColor White
Write-Host "  - Itinerary Swagger API:     http://localhost:8002/docs" -ForegroundColor White
Write-Host "  - RabbitMQ Management UI:    http://localhost:15672 (guest/guest)" -ForegroundColor White
Write-Host "  - Jaeger Distributed Traces: http://localhost:16686" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
