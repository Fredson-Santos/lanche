# TASK 1B: Reposição Automática de Estoque - Documentação Completa

## 📌 Visão Geral

**Requisito Funcional:** RF-06 - Reposição Automática de Estoque
**Fase:** 1 (Sprint Final)
**Prioridade:** ⭐⭐⭐ MÁXIMA
**Data de Conclusão:** 19 de Abril de 2026
**Status:** ✅ COMPLETO

### Objetivo

Implementar um sistema automatizado de reposição de estoque que:

1. **Monitorar Estoques Mínimos**: Verificar periodicamente se produtos estão abaixo do ponto de reposição
2. **Criar Ordens Automáticas**: Gerar ordens de reposição quando estoque atinge limites configuráveis
3. **Gerenciar Ordens Manuais**: Permitir criação e confirmação manual de ordens
4. **Rastrear Recebimento**: Registrar receitas parciais ou completas com atualização de estoque
5. **Auditoria**: Manter histórico de todas as operações de reposição

---

## 🏗️ Arquitetura da Solução

### Padrão de Camadas

```
Backend FastAPI
│
├─ Models (ORM)
│  └─ OrdemReposicao: Modelo de ordem com status e datas
│  └─ Estoque (modificado): Adicionado campos de configuração
│
├─ Schemas (Validação)
│  └─ OrdemReposicaoCreate/Update/Response
│  └─ EstoqueCreate/Update/Response (modificado)
│
├─ Utils (Negócio)
│  └─ reposicao.py: 7 funções de lógica de negócio
│  └─ scheduler.py (modificado): Job de verificação a cada 30 min
│
├─ Routes (API)
│  └─ reposicao.py: 7 endpoints RESTful com RBAC
│
└─ Database
   └─ Migrations: Alembic version b2c3d4e5f6a7
   └─ Tabelas: ordens_reposicao (nova) + campos em estoques
```

### Componentes Frontend

```
React Frontend
│
├─ Pages
│  └─ ReposicaoPage.jsx: Interface completa de gerenciamento
│
├─ Navigation
│  └─ Sidebar: Link integrado com ícone 🔄
│
└─ Hooks
   └─ useApi.js (reutilizado): Requisições HTTP
```

---

## 📊 Modelo de Dados

### OrdemReposicao

```python
class OrdemReposicao(Base):
    __tablename__ = "ordens_reposicao"
    
    id: int                         # Identificador único
    estoque_id: int                 # FK para Estoque
    produto_id: int                 # FK para Produto
    quantidade_solicitada: int      # Quantidade pedida
    quantidade_recebida: int        # Quantidade efetivamente recebida
    status: str                     # PENDENTE | CONFIRMADA | RECEBIDA | CANCELADA
    motivo: str                     # automática | manual
    observacoes: str                # Notas da ordem
    data_criacao: DateTime          # Timestamp de criação
    data_confirmacao: DateTime      # Quando foi confirmada
    data_recebimento: DateTime      # Quando foi recebida
    data_cancelamento: DateTime     # Quando foi cancelada
```

### StatusOrdemReposicao (Enum)

```python
class StatusOrdemReposicao(str, Enum):
    PENDENTE = "pendente"           # Criada, aguardando confirmação
    CONFIRMADA = "confirmada"       # Confirmada, aguardando recebimento
    RECEBIDA = "recebida"          # Recebida completamente
    CANCELADA = "cancelada"         # Cancelada antes de receber
```

### Estoque (Campos Novos)

```python
estoque_minimo: int          # Limite mínimo de estoque (padrão: 0)
estoque_maximo: int          # Limite máximo desejado (padrão: 100)
ponto_reposicao: int         # Valor que dispara automática (padrão: 10)
```

**Lógica de Reposição:**
- Quando `quantidade <= ponto_reposicao`: Sistema cria ordem
- Quantidade a pedir: `estoque_maximo - quantidade_atual`

---

## 🔌 API REST - Endpoints

### 1. Listar Ordens de Reposição

```http
GET /api/reposicao/
```

**Parâmetros Query:**
- `status_filtro` (opcional): "pendente", "confirmada", "recebida", "cancelada"
- `estoque_id` (opcional): ID do estoque para filtrar

