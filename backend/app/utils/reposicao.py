"""
Funções utilitárias para reposição automática de estoque
RF-06: Pedidos de reposição automáticos
"""

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.ordem_reposicao import OrdemReposicao, StatusOrdemReposicao
from app.models.estoque import Estoque
from app.models.produto import Produto
from app.core.logging import audit_logger


def verificar_estoques_minimos(db: Session) -> list[OrdemReposicao]:
    """
    Verifica produtos com estoque abaixo do mínimo e cria ordens de reposição.
    RF-06: Reposição automática
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Lista de ordens de reposição criadas
    """
    ordens_criadas = []
    
    # Busca todos os estoques
    estoques = db.query(Estoque).all()
    
    for estoque in estoques:
        produto = estoque.produto
        
        # Verifica se o estoque está abaixo do ponto de reposição
        if estoque.quantidade <= estoque.ponto_reposicao:
            # Verifica se já existe ordem pendente/confirmada
            ordem_existente = db.query(OrdemReposicao).filter(
                OrdemReposicao.estoque_id == estoque.id,
                OrdemReposicao.status.in_([
                    StatusOrdemReposicao.PENDENTE,
                    StatusOrdemReposicao.CONFIRMADA
                ])
            ).first()
            
            if not ordem_existente:
                # Calcula quantidade a repor (até atingir o máximo)
                quantidade_necessaria = estoque.estoque_maximo - estoque.quantidade
                
                nova_ordem = OrdemReposicao(
                    estoque_id=estoque.id,
                    produto_id=produto.id,
                    quantidade_solicitada=quantidade_necessaria,
                    motivo="automática",
                    status=StatusOrdemReposicao.PENDENTE,
                    observacoes=f"Reposição automática: estoque {estoque.quantidade} < ponto de reposição {estoque.ponto_reposicao}"
                )
                db.add(nova_ordem)
                ordens_criadas.append(nova_ordem)
                audit_logger.info(f"Ordem de reposição automática criada para estoque {estoque.id}: {quantidade_necessaria} unidades")
    
    if ordens_criadas:
        db.commit()
    
    return ordens_criadas


def criar_ordem_reposicao_manual(
    db: Session,
    estoque_id: int,
    produto_id: int,
    quantidade_solicitada: int,
    observacoes: str | None = None
) -> OrdemReposicao | None:
    """
    Cria uma ordem de reposição manual.
    
    Args:
        db: Sessão do banco de dados
        estoque_id: ID do estoque
        produto_id: ID do produto
        quantidade_solicitada: Quantidade a repor
        observacoes: Observações adicionais
        
    Returns:
        Ordem de reposição criada ou None se estoque não existe
    """
    # Verifica se estoque existe
    estoque = db.query(Estoque).filter(Estoque.id == estoque_id).first()
    
    if not estoque:
        audit_logger.warning(f"Tentativa de criar ordem para estoque inexistente: {estoque_id}")
        return None
    
    ordem = OrdemReposicao(
        estoque_id=estoque_id,
        produto_id=produto_id,
        quantidade_solicitada=quantidade_solicitada,
        motivo="manual",
        status=StatusOrdemReposicao.PENDENTE,
        observacoes=observacoes
    )
    
    db.add(ordem)
    db.commit()
    db.refresh(ordem)
    
    audit_logger.info(f"Ordem de reposição manual criada: {ordem.id} para produto {produto_id}")
    
    return ordem


def confirmar_ordem_reposicao(db: Session, ordem_id: int) -> OrdemReposicao | None:
    """
    Confirma uma ordem de reposição (muda status de pendente para confirmada).
    
    Args:
        db: Sessão do banco de dados
        ordem_id: ID da ordem
        
    Returns:
        Ordem atualizada ou None se não encontrada
    """
    ordem = db.query(OrdemReposicao).filter(OrdemReposicao.id == ordem_id).first()
    
    if not ordem:
        audit_logger.warning(f"Ordem de reposição não encontrada: {ordem_id}")
        return None
    
    if ordem.status != StatusOrdemReposicao.PENDENTE:
        audit_logger.warning(f"Não é possível confirmar ordem {ordem_id} com status {ordem.status}")
        return None
    
    ordem.status = StatusOrdemReposicao.CONFIRMADA
    ordem.data_confirmacao = datetime.now(tz=datetime.now().astimezone().tzinfo)
    
    db.commit()
    db.refresh(ordem)
    
    audit_logger.info(f"Ordem de reposição {ordem_id} confirmada")
    
    return ordem


