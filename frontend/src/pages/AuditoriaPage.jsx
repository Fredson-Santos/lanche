import React, { useEffect, useState } from 'react';
import db from '../db/auditDB';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { useOffline } from '../hooks/useOffline';

const fmtBRL = (v) => v.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
const fmtDate = (iso) => new Date(iso).toLocaleString('pt-BR', { day:'2-digit', month:'2-digit', year:'numeric', hour:'2-digit', minute:'2-digit' });

export default function AuditoriaPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const { downloadJournal } = useOffline();

  useEffect(() => {
    async function loadLogs() {
      const data = await db.vendas_local.orderBy('id_local').reverse().toArray();
      setLogs(data);
      setLoading(false);
    }
    loadLogs();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'sincronizado': return 'var(--color-success)';
      case 'pendente': return 'var(--color-warning)';
      default: return 'var(--color-text-muted)';
    }
  };

  return (
    <div className="animate-fade-in">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 className="page-title">Auditoria Local</h1>
          <p className="page-subtitle">Jornal de transações persistido neste dispositivo</p>
        </div>
        <Button variant="primary" onClick={downloadJournal}>
          📥 Exportar Log (.json)
        </Button>
      </div>

      <Card>
        <CardHeader title="Registros do Dispositivo" subtitle="Histórico redundante para auditoria física" />
        
        {loading ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>Carregando logs locais...</div>
        ) : logs.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📋</div>
            <p className="empty-state-title">Nenhum registro local encontrado</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>ID Local</th>
                  <th>Data/Hora</th>
                  <th>Status Sync</th>
                  <th>Itens</th>
                  <th>ID Servidor</th>
                </tr>
              </thead>
              <tbody>
                {logs.map(log => (
                  <tr key={log.id_local}>
                    <td style={{ fontWeight: 600 }}>#{log.id_local}</td>
                    <td>{fmtDate(log.timestamp)}</td>
                    <td>
                      <span style={{ 
                        color: getStatusColor(log.status_sync),
                        fontWeight: 600,
                        fontSize: '0.8rem',
                        textTransform: 'uppercase'
                      }}>
                        {log.status_sync}
                      </span>
                    </td>
                    <td>{log.dados_venda.itens.length} itens</td>
                    <td style={{ fontSize: '0.8rem', fontFamily: 'monospace' }}>
                      {log.server_id || '---'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>

      <div className="alert-box info" style={{ marginTop: '24px' }}>
        <strong>Nota de Segurança:</strong> Estes dados são armazenados exclusivamente no banco de dados IndexedDB deste navegador e servem como redundância caso haja divergência com o servidor central.
      </div>
    </div>
  );
}
