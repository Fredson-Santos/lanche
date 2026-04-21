# ESPECIFICAÇÃO DE REQUISITOS - LANCHE
## Projeto: LANCHE MVP - Sistema de Gestão para Varejo Alimentício
**Disciplina:** Engenharia de Software  
**Data:** 21 de Abril de 2026  
**Versão:** 4.0 (Padrão Acadêmico - Atividade Integradora)

---

## 1. Introdução

Este documento apresenta a especificação de requisitos para o sistema **LANCHE**, uma solução modular desenvolvida para resolver gargalos operacionais em redes de varejo alimentício. O sistema foca na automatização de processos críticos como controle de perecíveis, ultra-latência no PDV, sincronização multi-loja e conformidade legal (LGPD).

---

## 2. Atores do Sistema

Identificação dos perfis que interagem com o sistema:

| Ator | Descrição |
|:---|:---|
| **Administrador** | Responsável pela gestão centralizada: usuários, auditoria, segurança e relatórios globais. |
| **Gerente de Loja** | Responsável pela operação local: gestão de estoques, reposição e monitoramento de alertas. |
| **Caixa (Operador PDV)** | Responsável pela interface direta com o cliente: vendas, consultas e emissão de cupons. |
| **Sistema Externo** | Aplicativos de delivery e logística de terceiros que consomem os dados via API aberta. |

---

## 3. Requisitos Funcionais (RF)

Os requisitos funcionais descrevem as ações que o sistema deve ser capaz de realizar para atender às necessidades do cenário LANCHE.

| ID | Nome | Descrição | Prioridade | Status |
|:---|:---|:---|:---:|:---:|
| **RF-01** | Controle de Validade | Monitorar automaticamente a data de vencimento de todos os itens em estoque. | Crítica | ✅ |
| **RF-02** | Monitoramento de Temperatura | Monitorar em tempo real a temperatura dos itens perecíveis em estoque. | Crítica | ✅ |
| **RF-03** | Emissão de Alertas | Disparar alertas imediatos (validade e temperatura) para evitar perdas e riscos. | Crítica | ✅ |
| **RF-04** | Processamento de Vendas (PDV) | Interface para registro de produtos, cálculo de totais e finalização de venda. | Crítica | ✅ |
| **RF-05** | Emissão de Cupons | Gerar cupom fiscal (ou simulação) em poucos segundos após o pagamento. | Alta | ✅ |
| **RF-06** | Reposição Automática | Gerar ordens de reposição quando o estoque atinge o nível mínimo de segurança. | Alta | ✅ |
| **RF-07** | Painel de Relatórios | Consolidar vendas e fluxo de caixa de todas as filiais em um painel gerencial único. | Alta | ✅ |
| **RF-08** | Auditoria e Logs | Manter registro detalhado e imutável de todas as transações para fins de auditoria. | Alta | ✅ |
| **RF-09** | Modo de Contingência Offline | Permitir processamento de vendas mesmo em caso de queda de conexão. | Média | 📋 |
| **RF-10** | Sincronização Pós-Offline | Sincronizar dados automaticamente assim que a conexão for restabelecida. | Média | 📋 |
| **RF-11** | Gestão de Dados (LGPD) | Funcionalidades de deleção segura e exportação de dados de clientes (portabilidade). | Crítica | 🚀 |
| **RF-12** | Integração via API Aberta | Disponibilizar APIs modulares para integração com apps de logística e delivery. | Alta | ✅ |

---

## 4. Requisitos Não Funcionais (RNF)

Os requisitos não funcionais definem os critérios de qualidade e restrições do sistema.

| ID | Categoria | Descrição | Prioridade | Status |
|:---|:---|:---|:---:|:---:|
| **RNF-01** | Performance | A interface de PDV deve operar com latência ultra-baixa (transação < 1s). | Alta | ✅ |
| **RNF-02** | Segurança | A base de dados deve ser criptografada para proteger informações sensíveis. | Crítica | ✅ |
| **RNF-03** | Confiabilidade | O sistema deve possuir alta disponibilidade e suporte a falhas de rede. | Alta | 🚀 |
| **RNF-04** | Escalabilidade | A arquitetura deve ser modular para suportar a expansão da marca. | Alta | ✅ |
| **RNF-05** | Conformidade | O software deve atender rigorosamente à Lei Geral de Proteção de Dados (LGPD). | Crítica | 🚀 |

---

## 5. Regras de Negócio (RN)

As regras de negócio determinam o comportamento operacional e as restrições lógicas do sistema.

| ID | Nome | Descrição |
|:---|:---|:---|
| **RN-01** | Alerta de Temperatura | Se a temperatura de um item perecível sair da faixa ideal, um alerta crítico deve ser gerado no dashboard. |
| **RN-02** | Bloqueio de Vencimento | Produtos com validade expirada devem ser marcados automaticamente como indisponíveis para venda. |
| **RN-03** | Gatilho de Reposição | A ordem de reposição deve ser gerada no momento exato em que `quantidade_estoque <= estoque_minimo`. |
| **RN-04** | Privilégio de Operação | Somente usuários com role 'admin' ou 'gerente' podem autorizar estornos. |
| **RN-05** | Precedência Sincronização | Em caso de conflito na sincronização offline, os dados do servidor têm precedência (server-wins). |
| **RN-06** | Criptografia PII | Dados PII (email, nome, documentos) devem ser criptografados antes de serem persistidos no banco de dados. |

---

## 6. Documentação Complementar

- **MER/DER:** Consulte [05_DIAGRAMA_MER_MVP.puml](file:///c:/Users/Fred/Projetos/lanche/docs/arquitetura/diagramas/05_DIAGRAMA_MER_MVP.puml)
- **Arquitetura da Solução:** Consulte [ARQUITETURA.md](file:///c:/Users/Fred/Projetos/lanche/docs/arquitetura/ARQUITETURA.md)
- **Cenário de Referência:** [Cenario.md](file:///c:/Users/Fred/Projetos/lanche/docs/atividades/Atividade-a-Realizar/Cenario.md)

---

## 7. Roadmap Futuro (Pós-MVP)

Os requisitos abaixo foram identificados no cenário original, mas removidos do escopo inicial para implementação em fases futuras:

| ID | Nome | Descrição | Prioridade |
|:---|:---|:---|:---:|
| **RF-EXT-01** | Sincronização Bidirecional | Sincronizar inventário entre unidades e centro de distribuição em tempo real. | Alta |
| **RF-EXT-02** | Autenticação Multifator (MFA) | Exigir autenticação extra ou biométrica para estorno e abertura de gaveta. | Crítica |

---
**Documento Revisado para Atividade Integradora**  
✅ **Status:** Pronto para Submissão
