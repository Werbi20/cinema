# Test script to debug project creation issue
Write-Host "Testing Project Creation API" -ForegroundColor Yellow

$body = @{
    title = "Test Project"
    description = "Test project description"
    budget = 1000.0
    client_name = "Test Client"
} | ConvertTo-Json -Depth 3

Write-Host "Sending request to http://localhost:8000/api/v1/projects/" -ForegroundColor Cyan
Write-Host "Body:" -ForegroundColor White
Write-Host $body -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/projects/" -Method POST -Body $body -ContentType "application/json" -Verbose
    Write-Host "✅ Success! Project created:" -ForegroundColor Green
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ Error occurred:" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "Status Description: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red

    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response Body:" -ForegroundColor Red
        Write-Host $responseBody -ForegroundColor Red
    }

    Write-Host "Full Error:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}