def receber_ordem_reposicao(
    db: Session,
    ordem_id: int,
    quantidade_recebida: int
) -> OrdemReposicao | None:
    """
    Registra o recebimento de uma ordem de reposição.
    
    Args:
        db: Sessão do banco de dados
        ordem_id: ID da ordem
        quantidade_recebida: Quantidade recebida
        
    Returns:
        Ordem atualizada ou None se não encontrada
    """
    ordem = db.query(OrdemReposicao).filter(OrdemReposicao.id == ordem_id).first()
    
    if not ordem:
        audit_logger.warning(f"Ordem de reposição não encontrada: {ordem_id}")
        return None
    
    if ordem.status == StatusOrdemReposicao.CANCELADA:
        audit_logger.warning(f"Não é possível receber ordem cancelada: {ordem_id}")
        return None
    
    # Atualiza quantidade recebida
    ordem.quantidade_recebida = quantidade_recebida
    
    # Se recebeu tudo, marca como recebida
    if quantidade_recebida >= ordem.quantidade_solicitada:
        ordem.status = StatusOrdemReposicao.RECEBIDA
        ordem.data_recebimento = datetime.now(tz=datetime.now().astimezone().tzinfo)
        
        # Atualiza o estoque
        estoque = ordem.estoque
        estoque.quantidade += quantidade_recebida
        
        audit_logger.info(f"Ordem de reposição {ordem_id} recebida completamente. Estoque atualizado: +{quantidade_recebida}")
    else:
        # Recebimento parcial
        estoque = ordem.estoque
        estoque.quantidade += quantidade_recebida
        
        audit_logger.info(f"Ordem de reposição {ordem_id} recebimento parcial: {quantidade_recebida}/{ordem.quantidade_solicitada}")
    
    db.commit()
    db.refresh(ordem)
    
    return ordem


def cancelar_ordem_reposicao(db: Session, ordem_id: int, motivo: str | None = None) -> OrdemReposicao | None:
    """
    Cancela uma ordem de reposição.
    
    Args:
        db: Sessão do banco de dados
        ordem_id: ID da ordem
        motivo: Motivo do cancelamento
        
    Returns:
        Ordem atualizada ou None se não encontrada
    """
    ordem = db.query(OrdemReposicao).filter(OrdemReposicao.id == ordem_id).first()
    
    if not ordem:
        audit_logger.warning(f"Ordem de reposição não encontrada: {ordem_id}")
        return None
    
    if ordem.status == StatusOrdemReposicao.RECEBIDA:
        audit_logger.warning(f"Não é possível cancelar ordem já recebida: {ordem_id}")
        return None
    
    ordem.status = StatusOrdemReposicao.CANCELADA
    ordem.data_cancelamento = datetime.now(tz=datetime.now().astimezone().tzinfo)
    
    if motivo:
        ordem.observacoes = f"{ordem.observacoes or ''}\nCancelado: {motivo}".strip()
    
    db.commit()
    db.refresh(ordem)
    
    audit_logger.info(f"Ordem de reposição {ordem_id} cancelada")
    
    return ordem


def obter_ordens_pendentes(db: Session, estoque_id: int | None = None) -> list[OrdemReposicao]:
    """
    Obtém ordens de reposição pendentes ou confirmadas.
    
    Args:
        db: Sessão do banco de dados
        estoque_id: ID do estoque (opcional) para filtrar por estoque
        
    Returns:
        Lista de ordens pendentes/confirmadas
    """
    query = db.query(OrdemReposicao).filter(
        OrdemReposicao.status.in_([
            StatusOrdemReposicao.PENDENTE,
            StatusOrdemReposicao.CONFIRMADA
        ])
    )
    
    if estoque_id:
        query = query.filter(OrdemReposicao.estoque_id == estoque_id)
    
    return query.order_by(OrdemReposicao.data_criacao.asc()).all()


def obter_ordens_recebidas_recentemente(db: Session, dias: int = 7) -> list[OrdemReposicao]:
    """
    Obtém ordens de reposição recebidas nos últimos N dias.
    
    Args:
        db: Sessão do banco de dados
        dias: Número de dias a considerar
        
    Returns:
        Lista de ordens recebidas recentemente
    """
    from datetime import timedelta
    
    data_limite = datetime.now(tz=datetime.now().astimezone().tzinfo) - timedelta(days=dias)
    
    return db.query(OrdemReposicao).filter(
        OrdemReposicao.status == StatusOrdemReposicao.RECEBIDA,
        OrdemReposicao.data_recebimento >= data_limite
    ).order_by(OrdemReposicao.data_recebimento.desc()).all()
