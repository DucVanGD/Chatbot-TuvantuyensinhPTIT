# Script chạy Action Server
# Chạy file này trong một terminal riêng

$ErrorActionPreference = "Stop"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting RASA Action Server" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
& "$PSScriptRoot\venv\Scripts\Activate.ps1"

# Start action server
Write-Host "Starting action server on port 5055..." -ForegroundColor Yellow
rasa run actions
