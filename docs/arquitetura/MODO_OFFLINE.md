# 🔌 Modo Offline - Arquitetura e Implementação (TASK 3A)

**Data:** 21 de Abril de 2026  
**Status:** 🚀 Em Progresso (Valida\u00e7\u00f5es e UX Completas)  
**Responsável:** Frontend Development + Backend  
**Requisitos:** RF-09 (Modo Offline), RF-10 (Sincroniza\u00e7\u00e3o P\u00f3s-Offline)

---

## \ud83c\udf1f Vis\u00e3o Geral

O **Modo Offline** permite que operadores de caixa continuem vendendo mesmo sem conex\u00e3o com o servidor, com sincroniza\u00e7\u00e3o autom\u00e1tica quando reconectado.

```
┌─────────────────────────────────────────────────────────────────┐
│                      MODO OFFLINE                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Online                   → Sincroniza em tempo real           │
│  ├─ Venda criada         → POST /api/vendas/                  │
│  ├─ Estoque atualizado   → PUT /api/estoque/                  │
│  └─ Resposta enviada     → UI atualiza                        │
│                                                                 │
│  Offline                  → Armazena Localmente               │
│  ├─ Venda criada         → IndexedDB.vendas_local             │
│  ├─ Status: pendente     → Aguardando sincroniza\u00e7\u00e3o       │
│  ├─ Valida\u00e7\u00e3o de estoque → Local (BlockedUI)            │
│  └─ Download de auditoria→ JSON local                          │
│                                                                 │
│  Reconectando             → Sincronizar                        │
│  ├─ Detecta conex\u00e3o     → Service Worker online event       │
│  ├─ Batch sync           → POST /api/vendas/sync              │
│  ├─ Resolve conflitos    → Server-wins strategy               │
│  └─ Limpa IndexedDB      → User confirm                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## \ud83d\udcc4 Componentes Implementados

### 1. IndexedDB Schema (Dexie)

**Arquivo:** `frontend/src/db/auditDB.js`

```javascript
import Dexie from 'dexie';

const db = new Dexie('LancheDB');
db.version(1).stores({
  vendas_local: '++id_local, timestamp, status_sync, usuario_id',
  turnos: '++id, usuario_id, tipo'
});

