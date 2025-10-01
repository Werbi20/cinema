param(
  [string]$BaseUrl = 'https://palaoro-production.firebaseapp.com/api/v1/locations/'
)

$ErrorActionPreference = 'Stop'

Write-Host "GET $BaseUrl" -ForegroundColor Cyan
try {
  $resp = Invoke-RestMethod -Uri $BaseUrl -Method GET
  Write-Host ("Total: {0}" -f $resp.Count)
  $resp | Select-Object id, title, status, city, space_type | Format-Table -AutoSize
} catch {
  Write-Host "❌ Falha no GET:" -ForegroundColor Red
  if ($_.Exception.Response) {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $responseBody = $reader.ReadToEnd()
    Write-Host $responseBody -ForegroundColor Red
  } else {
    Write-Host $_.Exception.Message -ForegroundColor Red
  }
}
