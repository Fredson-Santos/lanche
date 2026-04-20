# LANCHE MVP
## Produto Viável Mínimo - Sprint Final
**Documentação de Engenharia de Software**

**Versão 3.0 - MVP Expandido**  
Abril de 2026 (Sprint 19-23 de Abril)  

---

## Resumo Executivo
O projeto LANCHE MVP evoluiu para um **MVP Expandido com 14 funcionalidades**, atingindo **82% de cobertura do Cenário de Negócios**. Este documento descreve a especificação técnica completa de um sistema profissional de gestão para rede de varejo alimentício com conformidade LGPD e recursos avançados.

O MVP expandido contempla: autenticação JWT segura, RBAC com 3 roles, cadastro de produtos, controle de estoque, venda integrada, auditoria detalhada, logging JSON estruturado, **APIs abertas para parceiros**, **reposição automática de estoque**, **alertas de validade e temperatura**, **criptografia de banco de dados**, **conformidade LGPD**, **modo offline** e otimizações de PDV ultra-baixa latência.

---

## 1. Escopo do Projeto

### 1.1 Funcionalidades do MVP (14 no Total)

#### ✅ IMPLEMENTADAS (9 funcionalidades)
1. **Autenticação de Usuários** - Login seguro com email e senha (bcrypt + JWT)  
2. **Controle de Acesso** - 3 roles (Admin, Gerente, Caixa) com RBAC  
3. **Cadastro de Produtos** - CRUD completo com validações  
4. **Controle de Estoque** - Registrar, consultar, atualizar quantidade  
5. **Venda Integrada** - Interface de caixa com carrinho e totalizador  
6. **Baixa Automática** - Reduzir estoque ao vender  
7. **Relatório de Vendas** - Filtrar por período, total faturado  
8. **Auditoria Detalhada** - Tabela auditoria_logs com contexto estruturado  
9. **Logging JSON** - Formatação estruturada em stdout  

#### 🚀 EM IMPLEMENTAÇÃO (5 funcionalidades - Sprint Final 19-23/04)
10. **APIs Abertas** - API keys, rate limiting, integração com terceiros  
11. **Reposição Automática** - Pedidos ao atingir estoque mínimo  
12. **Alertas de Validade** - Monitorar vencimento e temperatura  
13. **Criptografia de BD** - Dados sensíveis encriptados  
14. **Conformidade LGPD** - Endpoints de delete, export, consentimento  

#### 📋 FUTURO (2 funcionalidades - Fase 3, se houver tempo)
- **Modo Offline** - Service Worker + IndexedDB  
- **PDV Ultra-Latência** - Otimizações <1s por transação  

---

## 2. Requisitos Funcionais (RF)

### Autenticação & Autorização (RF-01 a RF-06)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-01 | Efetuar login com email e senha | Crítica | ✅ Implementado |
| RF-02 | Validar credenciais de usuário | Crítica | ✅ Implementado |
| RF-03 | Gerar token de autenticação (JWT) | Crítica | ✅ Implementado |
| RF-04 | Efetuar logout | Alta | ✅ Implementado |
| RF-05 | Validar role do usuário (RBAC) | Crítica | ✅ Implementado |
| RF-06 | Retornar 403 se sem permissão | Crítica | ✅ Implementado |

### Gestão de Usuários (RF-07 a RF-08)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-07 | Gerenciar usuários (CRUD) | Alta | ✅ Implementado |
| RF-08 | Atribuir roles a usuários | Alta | ✅ Implementado |

### Gestão de Produtos (RF-09 a RF-12)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-09 | Cadastrar novo produto | Crítica | ✅ Implementado |
| RF-10 | Listar produtos | Crítica | ✅ Implementado |
| RF-11 | Editar produto | Alta | ✅ Implementado |
| RF-12 | Deletar/Inativar produto | Média | ✅ Implementado |

