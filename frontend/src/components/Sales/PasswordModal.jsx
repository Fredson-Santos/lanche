import React, { useState } from 'react';
import { Modal } from '../ui/Modal';
import { Button } from '../ui/Button';

export function PasswordModal({ isOpen, title, onConfirm, onCancel, loading }) {
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onConfirm(password);
    setPassword('');
  };

  const footer = (
    <div style={{ display: 'flex', gap: 'var(--space-3)', width: '100%' }}>
      <Button
        type="button"
        variant="ghost"
        className="w-full"
        onClick={onCancel}
        disabled={loading}
      >
        Cancelar
      </Button>
      <Button
        type="button"
        variant="primary"
        className="w-full"
        onClick={handleSubmit}
        loading={loading}
        disabled={!password}
      >
        Confirmar
      </Button>
    </div>
  );

  return (
    <Modal open={isOpen} onClose={onCancel} title={title} icon="🔐" footer={footer}>
      <p style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-5)' }}>
        Para sua segurança, confirme sua senha de acesso.
      </p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">SENHA DO OPERADOR *</label>
          <input
            autoFocus
            type="password"
            className="form-input"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Digite sua senha..."
            required
          />
        </div>
      </form>
    </Modal>
  );
}
