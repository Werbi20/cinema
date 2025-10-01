param(
    [int]$Port = 8010,
    [string]$LogDir = "backend/logs",
    [string]$AppHost = "127.0.0.1"
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$logFile = Join-Path $LogDir "backend-$Port-$timestamp.log"
$errFile = Join-Path $LogDir "backend-$Port-$timestamp.err.log"

Write-Host "[DETACHED] Starting backend uvicorn directly on $($AppHost):$($Port) (logs: $logFile)" -ForegroundColor Cyan

# Kill existing process using port
Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
  Select-Object -ExpandProperty OwningProcess -Unique |
  ForEach-Object { try { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue } catch {} }

Push-Location "$PSScriptRoot/backend"
try {
    if (Test-Path .\venv\Scripts\Activate.ps1) { . .\venv\Scripts\Activate.ps1 }
    $env:DATABASE_URL = "sqlite:///./cinema_erp.db"
    Start-Process python -ArgumentList @('-m','uvicorn','app.main:app','--host',$AppHost,'--port',$Port) -RedirectStandardOutput $logFile -RedirectStandardError $errFile -WindowStyle Hidden | Out-Null
} finally {
    Pop-Location
}

Start-Sleep 5

$healthUrl = "http://$($AppHost):$($Port)/health"
$ok = $false
try {
    $resp = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 5
    if ($resp.status -and $resp.status -eq 'healthy') { $ok = $true }
} catch {}

if ($ok) {
    Write-Host "[DETACHED] Backend healthy at $healthUrl" -ForegroundColor Green
} else {
    Write-Warning "[DETACHED] Backend not healthy yet. Check logs: $logFile / $errFile"
}

Write-Output $logFile