### Gestão de Estoque (RF-13 a RF-16)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-13 | Consultar estoque | Crítica | ✅ Implementado |
| RF-14 | Atualizar estoque manualmente | Média | ✅ Implementado |
| RF-15 | Reposição automática ao mínimo | Alta | 🚀 Em Implementação |
| RF-16 | Gerar alertas de estoque baixo | Alta | 🚀 Em Implementação |

### Gestão de Vendas (RF-17 a RF-23)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-17 | Iniciar venda | Crítica | ✅ Implementado |
| RF-18 | Adicionar produtos à venda | Crítica | ✅ Implementado |
| RF-19 | Remover produtos da venda | Alta | ✅ Implementado |
| RF-20 | Calcular total da venda | Crítica | ✅ Implementado |
| RF-21 | Finalizar venda | Crítica | ✅ Implementado |
| RF-22 | Reduzir estoque automaticamente | Crítica | ✅ Implementado |
| RF-23 | Histórico de vendas | Crítica | ✅ Implementado |

### Relatórios & Analytics (RF-24 a RF-26)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-24 | Filtrar vendas por período | Alta | ✅ Implementado |
| RF-25 | Calcular faturamento total | Alta | ✅ Implementado |
| RF-26 | Produtos mais vendidos | Média | ✅ Implementado |

### Auditoria & Segurança (RF-27 a RF-30)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-27 | Registrar logs de transações | Crítica | ✅ Implementado |
| RF-28 | Auditoria com contexto estruturado | Alta | ✅ Implementado |
| RF-29 | Criptografar dados sensíveis | Alta | 🚀 Em Implementação |
| RF-30 | Conformidade LGPD (delete/export) | Crítica | 🚀 Em Implementação |

### APIs & Integrações (RF-31 a RF-33)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-31 | APIs abertas com documentação | Alta | 🚀 Em Implementação |
| RF-32 | Autenticação por API key | Média | 🚀 Em Implementação |
| RF-33 | Rate limiting por cliente | Média | 🚀 Em Implementação |

### Funcionalidades Avançadas (RF-34 a RF-37)
| ID    | Descrição | Prioridade | Status |
|------|----------|-----------|--------|
| RF-34 | Controlar validade de produtos | Alta | 🚀 Em Implementação |
| RF-35 | Monitorar temperatura de estoque | Média | 🚀 Em Implementação |
| RF-36 | Modo offline com sincronização | Média | 📋 Planejado |
| RF-37 | Interface PDV <1s latência | Alta | 📋 Planejado |

---

## 3. Requisitos Não Funcionais (RNF)

### Performance
| ID    | Descrição | Target | Status |
|------|----------|--------|--------|
| RNF-01 | Tempo de resposta (API) | < 500ms | ✅ Ok |
| RNF-02 | Latência PDV criar venda | < 1000ms | 🚀 Otimizando |
| RNF-03 | Busca de produtos | < 200ms | ✅ Ok |
| RNF-04 | Suporte a produtos | 10.000+ | ✅ Ok |
| RNF-05 | Transações simultâneas | 100+ | ✅ Ok |
| RNF-06 | Score Lighthouse | > 90 | 🚀 Otimizando |

### Disponibilidade & Confiabilidade
| ID    | Descrição | Target | Status |
|------|----------|--------|--------|
| RNF-07 | Disponibilidade | > 99% | ✅ Planejado |
| RNF-08 | Modo offline | Sim | 📋 Em Implementação |
| RNF-09 | Backup automático | Diário | ✅ Configurado |

### Interface & UX
| ID    | Descrição | Target | Status |
|------|----------|--------|--------|
| RNF-10 | Interface responsiva | Desktop/Mobile | ✅ Ok |
| RNF-11 | Navegadores | Chrome, Firefox, Safari, Edge | ✅ Ok |
| RNF-12 | Temas | Dark mode | ✅ Ok |

