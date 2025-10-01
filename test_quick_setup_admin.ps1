# Creates an initial admin user in production via quick-setup endpoint
# Usage: Right-click > Run with PowerShell, or run in a PowerShell window.

$ErrorActionPreference = 'Stop'

$BaseUrl = 'https://palaoro-production.web.app/api/v1/quick-setup/create-user'

# Build JSON safely using a here-string to avoid quoting issues
$json = @'
{
  "email": "admin@cinema-erp.com",
  "full_name": "Admin",
  "password": "Adm1n!23",
  "role": "admin"
}
'@

Write-Host "POST $BaseUrl" -ForegroundColor Cyan
Write-Host $json -ForegroundColor Yellow

try {
  $resp = Invoke-RestMethod -Uri $BaseUrl -Method Post -Body $json -ContentType 'application/json'
  Write-Host "✅ Admin criado:" -ForegroundColor Green
  $resp | ConvertTo-Json -Depth 5
} catch {
  Write-Host "❌ Falha ao criar admin:" -ForegroundColor Red
  if ($_.Exception.Response) {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $responseBody = $reader.ReadToEnd()
    Write-Host $responseBody -ForegroundColor Red
  } else {
    Write-Host $_.Exception.Message -ForegroundColor Red
  }
}
