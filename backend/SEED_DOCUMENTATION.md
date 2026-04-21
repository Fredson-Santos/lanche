# 🌱 Documentação - Script de Seed Completo

## Visão Geral

O script `app/db/seed_db.py` popula o banco de dados com dados de teste completos e realistas para toda a aplicação LANCHE MVP.

## O que é Criado

### 1. **Usuários (9 registros)**
- 2 Administradores
- 2 Gerentes
- 5 Caixas/Operadores
- Todos com senhas padrão para teste

**Credenciais de Teste:**
```
Admin:
  - admin@lanche.com / admin123
  - admin2@lanche.com / admin456

Gerente:
  - gerente@lanche.com / gerente123
  - gerente2@lanche.com / gerente456

Caixa:
  - caixa@lanche.com / caixa123
  - caixa2@lanche.com / caixa456
  - caixa3@lanche.com / caixa789
  - caixa_noite@lanche.com / noite123
```

### 2. **Produtos (44 registros)**
Organizados em 4 categorias:

| Categoria | Quantidade | Exemplos |
|-----------|-----------|----------|
| **Lanches** | 15 | Hambúrguer, X-Bacon, X-Tudo, Misto Quente |
| **Bebidas** | 12 | Refrigerante, Suco Natural, Milkshake, Café |
| **Acompanhamentos** | 9 | Batata Frita, Onion Rings, Salada |
| **Sobremesas** | 8 | Sorvete, Pudim, Brownie, Açaí |

### 3. **Estoques (44 registros)**
- Quantidades realistas por categoria
- Alguns produtos com estoque crítico
- Total de ~2.469 itens em estoque

### 4. **Vendas (403 registros)**
- Dados históricos dos últimos 30 dias
- Padrões realistas:
  - Mais vendas em fins de semana
  - Picos em horários de almoço (11-14h) e café (16-18h)
  - 1-5 itens por venda (maioria 2-3)
- **Faturamento Total:** R$ 19.629,50
- **Ticket Médio:** R$ 48,71

### 5. **API Keys (5 registros)**
- 4 Chaves ativas com diferentes limites
- 1 Chave desativada (exemplo de revogação)
- Descrições para identificação de uso
- Algumas com datas de expiração

```
Exemplo de chave gerada:
cd3ccf04a98055b4...0fdc8ca9
```

### 6. **Alertas (7 registros)**
Dois tipos:
- **Estoque Mínimo:** Produtos com quantidade baixa
- **Validade:** Produtos próximos do vencimento

### 7. **Ordens de Reposição (8 registros)**
Diferentes status simulados:
- Pendentes (3)
- Confirmadas (3)
- Recebidas (2)

### 8. **Auditoria (172 registros)**
Registros de eventos dos últimos 15 dias:
- Logins (AUTH)
- CRUD operations
- Eventos de segurança
- Relatórios do sistema
- 90% de sucesso, 10% de falhas (para teste)

## Como Usar

### Execução Básica

```bash
cd backend
python -m app.db.seed_db
```

### Execução via Script Python Direto

```bash
cd backend
python app/db/seed_db.py
```

### Integração com FastAPI (app/main.py)

Para popular automaticamente na primeira inicialização:

```python
from app.db.seed_db import seed_db

@app.on_event("startup")
async def startup_event():
    # Verificar se banco vazio e fazer seed
    seed_db()
```

## Estrutura de Dependências

O script segue a ordem correta de criação:

1. **Limpeza** - Remove todos os dados existentes
2. **Usuários** - Necessário para vendas e auditoria
3. **Produtos** - Base para estoques e vendas
4. **Estoques** - Rastreamento de quantidade
5. **Vendas** - Transações históricas
6. **API Keys** - Acesso de terceiros
7. **Alertas** - Notificações de problemas
8. **Ordens de Reposição** - Reabastecimento automático
9. **Auditoria** - Registro de eventos

## Características de Qualidade

### Dados Realistas
- Padrões de vendas por hora e dia da semana
- Distribuição realística de quantidade por item
- Valores de preço coerentes com categoria

### Cobertura Completa
- Todos os modelos da aplicação
- Diferentes status de registros (ativo, inativo, pendente, etc)
- Dados para testes de edge cases

### Segurança
- Senhas com hash (usando bcrypt)
- API Keys com segredos aleatórios
- Registros de auditoria com contexto

### Performance
- Inserções em batch com `db.flush()` e `db.commit()`
- Índices automáticos de banco criados
- Otimizado para executar em < 10 segundos

## Limpeza de Dados

Todos os dados anteriores são apagados antes do seed:

```python
def limpar_banco(db):
    # Deleta em ordem de dependências inversas
    # Preserva integridade referencial
```

## Estatísticas Exibidas

Após execução bem-sucedida:

```
📊 RESUMO COMPLETO DOS DADOS CRIADOS:
   ├─ Usuários: 9
   ├─ Produtos: 44
   ├─ Estoques: 44
   ├─ Vendas: 403
   ├─ API Keys: 5
   ├─ Alertas: 7
   ├─ Ordens de Reposição: 8
   └─ Registros de Auditoria: 172
```

## Troubleshooting

### Erro: "Banco de dados não existe"
```bash
# Executar migrations primeiro
alembic upgrade head

# Depois seed
python -m app.db.seed_db
```

### Erro: "Módulo não encontrado"
```bash
# Confirmar estar no diretório correto
cd backend

# Ou executar com caminho absoluto
python -m app.db.seed_db
```

### Erro: "Foreign key constraint failed"
- Confirmar que todas as migrations foram executadas
- Verificar integridade do banco com `PRAGMA integrity_check;`

## Desenvolvimento e Testes

### Para Testes Unitários
```python
from app.db.seed_db import criar_usuarios, criar_produtos

def test_usuarios():
    usuarios = criar_usuarios(db)
    assert len(usuarios) == 9
```

### Para Testes de API
```bash
# Depois de seed, a API está pronta para testes
python -m uvicorn app.main:app --reload
```

## Próximas Etapas

- [ ] Criar variante de seed com menos dados (desenvolvimento rápido)
- [ ] Adicionar script de seed com dados específicos por cenário
- [ ] Implementar seed incremental (não limpa dados existentes)
- [ ] Criar fixture de pytest para testes

## Notas

- **Segurança:** Nunca use essas credenciais em produção
- **Performance:** Dados suficientes para testes, sem excesso
- **Manutenção:** Script atualizado com novos modelos conforme adicionados
- **Reproducibilidade:** Cada execução cria os mesmos dados (exceto IDs e timestamps)
