"""
Script de inicialização e seed do banco de dados
Popula o banco com dados iniciais (usuários de teste) na primeira execução
"""

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.estoque import Estoque


def init_db(db: Session) -> None:
    """
    Inicializa o banco de dados com dados padrão se estiver vazio.
    Cria usuários de teste com diferentes roles.

    Args:
        db: Sessão do banco de dados
    """
    # Verifica se já existem usuários
    usuarios_count = db.query(Usuario).count()
    if usuarios_count > 0:
        return  # Banco já inicializado

    # Cria usuários padrão
    usuarios_padrao = [
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
    ]

    for usuario in usuarios_padrao:
        db.add(usuario)

    db.commit()

    # Cria produtos padrão
    produtos_padrao = [
        Produto(
            nome="Hambúrguer Simples",
            descricao="Hambúrguer com pão, carne e molho",
            preco=15.50,
            categoria="lanches",
        ),
        Produto(
            nome="X-Frango",
            descricao="Sanduíche com frango, queijo e molho",
            preco=18.00,
            categoria="lanches",
        ),
        Produto(
            nome="Refrigerante 350ml",
            descricao="Refrigerante gelado",
            preco=5.00,
            categoria="bebidas",
        ),
        Produto(
            nome="Batata Frita",
            descricao="Batata frita crocante",
            preco=8.00,
            categoria="acompanhamentos",
        ),
        Produto(
            nome="Milkshake",
            descricao="Milkshake de chocolate",
            preco=12.00,
            categoria="bebidas",
        ),
    ]

    for produto in produtos_padrao:
        db.add(produto)

    db.commit()

    # Cria registros de estoque
    produtos = db.query(Produto).all()
    for produto in produtos:
        estoque = Estoque(
            produto_id=produto.id,
            quantidade=50,  # Quantidade inicial
        )
        db.add(estoque)

    db.commit()
