#!/usr/bin/env python
"""Script completo de seed do banco de dados com dados realistas de teste"""
import hashlib
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from app.models.ordem_reposicao import OrdemReposicao
from app.core.security import hash_password

db = SessionLocal()

print("=" * 60)
print("🌱 SEED COMPLETO - LANCHE MVP")
print("=" * 60)

# ============================================================================
# 1. CRIAR USUÁRIOS
# ============================================================================
print("\n📋 Criando usuários...")

usuarios_teste = [
    {'email': 'admin@lanche.com', 'username': 'admin', 'role': 'admin', 'password': 'admin123'},
    {'email': 'gerente@lanche.com', 'username': 'gerente', 'role': 'gerente', 'password': 'gerente123'},
    {'email': 'caixa@lanche.com', 'username': 'caixa', 'role': 'caixa', 'password': 'caixa123'},
]

usuarios_criados = []
for user_data in usuarios_teste:
    # Verificar se já existe
    user_exists = db.query(Usuario).filter_by(username=user_data['username']).first()
    if user_exists:
        usuarios_criados.append(user_exists)
        print(f"  ⏭️  {user_data['email']} ({user_data['role']}) - JÁ EXISTE")
        continue
    
    email_hash = hashlib.sha256(user_data['email'].encode()).hexdigest()
    usuario = Usuario(
        email=user_data['email'],
        email_hash=email_hash,
        username=user_data['username'],
        senha_hash=hash_password(user_data['password']),
        role=user_data['role'],
        ativo=True
    )
    db.add(usuario)
    usuarios_criados.append(usuario)
    print(f"  ✅ {user_data['email']} ({user_data['role']})")

db.commit()
print(f"✅ {len(usuarios_criados)} usuários no banco")

# ============================================================================
# 2. CRIAR PRODUTOS
# ============================================================================
print("\n🍔 Criando produtos...")

produtos_data = [
    # Lanches
    {
        'nome': 'Hambúrguer Simples',
        'descricao': 'Pão, hambúrguer, alface, tomate',
        'preco': 15.00,
        'categoria': 'lanche',
        'data_validade': datetime.now() + timedelta(days=30),
        'temperatura_ideal_min': 5.0,
        'temperatura_ideal_max': 10.0,
        'lote': 'LOTE001'
    },
    {
        'nome': 'Hambúrguer Duplo',
        'descricao': 'Pão, 2 hambúrgueres, queijo, alface, tomate',
        'preco': 22.00,
        'categoria': 'lanche',
        'data_validade': datetime.now() + timedelta(days=30),
        'temperatura_ideal_min': 5.0,
        'temperatura_ideal_max': 10.0,
        'lote': 'LOTE002'
    },
    {
        'nome': 'Sanduíche de Frango',
        'descricao': 'Pão, frango grelhado, alface, tomate',
        'preco': 18.00,
        'categoria': 'lanche',
        'data_validade': datetime.now() + timedelta(days=25),
        'temperatura_ideal_min': 5.0,
        'temperatura_ideal_max': 10.0,
        'lote': 'LOTE003'
    },
    # Bebidas
    {
        'nome': 'Refrigerante 2L',
        'descricao': 'Refrigerante sabor cola',
        'preco': 8.00,
        'categoria': 'bebida',
        'data_validade': datetime.now() + timedelta(days=180),
        'temperatura_ideal_min': 0.0,
        'temperatura_ideal_max': 4.0,
        'lote': 'LOTE100'
    },
    {
        'nome': 'Suco Natural 500ml',
        'descricao': 'Suco natural de laranja',
        'preco': 6.00,
        'categoria': 'bebida',
        'data_validade': datetime.now() + timedelta(days=7),
        'temperatura_ideal_min': 2.0,
        'temperatura_ideal_max': 8.0,
        'lote': 'LOTE101'
    },
    # Acompanhamentos
    {
        'nome': 'Batata Frita',
        'descricao': 'Batata frita crocante',
        'preco': 7.00,
        'categoria': 'acompanhamento',
        'data_validade': datetime.now() + timedelta(days=5),
        'temperatura_ideal_min': 65.0,
        'temperatura_ideal_max': 75.0,
        'lote': 'LOTE200'
    },
    {
        'nome': 'Anéis de Cebola',
        'descricao': 'Anéis de cebola empanados',
        'preco': 8.00,
        'categoria': 'acompanhamento',
        'data_validade': datetime.now() + timedelta(days=5),
        'temperatura_ideal_min': 65.0,
        'temperatura_ideal_max': 75.0,
        'lote': 'LOTE201'
    },
]