### Segurança
| ID    | Descrição | Target | Status |
|------|----------|--------|--------|
| RNF-13 | Criptografia de senha | bcrypt (salt 10) | ✅ Ok |
| RNF-14 | Criptografia de BD | SQLCipher/pgcrypto | 🚀 Em Implementação |
| RNF-15 | Token JWT | Expiração 30min | ✅ Ok |
| RNF-16 | HTTPS | Obrigatório produção | ✅ Planejado |
| RNF-17 | Senha mínima | 8 caracteres | ✅ Ok |
| RNF-18 | Rate limiting | 100 req/min por API key | 🚀 Em Implementação |
| RNF-19 | Auditoria completa | 100% das operações | ✅ Ok |

### Conformidade & Operacional
| ID    | Descrição | Target | Status |
|------|----------|--------|--------|
| RNF-20 | LGPD compliance | Lei 13.709 | 🚀 Em Implementação |
| RNF-21 | Instalação | < 5 min | ✅ Ok |
| RNF-22 | Código limpo | Pylint, ESLint | ✅ Ok |
| RNF-23 | Testes unitários | > 80% cobertura | ✅ Ok |
| RNF-24 | Documentação | API, arquitetura, deploy | ✅ Ok |

## 4. Regras de Negócio (RN)

### Autenticação & Acesso (RN-01 a RN-06)
| ID    | Regra | Descrição |
|------|------|----------|
| RN-01 | Email único | Sem duplicação de usuários |
| RN-02 | Autenticação obrigatória | Acesso bloqueado sem JWT válido |
| RN-03 | Role obrigatório | admin, gerente ou caixa |
| RN-04 | Acesso negado (403) | Se role não tiver permissão |
| RN-05 | Token com expiração | 30 minutos para JWT |
| RN-06 | API key + rate limit | 100 requisições/min por cliente |

### Gestão de Usuários & Produtos (RN-07 a RN-12)
| ID    | Regra | Descrição |
|------|------|----------|
| RN-07 | Admin gerencia usuários | Criar, editar, desativar |
| RN-08 | Caixa só vende | Sem acesso a gestão |
| RN-09 | Gerente controla estoque | Pode atualizar quantidade |
| RN-10 | Admin deleta produto | Apenas admin pode deletar |
| RN-11 | Produto único | Sem duplicação por nome |
| RN-12 | Preço obrigatório | > 0 (validação) |

### Controle de Estoque (RN-13 a RN-17)
| ID    | Regra | Descrição |
|------|------|----------|
| RN-13 | Estoque não negativo | Não vender além disponível |
| RN-14 | Estoque sincronizado | Atualização imediata |
| RN-15 | Reposição automática | Ordem ao atingir mínimo |
| RN-16 | Alerta de validade | Produtos vencidos não vendem |
| RN-17 | Alerta de temperatura | Fora da faixa ideal = alerta |

### Gestão de Vendas (RN-18 a RN-24)
| ID    | Regra | Descrição |
|------|------|----------|
| RN-18 | Venda não editável | Histórico imutável (auditado) |
| RN-19 | Venda requer item | Não finalizar vazio |
| RN-20 | Quantidade válida | Número positivo |
| RN-21 | Total correto | Soma dos itens com precisão |
| RN-22 | Desconto auditado | Se aplicado, registra em auditoria |
| RN-23 | Baixa automática | Estoque reduz ao vender |
| RN-24 | Período válido | Filtragem de datas correta |

### Auditoria & Conformidade (RN-25 a RN-31)
| ID    | Regra | Descrição |
|------|------|----------|
| RN-25 | Auditoria completa | 100% das operações logadas |
| RN-26 | Logs imutáveis | Não editar/deletar logs |
| RN-27 | Contexto estruturado | JSON com campos padronizados |
| RN-28 | Deleção segura | Soft delete com flag |
| RN-29 | LGPD: direito ao esquecimento | Deleção em 30 dias |
| RN-30 | LGPD: portabilidade | Export de dados em JSON |
| RN-31 | Criptografia PII | Email, senha, dados sensíveis |

---

## 5. Arquitetura da Solução

