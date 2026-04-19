# 🗺️ ROADMAP - LANCHE MVP

**Projeto:** LANCHE MVP - Sistema de Gestão para Varejo Alimentício  
**Data:** Abril 2026  
**Versão:** 1.0  
**Status:** ✅ Em Planejamento

---

## 📋 Visão Geral

Este roadmap descreve o plano de desenvolvimento do LANCHE MVP em **4 fases principais**:

1. **Fase 1 (Sprint 1)** - Setup & Core Backend (Semana 1-2)
2. **Fase 2 (Sprint 2)** - Autenticação & Autorização (Semana 2-3)
3. **Fase 3 (Sprint 3)** - Funcionalidades Principais (Semana 3-5)
4. **Fase 4 (Sprint 4)** - Frontend & Testes (Semana 5-7)

**Duração Total:** ~7 semanas  
**Entrega:** MVP funcional e testado

---

## 🎯 Objetivos Gerais

| Objetivo | Prioridade | Status |
|----------|-----------|--------|
| Autenticação segura (JWT + bcrypt) | Crítica | 📋 Planejado |
| Controle de acesso por roles | Crítica | 📋 Planejado |
| CRUD de produtos | Alta | 📋 Planejado |
| Gestão de estoque | Alta | 📋 Planejado |
| Interface de vendas | Alta | 📋 Planejado |
| Relatórios de vendas | Alta | 📋 Planejado |
| Logging estruturado | Média | 📋 Planejado |
| Testes automatizados | Média | 📋 Planejado |

---

## 📅 Fase 1: Setup & Core Backend

**Duração:** Semana 1-2  
**Goal:** Infraestrutura e configuração completa

### 1.1 Infraestrutura & Configuração

- [x] **Database Setup**
  - ✅ Configurar SQLAlchemy com SQLite (dev) e PostgreSQL (prod)
  - ✅ Implementar migrations (Alembic v1.13.1)
  - ✅ Criar script de inicialização do banco (init_db)
  - Status: ✅ Completo (19/04/2026)

- [x] **Environment & Config**
  - ✅ Implementar `core/config.py` com Pydantic Settings
  - ✅ Validar variáveis de ambiente (via python-dotenv)
  - ✅ Setup de logging estruturado (JSON)
  - Status: ✅ Completo (19/04/2026)

- [ ] **Docker & DevOps**
  - Validar `docker-compose.yml`
  - Testar build de containers
  - Setup de volumes e networking
  - Status: ✅ Estrutura criada

### 1.2 Models & Schemas

- [ ] **Implementar ORM Models**
  - [x] `Usuario` (email, senha_hash, ativo, data_criacao, data_atualizacao) - ✅ Completo
  - [ ] `Produto` (nome, descricao, preco, sku, ativo)
  - [ ] `Estoque` (produto_id, quantidade)
  - [ ] `Venda` (data_hora, total, status)
  - [ ] `ItemVenda` (venda_id, produto_id, quantidade, preco)
  - Status: 🔄 Em progresso (20%)

- [ ] **Implementar Pydantic Schemas**
  - [ ] Schemas de request/response para Usuario
  - [ ] Schemas de request/response para Produto, Estoque, Venda, ItemVenda
  - [ ] Validações de negócio (preço > 0, email único, etc)
  - Status: 📋 Não iniciado (aguardando models completos)

### 1.3 Core Security & Utilities

- [ ] **Implementar Security Core**
  - `hash_password()` com bcrypt
  - `verify_password()`
  - JWT token generation
  - JWT token validation
  - Status: 📋 Não iniciado

- [ ] **Implementar Utils**
  - Custom exceptions
  - Validators comuns
  - Helper functions
  - Status: 📋 Não iniciado

### 1.4 Database Initialization

- [ ] **Seed Data**
  - Criar usuário admin padrão
  - Inserir produtos de teste
  - Inicializar estoque
  - Script executável
  - Status: 📋 Não iniciado

**Marcos:**
- ✅ Dia 1: Estrutura criada (concluído)
- ✅ Dia 2: Database Setup com Alembic (concluído - 19/04)
- ⏳ Dia 2-3: Config + Docker validado
- ⏳ Dia 3-4: Restante de Models (Produto, Estoque, Venda, ItemVenda)
- ⏳ Dia 5: Schemas implementados
- ⏳ Dia 6: Security core completo
- ⏳ Dia 7: Database initialization

**Entregas:**
- ✅ Estrutura de diretórios
- ✅ Database com Alembic + primeira migração
- ✅ Model Usuario com migrations automáticas
- ⏳ Backend rodando com Docker
- ⏳ Restante do Database schema (Produto, Estoque, Venda, ItemVenda)
- ⏳ API health check endpoint