**Resposta (200 OK):**
```json
[
  {
    "id": 1,
    "estoque_id": 5,
    "produto_id": 3,
    "quantidade_solicitada": 50,
    "quantidade_recebida": 0,
    "status": "pendente",
    "motivo": "automática",
    "observacoes": "Reposição automática",
    "data_criacao": "2026-04-19T10:00:00Z"
  }
]
```

**Auth:** Requer `@require_gerente` (gerente/admin)

---

### 2. Obter Detalhes de Uma Ordem

```http
GET /api/reposicao/{ordem_id}
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "estoque_id": 5,
  "produto_id": 3,
  "quantidade_solicitada": 50,
  "quantidade_recebida": 0,
  "status": "pendente",
  "motivo": "automática",
  "observacoes": "Reposição automática",
  "data_criacao": "2026-04-19T10:00:00Z",
  "data_confirmacao": null,
  "data_recebimento": null,
  "data_cancelamento": null
}
```

**Erros:**
- `404 NOT FOUND`: Ordem não encontrada

**Auth:** Requer `@require_gerente`

---

### 3. Criar Ordem Manual

```http
POST /api/reposicao/
Content-Type: application/json

{
  "estoque_id": 5,
  "produto_id": 3,
  "quantidade_solicitada": 100,
  "observacoes": "Pedido urgente para promoção"
}
```

**Resposta (201 CREATED):**
```json
{
  "id": 2,
  "estoque_id": 5,
  "produto_id": 3,
  "quantidade_solicitada": 100,
  "quantidade_recebida": null,
  "status": "pendente",
  "motivo": "manual",
  "observacoes": "Pedido urgente para promoção",
  "data_criacao": "2026-04-19T10:15:00Z"
}
```

**Erros:**
- `404 NOT FOUND`: Estoque não existe
- `400 BAD REQUEST`: Dados inválidos

**Auth:** Requer `@require_gerente`

---

### 4. Confirmar Ordem

```http
PUT /api/reposicao/{ordem_id}/confirmar
```

**Resposta (200 OK):**
```json
{
  "id": 1,
  "status": "confirmada",
  "data_confirmacao": "2026-04-19T10:30:00Z"
}
```

**Lógica:**
- Muda status de PENDENTE → CONFIRMADA
- Registra `data_confirmacao`
- Pode ser revertido cancelando

**Erros:**
- `400 BAD REQUEST`: Ordem não está PENDENTE
- `404 NOT FOUND`: Ordem não encontrada

**Auth:** Requer `@require_gerente`

---

### 5. Registrar Recebimento

```http
PUT /api/reposicao/{ordem_id}/receber?quantidade_recebida=50
```

**Parâmetros:**
- `quantidade_recebida`: Quanto foi realmente recebido (numérico)

**Resposta (200 OK):**
```json
{
  "id": 1,
  "quantidade_solicitada": 50,
  "quantidade_recebida": 50,
  "status": "recebida",
  "data_recebimento": "2026-04-19T11:00:00Z"
}
```

**Lógica:**
- Atualiza `quantidade_recebida`
- Aumenta `estoque.quantidade` pelo valor recebido
- Se `recebido >= solicitado`: status = RECEBIDA
- Se `recebido < solicitado`: mantém CONFIRMADA (recebimento parcial)

**Exemplo de Impacto no Estoque:**
```
ANTES:
  estoque.quantidade = 10
  
DEPOIS (recebimento de 50):
  estoque.quantidade = 10 + 50 = 60
```

**Erros:**
- `400 BAD REQUEST`: Ordem cancelada ou inválida
- `404 NOT FOUND`: Ordem não existe

**Auth:** Requer `@require_gerente`

---

### 6. Cancelar Ordem

```http
DELETE /api/reposicao/{ordem_id}?motivo=Falta%20de%20estoque%20no%20fornecedor
```

**Parâmetros:**
- `motivo` (opcional): Razão do cancelamento

**Resposta (200 OK):**
```json
{
  "id": 1,
  "status": "cancelada",
  "data_cancelamento": "2026-04-19T11:30:00Z",
  "observacoes": "Cancelada: Falta de estoque no fornecedor"
}
```

**Restrições:**
- Não pode cancelar ordem já RECEBIDA
- Registra motivo em `observacoes`