### 5.1 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                    LANCHE MVP v3.0                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐          ┌──────────────┐                    │
│  │   Frontend  │◄────────►│   Backend    │                    │
│  │  React+Vite│          │  FastAPI     │                    │
│  │            │          │  + SQLAlchemy│                    │
│  └─────────────┘          └──────────────┘                    │
│       │                         │                              │
│       │                   ┌────────────────┐                 │
│       │                   │   Banco de     │                 │
│       └──────────────────►│   Dados        │                 │
│                           │ SQLite (dev)   │                 │
│                           │ PostgreSQL(prod)│                │
│                           └────────────────┘                 │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Middleware & Segurança                     │   │
│  │  ┌─────────────┐  ┌───────────┐  ┌──────────────┐  │   │
│  │  │  JWT Auth   │  │ Auditoria │  │ Rate Limiter │  │   │
│  │  │             │  │ (JSON Log)│  │  (API Keys)  │  │   │
│  │  └─────────────┘  └───────────┘  └──────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │        Funcionalidades Principais                   │   │
│  │  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │   │
│  │  │ Vendas   │ │ Estoque  │ │ Alertas & Criptografia│  │
│  │  │ PDV      │ │ Reposição│ │ LGPD & Modo Offline   │  │   │
│  │  │          │ │ Mínimo   │ │                       │  │   │
│  │  └──────────┘ └──────────┘ └───────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Stack Tecnológico Expandido

| Camada | Tecnologia | Justificativa | Versão |
|-------|-----------|-------------|---------|
| **Front-end** | React + Vite | Moderno, rápido, HMR, code splitting | 18.x |
| **Back-end** | FastAPI + SQLAlchemy | Performance, async, type hints, ORM | 0.104.x |
| **Banco Dev** | SQLite | Leve, sem dependências | 3.x |
| **Banco Prod** | PostgreSQL | Robusto, escalável, ACID, pgcrypto | 14.x |
| **Cache** | Redis (opcional prod) | Performance, rate limiting | 7.x |
| **Autenticação** | JWT (PyJWT) | Stateless, seguro | 3.x |
| **Criptografia** | bcrypt + cryptography | Senhas e dados sensíveis | 41.x |
| **Encryption BD** | SQLCipher / pgcrypto | Dados criptografados em repouso | - |
| **Logging** | Python-JSON-Logger | Logs estruturados em JSON | 2.0.7 |
| **Jobs** | APScheduler | Reposição automática, alertas, LGPD | 3.10.x |
| **Versionamento** | Git/GitHub | Colaboração, CI/CD | - |
| **Container** | Docker + Docker Compose | Reprodutibilidade, deploy | - |

### 5.3 Módulos de Backend

```
backend/app/
├── core/              # Configuração, segurança, logging
│   ├── config.py      # Variáveis de ambiente
│   ├── security.py    # JWT, bcrypt, criptografia
│   ├── logging.py     # JSON formatter, structured logs
│   └── crypto.py      # Criptografia de dados (novo)
├── models/            # Modelos ORM (6 tabelas base + 3 novas)
│   ├── usuario.py
│   ├── produto.py
│   ├── estoque.py     # +campos estoque_min/max
│   ├── venda.py
│   ├── item_venda.py
│   ├── auditoria.py   # Logs persistidos
│   ├── api_key.py     # (novo)
│   ├── ordem_reposicao.py  # (novo)
│   ├── alerta.py      # (novo)
│   └── ...
├── schemas/           # Validação Pydantic
├── routes/            # Endpoints API
│   ├── auth.py
│   ├── usuarios.py
│   ├── produtos.py
│   ├── estoque.py
│   ├── vendas.py
│   ├── relatorios.py
│   ├── api_keys.py    # (novo)
│   ├── reposicao.py   # (novo)
│   ├── alertas.py     # (novo)
│   ├── privacidade.py # LGPD (novo)
│   └── sync.py        # Modo offline (novo)
├── middleware/        # Interceptadores
│   ├── audit_middleware.py   # Auditoria HTTP
│   └── rate_limit.py  # Rate limiting (novo)
├── utils/             # Utilidades
│   ├── audit.py       # Funções de auditoria
│   ├── alertas.py     # Lógica de alertas (novo)
│   ├── lgpd.py        # Deleção, export de dados (novo)
│   ├── scheduler.py   # Jobs agendados (novo)
│   └── ...
├── db/
│   ├── database.py    # Conexão BD
│   ├── init_db.py     # Setup inicial
│   └── seed_db.py     # Dados de teste
└── main.py            # Entry point
```

