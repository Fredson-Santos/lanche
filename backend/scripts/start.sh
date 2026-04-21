#!/bin/bash

# Esperar pelo banco de dados
python scripts/wait_for_db.py

# Rodar migrações
echo "Rodando migrações do Alembic..."
alembic upgrade head

# Iniciar o servidor
echo "Iniciando o servidor FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8008 --reload
