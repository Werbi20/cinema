# Smoke test for production API (Hosting or Cloud Run)
param(
  [string]$BaseUrl = 'https://cinema-erp-api-140199679738.us-central1.run.app'
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

if (-not $BaseUrl) {
  throw 'BaseUrl must not be empty'
}

# Normalize to API base. If BaseUrl already contains /api, assume it points to API base.
if ($BaseUrl -match '/api($|/)') {
  $apiBase = $BaseUrl.TrimEnd('/')
} else {
  $apiBase = ($BaseUrl.TrimEnd('/')) + '/api/v1'
}

Write-Host "Testing API base: $apiBase" -ForegroundColor Cyan

$tests = @(
  '/health',
  '/tags/',
  '/locations/',
  '/projects/'
)

foreach ($p in $tests) {
  $url = $apiBase + $p
  try {
    $resp = Invoke-WebRequest -UseBasicParsing -Uri $url -Method GET -TimeoutSec 20
    Write-Host ("{0} -> {1}" -f $p, $resp.StatusCode) -ForegroundColor Green
  } catch {
    $code = if ($_.Exception.Response) { $_.Exception.Response.StatusCode.value__ } else { 'ERR' }
    $msg = if ($_.Exception.Message) { $_.Exception.Message } else { $_.ToString() }
    Write-Host ("{0} -> {1} ({2})" -f $p, $code, $msg) -ForegroundColor Red
  }
}

Write-Host "Done." -ForegroundColor Yellow
