"""
Testes para alertas - RF-01, RF-02, RF-03
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.models.estoque import Estoque
from app.models.alerta import Alerta, TipoAlerta
from app.schemas.alerta import TipoAlertaSchema
from app.utils.alertas import (
    verificar_alertas_validade,
    verificar_alertas_temperatura,
    marcar_alerta_como_lido,
    limpar_alertas_resolvidos,
    obter_alertas_ativos,
)


class TestAlertasValidade:
    """Testes para alertas de validade"""

    def test_criar_alerta_produto_vencido(self, test_db: Session):
        """Testa criação de alerta para produto vencido"""
        # Cria produto com data de validade no passado
        produto = Produto(
            nome="Produto Vencido",
            preco=10.0,
            categoria="alimentos",
            data_validade=datetime.now().astimezone() - timedelta(days=1),
            lote="LOTE-001",
        )
        test_db.add(produto)
        test_db.commit()

        # Verifica alertas
        alertas = verificar_alertas_validade(test_db)

        # Verifica se alerta foi criado
        assert len(alertas) == 1
        assert alertas[0].tipo == TipoAlerta.VALIDADE
        assert alertas[0].produto_id == produto.id
        assert "venceu" in alertas[0].titulo.lower()

    def test_criar_alerta_produto_proximo_vencer(self, test_db: Session):
        """Testa criação de alerta para produto próximo de vencer"""
        # Cria produto com data de validade em 3 dias
        produto = Produto(
            nome="Produto Próximo de Vencer",
            preco=10.0,
            categoria="alimentos",
            data_validade=datetime.now().astimezone() + timedelta(days=3),
            lote="LOTE-002",
        )
        test_db.add(produto)
        test_db.commit()

        # Verifica alertas
        alertas = verificar_alertas_validade(test_db)

        # Verifica se alerta foi criado (próximo de vencer em 7 dias)
        assert len(alertas) == 1
        assert alertas[0].tipo == TipoAlerta.VALIDADE
        assert "próximo" in alertas[0].titulo.lower() or "vence" in alertas[0].titulo.lower()

    def test_nao_criar_alerta_produto_com_validade_ok(self, test_db: Session):
        """Testa que não cria alerta para produto com validade ok"""
        # Cria produto com data de validade em 20 dias
        produto = Produto(
            nome="Produto OK",
            preco=10.0,
            categoria="alimentos",
            data_validade=datetime.now().astimezone() + timedelta(days=20),
        )
        test_db.add(produto)
        test_db.commit()

        # Verifica alertas
        alertas = verificar_alertas_validade(test_db)

        # Verifica que nenhum alerta foi criado
        assert len(alertas) == 0

    def test_nao_criar_alerta_duplicado(self, test_db: Session):
        """Testa que não cria alertas duplicados"""
        # Cria produto vencido
        produto = Produto(
            nome="Produto Duplicado",
            preco=10.0,
            categoria="alimentos",
            data_validade=datetime.now().astimezone() - timedelta(days=1),
            lote="LOTE-003",
        )
        test_db.add(produto)
        test_db.commit()

        # Verifica alertas primeira vez
        alertas1 = verificar_alertas_validade(test_db)
        assert len(alertas1) == 1

        # Verifica alertas segunda vez
        alertas2 = verificar_alertas_validade(test_db)
        assert len(alertas2) == 0  # Não deve criar duplicado


class TestAlertasTemperatura:
    """Testes para alertas de temperatura"""

    def test_criar_alerta_temperatura_abaixo_minima(self, test_db: Session):
        """Testa criação de alerta para temperatura abaixo do mínimo"""
        # Cria produto com temperatura ideal
        produto = Produto(
            nome="Produto Refrigerado",
            preco=20.0,
            categoria="alimentos",
            temperatura_ideal_min=4.0,
            temperatura_ideal_max=8.0,
        )
        test_db.add(produto)
        test_db.commit()

        # Cria estoque com temperatura abaixo do mínimo
        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            temperatura_atual=2.0,  # Abaixo do mínimo (4.0)
        )
        test_db.add(estoque)
        test_db.commit()

        # Verifica alertas
        alertas = verificar_alertas_temperatura(test_db)

        # Verifica se alerta foi criado
        assert len(alertas) == 1
        assert alertas[0].tipo == TipoAlerta.TEMPERATURA
        assert alertas[0].estoque_id == estoque.id
        assert "abaixo" in alertas[0].descricao.lower()

    def test_criar_alerta_temperatura_acima_maxima(self, test_db: Session):
        """Testa criação de alerta para temperatura acima do máximo"""
        # Cria produto com temperatura ideal
        produto = Produto(
            nome="Produto Congelado",
            preco=25.0,
            categoria="alimentos",
            temperatura_ideal_min=-18.0,
            temperatura_ideal_max=-15.0,
        )
        test_db.add(produto)
        test_db.commit()

        # Cria estoque com temperatura acima do máximo
        estoque = Estoque(
            produto_id=produto.id,
            quantidade=5,
            temperatura_atual=-10.0,  # Acima do máximo (-15.0)
        )
        test_db.add(estoque)
        test_db.commit()

        # Verifica alertas
        alertas = verificar_alertas_temperatura(test_db)

        # Verifica se alerta foi criado
        assert len(alertas) == 1
        assert alertas[0].tipo == TipoAlerta.TEMPERATURA
        assert "acima" in alertas[0].descricao.lower()

    def test_nao_criar_alerta_temperatura_ok(self, test_db: Session):
        """Testa que não cria alerta para temperatura dentro da faixa"""
        # Cria produto com temperatura ideal
        produto = Produto(
            nome="Produto OK",
            preco=15.0,
            categoria="alimentos",
            temperatura_ideal_min=4.0,
            temperatura_ideal_max=8.0,
        )
        test_db.add(produto)
        test_db.commit()

        # Cria estoque com temperatura ok
        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            temperatura_atual=6.0,  # Dentro da faixa
        )
        test_db.add(estoque)
        test_db.commit()

        # Verifica alertas
        alertas = verificar_alertas_temperatura(test_db)

        # Verifica que nenhum alerta foi criado
        assert len(alertas) == 0


class TestGerenciamentoAlertas:
    """Testes para gerenciamento de alertas"""

    def test_marcar_alerta_como_lido(self, test_db: Session):
        """Testa marcação de alerta como lido"""
        # Cria alerta
        alerta = Alerta(
            produto_id=1,
            tipo=TipoAlerta.VALIDADE,
            titulo="Teste",
            lido=False,
        )
        test_db.add(alerta)
        test_db.commit()

        # Marca como lido
        alerta_lido = marcar_alerta_como_lido(test_db, alerta.id)

        # Verifica
        assert alerta_lido is not None
        assert alerta_lido.lido is True
        assert alerta_lido.data_leitura is not None

    def test_limpar_alerta_resolvido(self, test_db: Session):
        """Testa marcação de alerta como resolvido"""
        # Cria alerta
        alerta = Alerta(
            produto_id=1,
            tipo=TipoAlerta.VALIDADE,
            titulo="Teste",
            ativo=True,
        )
        test_db.add(alerta)
        test_db.commit()

        # Marca como resolvido
        alerta_resolvido = limpar_alertas_resolvidos(test_db, alerta.id)

        # Verifica
        assert alerta_resolvido is not None
        assert alerta_resolvido.ativo is False
        assert alerta_resolvido.data_resolucao is not None

    def test_obter_alertas_ativos(self, test_db: Session):
        """Testa obtenção de alertas ativos"""
        # Cria alertas
        alerta1 = Alerta(
            produto_id=1,
            tipo=TipoAlerta.VALIDADE,
            titulo="Alerta 1",
            ativo=True,
            lido=False,
        )
        alerta2 = Alerta(
            produto_id=2,
            tipo=TipoAlerta.TEMPERATURA,
            titulo="Alerta 2",
            ativo=True,
            lido=True,  # Lido
        )
        alerta3 = Alerta(
            produto_id=3,
            tipo=TipoAlerta.VALIDADE,
            titulo="Alerta 3",
            ativo=False,  # Inativo
            lido=False,
        )
        test_db.add_all([alerta1, alerta2, alerta3])
        test_db.commit()

        # Obtém alertas ativos
        alertas = obter_alertas_ativos(test_db)

        # Verifica - apenas alerta1 deve ser retornado
        assert len(alertas) == 1
        assert alertas[0].id == alerta1.id

    def test_obter_alertas_ativos_por_produto(self, test_db: Session):
        """Testa obtenção de alertas ativos de um produto específico"""
        # Cria alertas
        alerta1 = Alerta(
            produto_id=1,
            tipo=TipoAlerta.VALIDADE,
            titulo="Alerta 1",
            ativo=True,
            lido=False,
        )
        alerta2 = Alerta(
            produto_id=2,
            tipo=TipoAlerta.TEMPERATURA,
            titulo="Alerta 2",
            ativo=True,
            lido=False,
        )
        test_db.add_all([alerta1, alerta2])
        test_db.commit()

        # Obtém alertas ativos do produto 1
        alertas = obter_alertas_ativos(test_db, produto_id=1)

        # Verifica
        assert len(alertas) == 1
        assert alertas[0].produto_id == 1
