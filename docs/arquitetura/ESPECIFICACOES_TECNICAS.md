# Especificações Técnicas - Projeto LANCHE

Este documento detalha o conjunto de tecnologias, práticas de segurança e arquitetura utilizadas no desenvolvimento do **LANCHE MVP**.

## 1. Stack Tecnológica

### Backend (API)
- **Linguagem**: [Python 3.11+](https://www.python.org/)
- **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/) (Alta performance, suporte a assincronismo)
- **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
- **Banco de Dados**: 
  - **Produção**: [PostgreSQL](https://www.postgresql.org/)
  - **Desenvolvimento/Testes**: [SQLite](https://www.sqlite.org/) (com suporte opcional a `sqlcipher3`)
- **ORM (Object Relational Mapper)**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Migrações de Banco**: [Alembic](https://alembic.sqlalchemy.org/)
- **Validação de Dados**: [Pydantic v2](https://docs.pydantic.dev/)
- **Gestão de Dependências**: Pip (via `requirements.txt`)

### Frontend (Aplicação Web)
- **Framework**: [React 18](https://reactjs.org/)
- **Ferramenta de Build**: [Vite](https://vitejs.dev/) (Substituto moderno e rápido para Create React App)
- **Roteamento**: [React Router DOM](https://reactrouter.com/)
- **Cliente HTTP**: [Axios](https://axios-http.com/)
- **Armazenamento Offline**: [Dexie.js](https://dexie.org/) (Wrapper para IndexedDB) para suporte a redundância offline e journaling.

## 2. Segurança e Criptografia

O projeto utiliza múltiplas camadas de segurança para proteção de dados sensíveis:

### Autenticação e Autorização
- **Tokens**: [JWT (JSON Web Tokens)](https://jwt.io/) via biblioteca `python-jose`.
- **Algoritmo de Assinatura**: `HS256` (HMAC com SHA-256).
- **Validade**: Expiração configurável via variáveis de ambiente (padrão 24h).

### Proteção de Senhas
- **Algoritmo**: [Bcrypt](https://en.wikipedia.org/wiki/Bcrypt).
- **Implementação**: `passlib` com contexto `bcrypt`. As senhas são "salteadas" (salted) e transformadas em hash antes de serem salvas no banco de dados.

### Criptografia de Campos Sensíveis
- **Algoritmo**: [Fernet (Symmetric Encryption)](https://cryptography.io/en/latest/fernet/) - Baseado em **AES-128** no modo CBC com HMAC usando SHA256.
- **Uso**: Campos que precisam ser lidos de volta (como chaves de API externas) são encriptados no banco de dados.
- **Gestão de Chaves**: Gerenciador de criptografia centralizado em `app/core/crypto.py`, utilizando a variável de ambiente `ENCRYPTION_KEY`.

### Outros Recursos de Segurança
- **API Rate Limiting**: Limitação de taxa de requisições por chave de API para prevenir abusos.
- **CORS**: Configurado para permitir apenas origens autorizadas (especialmente em produção).

## 3. Infraestrutura e DevOps

- **Conteinerização**: [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/).
  - Multi-stage builds para o frontend (compilação com Node -> serviço estático com Nginx).
  - Imagens leves baseadas em Python-slim para o backend.
- **Observabilidade**:
  - **Logging Estruturado**: Saída em formato JSON (`python-json-logger`) para fácil integração com sistemas de log (ELK, CloudWatch, etc.).
  - **Middlewares de Auditoria**: Registro de requisições e processamento.
- **Ambientes**: Configuração baseada em arquivos `.env` para distinção entre `development`, `staging` e `production`.

## 4. Diferenciais do Projeto

- **Offline Redundancy (Journaling)**: Mecanismo no frontend que garante que vendas e ações críticas sejam salvas localmente no `IndexedDB` e sincronizadas automaticamente quando houver conexão.
- **Acessibilidade em Rede Local**: Configurado para ser acessível via IP na rede local (Ex: `http://192.168.x.x:8008`), facilitando o uso em dispositivos móveis dentro do estabelecimento.

---
*Gerado automaticamente para documentação técnica do sistema.*