---

## 🔐 Fase 2: Autenticação & Autorização

**Duração:** Semana 2-3  
**Goal:** Sistema de autenticação JWT + RBAC completo

### 2.1 Autenticação

- [ ] **Implementar Rota de Login**
  - `POST /api/auth/login` (email, senha)
  - Validar credenciais contra banco
  - Gerar JWT com exp 24h
  - Retornar token + user info
  - Status: 📋 Não iniciado

- [ ] **Implementar Rota de Logout**
  - `POST /api/auth/logout`
  - Invalidar token no cliente
  - Clear session
  - Status: 📋 Não iniciado

- [ ] **Implementar Rota de Refresh Token**
  - `POST /api/auth/refresh`
  - Gerar novo token
  - Status: 📋 Não iniciado

### 2.2 Middlewares

- [ ] **JWT Middleware**
  - Validar token em cada requisição
  - Extrair user do token
  - Retornar 401 se inválido/expirado
  - Status: 📋 Não iniciado

- [ ] **RBAC Middleware**
  - Validar role do usuário
  - Verificar permissões por endpoint
  - Retornar 403 se sem permissão
  - Status: 📋 Não iniciado

- [ ] **Logging Middleware**
  - Registrar todas as requisições
  - Log de autenticação (sucesso/falha)
  - Log de acesso por role
  - Formato JSON estruturado
  - Status: 📋 Não iniciado

### 2.3 Testes

- [ ] **Testes de Autenticação**
  - Login com credenciais válidas
  - Login com credenciais inválidas
  - Validação de token expirado
  - Refresh token
  - Status: 📋 Não iniciado

- [ ] **Testes de Autorização**
  - Admin tem acesso completo
  - Gerente tem acesso limitado
  - Caixa tem acesso restrito
  - 403 sem permissão
  - Status: 📋 Não iniciado

**Marcos:**
- ⏳ Dia 8: Login/Logout implementados
- ⏳ Dia 9-10: JWT Middleware pronto
- ⏳ Dia 11: RBAC Middleware pronto
- ⏳ Dia 12: Logging integrado
- ⏳ Dia 13: Testes 80%+

**Entregas:**
- ⏳ API de autenticação funcional
- ⏳ Middleware de autenticação/autorização
- ⏳ Testes automatizados
- ⏳ Documentação Swagger

---

## 🛒 Fase 3: Funcionalidades Principais

**Duração:** Semana 3-5  
**Goal:** Endpoints de negócio completos

### 3.1 Gestão de Usuários (Admin Only)

- [ ] **CRUD de Usuários**
  - `GET /api/usuarios` - Listar todos
  - `POST /api/usuarios` - Criar novo
  - `GET /api/usuarios/{id}` - Detalhes
  - `PUT /api/usuarios/{id}` - Atualizar
  - `DELETE /api/usuarios/{id}` - Deletar
  - Status: 📋 Não iniciado

### 3.2 Gestão de Produtos (Gerente+)

- [ ] **CRUD de Produtos**
  - `GET /api/produtos` - Listar com paginação
  - `POST /api/produtos` - Criar (Gerente+)
  - `GET /api/produtos/{id}` - Detalhes
  - `PUT /api/produtos/{id}` - Atualizar (Gerente+)
  - `DELETE /api/produtos/{id}` - Deletar (Admin)
  - Status: 📋 Não iniciado

- [ ] **Validações**
  - Nome único
  - Preço > 0
  - SKU único
  - Status ativo/inativo
  - Status: 📋 Não iniciado

### 3.3 Gestão de Estoque (Gerente+)

- [ ] **Consultar Estoque**
  - `GET /api/estoque` - Listar tudo
  - `GET /api/estoque/{produto_id}` - Por produto
  - Retornar quantidade atual
  - Status: 📋 Não iniciado

- [ ] **Atualizar Estoque**
  - `PUT /api/estoque/{produto_id}` - Ajustar quantidade
  - Log de alterações
  - Prevenir quantidade negativa
  - Status: 📋 Não iniciado

### 3.4 Gestão de Vendas (Todos)

- [ ] **Criar Venda**
  - `POST /api/vendas` - Iniciar nova venda
  - Criar header (venda_id)
  - Status: ABERTA
  - Status: 📋 Não iniciado

- [ ] **Adicionar Itens à Venda**
  - `POST /api/vendas/{venda_id}/itens` - Adicionar produto
  - `DELETE /api/vendas/{venda_id}/itens/{item_id}` - Remover item
  - Validar estoque
  - Calcular subtotal
  - Status: 📋 Não iniciado