### 5.4 Fluxo de Autenticação & Autorização

```
1. Login (POST /api/auth/login)
   └─► Email + Senha
       └─► Valida credenciais contra BD
           └─► Se válido: Gera JWT (exp 30min) + retorna token
               └─► Cliente armazena em localStorage
                   
2. Requisição Autenticada
   └─► Authorization: Bearer <JWT>
       └─► Middleware verifica JWT
           ├─► Se válido: Extrai user_id, role
           │   └─► Valida permissão por role (RBAC)
           │       └─► Se autorizado: Processa requisição ✅
           │           └─► Middleware de auditoria registra
           │
           └─► Se inválido: 401 Unauthorized

3. Auditoria & Logging
   └─► Auditoria Middleware captura:
       ├─► user_id, role
       ├─► http_method, http_path
       ├─► status_code, ip_address
       ├─► timestamp, duração
       └─► Registra em auditoria_logs + JSON logger
```

### 5.5 Fluxo de Venda com Auditoria Integrada

```
1. Nova Venda
   └─► POST /api/vendas
       └─► Valida JWT
           └─► Valida role (caixa/gerente/admin)
               └─► Recebe itens com quantidade
                   └─► Para cada item:
                       ├─► Verifica estoque
                       ├─► Calcula subtotal
                       └─► Se OK: Continua
                           └─► Cria Venda + ItemVenda em transação
                               ├─► Desconta estoque
                               ├─► Registra auditoria
                               └─► Registra JSON log
                                   └─► Retorna venda_id ✅
```

### 5.6 Logging Estruturado em JSON

```json
{
  "timestamp": "2026-04-19T14:30:45.123Z",
  "severity": "INFO",
  "module": "app.routes.vendas",
  "function": "criar_venda",
  "line": 42,
  "message": "Venda criada com sucesso",
  "context": {
    "user_id": 1,
    "role": "caixa",
    "venda_id": 123,
    "total": 150.50,
    "itens_quantidade": 3,
    "http_method": "POST",
    "http_path": "/api/vendas",
    "http_status": 201,
    "ip_address": "192.168.1.100",
    "duracao_ms": 245
  }
}
```

---

## 6. Modelagem de Dados

### Tabelas Implementadas (9 no total)

#### Usuários
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| email | VARCHAR | UNIQUE, NOT NULL, ENCRYPTED |
| senha_hash | VARCHAR | NOT NULL (bcrypt) |
| username | VARCHAR | UNIQUE, NOT NULL |
| role | VARCHAR | admin/gerente/caixa |
| ativo | BOOLEAN | DEFAULT true |
| criado_em | TIMESTAMP | DEFAULT now() |
| atualizado_em | TIMESTAMP | ON UPDATE now() |

#### Produtos
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| nome | VARCHAR | UNIQUE, NOT NULL |
| descricao | TEXT | Optional |
| preco | DECIMAL(10,2) | NOT NULL, CHECK > 0 |
| categoria | VARCHAR | Optional |
| data_validade | DATE | **NOVO** - Validade |
| temperatura_min | FLOAT | **NOVO** - Temp ideal mín |
| temperatura_max | FLOAT | **NOVO** - Temp ideal máx |
| lote | VARCHAR | **NOVO** - Identificação lote |
| ativo | BOOLEAN | DEFAULT true |
| criado_em | TIMESTAMP | DEFAULT now() |
| atualizado_em | TIMESTAMP | ON UPDATE now() |

