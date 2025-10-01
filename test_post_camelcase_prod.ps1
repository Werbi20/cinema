# POST camelCase payload against production Hosting -> Cloud Run
param(
  [string]$BaseUrl = 'https://palaoro-production.firebaseapp.com/api/v1/locations/'
)

$ErrorActionPreference = 'Stop'

$bodyObj = @{
    title = "Teste CamelCase"
    summary = "Envio camelCase via prod"
    description = "Compat handler test"
    status = "APPROVED"
    sectorType = "CINEMA"
    spaceType = "indoor"
    city = "Rio de Janeiro"
    country = "Brasil"
}

$body = $bodyObj | ConvertTo-Json -Depth 3

Write-Host "POST $BaseUrl" -ForegroundColor Cyan
Write-Host $body -ForegroundColor Yellow

try {
  $resp = Invoke-RestMethod -Uri $BaseUrl -Method POST -Body $body -ContentType 'application/json'
  Write-Host "✅ Criada com sucesso:" -ForegroundColor Green
  $resp | ConvertTo-Json -Depth 5
} catch {
  Write-Host "❌ Falha no POST:" -ForegroundColor Red
  if ($_.Exception.Response) {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $responseBody = $reader.ReadToEnd()
    Write-Host $responseBody -ForegroundColor Red
  } else {
    Write-Host $_.Exception.Message -ForegroundColor Red
  }
}
