"""
Script de seed para popular o banco de dados com dados iniciais
Pode ser executado independentemente: python seed_db.py
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
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
        # Administradores
        Usuario(
            email="admin@lanche.com",
            username="admin",
            senha_hash=hash_password("admin123"),
            role="admin",
            ativo=True,
        ),
        Usuario(
            email="admin2@lanche.com",
            username="admin_backup",
            senha_hash=hash_password("admin456"),
            role="admin",
            ativo=True,
        ),
        # Gerentes
        Usuario(
            email="gerente@lanche.com",
            username="gerente",
            senha_hash=hash_password("gerente123"),
            role="gerente",
            ativo=True,
        ),
        Usuario(
            email="gerente2@lanche.com",
            username="gerente_noite",
            senha_hash=hash_password("gerente456"),
            role="gerente",
            ativo=True,
        ),
        # Caixas (operadores de ponto de venda)
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
        Usuario(
            email="caixa3@lanche.com",
            username="caixa3",
            senha_hash=hash_password("caixa789"),
            role="caixa",
            ativo=True,
        ),
        Usuario(
            email="caixa_noite@lanche.com",
            username="caixa_turno_noite",
            senha_hash=hash_password("noite123"),
            role="caixa",
            ativo=True,
        ),
        # Usuário inativo para teste
        Usuario(
            email="inativo@lanche.com",
            username="usuario_inativo",
            senha_hash=hash_password("inativo123"),
            role="caixa",
            ativo=False,
        ),
    ]
    
    for usuario in usuarios:
        db.add(usuario)
    
    db.commit()
    print(f"✅ {len(usuarios)} usuários criados")
    return usuarios


def criar_produtos(db: Session):
    """Cria produtos de exemplo com mais variedade"""
    print("📝 Criando produtos...")
    
    produtos = [
        # LANCHES PRINCIPAIS (15 itens)
        Produto(
            nome="Hambúrguer Simples",
            descricao="Hambúrguer com pão, carne grelhada e molho especial",
            preco=15.50,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Hambúrguer Duplo",
            descricao="Hambúrguer com 2 carnes, queijo, alface e tomate",
            preco=22.00,
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
            nome="X-Bacon",
            descricao="Carne grelhada, bacon crocante e queijo derretido",
            preco=19.50,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="X-Tudo",
            descricao="Carne, frango, bacon, queijo, ovo, alface, tomate e molho",
            preco=25.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="X-Salada",
            descricao="Carne, alface, tomate, cebola, picles e molho verde",
            preco=17.00,
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
            descricao="Pão com salsicha, molho e crocante",
            preco=10.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Cachorro Quente Completo",
            descricao="Salsicha, bacon, queijo, ovo e crocante",
            preco=15.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Queijo Quente",
            descricao="Queijo derretido no pão com molho especial",
            preco=11.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Vegano Especial",
            descricao="Pão integral, alface, tomate, cebola, abacate e molho vegano",
            preco=18.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Frango Crocante",
            descricao="Peito de frango frito, alface, tomate e maionese",
            preco=19.50,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Carne Seca",
            descricao="Carne seca desfiada, queijo, cebola roxa e molho especial",
            preco=21.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Tira Caldo",
            descricao="Caldo crocante, carne, queijo e molho picante",
            preco=14.00,
            categoria="lanches",
            ativo=True,
        ),
        Produto(
            nome="Super Lanche",
            descricao="Combinação premium com todos os acompanhamentos",
            preco=28.00,
            categoria="lanches",
            ativo=True,
        ),
        
        # BEBIDAS (12 itens)
        Produto(
            nome="Refrigerante 350ml",
            descricao="Refrigerante gelado (Coca, Guaraná ou Fanta)",
            preco=5.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Refrigerante 500ml",
            descricao="Refrigerante gelado em garrafa 500ml",
            preco=7.00,
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
            nome="Suco Natural Laranja",
            descricao="Suco natural de laranja espremida na hora",
            preco=8.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Suco Natural Abacaxi",
            descricao="Suco natural de abacaxi gelado",
            preco=8.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Suco Natural Melancia",
            descricao="Refrescante suco de melancia",
            preco=8.50,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Milkshake Morango",
            descricao="Milkshake cremoso com morango fresco",
            preco=12.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Milkshake Chocolate",
            descricao="Milkshake cremoso de chocolate belga",
            preco=12.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Milkshake Baunilha",
            descricao="Milkshake cremoso de baunilha",
            preco=12.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Café Coado",
            descricao="Café coado quentinho tradicional",
            preco=3.50,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Café com Leite",
            descricao="Café coado com leite quente",
            preco=5.00,
            categoria="bebidas",
            ativo=True,
        ),
        Produto(
            nome="Água Mineral",
            descricao="Água mineral gelada 500ml",
            preco=2.50,
            categoria="bebidas",
            ativo=True,
        ),
        
        # ACOMPANHAMENTOS (9 itens)
        Produto(
            nome="Batata Frita Pequena",
            descricao="Batata frita crocante com sal - porção pequena",
            preco=8.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Batata Frita Grande",
            descricao="Batata frita crocante com sal - porção grande",
            preco=12.00,
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
            nome="Fritas com Bacon",
            descricao="Batata frita com bacon crocante e queijo",
            preco=13.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Fritas com Cheddar",
            descricao="Fritas com molho cheddar derretido",
            preco=11.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Polenta Frita",
            descricao="Cubos de polenta fritos e dourados",
            preco=9.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Salada Verde",
            descricao="Alface, tomate, cebola e molho vinagrete",
            preco=7.50,
            categoria="acompanhamentos",
            ativo=True,
        ),
        Produto(
            nome="Salada Caesar",
            descricao="Alface, croutons, queijo parmesão e molho caesar",
            preco=10.00,
            categoria="acompanhamentos",
            ativo=True,
        ),
        
        # SOBREMESAS (8 itens)
        Produto(
            nome="Sorvete Baunilha",
            descricao="Sorvete cremoso baunilha em casquinha",
            preco=7.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Sorvete Chocolate",
            descricao="Sorvete cremoso chocolate belga em casquinha",
            preco=7.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Sorvete Morango",
            descricao="Sorvete cremoso morango fresco em casquinha",
            preco=7.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Pudim de Leite",
            descricao="Pudim caseiro com leite condensado e calda de caramelo",
            preco=6.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Brownie Chocolate",
            descricao="Brownies de chocolate com calda quente",
            preco=8.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Pavê",
            descricao="Pavê tradicional com biscoito, leite condensado e chocolate",
            preco=7.50,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Mousse de Chocolate",
            descricao="Mousse aéreo e cremoso de chocolate",
            preco=7.00,
            categoria="sobremesas",
            ativo=True,
        ),
        Produto(
            nome="Açaí",
            descricao="Açaí batido com granola e mel",
            preco=14.00,
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
    """Cria registros de estoque para os produtos com quantidades realistas"""
    print("📝 Criando estoques...")
    
    estoques = []
    
    # Categorizar produtos para quantidades mais realistas
    for i, produto in enumerate(produtos):
        # Produtos mais populares têm estoque maior
        if "Hambúrguer" in produto.nome or "Fritas" in produto.nome or "Refrigerante" in produto.nome:
            quantidade_inicial = random.randint(50, 150)
        # Bebidas quentes têm menos estoque
        elif "Café" in produto.nome or "Água" in produto.nome:
            quantidade_inicial = random.randint(30, 80)
        # Sobremesas e acompanhamentos
        elif produto.categoria in ["sobremesas", "acompanhamentos"]:
            quantidade_inicial = random.randint(25, 60)
        # Lanches diversos
        else:
            quantidade_inicial = random.randint(35, 100)
        
        # Simular alguns produtos com estoque baixo (realista)
        if i % 7 == 0:  # 1 a cada 7 produtos
            quantidade_inicial = random.randint(5, 15)
        
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
    """Cria vendas de exemplo com padrões realistas dos últimos 30 dias"""
    print("📝 Criando vendas de exemplo...")
    
    vendas_criadas = 0
    caixas = [u for u in usuarios if u.role == "caixa"]
    
    if not caixas:
        print("⚠️  Nenhum caixa encontrado para criar vendas")
        return
    
    # Criar vendas para os últimos 30 dias
    for dia in range(30):
        data_base = datetime.now() - timedelta(days=dia)
        
        # Padrão de vendas: mais vendas em dias de semana e horários de pico
        dia_semana = data_base.weekday()  # 0=seg, 4=sex, 5=sab, 6=dom
        
        # Ajustar quantidade de vendas por dia
        if dia_semana == 5:  # Sábado - mais vendas
            num_vendas = random.randint(15, 25)
        elif dia_semana == 6:  # Domingo - vendas normais
            num_vendas = random.randint(12, 18)
        elif dia_semana in [3, 4]:  # Quinta/Sexta - movimento bom
            num_vendas = random.randint(10, 16)
        else:  # Seg-Qua - movimento normal
            num_vendas = random.randint(8, 14)
        
        for venda_idx in range(num_vendas):
            # Distribuir vendas ao longo do dia com mais pico no almoço (11-14h) e café (16-18h)
            hora = random.choice(
                [random.randint(11, 13)] * 4 +  # Almoço (4x mais provável)
                [random.randint(7, 10)] * 2 +   # Café da manhã
                [random.randint(16, 18)] * 3 +  # Café/lanche (3x mais provável)
                [random.randint(19, 21)] * 2 +  # Noite
                [random.randint(22, 23)]        # Madrugada
            )
            minuto = random.randint(0, 59)
            
            data_venda = data_base.replace(hour=hora, minute=minuto, second=0)
            
            # 1-5 itens por venda (mais realista)
            num_itens = random.choices(
                [1, 2, 3, 4, 5],
                weights=[20, 35, 25, 15, 5]  # Maioria de 2-3 itens
            )[0]
            
            total_venda = 0
            produtos_selecionados = random.sample(produtos, min(num_itens, len(produtos)))
            itens_data = []
            
            for produto in produtos_selecionados:
                quantidade = random.choices(
                    [1, 2, 3, 4],
                    weights=[60, 25, 10, 5]  # Maioria de 1-2 unidades
                )[0]
                itens_data.append({
                    "produto_id": produto.id,
                    "quantidade": quantidade,
                    "preco_unitario": produto.preco,
                })
                total_venda += produto.preco * quantidade
            
            # Selecionar caixa aleatoriamente
            caixa_user = random.choice(caixas)
            
            # Criar venda
            venda = Venda(
                usuario_id=caixa_user.id,
                total=round(total_venda, 2),
                data_venda=data_venda,
            )
            db.add(venda)
            db.flush()
            
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
    
    # Calcular e exibir estatísticas
    total_vendido = db.query(func.sum(Venda.total)).scalar() or 0
    ticket_medio = total_vendido / vendas_criadas if vendas_criadas > 0 else 0
    
    print(f"\n📊 Estatísticas de vendas:")
    print(f"   - Total de vendas: R$ {total_vendido:.2f}")
    print(f"   - Ticket médio: R$ {ticket_medio:.2f}")
    print(f"   - Número de transações: {vendas_criadas}")



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
    print("\n" + "="*60)
    print("🌱 INICIANDO SEED COMPLETO DO BANCO DE DADOS")
    print("="*60 + "\n")
    
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
        
        # Calcular estatísticas
        total_usuarios = len(usuarios)
        total_produtos = len(produtos)
        total_estoques = len(estoques)
        total_vendas = db.query(func.count(Venda.id)).scalar() or 0
        total_itens_vendidos = db.query(func.count(ItemVenda.id)).scalar() or 0
        total_faturado = db.query(func.sum(Venda.total)).scalar() or 0
        ticket_medio = total_faturado / total_vendas if total_vendas > 0 else 0
        
        print("\n" + "="*60)
        print("✨ SEED CONCLUÍDO COM SUCESSO!")
        print("="*60)
        
        print("\n📊 RESUMO COMPLETO DOS DADOS CRIADOS:")
        print(f"   ├─ Usuários: {total_usuarios}")
        print(f"   │  ├─ Administradores: {len([u for u in usuarios if u.role == 'admin'])}")
        print(f"   │  ├─ Gerentes: {len([u for u in usuarios if u.role == 'gerente'])}")
        print(f"   │  ├─ Caixas: {len([u for u in usuarios if u.role == 'caixa'])}")
        print(f"   │  └─ Inativos: {len([u for u in usuarios if not u.ativo])}")
        print(f"   ├─ Produtos: {total_produtos}")
        
        # Contar por categoria
        categorias = {}
        for prod in produtos:
            categorias[prod.categoria] = categorias.get(prod.categoria, 0) + 1
        
        for i, (cat, qtd) in enumerate(sorted(categorias.items())):
            if i == len(categorias) - 1:
                print(f"   │  └─ {cat.capitalize()}: {qtd}")
            else:
                print(f"   │  ├─ {cat.capitalize()}: {qtd}")
        
        print(f"   ├─ Estoques: {total_estoques}")
        print(f"   └─ Vendas: {total_vendas}")
        print(f"      ├─ Itens vendidos: {total_itens_vendidos}")
        print(f"      ├─ Faturamento: R$ {total_faturado:.2f}")
        print(f"      └─ Ticket médio: R$ {ticket_medio:.2f}")
        
        print(f"\n🔐 CREDENCIAIS PADRÃO PARA TESTE:")
        print(f"   ├─ Admin:")
        print(f"   │  ├─ admin@lanche.com / admin123")
        print(f"   │  └─ admin2@lanche.com / admin456")
        print(f"   ├─ Gerente:")
        print(f"   │  ├─ gerente@lanche.com / gerente123")
        print(f"   │  └─ gerente2@lanche.com / gerente456")
        print(f"   └─ Caixa:")
        print(f"      ├─ caixa@lanche.com / caixa123")
        print(f"      ├─ caixa2@lanche.com / caixa456")
        print(f"      ├─ caixa3@lanche.com / caixa789")
        print(f"      └─ caixa_noite@lanche.com / noite123")
        
        print(f"\n💾 Base de dados populada com sucesso!")
        print(f"   Dados disponíveis para teste por 30 dias\n")
        
    except Exception as e:
        print(f"\n❌ Erro durante o seed: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
