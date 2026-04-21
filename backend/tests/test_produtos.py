"""
Testes de Produtos - Testes para rotas CRUD de produtos
"""

import pytest
from fastapi.testclient import TestClient


class TestProdutosCreate:
    """Testes para endpoint POST /api/produtos"""

    def test_criar_produto_com_gerente(self, client: TestClient, gerente_token, produto_data):
        """Testa criação de produto com permissão gerente"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == produto_data["nome"]
        assert data["preco"] == produto_data["preco"]
        assert data["categoria"] == produto_data["categoria"]
        assert data["data_validade"] is None

    def test_criar_produto_com_validade(self, client: TestClient, gerente_token, produto_data):
        """Testa criação de produto com data de validade (curta)"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        validade = "2026-12-31"
        produto_data["data_validade"] = validade
        
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["data_validade"].startswith("2026-12-31")

    def test_criar_produto_com_admin(self, client: TestClient, admin_token, produto_data):
        """Testa criação de produto com permissão admin"""
        headers = {"Authorization": f"Bearer {admin_token}"}
        
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == produto_data["nome"]

    def test_criar_produto_com_caixa(self, client: TestClient, caixa_token, produto_data):
        """Testa que caixa não consegue criar produto"""
        headers = {"Authorization": f"Bearer {caixa_token}"}
        
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        
        assert response.status_code == 403

    def test_criar_produto_sem_autenticacao(self, client: TestClient, produto_data):
        """Testa que usuário não autenticado não consegue criar"""
        response = client.post("/api/produtos/", json=produto_data)
        
        assert response.status_code == 401

    def test_criar_produto_dados_incompletos(self, client: TestClient, gerente_token):
        """Testa criação com dados incompletos"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.post(
            "/api/produtos/",
            json={"nome": "Lanche"},  # Faltam campos obrigatórios
            headers=headers
        )
        
        assert response.status_code == 422

    def test_criar_produto_preco_negativo(self, client: TestClient, gerente_token):
        """Testa que preço negativo é rejeitado"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.post(
            "/api/produtos/",
            json={
                "nome": "Lanche",
                "descricao": "Descrição",
                "preco": -10.0,
                "categoria": "lanches",
            },
            headers=headers
        )
        
        assert response.status_code == 422

    def test_criar_produto_cria_estoque(self, client: TestClient, gerente_token, produto_data, test_db):
        """Testa que criar produto também cria registro de estoque"""
        from app.models.estoque import Estoque
        
        headers = {"Authorization": f"Bearer {gerente_token}"}
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        
        assert response.status_code == 201
        produto_id = response.json()["id"]
        
        # Verifica se estoque foi criado
        estoque = test_db.query(Estoque).filter(Estoque.produto_id == produto_id).first()
        assert estoque is not None
        assert estoque.quantidade == 0


class TestProdutosRead:
    """Testes para endpoints GET de produtos"""

    def test_listar_produtos_publico(self, client: TestClient, gerente_token, produto_data):
        """Testa listagem de produtos sem autenticação"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria um produto
        client.post("/api/produtos/", json=produto_data, headers=headers)
        
        # Lista sem autenticação
        response = client.get("/api/produtos/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["nome"] == produto_data["nome"]

    def test_obter_produto_por_id(self, client: TestClient, gerente_token, produto_data):
        """Testa obtenção de produto específico"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria um produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Obtém o produto
        response = client.get(f"/api/produtos/{produto_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == produto_id
        assert data["nome"] == produto_data["nome"]
        assert data["preco"] == produto_data["preco"]

    def test_obter_produto_inexistente(self, client: TestClient):
        """Testa busca de produto que não existe"""
        response = client.get("/api/produtos/9999")
        
        assert response.status_code == 404

    def test_listar_produtos_vazio(self, client: TestClient):
        """Testa listagem quando não há produtos"""
        response = client.get("/api/produtos/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


class TestProdutosUpdate:
    """Testes para endpoint PUT /api/produtos/{id}"""

    def test_atualizar_produto_com_gerente(self, client: TestClient, gerente_token, produto_data):
        """Testa atualização de produto com gerente"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Atualiza
        response = client.put(
            f"/api/produtos/{produto_id}",
            json={"preco": 30.00, "nome": "Lanche Premium"},
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["preco"] == 30.00
        assert data["nome"] == "Lanche Premium"

    def test_atualizar_produto_com_caixa(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa que caixa não consegue atualizar produto"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto com gerente
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Tenta atualizar com caixa
        response = client.put(
            f"/api/produtos/{produto_id}",
            json={"preco": 30.00},
            headers=headers_caixa
        )
        
        assert response.status_code == 403

    def test_atualizar_produto_inexistente(self, client: TestClient, gerente_token):
        """Testa atualização de produto que não existe"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.put(
            "/api/produtos/9999",
            json={"preco": 30.00},
            headers=headers
        )
        
        assert response.status_code == 404


class TestProdutosDelete:
    """Testes para endpoint DELETE /api/produtos/{id}"""

    def test_deletar_produto_com_gerente(self, client: TestClient, gerente_token, produto_data):
        """Testa deleção de produto com gerente"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # Cria produto
        response = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = response.json()["id"]
        
        # Deleta
        response = client.delete(f"/api/produtos/{produto_id}", headers=headers)
        
        assert response.status_code == 204
        
        # Verifica que foi deletado
        response = client.get(f"/api/produtos/{produto_id}")
        assert response.status_code == 404

    def test_deletar_produto_com_vinculos(self, client: TestClient, gerente_token, produto_data, test_db):
        """Testa que não é possível excluir produto com histórico de vendas"""
        from app.models.venda import Venda
        from app.models.item_venda import ItemVenda
        from app.models.usuario import Usuario
        
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        # 1. Cria produto
        resp_prod = client.post("/api/produtos/", json=produto_data, headers=headers)
        produto_id = resp_prod.json()["id"]
        
        # 2. Cria uma venda vinculada (usando models diretamente para simplificar o setup)
        usuario = test_db.query(Usuario).first()
        nova_venda = Venda(usuario_id=usuario.id, total=25.5)
        test_db.add(nova_venda)
        test_db.commit()
        
        item = ItemVenda(venda_id=nova_venda.id, produto_id=produto_id, quantidade=1, preco_unitario=25.5)
        test_db.add(item)
        test_db.commit()
        
        # 3. Tenta deletar o produto via API
        response = client.delete(f"/api/produtos/{produto_id}", headers=headers)
        
        assert response.status_code == 409
        assert "vendas" in response.json()["detail"].lower()

    def test_deletar_produto_com_caixa(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa que caixa não consegue deletar produto"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria produto com gerente
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        # Tenta deletar com caixa
        response = client.delete(f"/api/produtos/{produto_id}", headers=headers_caixa)
        
        assert response.status_code == 403

    def test_deletar_produto_inexistente(self, client: TestClient, gerente_token):
        """Testa deleção de produto que não existe"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.delete("/api/produtos/9999", headers=headers)
        
        assert response.status_code == 404


__all__ = [
    "TestProdutosCreate",
    "TestProdutosRead",
    "TestProdutosUpdate",
    "TestProdutosDelete",
]