**Erros:**
- `400 BAD REQUEST`: Ordem já foi recebida
- `404 NOT FOUND`: Ordem não existe

**Auth:** Requer `@require_gerente`

---

### 7. Dashboard - Resumo de Reposições

```http
GET /api/reposicao/dashboard/resumo
```

**Resposta (200 OK):**
```json
{
  "ordens_pendentes": 3,
  "ordens_recebidas_7dias": 12,
  "quantidade_total_pendente": 250,
  "quantidade_total_recebida": 1840
}
```

**Campos:**
- `ordens_pendentes`: Contar ordens com status PENDENTE ou CONFIRMADA
- `ordens_recebidas_7dias`: Ordens RECEBIDAS nos últimos 7 dias
- `quantidade_total_pendente`: Soma de (solicitado - recebido) para ordens abertas
- `quantidade_total_recebida`: Soma de quantidade_recebida para ordens recentes

**Auth:** Requer `@require_gerente`

---

## ⚙️ Job Agendado - Verificação Automática

### Job: `job_verificar_estoques_minimos()`

**Intervalo:** A cada **30 minutos**
**Horário:** Executado continuamente pelo APScheduler
**Função:** Verificar todos os estoques e criar ordens automaticamente

**Algoritmo:**
```python
1. Listar todos os Estoque
2. Para cada estoque:
   a. Se quantidade <= ponto_reposicao:
      i. Verificar se existe ordem PENDENTE ou CONFIRMADA ativa
      ii. Se NÃO existe:
          - Calcular quantidade = estoque_maximo - quantidade
          - Criar nova OrdemReposicao com motivo="automática"
   b. Se não <= ponto_reposicao:
      i. Continuar para próximo
3. Registrar em log: "X ordens criadas"
```

**Logging:**
```
INFO: Job verificar_estoques_minimos executado: 3 ordens de reposição criadas
```

**Erro Handling:**
```
ERROR: Erro ao verificar estoques mínimos: [exceção]
```

---

## 🗄️ Migration Alembic

**Arquivo:** `backend/alembic/versions/b2c3d4e5f6a7_add_ordem_reposicao_table.py`

### Upgrade (aplicar migração)

```python
# 1. Adiciona campos em estoques
ALTER TABLE estoques ADD COLUMN estoque_minimo INTEGER;
ALTER TABLE estoques ADD COLUMN estoque_maximo INTEGER;
ALTER TABLE estoques ADD COLUMN ponto_reposicao INTEGER;

# 2. Cria tabela ordens_reposicao
CREATE TABLE ordens_reposicao (
    id INTEGER PRIMARY KEY,
    estoque_id INTEGER FOREIGN KEY REFERENCES estoques.id,
    produto_id INTEGER FOREIGN KEY REFERENCES produtos.id,
    quantidade_solicitada INTEGER NOT NULL,
    quantidade_recebida INTEGER,
    status VARCHAR(50),
    motivo VARCHAR(255),
    observacoes TEXT,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_confirmacao DATETIME,
    data_recebimento DATETIME,
    data_cancelamento DATETIME
);

# 3. Cria índices
CREATE INDEX ix_ordens_reposicao_status ON ordens_reposicao(status);
CREATE INDEX ix_ordens_reposicao_estoque_id ON ordens_reposicao(estoque_id);
CREATE INDEX ix_ordens_reposicao_produto_id ON ordens_reposicao(produto_id);
CREATE INDEX ix_ordens_reposicao_data_criacao ON ordens_reposicao(data_criacao);
```

### Downgrade (reverter migração)

Remove tabela `ordens_reposicao` e campos de `estoques`.

---

## 🧪 Testes Implementados

**Arquivo:** `backend/tests/test_reposicao.py`

### Classe: `TestReposicaoAutomatica`

#### 1. `test_criar_ordem_reposicao_manual`
- ✅ Valida criação de ordem manual
- Verifica campo `motivo = "manual"`
- Status inicial = PENDENTE

#### 2. `test_verificar_estoques_abaixo_minimo`
- ✅ Valida criação automática de ordem
- Quantidade solicitada = estoque_maximo - quantidade_atual
- Motivo = "automática"