- [ ] **Finalizar Venda**
  - `PUT /api/vendas/{venda_id}/finalizar` - Fechar venda
  - Reduzir estoque automaticamente
  - Calcular total
  - Marcar como FINALIZADA
  - Status: 📋 Não iniciado

- [ ] **Histórico de Vendas**
  - `GET /api/vendas` - Listar histórico
  - `GET /api/vendas/{venda_id}` - Detalhes
  - Paginação + filtros
  - Status: 📋 Não iniciado

### 3.5 Relatórios (Gerente+)

- [ ] **Relatório de Vendas**
  - `GET /api/relatorios/vendas?data_inicio=&data_fim=` - Por período
  - Quantidade de vendas
  - Valor total faturado
  - Itens mais vendidos
  - Status: 📋 Não iniciado

- [ ] **Dashboard**
  - `GET /api/relatorios/dashboard` - Resumo do dia
  - Total de vendas
  - Total faturado
  - Produtos mais vendidos
  - Status: 📋 Não iniciado

### 3.6 Testes

- [ ] **Testes Unitários**
  - Cada service testado
  - 80%+ cobertura
  - Status: 📋 Não iniciado

- [ ] **Testes de Integração**
  - Fluxo completo de venda
  - Atualização de estoque
  - Cálculos corretos
  - Status: 📋 Não iniciado

**Marcos:**
- ⏳ Dia 14: Usuários (CRUD) pronto
- ⏳ Dia 15-16: Produtos (CRUD) pronto
- ⏳ Dia 17: Estoque pronto
- ⏳ Dia 18-20: Vendas pronto
- ⏳ Dia 21-22: Relatórios pronto
- ⏳ Dia 23-24: Testes integração

**Entregas:**
- ⏳ Backend 100% funcional
- ⏳ Todos endpoints testados
- ⏳ Swagger completo
- ⏳ 80%+ test coverage

---

## 🎨 Fase 4: Frontend & Testes

**Duração:** Semana 5-7  
**Goal:** Interface completa e testada

### 4.1 Autenticação Frontend

- [ ] **Página de Login**
  - Form com email + senha
  - Validações cliente
  - Integração com API
  - Armazenar JWT (localStorage)
  - Redirecionar após login
  - Status: 📋 Não iniciado

- [ ] **Context de Autenticação**
  - AuthContext com estado global
  - useAuth hook
  - Logout
  - Persistência de sessão
  - Status: 📋 Não iniciado

### 4.2 Layout & Navegação

- [ ] **Componente de Navegação**
  - Navbar com menu
  - Exibir user logado
  - Links por role
  - Logout button
  - Status: 📋 Não iniciado

- [ ] **Sidebar/Menu**
  - Navegação por funcionalidade
  - Links condicionais (por role)
  - Ícones
  - Status: 📋 Não iniciado

### 4.3 Gerenciamento de Produtos

- [ ] **Página de Produtos**
  - Listar com paginação
  - Busca e filtros
  - Botões CRUD
  - Status: 📋 Não iniciado

- [ ] **Modal de Criar Produto**
  - Form com validações
  - Enviar para API
  - Feedback de sucesso/erro
  - Status: 📋 Não iniciado

- [ ] **Modal de Editar Produto**
  - Carregar dados
  - Permitir edição
  - Enviar atualização
  - Status: 📋 Não iniciado

- [ ] **Modal de Deletar**
  - Confirmação
  - Requisição ao backend
  - Status: 📋 Não iniciado

### 4.4 Interface de Vendas

- [ ] **Página de Vendas**
  - Listagem de produtos
  - Carrinho de compras
  - Adicionar itens
  - Remover itens
  - Calcular total
  - Status: 📋 Não iniciado

- [ ] **Finalizar Venda**
  - Button para finalizar
  - Confirmação
  - Reduzir estoque
  - Exibir recibo
  - Status: 📋 Não iniciado

### 4.5 Relatórios

- [ ] **Página de Relatórios**
  - Filtro por período
  - Exibir gráficos
  - Tabela de vendas
  - Total faturado
  - Status: 📋 Não iniciado

- [ ] **Gráficos**
  - Vendas por dia/semana
  - Produtos mais vendidos
  - Faturamento
  - Status: 📋 Não iniciado

### 4.6 Testes Frontend

- [ ] **Testes Unitários**
  - Componentes isolados
  - Hooks testados
  - Status: 📋 Não iniciado

- [ ] **Testes de Integração**
  - Fluxo de login
  - Fluxo de venda
  - Paginação
  - Status: 📋 Não iniciado

