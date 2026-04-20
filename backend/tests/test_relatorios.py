"""
Testes de Relatórios - Testes para rotas de relatórios
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta


class TestRelatoriosVendas:
    """Testes para relatórios de vendas"""

    def test_relatorio_vendas_diarias(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa relatório de vendas do dia"""
        headers_gerente = {"Authorization": f"Bearer {gerente_token}"}
        headers_caixa = {"Authorization": f"Bearer {caixa_token}"}
        
        # Cria e executa venda
        response = client.post("/api/produtos/", json=produto_data, headers=headers_gerente)
        produto_id = response.json()["id"]
        
        client.post(
            f"/api/estoque/{produto_id}/adicionar",
            json={"quantidade": 100},
            headers=headers_gerente
        )
        
        venda_data = {
            "itens": [
                {"produto_id": produto_id, "quantidade": 5, "preco_unitario": 25.50}
            ],
            "metodo_pagamento": "dinheiro",
        }
        client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        # Obtém relatório do dia
        response = client.get("/api/relatorios/vendas/diarias", headers=headers_gerente)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_vendas" in data
        assert "quantidade_transacoes" in data
        assert data["total_vendas"] == 127.50  # 5 * 25.50

    def test_relatorio_vendas_por_periodo(self, client: TestClient, gerente_token):
        """Testa relatório de vendas por período"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        data_inicio = (datetime.now() - timedelta(days=30)).isoformat()
        data_fim = datetime.now().isoformat()
        
        response = client.get(
            f"/api/relatorios/vendas/periodo?data_inicio={data_inicio}&data_fim={data_fim}",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "total_vendas" in data
        assert "quantidade_transacoes" in data
        assert isinstance(data["vendas"], list)

    def test_relatorio_vendas_por_metodo(self, client: TestClient, caixa_token, gerente_token, produto_data):
        """Testa relatório de vendas por método de pagamento"""
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
        
        # Cria vendas com diferentes métodos
        for metodo in ["dinheiro", "cartao"]:
            venda_data = {
                "itens": [
                    {"produto_id": produto_id, "quantidade": 1, "preco_unitario": 25.50}
                ],
                "metodo_pagamento": metodo,
            }
            client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        # Obtém relatório
        response = client.get(
            "/api/relatorios/vendas/por-metodo",
            headers=headers_gerente
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_relatorio_sem_autenticacao(self, client: TestClient):
        """Testa que não consegue acessar relatório sem autenticação"""
        response = client.get("/api/relatorios/vendas/diarias")
        
        assert response.status_code == 403

    def test_relatorio_com_caixa(self, client: TestClient, caixa_token):
        """Testa que caixa não consegue acessar relatórios"""
        headers = {"Authorization": f"Bearer {caixa_token}"}
        
        response = client.get("/api/relatorios/vendas/diarias", headers=headers)
        
        assert response.status_code == 403


class TestRelatorioProdutos:
    """Testes para relatórios de produtos"""

    def test_relatorio_produtos_populares(self, client: TestClient, gerente_token, caixa_token, produto_data):
        """Testa relatório de produtos mais vendidos"""
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
        
        # Cria múltiplas vendas
        for _ in range(5):
            venda_data = {
                "itens": [
                    {"produto_id": produto_id, "quantidade": 2, "preco_unitario": 25.50}
                ],
                "metodo_pagamento": "dinheiro",
            }
            client.post("/api/vendas/", json=venda_data, headers=headers_caixa)
        
        # Obtém relatório
        response = client.get(
            "/api/relatorios/produtos/populares",
            headers=headers_gerente
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_relatorio_estoque_critico(self, client: TestClient, gerente_token):
        """Testa relatório de produtos com estoque crítico"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.get(
            "/api/relatorios/produtos/estoque-critico",
            headers=headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


class TestRelatorioMetricas:
    """Testes para métricas gerais"""

    def test_relatorio_dashboard(self, client: TestClient, gerente_token):
        """Testa relatório de dashboard com métricas gerais"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.get("/api/relatorios/dashboard", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "total_vendas" in data
        assert "total_transacoes" in data
        assert "produtos_cadastrados" in data
        assert "usuarios_ativos" in data

    def test_relatorio_resumo_mensal(self, client: TestClient, gerente_token):
        """Testa resumo mensal de vendas"""
        headers = {"Authorization": f"Bearer {gerente_token}"}
        
        response = client.get("/api/relatorios/vendas/mensal", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "mes" in data or "month" in data or "total" in data


__all__ = [
    "TestRelatoriosVendas",
    "TestRelatorioProdutos",
    "TestRelatorioMetricas",
]
