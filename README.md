# LANCHE MVP

> **Atividade Integradora / Projeto Prático**  
> **Sistema de Gestão para Varejo Alimentício**  
> Produto Viável Mínimo com Autenticação Segura, Controle de Acesso e Gerenciamento de Vendas

## 📋 Atividade Prática
Este projeto foi desenvolvido como parte de uma atividade prática integradora. O objetivo foi aplicar conceitos de desenvolvimento full-stack e engenharia de software no cenário **LANCHE**.

- [📄 Detalhes da Atividade](docs/atividade/Atividade-a-Realizar/ATIVIDADE_PRATICA.md)
- [📖 Cenário de Referência](docs/atividade/Atividade-a-Realizar/Cenario.md)

## 🎯 Objetivo


Desenvolver um sistema simplificado e funcional para gestão de vendas em lojas de varejo alimentício, com foco em:
- ✅ Autenticação segura (JWT + bcrypt)
- ✅ Controle de acesso por roles (Admin, Gerente, Caixa)
- ✅ Gestão de produtos e estoque
- ✅ Interface de caixa para vendas
- ✅ Relatórios de vendas
- ✅ Logging estruturado e auditoria
- ✅ Controle de validade e temperatura
- ✅ Gestão de dados pessoais (LGPD Lite)
- ✅ Criptografia de dados PII

## 📊 Stack Tecnológico

| Camada | Tecnologia | Descrição |
|--------|-----------|----------|
| **Frontend** | React 18 + Vite | Interface responsiva e rápida |
| **Backend** | FastAPI (Python) | API RESTful com type hints |
| **Database** | SQLite (dev) / PostgreSQL (prod) | Dados persistidos |
| **Autenticação** | JWT + bcrypt | Segurança robusta |
| **DevOps** | Docker + Docker Compose | Containerização |

## 🏗️ Estrutura do Projeto

```
lanche/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── core/              # Segurança, configuração, logging
│   │   ├── models/            # ORM SQLAlchemy
│   │   ├── schemas/           # Pydantic (request/response)
│   │   ├── routes/            # Endpoints da API
│   │   ├── middleware/        # Auth, RBAC, Logging
│   │   ├── db/                # Database config
│   │   └── utils/             # Helpers e exceptions
│   ├── tests/                 # Testes automatizados
│   ├── requirements.txt        # Dependências Python
│   ├── .env.example           # Template de variáveis
│   └── Dockerfile             # Containerização
│
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── components/        # Componentes reutilizáveis
│   │   ├── pages/             # Páginas (rotas)
│   │   ├── services/          # API calls
│   │   ├── hooks/             # Custom hooks
│   │   ├── context/           # State management
│   │   ├── styles/            # CSS
│   │   └── main.jsx           # Entry point
│   ├── index.html
│   ├── package.json           # Dependências Node
│   ├── vite.config.js         # Configuração Vite
│   ├── .env.example           # Template de variáveis
│   └── Dockerfile             # Containerização
│
├── docs/                       # Central de Documentação
│   ├── arquitetura/            # Tech Stack e Design
│   │   └── diagramas/          # Diagramas UML
│   ├── requisitos/             # RF, RNF e RN
│   ├── planejamento/           # Roadmaps e Planos
│   ├── tasks/                  # Histórico de entregas
│   ├── testes/                 # Logs e Resultados de QA
│   ├── conclusao/              # Certificados e Marcos
│   └── atividades/             # Atividades integradoras
│
├── docker-compose.yml          # Orquestração local
├── .env.example               # Template de variáveis
└── README.md                  # Este arquivo
```

Consulte [docs/arquitetura/ARQUITETURA.md](docs/arquitetura/ARQUITETURA.md) para detalhes completos da arquitetura.

## 🚀 Início Rápido

### Pré-requisitos
- Docker e Docker Compose instalados
- OU Python 3.11+ e Node.js 20+

### Opção 1: Com Docker Compose (Recomendado)

```bash
# Clone o repositório
git clone <repo-url>
cd lanche

# Copie as variáveis de ambiente
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Inicie os serviços
docker-compose up --build

# Acesse:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
# - Swagger API: http://localhost:8000/docs
```

### Opção 2: Desenvolvimento Local

#### Backend

```bash
# Navegue para o backend
cd backend

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env

# Inicie o servidor
uvicorn app.main:app --reload
```

#### Frontend

```bash
# Navegue para o frontend
cd frontend

# Instale dependências
npm install

# Configure variáveis de ambiente
cp .env.example .env

# Inicie o servidor de desenvolvimento
npm run dev
```

## 📝 Funcionalidades Implementadas

### MVP v1.0

- [x] Autenticação com JWT
- [x] Controle de acesso por roles (RBAC)
- [x] CRUD de usuários (Admin)
- [x] CRUD de produtos
- [x] Gestão de estoque
- [x] Interface de vendas
- [x] Relatório de vendas
- [x] Logging estruturado
- [x] Testes automatizados (Unitários e E2E)
- [x] Documentação Swagger (OpenAPI)