#### 3. `test_nao_criar_ordem_duplicada`
- ✅ Valida que não cria ordens duplicadas
- Segunda execução retorna lista vazia
- Previne múltiplas ordens para mesmo estoque

#### 4. `test_confirmando_ordem`
- ✅ Transição de status PENDENTE → CONFIRMADA
- Registra `data_confirmacao`

#### 5. `test_receber_ordem_completa`
- ✅ Recebimento completo de ordem
- Atualiza estoque.quantidade corretamente
- Status → RECEBIDA

#### 6. `test_receber_ordem_parcial`
- ✅ Recebimento parcial (20 de 50)
- Estoque atualizado com quantidade recebida
- Status não muda para RECEBIDA

#### 7. `test_cancelar_ordem`
- ✅ Cancelamento de ordem
- Registra `data_cancelamento`
- Motivo adicionado a `observacoes`

#### 8. `test_obter_ordens_pendentes`
- ✅ Filtragem de ordens por status
- Retorna apenas PENDENTE e CONFIRMADA
- Exclui RECEBIDA

---

## 📁 Estrutura de Arquivos Criados/Modificados

### ✅ Novos Arquivos Criados

| Arquivo | Linhas | Descrição |
|---------|--------|-----------|
| `app/models/ordem_reposicao.py` | ~50 | Modelo ORM com status enum |
| `app/schemas/ordem_reposicao.py` | ~80 | 4 schemas de validação |
| `app/utils/reposicao.py` | ~200 | 7 funções de negócio |
| `app/routes/reposicao.py` | ~250 | 7 endpoints RESTful |
| `frontend/src/pages/ReposicaoPage.jsx` | ~350 | Interface completa de UI |
| `alembic/versions/b2c3d4e5f6a7_*.py` | ~100 | Migration Alembic |
| `tests/test_reposicao.py` | ~280 | 8 casos de teste |

**Total de Novo Código:** ~1.310 linhas

### 🔄 Arquivos Modificados

| Arquivo | Mudanças |
|---------|----------|
| `app/models/estoque.py` | +3 campos (estoque_minimo, estoque_maximo, ponto_reposicao) |
| `app/schemas/estoque.py` | +3 campos em schemas |
| `app/models/__init__.py` | +2 exports (OrdemReposicao, StatusOrdemReposicao) |
| `app/utils/scheduler.py` | +1 job (verificar_estoques_minimos a cada 30min) |
| `app/main.py` | +1 import rota + 1 include_router |
| `frontend/src/App.jsx` | +1 import ReposicaoPage + 1 rota protegida |
| `frontend/src/components/layout/Sidebar.jsx` | +1 item nav (Reposição 🔄) |

**Total de Linhas Modificadas:** ~40 linhas

---

## 🚀 Instruções de Deployment

### 1. Aplicar Migration no Banco

```bash
cd backend

# Atualizar para última versão
alembic upgrade head

# Verificar status
alembic current
```

**Saída esperada:**
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL is supported by backend
INFO  [alembic.runtime.migration] Running upgrade a1b2c3d4e5f6 -> b2c3d4e5f6a7, add_ordem_reposicao_table
```

### 2. Instalar Dependências (se necessário)

```bash
# Backend - APScheduler já foi adicionado em TASK-1C
pip install -r requirements.txt

# Frontend - sem novas dependências
cd ../frontend
npm install  # Já tem todas as dependências
```

### 3. Reiniciar Aplicação

```bash
# Backend
cd backend
python -m uvicorn app.main:app --reload

# Frontend (em outro terminal)
cd frontend
npm run dev
```

### 4. Verificar Scheduler

**Logs esperados ao iniciar:**
```
INFO: Scheduler iniciado com sucesso
INFO: Job verificar_alertas_validade agendado para cada 15 minutos
INFO: Job verificar_alertas_temperatura agendado para cada 15 minutos
INFO: Job verificar_estoques_minimos agendado para cada 30 minutos
```

### 5. Testar Manualmente

**No arquivo `conftest.py`, os testes já usam fixtures preparadas:**

```bash
cd backend
pytest tests/test_reposicao.py -v
```

---

## 🔐 Segurança - RBAC

### Permissões por Papel

| Endpoint | Admin | Gerente | Caixa | Vendedor |
|----------|-------|---------|-------|----------|
| GET /api/reposicao/ | ✅ | ✅ | ❌ | ❌ |
| POST /api/reposicao/ | ✅ | ✅ | ❌ | ❌ |
| PUT /reposicao/{id}/confirmar | ✅ | ✅ | ❌ | ❌ |
| PUT /reposicao/{id}/receber | ✅ | ✅ | ❌ | ❌ |
| DELETE /reposicao/{id} | ✅ | ✅ | ❌ | ❌ |

**Implementação:**
```python
@require_gerente  # Decorador verifica: user.role in [gerente, admin]
async def endpoint(...):
    # Conteúdo
