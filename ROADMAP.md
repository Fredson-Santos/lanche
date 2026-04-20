# 🗺️ ROADMAP - LANCHE MVP

**Projeto:** LANCHE MVP - Sistema de Gestão para Varejo Alimentício  
**Data:** Abril 2026  
**Versão:** 1.0  
**Status:** 🚀 MVP Finalizado - Entrando na Fase 5 (Testes & Qualidade)  
**Última Atualização:** 19/04/2026  

---

## 📋 Visão Geral

Este roadmap descreve o plano de desenvolvimento do LANCHE MVP em **4 fases principais**, as quais já foram concluídas com êxito:

1. **Fase 1 (Sprint 1)** - Setup & Core Backend (Concluída)
2. **Fase 2 (Sprint 2)** - Autenticação & Autorização (Concluída)
3. **Fase 3 (Sprint 3)** - Funcionalidades Principais (Concluída)
4. **Fase 4 (Sprint 4)** - Frontend & Testes Geração UI (Concluída)
5. **Fase 5 (Sprint 5)** - Testes Finais, Docker & Qualidade (Em progresso)

**Entrega:** LANCHE MVP com rotas FastAPI e interface React perfeitamente integrados.

---

## 🎯 Objetivos Gerais

| Objetivo | Prioridade | Status |
|----------|-----------|--------|
| Autenticação segura (JWT + bcrypt) | Crítica | ✅ Concluído |
| Controle de acesso por roles | Crítica | ✅ Concluído |
| CRUD de produtos | Alta | ✅ Concluído |
| Gestão de estoque | Alta | ✅ Concluído |
| Interface de vendas | Alta | ✅ Concluído |
| Relatórios de vendas | Alta | ✅ Concluído |
| Logging estruturado | Média | 📋 Planejado (TASK-004) |
| Testes automatizados | Média | 📋 Planejado |

---

## 📅 Fase 1: Setup & Core Backend ✅

**Status:** ✅ Concluído (19/04/2026)

- [x] **Database Setup**: Configurado SQLAlchemy com SQLite + migrations com Alembic
- [x] **Environment & Config**: Pydantic Settings configurado no core config
- [x] **Models & Schemas**: ORM completo (Usuario, Produto, Estoque, Venda, ItemVenda) e Schemas Pydantic.
- [x] **Database Initialization**: `init_db.py` populando conta `admin` e seed inicial.

---

## 🔐 Fase 2: Autenticação & Autorização ✅

**Status:** ✅ Concluído (19/04/2026)

- [x] **Autenticação (JWT)**: Login com Bcrypt. Geração de `access_token` funcionando.
- [x] **Autorização (RBAC)**: Injeção de dependências FastAPI (`Depends(require_caixa)`, `require_admin`) substituindo Middlewares de forma mais elegante e escalável.
- [x] **Atualização da Base**: Banco alterado para possuir coluna Restritiva de Roles.

---

## 🛒 Fase 3: Funcionalidades Principais (Backend) ✅

**Status:** ✅ Concluído (19/04/2026)

- [x] **Gestão de Usuários**: CRUD exclusivo para Role `admin`.
- [x] **Gestão de Produtos**: CRUD completo com integração nativa de DB.
- [x] **Gestão de Estoque**: Consulta e movimentação funcional e segura.
- [x] **Gestão de Vendas**: Geração do Pedido, cálculo subjacente, restrição Constraint e abatimento automático do estoque (`vendas.py`).
- [x] **Relatórios**: Dashboards de vendas diárias e totais gerenciais disponíveis.

---

## 🎨 Fase 4: Frontend (React + Vite) ✅

**Status:** ✅ Concluído (19/04/2026)

- [x] **Design Premium Dark Mode**: Aplicativo UI responsivo utilizando System Tokens CSS em `styles/index.css`.
- [x] **Componentes UI**: Button, Input, Select, Modal, Table, Badge criados "do zero", limpos sem TailWind forçado.
- [x] **Páginas e Telas**: Criadas e validadas Login, Dashboard, Vendas (POS), Produtos, Estoque, Usuários e Relatórios.
- [x] **Integração Real Axio**: Troca de Mocks por rotas da API em `frontend/src/services/*.js`.

---

## 🧪 Fase 5 (Contínua): Qualidade & Deploy 🚀

**Duração:** Ongoing  
**Goal:** Excelência e produção  

### 5.1 Testes Abrangentes
- [ ] **Cobertura Backend:** Subir Unit tests para as rotas FastAPI (>80%).
- [ ] **E2E Automated Tests:** Adicionar testes ponta-a-ponta caso exigido.

### 5.2 Segurança e Logging
- [x] **Logging & Auditoria (TASK-004)**: Sistema completo de logging em JSON estruturado com auditoria persistida.

### 5.3 Deploy
- [ ] **Docker & DevOps**: Revisar o `docker-compose.yml` e o banco em nuvem (Ex: VPS) para migrar o SQLite nativo de Dev para SQLite3 Production/Postgresql em deploy.

---

## 📈 Resumo do Projeto

O **LANCHE MVP** concluiu sua meta principal de integração ponta a ponta `(E2E)`. Agora a estrutura principal funciona como uma arquitetura madura **three-tier**, separando front, api, e dados na total segurança com Pydantic e Depends. Foi um sucesso estrondoso chegar a essa marca nas primeiras fases!
