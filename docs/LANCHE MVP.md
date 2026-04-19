# LANCHE MVP
## Produto Viável Mínimo  
**Documentação de Engenharia de Software**

**Versão 2.0 - MVP**  
Abril de 2026  

---

## Resumo Executivo
O projeto LANCHE MVP é uma versão simplificada e funcional do sistema de gestão para rede de varejo alimentício. Este documento descreve a especificação técnica de um Produto Viável Mínimo (MVP) com 7 funcionalidades principais, desenvolvido com qualidade e documentação completa.

O MVP contempla as funcionalidades essenciais para operação básica de uma loja de varejo: autenticação de usuários com login seguro, controle de acesso por roles (Admin, Gerente, Caixa), cadastro de produtos, controle de estoque, venda simplificada, baixa automática de estoque e relatório de vendas.

---

## 1. Escopo do Projeto

### 1.1 Funcionalidades do MVP
1. Autenticação de Usuários - Login seguro com email e senha (hashed com bcrypt)  
2. Controle de Acesso - 3 roles (Admin, Gerente, Caixa) com permissões específicas  
3. Cadastro de Produtos - Criar, ler, atualizar e deletar produtos com nome, preço e descrição  
4. Controle de Estoque - Registrar quantidade de cada produto em estoque  
5. Venda Simples - Interface básica de caixa para simular vendas  
6. Baixa Automática - Reduzir quantidade de estoque automaticamente ao vender  
7. Relatório de Vendas - Consultar vendas realizadas e total faturado  

2. Múltiplas filiais  
3. Controle de validade de produtos  
4. Múltiplas formas de pagamento  
5. Cupom fiscal (CF-e)  
6. Auditoria e logs detalhados  
7. Sincronização de dados  
8. Modo offline  
9. Recuperação de senha por email  
10. Dashboard personalizado por role
8. Recuperação de senha por email  

---

## 2. Requisitos Funcionais (RF)

| ID    | Descrição | Prioridade |
|------|----------|-----------|
| RF-01 | Efetuar login com email e senha | Crítica |
| RF-02 | Validar credenciais de usuário | Crítica |
| RF-03 | Gerar token de autenticação (JWT) | Crítica |
| RF-04 | Efetuar logout | Alta |
| RF-05 | Validar role do usuário | Crítica |
| RF-07 | Retornar 403 se sem permissão | Crítica |
| RF-08 | Gerenciar usuários (CRUD) | Alta |
| RF-09 | Atribuir roles a usuários | Alta |
| RF-10 | Cadastrar novo produto | Crítica |
| RF-11 | Listar produtos | Crítica |
| RF-12 | Editar produto | Alta |
| RF-13 | Deletar/Inativar produto | Média |
| RF-14 | Consultar estoque | Crítica |
| RF-15 | Atualizar estoque manualmente | Média |
| RF-16 | Iniciar venda | Crítica |
| RF-17 | Adicionar produtos à venda | Crítica |
| RF-18 | Remover produtos da venda | Alta |
| RF-19 | Calcular total da venda | Crítica |
| RF-20 | Finalizar venda | Crítica |
| RF-21 | Reduzir estoque | Crítica |
| RF-22 | Histórico de vendas | Crítica |
| RF-23 | Filtrar vendas por períodperíodo | Alta |
| RF-20 | Calcular faturamento | Alta |

---

## 3. Requisitos Não Funcionais (RNF)

| ID    | Descrição | Valor |
|------|----------|------|
| RNF-01 | Tempo de resposta | < 2s |
| RNF-02 | Disponibilidade | > 95% |
| RNF-03 | Suporte a produtos | 1000 |
| RNF-04 | Transações | 10000 |
| RNF-05 | Interface responsiva | Sim |
| RNF-06 | Navegadores | Chrome, Firefox, Safari |
| RNF-07 | Banco de dados | Local/Remoto |
| RNF-08 | Instalação | < 5 min |
| RNF-09 | Código limpo | Sim |
| RNF-10 | Performance de busca | < 500ms |
| RNF-11 | Criptografia de senha | bcrypt (salt 10) |
| RNF-12 | Token JWT | Expiração 24h |
| RNF-13 | HTTPS | Recomendado produção |
| RNF-14 | Segurança de senha | Mínimo 8 caracteres |
| RNF-15 | Auditoria de acesso | Log de logins bem-sucedidos/falhados |

---

## 4. Regras de Negócio (RN)
| RNF-08 | Instalação | < 5 min |
| RNF-09 | Código limpo | Sim |
| RNF-10 | Performance de busca | < 500ms |
| RNF-11 | Criptografia de senha | bcrypt (salt 10) |
| RNF-12 | Token JWT | Expiração 24h |
| RNF-13 | HTTPS | Recomendado produção |
| RNF-14 | Segurança de senha | Mínimo 8 caracteres |
| RNF-15 | Auditoria de acesso | Log de logins bem-sucedidos/falhados |

---

## 4. Regras de Negócio (RN)

