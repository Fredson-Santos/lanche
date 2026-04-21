# 🏗️ Arquitetura do Projeto LANCHE MVP

## Visão Geral

O projeto LANCHE MVP segue uma arquitetura **three-tier** com separação clara entre Frontend, Backend e Database.

```
┌─────────────────────────────────────────────────────┐
│           FRONTEND (React + Vite)                   │
│    - Componentes por domínio de negócio             │
│    - Context API para autenticação + estado        │
│    - Services para API calls                        │
└─────────────────────────────────────────────────────┘
                      ↓ HTTP/REST + JWT
┌─────────────────────────────────────────────────────┐
│           BACKEND (FastAPI - Python)                │
│    - Rotas RESTful com RBAC                         │
│    - Middlewares (Auth, Logging, RBAC)             │
│    - Models + Schemas (SQLAlchemy + Pydantic)      │
│    - Core: Security, Config, Logging               │
└─────────────────────────────────────────────────────┘
                      ↓ SQL
┌─────────────────────────────────────────────────────┐
│      DATABASE (SQLite dev → PostgreSQL prod)        │
│    - 5 Tabelas: usuarios, produtos, estoque...     │
│    - Relações e constraints                        │
└─────────────────────────────────────────────────────┘
```

---

## 📂 Estrutura de Diretórios

### Backend (`backend/`)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Entry point FastAPI
│   ├── core/
│   │   ├── config.py           # Configurações (env vars)
│   │   ├── security.py         # Autenticação JWT + bcrypt
│   │   └── logging.py          # Setup logging estruturado
│   ├── models/                 # SQLAlchemy ORM
│   │   ├── usuario.py
│   │   ├── produto.py
│   │   ├── estoque.py
│   │   ├── venda.py
│   │   └── item_venda.py
│   ├── schemas/                # Pydantic (request/response)
│   │   ├── usuario.py
│   │   ├── produto.py
│   │   ├── estoque.py
│   │   ├── venda.py
│   │   └── item_venda.py
│   ├── routes/                 # FastAPI routers
│   │   ├── auth.py            # POST /login, /logout
│   │   ├── usuarios.py        # CRUD usuarios (Admin)
│   │   ├── produtos.py        # CRUD produtos
│   │   ├── estoque.py         # GET/PUT estoque
│   │   ├── vendas.py          # POST vendas, GET histórico
│   │   └── relatorios.py      # GET relatórios
│   ├── middleware/
│   │   ├── auth.py            # Validação JWT
│   │   ├── rbac.py            # Controle de roles
│   │   └── logging.py         # Request/Response logging
│   ├── db/
│   │   ├── database.py        # SQLAlchemy config
│   │   └── init_db.py         # Seed dados iniciais
│   └── utils/
│       ├── exceptions.py      # Custom exceptions
│       └── validators.py      # Validações comuns
├── tests/
│   ├── test_auth.py
│   ├── test_usuarios.py
│   ├── test_produtos.py
│   └── test_vendas.py
├── requirements.txt            # Dependências Python
├── .env.example               # Template variáveis
├── Dockerfile                 # Containerização
└── .gitignore
```

### Frontend (`frontend/`)

```
frontend/
├── src/
│   ├── main.jsx               # Entry point React
│   ├── App.jsx                # Componente raiz
│   ├── components/            # Componentes reutilizáveis
│   │   ├── Login/            # Componentes de autenticação
│   │   ├── Navigation/       # Menu, navbar
│   │   ├── Products/         # CRUD de produtos
│   │   ├── Sales/            # Interface de vendas
│   │   └── Reports/          # Relatórios
│   ├── pages/                 # Páginas (rotas)
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── ProductsPage.jsx
│   │   ├── SalesPage.jsx
│   │   └── ReportsPage.jsx
│   ├── services/              # API calls
│   │   ├── api.js            # Axios config + interceptors
│   │   ├── authService.js
│   │   ├── productService.js
│   │   ├── salesService.js
│   │   └── reportService.js
│   ├── hooks/                 # Custom hooks
│   │   └── useAuth.js        # Hook para autenticação
│   ├── context/               # Context API
│   │   └── AuthContext.jsx   # Estado global auth
│   ├── styles/                # CSS
│   │   └── index.css
│   └── App.css
├── public/                    # Assets estáticos
├── index.html                # Template HTML
├── package.json              # Dependências Node
├── vite.config.js            # Configuração Vite
├── .env.example              # Template variáveis
├── Dockerfile                # Containerização
└── .gitignore
```

---

## 🔐 Fluxo de Autenticação

```
1. User entra credenciais (email + senha)
   ↓
