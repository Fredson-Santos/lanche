"""
Funções utilitárias para verificação e criação de alertas
RF-01, RF-02, RF-03: Lógica de alertas de validade, temperatura e estoque
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.alerta import Alerta, TipoAlerta
from app.models.produto import Produto
from app.models.estoque import Estoque
from app.core.logging import audit_logger


def verificar_alertas_validade(db: Session) -> list[Alerta]:
    """
    Verifica produtos com data de validade vencida ou próxima de vencer (próximos 7 dias).
    RF-01: Controlar validade de produtos
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Lista de alertas criados/atualizados
    """
    alertas_criados = []
    agora = datetime.now(tz=datetime.now().astimezone().tzinfo)
    data_limite = agora + timedelta(days=7)
    
    # Busca produtos com data_validade definida
    produtos_com_validade = db.query(Produto).filter(
        Produto.data_validade.isnot(None),
        Produto.ativo == True
    ).all()
    
    for produto in produtos_com_validade:
        # Verifica se já existe alerta ativo para este produto
        alerta_existente = db.query(Alerta).filter(
            Alerta.produto_id == produto.id,
            Alerta.tipo == TipoAlerta.VALIDADE,
            Alerta.ativo == True,
            Alerta.lido == False
        ).first()
        
        # Garante que data_validade tem timezone info
        data_validade = produto.data_validade
        if data_validade and data_validade.tzinfo is None:
            data_validade = data_validade.replace(tzinfo=agora.tzinfo)
        
        if data_validade <= agora:
            # Produto vencido
            if not alerta_existente:
                novo_alerta = Alerta(
                    produto_id=produto.id,
                    tipo=TipoAlerta.VALIDADE,
                    titulo=f"Produto venceu: {produto.nome}",
                    descricao=f"Produto {produto.nome} (lote: {produto.lote}) venceu em {data_validade.strftime('%d/%m/%Y')}",
                    lido=False,
                    ativo=True
                )
                db.add(novo_alerta)
                alertas_criados.append(novo_alerta)
                audit_logger.info(f"Alerta de validade criado para produto {produto.id}")
                
        elif data_validade <= data_limite:
            # Produto próximo de vencer
            if not alerta_existente:
                dias_restantes = (data_validade - agora).days
                novo_alerta = Alerta(
                    produto_id=produto.id,
                    tipo=TipoAlerta.VALIDADE,
                    titulo=f"Produto próximo de vencer: {produto.nome}",
                    descricao=f"Produto {produto.nome} (lote: {produto.lote}) vence em {dias_restantes} dias ({data_validade.strftime('%d/%m/%Y')})",
                    lido=False,
                    ativo=True
                )
                db.add(novo_alerta)
                alertas_criados.append(novo_alerta)
                audit_logger.info(f"Alerta de validade (próximo vencimento) criado para produto {produto.id}")
    
    db.commit()
    return alertas_criados


def verificar_alertas_temperatura(db: Session) -> list[Alerta]:
    """
    Verifica estoques com temperatura fora do intervalo ideal.
    RF-02: Monitorar temperatura
    
    Args:
        db: Sessão do banco de dados
        
    Returns:
        Lista de alertas criados/atualizados
    """
    alertas_criados = []
    
    # Busca estoques com temperatura registrada
    estoques = db.query(Estoque).filter(
        Estoque.temperatura_atual.isnot(None)
    ).all()
    
    for estoque in estoques:
        produto = estoque.produto
        
        if not produto.ativo or produto.temperatura_ideal_min is None:
            continue
        
        # Verifica se já existe alerta ativo
        alerta_existente = db.query(Alerta).filter(
            Alerta.estoque_id == estoque.id,
            Alerta.tipo == TipoAlerta.TEMPERATURA,
            Alerta.ativo == True,
            Alerta.lido == False
        ).first()
        
        # Verifica se temperatura está fora do intervalo
        temp_abaixo = produto.temperatura_ideal_min and estoque.temperatura_atual < produto.temperatura_ideal_min
        temp_acima = produto.temperatura_ideal_max and estoque.temperatura_atual > produto.temperatura_ideal_max
        
        if temp_abaixo or temp_acima:
            if not alerta_existente:
                if temp_abaixo:
                    descricao = f"Temperatura abaixo do ideal: {estoque.temperatura_atual}°C (mínimo: {produto.temperatura_ideal_min}°C)"
                else:
                    descricao = f"Temperatura acima do ideal: {estoque.temperatura_atual}°C (máximo: {produto.temperatura_ideal_max}°C)"
                
                novo_alerta = Alerta(
                    produto_id=produto.id,
                    estoque_id=estoque.id,
                    tipo=TipoAlerta.TEMPERATURA,
                    titulo=f"Temperatura fora do intervalo: {produto.nome}",
                    descricao=descricao,
                    lido=False,
                    ativo=True
                )
                db.add(novo_alerta)
                alertas_criados.append(novo_alerta)
                audit_logger.info(f"Alerta de temperatura criado para estoque {estoque.id}")
    
    db.commit()
    return alertas_criados


def marcar_alerta_como_lido(db: Session, alerta_id: int) -> Alerta | None:
    """
    Marca um alerta como lido.
    
    Args:
        db: Sessão do banco de dados
        alerta_id: ID do alerta
        
    Returns:
        Alerta atualizado ou None se não encontrado
    """
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    
    if alerta:
        alerta.lido = True
        alerta.data_leitura = datetime.now(tz=datetime.now().astimezone().tzinfo)
        db.commit()
        db.refresh(alerta)
        audit_logger.info(f"Alerta {alerta_id} marcado como lido")
    
    return alerta


def limpar_alertas_resolvidos(db: Session, alerta_id: int) -> Alerta | None:
    """
    Marca um alerta como resolvido (inativo).
    
    Args:
        db: Sessão do banco de dados
        alerta_id: ID do alerta
        
    Returns:
        Alerta atualizado ou None se não encontrado
    """
    alerta = db.query(Alerta).filter(Alerta.id == alerta_id).first()
    
    if alerta:
        alerta.ativo = False
        alerta.data_resolucao = datetime.now(tz=datetime.now().astimezone().tzinfo)
        db.commit()
        db.refresh(alerta)
        audit_logger.info(f"Alerta {alerta_id} marcado como resolvido")
    
    return alerta


def obter_alertas_ativos(db: Session, produto_id: int | None = None) -> list[Alerta]:
    """
    Obtém todos os alertas ativos (não lidos e ativo=True).
    
    Args:
        db: Sessão do banco de dados
        produto_id: ID do produto (opcional) para filtrar alertas de um produto específico
        
    Returns:
        Lista de alertas ativos
    """
    query = db.query(Alerta).filter(
        Alerta.ativo == True,
        Alerta.lido == False
    )
    
    if produto_id:
        query = query.filter(Alerta.produto_id == produto_id)
    
    return query.order_by(Alerta.data_criacao.desc()).all()