| ID    | Regra | Descrição |
|------|------|----------|
| RN-01 | Email único | Sem duplicação de usuários |
| RN-02 | Autenticação obrigatória | Acesso bloqueado sem login |
| RN-03 | Role obrigatório | admin, gerente ou caixa |
| RN-07 | Admin gerencia usuários | Criar, editar, desativar usuários |
| RN-08 | Caixa só vende | Sem acesso a gestão de produtos |
| RN-09 | Gerente controla estoque | Pode atualizar quantidade |
| RN-10 | Admin deleta produto | Apenas admin pode deletar |
| RN-11 | Acesso negado (403) | Se role não tiver permissão |
| RN-12 | Estoque não negativo | Não vender além do estoque |
| RN-13 | Preço obrigatório | > 0 |
| RN-14 | Produto único | Sem duplicação |
| RN-15 | Venda não editável | Histórico imutável |
| RN-16 | Estoque sincronizado | Atualização imediata |
| RN-17 | Venda requer item | Não finalizar vazio |
| RN-18 | Quantidade válida | Número positivo |
| RN-19 | Total correto | Soma dos itenso |
| RN-13 | Total correto | Soma dos itens |
| RN-14 | Deleção segura | Manter histórico |
| RN-15 | Período válido | Filtragem correta |

---

## 5. Arquitetura da Solução

### 5.1 Visão Geral
- Front-end: React + Vite  
- Back-end: FastAPI (Python)  
- Banco: SQLite (dev) → PostgreSQL (prod)  
- Autenticação: JWT (JSON Web Tokens)  
- Criptografia: bcrypt para senhas  

### 5.2 Fluxo de Autenticação
1. Usuário entra com email e senha
2. Backend valida credenciais contra banco de dados
3. Se válido, gera token JWT com expiração 24h
4. Cliente armazena token (localStorage/sessionStorage)
5. Token é enviado em Authorization header em cada requisição
6. Middleware valida token antes de processar requisição  

### 5.3 Stack Tecnológico

| Camada | Tecnologia | Justificativa |
|-------|-----------|-------------|
| Front-end | React + Vite | Moderno, rápido, HMR |
| Back-end | FastAPI | Performance, async, type hints |
| Banco Dev | SQLite | Leve, sem dependências |
| Banco Prod | PostgreSQL | Robusto, escalável, ACID |
| Versionamento | Git/GitHub | Colaboração |

---

## 6. Modelagem de Dados

### Usuários
| Campo | Tipo | Descrição |
|------|------|----------|
| role | VARCHAR | admin/gerente/caixa |
| id | INTEGER | PK |
| email | VARCHAR | Único, obrigatório |
| senha_hash | VARCHAR | bcrypt, obrigatório |
| nome | VARCHAR | Obrigatório |
| ativo | BOOLEAN | true |
| criado_em | TIMESTAMP | |
| atualizado_em | TIMESTAMP | |
| ultimo_acesso | TIMESTAMP | |

### Produtos
| Campo | Tipo | Descrição |
|------|------|----------|
| id | INTEGER | PK |
| nome | VARCHAR | Obrigatório |
| descricao | TEXT | Opcional |
| preco | DECIMAL | > 0 |
| sku | VARCHAR | Único |
| ativo | BOOLEAN | true |
| criado_em | TIMESTAMP | |
| atualizado_em | TIMESTAMP | |

### Estoque
| Campo | Tipo |
|------|------|
| id | INTEGER |
| produto_id | FK |
| quantidade | INTEGER |
| atualizado_em | TIMESTAMP |

### Vendas
| Campo | Tipo |
|------|------|
| id | INTEGER |
| data_hora | TIMESTAMP |
| subtotal | DECIMAL |
| total | DECIMAL |
| status | VARCHAR |

### ItensVenda
| Campo | Tipo |
|------|------|
| id | INTEGER |
| venda_id | FK |
| produto_id | FK |
| quantidade | INTEGER |
| preco_unitario | DECIMAL |
| subtotal | DECIMAL |

---

## 7. Fluxos

### 7.1 Venda
1. Nova venda  
2. Carrinho vazio  
3. Adicionar produtos  
4. Validar estoque  
5. Finalizar  
6. Atualizar estoque  
7. Registrar  

### 7.2 Relatório
1. Acessar relatórios  
2. Selecionar período  
3. Calcular métricas  
4. Exibir resultados  

---

## 8. Diagramas UML
- Diagrama de Classes  
- Casos de Uso  
- Sequência  
- Estados  
- MER  

---

## 9. Plano de Implementação

| Dia | Atividade | Horas | Entrega |
|----|----------|------|--------|
| 1-2 | Setup + API | 14h | CRUD |
| 3-4 | Front Produtos | 14h | Interface |
| 5-6 | Venda + Relatório | 14h | Funcional |
| 7 | Testes | 8h | MVP |

---

## Conclusão
O MVP do projeto LANCHE é viável e funcional, com funcionalidades essenciais para operação de varejo, incluindo autenticação segura de usuários e controle de acesso por roles.

Após a entrega, pode evoluir com:
- Recuperação de senha por email
- Múltiplas filiais  
- Dashboard personalizado por role
- Validade de produtos  
- Cupom fiscal  
- Integrações e APIs públicas

Este documento serve como base para desenvolvimento e pode ser atualizado conforme necessário.