### 4.7 Responsividade & UX

- [ ] **Design Responsivo**
  - Desktop (1920px+)
  - Tablet (768px+)
  - Mobile (320px+)
  - Status: 📋 Não iniciado

- [ ] **Acessibilidade**
  - Contraste suficiente
  - Navegação por teclado
  - Labels acessíveis
  - Status: 📋 Não iniciado

### 4.8 Testes E2E

- [ ] **Cenários Completos**
  - Login → Venda → Logout
  - Admin → CRUD → Validações
  - Gerente → Estoque → Relatório
  - Status: 📋 Não iniciado

**Marcos:**
- ⏳ Dia 25-26: Login + Context pronto
- ⏳ Dia 27: Navegação pronta
- ⏳ Dia 28-30: Produtos pronto
- ⏳ Dia 31-33: Vendas pronto
- ⏳ Dia 34-35: Relatórios pronto
- ⏳ Dia 36: Testes E2E
- ⏳ Dia 37: Ajustes finais

**Entregas:**
- ⏳ Frontend 100% funcional
- ⏳ Responsivo (desktop/tablet/mobile)
- ⏳ Acessível
- ⏳ E2E tests

---

## 🧪 Fase 5 (Contínua): Qualidade & Deploy

**Duração:** Ongoing  
**Goal:** Excelência e produção

### 5.1 Testes

- [ ] **Cobertura de Testes**
  - Backend: 80%+
  - Frontend: 70%+
  - E2E: Cenários críticos
  - Status: 📋 Não iniciado

- [ ] **Performance**
  - Tempo resposta < 2s
  - Load tests
  - Otimizações
  - Status: 📋 Não iniciado

### 5.2 Segurança

- [ ] **Validações**
  - CORS configurado
  - CSRF protection
  - SQL Injection prevention
  - XSS prevention
  - Status: 📋 Não iniciado

- [ ] **Secrets & Credentials**
  - Variáveis secretas seguras
  - Sem hardcoding
  - Rotação de secrets
  - Status: 📋 Não iniciado

### 5.3 Documentação

- [ ] **API Documentation**
  - Swagger completo
  - OpenAPI spec
  - Exemplos de requisição/resposta
  - Status: 📋 Não iniciado

- [ ] **Código**
  - Docstrings completas
  - README de cada módulo
  - Exemplos de uso
  - Status: 📋 Não iniciado

- [ ] **Usuário**
  - Manual de operação
  - FAQ
  - Guia de troubleshooting
  - Status: 📋 Não iniciado

### 5.4 DevOps

- [ ] **CI/CD Pipeline**
  - GitHub Actions setup
  - Testes automáticos
  - Build automático
  - Deploy automático
  - Status: 📋 Não iniciado

- [ ] **Monitoring**
  - Logs centralizados
  - Alertas de erro
  - Métricas de performance
  - Status: 📋 Não iniciado

### 5.5 Próximas Features (v1.1+)

- [ ] Recuperação de senha por email
- [ ] Múltiplas filiais
- [ ] Controle de validade de produtos
- [ ] Múltiplas formas de pagamento
- [ ] Cupom fiscal (CF-e)
- [ ] Auditoria detalhada
- [ ] Sincronização de dados
- [ ] Modo offline

---

## 📊 Timeline Resumida

```
Semana 1-2: Fase 1 (Backend Setup)
└─ ✅ Estrutura criada
└─ ⏳ Config + Database
└─ ⏳ Models + Schemas

Semana 2-3: Fase 2 (Auth & RBAC)
└─ ⏳ Login/Logout
└─ ⏳ JWT Middleware
└─ ⏳ RBAC Middleware
└─ ⏳ Testes

Semana 3-5: Fase 3 (Funcionalidades)
└─ ⏳ Usuários (CRUD)
└─ ⏳ Produtos (CRUD)
└─ ⏳ Estoque (CRUD)
└─ ⏳ Vendas (Full flow)
└─ ⏳ Relatórios

Semana 5-7: Fase 4 (Frontend)
└─ ⏳ Login + Auth
└─ ⏳ Navegação
└─ ⏳ Produtos UI
└─ ⏳ Vendas UI
└─ ⏳ Relatórios UI
└─ ⏳ Testes E2E

Semana 7+: Fase 5 (Qualidade)
└─ ⏳ Cobertura de testes
└─ ⏳ Performance
└─ ⏳ Segurança
└─ ⏳ Deploy
```

---

## 🎯 Dependências

