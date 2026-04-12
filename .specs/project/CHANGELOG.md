# Changelog

Registro cronológico das mudanças do projeto, agrupado por data.
Datas mais recentes aparecem no topo.

Categorias usadas: **Added** (novo), **Changed** (mudança em algo existente), **Fixed** (correção), **Removed** (removido), **Docs** (documentação), **Chore** (infraestrutura/tooling).

---

## 2026-04-12

### Docs
- Convenção de type hints obrigatórios adicionada ao `CLAUDE.md` (assinaturas, generics nativos, `from __future__ import annotations`)
- Estrutura `.specs/features/` criada com template (`_TEMPLATE.md`) para specs de features
- Spec da F-02 preenchido como referência (`F-02.md` — Custom User + Email Verification)
- Convenção de feature specs registrada no `CLAUDE.md` (spec obrigatório antes de implementar)

## 2026-04-11

### Added
- App `apps.accounts` com modelo `User` customizado (login por email, `USERNAME_FIELD = "email"`, username mantido como campo de display)
- `UserManager` customizado com `create_user` e `create_superuser` baseados em email
- Modelo `EmailVerification` (código de 6 dígitos, expiração de 15 minutos, método `mark_used` para uso único)
- Registro mínimo de `User` e `EmailVerification` no Django Admin
- Migrations iniciais do app `accounts` (`0001_initial`)
- 16 testes TDD cobrindo `User` e `EmailVerification`
- Documentação CHANGELOG em `.specs/project/CHANGELOG.md`

### Changed
- `AUTH_USER_MODEL` definido como `accounts.User` em `config/settings/base.py`
- `apps.accounts` adicionado a `LOCAL_APPS`
- Banco de dev recriado do zero para aplicar o novo `AUTH_USER_MODEL`
- Decisões de F-02 registradas em `STATE.md` (session cookies, login por email, Resend, grupos nativos, self-registration aberta)
- F-02 movido para `Done` no `ROADMAP.md`

### Chore
- Pre-commit hook instalado automaticamente pelo `make setup`
- Logging de console adicionado ao ambiente dev; novo target `make stop`
- `**/migrations/**` excluído do ruff (arquivos auto-gerados pelo Django)

### Docs
- Provedor do banco de dados atualizado de Render para Neon
- Formato do CHANGELOG reescrito no estilo Keep a Changelog (agrupamento por data, sem hashes de commit)

## 2026-04-10

### Added
- Projeto Django inicializado com `uv` e dependências base
- Settings do Django divididos em `base.py`, `dev.py` e `prod.py`
- Diretório `apps/` criado com o app `core` (estrutura flat com namespace `apps.*`)
- Docker Compose para PostgreSQL local, arquivo `.env` e `.gitignore`
- Endpoint de health check (`/api/health/`) implementado via TDD
- Endpoint de system status (`/api/status/`) com verificação de componentes
- Makefile com comandos comuns de desenvolvimento (`setup`, `dev`, `test`, `lint`, `format`, `migrate`)
- Script `build.sh` para deploy no Render
- README do projeto

### Chore
- `pyproject.toml` configurado com ruff e pytest-django
- Pre-commit configurado com ruff e hooks padrão

### Docs
- PRD inicial e estrutura `.specs/` criados
- TDD registrado como princípio obrigatório do projeto
- Convenções em `CLAUDE.md`
- Documentação do projeto atualizada após conclusão do F-01
