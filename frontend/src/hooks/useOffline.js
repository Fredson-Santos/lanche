import { useState, useEffect, useCallback } from 'react';
import db from '../db/auditDB';
import api from '../services/api';
import { toast } from './useToast';

export function useOffline() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [pendingCount, setPendingCount] = useState(0);

  // Monitor Network Status
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Sync count update
  const updatePendingCount = useCallback(async () => {
    const count = await db.vendas_local.where('status_sync').equals('pendente').count();
    setPendingCount(count);
  }, []);

  useEffect(() => {
    updatePendingCount();
  }, [updatePendingCount]);

  // Log a sale to IndexedDB
  const logSale = async (vendaData, status = 'pendente', serverId = null) => {
    const id = await db.vendas_local.add({
      timestamp: new Date().toISOString(),
      dados_venda: vendaData,
      status_sync: status,
      server_id: serverId
    });
    updatePendingCount();
    return id;
  };

  // Update status after sync
  const updateSyncStatus = async (localId, serverId, status = 'sincronizado') => {
    await db.vendas_local.update(localId, {
      status_sync: status,
      server_id: serverId
    });
    updatePendingCount();
  };

  // Synchronize all pending sales
  const syncPending = async () => {
    const pending = await db.vendas_local.where('status_sync').equals('pendente').toArray();
    
    console.log('Vendas pendentes para sincronizar:', pending.length);
    pending.forEach(p => {
      console.log('  -', { id_local: p.id_local, timestamp: p.timestamp, itens_count: p.dados_venda.itens?.length || 0 });
    });

    if (pending.length === 0) return { success: true, count: 0 };

    let successCount = 0;
    let failCount = 0;

    for (const sale of pending) {
      try {
        // Prepara o payload para sincronização - apenas itens
        // Backend irá usar o current_user.id para usuario_id
        const syncPayload = {
          itens: sale.dados_venda.itens || []
        };
        
        console.log('Sincronizando venda:', { id_local: sale.id_local, payload: JSON.stringify(syncPayload) });
        
        const response = await api.post('/api/vendas/', syncPayload);
        await updateSyncStatus(sale.id_local, response.data.id, 'sincronizado');
        console.log('✅ Venda sincronizada com sucesso:', { id_local: sale.id_local, serverId: response.data.id });
        successCount++;
      } catch (err) {
        const errorDetail = err.response?.data?.detail || err.response?.data || err.message;
        console.error('❌ Falha ao sincronizar venda:', { id_local: sale.id_local, error: errorDetail });
        failCount++;
      }
    }

    if (successCount > 0) {
      toast.success('Sincronização', `${successCount} venda(s) sincronizada(s) com sucesso.`);
    }
    if (failCount > 0) {
      toast.error('Sincronização', `${failCount} venda(s) falharam ao sincronizar. Verifique o console para detalhes.`);
    }

    return { success: failCount === 0, count: successCount };
  };

  // Export audit log as JSON
  const downloadJournal = async () => {
    const all = await db.vendas_local.toArray();
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(all, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", `auditoria_vendas_${new Date().toISOString().split('T')[0]}.json`);
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  // Clear all sales from local database (called when cashier closes)
  const clearAllSales = async () => {
    try {
      await db.vendas_local.clear();
      setPendingCount(0);
      console.log('✅ Todas as vendas locais foram apagadas');
    } catch (err) {
      console.error('❌ Erro ao apagar vendas locais:', err);
    }
  };

  return {
    isOnline,
    pendingCount,
    logSale,
    updateSyncStatus,
    syncPending,
    downloadJournal,
    clearAllSales,
    refreshPending: updatePendingCount
  };
}
