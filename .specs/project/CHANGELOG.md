# Changelog

Registro cronológico das mudanças do projeto, organizado por commit.
Commits mais recentes aparecem no topo.

Formato: `hash curto — tipo: descrição`

---

## 2026-04-11

- `760602e` — **feat(accounts):** F-02 concluído — app `apps.accounts` com `User` customizado (login por email), `EmailVerification` (código de 6 dígitos, 15 min) e admin mínimo; `AUTH_USER_MODEL=accounts.User`; banco dev recriado; 16 testes TDD; migrations excluídas do lint.
- `c85a2fd` — **docs:** adicionado `CHANGELOG.md` em `.specs/project/` para registrar histórico de commits.
- `d2a699d` — **chore:** instalação do pre-commit hook integrada ao `make setup`.
- `b6de187` — **chore:** adicionado logging de console em dev e novo target `make stop`.

## 2026-04-10

- `dd86915` — **docs:** provedor do banco de dados atualizado de Render para Neon.
- `c4ace0c` — **docs:** adicionado README e removido arquivo mermaid standalone.
- `a4db603` — **feat:** endpoint de system status com health checks de componentes.
- `db76557` — **docs:** documentação do projeto atualizada após conclusão do F-01.
- `9eb37db` — **chore:** Makefile com comandos comuns de desenvolvimento.
- `fcf4010` — **chore:** correções de lint e formatação do ruff.
- `887ff39` — **chore:** script de build do Render e convenções em `CLAUDE.md`.
- `d42634c` — **feat:** endpoint de health check implementado via TDD.
- `6f4dc93` — **chore:** configuração do pre-commit com ruff e hooks padrão.
- `2495c52` — **chore:** configuração de ruff e pytest-django no `pyproject.toml`.
- `8755760` — **feat:** Docker Compose para PostgreSQL, `.env` e `.gitignore`.
- `449a5ec` — **feat:** estrutura inicial do diretório `apps/` com app `core`.
- `00f25f2` — **refactor:** settings do Django divididos em `base`, `dev` e `prod`.
- `fbdd26f` — **feat:** projeto Django inicializado com uv e dependências base.
- `ce88046` — **docs:** TDD registrado como princípio obrigatório do projeto.
- `20eab94` — **docs:** projeto iniciado com PRD e documentação em `.specs/`.
