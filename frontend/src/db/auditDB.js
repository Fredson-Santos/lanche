import Dexie from 'dexie';

export const db = new Dexie('LancheAuditDB');

// Define database schema
db.version(1).stores({
  vendas_local: '++id_local, timestamp, status_sync, usuario_id',
  turnos: '++id_turno, aberto_em, fechado_em, usuario_id'
});

export default db;