```

---

## 📊 Dashboard Frontend

### Componentes Renderizados

1. **Cards de Resumo**
   - Ordens Pendentes/Confirmadas (cor laranja)
   - Ordens Recebidas (últimos 7 dias, cor verde)
   - Quantidade Total Pendente (cor azul)
   - Quantidade Total Recebida (cor cinza)

2. **Filtro de Status**
   - Dropdown com opções: Todos, Pendente, Confirmada, Recebida, Cancelada

3. **Grid de Ordens**
   - Cards responsivos mostrando:
     - Status com badge colorido
     - ID da ordem
     - Produto e Motivo
     - Quantidades (solicitado vs recebido)
     - Observações
     - Botões de ação contextual
     - Data de criação

4. **Ações Contextais**
   - Status PENDENTE: Botões [Confirmar] [Cancelar]
   - Status CONFIRMADA: Botão [Registrar Recebimento]
   - Status RECEBIDA/CANCELADA: Sem ações

---

## 📝 Logs - Exemplos

### Sucesso

```json
{
  "timestamp": "2026-04-19T10:15:32.123Z",
  "level": "INFO",
  "message": "Usuário 5 criou ordem de reposição 42",
  "event": "ordem_criada",
  "user_id": 5,
  "ordem_id": 42
}
```

### Operação Automática

```json
{
  "timestamp": "2026-04-19T10:30:00.000Z",
  "level": "INFO",
  "message": "Job verificar_estoques_minimos executado: 3 ordens de reposição criadas",
  "event": "job_reposicao",
  "ordens_criadas": 3
}
```

### Erro

```json
{
  "timestamp": "2026-04-19T10:35:45.789Z",
  "level": "ERROR",
  "message": "Erro ao verificar estoques mínimos: Database connection timeout",
  "event": "job_error",
  "exception": "timeout"
}
```

---

## ✅ Checklist de Validação

- [x] Todos os arquivos criados com sintaxe válida
- [x] Imports verificados e funcionais
- [x] Migration Alembic criada e pronta para upgrade
- [x] Job scheduler adicionado (30 minutos)
- [x] Rotas integradas em main.py
- [x] Frontend Page criada com UI completa
- [x] Link de navegação adicionado
- [x] Testes implementados
- [x] RBAC aplicado (require_gerente)
- [x] Logging estruturado em todas as operações
- [x] Documentação completa (este arquivo)

---

## 🎯 Métricas de Sucesso

| Métrica | Target | Status |
|---------|--------|--------|
| Requisito RF-06 Coverage | 100% | ✅ |
| Endpoints Implementados | 7/7 | ✅ |
| Linhas de Código | ~1.350 | ✅ |
| Testes Implementados | 8/8 | ✅ |
| Migration Status | Ready | ✅ |
| Scheduler Job | Integrado | ✅ |
| RBAC Compliance | 100% | ✅ |
| Frontend Integration | Completa | ✅ |

---

## 🔗 Referências

- **ROADMAP:** `ROADMAP_SPRINT_FINAL.md` - Task 1B
- **Task 1C:** `docs/TASK_1C_ALERTAS_COMPLETA.md` - Padrão arquitetural
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Banco de Dados:** SQLite com Alembic migrations
- **Scheduler:** APScheduler 3.10.4

---

## 📞 Suporte

Para dúvidas sobre implementação, consultar:
- Estrutura de logs em `app/core/logging.py`
- Decoradores RBAC em `app/api/deps.py`
- Padrões de schemas em `app/schemas/`
- Testes em `tests/test_reposicao.py`
