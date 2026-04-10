# STATE — Memoria Persistente do Projeto

## Decisoes

| Data       | Decisao                                                         | Contexto                                      |
|------------|-----------------------------------------------------------------|-----------------------------------------------|
| 2026-04-10 | Projeto inicializado com estrutura .specs/                      | Setup inicial da documentacao base             |
| 2026-04-10 | Backend Django, Frontend React, PostgreSQL                      | Definido no PRD (secao 6.1)                    |
| 2026-04-10 | Frontend hospedado no Cloudflare Pages                          | Definido no PRD (secao 6.1)                    |
| 2026-04-10 | Pipeline ML integrado ao backend (mesmo projeto, modulo separado)| PRD prioriza simplicidade arquitetural         |
| 2026-04-10 | Desenvolvimento incremental em 4 fases                          | Roadmap derivado do PRD (secao 20)             |
| 2026-04-10 | TDD obrigatorio — testes antes da implementacao                 | Decisao do usuario, principio fundamental      |
| 2026-04-10 | Python 3.12, uv como gerenciador de deps                        | Setup F-01, versao estavel com boa compat.     |
| 2026-04-10 | Apps Django em apps/ com prefixo apps.*                         | Setup F-01, organizacao flat com namespace      |
| 2026-04-10 | Settings split: base.py, dev.py, prod.py                        | Setup F-01, separacao por ambiente              |
| 2026-04-10 | DRF como framework de API REST                                  | Setup F-01, padrao da comunidade Django         |
| 2026-04-10 | ruff + pytest-django + pre-commit como tooling                  | Setup F-01, qualidade de codigo                 |
| 2026-04-10 | Deploy no Render (gunicorn + whitenoise)                        | Simplicidade e custo acessivel                  |

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
