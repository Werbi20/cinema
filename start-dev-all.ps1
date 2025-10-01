param(
  [int]$Port = 8010
)

$ErrorActionPreference = 'Stop'
Write-Host "🚀 Starting backend and frontend (dev)" -ForegroundColor Cyan

# Start backend in a new window
$backendTitle = "Backend - Cinema ERP ($Port)"
$backendCmd = "cd `"$PSScriptRoot`"; powershell -NoProfile -ExecutionPolicy Bypass -File .\start-backend.ps1 -Port $Port"
Start-Process -FilePath powershell -ArgumentList '-NoProfile','-NoExit','-Command', $backendCmd -WindowStyle Normal -WorkingDirectory $PSScriptRoot -Verb Open -Wait:$false | Out-Null

Start-Sleep 5

# Health check
$healthUrl = "http://127.0.0.1:$Port/health"
try {
  $resp = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 5
  if ($resp.status -eq 'healthy') {
    Write-Host "✅ Backend OK: $healthUrl" -ForegroundColor Green
  } else {
    Write-Warning "Backend responded but not healthy: $($resp | ConvertTo-Json -Depth 3)"
  }
} catch {
  Write-Warning "Backend not reachable yet at $healthUrl"
}

# Start frontend in a new window
$frontendTitle = "Frontend - Cinema ERP"
$frontendCmd = "cd `"$PSScriptRoot\frontend`"; npm run dev"
Start-Process -FilePath powershell -ArgumentList '-NoProfile','-NoExit','-Command', $frontendCmd -WindowStyle Normal -WorkingDirectory "$PSScriptRoot\frontend" -Verb Open -Wait:$false | Out-Null

Write-Host "\n🌐 Frontend: http://localhost:5173" -ForegroundColor Yellow
Write-Host "🔧 Backend:  http://127.0.0.1:$Port" -ForegroundColor Yellow
Write-Host "📚 Docs:     http://127.0.0.1:$Port/docs" -ForegroundColor Yellow
