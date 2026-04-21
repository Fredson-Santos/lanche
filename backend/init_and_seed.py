#!/usr/bin/env python
"""Script para inicializar e fazer seed do banco de dados"""
from app.db.database import init_db, SessionLocal
from app.models.usuario import Usuario
from app.core.security import hash_password
import hashlib

# Criar todas as tabelas
print("✅ Criando tabelas do banco...")
init_db()

db = SessionLocal()

# Criar usuários de teste
usuarios_teste = [
    {'email': 'admin@lanche.com', 'username': 'admin', 'role': 'admin'},
    {'email': 'gerente@lanche.com', 'username': 'gerente', 'role': 'gerente'},
    {'email': 'vendedor1@lanche.com', 'username': 'vendedor1', 'role': 'vendedor'},
    {'email': 'vendedor2@lanche.com', 'username': 'vendedor2', 'role': 'vendedor'},
]

print('\n✅ Criando usuários de teste...')
for user_data in usuarios_teste:
    email_hash = hashlib.sha256(user_data['email'].encode()).hexdigest()
    usuario = Usuario(
        email=user_data['email'],
        email_hash=email_hash,
        username=user_data['username'],
        senha_hash=hash_password('password123'),
        role=user_data['role']
    )
    db.add(usuario)
    print(f"  ✅ {user_data['email']}: {email_hash[:16]}...")

db.commit()
print(f"\n✅ {len(usuarios_teste)} usuários criados com sucesso!")

# Verificar
usuarios = db.query(Usuario).all()
print(f"\n📊 Total de usuários no banco: {len(usuarios)}")
for u in usuarios:
    print(f"  - {u.email} ({u.role})")
    
db.close()
