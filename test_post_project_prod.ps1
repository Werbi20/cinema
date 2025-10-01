# POST test against production Hosting -> Cloud Run for projects
param(
  [string]$BaseUrl = 'https://palaoro-production.firebaseapp.com/api/v1/projects'
)

$ErrorActionPreference = 'Stop'

$body = @{
    title = "Projeto teste sem cliente"
    description = "Criado para validar client_name opcional"
} | ConvertTo-Json -Depth 3

Write-Host "POST $BaseUrl" -ForegroundColor Cyan
Write-Host $body -ForegroundColor Yellow

try {
  $resp = Invoke-RestMethod -Uri $BaseUrl -Method POST -Body $body -ContentType 'application/json'
  Write-Host "✅ Projeto criado com sucesso:" -ForegroundColor Green
  $resp | ConvertTo-Json -Depth 4
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
