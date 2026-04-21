import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.auditoria import AuditoriaLog

class TestLGPDLite:
    """Testes para conformidade LGPD Lite (Transparência e Direito de Acesso)"""

    def test_exportar_meus_dados_sucesso(self, client: TestClient, test_db: Session, gerente_token):
        """Testa se um usuário consegue exportar seus próprios dados"""
        # Criar alguns logs para o usuário gerente
        gerente = test_db.query(Usuario).filter(Usuario.role == "gerente").first()
        log1 = AuditoriaLog(
            user_id=gerente.id,
            event_type="AUTH",
            action="LOGIN",
            status="SUCCESS",
            resource_type="Usuario",
            context={"msg": "Login de teste 1"}
        )
        log2 = AuditoriaLog(
            user_id=gerente.id,
            event_type="CRUD",
            action="READ",
            status="SUCCESS",
            resource_type="Estoque",
            context={"msg": "Consulta de teste 1"}
        )
        test_db.add_all([log1, log2])
        test_db.commit()

        headers = {"Authorization": f"Bearer {gerente_token}"}
        response = client.get("/api/usuarios/me/dados", headers=headers)

        if response.status_code != 200:
            print(f"Erro {response.status_code}: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert "perfil" in data
        assert data["perfil"]["username"] == gerente.username
        assert "atividades_recentes" in data
        assert len(data["atividades_recentes"]) >= 2
        assert "total_atividades" in data
        assert "data_geracao" in data

    def test_exportar_dados_nao_autenticado(self, client: TestClient):
        """Testa se acesso sem token é bloqueado"""
        response = client.get("/api/usuarios/me/dados")
        assert response.status_code == 401

    def test_aviso_privacidade_existe(self):
        """Testa se o documento de aviso de privacidade existe na pasta docs"""
        import os
        # Tenta encontrar o arquivo subindo níveis se necessário
        possiveis_caminhos = [
            "docs/AVISO_PRIVACIDADE_INTERNO.md",
            "../docs/AVISO_PRIVACIDADE_INTERNO.md",
            "../../docs/AVISO_PRIVACIDADE_INTERNO.md"
        ]
        path = None
        for p in possiveis_caminhos:
            if os.path.exists(p):
                path = p
                break
        
        assert path is not None, "Arquivo AVISO_PRIVACIDADE_INTERNO.md não encontrado"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            assert "# Aviso de Privacidade Interno" in content
            assert "LGPD" in content
