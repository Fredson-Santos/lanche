"""
Testes de Usuários - Testes para rotas CRUD de usuários (admin only)
"""

import pytest
from fastapi.testclient import TestClient


class TestUsuariosCreate:
    """Testes para endpoint POST /api/usuarios"""

    def test_criar_usuario_com_admin(self, client: TestClient, admin_token):
        """Testa criação de usuário com permissão admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "email": "novo@test.com",
            "username": "novousuario",
            "senha": "senhaSegura123",
            "role": "caixa",
        }
        
        response = client.post("/api/usuarios/", json=payload, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "novo@test.com"
        assert data["username"] == "novousuario"
        assert data["role"] == "caixa"
        assert data["ativo"] is True

    def test_criar_usuario_sem_autenticacao(self, client: TestClient):
        """Testa que usuário não autenticado não consegue criar usuário"""
        payload = {
            "email": "novo@test.com",
            "username": "novousuario",
            "senha": "senhaSegura123",
            "role": "caixa",
        }
        
        response = client.post("/api/usuarios/", json=payload)
        
        assert response.status_code == 403

    def test_criar_usuario_sem_admin(self, client: TestClient, gerente_token):
        """Testa que usuário sem role admin não consegue criar usuário"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        payload = {
            "email": "novo@test.com",
            "username": "novousuario",
            "senha": "senhaSegura123",
            "role": "caixa",
        }
        
        response = client.post("/api/usuarios/", json=payload, headers=headers)
        
        assert response.status_code == 403

    def test_criar_usuario_email_duplicado(self, client: TestClient, admin_token, admin_user):
        """Testa que não pode criar usuário com email duplicado"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "email": "admin@test.com",  # Email já existe
            "username": "outronome",
            "senha": "senhaSegura123",
            "role": "caixa",
        }
        
        response = client.post("/api/usuarios/", json=payload, headers=headers)
        
        assert response.status_code == 400
        assert "Email já registrado" in response.json()["detail"]

    def test_criar_usuario_username_duplicado(self, client: TestClient, admin_token, admin_user):
        """Testa que não pode criar usuário com username duplicado"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "email": "outro@test.com",
            "username": "admin",  # Username já existe
            "senha": "senhaSegura123",
            "role": "caixa",
        }
        
        response = client.post("/api/usuarios/", json=payload, headers=headers)
        
        assert response.status_code == 400
        assert "Username já registrado" in response.json()["detail"]

    def test_criar_usuario_senha_fraca(self, client: TestClient, admin_token):
        """Testa validação de senha fraca"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "email": "novo@test.com",
            "username": "novousuario",
            "senha": "123",  # Senha muito curta
            "role": "caixa",
        }
        
        response = client.post("/api/usuarios/", json=payload, headers=headers)
        
        assert response.status_code == 422

    def test_criar_usuario_role_invalida(self, client: TestClient, admin_token):
        """Testa criação de usuário com role inválida"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "email": "novo@test.com",
            "username": "novousuario",
            "senha": "senhaSegura123",
            "role": "superuser",  # Role inválida
        }
        
        response = client.post("/api/usuarios/", json=payload, headers=headers)
        
        assert response.status_code == 422


class TestUsuariosRead:
    """Testes para endpoint GET /api/usuarios"""

    def test_listar_usuarios_com_admin(self, client: TestClient, admin_token, admin_user):
        """Testa listagem de usuários com admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/usuarios/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["email"] == admin_user.email

    def test_listar_usuarios_sem_autenticacao(self, client: TestClient):
        """Testa que usuário não autenticado não consegue listar"""
        response = client.get("/api/usuarios/")
        
        assert response.status_code == 403

    def test_listar_usuarios_sem_admin(self, client: TestClient, gerente_token):
        """Testa que gerente não consegue listar usuários"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        response = client.get("/api/usuarios/", headers=headers)
        
        assert response.status_code == 403

    def test_obter_usuario_por_id(self, client: TestClient, admin_token, admin_user):
        """Testa obtenção de usuário específico"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get(f"/api/usuarios/{admin_user.id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == admin_user.id
        assert data["email"] == admin_user.email

    def test_obter_usuario_inexistente(self, client: TestClient, admin_token):
        """Testa busca de usuário que não existe"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.get("/api/usuarios/9999", headers=headers)
        
        assert response.status_code == 404


class TestUsuariosUpdate:
    """Testes para endpoint PUT /api/usuarios/{id}"""

    def test_atualizar_usuario_com_admin(self, client: TestClient, admin_token, caixa_user):
        """Testa atualização de usuário com admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {
            "email": "caixa_novo@test.com",
            "role": "gerente",
        }
        
        response = client.put(
            f"/api/usuarios/{caixa_user.id}",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "caixa_novo@test.com"
        assert data["role"] == "gerente"

    def test_atualizar_usuario_sem_admin(self, client: TestClient, gerente_token, caixa_user):
        """Testa que gerente não consegue atualizar usuário"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        payload = {"role": "admin"}
        
        response = client.put(
            f"/api/usuarios/{caixa_user.id}",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 403

    def test_atualizar_usuario_email_duplicado(self, client: TestClient, admin_token, admin_user, caixa_user):
        """Testa que não pode atualizar para email duplicado"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        payload = {"email": "admin@test.com"}  # Email já existe
        
        response = client.put(
            f"/api/usuarios/{caixa_user.id}",
            json=payload,
            headers=headers
        )
        
        assert response.status_code == 400

    def test_ativar_desativar_usuario(self, client: TestClient, admin_token, caixa_user):
        """Testa ativar/desativar usuário"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Desativa
        response = client.put(
            f"/api/usuarios/{caixa_user.id}",
            json={"ativo": False},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["ativo"] is False
        
        # Ativa
        response = client.put(
            f"/api/usuarios/{caixa_user.id}",
            json={"ativo": True},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["ativo"] is True


class TestUsuariosDelete:
    """Testes para endpoint DELETE /api/usuarios/{id}"""

    def test_deletar_usuario_com_admin(self, client: TestClient, admin_token, test_db):
        """Testa deleção de usuário com admin"""
        # Cria um usuário novo para deletar
        from app.models.usuario import Usuario
        from app.core.security import hash_password
        
        novo_user = Usuario(
            email="delete@test.com",
            username="deluser",
            senha_hash=hash_password("senha123"),
            role="caixa",
            ativo=True,
        )
        test_db.add(novo_user)
        test_db.commit()
        user_id = novo_user.id
        
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.delete(f"/api/usuarios/{user_id}", headers=headers)
        
        assert response.status_code == 200
        
        # Verifica que foi realmente deletado
        response = client.get(f"/api/usuarios/{user_id}", headers=headers)
        assert response.status_code == 404

    def test_deletar_usuario_sem_admin(self, client: TestClient, gerente_token, caixa_user):
        """Testa que gerente não consegue deletar usuário"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        response = client.delete(f"/api/usuarios/{caixa_user.id}", headers=headers)
        
        assert response.status_code == 403

    def test_deletar_usuario_inexistente(self, client: TestClient, admin_token):
        """Testa deleção de usuário que não existe"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = client.delete("/api/usuarios/9999", headers=headers)
        
        assert response.status_code == 404


__all__ = [
    "TestUsuariosCreate",
    "TestUsuariosRead",
    "TestUsuariosUpdate",
    "TestUsuariosDelete",
]
