# Teste correto do endpoint POST com schema adequado
$body = @{
    title = "Teste Location"
    summary = "Locacao de teste para validacao da API"
    description = "Locacao de teste para validacao da API"
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

Write-Host "Enviando dados:" -ForegroundColor Yellow
Write-Host $body -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/locations" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Sucesso! Locação criada:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Erro na requisição:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Resposta do servidor:" -ForegroundColor Yellow
        Write-Host $responseBody -ForegroundColor Red
    }
}
