import React from 'react';
import { useOffline } from '../../hooks/useOffline';
import { Button } from '../ui/Button';

export function OfflineStatusBanner() {
  const { isOnline, pendingCount, syncPending } = useOffline();

  if (isOnline && pendingCount === 0) return null;

  return (
    <div className={`offline-banner ${!isOnline ? 'danger' : 'warning'}`}>
      <div className="offline-banner-content">
        <span className="offline-banner-icon">
          {!isOnline ? '📡' : '✅'}
        </span>
        <span className="offline-banner-text">
          {!isOnline 
            ? 'Você está Offline. As vendas serão salvas no dispositivo.' 
            : `Conexão restaurada! Você tem ${pendingCount} venda(s) pendente(s).`}
        </span>
      </div>
      
      {isOnline && pendingCount > 0 && (
        <Button 
          size="sm" 
          variant="secondary" 
          onClick={syncPending}
          className="ml-4"
        >
          Sincronizar Agora
        </Button>
      )}
    </div>
  );
}