produtos_criados = []
for prod_data in produtos_data:
    # Verificar se já existe
    prod_exists = db.query(Produto).filter_by(nome=prod_data['nome']).first()
    if prod_exists:
        produtos_criados.append(prod_exists)
        print(f"  ⏭️  {prod_data['nome']} - JÁ EXISTE")
        continue
    
    produto = Produto(
        nome=prod_data['nome'],
        descricao=prod_data['descricao'],
        preco=prod_data['preco'],
        categoria=prod_data['categoria'],
        data_validade=prod_data['data_validade'],
        temperatura_ideal_min=prod_data['temperatura_ideal_min'],
        temperatura_ideal_max=prod_data['temperatura_ideal_max'],
        lote=prod_data['lote']
    )
    db.add(produto)
    produtos_criados.append(produto)
    print(f"  ✅ {prod_data['nome']} (R$ {prod_data['preco']:.2f})")

db.commit()
print(f"✅ {len(produtos_criados)} produtos no banco")

# ============================================================================
# 3. CRIAR ESTOQUE
# ============================================================================
print("\n📦 Criando estoque...")

estoque_criado = []
for produto in produtos_criados:
    # Verificar se estoque já existe
    est_exists = db.query(Estoque).filter_by(produto_id=produto.id).first()
    if est_exists:
        estoque_criado.append(est_exists)
        print(f"  ⏭️  {produto.nome} - JÁ EXISTE")
        continue
    
    # Definir quantities baseado no tipo
    if 'Hambúrguer' in produto.nome or 'Sanduíche' in produto.nome:
        quantidade = 50
        estoque_minimo = 10
        estoque_maximo = 100
    elif 'Refrigerante' in produto.nome or 'Suco' in produto.nome:
        quantidade = 30
        estoque_minimo = 5
        estoque_maximo = 50
    else:  # Acompanhamentos
        quantidade = 20
        estoque_minimo = 5
        estoque_maximo = 40
    
    estoque = Estoque(
        produto_id=produto.id,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo,
        estoque_maximo=estoque_maximo,
        ponto_reposicao=estoque_minimo + 5,
        temperatura_atual=8.0,
        data_ultima_verificacao=datetime.now()
    )
    db.add(estoque)
    estoque_criado.append(estoque)
    print(f"  ✅ {produto.nome}: {quantidade} unidades")

db.commit()
print(f"✅ {len(estoque_criado)} registros de estoque no banco")

# ============================================================================
# 4. CRIAR VENDAS DE TESTE
# ============================================================================
print("\n💰 Criando vendas de teste...")

vendedor = usuarios_criados[2]  # caixa
vendas_criadas = []

# Venda 1: Hoje
venda1 = Venda(
    usuario_id=vendedor.id,
    total=50.00,
    data_venda=datetime.now()
)
db.add(venda1)
db.flush()

item1 = ItemVenda(
    venda_id=venda1.id,
    produto_id=produtos_criados[0].id,  # Hambúrguer Simples
    quantidade=2,
    preco_unitario=15.00
)
item2 = ItemVenda(
    venda_id=venda1.id,
    produto_id=produtos_criados[4].id,  # Suco
    quantidade=2,
    preco_unitario=6.00
)
db.add(item1)
db.add(item2)
vendas_criadas.append(venda1)
print(f"✅ Venda 1: 2x Hambúrguer + 2x Suco (R$ {venda1.total:.2f}) - Caixa: {vendedor.email}")