export default db;
```

**Tabelas:**

| Tabela | Campos | Prop\u00f3sito |
|--------|--------|----------|
| `vendas_local` | id_local, timestamp, dados_venda, status_sync, server_id | Armazena vendas pendentes |
| `turnos` | id, usuario_id, aberto_em, fechado_em, tipo | Registra abertura/fechamento de caixas |

### 2. Hook useOffline

**Arquivo:** `frontend/src/hooks/useOffline.js`

#### Funcionalidades:

```javascript
export function useOffline() {
  // ✅ Monitoramento de conectividade
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  // ✅ Logging de venda ao IndexedDB
  const logSale = async (vendaData, status, serverId) => {
    const id = await db.vendas_local.add({
      timestamp: new Date().toISOString(),
      dados_venda: vendaData,
      status_sync: status,
      server_id: serverId
    });
    return id;
  };

  // ✅ Marcar como sincronizada
  const updateSyncStatus = async (localId, serverId, status) => {
    await db.vendas_local.update(localId, {
      status_sync: status,
      server_id: serverId
    });
  };

  // ✅ Sincronizar todas as vendas pendentes
  const syncPending = async () => {
    const pending = await db.vendas_local
      .where('status_sync').equals('pendente').toArray();

    for (const sale of pending) {
      try {
        const syncPayload = { itens: sale.dados_venda.itens };
        const response = await api.post('/api/vendas/', syncPayload);
        await updateSyncStatus(sale.id_local, response.data.id, 'sincronizado');
      } catch (err) {
        console.error('Erro na sincroniza\u00e7\u00e3o:', err);
      }
    }
  };

  // ✅ Exportar logs em JSON
  const downloadJournal = async () => {
    const logs = await db.vendas_local.toArray();
    const dataStr = JSON.stringify(logs, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `auditoria_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  // ✅ Limpar todas as vendas (ap\u00f3s confirma\u00e7\u00e3o)
  const clearAllSales = async () => {
    await db.vendas_local.clear();
    setPendingCount(0);
  };

  return {
    isOnline,
    pendingCount,
    logSale,
    updateSyncStatus,
    syncPending,
    downloadJournal,
    clearAllSales
  };
}
```

### 3. Hook useCashier

**Arquivo:** `frontend/src/hooks/useCashier.js`

#### Fluxo de Fechamento:

```javascript
const closeCashier = useCallback(async (senha) => {
  try {
    // 1. Valida senha
    await authService.login(user.email, senha);

    // 2. Sincroniza vendas pendentes
    await syncPending();

    // 3. Fecha caixa
    setIsOpen(false);
    localStorage.setItem('lanche_caixa_aberto', 'false');

    // 4. Log de evento
    await db.turnos.add({
      fechado_em: new Date().toISOString(),
      usuario_id: user.id,
      tipo: 'FECHAMENTO'
    });

    return true;
  } catch (err) {
    return false;
  }
}, [user, syncPending]);
```

### 4. Valida\u00e7\u00f5es de Estoque (TASK 3A-UX)

**Arquivo:** `frontend/src/pages/VendasPage.jsx`

#### Bloqueios Implementados:

```javascript
// 1. N\u00e3o permitir adicionar sem estoque
const addToCart = (produto) => {
  const estoque = stockInfo[produto.id] || 0;
  const emCarrinho = cart.find(i => i.produto_id === produto.id)?.quantidade || 0;

  if (estoque === 0) {
    toast.error('Sem Estoque', `${produto.nome} n\u00e3o est\u00e1 dispon\u00edvel.`);
    return;
  }

  if (emCarrinho >= estoque) {
    toast.warning('Estoque Insuficiente', 
      `Voc\u00ea j\u00e1 tem ${emCarrinho} ${produto.nome}. Estoque: ${estoque}`);
    return;
  }

  // Adicionar ao carrinho
  // ...
};

// 2. N\u00e3o permitir aumentar acima do estoque
const updateQty = (produto_id, delta) => {
  const item = cart.find(i => i.produto_id === produto_id);
  const novaQtd = item.quantidade + delta;
  const estoque = stockInfo[produto_id] || 0;

  if (delta > 0 && novaQtd > estoque) {
    toast.warning('Estoque Insuficiente', 
      `Estoque dispon\u00edvel: ${estoque}`);
    return;
  }

  // Atualizar quantidade
  // ...
};
```

### 5. Modal de Download

**Arquivo:** `frontend/src/pages/VendasPage.jsx`

```javascript
// Ap\u00f3s fechar caixa com sucesso
<Modal
  open={showDownloadAfterClose}
  title="Finalizar Turno"
  icon="✅"
>
  <p>Deseja baixar o arquivo de auditoria (.json)?</p>
  <footer>
    <Button onClick={() => clearAllSales()}>
      N\u00e3o, apenas apagar
    </Button>
    <Button onClick={() => {
      downloadJournal();
      clearAllSales();
    }}>
      Sim, baixar e apagar
    </Button>
  </footer>
</Modal>
```

---

## \ud83d\udd�\ufe0f Fluxo Completo de Opera\u00e7\u00e3o

### Cen\u00e1rio 1: Online (Normal)

```
1. Caixa abre caixa (senha verificada no servidor)
   ↓
2. Adiciona produto ao carrinho
   ↓
3. Valida estoque localmente (stockInfo atualizado)
   ↓
4. Finaliza venda
   ↓
5. POST /api/vendas/ → 200 OK
   ↓
6. logSale() marca como sincronizado
   ↓
7. Toast: "Venda finalizada!"
```

### Cen\u00e1rio 2: Offline (Sem Internet)

```
1. Caixa abre caixa (senha verificada offline - localStorage)
   ↓
2. Adiciona produto ao carrinho
   ↓
3. Valida estoque localmente
   ↓
4. Finaliza venda
   ↓
5. POST /api/vendas/ → TIMEOUT (sem rede)
   ↓
6. logSale() marca como PENDENTE no IndexedDB
   ↓
7. Toast: "Sem conex\u00e3o. Salvo para sincroniza\u00e7\u00e3o"
   ↓
8. Venda permanece em IndexedDB
```

### Cen\u00e1rio 3: Reconectando

```
1. Internet volta
   ↓
2. useOffline detecta online event
   ↓
3. OfflineStatusBanner mostra "Sincronizar Agora"
   ↓
4. Operador clica (ou sincroniza automaticamente)
   ↓
5. syncPending() POST /api/vendas/sync
   ↓
6. Backend processa todas as vendas pendentes
   ↓
7. IndexedDB marca como sincronizado
   ↓
8. Toast: "Sincroniza\u00e7\u00e3o conclu\u00edda"
```

### Cen\u00e1rio 4: Fechando Caixa

```
1. Caixa clica "Fechar Caixa"
   ↓
2. Insere senha
   ↓
3. Sistema sincroniza vendas pendentes
   ↓
4. Caixa fecha (localStorage.lanche_caixa_aberto = false)
   ↓
5. Modal aparece: "Deseja baixar auditoria?"
   ↓
6. Op\u00e7\u00e3o 1: "Sim, baixar e apagar"
   → downloadJournal() → clearAllSales()
   ↓
   Op\u00e7\u00e3o 2: "N\u00e3o, apenas apagar"
   → clearAllSales()
   ↓
7. IndexedDB limpo
   ↓
8. Toast: "Conclu\u00eddo"
```

---

## \ud83d\udc� Estrutura de Dados - IndexedDB

### Tabela: vendas_local

```json
{
  "id_local": 1,
  "timestamp": "2026-04-21T10:30:00Z",
  "dados_venda": {
    "usuario_id": 2,
    "itens": [
      {
        "produto_id": 1,
        "quantidade": 2,
        "preco_unitario": 15.00
      }
    ]
  },
  "status_sync": "pendente",
  "server_id": null
}
```

### Tabela: turnos

```json
{
  "id": 1,
  "usuario_id": 2,
  "aberto_em": "2026-04-21T08:00:00Z",
  "fechado_em": "2026-04-21T16:00:00Z",
  "tipo": "ABERTURA"
}
```

---

## \ud83e\uddee Casos de Uso

### Use Case 1: Venda Offline

```
DADO que estou offline
QUANDO finalizo uma venda
ENT\u00c3O venda \u00e9 armazenada em IndexedDB
E operador v\u00ea toast "Salvo para sincroniza\u00e7\u00e3o"
```

### Use Case 2: Sincroniza\u00e7\u00e3o Manual

```
DADO que tenho vendas pendentes
E internet volta
QUANDO clico "Sincronizar Agora"
ENT\u00c3O vendas s\u00e3o enviadas ao servidor
E marcadas como sincronizadas
```

### Use Case 3: Bloqueio de Estoque

```
DADO que produto tem estoque = 0
QUANDO tento adicionar ao carrinho
ENT\u00c3O a\u00e7\u00e3o \u00e9 bloqueada
E vejo toast "Sem Estoque"
```

### Use Case 4: Download de Auditoria

```
DADO que fechei o caixa
QUANDO escolho "Sim, baixar e apagar"
ENT\u00c3O arquivo JSON \u00e9 baixado
E IndexedDB \u00e9 limpo
```

---

## \ud83d\udd§ Configura\u00e7\u00e3o Recomendada (Pr\u00f3ximas Fases)

### Service Worker (Fase 3A-2)

```javascript
// frontend/src/service-worker.js
self.addEventListener('install', event => {
  // Cache est\u00e1tico
  event.waitUntil(
    caches.open('v1').then(cache => {
      return cache.addAll([
        '/',
        '/index.html',
        '/assets/...'
      ]);
    })
  );
});

self.addEventListener('fetch', event => {
  // Estratégia: cache first, fallback network
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
      .catch(() => caches.match('/offline.html'))
  );
});
```

### Sincroniza\u00e7\u00e3o Autom\u00e1tica

```javascript
// Detectar reconex\u00e3o
window.addEventListener('online', async () => {
  console.log('\ud83d\udd0d Online! Sincronizando...');
  await syncPending();
});
```

---

## \ud83d\udccb Documentos Relacionados

- [TASK_3A_VALIDACOES_UX.md](../tasks/TASK_3A_VALIDACOES_UX.md) - Valida\u00e7\u00f5es de estoque implementadas
- [useOffline Hook](../../frontend/src/hooks/useOffline.js) - C\u00f3digo do hook
- [useCashier Hook](../../frontend/src/hooks/useCashier.js) - C\u00f3digo do hook
- [VendasPage](../../frontend/src/pages/VendasPage.jsx) - Interface de vendas
- [auditDB.js](../../frontend/src/db/auditDB.js) - Schema IndexedDB

---

## \u2705 Status de Implementa\u00e7\u00e3o

| Componente | Status | Data |
|-----------|--------|------|
| **IndexedDB Schema** | ✅ Completo | 21/04 |
| **useOffline Hook** | ✅ Completo | 21/04 |
| **useCashier Hook** | ✅ Completo | 21/04 |
| **Valida\u00e7\u00f5es de Estoque** | ✅ Completo | 21/04 |
| **Modal de Download** | ✅ Completo | 21/04 |
| **Limpeza de Dados** | ✅ Completo | 21/04 |
| **Service Worker** | \ud83d\udccb Planejado | TBD |
| **Sync Autom\u00e1tico** | \ud83d\udccb Planejado | TBD |
| **Endpoint /api/vendas/sync** | \ud83d\udccb Planejado | TBD |

---

## \ud83d\ude80 Pr\u00f3ximos Passos

### Imediato
- [ ] Testar completo offline mode com rede desligada
- [ ] Validar UI em mobile devices
- [ ] Testar sincroniza\u00e7\u00e3o de dados

### Curto Prazo
- [ ] Implementar Service Worker
- [ ] Adicionar sincroniza\u00e7\u00e3o autom\u00e1tica
- [ ] Criar endpoint backend /api/vendas/sync
- [ ] Performance testing com muitos produtos

### M\u00e9dio Prazo
- [ ] Testes E2E automatizados (Cypress/Playwright)
- [ ] Resolu\u00e7\u00e3o de conflitos avan\u00e7ada
- [ ] Documenta\u00e7\u00e3o de operador

---

**Preparado por:** Tim Dev  
**Data:** 21 de Abril de 2026  
**Vers\u00e3o:** 1.0  
**Status:** \ud83d\ude80 Em Progresso
