param(
    [string]$BaseUrl = "http://localhost:8000"
)

# Teste mínimo com apenas o campo obrigatório
$bodyObj = @{ title = "Teste Minimal" }
$body = $bodyObj | ConvertTo-Json -Depth 3

$url = "$BaseUrl/api/v1/locations/"  # usar barra final para evitar redirecionamento 307

Write-Host "Enviando dados mínimos para: $url" -ForegroundColor Yellow
Write-Host $body -ForegroundColor Cyan

try {
    $response = Invoke-RestMethod -Uri $url -Method POST -Body $body -ContentType "application/json"
    Write-Host "✅ Sucesso! Locação criada:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "❌ Erro na requisição:" -ForegroundColor Red
    $ex = $_.Exception
    Write-Host $ex.Message -ForegroundColor Red
    if ($ex.Response) {
        try {
            $resp = [System.Net.HttpWebResponse]$ex.Response
            Write-Host ("StatusCode: {0}" -f [int]$resp.StatusCode) -ForegroundColor DarkYellow
        } catch {}
        try {
            $reader = New-Object System.IO.StreamReader($ex.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            if ($responseBody) {
                Write-Host "Resposta do servidor:" -ForegroundColor Yellow
                Write-Host $responseBody -ForegroundColor Red
            }
        } catch {}
    }
    exit 1
}
