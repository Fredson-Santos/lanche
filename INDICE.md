# 📑 Índice de Documentação - LANCHE MVP

Guia centralizado para navegação e referência rápida de toda a documentação do projeto.

---

## 🎯 Comece Por Aqui

1. **Novo no projeto?** → [SETUP.md](SETUP.md)
2. **Quer entender a arquitetura?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md)
3. **Qual é o plano?** → [ROADMAP.md](ROADMAP.md)
4. **Como está a estrutura?** → [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md)

---

## 📚 Documentação por Categoria

### 🚀 Início Rápido & Setup

| Documento | Descrição | Para Quem |
|-----------|-----------|----------|
| [README.md](README.md) | Visão geral do projeto | Todos |
| [SETUP.md](SETUP.md) | Guia passo-a-passo de setup | Desenvolvedores |
| [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md) | Estrutura e checklist | Desenvolvedores |

### 📋 Planejamento & Roadmap

| Documento | Descrição | Para Quem |
|-----------|-----------|----------|
| [ROADMAP.md](ROADMAP.md) | Timeline completa do projeto (4 fases) | Product Owner, Dev Lead |
| [docs/README_MVP.md](docs/README_MVP.md) | Requisitos funcionais e não-funcionais | Analista, QA |
| [docs/LANCHE MVP.md](docs/LANCHE%20MVP.md) | Especificação técnica detalhada | Todos |

### 🏗️ Arquitetura & Design

| Documento | Descrição | Para Quem |
|-----------|-----------|----------|
| [docs/ARQUITETURA.md](docs/ARQUITETURA.md) | Arquitetura three-tier, fluxos, modelagem | Arquiteto, Dev |
| [docs/diagramas/01_DIAGRAMA_CLASSES_MVP.puml](docs/diagramas/01_DIAGRAMA_CLASSES_MVP.puml) | Diagrama de Classes UML | Arquiteto, Senior Dev |
| [docs/diagramas/02_DIAGRAMA_CASOS_USO_MVP.puml](docs/diagramas/02_DIAGRAMA_CASOS_USO_MVP.puml) | Casos de Uso do MVP | Analista, PO |
| [docs/diagramas/03_DIAGRAMA_SEQUENCIA_MVP.puml](docs/diagramas/03_DIAGRAMA_SEQUENCIA_MVP.puml) | Fluxos de Sequência | Dev |
| [docs/diagramas/04_DIAGRAMA_ESTADOS_MVP.puml](docs/diagramas/04_DIAGRAMA_ESTADOS_MVP.puml) | Estados da Autenticação | Dev Security |
| [docs/diagramas/05_DIAGRAMA_MER_MVP.puml](docs/diagramas/05_DIAGRAMA_MER_MVP.puml) | Modelagem ER do Banco | DBA, Dev |

### 🎓 Atividades & Cenários

| Documento | Descrição | Para Quem |
|-----------|-----------|----------|
| [docs/Atividade-a-Realizar/Atividade prática integradora.txt](docs/Atividade-a-Realizar/Atividade%20prática%20integradora.txt) | Atividade integradora do projeto | Estudantes |
| [docs/Atividade-a-Realizar/Cenario.md](docs/Atividade-a-Realizar/Cenario.md) | Cenário de negócio detalhado | Todos |

---

## 🔍 Procurando Algo Específico?

