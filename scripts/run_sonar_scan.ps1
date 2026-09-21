# Script de Análisis Estático de Código con SonarScanner
param (
    [string]$SonarHost = "http://localhost:9000",
    [string]$SonarToken = $env:SONAR_TOKEN
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "Ejecutando Análisis Estático con SonarQube" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Validar reporte de cobertura
if (-not (Test-Path "coverage.xml")) {
    Write-Host "Generando coverage.xml antes de escanear..." -ForegroundColor Yellow
    & .\scripts\run_tests.ps1
}

# 2. Ejecutar sonar-scanner
if (Get-Command sonar-scanner -ErrorAction SilentlyContinue) {
    if ($SonarToken) {
        sonar-scanner -Dsonar.host.url=$SonarHost -Dsonar.token=$SonarToken
    } else {
        sonar-scanner -Dsonar.host.url=$SonarHost
    }
} else {
    Write-Host "sonar-scanner CLI no encontrado. Puede ejecutar vía Docker con:" -ForegroundColor Yellow
    Write-Host "docker run --rm -v `${PWD}:/usr/src sonarsource/sonar-scanner-cli -Dsonar.host.url=$SonarHost" -ForegroundColor White
}
