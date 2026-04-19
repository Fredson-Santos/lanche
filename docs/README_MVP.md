# Documentação LANCHE MVP

> **Produto Viável Mínimo** - Sistema de varejo simplificado com funcionalidades essenciais, autenticação segura e controle de acesso por roles

## 📋 Visão Geral

O LANCHE MVP é uma versão simplificada do sistema de gestão para rede de varejo alimentício, desenvolvido com foco em funcionalidades essenciais, segurança e controle de acesso.

### ✨ Funcionalidades Incluídas

✅ **Autenticação Segura** - Login com email/senha, tokens JWT e criptografia bcrypt  
✅ **Controle de Acesso** - 3 roles (Admin, Gerente, Caixa) com permissões específicas  
✅ **Cadastro de Produtos** - Criar, ler, atualizar e deletar produtos  
✅ **Controle de Estoque** - Registrar e consultar quantidades  
✅ **Venda Simples** - Interface de caixa para simular vendas  
✅ **Baixa Automática de Estoque** - Reduzir quantidade ao vender  
✅ **Relatório de Vendas** - Consultar vendas por período  

### ❌ Funcionalidades Excluídas (Próximas Versões)

- Múltiplas filiais
- Controle de validade de produtos
- Múltiplas formas de pagamento
- Cupom fiscal (CF-e)
- Auditoria detalhada
- Sincronização de dados
- Modo offline
- Recuperação de senha por email

---

## 📊 Requisitos do Sistema

### Papéis (Roles) e Permissões

| Role | Descrição | Permissões |
|------|-----------|-----------|
| **Admin** | Administrador do sistema | Tudo (login, vendas, gestão, usuários) |
| **Gerente** | Gerente de loja | Vendas, gestão de produtos/estoque, relatórios |
| **Caixa** | Operador de caixa | Vendas, consulta de produtos/estoque |

### Matriz de Acesso

| Funcionalidade | Caixa | Gerente | Admin |
|---|---|---|---|
| Login | ✅ | ✅ | ✅ |
| Fazer vendas | ✅ | ✅ | ✅ |
| Consultar estoque | ✅ | ✅ | ✅ |
| Listar produtos | ✅ | ✅ | ✅ |
| Cadastrar produto | ❌ | ✅ | ✅ |
| Editar produto | ❌ | ✅ | ✅ |
| Deletar produto | ❌ | ❌ | ✅ |
| Atualizar estoque | ❌ | ✅ | ✅ |
| Ver relatórios | ❌ | ✅ | ✅ |
| Gerenciar usuários | ❌ | ❌ | ✅ |

---

### Requisitos Funcionais (23 RFs)

| ID | Descrição | Prioridade |
|----|-----------|-----------|
| RF-01 | Efetuar login com email e senha | Crítica |
| RF-02 | Validar credenciais de usuário | Crítica |
| RF-03 | Gerar token de autenticação (JWT) | Crítica |
| RF-04 | Efetuar logout | Alta |
| RF-05 | Proteger rotas com autenticação | Crítica |
| RF-06 | Validar role do usuário | Crítica |
| RF-07 | Retornar 403 se sem permissão | Crítica |
| RF-08 | Gerenciar usuários (CRUD) | Alta |
| RF-09 | Atribuir roles a usuários | Alta |
| RF-10 | Cadastrar novo produto | Crítica |
| RF-11 | Listar todos os produtos | Crítica |
| RF-12 | Editar dados de produto | Alta |
| RF-13 | Deletar/Inativar produto | Média |
| RF-14 | Consultar estoque por produto | Crítica |
| RF-15 | Atualizar quantidade manualmente | Média |
| RF-16 | Iniciar nova venda | Crítica |
| RF-17 | Adicionar produtos à venda | Crítica |
| RF-18 | Remover produtos da venda | Alta |
| RF-19 | Calcular total automaticamente | Crítica |
| RF-20 | Finalizar venda | Crítica |
| RF-21 | Reduzir estoque ao vender | Crítica |
| RF-22 | Listar histórico de vendas | Crítica |
| RF-23 | Filtrar vendas por período | Alta |

