# Configuração Firebase para Cinema ERP - Versão Atualizada

## Novos Endpoints Adicionados

### Firebase Project Stages

#### 1. Criar Etapa via Firebase

```
POST /api/v1/project-stages/firebase
```

**Corpo da requisição:**

```json
{
  "name": "Preparação do Set",
  "description": "Configuração inicial do ambiente de filmagem",
  "status": "pending",
  "project_id": 1,
  "location_id": 2,
  "progress_percentage": 0,
  "budget_allocated": 5000.0,
  "planned_start_date": "2025-10-01",
  "planned_end_date": "2025-10-03",
  "notes": "Verificar equipamentos de iluminação",
  "order": 1
}
```

#### 2. Atualizar Status de Etapa via Firebase

```
PUT /api/v1/project-stages/{stage_id}/firebase
```

**Corpo da requisição:**

```json
{
  "status": "in_progress",
  "progress_percentage": 25,
  "notes": "Iniciado conforme planejado",
  "actual_start_date": "2025-10-01T08:00:00"
}
```

#### 3. Obter Resumo das Etapas via Firebase

```
GET /api/v1/project-stages/firebase/{project_id}/summary
```

#### 4. Obter Todas as Etapas de um Projeto via Firebase

```
GET /api/v1/project-stages/firebase/{project_id}
```

#### 5. Criar Etapas Padrão via Firebase

```
POST /api/v1/project-stages/firebase/{project_id}/location/{location_id}/default
```

#### 6. Sincronizar Etapas com Firebase

```
POST /api/v1/project-stages/firebase/sync
```

### Firebase Locations - Novos Endpoints para Etapas

#### 1. Obter Etapas de uma Locação

```
GET /api/v1/locations/{location_id}/firebase-project-stages?project_id={project_id}
```

#### 2. Criar Etapas Padrão para Locação

```
POST /api/v1/locations/{location_id}/firebase-project-stages/{project_id}/default
```

#### 3. Atualizar Status de Etapa de Locação

```
PUT /api/v1/locations/{location_id}/firebase-project-stages/{stage_id}/status
```

**Corpo da requisição:**

```json
{
  "status": "completed",
  "progress_percentage": 100,
  "notes": "Etapa concluída com sucesso"
}
```

## Status Válidos para Etapas

- `pending`: Pendente
- `in_progress`: Em andamento
- `completed`: Concluída
- `on_hold`: Em pausa
- `cancelled`: Cancelada
- `approved`: Aprovada
- `rejected`: Rejeitada

## Validações Implementadas

### Dados da Etapa

- **name**: Obrigatório, string não vazia
- **status**: Obrigatório, deve ser um dos status válidos
- **project_id**: Obrigatório, número inteiro
- **location_id**: Obrigatório, número inteiro
- **progress_percentage**: Opcional, número entre 0 e 100
- **budget_allocated**: Opcional, número decimal positivo

### Tratamento de Erros

#### Conectividade Firebase

- **503 Service Unavailable**: Firebase não disponível
- **500 Internal Server Error**: Erro de banco de dados ou inesperado

#### Validação de Dados

- **400 Bad Request**: Dados inválidos ou campos obrigatórios ausentes
- **404 Not Found**: Recurso não encontrado (projeto, locação, etapa)

#### Logs Detalhados

Todos os endpoints incluem logging detalhado para:

- Operações bem-sucedidas
- Erros de validação
- Falhas de banco de dados
- Problemas de conectividade

## Melhorias Implementadas

### 1. **Validação Robusta**

- Verificação de tipos de dados
- Conversão automática quando possível
- Mensagens de erro específicas

### 2. **Tratamento de Transações**

- Rollback automático em caso de erro
- Commits explícitos após operações bem-sucedidas

### 3. **Conectividade Firebase**

- Verificação de disponibilidade antes de operações
- Função auxiliar reutilizável

### 4. **Serialização Completa**

- Conversão adequada de datas para ISO format
- Campos opcionais tratados corretamente

### 5. **Integração com Serviços Existentes**

- Uso dos serviços já implementados
- Evita duplicação de lógica de negócio

## Compatibilidade

Todos os novos endpoints são totalmente compatíveis com:

- Frontend React atualizado
- Sistema de queries do React Query
- Estrutura de dados existente
- Validações de tipos TypeScript

## Próximos Passos

1. **Testes de Integração**: Validar endpoints com dados reais
2. **Documentação Swagger**: Atualizar documentação automática
3. **Monitoramento**: Implementar métricas de performance
4. **Cache**: Adicionar cache para consultas frequentes