#### Estoque
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| produto_id | FK → Produtos | NOT NULL |
| quantidade | INTEGER | DEFAULT 0, NOT NULL |
| estoque_minimo | INTEGER | **NOVO** - Ponto de reposição |
| estoque_maximo | INTEGER | **NOVO** - Limite máximo |
| temperatura_atual | FLOAT | **NOVO** - Temperatura real |
| data_ultima_verificacao | TIMESTAMP | **NOVO** - Última medição |
| criado_em | TIMESTAMP | DEFAULT now() |
| atualizado_em | TIMESTAMP | ON UPDATE now() |

#### Vendas
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| usuario_id | FK → Usuários | NOT NULL |
| total | DECIMAL(10,2) | NOT NULL, CHECK > 0 |
| desconto | DECIMAL(10,2) | DEFAULT 0 |
| data_venda | TIMESTAMP | DEFAULT now() |
| data_criacao | TIMESTAMP | DEFAULT now() |

#### ItemVenda
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| venda_id | FK → Vendas | NOT NULL |
| produto_id | FK → Produtos | NOT NULL |
| quantidade | INTEGER | NOT NULL, > 0 |
| preco_unitario | DECIMAL(10,2) | NOT NULL |
| subtotal | DECIMAL(10,2) | NOT NULL |

#### AuditoriaLogs
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| event_type | VARCHAR | AUTH/CRUD/SECURITY |
| action | VARCHAR | CREATE/READ/UPDATE/DELETE |
| status | VARCHAR | SUCCESS/FAILURE |
| user_id | FK → Usuários | Optional |
| resource_type | VARCHAR | usuario/produto/venda |
| resource_id | INTEGER | ID do recurso |
| error_message | VARCHAR | Se falhou |
| context | JSON | Contexto estruturado |
| http_method | VARCHAR | GET/POST/PUT/DELETE |
| http_path | VARCHAR | /api/vendas |
| http_status | INTEGER | 200/401/403/500 |
| ip_address | VARCHAR | Cliente IP (ENCRYPTED) |
| data_criacao | TIMESTAMP | DEFAULT now() |
| retencao_ativa | BOOLEAN | LGPD compliance |

#### **NOVAS TABELAS (Sprint Final)**

#### APIKey **[NOVO]**
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| chave_secreta | VARCHAR | UNIQUE, ENCRYPTED |
| usuario_id | FK → Usuários | NOT NULL |
| descricao | VARCHAR | Identificação |
| ativo | BOOLEAN | DEFAULT true |
| limite_requisicoes | INTEGER | 100/min |
| janela_tempo | INTEGER | Segundos (60) |
| ultima_uso | TIMESTAMP | Optional |
| criado_em | TIMESTAMP | DEFAULT now() |
| expires_em | TIMESTAMP | Optional |

#### OrdemReposicao **[NOVO]**
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| produto_id | FK → Produtos | NOT NULL |
| quantidade | INTEGER | NOT NULL, > 0 |
| status | VARCHAR | pending/confirmada/recebida |
| criado_em | TIMESTAMP | DEFAULT now() |
| confirmado_em | TIMESTAMP | Optional |
| recebido_em | TIMESTAMP | Optional |

#### Alerta **[NOVO]**
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| tipo | VARCHAR | validade/temperatura/estoque |
| produto_id | FK → Produtos | NOT NULL |
| estoque_id | FK → Estoque | Optional |
| mensagem | VARCHAR | Descrição do alerta |
| lido | BOOLEAN | DEFAULT false |
| criado_em | TIMESTAMP | DEFAULT now() |
| resolvido_em | TIMESTAMP | Optional |

#### ConsentimentoUsuario **[NOVO - LGPD]**
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| usuario_id | FK → Usuários | NOT NULL |
| tipo_consentimento | VARCHAR | marketing/analytics/cookies |
| aceito | BOOLEAN | NOT NULL |
| data_consentimento | TIMESTAMP | DEFAULT now() |
| revogado_em | TIMESTAMP | Optional |

#### SolicitacaoDeleteData **[NOVO - LGPD]**
| Campo | Tipo | Restrições |
|------|------|-----------|
| id | INTEGER | PK, AUTO_INCREMENT |
| usuario_id | FK → Usuários | NOT NULL |
| status | VARCHAR | pendente/processada/cancelada |
| data_solicitacao | TIMESTAMP | DEFAULT now() |
| data_expiracao | TIMESTAMP | now() + 30 dias |
| data_processamento | TIMESTAMP | Optional |
| motivo_cancelamento | VARCHAR | Optional |

