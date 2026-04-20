"""
Fixtures compartilhadas para testes - Configuração de test database e clients
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.models.usuario import Usuario
from app.core.security import hash_password


# Database de teste (em memória)
@pytest.fixture(scope="function")
def test_db():
    """Cria um banco de dados SQLite em memória para os testes"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Cria sessão
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield SessionLocal()


@pytest.fixture(scope="function")
def client(test_db: Session):
    """Cria um TestClient com banco de dados de teste"""
    
    def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    
    # Limpa os overrides após o teste
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(test_db: Session) -> Usuario:
    """Cria um usuário admin para testes"""
    usuario = Usuario(
        email="admin@test.com",
        username="admin",
        senha_hash=hash_password("senha123"),
        role="admin",
        ativo=True,
    )
    test_db.add(usuario)
    test_db.commit()
    test_db.refresh(usuario)
    return usuario


@pytest.fixture(scope="function")
def gerente_user(test_db: Session) -> Usuario:
    """Cria um usuário gerente para testes"""
    usuario = Usuario(
        email="gerente@test.com",
        username="gerente",
        senha_hash=hash_password("senha123"),
        role="gerente",
        ativo=True,
    )
    test_db.add(usuario)
    test_db.commit()
    test_db.refresh(usuario)
    return usuario


@pytest.fixture(scope="function")
def caixa_user(test_db: Session) -> Usuario:
    """Cria um usuário caixa para testes"""
    usuario = Usuario(
        email="caixa@test.com",
        username="caixa",
        senha_hash=hash_password("senha123"),
        role="caixa",
        ativo=True,
    )
    test_db.add(usuario)
    test_db.commit()
    test_db.refresh(usuario)
    return usuario


@pytest.fixture(scope="function")
def admin_token(client: TestClient, admin_user: Usuario):
    """Obtém token JWT para usuário admin"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "admin@test.com",
            "senha": "senha123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


@pytest.fixture(scope="function")
def gerente_token(client: TestClient, gerente_user: Usuario):
    """Obtém token JWT para usuário gerente"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "gerente@test.com",
            "senha": "senha123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


@pytest.fixture(scope="function")
def caixa_token(client: TestClient, caixa_user: Usuario):
    """Obtém token JWT para usuário caixa"""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "caixa@test.com",
            "senha": "senha123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    return data["access_token"]


@pytest.fixture(scope="function")
def auth_headers(admin_token: str):
    """Headers de autenticação com token admin"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="function")
def produto_data():
    """Dados de exemplo de um produto"""
    return {
        "nome": "Lanche Completo",
        "descricao": "Lanche com tudo incluído",
        "preco": 25.50,
        "categoria": "lanches",
    }


@pytest.fixture(scope="function")
def usuario_data():
    """Dados de exemplo de um novo usuário"""
    return {
        "email": "novo@test.com",
        "username": "novousuario",
        "senha": "senhaSegura123",
        "role": "caixa",
    }


__all__ = [
    "test_db",
    "client",
    "admin_user",
    "gerente_user",
    "caixa_user",
    "admin_token",
    "gerente_token",
    "caixa_token",
    "auth_headers",
    "produto_data",
    "usuario_data",
]
