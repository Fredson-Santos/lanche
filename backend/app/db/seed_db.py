"""
Script de seed para popular o banco de dados com dados iniciais
Pode ser executado independentemente: python seed_db.py
"""

from sqlalchemy.orm import Session
from app.db.database import SessionLocal, Base, engine
from app.core.security import hash_password
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.models.venda import Venda
from app.models.item_venda import ItemVenda
from datetime import datetime, timedelta
import random


def criar_usuarios(db: Session):
    """Cria usuários padrão e de teste"""
    print("📝 Criando usuários...")
    
    usuarios = [
        Usuario(
            email="admin@lanche.com",
            username="admin",
            senha_hash=hash_password("admin123"),
            role="admin",
            ativo=True,
        ),
        Usuario(
            email="gerente@lanche.com",
            username="gerente",
            senha_hash=hash_password("gerente123"),
            role="gerente",
            ativo=True,
        ),
        Usuario(
            email="caixa@lanche.com",
            username="caixa",
            senha_hash=hash_password("caixa123"),
            role="caixa",
            ativo=True,
        ),
        Usuario(
            email="caixa2@lanche.com",
            username="caixa2",
            senha_hash=hash_password("caixa456"),
            role="caixa",
            ativo=True,
        ),
    ]
    
    for usuario in usuarios:
        db.add(usuario)
    
    db.commit()
    print(f"✅ {len(usuarios)} usuários criados")
    return usuarios


def criar_produtos(db: Session):
    """Cria produtos de exemplo"""
    print("📝 Criando produtos...")
    
    produtos = [
        Produto(
            nome="Hambúrguer Simples",
            descricao="Hambúrguer com pão, carne grelhada e molho especial",
            preco=15.50,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="X-Frango",
            descricao="Sanduíche com frango desfiado, queijo derretido e molho",
            preco=18.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="X-Tudo",
            descricao="Sanduíche com carne, frango, queijo, bacon e ovo",
            preco=22.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Misto Quente",
            descricao="Pão tostado com presunto e queijo derretido",
            preco=12.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Cachorro Quente",
            descricao="Pão com salsicha e molho especial",
            preco=10.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Refrigerante 350ml",
            descricao="Refrigerante gelado (Coca, Guaraná ou Fanta)",
            preco=5.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Refrigerante 2L",
            descricao="Garrafa de refrigerante 2 litros",
            preco=12.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Suco Natural",
            descricao="Suco natural de laranja ou abacaxi",
            preco=8.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Milkshake",
            descricao="Milkshake cremoso (Morango, Chocolate ou Baunilha)",
            preco=12.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Café",
            descricao="Café coado quentinho",
            preco=3.50,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Batata Frita",
            descricao="Batata frita crocante com sal",
            preco=8.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Onion Rings",
            descricao="Anéis de cebola fritos e crocantes",
            preco=9.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Fritas com Queijo",
            descricao="Batata frita coberta com queijo derretido",
            preco=12.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Sorvete",
            descricao="Sorvete casquinha (Baunilha, Chocolate ou Morango)",
            preco=7.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Pudim",
            descricao="Pudim de leite condensado com calda de caramelo",
            preco=6.00,
            categoria="sobremesas",
            ativo=True,
        ),
    ]
    
    for produto in produtos:
        db.add(produto)
    
    db.commit()
    print(f"✅ {len(produtos)} produtos criados")
    return produtos


def criar_estoques(db: Session, produtos):
    """Cria registros de estoque para os produtos"""
    print("📝 Criando estoques...")
    
    estoques = []
    for produto in produtos:
        quantidade_inicial = random.randint(20, 100)
        estoque = Estoque(
            produto_id=produto.id,
            quantidade=quantidade_inicial,
        )
        estoques.append(estoque)
        db.add(estoque)
    
    db.commit()
    print(f"✅ {len(estoques)} registros de estoque criados")
    return estoques


def criar_vendas_exemplo(db: Session, usuarios, produtos):
    """Cria vendas de exemplo dos últimos 7 dias"""
    print("📝 Criando vendas de exemplo...")
    
    vendas_criadas = 0
    caixa_user = next((u for u in usuarios if u.role == "caixa"), usuarios[0])
    
    # Criar vendas para os últimos 7 dias
    for dia in range(7):
        data_venda = datetime.now() - timedelta(days=dia)
        
        # 3-8 vendas por dia
        num_vendas = random.randint(3, 8)
        
        for _ in range(num_vendas):
            # 1-4 itens por venda
            num_itens = random.randint(1, 4)
            total_venda = 0
            
            # Selecionar produtos e calcular total antes de criar a venda
            produtos_selecionados = random.sample(produtos, min(num_itens, len(produtos)))
            itens_data = []
            
            for produto in produtos_selecionados:
                quantidade = random.randint(1, 3)
                itens_data.append({
                    "produto_id": produto.id,
                    "quantidade": quantidade,
                    "preco_unitario": produto.preco,
                })
                total_venda += produto.preco * quantidade
            
            # Criar venda com total já calculado
            venda = Venda(
                usuario_id=caixa_user.id,
                total=total_venda,
                data_venda=data_venda,
            )
            db.add(venda)
            db.flush()  # Para obter o ID da venda
            
            # Criar itens da venda
            for item_data in itens_data:
                item_venda = ItemVenda(
                    venda_id=venda.id,
                    produto_id=item_data["produto_id"],
                    quantidade=item_data["quantidade"],
                    preco_unitario=item_data["preco_unitario"],
                )
                db.add(item_venda)
            
            vendas_criadas += 1
    
    db.commit()
    print(f"✅ {vendas_criadas} vendas de exemplo criadas")


def limpar_banco(db: Session):
    """Limpa todas as tabelas antes de fazer seed"""
    print("🗑️  Limpando banco de dados...")
    
    try:
        # Deletar na ordem certa de dependências
        db.query(ItemVenda).delete()
        db.query(Venda).delete()
        db.query(Estoque).delete()
        db.query(Produto).delete()
        db.query(Usuario).delete()
        db.commit()
        print("✅ Banco limpo com sucesso")
    except Exception as e:
        db.rollback()
        print(f"⚠️  Erro ao limpar banco: {e}")


def seed_db():
    """Executa o seed completo do banco de dados"""
    print("\n" + "="*50)
    print("🌱 Iniciando seed do banco de dados...")
    print("="*50 + "\n")
    
    # Criar todas as tabelas
    print("📋 Criando estrutura do banco...")
    Base.metadata.create_all(bind=engine)
    print("✅ Estrutura criada\n")
    
    db = SessionLocal()
    
    try:
        # Limpar banco
        limpar_banco(db)
        print()
        
        # Criar dados
        usuarios = criar_usuarios(db)
        produtos = criar_produtos(db)
        estoques = criar_estoques(db, produtos)
        criar_vendas_exemplo(db, usuarios, produtos)
        
        print("\n" + "="*50)
        print("✨ Seed concluído com sucesso!")
        print("="*50)
        print("\n📊 Resumo dos dados criados:")
        print(f"   - Usuários: {len(usuarios)}")
        print(f"   - Produtos: {len(produtos)}")
        print(f"   - Estoques: {len(estoques)}")
        print(f"\n🔐 Credenciais padrão:")
        print(f"   - admin@lanche.com / admin123")
        print(f"   - gerente@lanche.com / gerente123")
        print(f"   - caixa@lanche.com / caixa123")
        print(f"   - caixa2@lanche.com / caixa456\n")
        
    except Exception as e:
        print(f"\n❌ Erro durante o seed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