### Requisitos Não Funcionais (17 RNFs)

| ID | Descrição | Valor Alvo |
|----|-----------|-----------|
| RNF-01 | Tempo de resposta | < 2 segundos |
| RNF-02 | Disponibilidade | > 95% |
| RNF-03 | Suportar produtos | até 1000 |
| RNF-04 | Suportar transações | até 10.000 |
| RNF-05 | Interface responsiva | desktop/tablet |
| RNF-06 | Navegador compatível | Chrome, Firefox, Safari |
| RNF-07 | Banco de dados | local ou remoto |
| RNF-08 | Facilidade instalação | < 5 minutos |
| RNF-09 | Código limpo | documentado |
| RNF-10 | Performance de busca | < 500ms para 1000 produtos |
| RNF-11 | Criptografia de senha | bcrypt (salt 10) |
| RNF-12 | Token JWT | Expiração 24h |
| RNF-13 | HTTPS | Recomendado em produção |
| RNF-14 | Segurança de senha | Mínimo 8 caracteres |
| RNF-15 | Auditoria de acesso | Log de logins bem-sucedidos/falhados |
| RNF-16 | Controle de acesso | Validação de role em cada rota |
| RNF-17 | Separação de permissões | Admin > Gerente > Caixa |

### Regras de Negócio (19 RNs)

| ID | Regra | Descrição |
|----|-------|-----------|
| RN-01 | Email único | Sem duplicação de usuários |
| RN-02 | Autenticação obrigatória | Acesso bloqueado sem login |
| RN-03 | Senha criptografada | Nunca armazenar em texto plano |
| RN-04 | Sessão autenticada | Token JWT válido por 24h |
| RN-05 | Logout limpa sessão | Invalidar token no cliente |
| RN-06 | Role obrigatório | admin, gerente ou caixa |
| RN-07 | Admin gerencia usuários | Criar, editar, desativar usuários |
| RN-08 | Caixa só vende | Sem acesso a gestão de produtos |
| RN-09 | Gerente controla estoque | Pode atualizar quantidade |
| RN-10 | Admin deleta produto | Apenas admin pode deletar |
| RN-11 | Acesso negado (403) | Se role não tiver permissão |
| RN-12 | Estoque não negativo | Não vender mais que em estoque |
| RN-13 | Preço obrigatório | Todo produto deve ter preço > 0 |
| RN-14 | Produto único | Não permitir duplicatas SKU/nome |
| RN-15 | Venda imutável | Histórico não pode ser editado |
| RN-16 | Estoque sincronizado | Reduzir ao finalizar venda |
| RN-17 | Venda requer item | Não finalizar venda vazia |
| RN-18 | Quantidade válida | Deve ser número positivo |
| RN-19 | Total correto | SUM(quantidade × preço) |

---

## 🏗️ Arquitetura

### Stack Tecnológico

```
┌─────────────────────────────────────────────────────┐
│               FRONTEND (React + Vite)               │
│    Interface responsiva + Roles (Admin/Ger/Caixa)   │
└─────────────────────────────────────────────────────┘
                          ↓ HTTP/REST + JWT
┌─────────────────────────────────────────────────────┐
│               BACKEND (FastAPI - Python)             │
│   API RESTful com autenticação JWT e RBAC (bcrypt)  │
│   Gerencia: Usuarios, Produtos, Vendas, Estoque     │
└─────────────────────────────────────────────────────┘
                          ↓ SQL
┌─────────────────────────────────────────────────────┐
│    DATABASE (SQLite dev → PostgreSQL prod)          │
│     5 Tabelas: Usuarios, Produtos, Estoque, etc    │
└─────────────────────────────────────────────────────┘
```

### Fluxo de Autenticação

```
1. Usuário entra credenciais (email + senha)
2. Backend valida contra tabela Usuarios
3. Se válido → Gera JWT com exp. 24h + role
4. Cliente armazena token (localStorage)
5. Cada requisição envia: Authorization: Bearer <token>
6. Middleware valida token e role
7. Token inválido → redireciona para login
8. Sem permissão → retorna 403 Forbidden
```

