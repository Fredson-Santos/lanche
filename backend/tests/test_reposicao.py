"""
Testes para reposição automática - RF-06
"""

import pytest
from sqlalchemy.orm import Session

from app.models.estoque import Estoque
from app.models.produto import Produto
from app.models.ordem_reposicao import OrdemReposicao, StatusOrdemReposicao
from app.utils.reposicao import (
    verificar_estoques_minimos,
    criar_ordem_reposicao_manual,
    confirmar_ordem_reposicao,
    receber_ordem_reposicao,
    cancelar_ordem_reposicao,
    obter_ordens_pendentes,
)


class TestReposicaoAutomatica:
    """Testes para reposição automática"""

    def test_criar_ordem_reposicao_manual(self, test_db: Session):
        """Testa criação de ordem de reposição manual"""
        # Cria produto e estoque
        produto = Produto(nome="Produto Teste", preco=10.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=5,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        # Cria ordem manual
        ordem = criar_ordem_reposicao_manual(
            test_db,
            estoque.id,
            produto.id,
            quantidade_solicitada=30,
            observacoes="Reposição manual para teste"
        )

        # Verifica
        assert ordem is not None
        assert ordem.quantidade_solicitada == 30
        assert ordem.motivo == "manual"
        assert ordem.status == StatusOrdemReposicao.PENDENTE

    def test_verificar_estoques_abaixo_minimo(self, test_db: Session):
        """Testa verificação de estoque abaixo do mínimo"""
        # Cria produto e estoque abaixo do mínimo
        produto = Produto(nome="Produto Baixo", preco=15.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=5,  # Abaixo do ponto de reposição (15)
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        # Verifica estoques
        ordens = verificar_estoques_minimos(test_db)

        # Verifica
        assert len(ordens) == 1
        assert ordens[0].estoque_id == estoque.id
        assert ordens[0].quantidade_solicitada == 45  # 50 - 5 = 45
        assert ordens[0].motivo == "automática"

    def test_nao_criar_ordem_duplicada(self, test_db: Session):
        """Testa que não cria ordens duplicadas"""
        # Cria produto e estoque abaixo do mínimo
        produto = Produto(nome="Produto Duplicado", preco=20.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=3,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        # Verifica estoques primeira vez
        ordens1 = verificar_estoques_minimos(test_db)
        assert len(ordens1) == 1

        # Verifica estoques segunda vez
        ordens2 = verificar_estoques_minimos(test_db)
        assert len(ordens2) == 0  # Não deve criar duplicado

    def test_confirmando_ordem(self, test_db: Session):
        """Testa confirmação de ordem"""
        # Cria ordem
        produto = Produto(nome="Produto Confirmação", preco=25.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        ordem = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=30,
            status=StatusOrdemReposicao.PENDENTE
        )
        test_db.add(ordem)
        test_db.commit()

        # Confirma ordem
        ordem_confirmada = confirmar_ordem_reposicao(test_db, ordem.id)

        # Verifica
        assert ordem_confirmada is not None
        assert ordem_confirmada.status == StatusOrdemReposicao.CONFIRMADA
        assert ordem_confirmada.data_confirmacao is not None

    def test_receber_ordem_completa(self, test_db: Session):
        """Testa recebimento completo de uma ordem"""
        # Cria ordem
        produto = Produto(nome="Produto Recebimento", preco=30.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        ordem = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=30,
            status=StatusOrdemReposicao.CONFIRMADA
        )
        test_db.add(ordem)
        test_db.commit()

        quantidade_inicial = estoque.quantidade

        # Recebe ordem
        ordem_recebida = receber_ordem_reposicao(test_db, ordem.id, 30)

        # Verifica
        assert ordem_recebida is not None
        assert ordem_recebida.status == StatusOrdemReposicao.RECEBIDA
        assert ordem_recebida.quantidade_recebida == 30
        assert ordem_recebida.data_recebimento is not None
        
        # Verifica estoque atualizado
        test_db.refresh(estoque)
        assert estoque.quantidade == quantidade_inicial + 30

    def test_receber_ordem_parcial(self, test_db: Session):
        """Testa recebimento parcial de uma ordem"""
        # Cria ordem
        produto = Produto(nome="Produto Parcial", preco=35.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        ordem = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=30,
            status=StatusOrdemReposicao.CONFIRMADA
        )
        test_db.add(ordem)
        test_db.commit()

        quantidade_inicial = estoque.quantidade

        # Recebe ordem parcial
        ordem_atualizada = receber_ordem_reposicao(test_db, ordem.id, 20)

        # Verifica
        assert ordem_atualizada is not None
        assert ordem_atualizada.quantidade_recebida == 20
        assert ordem_atualizada.status != StatusOrdemReposicao.RECEBIDA  # Ainda pendente
        
        # Verifica estoque atualizado
        test_db.refresh(estoque)
        assert estoque.quantidade == quantidade_inicial + 20

    def test_cancelar_ordem(self, test_db: Session):
        """Testa cancelamento de uma ordem"""
        # Cria ordem
        produto = Produto(nome="Produto Cancelamento", preco=40.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        ordem = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=30,
            status=StatusOrdemReposicao.PENDENTE
        )
        test_db.add(ordem)
        test_db.commit()

        # Cancela ordem
        ordem_cancelada = cancelar_ordem_reposicao(test_db, ordem.id, "Falta de estoque no fornecedor")

        # Verifica
        assert ordem_cancelada is not None
        assert ordem_cancelada.status == StatusOrdemReposicao.CANCELADA
        assert ordem_cancelada.data_cancelamento is not None
        assert "cancelada" in ordem_cancelada.observacoes.lower() or "Cancelado" in ordem_cancelada.observacoes

    def test_obter_ordens_pendentes(self, test_db: Session):
        """Testa obtenção de ordens pendentes"""
        # Cria múltiplas ordens com status diferentes
        produto = Produto(nome="Produto Pendentes", preco=45.0)
        test_db.add(produto)
        test_db.commit()

        estoque = Estoque(
            produto_id=produto.id,
            quantidade=10,
            estoque_minimo=10,
            estoque_maximo=50,
            ponto_reposicao=15
        )
        test_db.add(estoque)
        test_db.commit()

        # Ordem pendente
        ordem1 = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=20,
            status=StatusOrdemReposicao.PENDENTE
        )
        
        # Ordem confirmada
        ordem2 = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=15,
            status=StatusOrdemReposicao.CONFIRMADA
        )
        
        # Ordem recebida (não deve aparecer em pendentes)
        ordem3 = OrdemReposicao(
            estoque_id=estoque.id,
            produto_id=produto.id,
            quantidade_solicitada=10,
            status=StatusOrdemReposicao.RECEBIDA
        )
        
        test_db.add_all([ordem1, ordem2, ordem3])
        test_db.commit()

        # Obtém pendentes
        ordens_pendentes = obter_ordens_pendentes(test_db)

        # Verifica
        assert len(ordens_pendentes) == 2  # Apenas pendente e confirmada
        assert ordem3.id not in [o.id for o in ordens_pendentes]
