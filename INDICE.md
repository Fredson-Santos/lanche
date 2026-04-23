# 📑 Índice de Documentação - LANCHE

Guia centralizado para navegação e referência rápida da documentação do projeto final.

---

## 🎯 Comece Por Aqui

1. **Quer entender a arquitetura?** → [docs/arquitetura/ARQUITETURA.md](docs/arquitetura/ARQUITETURA.md)
2. **Visão Geral** → [README.md](README.md)

---

## 📚 Documentação por Categoria

### 🏗️ Arquitetura & Design
| Documento | Descrição |
|-----------|-----------|
| [ARQUITETURA.md](docs/arquitetura/ARQUITETURA.md) | Arquitetura three-tier, fluxos, modelagem |
| [ESPECIFICACOES_TECNICAS.md](docs/ESPECIFICACOES_TECNICAS.md) | Detalhamento da Stack e Criptografia (Resumo) |
| [MODO_OFFLINE.md](docs/arquitetura/MODO_OFFLINE.md) | Modo Offline: IndexedDB, Sincronização, Validações |
| [ENCRYPTION_SETUP.md](docs/arquitetura/ENCRYPTION_SETUP.md) | Guia de configuração de criptografia de banco |
| [Diagrama de Classes](docs/arquitetura/diagramas/01_DIAGRAMA_CLASSES_MVP.puml) | Modelagem de classes UML |
| [Casos de Uso](docs/arquitetura/diagramas/02_DIAGRAMA_CASOS_USO_MVP.puml) | Diagrama de casos de uso |

### 📋 Requisitos & Negócio
| Documento | Descrição |
|-----------|-----------|
| [REQUISITOS_MVP.md](docs/requisitos/REQUISITOS_MVP.md) | Especificação técnica, RF, RNF e RN (Unificado) |

### 🧪 Testes & Qualidade
| Documento | Descrição |
|-----------|-----------|
| [TESTES_VALIDACAO_FINAL.md](docs/testes/TESTES_VALIDACAO_FINAL.md) | Plano de testes e documentação de validação |

---

## 📊 Estrutura de Pastas (Organizada)

```text
lanche/
├── README.md                      # Ponto de entrada
├── INDICE.md                      # Este guia
│
├── docs/                          # Central de Documentação
│   ├── arquitetura/               # Tech Stack e Design
│   │   └── diagramas/             # Arquivos PlantUML e PNGs
│   ├── requisitos/                # RN, RF e RNF
│   └── testes/                    # Logs e métricas de QA
│
├── backend/                       # API FastAPI
└── frontend/                      # App Frontend
```

---
**Status:** ✅ Documentação Reorganizada e Limpa para Entrega Final
