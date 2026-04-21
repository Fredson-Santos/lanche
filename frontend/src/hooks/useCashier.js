import { useState, useCallback, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { authService } from '../services/authService';
import { useOffline } from './useOffline';
import { toast } from './useToast';
import db from '../db/auditDB';

export function useCashier() {
  const { user } = useAuth();
  const { syncPending, downloadJournal } = useOffline();
  
  // Persist cashier status in LocalStorage (Edge only)
  const [isOpen, setIsOpen] = useState(() => {
    return localStorage.getItem('lanche_caixa_aberto') === 'true';
  });

  const openCashier = useCallback(async (senha) => {
    try {
      // Re-verify password by trying to login (Simple way)
      await authService.login(user.email, senha);
      
      setIsOpen(true);
      localStorage.setItem('lanche_caixa_aberto', 'true');
      
      // Log event
      await db.turnos.add({
        aberto_em: new Date().toISOString(),
        usuario_id: user.id,
        tipo: 'ABERTURA'
      });
      
      toast.success('Sucesso', 'Caixa aberto com sucesso.');
      return true;
    } catch (err) {
      toast.error('Erro', 'Senha incorreta ou falha na autenticação.');
      return false;
    }
  }, [user]);

  const closeCashier = useCallback(async (senha) => {
    try {
      // Re-verify password
      await authService.login(user.email, senha);
      
      // 1. Trigger Sync
      toast.info('Sincronizando', 'Enviando vendas pendentes antes de fechar...');
      const syncResult = await syncPending();
      
      // 2. Set status to closed to block new sales
      setIsOpen(false);
      localStorage.setItem('lanche_caixa_aberto', 'false');

      // Log event
      await db.turnos.add({
        fechado_em: new Date().toISOString(),
        usuario_id: user.id,
        tipo: 'FECHAMENTO'
      });

      toast.success('Caixa Fechado', 'Turno encerrado e vendas sincronizadas.');
      return true;
    } catch (err) {
      toast.error('Erro', 'Senha incorreta ou falha no fechamento.');
      return false;
    }
  }, [user, syncPending]);

  return {
    isOpen,
    openCashier,
    closeCashier,
    downloadJournal
  };
}
