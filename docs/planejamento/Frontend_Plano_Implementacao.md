# Frontend LANCHE MVP — Plano de Implementação

## Contexto

O **LANCHE MVP** é um sistema de gestão para varejo alimentício. O backend já está estruturado em FastAPI (Python) com SQLite, mas sem rotas funcionais ainda — apenas o esqueleto de auth, models e DB. O frontend está essencialmente zerado (`App.jsx` com apenas um contador de exemplo).

Serei responsável por **projetar e implementar o frontend completo** em **React 18 + Vite**, com design premium e integração com a API.

---

## Visão Geral da Aplicação

### Roles e Acesso (RBAC)
| Área | Caixa | Gerente | Admin |
|------|-------|---------|-------|
| Login | ✅ | ✅ | ✅ |
| Vendas (Nova + Histórico) | ✅ | ✅ | ✅ |
| Produtos (consulta) | ✅ | ✅ | ✅ |
| Produtos (CRUD) | ❌ | ✅ | ✅ |
| Estoque (consulta) | ✅ | ✅ | ✅ |
| Estoque (atualizar) | ❌ | ✅ | ✅ |
| Relatórios | ❌ | ✅ | ✅ |
| Usuários (CRUD) | ❌ | ❌ | ✅ |

---

## Design System

### Paleta de Cores
- **Primária:** `#F97316` (laranja vibrante — identidade de lanchonete)
- **Fundo principal:** `#0F172A` (dark slate)
- **Fundo card:** `#1E293B`
- **Fundo sidebar:** `#111827`
- **Texto primário:** `#F8FAFC`
- **Texto secundário:** `#94A3B8`
- **Sucesso:** `#22C55E`
- **Perigo:** `#EF4444`
- **Aviso:** `#EAB308`
- **Glassmorphism:** `rgba(30, 41, 59, 0.85)` + `backdrop-filter: blur(12px)`

### Tipografia
- **Fonte:** `Inter` (Google Fonts)
- **Títulos:** `700` / `600`
- **Corpo:** `400` / `500`

### Estilo Geral
- Dark mode como padrão
- Cards com `border-radius: 12px` e `border: 1px solid rgba(255,255,255,0.07)`
- Transições suaves (`0.2s ease`)
- Micro-animações nas interações
- Sidebar fixa no desktop, drawer no mobile

---

## Páginas e Componentes

### Páginas (Rotas)
| Rota | Componente | Acesso |
|------|-----------|--------|
| `/login` | `LoginPage` | Público |
| `/dashboard` | `DashboardPage` | Todos |
| `/vendas` | `VendasPage` | Todos |
| `/produtos` | `ProdutosPage` | Todos |
| `/estoque` | `EstoquePage` | Todos |
| `/relatorios` | `RelatoriosPage` | Gerente + Admin |
| `/usuarios` | `UsuariosPage` | Admin |

### Componentes Reutilizáveis
- `Sidebar` — Navegação lateral com ícones e labels
- `Topbar` — Header com info do usuário e logout
- `Button` — Variantes: primary, secondary, danger, ghost
- `Input` / `Select` — Inputs estilizados com validação visual
- `Modal` — Overlay para forms de criação/edição
- `Table` — Tabela com paginação e ordenação
- `Badge` — Status (ativo/inativo, role)
- `Card` — Container de conteúdo
- `StatCard` — Card de métrica para dashboard
- `Toast` — Notificações de sucesso/erro
- `Spinner` / `Skeleton` — Loading states
- `ProtectedRoute` — HOC para RBAC

---

## Arquitetura de Estado e Serviços

### Context API
- `AuthContext` — Usuário logado, token JWT, role, funções login/logout

### Services (Axios)
- `api.js` — Instância Axios com baseURL e interceptor de token
- `authService.js` — `login()`, `logout()`
- `productService.js` — CRUD produtos
- `stockService.js` — get/update estoque
- `salesService.js` — criar venda, adicionar itens, histórico
- `reportService.js` — relatórios de vendas e faturamento
- `userService.js` — CRUD usuários (admin)

### Hooks Customizados
- `useAuth()` — Acesso ao AuthContext
- `useApi()` — Wrapper para chamadas com loading/error state
- `useToast()` — Disparar notificações

---

## Estrutura de Arquivos (Alvo)

```
frontend/src/
├── main.jsx
├── App.jsx
├── App.css
├── components/
│   ├── ui/
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Select.jsx
│   │   ├── Modal.jsx
│   │   ├── Table.jsx
│   │   ├── Badge.jsx
│   │   ├── Card.jsx
│   │   ├── StatCard.jsx
│   │   ├── Toast.jsx
│   │   └── Spinner.jsx
│   ├── layout/
│   │   ├── Sidebar.jsx
│   │   ├── Topbar.jsx
│   │   └── Layout.jsx
│   └── auth/
│       └── ProtectedRoute.jsx
├── pages/
│   ├── LoginPage.jsx
│   ├── DashboardPage.jsx
│   ├── VendasPage.jsx
│   ├── ProdutosPage.jsx
│   ├── EstoquePage.jsx
│   ├── RelatoriosPage.jsx
│   └── UsuariosPage.jsx
├── services/
│   ├── api.js
│   ├── authService.js
│   ├── productService.js
│   ├── stockService.js
│   ├── salesService.js
│   ├── reportService.js
│   └── userService.js
├── hooks/
│   ├── useAuth.js
│   ├── useApi.js
│   └── useToast.js
├── context/
│   └── AuthContext.jsx
└── styles/
    └── index.css
```

