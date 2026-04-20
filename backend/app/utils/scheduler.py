"""
Scheduler de jobs agendados com APScheduler
RF-01, RF-02, RF-03: Jobs para verificar alertas de validade, temperatura
RF-06: Jobs para reposição automática
"""

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.utils.alertas import verificar_alertas_validade, verificar_alertas_temperatura
from app.utils.reposicao import verificar_estoques_minimos
from app.core.logging import audit_logger

scheduler = BackgroundScheduler()


def iniciar_scheduler():
    """Inicializa o scheduler de jobs agendados"""
    if scheduler.running:
        audit_logger.info("Scheduler já está rodando")
        return
    
    # Job para verificar alertas de validade a cada 15 minutos
    scheduler.add_job(
        job_verificar_alertas_validade,
        "interval",
        minutes=15,
        id="verificar_alertas_validade",
        name="Verificar Alertas de Validade",
        replace_existing=True,
    )
    
    # Job para verificar alertas de temperatura a cada 15 minutos
    scheduler.add_job(
        job_verificar_alertas_temperatura,
        "interval",
        minutes=15,
        id="verificar_alertas_temperatura",
        name="Verificar Alertas de Temperatura",
        replace_existing=True,
    )
    
    # Job para verificar estoques mínimos a cada 30 minutos (RF-06)
    scheduler.add_job(
        job_verificar_estoques_minimos,
        "interval",
        minutes=30,
        id="verificar_estoques_minimos",
        name="Verificar Estoques Mínimos e Criar Ordens de Reposição",
        replace_existing=True,
    )
    
    scheduler.start()
    audit_logger.info("Scheduler iniciado com sucesso")


def parar_scheduler():
    """Para o scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        audit_logger.info("Scheduler parado")


def job_verificar_alertas_validade():
    """Job que verifica alertas de validade"""
    try:
        db = next(get_db())
        alertas = verificar_alertas_validade(db)
        audit_logger.info(f"Job verificar_alertas_validade executado: {len(alertas)} alertas criados/atualizados")
    except Exception as e:
        audit_logger.error(f"Erro ao verificar alertas de validade: {str(e)}")
    finally:
        db.close()


def job_verificar_alertas_temperatura():
    """Job que verifica alertas de temperatura"""
    try:
        db = next(get_db())
        alertas = verificar_alertas_temperatura(db)
        audit_logger.info(f"Job verificar_alertas_temperatura executado: {len(alertas)} alertas criados/atualizados")
    except Exception as e:
        audit_logger.error(f"Erro ao verificar alertas de temperatura: {str(e)}")
    finally:
        db.close()


def job_verificar_estoques_minimos():
    """Job que verifica estoques mínimos e cria ordens de reposição (RF-06)"""
    try:
        db = next(get_db())
        ordens = verificar_estoques_minimos(db)
        audit_logger.info(f"Job verificar_estoques_minimos executado: {len(ordens)} ordens de reposição criadas")
    except Exception as e:
        audit_logger.error(f"Erro ao verificar estoques mínimos: {str(e)}")
    finally:
        db.close()