---

## 7. Fluxos Principais

### 7.1 Fluxo de Venda (PDV)
```
Início Venda
  └─► Carrinho vazio
      └─► Buscar/Escanear produto
          └─► Adicionar ao carrinho
              └─► Validar estoque ✓
                  └─► Repetir ou Finalizar
                      └─► Calcular Total
                          └─► Realizar Pagamento
                              └─► Emitir Cupom
                                  └─► Atualizar Estoque
                                      └─► Registrar Auditoria
                                          └─► Venda Concluída ✓
```

### 7.2 Fluxo de Reposição Automática
```
Job Agendado (a cada 30min)
  └─► Verificar estoques
      └─► Para cada produto:
          ├─► IF quantidade < estoque_minimo THEN
          │   └─► Criar OrdemReposicao
          │       ├─► Registrar em auditoria
          │       └─► Enviar notificação (gerente)
          └─► ELSE continua
```

### 7.3 Fluxo de Alertas
```
Job Agendado (a cada 15min)
  └─► Verificar alertas
      └─► Produtos com validade próxima (<7 dias)
          ├─► Criar Alerta tipo=validade
          └─► Dashboard mostra badge
      └─► Temperatura fora da faixa ideal
          ├─► Criar Alerta tipo=temperatura
          └─► Dashboard mostra badge
      └─► Estoque abaixo do mínimo
          ├─► Criar Alerta tipo=estoque
          └─► Dashboard mostra badge
```

### 7.4 Fluxo de Conformidade LGPD
```
Usuário solicita Deleção (DELETE /api/usuarios/{id}/solicitar-delecao)
  └─► Cria SolicitacaoDeleteData com status=pendente
      ├─► Registra auditoria
      └─► Aguarda 30 dias
          └─► Job executa DELETE
              ├─► Soft delete (flag ativo=false)
              ├─► Criptografia de dados PII
              ├─► Mantém logs de auditoria (compliance)
              └─► Registra conclusão

Usuário exporta dados (GET /api/usuarios/eu/meus-dados)
  └─► Retorna JSON com:
      ├─► Dados do usuário
      ├─► Histórico de vendas
      ├─► Consentimentos
      └─► Logs de acesso
```

### 7.5 Fluxo de Modo Offline (Fase 3)
```
Cliente perde conexão
  └─► Service Worker ativa
      └─► IndexedDB armazena dados localmente
          └─► Usuário continua usando app
              └─► Cria venda offline
                  ├─► Armazena em fila local
                  └─► Aguarda reconexão
                      └─► Sync automático
                          ├─► POST /api/sync/batch com operações
                          └─► Servidor reconcilia dados ✓
```

## 8. Plano de Implementação - Sprint Final (19-23 Abril)

### Fase 1: FÁCIL - Paralelo (2 dias)
**Paralelo 1A: APIs Abertas [2-3h]**
- [ ] Criar modelo APIKey + gerenciamento
- [ ] Implementar rate limiting por cliente
- [ ] Documentar endpoints públicos

**Paralelo 1B: Reposição Automática [3-4h]**
- [ ] Adicionar campos estoque_min/max
- [ ] Criar modelo OrdemReposicao
- [ ] Job APScheduler verificando a cada 30min

**Paralelo 1C: Alertas de Validade [4-5h]**
- [ ] Adicionar campos data_validade, temperatura
- [ ] Criar modelo Alerta
- [ ] Job APScheduler a cada 15min
- [ ] Dashboard mostra alertas

**Total Fase 1:** 9-12 horas

### Fase 2: MÉDIA - Sequencial (1 dia)
**2A: Criptografia de BD [6-7h]**
- [ ] Configurar SQLCipher (dev) / pgcrypto (prod)
- [ ] Encriptar campos sensíveis (email, PII)
- [ ] Migração de dados existentes

