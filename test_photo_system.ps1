#!/usr/bin/env powershell

Write-Host "🚀 Iniciando sistema para teste de upload de fotos..." -ForegroundColor Green

# Matar processos existentes na porta 8020
Write-Host "🔄 Verificando processos na porta 8020..." -ForegroundColor Yellow
$processes = Get-Process | Where-Object {$_.ProcessName -eq "python"}
foreach ($process in $processes) {
    try {
        $connections = netstat -ano | Select-String ":8020" | Select-String $process.Id
        if ($connections) {
            Write-Host "   Matando processo Python $($process.Id)" -ForegroundColor Red
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
    } catch {
        # Ignorar erros
    }
}

# Esperar um pouco
Start-Sleep -Seconds 2

# Navegar para backend e ativar ambiente virtual
Set-Location "backend"

# Ativar ambiente virtual
Write-Host "🔧 Ativando ambiente virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Iniciar backend
Write-Host "🚀 Iniciando backend na porta 8020..." -ForegroundColor Green
Write-Host "   Backend será iniciado em segundo plano..." -ForegroundColor Gray

# Iniciar backend em job separado
$job = Start-Job -ScriptBlock {
    Set-Location $args[0]
    & ".\venv\Scripts\Activate.ps1"
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8020
} -ArgumentList (Get-Location).Path

# Esperar backend inicializar
Write-Host "⏳ Aguardando backend inicializar..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Testar se backend está funcionando
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8020/health" -Method GET -TimeoutSec 5
    Write-Host "✅ Backend está funcionando!" -ForegroundColor Green

    # Navegar de volta para raiz
    Set-Location ".."

    # Executar teste de upload
    Write-Host "🧪 Executando teste de upload..." -ForegroundColor Green
    python fix_photo_upload.py

} catch {
    Write-Host "❌ Backend não está respondendo" -ForegroundColor Red
    Write-Host "   Verificando output do job..." -ForegroundColor Yellow

    $jobOutput = Receive-Job -Job $job
    if ($jobOutput) {
        Write-Host "Output do backend:" -ForegroundColor Gray
        Write-Host $jobOutput -ForegroundColor Gray
    }
}

# Manter o job rodando para que o usuário possa continuar testando
Write-Host "💡 Backend está rodando em segundo plano." -ForegroundColor Cyan
Write-Host "   Use 'Get-Job' para verificar status" -ForegroundColor Cyan
Write-Host "   Use 'Stop-Job -Id $($job.Id)' para parar o backend" -ForegroundColor Cyan
Write-Host "   ID do Job: $($job.Id)" -ForegroundColor Cyan