---

## Proposed Changes

### Layer 1 — Fundação (Design System + Infra)

#### [MODIFY] `frontend/src/styles/index.css`
Criar o design system completo com CSS custom properties (tokens de cor, tipografia, espaçamento, animações).

#### [MODIFY] `frontend/src/main.jsx`
Envolver App com `AuthProvider` e `BrowserRouter`.

#### [MODIFY] `frontend/src/App.jsx`
Configurar rotas com `react-router-dom`, incluindo `ProtectedRoute`.

---

### Layer 2 — Context, Hooks & Services

#### [NEW] `frontend/src/context/AuthContext.jsx`
Context com `user`, `token`, `role`, `login()`, `logout()`. Persiste em `localStorage`.

#### [NEW] `frontend/src/hooks/useAuth.js`
Hook que consome `AuthContext`.

#### [NEW] `frontend/src/hooks/useApi.js`
Hook genérico: `{ data, loading, error, execute }`.

#### [NEW] `frontend/src/hooks/useToast.js`
Hook para disparar toasts globais.

#### [NEW] `frontend/src/services/api.js`
Instância Axios configurada com baseURL e interceptors para JWT.

#### [NEW] `frontend/src/services/authService.js`
#### [NEW] `frontend/src/services/productService.js`
#### [NEW] `frontend/src/services/stockService.js`
#### [NEW] `frontend/src/services/salesService.js`
#### [NEW] `frontend/src/services/reportService.js`
#### [NEW] `frontend/src/services/userService.js`

---

### Layer 3 — Componentes UI

#### [NEW] `frontend/src/components/ui/Button.jsx`
#### [NEW] `frontend/src/components/ui/Input.jsx`
#### [NEW] `frontend/src/components/ui/Select.jsx`
#### [NEW] `frontend/src/components/ui/Modal.jsx`
#### [NEW] `frontend/src/components/ui/Table.jsx`
#### [NEW] `frontend/src/components/ui/Badge.jsx`
#### [NEW] `frontend/src/components/ui/Card.jsx`
#### [NEW] `frontend/src/components/ui/StatCard.jsx`
#### [NEW] `frontend/src/components/ui/Toast.jsx`
#### [NEW] `frontend/src/components/ui/Spinner.jsx`

---

### Layer 4 — Layout

#### [NEW] `frontend/src/components/layout/Sidebar.jsx`
Sidebar fixa com logo, navegação por role e indicador de página ativa.

#### [NEW] `frontend/src/components/layout/Topbar.jsx`
Header com nome do usuário, role badge e botão de logout.

#### [NEW] `frontend/src/components/layout/Layout.jsx`
Wrapper que compõe Sidebar + Topbar + conteúdo.

#### [NEW] `frontend/src/components/auth/ProtectedRoute.jsx`
Redireciona para `/login` se não autenticado. Bloqueia por role se necessário.

---

### Layer 5 — Páginas

#### [NEW] `frontend/src/pages/LoginPage.jsx`
Formulário de login com e-mail e senha, validação e feedback de erro.

#### [NEW] `frontend/src/pages/DashboardPage.jsx`
Cards de métricas: total de vendas hoje, produtos ativos, itens com estoque baixo, faturamento do dia.

#### [NEW] `frontend/src/pages/ProdutosPage.jsx`
Tabela de produtos com busca, filtro ativo/inativo, modal de criação/edição, botão de deletar (Admin).

#### [NEW] `frontend/src/pages/EstoquePage.jsx`
Tabela de estoque com indicadores de nível (baixo/normal/alto), atualização inline para Gerente+.

#### [NEW] `frontend/src/pages/VendasPage.jsx`
Interface de caixa: busca de produtos, carrinho com itens, total calculado, botão finalizar venda. Aba de histórico de vendas.

#### [NEW] `frontend/src/pages/RelatoriosPage.jsx`
Filtro por período (data início/fim), tabela de vendas, total faturado, gráfico simples de barras em CSS.

#### [NEW] `frontend/src/pages/UsuariosPage.jsx`
CRUD de usuários (Admin only): tabela, modal de criação com seleção de role, ativar/desativar.

---

## Estratégia de Mock/API

> [!IMPORTANT]
> Como o backend ainda não tem rotas funcionais (apenas auth.py esqueleto), o frontend será construído com **dados mockados** nos services, com estrutura de API já apontando para `http://localhost:8000`. Quando o backend estiver pronto, basta remover os mocks.

```js
// services/productService.js (exemplo)
export const getProducts = async () => {
  // return await api.get('/produtos') // Ativar quando backend pronto
  return { data: MOCK_PRODUCTS } // Mock temporário
}
```

---

## Verificação

### Testes Funcionais
- [ ] Login com credenciais válidas → redireciona para dashboard
- [ ] Login inválido → exibe toast de erro
- [ ] Logout → limpa contexto e redireciona para `/login`
- [ ] Rota protegida sem login → redireciona para `/login`
- [ ] Rota de Admin acessada por Caixa → redireciona para `/dashboard`
- [ ] CRUD de produtos funciona via modal
- [ ] Venda: adicionar produto, remover, finalizar
- [ ] Relatório: filtrar por período e ver resultados

### Validação Visual
- Revisar no browser após `npm run dev`
- Verificar responsividade mobile (375px)
- Verificar dark mode, cores e animações
