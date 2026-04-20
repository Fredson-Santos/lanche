"""
Testes para API Keys - RF-11
Validação de geração, verificação, rate limiting e revogação de chaves
"""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.api_key import APIKey
from app.utils.api_keys import (
    gerar_chave_api,
    criar_api_key,
    verificar_api_key,
    registrar_uso_api_key,
    verificar_rate_limit,
    resetar_contador_requisicoes,
    revogar_api_key,
    obter_todas_api_keys,
    limpar_api_keys_expiradas,
)


class TestGeracaoChaves:
    """Testes para geração de chaves de API"""
    
    def test_gerar_chave_api(self):
        """Verifica se a chave é gerada como UUID hex (32 caracteres)"""
        chave = gerar_chave_api()
        
        assert isinstance(chave, str)
        assert len(chave) == 32
        assert all(c in "0123456789abcdef" for c in chave)
    
    def test_chaves_unicas(self):
        """Verifica se chaves geradas são únicas"""
        chave1 = gerar_chave_api()
        chave2 = gerar_chave_api()
        
        assert chave1 != chave2


class TestCriacaoChaves:
    """Testes para criação de API keys"""
    
    def test_criar_api_key_com_defaults(self, test_db: Session):
        """Cria API key com parâmetros padrão"""
        api_key = criar_api_key(
            db=test_db,
            descricao="Delivery A"
        )
        
        assert api_key is not None
        assert api_key.descricao == "Delivery A"
        assert api_key.ativo is True
        assert api_key.limite_requisicoes == 100
        assert api_key.janela_tempo == 60
        assert api_key.expires_em is None
        assert len(api_key.chave) == 32
    
    def test_criar_api_key_com_expiacao(self, test_db: Session):
        """Cria API key com data de expiração"""
        expires = datetime.utcnow() + timedelta(days=30)
        api_key = criar_api_key(
            db=test_db,
            descricao="Parceiro B",
            expires_em=expires
        )
        
        assert api_key is not None
        assert api_key.expires_em is not None
    
    def test_criar_api_key_com_limites_customizados(self, test_db: Session):
        """Cria API key com limites personalizados"""
        api_key = criar_api_key(
            db=test_db,
            descricao="Terceiro C",
            limite_requisicoes=500,
            janela_tempo=120
        )
        
        assert api_key is not None
        assert api_key.limite_requisicoes == 500
        assert api_key.janela_tempo == 120


class TestVerificacaoChaves:
    """Testes para verificação de API keys"""
    
    def test_verificar_chave_valida(self, test_db: Session):
        """Verifica uma chave válida e ativa"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        verificada = verificar_api_key(db=test_db, chave=api_key.chave)
        
        assert verificada is not None
        assert verificada.id == api_key.id
    
    def test_verificar_chave_invalida(self, test_db: Session):
        """Tenta verificar uma chave que não existe"""
        resultado = verificar_api_key(db=test_db, chave="chave_inexistente")
        
        assert resultado is None
    
    def test_verificar_chave_inativa(self, test_db: Session):
        """Tenta verificar uma chave desativada"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        api_key.ativo = False
        test_db.commit()
        
        resultado = verificar_api_key(db=test_db, chave=api_key.chave)
        
        assert resultado is None
    
    def test_verificar_chave_expirada(self, test_db: Session):
        """Tenta verificar uma chave expirada"""
        expires = datetime.utcnow() - timedelta(days=1)  # Expirou
        api_key = criar_api_key(
            db=test_db,
            descricao="Test",
            expires_em=expires
        )
        
        resultado = verificar_api_key(db=test_db, chave=api_key.chave)
        
        assert resultado is None


