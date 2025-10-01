param(
    [int]$Port = 8000
)

$ErrorActionPreference = 'Stop'

Write-Host "Killing any process on port $Port..." -ForegroundColor Yellow
Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty OwningProcess -Unique |
  ForEach-Object { try { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue } catch {} }

Write-Host "Starting backend on http://127.0.0.1:$Port ..." -ForegroundColor Cyan
Push-Location "$PSScriptRoot\backend"
try {
  .\venv\Scripts\Activate.ps1
  $env:DATABASE_URL = "sqlite:///./cinema_erp.db"
  uvicorn app.main:app --host 127.0.0.1 --port $Port
} finally {
  Pop-Location
}
