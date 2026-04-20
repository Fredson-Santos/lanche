"""
Middleware de Auditoria
Intercepta requisições HTTP e registra eventos de auditoria
"""

import time
import json
from typing import Callable, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from app.core.logging import audit_logger


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware para interceptar e auditar requisições HTTP
    Registra informações de requisição/resposta para fins de auditoria
    """

    def __init__(self, app: ASGIApp):
        """Inicializa o middleware"""
        super().__init__(app)
        self.excluded_paths = {
            "/api/docs",
            "/api/redoc",
            "/api/openapi.json",
            "/health",
            "/metrics",
        }

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Processa a requisição, registra auditoria e passa para próximo middleware
        
        Args:
            request: Requisição HTTP
            call_next: Próxima função middleware
            
        Returns:
            Response: Resposta HTTP com headers de auditoria
        """
        
        # Verifica se caminho deve ser auditado
        if self._deve_auditar(request.url.path):
            # Extrai informações da requisição
            start_time = time.time()
            client_ip = self._obter_ip_cliente(request)
            method = request.method
            path = request.url.path
            
            try:
                # Processa requisição
                response = await call_next(request)
                
                # Calcula tempo de processamento
                process_time = time.time() - start_time
                
                # Registra auditoria bem-sucedida
                self._registrar_auditoria(
                    method=method,
                    path=path,
                    status_code=response.status_code,
                    process_time=process_time,
                    client_ip=client_ip,
                    usuario_id=self._extrair_usuario_id(request),
                    sucesso=response.status_code < 400,
                )
                
                # Adiciona headers de rastreamento
                response.headers["X-Audit-Logged"] = "true"
                
                return response
                
            except Exception as exc:
                # Registra erro de requisição
                process_time = time.time() - start_time
                self._registrar_auditoria(
                    method=method,
                    path=path,
                    status_code=500,
                    process_time=process_time,
                    client_ip=client_ip,
                    usuario_id=self._extrair_usuario_id(request),
                    sucesso=False,
                    erro=str(exc),
                )
                raise
        else:
            # Passa direto para próximo middleware
            response = await call_next(request)
            return response

    def _deve_auditar(self, path: str) -> bool:
        """
        Verifica se o caminho deve ser auditado
        
        Args:
            path: Caminho da requisição
            
        Returns:
            bool: True se deve auditar
        """
        for excluded in self.excluded_paths:
            if path.startswith(excluded):
                return False
        return path.startswith("/api/")

    def _obter_ip_cliente(self, request: Request) -> str:
        """
        Obtém o IP real do cliente considerando proxies
        
        Args:
            request: Requisição HTTP
            
        Returns:
            str: Endereço IP do cliente
        """
        # Verifica X-Forwarded-For primeiro (aplicações atrás de proxy)
        if "x-forwarded-for" in request.headers:
            return request.headers["x-forwarded-for"].split(",")[0].strip()
        
        # Depois tenta X-Real-IP
        if "x-real-ip" in request.headers:
            return request.headers["x-real-ip"]
        
        # Por fim, usa o IP de conexão direto
        if request.client:
            return request.client.host
        
        return "unknown"

    def _extrair_usuario_id(self, request: Request) -> Optional[int]:
        """
        Extrai ID do usuário do contexto da requisição (se disponível)
        
        Args:
            request: Requisição HTTP
            
        Returns:
            Optional[int]: ID do usuário ou None
        """
        # Tenta extrair do estado da requisição
        if hasattr(request.state, "user_id"):
            return request.state.user_id
        
        # Tenta extrair do escopo ASGI
        if "user" in request.scope:
            user = request.scope["user"]
            if hasattr(user, "id"):
                return user.id
        
        return None

    def _registrar_auditoria(
        self,
        method: str,
        path: str,
        status_code: int,
        process_time: float,
        client_ip: str,
        usuario_id: Optional[int] = None,
        sucesso: bool = True,
        erro: Optional[str] = None,
    ):
        """
        Registra informações de auditoria da requisição
        
        Args:
            method: Método HTTP (GET, POST, etc)
            path: Caminho da requisição
            status_code: Código de status HTTP
            process_time: Tempo de processamento em segundos
            client_ip: IP do cliente
            usuario_id: ID do usuário (opcional)
            sucesso: Se a requisição foi bem-sucedida
            erro: Mensagem de erro (opcional)
        """
        # Mapa para determinar tipo de evento baseado no método
        tipo_evento = "CRUD"
        if method in ["GET"]:
            tipo_evento = "READ"
        elif method in ["POST"]:
            tipo_evento = "CREATE"
        elif method in ["PUT", "PATCH"]:
            tipo_evento = "UPDATE"
        elif method in ["DELETE"]:
            tipo_evento = "DELETE"
        
        # Prepara contexto
        context = {
            "http_method": method,
            "http_path": path,
            "http_status": status_code,
            "process_time_ms": round(process_time * 1000, 2),
            "client_ip": client_ip,
        }
        
        # Registra no logger estruturado
        audit_logger.log_event(
            event_type=tipo_evento,
            action=f"{method} {path}",
            status="SUCCESS" if sucesso else "FAILURE",
            user_id=usuario_id,
            error_message=erro,
            details=context,
        )


__all__ = ["AuditMiddleware"]
