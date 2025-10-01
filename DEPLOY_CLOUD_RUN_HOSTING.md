# Deploy Unificado: Cloud Run (Backend) + Firebase Hosting (Frontend)

## Visão Geral

Este fluxo constrói a imagem Docker do backend FastAPI, publica no Artifact Registry, faz deploy no Cloud Run e em seguida publica o frontend no Firebase Hosting com rewrite /api/\*\* apontando para o serviço.

## Pré-requisitos

- gcloud CLI autenticado: `gcloud auth login`
- Projeto configurado: `gcloud config set project <PROJECT_ID>`
- Firebase CLI autenticado: `firebase login`
- APIs habilitadas (uma vez):

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

- Repositório Artifact Registry criado (uma vez):

```bash
gcloud artifacts repositories create cinema-backend \
  --repository-format=docker \
  --location=us-central1 \
  --description="Cinema ERP backend images"
```

## Script Principal

Use: `deploy_cloudrun_hosting.ps1`

### Parâmetros

| Parâmetro          | Default            | Descrição                              |
| ------------------ | ------------------ | -------------------------------------- |
| `ProjectId`        | palaoro-production | ID do projeto GCP/Firebase             |
| `Region`           | us-central1        | Região Cloud Run / Artifact Registry   |
| `ServiceName`      | cinema-backend     | Nome do serviço Cloud Run              |
| `RepoName`         | cinema-backend     | Nome do repositório Artifact Registry  |
| `ImageTag`         | latest             | Tag da imagem                          |
| `SkipBuild`        | (switch)           | Pula etapa de build da imagem          |
| `SkipCloudRun`     | (switch)           | Pula deploy Cloud Run                  |
| `SkipHosting`      | (switch)           | Pula deploy Hosting                    |
| `EnablePlaywright` | (switch)           | Define PLAYWRIGHT_ENABLED=1 no serviço |
| `DryRun`           | (switch)           | Mostra comandos sem executar           |

### Exemplos

Build + deploy completo:

```powershell
./deploy_cloudrun_hosting.ps1 -ProjectId palaoro-production
```

Somente atualizar frontend (sem rebuild backend):

```powershell
./deploy_cloudrun_hosting.ps1 -SkipBuild -SkipCloudRun
```

Habilitar Playwright para PDF:

```powershell
./deploy_cloudrun_hosting.ps1 -EnablePlaywright
```

Dry-run (visualizar comandos):

```powershell
./deploy_cloudrun_hosting.ps1 -DryRun
```

## Variáveis de Ambiente Backend

Definidas via `--set-env-vars` no deploy. Adicionar conforme necessário:

- `DATABASE_URL` (ex: postgres://user:pass@host:5432/db)
- `SECRET_KEY`
- `OPENAI_API_KEY` (opcional para enriquecimento IA)
- `PLAYWRIGHT_ENABLED=1` (para PDF servidor real)

Para atualizar sem rebuild da imagem (apenas env vars):

```powershell
gcloud run deploy cinema-backend `
  --project palaoro-production `
  --region us-central1 `
  --image us-central1-docker.pkg.dev/palaoro-production/cinema-backend/backend:latest `
  --set-env-vars SECRET_KEY=xxx,DATABASE_URL=...,OPENAI_API_KEY=...,PLAYWRIGHT_ENABLED=1
```

## firebase.json Rewrite

Já configurado:

```json
"rewrites": [
  { "source": "/api/**", "run": { "serviceId": "cinema-backend", "region": "us-central1" } }
]
```

## Validação Pós-Deploy

Veja `POST_DEPLOY_VALIDATION.md`.

## Rollback

- Listar revisões: `gcloud run revisions list --service cinema-backend --region us-central1`
- Reverter: `gcloud run deploy cinema-backend --revision <REVISAO> --region us-central1`

## Dicas Performance

- Ajustar `--max-instances` conforme tráfego.
- Usar conexão gerenciada (Cloud SQL) se migrar DB.
- Ativar Cloud Logging & Error Reporting.

## Playwright (PDF Servidor)

Para gerar PDFs reais (em vez do fallback HTML) é necessário:

1. Adicionar dependências de runtime do Chromium (a imagem python:3.11-slim frequentemente já suporta; se faltar libs, criar Dockerfile estágio que roda `playwright install --with-deps chromium`).
2. Definir `PLAYWRIGHT_ENABLED=1` no deploy.
3. (Opcional) Cache de layer: executar `playwright install chromium` durante build para evitar download em cada cold start.

Exemplo Dockerfile trecho:

```dockerfile
RUN pip install playwright && playwright install --with-deps chromium
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
```

## Staging vs Produção

O script suporta `-Staging` para:

- Sufixar serviço Cloud Run: `<service>-staging`
- Usar canal de Hosting: `firebase hosting:channel:deploy staging`
- Permitir teste sem afetar site live

Deploy staging:

```powershell
./deploy_cloudrun_hosting.ps1 -Staging -ImageTag staging
```

## Próximos Passos

- Adicionar pipeline CI (GitHub Actions) para automatizar.
- Separar ambientes (staging vs production) com projeto ou prefixos.
- Monitorar custo de invocações Cloud Run.
