# Plano de Implementação: Integração de Alertas e UI de Integrações

Este plano descreve as etapas para integrar a página de Alertas e criar a interface de gerenciamento de API Keys (Integrações) no frontend, utilizando as APIs já disponíveis no backend.

## User Review Required

> [!IMPORTANT]
> A página de **Integrações (API Keys)** será restrita apenas ao papel de **Administrador**, conforme as regras de negócio definidas. A página de **Alertas** será visível para Admin e Gerente.

---

## Proposed Changes

### 1. Sistema de Alertas
O backend já possui a lógica de alertas de validade, temperatura e estoque. A página frontend também já existe, mas não está acessível.

#### [MODIFY] [App.jsx](file:///c:/Users/Fred/Projetos/lanche/frontend/src/App.jsx)
*   Importar `AlertasPage`.
*   Adicionar a rota `/alertas` protegida para os roles `['admin', 'gerente']`.

#### [MODIFY] [Sidebar.jsx](file:///c:/Users/Fred/Projetos/lanche/frontend/src/components/layout/Sidebar.jsx)
*   Adicionar o item "Alertas" ao array `NAV_ITEMS` com ícone ⚠️ e permissões para Admin e Gerente.

#### [MODIFY] [DashboardPage.jsx](file:///c:/Users/Fred/Projetos/lanche/frontend/src/pages/DashboardPage.jsx)
*   Integrar um card de resumo ou badge de alertas ativos que linka para a página de Alertas.

---

### 2. Interface de Integrações (API Keys)
Criar uma interface para gerenciar chaves de acesso de terceiros (Delivery, Parceiros).

#### [NEW] [ApiKeysPage.jsx](file:///c:/Users/Fred/Projetos/lanche/frontend/src/pages/ApiKeysPage.jsx)
*   Criar uma nova página que utiliza o hook `useApi`.
*   **Funcionalidades:**
    *   Listagem de chaves existentes (exibindo apenas o prefixo).
    *   Modal de criação de nova chave (Descrição, Limite de Reqs, Validade).
    *   Exibição da chave gerada (mostrada apenas uma vez com aviso de segurança).
    *   Ações de Ativar/Desativar e Revogar.

#### [MODIFY] [App.jsx](file:///c:/Users/Fred/Projetos/lanche/frontend/src/App.jsx)
*   Importar `ApiKeysPage`.
*   Adicionar a rota `/integracoes` protegida exclusivamente para o role `['admin']`.

#### [MODIFY] [Sidebar.jsx](file:///c:/Users/Fred/Projetos/lanche/frontend/src/components/layout/Sidebar.jsx)
*   Adicionar o item "Integrações" ao array `NAV_ITEMS` com ícone 🔌 e permissão apenas para Admin.

---

## Open Questions

*   **Design das API Keys:** Deseja que a chave gerada seja exibida em um modal de destaque com botão de "Copiar para área de transferência"?
*   **Alertas no Dashboard:** Devemos exibir apenas o número de alertas não lidos ou uma lista dos 3 mais recentes?

## Verification Plan

### Automated Tests
*   Verificar se a rota `/integracoes` retorna redirecionamento para usuários sem role `admin`.
*   Testar o fluxo de criação de API Key e garantir que a chave completa é exibida após o sucesso.

### Manual Verification
*   Login como **Admin**: Verificar se ambos os itens (Alertas e Integrações) aparecem no menu.
*   Login como **Gerente**: Verificar se apenas Alertas aparece.
*   Login como **Caixa**: Verificar se nenhum dos dois aparece.
*   Testar marcar um alerta como lido e validar se a lista de "Não lidos" atualiza.