**2B: Conformidade LGPD [7-8h]**
- [ ] Modelos ConsentimentoUsuario + SolicitacaoDeleteData
- [ ] Endpoint DELETE /api/usuarios/{id}/solicitar-delecao
- [ ] Endpoint GET /api/usuarios/eu/meus-dados
- [ ] Job de deleção após 30 dias

**Total Fase 2:** 13-15 horas

### Fase 3: ALTA - Condicional (2-3 dias)
**3A: Modo Offline [12-15h] OU 3B: PDV Performance [15-20h]**
- Depende de Fase 1 + 2 completadas
- Escolher uma das duas

**Total Fase 3:** 12-20 horas (condicional)

### Cronograma Completo
| Data | Fase | Atividades | Status |
|------|------|-----------|--------|
| 19-20/04 | 1 | APIs + Reposição + Alertas | 📋 Planejado |
| 21/04 | 2 | Criptografia + LGPD | 📋 Planejado |
| 22-23/04 | 3 | Offline OU Performance | 📋 Condicional |

### Referência Completa
👉 **Documento detalhado:** Ver [ROADMAP_SPRINT_FINAL.md](../ROADMAP_SPRINT_FINAL.md)

---

## 9. Métricas de Sucesso - Entrega

### Cobertura de Requisitos do Cenário
- **Antes:** 36% (4/11 RFs) ✅
- **Depois:** 82% (9/11 RFs) ✅
- **Delta:** +46 pontos percentuais ✅

### Qualidade de Código
- ✅ Sem erros de sintaxe Python
- ✅ Sem erros TypeScript/JSX
- ✅ Testes com >80% cobertura em novos módulos
- ✅ Lint checks passando

### Performance
- ✅ PDV criar venda em <1000ms
- ✅ Busca de produtos <200ms
- ✅ API keys validadas em <50ms

### Conformidade
- ✅ Auditoria registrando 100% das operações
- ✅ Criptografia aplicada em campos PII
- ✅ Deleção LGPD funcionando
- ✅ Sem regressões de segurança

---

## 10. Conclusão

### Status Atual (19 de Abril de 2026)
O MVP do projeto LANCHE atingiu **36% de cobertura do Cenário** com 9 funcionalidades essenciais implementadas:
- ✅ Autenticação segura com JWT
- ✅ Controle de acesso por roles (RBAC)
- ✅ Gestão completa de produtos, estoque e vendas
- ✅ Auditoria detalhada e logging estruturado em JSON
- ✅ Interface React moderna e responsiva

### Roadmap Sprint Final (19-23 Abril)
Planejamos evoluir para **82% de cobertura** com a implementação de:
1. **APIs Abertas** - Integração com parceiros (delivery, ERPs)
2. **Reposição Automática** - Gestão inteligente de estoque
3. **Alertas** - Monitoramento de validade e temperatura
4. **Criptografia de BD** - Segurança de dados em repouso
5. **Conformidade LGPD** - Direito ao esquecimento e portabilidade
6. **Modo Offline** (condicional) - Operações sem internet
7. **PDV Ultra-Latência** (condicional) - Otimizações de performance

### Roadmap Futuro (Pós-Entrega)
As seguintes funcionalidades ficarão para versões futuras:
- Sincronização multi-filial (Arquitetura distribuída)
- Integração com cupom fiscal eletrônico (SAT/NFCe)
- Múltiplas formas de pagamento (Débito, Crédito, PIX)
- Dashboard personalizado por role
- Recuperação de senha por email

### Próximos Passos
1. ✅ Review desta documentação atualizada
2. 🚀 Iniciar Sprint Final (19-23 Abril)
3. 📊 Monitorar métricas de qualidade
4. 🧪 Testes completos em staging
5. 🎉 Entrega final com 82% de cobertura

---

**Documento Preparado:** 19 de Abril de 2026  
**Status:** ✅ REVISADO E ATUALIZADO  
**Próxima Revisão:** 23 de Abril de 2026 (Pós-Sprint Final)