# 📑 Índice de Documentação - LANCHE MVP

Guia centralizado para navegação e referência rápida de toda a documentação do projeto.

---

## 🎯 Comece Por Aqui

1. **Quer entender a arquitetura?** → [docs/arquitetura/ARQUITETURA.md](docs/arquitetura/ARQUITETURA.md)
2. **Qual é o plano?** → [ROADMAP.md](ROADMAP.md)
3. **Visão Geral** → [README.md](README.md)

---

## 📚 Documentação por Categoria

### 🏗️ Arquitetura & Design
| Documento | Descrição |
|-----------|-----------|
| [ARQUITETURA.md](docs/arquitetura/ARQUITETURA.md) | Arquitetura three-tier, fluxos, modelagem |
| [ENCRYPTION_SETUP.md](docs/arquitetura/ENCRYPTION_SETUP.md) | Guia de configuração de criptografia de banco |
| [Diagrama de Classes](docs/arquitetura/diagramas/01_DIAGRAMA_CLASSES_MVP.puml) | Modelagem de classes UML |
| [Casos de Uso](docs/arquitetura/diagramas/02_DIAGRAMA_CASOS_USO_MVP.puml) | Diagrama de casos de uso |

### 📋 Requisitos & Negócio
| Documento | Descrição |
|-----------|-----------|
| [REQUISITOS_MVP.md](docs/requisitos/REQUISITOS_MVP.md) | Especificação técnica, RF, RNF e RN (Unificado) |
| [Cenário de Negócio](docs/atividades/Atividade-a-Realizar/Cenario.md) | Contexto e regras de negócio |

### 🚀 Planejamento & Roadmaps
| Documento | Descrição |
|-----------|-----------|
| [ROADMAP.md](ROADMAP.md) | Timeline principal do projeto |
| [ROADMAP_SPRINT_FINAL.md](docs/planejamento/ROADMAP_SPRINT_FINAL.md) | Planejamento da fase final de entrega |
| [Plano Frontend](docs/planejamento/Frontend_Plano_Implementacao.md) | Plano de implementação da UI React |

### ✅ Tarefas & Conclusões
| Documento | Descrição |
|-----------|-----------|
| [TASK_1A_APIS](docs/tasks/TASK_1A_APIS_COMPLETA.md) | API Keys e Rate Limiting |
| [TASK_1B_REPOSICAO](docs/tasks/TASK_1B_REPOSICAO_COMPLETA.md) | Reposição Automática de Estoque |
| [TASK_1C_ALERTAS](docs/tasks/TASK_1C_ALERTAS_COMPLETA.md) | Monitoramento de Validade e Alertas |
| [TASK_2A_CRIPTOGRAFIA](docs/tasks/TASK_2A_CRIPTOGRAFIA_COMPLETA.md) | Criptografia de Dados PII |
| [TASK_2B_LGPD](docs/tasks/TASK_2B_LGPD_COMPLETA.md) | Conformidade LGPD Lite |
| [FASE1_CONCLUSAO.md](docs/conclusao/FASE1_CONCLUSAO.md) | Registro de conclusão da Fase 1 |
| [CERTIFICATE.md](docs/conclusao/COMPLETION_CERTIFICATE.md) | Certificado de conclusão do MVP |

### 🧪 Testes & Qualidade
| Documento | Descrição |
|-----------|-----------|
| [TESTES_VALIDACAO.md](docs/testes/TESTES_VALIDACAO_FINAL.md) | Plano de testes e resultados finais |
| [TEST_RESULTS_SUMMARY.md](docs/testes/TEST_RESULTS_SUMMARY.md) | Sumário executivo de testes |
| [FINAL_TEST_OUTPUT.txt](docs/testes/FINAL_TEST_OUTPUT.txt) | Log detalhado da execução de testes |

---

## 📊 Estrutura de Pastas (Organizada)

```
lanche/
├── README.md                      # Ponto de entrada
├── ROADMAP.md                     # Timeline principal
├── INDICE.md                      # Este guia
│
├── docs/                          # Central de Documentação
│   ├── arquitetura/               # Tech Stack e Design
│   │   └── diagramas/             # Arquivos PlantUML
│   ├── requisitos/                # RN, RF e RNF
│   ├── planejamento/              # Roadmaps e planos de ação
│   ├── tasks/                     # Histórico de entregas (TASK_*)
│   ├── testes/                    # Logs e métricas de QA
│   ├── conclusao/                 # Certificados e marcos
│   └── atividades/                # Atividades acadêmicas/integradora
│
├── backend/                       # API FastAPI
└── frontend/                      # React Native / Vite
```

---
**Última atualização:** 21 de Abril de 2026  
**Status:** ✅ Documentação Reorganizada
