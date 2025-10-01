# Script to test project creation and debug the 500 error
# This will run in a separate process to avoid interfering with the server

Write-Host "=== Cinema ERP Project Creation Debug ===" -ForegroundColor Yellow
Write-Host "Testing project creation API to identify the 500 error..." -ForegroundColor Cyan

# Test data
$testProject = @{
    title = "Test Project Debug"
    description = "Testing project creation to identify error"
    budget = 1500.0
    client_name = "Debug Client"
} | ConvertTo-Json -Depth 3

Write-Host "`nRequest Body:" -ForegroundColor White
Write-Host $testProject -ForegroundColor Gray

try {
    Write-Host "`nMaking HTTP POST request to http://localhost:8000/api/v1/projects/" -ForegroundColor Cyan

    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/projects/" -Method POST -Body $testProject -ContentType "application/json" -ErrorAction Stop

    Write-Host "✅ SUCCESS! Project created:" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 3) -ForegroundColor Green

} catch {
    Write-Host "❌ ERROR DETECTED:" -ForegroundColor Red
    Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Status Description: $($_.Exception.Response.StatusDescription)" -ForegroundColor Red

    # Try to get response body
    if ($_.Exception.Response) {
        try {
            $stream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $responseBody = $reader.ReadToEnd()
            Write-Host "`nServer Response:" -ForegroundColor Yellow
            Write-Host $responseBody -ForegroundColor Red
        } catch {
            Write-Host "Could not read response body" -ForegroundColor Yellow
        }
    }

    Write-Host "`nFull Error Details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red

    if ($_.Exception.Response.StatusCode.value__ -eq 500) {
        Write-Host "`n🔍 ANALYSIS: 500 Internal Server Error detected" -ForegroundColor Magenta
        Write-Host "This is likely caused by:" -ForegroundColor Magenta
        Write-Host "  1. Foreign key constraint violation (no user with ID 1)" -ForegroundColor Magenta
        Write-Host "  2. Database schema mismatch" -ForegroundColor Magenta
        Write-Host "  3. Missing required fields in project creation" -ForegroundColor Magenta
    }
}

Write-Host "`n=== Debug Complete ===" -ForegroundColor Yellow