---

## 💾 Modelagem de Dados

### Tabelas (5 no total)

```sql
-- Usuários do sistema com roles
CREATE TABLE usuarios (
  id INTEGER PRIMARY KEY,
  email VARCHAR(100) UNIQUE NOT NULL,
  senha_hash VARCHAR(255) NOT NULL,
  nome VARCHAR(100) NOT NULL,
  role VARCHAR(20) NOT NULL CHECK(role IN ('admin', 'gerente', 'caixa')),
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT NOW(),
  atualizado_em TIMESTAMP,
  ultimo_acesso TIMESTAMP
);

-- Produtos do catálogo
CREATE TABLE produtos (
  id INTEGER PRIMARY KEY,
  nome VARCHAR(100) UNIQUE NOT NULL,
  descricao TEXT,
  preco DECIMAL(10,2) NOT NULL,
  sku VARCHAR(50) UNIQUE,
  ativo BOOLEAN DEFAULT true,
  criado_em TIMESTAMP DEFAULT NOW()
);

-- Quantidade em estoque
CREATE TABLE estoque (
  id INTEGER PRIMARY KEY,
  produto_id INTEGER UNIQUE NOT NULL,
  quantidade INTEGER DEFAULT 0,
  FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- Transações de venda
CREATE TABLE vendas (
  id INTEGER PRIMARY KEY,
  usuario_id INTEGER NOT NULL,
  data_hora TIMESTAMP DEFAULT NOW(),
  subtotal DECIMAL(10,2) NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  status VARCHAR(20) DEFAULT 'aberta',
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Itens dentro de cada venda
CREATE TABLE itens_venda (
  id INTEGER PRIMARY KEY,
  venda_id INTEGER NOT NULL,
  produto_id INTEGER NOT NULL,
  quantidade INTEGER NOT NULL,
  preco_unitario DECIMAL(10,2) NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (venda_id) REFERENCES vendas(id),
  FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
```

---

## 🎨 Diagramas UML

### Diagramas Disponíveis

1. **01_DIAGRAMA_CLASSES_MVP.puml** - 5 classes com roles
2. **02_DIAGRAMA_CASOS_USO_MVP.puml** - 18+ casos com 3 atores
3. **03_DIAGRAMA_SEQUENCIA_MVP.puml** - Fluxo completo com autenticação
4. **04_DIAGRAMA_ESTADOS_MVP.puml** - Estados com autenticação
5. **05_DIAGRAMA_MER_MVP.puml** - Modelo E-R com 5 tabelas

---

## 📊 Estatísticas

- **Requisitos Funcionais:** 23 RFs (com autenticação e roles)
- **Requisitos Não-Funcionais:** 17 RNFs (com controle de acesso)
- **Regras de Negócio:** 19 RNs (com regras de permissão)
- **Tabelas do BD:** 5 (Usuarios, Produtos, Estoque, Vendas, Itens_Venda)
- **Roles de usuário:** 3 (Admin, Gerente, Caixa)
- **Casos de Uso:** 18+
- **Diagramas UML:** 5
- **Linhas de Código (est.):** ~3.000-4.000

---

## 📞 Próximas Etapas (Versão 2.0)

Após entrega do MVP com autenticação e roles:

1. **Dashboard Personalizado** - Layout específico por role
2. **Recuperação de Senha** - Reset por email
3. **Múltiplas Filiais** - Sincronização entre lojas
4. **Auditoria Avançada** - Rastreamento de operações
5. **Validade** - Controle de data de vencimento
6. **Cupom Fiscal** - Emissão de CF-e
7. **Pagamentos** - Integração com processadora
8. **Analytics** - Dashboards de KPIs
9. **Mobile** - Aplicativo para smartphone
10. **API Pública** - Integração com terceiros

---

**Versão:** 2.0 (MVP)  
**Data:** Abril/2026  
**Status:** ✅ Pronto para Desenvolvimento  
**Autor:** Documentação Técnica LANCHE
