# STATE — Memoria Persistente do Projeto

## Decisoes

| Data       | Decisao                                                         | Contexto                                      |
|------------|-----------------------------------------------------------------|-----------------------------------------------|
| 2026-04-10 | Projeto inicializado com estrutura .specs/                      | Setup inicial da documentacao base             |
| 2026-04-10 | Backend Django, Frontend React, PostgreSQL                      | Definido no PRD (secao 6.1)                    |
| 2026-04-10 | Frontend hospedado no Cloudflare Pages                          | Definido no PRD (secao 6.1)                    |
| 2026-04-10 | Pipeline ML integrado ao backend (mesmo projeto, modulo separado)| PRD prioriza simplicidade arquitetural         |
| 2026-04-10 | Desenvolvimento incremental em 4 fases                          | Roadmap derivado do PRD (secao 20)             |

## Blockers

_Nenhum blocker ativo._

## Lessons

_Nenhuma licao registrada ainda._

## Todos

- [ ] Resolver estrategia de autenticacao (JWT vs session vs OAuth)
- [ ] Definir se v1 tera reexecucao manual do pipeline
- [ ] Definir politica de atualizacao de dados (sobrescrita vs versionamento vs incremental)
- [ ] Definir conjunto minimo de filtros para consulta

## Deferred Ideas

- Extracao futura do pipeline para servico separado (se complexidade crescer)
- Area publica para visitantes nao autenticados (decisao futura)
- Fluxo de aprovacao manual antes da publicacao de resultados

## Preferences

_Nenhuma preferencia registrada ainda._
