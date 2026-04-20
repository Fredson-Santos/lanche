"""
Testes de Autenticação - Testes para rotas de login e tokens
"""

import pytest
from fastapi.testclient import TestClient


class TestAuthLogin:
    """Testes para endpoint POST /api/auth/login"""

    def test_login_bem_sucedido(self, client: TestClient, admin_user):
        """Testa login bem-sucedido com credenciais válidas"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "senha": "senha123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["usuario"]["email"] == "admin@test.com"
        assert data["usuario"]["role"] == "admin"
        assert data["usuario"]["ativo"] is True

    def test_login_email_invalido(self, client: TestClient):
        """Testa login com email que não existe"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "inexistente@test.com",
                "senha": "senha123",
            },
        )
        
        assert response.status_code == 401
        assert "Email ou senha inválidos" in response.json()["detail"]

    def test_login_senha_invalida(self, client: TestClient, admin_user):
        """Testa login com senha incorreta"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "senha": "senhaErrada",
            },
        )
        
        assert response.status_code == 401
        assert "Email ou senha inválidos" in response.json()["detail"]

    def test_login_usuario_inativo(self, client: TestClient, test_db, admin_user):
        """Testa login com usuário inativo"""
        # Desativa o usuário
        admin_user.ativo = False
        test_db.commit()
        
        response = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "senha": "senha123",
            },
        )
        
        assert response.status_code == 403
        assert "Usuário inativo" in response.json()["detail"]

    def test_login_dados_invalidos(self, client: TestClient):
        """Testa login com dados inválidos (sem email)"""
        response = client.post(
            "/api/auth/login",
            json={
                "senha": "senha123",
            },
        )
        
        assert response.status_code == 422  # Unprocessable Entity

    def test_login_email_vazio(self, client: TestClient):
        """Testa login com email vazio"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "",
                "senha": "senha123",
            },
        )
        
        assert response.status_code == 422

    def test_login_retorna_dados_usuario(self, client: TestClient, admin_user):
        """Testa se login retorna os dados completos do usuário"""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "admin@test.com",
                "senha": "senha123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()["usuario"]
        
        assert data["id"] == admin_user.id
        assert data["email"] == admin_user.email
        assert data["username"] == admin_user.username
        assert data["role"] == admin_user.role
        assert "data_criacao" in data
        assert "data_atualizacao" in data


class TestAuthTokenValidation:
    """Testes para validação de tokens"""

    def test_requisicao_sem_token(self, client: TestClient):
        """Testa que endpoint protegido nega acesso sem token"""
        response = client.get("/api/usuarios/")
        
        assert response.status_code == 403
        assert "Acesso não autorizado" in response.json()["detail"]

    def test_requisicao_com_token_invalido(self, client: TestClient):
        """Testa que token inválido é rejeitado"""
        headers = {"Authorization": "Bearer token_invalido"}
        response = client.get("/api/usuarios/", headers=headers)
        
        assert response.status_code == 403

    def test_requisicao_com_bearer_invalido(self, client: TestClient, admin_token):
        """Testa que formato Bearer incorreto é rejeitado"""
        headers = {"Authorization": f"Basic {admin_token}"}
        response = client.get("/api/usuarios/", headers=headers)
        
        assert response.status_code == 403

    def test_token_acessa_dados_do_usuario(self, client: TestClient, admin_user, admin_token):
        """Testa que token permite acesso a endpoint protegido"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/usuarios/", headers=headers)
        
        assert response.status_code == 200


class TestAuthMultipleRoles:
    """Testes de autenticação com diferentes roles"""

    def test_diferentes_roles_fazem_login(self, client: TestClient, gerente_user, caixa_user):
        """Testa que usuários com diferentes roles conseguem fazer login"""
        # Login gerente
        response_gerente = client.post(
            "/api/auth/login",
            json={"email": "gerente@test.com", "senha": "senha123"},
        )
        assert response_gerente.status_code == 200
        assert response_gerente.json()["usuario"]["role"] == "gerente"
        
        # Login caixa
        response_caixa = client.post(
            "/api/auth/login",
            json={"email": "caixa@test.com", "senha": "senha123"},
        )
        assert response_caixa.status_code == 200
        assert response_caixa.json()["usuario"]["role"] == "caixa"


__all__ = [
    "TestAuthLogin",
    "TestAuthTokenValidation",
    "TestAuthMultipleRoles",
]
