# Script chạy RASA Shell
# Trước khi chạy file này, hãy chạy run_actions.ps1 trong terminal khác

$ErrorActionPreference = "Stop"

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Starting RASA Chatbot Shell" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "CẢNH BÁO: Hãy đảm bảo Action Server đã được khởi động!" -ForegroundColor Red
Write-Host "Chạy 'run_actions.ps1' trong terminal khác trước." -ForegroundColor Yellow
Write-Host ""
Write-Host "Nhấn Enter để tiếp tục..." -ForegroundColor Yellow
Read-Host

# Activate virtual environment
& "$PSScriptRoot\venv\Scripts\Activate.ps1"

# Start RASA shell
Write-Host "Starting RASA shell..." -ForegroundColor Yellow

# Suppress warnings
$env:LOG_LEVEL = "WARNING"
$env:SQLALCHEMY_SILENCE_UBER_WARNING = "1"
$env:PYTHONWARNINGS = "ignore"

rasa shell
