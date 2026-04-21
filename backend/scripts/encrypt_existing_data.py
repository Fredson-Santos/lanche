#!/usr/bin/env python
"""
Script para encriptar dados existentes no banco de dados
Deve ser executado APÓS aplicar a migration Alembic

Uso:
    python backend/scripts/encrypt_existing_data.py
    
Variáveis de ambiente:
    DATABASE_URL: URL do banco de dados (padrão: sqlite:///./lanche.db)
    ENCRYPTION_KEY: Chave de encriptação (padrão: gerada automaticamente)
"""
import os
import sys
import logging
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.crypto import get_crypto_manager
import hashlib

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_email_hash(email: str) -> str:
    """Gera hash SHA-256 do email"""
    return hashlib.sha256(email.encode()).hexdigest()


def migrate_usuarios_encryption():
    """
    Migra dados de usuários para formato encriptado
    
    Etapas:
    1. Conecta ao banco
    2. Busca usuários com email_encrypted vazio
    3. Encripta email
    4. Calcula email_hash
    5. Atualiza registro
    """
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./lanche.db"
    )
    
    logger.info(f"Conectando ao banco: {database_url}")
    
    # Criar engine e sessão
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(bind=engine)
    
    try:
        conn = engine.connect()
        logger.info("✅ Conexão estabelecida")
        
        # Obter gerenciador de criptografia
        crypto = get_crypto_manager()
        logger.info(f"✅ Gerenciador de criptografia inicializado")
        logger.info(f"   Chave disponível: {bool(crypto.key)}")
        
        # Contar usuários
        result = conn.execute(text("SELECT COUNT(*) FROM usuarios"))
        total_usuarios = result.scalar()
        logger.info(f"📊 Total de usuários: {total_usuarios}")
        
        # Buscar usuários
        result = conn.execute(text("""
            SELECT id, email_encrypted, email_hash 
            FROM usuarios 
            WHERE email_hash IS NULL OR email_hash = ''
        """))
        
        usuarios_para_migrar = result.fetchall()
        logger.info(f"🔄 Usuários para migrar: {len(usuarios_para_migrar)}")
        
        if not usuarios_para_migrar:
            logger.info("✅ Nenhum usuário para migrar - dados já estão encriptados!")
            return True
        
        # Migrar cada usuário
        migrados = 0
        erros = 0
        
        for usuario_id, email_encrypted, email_hash in usuarios_para_migrar:
            try:
                # Descriptografar email se necessário
                email_original = crypto.decrypt(email_encrypted)
                
                # Gerar hash
                novo_hash = get_email_hash(email_original)
                
                # Atualizar no banco
                conn.execute(text("""
                    UPDATE usuarios 
                    SET email_hash = :hash
                    WHERE id = :id
                """), {"hash": novo_hash, "id": usuario_id})
                
                migrados += 1
                logger.info(f"  ✅ Usuário {usuario_id}: email_hash calculado")
                
            except Exception as e:
                erros += 1
                logger.error(f"  ❌ Usuário {usuario_id}: {str(e)}")
        
        # Commitar transação
        conn.commit()
        conn.close()
        
        logger.info(f"""
╔══════════════════════════════════════════════╗
║           MIGRAÇÃO COMPLETA                  ║
╠══════════════════════════════════════════════╣
║ Usuários migrados: {migrados:<30} ║
║ Erros encontrados: {erros:<30} ║
║ Status: {"✅ SUCESSO" if erros == 0 else "⚠️ COM ERROS":<30} ║
╚══════════════════════════════════════════════╝
        """)
        
        return erros == 0
        
    except Exception as e:
        logger.error(f"❌ Erro durante migração: {str(e)}", exc_info=True)
        return False
    finally:
        engine.dispose()


def verify_encryption():
    """
    Verifica se a encriptação está funcionando corretamente
    """
    logger.info("\n🔐 Verificando criptografia...")
    
    try:
        crypto = get_crypto_manager()
        
        # Teste 1: Encriptação básica
        texto_original = "teste@example.com"
        encriptado = crypto.encrypt(texto_original)
        decriptado = crypto.decrypt(encriptado)
        
        assert decriptado == texto_original, f"Mismatch: {decriptado} != {texto_original}"
        logger.info(f"  ✅ Teste 1: Encriptação/Decriptação OK")
        logger.info(f"     Original: {texto_original}")
        logger.info(f"     Encriptado: {encriptado[:50]}...")
        
        # Teste 2: Hash
        hash1 = get_email_hash(texto_original)
        hash2 = get_email_hash(texto_original)
        assert hash1 == hash2, "Hashes diferentes para mesmo input"
        logger.info(f"  ✅ Teste 2: Hash consistente")
        
        logger.info("✅ Todos os testes de criptografia passaram!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro na verificação: {str(e)}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("""
╔═══════════════════════════════════════════════════╗
║     MIGRAÇÃO DE DADOS - CRIPTOGRAFIA DE BANCO    ║
╚═══════════════════════════════════════════════════╝
    """)
    
    # Verificar criptografia
    if not verify_encryption():
        sys.exit(1)
    
    # Executar migração
    if migrate_usuarios_encryption():
        logger.info("\n✅ MIGRAÇÃO FINALIZADA COM SUCESSO!")
        sys.exit(0)
    else:
        logger.error("\n❌ MIGRAÇÃO FINALIZADA COM ERROS!")
        sys.exit(1)
