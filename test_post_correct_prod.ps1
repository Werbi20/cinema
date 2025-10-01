# POST test against production Hosting -> Cloud Run
param(
  [string]$BaseUrl = 'https://palaoro-production.firebaseapp.com/api/v1/locations'
)

$ErrorActionPreference = 'Stop'

$body = @{
    title = "Teste Location"
    summary = "Locacao de teste via prod"
    description = "Locacao de teste via Hosting"
    status = "draft"
    sector_type = "cinema"
    space_type = "office"
    area_size = 100.5
    capacity = 50
    city = "Sao Paulo"
    state = "SP"
    country = "Brasil"
    postal_code = "01234-567"
    supplier_name = "Fornecedor Teste"
    supplier_phone = "(11) 99999-9999"
    supplier_email = "teste@exemplo.com"
    currency = "BRL"
    price_day_cinema = 1000.0
    price_hour_cinema = 150.0
} | ConvertTo-Json -Depth 3

Write-Host "POST $BaseUrl" -ForegroundColor Cyan
Write-Host $body -ForegroundColor Yellow

try {
  $resp = Invoke-RestMethod -Uri $BaseUrl -Method POST -Body $body -ContentType 'application/json'
  Write-Host "✅ Criada com sucesso:" -ForegroundColor Green
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
