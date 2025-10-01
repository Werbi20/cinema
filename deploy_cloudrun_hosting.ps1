param(
  [string]$ProjectId = "palaoro-production",
  [string]$Region = "us-central1",
  [string]$ServiceName = "cinema-backend",
  [string]$RepoName = "cinema-backend",
  [string]$ImageTag = "latest",
  [switch]$Staging,
  [switch]$SkipBuild,
  [switch]$SkipCloudRun,
  [switch]$SkipHosting,
  [switch]$EnablePlaywright,
  [switch]$DryRun
)

Write-Host "=== Unified Deploy: Cloud Run + Firebase Hosting ===" -ForegroundColor Cyan
if ($Staging) { Write-Host "(Modo STAGING)" -ForegroundColor Magenta }
Write-Host "Project: $ProjectId | Region: $Region | Service: $ServiceName" -ForegroundColor Yellow

function Exec {
  param($Cmd, [string]$Desc)
  Write-Host "-- $Desc" -ForegroundColor DarkCyan
  Write-Host "   > $Cmd" -ForegroundColor DarkGray
  if ($DryRun) { return }
  Invoke-Expression $Cmd
  if ($LASTEXITCODE -ne 0) { throw "Failed: $Desc" }
}

if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) { throw "gcloud CLI não encontrado" }
if (-not (Get-Command firebase -ErrorAction SilentlyContinue)) { throw "Firebase CLI não encontrado" }

if ($Staging) {
  if (-not $ImageTag) { $ImageTag = "staging" }
  $ServiceEffective = "$ServiceName-staging"
  $ImagePath = "$Region-docker.pkg.dev/$ProjectId/$RepoName/backend:$ImageTag"
} else {
  $ServiceEffective = $ServiceName
  $ImagePath = "$Region-docker.pkg.dev/$ProjectId/$RepoName/backend:$ImageTag"
}

if (-not $SkipBuild) {
  Exec "gcloud builds submit --project $ProjectId --region $Region --tag $ImagePath ./backend" "Cloud Build image $ImagePath"
}
else {
  Write-Host "SkipBuild ON - pulando build" -ForegroundColor DarkYellow
}

$playwrightFlag = if ($EnablePlaywright) { '1' } else { '0' }

if (-not $SkipCloudRun) {
  $envVars = @(
    "PLAYWRIGHT_ENABLED=$playwrightFlag"
  )
  $envVarArgs = $envVars -join ','
  Exec "gcloud run deploy $ServiceEffective --project $ProjectId --region $Region --image $ImagePath --port 8080 --allow-unauthenticated --set-env-vars $envVarArgs" "Deploy Cloud Run service $ServiceEffective"
}
else {
  Write-Host "SkipCloudRun ON - pulando deploy Cloud Run" -ForegroundColor DarkYellow
}

if (-not $SkipHosting) {
  if (-not (Test-Path frontend)) { throw "Pasta frontend não encontrada" }
  Push-Location frontend
  if (-not (Test-Path node_modules)) { Exec "npm install --no-audit --no-fund" "Install frontend deps" }
  Exec "npm run build" "Build frontend"
  Pop-Location
  if ($Staging) {
    Exec "firebase hosting:channel:deploy staging --project $ProjectId" "Deploy Hosting staging channel"
  } else {
    Exec "firebase deploy --only hosting --project $ProjectId" "Deploy Firebase Hosting (live)"
  }
}
else {
  Write-Host "SkipHosting ON - pulando deploy Hosting" -ForegroundColor DarkYellow
}

Write-Host "=== Deploy finalizado com sucesso ===" -ForegroundColor Green
if ($Staging) {
  Write-Host "Health test staging (após propagação): https://staging-$ProjectId.web.app/api/v1/health (ou URL do canal retornada)" -ForegroundColor Gray
} else {
  Write-Host "Health test (após propagação): https://$ProjectId.web.app/api/v1/health" -ForegroundColor Gray
}
Write-Host "PDF export (se Playwright): POST https://$ProjectId.web.app/api/v1/presentations/export" -ForegroundColor Gray
