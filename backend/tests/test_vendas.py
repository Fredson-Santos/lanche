"""
Testes de Vendas - Testes para rotas de vendas
"""

import pytest
from fastapi.testclient import TestClient


class TestVendasCreate:
    """Testes para criação de vendas"""

    def test_criar_venda_simples(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa criação de uma venda simples"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Adiciona estoque
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        # Cria venda
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 2, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        
        response = client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        assert response.status_code == 201
        data = response.json()
        assert data["total"] == 51.00
        assert len(data["itens"]) == 1

    def test_criar_venda_multiplos_itens(self, client: TestClient, caixa_token, gerente_token, test_db):
        """Testa criação de venda com múltiplos itens"""
        from app.models.produto import Produto
        from app.models.estoque import Estoque
        
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria 2 produtos
        produtos = []
        for i in range(2):
            p = Produto(
                nome=f"Produto {i+1}",
                descricao=f"Desc {i+1}",
                preco=10.00 * (i + 1),
                categoria="lanches"
            )
            test_db.add(p)
            test_db.flush()
            
            e = Estoque(produto_id=p.id, quantidade=100)
            test_db.add(e)
            produtos.append(p)
        test_db.commit()
        
        # Cria venda com múltiplos itens
        venda_data = {
            "itens": [
                {"produto_id": produtos[0].id, "quantidade": 2, "preco_unitario": 10.00},
                {"produto_id": produtos[1].id, "quantidade": 1, "preco_unitario": 20.00},
            ],
            "metodo_pagamento": "cartao",
        }
        
        response = client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        assert response.status_code == 201
        data = response.json()
        assert data["total"] == 40.00  # 2*10 + 1*20
        assert len(data["itens"]) == 2

    def test_criar_venda_estoque_insuficiente(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa criação de venda com estoque insuficiente"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Adiciona apenas 1 unidade
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 1},
            headers=headers_gerente
        )
        
        # Tenta criar venda com 5 unidades
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 5, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        
        response = client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        assert response.status_code == 400
        assert "Estoque insuficiente" in response.json()["detail"]

    def test_criar_venda_desconta_estoque(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa que criação de venda desconta o estoque"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Adiciona estoque
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        # Verifica estoque antes
        response = client.get(f"/api/estoque/{produto_id}", headers=headers_gerente)
        estoque_antes = response.json()["quantidade"]
        
        # Cria venda
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 10, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        # Verifica estoque depois
        response = client.get(f"/api/estoque/{produto_id}", headers=headers_gerente)
        estoque_depois = response.json()["quantidade"]
        
        assert estoque_depois == estoque_antes - 10

    def test_criar_venda_sem_itens(self, client: TestClient, caixa_token):
        """Testa criação de venda sem itens"""
        headers = {"Authorization": f"Bearer {caixa_token}"}
        
        venda_data = {
            "itens": [],
            "metodo_pagamento": "dinheiro",
        }
        
        response = client.post("/api/vendas/", json=venda_data, headers=headers)
        
        assert response.status_code == 422

    def test_criar_venda_com_gerente(self, client: TestClient, gerente_token, produto_data):
        """Testa que gerente não consegue criar venda"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Adiciona estoque
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        # Tenta criar venda
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 2, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        
        response = client.post("/api/vendas/", json=venda_data, headers=headers_gerente)
        
        assert response.status_code == 403


class TestVendasRead:
    """Testes para leitura de vendas"""

    def test_listar_vendas(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa listagem de vendas"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto e venda
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 2, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        # Lista vendas
        response = client.get("/api/vendas/", headers=headers_caixa)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_obter_venda_por_id(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa obtenção de venda específica"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria venda
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 2, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        response = client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        venda_id = response.json()["id"]
        
        # Obtém venda
        response = client.get(f"/api/vendas/{venda_id}", headers=headers_caixa)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == venda_id
        assert data["total"] == 51.00

    def test_obter_venda_inexistente(self, client: TestClient, caixa_token):
        """Testa obtenção de venda que não existe"""
        headers = {"Authorization": f"Bearer {caixa_token}"}
        
        response = client.get("/api/vendas/9999", headers=headers)
        
        assert response.status_code == 404


class TestVendasMetodos:
    """Testes para diferentes métodos de pagamento"""

    @pytest.mark.parametrize("metodo", ["dinheiro", "cartao", "cheque"])
    def test_criar_venda_diferentes_metodos(self, client: TestClient, caixa_token, gerente_token, produto_data, metodo):
        """Testa criação de venda com diferentes métodos de pagamento"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        # Cria venda
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 1, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": metodo,
        }
        
        response = client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        assert response.status_code == 201
        data = response.json()
        assert data["metodo_pagamento"] == metodo


__all__ = [
    "TestVendasCreate",
    "TestVendasRead",
    "TestVendasMetodos",
]