class TestRateLimiting:
    """Testes para rate limiting de API keys"""
    
    def test_rate_limit_dentro_do_limite(self, test_db: Session):
        """Chave dentro do limite de requisições"""
        api_key = criar_api_key(db=test_db, descricao="Test", limite_requisicoes=5)
        api_key.requisicoes_usadas = 3
        test_db.commit()
        
        pode_usar = verificar_rate_limit(db=test_db, chave_id=api_key.id)
        
        assert pode_usar is True
    
    def test_rate_limit_excedido(self, test_db: Session):
        """Chave atingiu o limite de requisições"""
        api_key = criar_api_key(db=test_db, descricao="Test", limite_requisicoes=5)
        api_key.requisicoes_usadas = 5
        test_db.commit()
        
        pode_usar = verificar_rate_limit(db=test_db, chave_id=api_key.id)
        
        assert pode_usar is False
    
    def test_registrar_uso_incrementa_contador(self, test_db: Session):
        """Registra uso e incrementa contador"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        contador_antes = api_key.requisicoes_usadas
        
        registrar_uso_api_key(db=test_db, chave_id=api_key.id)
        
        api_key = test_db.query(APIKey).filter(APIKey.id == api_key.id).first()
        assert api_key.requisicoes_usadas == contador_antes + 1
        assert api_key.ultima_uso is not None
    
    def test_resetar_contador(self, test_db: Session):
        """Reseta contador de requisições"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        api_key.requisicoes_usadas = 50
        test_db.commit()
        
        resetar_contador_requisicoes(db=test_db, chave_id=api_key.id)
        
        api_key = test_db.query(APIKey).filter(APIKey.id == api_key.id).first()
        assert api_key.requisicoes_usadas == 0


class TestRevogacaoChaves:
    """Testes para revogação de API keys"""
    
    def test_revogar_chave(self, test_db: Session):
        """Revoga uma chave ativa"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        assert api_key.ativo is True
        
        revogar_api_key(db=test_db, chave_id=api_key.id)
        
        api_key = test_db.query(APIKey).filter(APIKey.id == api_key.id).first()
        assert api_key.ativo is False
    
    def test_nao_pode_usar_chave_revogada(self, test_db: Session):
        """Não consegue usar uma chave após revogação"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        revogar_api_key(db=test_db, chave_id=api_key.id)
        
        verificada = verificar_api_key(db=test_db, chave=api_key.chave)
        
        assert verificada is None


class TestGerenciamentoChaves:
    """Testes para gerenciamento geral de API keys"""
    
    def test_obter_todas_chaves(self, test_db: Session):
        """Lista todas as API keys"""
        criar_api_key(db=test_db, descricao="Key 1")
        criar_api_key(db=test_db, descricao="Key 2")
        
        chaves = obter_todas_api_keys(db=test_db)
        
        assert len(chaves) >= 2
    
    def test_obter_apenas_chaves_ativas(self, test_db: Session):
        """Lista apenas chaves ativas"""
        api_key1 = criar_api_key(db=test_db, descricao="Ativa")
        api_key2 = criar_api_key(db=test_db, descricao="Inativa")
        revogar_api_key(db=test_db, chave_id=api_key2.id)
        
        ativas = obter_todas_api_keys(db=test_db, apenas_ativas=True)
        
        assert any(k.id == api_key1.id for k in ativas)
        assert not any(k.id == api_key2.id for k in ativas)
    
    def test_limpar_chaves_expiradas(self, test_db: Session):
        """Remove chaves expiradas após retenção"""
        # Cria chave expirada há mais de 30 dias
        expires = datetime.utcnow() - timedelta(days=35)
        api_key = criar_api_key(
            db=test_db,
            descricao="Expirada",
            expires_em=expires
        )
        revogar_api_key(db=test_db, chave_id=api_key.id)
        
        # Limpeza deve remover
        total_removidas = limpar_api_keys_expiradas(db=test_db)
        
        assert total_removidas > 0
        
        # Verifica se foi removida
        verificar = test_db.query(APIKey).filter(APIKey.id == api_key.id).first()
        assert verificar is None


class TestEstadoChaves:
    """Testes para estado e validação de chaves"""
    
    def test_chave_ativa_nao_expirada(self, test_db: Session):
        """Chave ativa e não expirada"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        
        assert api_key.esta_ativa() is True
    
    def test_chave_inativa(self, test_db: Session):
        """Chave revogada não está ativa"""
        api_key = criar_api_key(db=test_db, descricao="Test")
        api_key.ativo = False
        test_db.commit()
        
        assert api_key.esta_ativa() is False
    
    def test_chave_expirada_nao_ativa(self, test_db: Session):
        """Chave expirada não está ativa"""
        expires = datetime.utcnow() - timedelta(hours=1)
        api_key = criar_api_key(
            db=test_db,
            descricao="Test",
            expires_em=expires
        )
        
        assert api_key.esta_ativa() is False
