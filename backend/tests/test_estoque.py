"""
Testes de Estoque - Testes para rotas de estoque
"""

import pytest
from fastapi.testclient import TestClient


class TestEstoqueRead:
    """Testes para leitura de estoque"""

    def test_obter_estoque_produto(self, client: TestClient, gerente_token, produto_data):
        """Testa obtenção de estoque de um produto"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Obtém estoque
        response = client.get(f"/api/estoque/{produto_id}", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["produto_id"] == produto_id
        assert data["quantidade"] == 0

    def test_listar_estoque_com_produtos(self, client: TestClient, gerente_token, produto_data):
        """Testa listagem de estoque"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        client.post("/api/produtos/", json=produto_data, headers=headers)
        
        # Lista estoque
        response = client.get("/api/estoque/", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_obter_estoque_produto_inexistente(self, client: TestClient, gerente_token):
        """Testa obtenção de estoque de produto que não existe"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.get("/api/estoque/9999", headers=headers)
        
        assert response.status_code == 404

    def test_estoque_sem_autenticacao(self, client: TestClient):
        """Testa que sem autenticação não consegue acessar estoque"""
        response = client.get("/api/estoque/")
        
        assert response.status_code == 403


class TestEstoqueMovimentacao:
    """Testes para movimentação de estoque"""

    def test_adicionar_estoque(self, client: TestClient, gerente_token, produto_data):
        """Testa adição de estoque"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Adiciona estoque
        response = client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 50},
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["quantidade"] == 50

    def test_remover_estoque(self, client: TestClient, gerente_token, produto_data):
        """Testa remoção de estoque"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Adiciona estoque
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 50},
            headers=headers
        )
        
        # Remove estoque
        response = client.post(
            f"/api/estoque/{produto_id}/remover",
            json={"quantidade": 20},
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["quantidade"] == 30

    def test_remover_estoque_insuficiente(self, client: TestClient, gerente_token, produto_data):
        """Testa remoção com estoque insuficiente"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Adiciona 10 unidades
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 10},
            headers=headers
        )
        
        # Tenta remover 20
        response = client.post(
            f"/api/estoque/{produto_id}/remover",
            json={"quantidade": 20},
            headers=headers
        )
        
        assert response.status_code == 400
        assert "Estoque insuficiente" in response.json()["detail"]

    def test_remover_estoque_negativo(self, client: TestClient, gerente_token, produto_data):
        """Testa remoção com quantidade negativa"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Tenta remover quantidade negativa
        response = client.post(
            f"/api/estoque/{produto_id}/remover",
            json={"quantidade": -10},
            headers=headers
        )
        
        assert response.status_code == 422

    def test_adicionar_estoque_quantidade_zero(self, client: TestClient, gerente_token, produto_data):
        """Testa adição de quantidade zero"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Tenta adicionar zero
        response = client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 0},
            headers=headers
        )
        
        assert response.status_code == 422

    def test_movimentacao_estoque_com_caixa(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa que caixa não consegue fazer movimentação"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto com gerente
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Tenta adicionar com caixa
        response = client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 50},
            headers=headers_caixa
        )
        
        assert response.status_code == 403

    def test_historico_movimentacao(self, client: TestClient, gerente_token, produto_data):
        """Testa histórico de movimentações de estoque"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Faz movimentações
        client.post(f"/api/estoque/{produto_id}/adicionar", json={"quantidade": 50}, headers=headers)
        client.post(f"/api/estoque/{produto_id}/remover", json={"quantidade": 10}, headers=headers)
        
        # Obtém histórico
        response = client.get(f"/api/estoque/{produto_id}/historico", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 2  # Pelo menos 2 movimentações


__all__ = [
    "TestEstoqueRead",
    "TestEstoqueMovimentacao",
]
