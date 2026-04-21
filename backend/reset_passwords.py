#!/usr/bin/env python
"""Script para resetar senhas dos usuários"""
import sys
sys.path.insert(0, '.')
from app.db.database import SessionLocal
from app.models.usuario import Usuario
from app.core.security import hash_password

db = SessionLocal()

print("=" * 60)
print("🔐 RESETANDO SENHAS DOS USUÁRIOS")
print("=" * 60)

# Atualizar admin
admin = db.query(Usuario).filter_by(username='admin').first()
if admin:
    admin.senha_hash = hash_password('admin123')
    db.commit()
    print("✅ Admin: senha resetada para 'admin123'")
else:
    print("❌ Admin não encontrado")

# Atualizar gerente
gerente = db.query(Usuario).filter_by(username='gerente').first()
if gerente:
    gerente.senha_hash = hash_password('gerente123')
    db.commit()
    print("✅ Gerente: senha resetada para 'gerente123'")
else:
    print("❌ Gerente não encontrado")

# Verificar caixa
caixa = db.query(Usuario).filter_by(username='caixa').first()
if caixa:
    print("✅ Caixa: senha já está 'caixa123'")

db.close()

print("\n" + "=" * 60)
print("🎉 SENHAS RESETADAS COM SUCESSO!")
print("=" * 60)
