#!/usr/bin/env python
"""Script para atualizar email_hash de usuários existentes"""
import sqlite3
import hashlib
from app.core.crypto import get_crypto_manager

# Conectar ao banco
conn = sqlite3.connect("./lanche.db")
cursor = conn.cursor()

# Verificar schema
cursor.execute("PRAGMA table_info(usuarios)")
columns = cursor.fetchall()
print("Colunas da tabela usuarios:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Buscar usuários
cursor.execute("SELECT id, email_encrypted FROM usuarios WHERE email_hash = ''")
usuarios = cursor.fetchall()
print(f"\n📊 Atualizando {len(usuarios)} usuários com email_hash vazio...")

crypto = get_crypto_manager()

for usuario_id, email_encrypted in usuarios:
    # Descriptografar
    try:
        email = crypto.decrypt(email_encrypted)
        email_hash = hashlib.sha256(email.encode()).hexdigest()
        cursor.execute("UPDATE usuarios SET email_hash = ? WHERE id = ?", (email_hash, usuario_id))
        print(f"  ✅ Usuario {usuario_id}: {email[:20]}... -> {email_hash[:16]}...")
    except Exception as e:
        print(f"  ❌ Usuario {usuario_id}: Erro - {str(e)}")

conn.commit()
print("\n✅ Concluído!")