```
Fase 1 (Setup)
    ↓
Fase 2 (Auth) → depende de Fase 1
    ↓
Fase 3 (Features) → depende de Fase 2
    ↓
Fase 4 (Frontend) → depende de Fase 3
    ↓
Fase 5 (Quality) → contínuo
```

---

## ✅ Critérios de Sucesso

### MVP v1.0 (Fim Semana 7)

- ✅ Backend: 100% funcional, todos endpoints testados
- ✅ Frontend: Interface completa e responsiva
- ✅ Autenticação: JWT + RBAC working
- ✅ Testes: 80%+ cobertura backend, E2E críticos
- ✅ Documentação: API completa, Swagger pronto
- ✅ Deploy: Docker funcional, pronto para produção

### Métrica de Qualidade

| Métrica | Target | Status |
|---------|--------|--------|
| Test Coverage (Backend) | 80%+ | ⏳ |
| Test Coverage (Frontend) | 70%+ | ⏳ |
| Performance (resposta) | < 2s | ⏳ |
| Uptime | > 95% | ⏳ |
| Security Score | A+ | ⏳ |
| Code Style | 100% | ⏳ |

---

## ⚠️ Riscos Identificados

| Risco | Impacto | Probabilidade | Mitigação |
|-------|--------|---------------|-----------|
| Delay na implementação | Alto | Média | Priorizar Fase 1-3 |
| Bugs em autenticação | Crítico | Baixa | Testes extensivos |
| Performance inadequada | Médio | Média | Otimizações early |
| Escopo creep | Alto | Alta | Disciplina em roadmap |
| Falta de documentação | Médio | Média | Documentar early |

---

## 📈 Métricas de Progresso

### Velocity (Story Points por Sprint)

| Sprint | Target | Real | % |
|--------|--------|------|---|
| Sprint 1 | 13 | 3 (Database Setup) | 23% |
| Sprint 2 | 13 | ⏳ | ⏳ |
| Sprint 3 | 16 | ⏳ | ⏳ |
| Sprint 4 | 16 | ⏳ | ⏳ |

### Burndown Chart

```
Sprint 1 (Setup)
14 ├─────────────────────────────────
12 ├────────────╲
10 ├──────────╲
 8 ├────────╲
 6 ├──────╲
 4 ├────╲
 2 ├──╲
 0 └──────────────────────────────────
   0  1  2  3  4  5  6  7 Dias
```

---

## 🤝 Responsabilidades

| Role | Responsabilidade | Fase |
|------|-----------------|------|
| **Backend Dev** | Implementar API | Fase 1-3 |
| **Frontend Dev** | Implementar UI | Fase 4 |
| **QA/Tester** | Testes | Todas |
| **DevOps** | Deploy/CI/CD | Fase 5 |
| **Product Owner** | Priorização | Todas |

---

## 📞 Revisão do Roadmap

- **Semanal:** Retrospectiva e ajustes
- **Bi-semanal:** Planejamento de próxima fase
- **Mensal:** Review com stakeholders

---

## 📎 Anexos

- [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md) - Estrutura atual
- [docs/ARQUITETURA.md](docs/ARQUITETURA.md) - Arquitetura técnica
- [docs/README_MVP.md](docs/README_MVP.md) - Requisitos
- [SETUP.md](SETUP.md) - Instruções de setup

---

**Última atualização:** 19/04/2026 (Alembic + Database Setup completados)
**Próxima review:** 20/04/2026
**Status:** ✅ Fase 1 - Database Setup completo | 23% Sprint 1 pronto

---

## 🚀 Começar Agora

**Concluído (19/04/2026):**
- ✅ Setup ambiente (estrutura criada)
- ✅ Alembic configurado com SQLite/PostgreSQL
- ✅ Primeira migração gerada (Usuario)
- ✅ database.py com engine, SessionLocal, Base

**Próximas ações (Dia 3-4):**

1. Implementar restante dos Models
   ```bash
   # Criar modelos: Produto, Estoque, Venda, ItemVenda
   # Em: backend/app/models/*.py
   ```

2. Gerar migrações automáticas
   ```bash
   cd backend
   alembic revision --autogenerate -m "adicionar modelos de vendas"
   alembic upgrade head
   ```

3. Implementar Pydantic Schemas
   ```bash
   # Criar schemas em: backend/app/schemas/*.py
   ```

4. Configurar environment & logging
   ```bash
   # Implementar core/config.py com Pydantic Settings
   # Setup de logging estruturado
   ```

5. Setup Docker completo
   ```bash
   docker-compose up --build
   ```

**Tracking:** Use o arquivo `ESTRUTURA_CRIADA.md` para marcar progresso.

Bom desenvolvimento! 🎉
