# Teste simples do endpoint POST
$body = @{
    name = "Teste Location"
    address = "Rua Teste, 123"
    city = "Sao Paulo"
    state = "SP"
    zip_code = "01234-567"
    phone = "(11) 99999-9999"
    email = "teste@exemplo.com"
    status = "active"
    sector_type = "commercial"
    space_type = "office"
    area = 100.5
    capacity = 50
    description = "Locacao de teste"
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