# Venda 2: Ontem
venda2 = Venda(
    usuario_id=vendedor.id,
    total=37.00,
    data_venda=datetime.now() - timedelta(days=1)
)
db.add(venda2)
db.flush()

item3 = ItemVenda(
    venda_id=venda2.id,
    produto_id=produtos_criados[1].id,  # Hambúrguer Duplo
    quantidade=1,
    preco_unitario=22.00
)
item4 = ItemVenda(
    venda_id=venda2.id,
    produto_id=produtos_criados[5].id,  # Batata Frita
    quantidade=1,
    preco_unitario=7.00
)
item5 = ItemVenda(
    venda_id=venda2.id,
    produto_id=produtos_criados[3].id,  # Refrigerante
    quantidade=1,
    preco_unitario=8.00
)
db.add(item3)
db.add(item4)
db.add(item5)
vendas_criadas.append(venda2)
print(f"  ✅ Venda 2: 1x Hambúrguer Duplo + 1x Batata + 1x Refri (R$ {venda2.total:.2f})")

db.commit()
print(f"✅ {len(vendas_criadas)} vendas criadas com {len(vendas_criadas) * 2.5:.0f} itens")

# ============================================================================
# 5. CRIAR ORDENS DE REPOSIÇÃO
# ============================================================================
print("\n📫 Criando ordens de reposição...")

# Buscar estoques
estoques = db.query(Estoque).all()

ordem1 = OrdemReposicao(
    estoque_id=estoques[0].id,
    produto_id=produtos_criados[0].id,
    quantidade_solicitada=30,
    status='confirmada',
    motivo='automática',
    data_confirmacao=datetime.now() - timedelta(days=1)
)
db.add(ordem1)

ordem2 = OrdemReposicao(
    estoque_id=estoques[3].id,
    produto_id=produtos_criados[3].id,
    quantidade_solicitada=20,
    status='pendente',
    motivo='automática'
)
db.add(ordem2)

db.commit()
print(f"  ✅ Ordem 1: 30x {produtos_criados[0].nome} (confirmada)")
print(f"  ✅ Ordem 2: 20x {produtos_criados[3].nome} (pendente)")
print(f"✅ 2 ordens de reposição criadas")

# ============================================================================
# RELATÓRIO FINAL
# ============================================================================
print("\n" + "=" * 60)
print("📊 RESUMO FINAL")
print("=" * 60)

usuarios_total = db.query(Usuario).count()
produtos_total = db.query(Produto).count()
estoque_total = db.query(Estoque).count()
vendas_total = db.query(Venda).count()
itens_venda_total = db.query(ItemVenda).count()
reposicoes_total = db.query(OrdemReposicao).count()

print(f"\n✅ Usuários criados: {usuarios_total}")
for u in db.query(Usuario).all():
    print(f"   - {u.email} ({u.role})")

print(f"\n✅ Produtos criados: {produtos_total}")
for p in db.query(Produto).all():
    print(f"   - {p.nome} (R$ {p.preco:.2f})")

print(f"\n✅ Registros de estoque: {estoque_total}")
total_items_estoque = sum(e.quantidade for e in db.query(Estoque).all())
print(f"   Total de itens em estoque: {total_items_estoque}")

print(f"\n✅ Vendas criadas: {vendas_total}")
print(f"   Itens de venda: {itens_venda_total}")
total_vendas = sum(v.total for v in db.query(Venda).all())
print(f"   Total em vendas: R$ {total_vendas:.2f}")

print(f"\n✅ Ordens de reposição: {reposicoes_total}")

print("\n" + "=" * 60)
print("🎉 SEED COMPLETO FINALIZADO COM SUCESSO!")
print("=" * 60)