### MVP v1.1 - Funcionalidades Avançadas (21/04/2026)

- [x] Controle de validade e Alertas (TASK 1C)
- [x] Gestão de Dados/LGPD (TASK 2B)
- [x] Criptografia de Banco de Dados (TASK 2A)
- [x] APIs Abertas para Terceiros (TASK 1A)
- [x] Reposição Automática de Estoque (TASK 1B)
- [x] Validações de Estoque no Carrinho (TASK 3A-UX)
- [x] Modo Offline - Journaling Offline (Iniciado TASK 3A)
  - [x] IndexedDB com Dexie
  - [x] Sync manual com backend
  - [x] Limpeza de dados após decisão
  - [x] Download de auditoria
  - [ ] Service Worker (próximo)
  - [ ] Cache API (próximo)

## 🔐 Segurança

### Autenticação
```
email + senha (bcrypt) → JWT (24h) → Authorization Header
```

### Autorização
| Recurso | Caixa | Gerente | Admin |
|---------|-------|---------|-------|
| Vendas | ✅ | ✅ | ✅ |
| Consultar Estoque | ✅ | ✅ | ✅ |
| Cadastrar Produto | ❌ | ✅ | ✅ |
| Editar Produto | ❌ | ✅ | ✅ |
| Deletar Produto | ❌ | ❌ | ✅ |
| Gerenciar Usuários | ❌ | ❌ | ✅ |
| Relatórios | ❌ | ✅ | ✅ |

## 📚 Documentação

- [📑 Índice Completo](INDICE.md) - Navegação centralizada da documentação
- [🗺️ ROADMAP do Projeto](ROADMAP.md) - Timeline, fases, milestones
- [🏗️ Arquitetura Detalhada](docs/arquitetura/ARQUITETURA.md) - Stack, fluxos, modelagem
- [📋 Requisitos & Especificação](docs/requisitos/REQUISITOS_MVP.md) - Documentação unificada de RF, RNF e RN
- [📐 Diagramas UML](docs/arquitetura/diagramas/) - Classes, casos de uso, sequência

### Endpoints Principais

#### Autenticação
```
POST /api/auth/login          # Efetua login
POST /api/auth/logout         # Efetua logout
```

#### Usuários (Admin)
```
GET    /api/usuarios          # Lista usuários
POST   /api/usuarios          # Cria usuário
GET    /api/usuarios/{id}     # Obtém usuário
PUT    /api/usuarios/{id}     # Atualiza usuário
DELETE /api/usuarios/{id}     # Deleta usuário
```

#### Produtos
```
GET    /api/produtos          # Lista produtos
POST   /api/produtos          # Cria produto (Gerente+)
GET    /api/produtos/{id}     # Obtém produto
PUT    /api/produtos/{id}     # Atualiza produto (Gerente+)
DELETE /api/produtos/{id}     # Deleta produto (Admin)
```

#### Estoque
```
GET    /api/estoque           # Lista estoque
GET    /api/estoque/{id}      # Obtém estoque de um produto
PUT    /api/estoque/{id}      # Atualiza quantidade (Gerente+)
```

#### Vendas
```
POST   /api/vendas            # Cria nova venda
POST   /api/vendas/{id}/itens # Adiciona item à venda
GET    /api/vendas            # Lista histórico de vendas
GET    /api/vendas/{id}       # Obtém detalhes da venda

#### LGPD & Segurança
GET    /api/usuarios/me/dados # Exportar meus dados (Acesso)
GET    /api/keys/             # Listar chaves API (Admin)
POST   /api/keys/             # Gerar nova chave (Admin)
```

#### Relatórios
```
GET    /api/relatorios/vendas # Relatório de vendas (período)
GET    /api/relatorios/faturamento # Faturamento total
```

## 🧪 Testes

```bash
# Backend
cd backend
pytest                        # Executa todos os testes
pytest -v                     # Modo verbose
pytest --cov                  # Com cobertura

# Frontend
cd frontend
npm test                      # Executa testes
npm test -- --coverage        # Com cobertura
```

## 📋 Requisitos do Sistema

### Funcionais (23 RFs)
Autenticação, autorização, CRUD de usuários/produtos/estoque, vendas, relatórios.

### Não Funcionais (17 RNFs)
- Tempo de resposta: < 2s
- Disponibilidade: > 95%
- Segurança: bcrypt, JWT, HTTPS (prod)
- Performance: < 500ms para 1000 produtos

### Regras de Negócio (19 RNs)
Email único, senha criptografada, role obrigatório, estoque não negativo, venda imutável, etc.

Consulte [docs/requisitos/REQUISITOS_MVP.md](docs/requisitos/REQUISITOS_MVP.md) para a lista completa. O projeto atingiu **82% de cobertura** dos requisitos funcionais planejados para o MVP.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

**Última atualização**: Abril 2026  
**Versão**: 1.0.0 - MVP