### Setup & Instalação
- **Como instalar?** → [SETUP.md](SETUP.md)
- **Estrutura de pastas?** → [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md)
- **Docker Compose?** → [SETUP.md](SETUP.md#opção-a-iniciando-com-docker-compose)
- **Variáveis de ambiente?** → [.env.example](.env.example)

### Desenvolvimento Backend
- **Stack tecnológico?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md#stack-tecnológico)
- **Estrutura do backend?** → [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md#backend-estrutura)
- **Models e schemas?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md#modelagem-de-dados)
- **Autenticação?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md#fluxo-de-autenticação)
- **Endpoints da API?** → [README.md](README.md#endpoints-principais)

### Desenvolvimento Frontend
- **Estrutura do frontend?** → [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md#frontend-estrutura)
- **Como rodar React?** → [SETUP.md](SETUP.md#frontend-react--vite)
- **Componentes?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md#frontend-react--vite)

### Requisitos & Especificações
- **Funcionalidades do MVP?** → [docs/README_MVP.md](docs/README_MVP.md#-funcionalidades-incluídas)
- **Requisitos funcionais (23 RFs)?** → [docs/README_MVP.md](docs/README_MVP.md#requisitos-funcionais-23-rfs)
- **Requisitos não-funcionais (17 RNFs)?** → [docs/README_MVP.md](docs/README_MVP.md#requisitos-não-funcionais-17-rnfs)
- **Regras de negócio (19 RNs)?** → [docs/README_MVP.md](docs/README_MVP.md#regras-de-negócio-19-rns)
- **Matriz de acesso?** → [docs/README_MVP.md](docs/README_MVP.md#matriz-de-acesso)

### Planejamento & Timeline
- **Quando será entregue?** → [ROADMAP.md](ROADMAP.md#-timeline-resumida)
- **Qual é a próxima fase?** → [ROADMAP.md](ROADMAP.md#-fase-1-setup--core-backend)
- **Quais são os riscos?** → [ROADMAP.md](ROADMAP.md#⚠️-riscos-identificados)
- **Como acompanhar progresso?** → [ROADMAP.md](ROADMAP.md#📈-métricas-de-progresso)

### Segurança
- **Como funciona autenticação?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md#fluxo-de-autenticação)
- **Matriz de acesso (RBAC)?** → [docs/README_MVP.md](docs/README_MVP.md#matriz-de-acesso)
- **Como senhas são protegidas?** → [docs/ARQUITETURA.md](docs/ARQUITETURA.md#segurança)

---

## 📊 Estrutura de Documentação

```
lanche/
├── README.md                          ← Comece aqui!
├── ROADMAP.md                         ← Timeline do projeto
├── SETUP.md                           ← Como configurar
├── ESTRUTURA_CRIADA.md               ← Checklist de estrutura
├── INDICE.md                         ← Este arquivo
├── .env.example                       ← Variáveis de ambiente
├── docker-compose.yml                ← Orquestração
│
├── backend/
│   ├── requirements.txt               ← Dependências Python
│   ├── .env.example                   ← Backend env template
│   └── Dockerfile                     ← Backend container
│
├── frontend/
│   ├── package.json                   ← Dependências Node
│   ├── .env.example                   ← Frontend env template
│   └── Dockerfile                     ← Frontend container
│
└── docs/
    ├── LANCHE MVP.md                  ← Especificação técnica
    ├── README_MVP.md                  ← Requisitos (RF/RNF/RN)
    ├── ARQUITETURA.md                 ← Arquitetura detalhada
    ├── Atividade-a-Realizar/
    │   ├── Atividade prática integradora.txt
    │   └── Cenario.md
    └── diagramas/
        ├── 01_DIAGRAMA_CLASSES_MVP.puml
        ├── 02_DIAGRAMA_CASOS_USO_MVP.puml
        ├── 03_DIAGRAMA_SEQUENCIA_MVP.puml
        ├── 04_DIAGRAMA_ESTADOS_MVP.puml
        └── 05_DIAGRAMA_MER_MVP.puml
```

---

## 🎯 Roadmap de Documentação

### Fase 1 (Semana 1-2)
- ✅ README.md
- ✅ SETUP.md
- ✅ ESTRUTURA_CRIADA.md
- ✅ ARQUITETURA.md
- ✅ ROADMAP.md
- ✅ INDICE.md (este)

### Fase 2 (Semana 2-3)
- ⏳ API Documentation (Swagger)
- ⏳ Guia de Contribuição
- ⏳ Coding Standards

### Fase 3 (Semana 3-5)
- ⏳ API Reference (endpoints)
- ⏳ Guia de Testes
- ⏳ Troubleshooting

### Fase 4 (Semana 5-7)
- ⏳ Manual do Usuário (Frontend)
- ⏳ FAQ
- ⏳ Guia de Operação

---

## 🚀 Próximos Passos

1. **Leia** [SETUP.md](SETUP.md) para configurar o ambiente
2. **Entenda** [docs/ARQUITETURA.md](docs/ARQUITETURA.md) para arquitetura
3. **Consulte** [ROADMAP.md](ROADMAP.md) para timeline
4. **Acompanhe** [ESTRUTURA_CRIADA.md](ESTRUTURA_CRIADA.md) para progresso

---

## 💡 Dicas de Navegação

- Use `Ctrl+K Ctrl+O` (VSCode) para abrir rápido qualquer arquivo
- Use `Ctrl+Shift+F` para buscar em todos os documentos
- Clone este repositório para ter tudo offline
- Abra os arquivos `.puml` com extensões PlantUML para visualizar diagramas

---

## 📞 Dúvidas?

- **Setup:** Veja [SETUP.md](SETUP.md)
- **Arquitetura:** Veja [docs/ARQUITETURA.md](docs/ARQUITETURA.md)
- **Requisitos:** Veja [docs/README_MVP.md](docs/README_MVP.md)
- **Timeline:** Veja [ROADMAP.md](ROADMAP.md)

---

**Última atualização:** Abril 19, 2026  
**Documentação:** v1.0  
**Status:** ✅ Completa
