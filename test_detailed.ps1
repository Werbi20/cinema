# Teste detalhado com captura completa do erro
$body = @{
    title = "Teste Detailed"
} | ConvertTo-Json -Depth 3

Write-Host "Enviando dados:" -ForegroundColor Yellow
Write-Host $body -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/locations" -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Sucesso! Locação criada:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Erro na requisição:" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "Status Description: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red

    if ($_.Exception.Response) {
        $stream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($stream)
        $responseBody = $reader.ReadToEnd()
        Write-Host "Resposta completa do servidor:" -ForegroundColor Yellow
        Write-Host $responseBody -ForegroundColor Red
    }

    Write-Host "`nDetalhes da exceção:" -ForegroundColor Yellow
    Write-Host $_.Exception.ToString() -ForegroundColor Red
}

