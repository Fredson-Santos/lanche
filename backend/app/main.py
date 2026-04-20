"""
LANCHE MVP - Main Application Entry Point
FastAPI application with authentication, RBAC, and structured logging
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core import settings, logger
from app.db.database import Base, engine, get_db
from app.models import Usuario, Produto, Estoque, Venda, ItemVenda, AuditoriaLog
from app.middleware import AuditMiddleware
from app.db.init_db import init_db
from app.routes import auth, usuarios, produtos, estoque, vendas, relatorios

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Inicializa o banco com dados padrão
    db = next(get_db())
    init_db(db)
    yield

app = FastAPI(
    title="LANCHE MVP API",
    description="Sistema de gestão para varejo alimentício",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware de Auditoria (deve ser adicionado antes de outros middlewares)
app.add_middleware(AuditMiddleware)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(produtos.router, prefix="/api/produtos", tags=["Produtos"])
app.include_router(estoque.router, prefix="/api/estoque", tags=["Estoque"])
app.include_router(vendas.router, prefix="/api/vendas", tags=["Vendas"])
app.include_router(relatorios.router, prefix="/api/relatorios", tags=["Relatórios"])

@app.get("/", tags=["root"])
async def root():
    """Endpoint raiz da API"""
    logger.info(
        "Root endpoint accessed",
        extra={"event": "root_access"},
    )
    return {
        "message": "LANCHE MVP API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Endpoint de health check da API"""
    logger.info(
        "Health check endpoint accessed",
        extra={
            "event": "health_check",
            "environment": settings.ENVIRONMENT,
            "database": settings.DATABASE_URL.split("://")[0] if settings.DATABASE_URL else "unknown",
        },
    )
    return {
        "status": "healthy",
        "message": "LANCHE MVP API is running",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "log_level": settings.LOG_LEVEL,
    }

# Log initial startup information
logger.info(
    "LANCHE MVP API Startup",
    extra={
        "event": "app_startup",
        "environment": settings.ENVIRONMENT,
        "log_format": settings.LOG_FORMAT,
        "log_level": settings.LOG_LEVEL,
        "debug": settings.DEBUG,
    },
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