2. Frontend envia POST /api/auth/login
   ↓
3. Backend valida contra tabela usuarios
   - Email existe?
   - Senha válida? (bcrypt.compare)
   ↓
4. Se válido:
   - Gera JWT com exp=24h + role
   - Retorna token + user info
   ↓
5. Frontend armazena token em localStorage
   ↓
6. Cada requisição envia:
   Authorization: Bearer <token>
   ↓
7. Middleware JWTMiddleware valida:
   - Token válido?
   - Token expirou?
   ↓
8. Middleware RBACMiddleware valida:
   - User tem role necessário?
   - Retorna 403 Forbidden se não
   ↓
9. Se válido, requisição processa normalmente
```

---

## 📋 Stack Tecnológico

### Backend
- **FastAPI**: Framework async para APIs rápidas
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados e serialização
- **bcrypt**: Criptografia de senhas
- **PyJWT**: Geração e validação de tokens JWT
- **python-json-logger**: Logging estruturado em JSON
- **pytest**: Testes unitários e integração

### Frontend
- **React 18**: Library para UI
- **Vite**: Build tool rápido
- **React Router**: Roteamento entre páginas
- **Axios**: HTTP client para API calls
- **Context API**: State management simples

### Database
- **SQLite**: Development (leve, sem dependências)
- **PostgreSQL**: Production (robusto, escalável)

### DevOps
- **Docker**: Containerização
- **Docker Compose**: Orquestração local

---

## 🔄 Fluxo de Venda (Caso de Uso Principal)

```
1. Caixa faz login
   ↓
2. Acessa página de Vendas
   ↓
3. Inicia nova venda (cria row em vendas)
   ↓
4. Adiciona produtos ao carrinho
   - Valida estoque
   - Adiciona row em itens_venda
   ↓
5. Sistema calcula total automaticamente
   ↓
6. Finaliza venda
   - Calcula estoque_reduzido = estoque - quantidade
   - Atualiza tabela estoque
   - Marca venda como finalizada
   ↓
7. Exibe recibo
   ↓
8. Venda registrada no histórico (imutável)
```

---

## 🛡️ Segurança

### Autenticação
- **Senhas**: Criptografadas com bcrypt (salt=10)
- **JWT**: Token com expiração 24h
- **HTTPS**: Recomendado em produção

### Autorização (RBAC)
- **Admin**: Acesso completo
- **Gerente**: Vendas + Gestão (produtos/estoque/relatórios)
- **Caixa**: Apenas vendas + consultas

### Validações
- Email único em database
- Estoque não negativo
- Preço obrigatório (> 0)
- Quantidade válida (número positivo)
- Venda requer pelo menos 1 item

---

## 📊 Modelagem de Dados

### Tabelas

**Usuarios**
```sql
id, email (UNIQUE), senha_hash, nome, role, ativo, criado_em, atualizado_em, ultimo_acesso
```

**Produtos**
```sql
id, nome (UNIQUE), descricao, preco (>0), sku (UNIQUE), ativo, criado_em
```

**Estoque**
```sql
id, produto_id (FK), quantidade, atualizado_em
```

**Vendas**
```sql
id, usuario_id (FK), data_hora, subtotal, total, status, criado_em
```

**ItensVenda**
```sql
id, venda_id (FK), produto_id (FK), quantidade, preco_unitario, subtotal
```

---

## 🚀 Próximas Implementações

1. **Modo Offline com Sincronização (TASK-3A)**
   - IndexedDB para armazenamento local
   - Service Worker para cache
   - Sincronização automática quando reconectado
   - Validações de estoque funcionam offline

2. **Validações Avançadas de Estoque**
   - Bloqueio de produtos sem estoque ✅
   - Validação de quantidade máxima ✅
   - Bloqueio de aumento acima do estoque ✅
   - UI visual desabilitada para itens indisponíveis ✅

3. **Logging + Auditoria** (TASK-004)
   - Estruturado em JSON
   - Rastreamento de ações por usuário
   - Middleware centralizado

4. **Validações Avançadas**
   - Regras de negócio em schemas
   - Validadores customizados

5. **Testes Automatizados**
   - Unit tests para services
   - Integration tests para rotas

4. **Documentação Swagger/OpenAPI**
   - Gerada automaticamente por FastAPI
   - Testes diretos pelo Swagger UI

---

## 📚 Referências

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Docker Documentation](https://docs.docker.com/)
