param(
  [string]$ProjectId = "palaoro-production",
  [switch]$SkipFunctions,
  [switch]$SkipHosting,
  [switch]$SkipRules,
  [switch]$SkipIndexes,
  [switch]$SkipStorage,
  [switch]$OnlyBuildFrontend
)

Write-Host "=== Cinema ERP - Deploy Firebase ===" -ForegroundColor Cyan
Write-Host "Projeto: $ProjectId" -ForegroundColor Yellow

if (-not (Get-Command firebase -ErrorAction SilentlyContinue)) {
  Write-Host "Firebase CLI não encontrado. Instale com: npm install -g firebase-tools" -ForegroundColor Red
  exit 1
}

Write-Host "Selecionando projeto..." -ForegroundColor Yellow
firebase use $ProjectId 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "Falha ao selecionar projeto" -ForegroundColor Red; exit 1 }

# Build frontend
if (Test-Path frontend) {
  Write-Host "Build frontend..." -ForegroundColor Yellow
  Push-Location frontend
  if (-not (Test-Path node_modules)) { npm install --no-audit --no-fund }
  npm run build
  if ($LASTEXITCODE -ne 0) { Write-Host "Falha build frontend" -ForegroundColor Red; Pop-Location; exit 1 }
  Pop-Location
} else {
  Write-Host "Pasta frontend não encontrada" -ForegroundColor Red
}

if ($OnlyBuildFrontend) { Write-Host "OnlyBuildFrontend ativo - encerrando." -ForegroundColor Green; exit 0 }

$targets = @()
if (-not $SkipRules)   { $targets += 'firestore:rules' }
if (-not $SkipIndexes) { $targets += 'firestore:indexes' }
if (-not $SkipStorage) { $targets += 'storage' }
if (-not $SkipFunctions) { $targets += 'functions' }
if (-not $SkipHosting) { $targets += 'hosting' }

if ($targets.Count -eq 0) {
  Write-Host "Nenhum target selecionado - nada a fazer." -ForegroundColor Yellow
  exit 0
}

Write-Host ("Targets: " + ($targets -join ', ')) -ForegroundColor Cyan

$deployCmd = "firebase deploy --only " + ($targets -join ',')
Write-Host "Executando: $deployCmd" -ForegroundColor Yellow
Invoke-Expression $deployCmd
if ($LASTEXITCODE -ne 0) { Write-Host "Falha no deploy" -ForegroundColor Red; exit 1 }

Write-Host "Deploy concluído com sucesso!" -ForegroundColor Green

Write-Host "Sugestões de testes pós-deploy:" -ForegroundColor Cyan
Write-Host "  1. Verificar Hosting: https://$ProjectId.web.app" -ForegroundColor Gray
Write-Host "  2. Testar health API via rewrite (se Cloud Run ativo): https://$ProjectId.web.app/api/v1/health" -ForegroundColor Gray
Write-Host "  3. Enviar imagem para Storage e checar thumbnail (pasta locations)." -ForegroundColor Gray
Write-Host "  4. Ver logs Functions: firebase functions:log --only generateLocationThumbnail" -ForegroundColor Gray
