# PROJECT — Plataforma de Monitoramento e Curadoria com Pipeline de Dados/ML

## Visao

Plataforma web para consulta, administracao e atualizacao periodica de resultados gerados por um pipeline de dados e aprendizado de maquina. O sistema atende um grupo restrito de usuarios autenticados, com perfis administrativos que ajustam parametros do pipeline sem intervencao no codigo.

## Problema

O fluxo atual de obtencao de dados envolve multiplas etapas manuais (busca em repositorios, interseccao, modelos ML, pos-processamento). Sem uma plataforma estruturada, o processo e manual, pouco auditavel e dependente de intervencoes tecnicas para ajustes operacionais simples.

## Objetivos

1. **Autenticacao e autorizacao** — controle de acesso seguro com perfis (padrao e admin)
2. **Consulta de resultados** — interface web para visualizacao, busca e filtragem dos dados processados
3. **Administracao do pipeline** — painel para ajustar parametros operacionais do fluxo de atualizacao
4. **Atualizacao periodica** — cron job mensal rastreavel para atualizar o banco de dados
5. **Controle de visibilidade** — admins podem ocultar, remover ou revisar resultados

## Objetivos de Negocio

- Reduzir esforco manual para atualizacao dos dados
- Centralizar administracao do pipeline e consulta de resultados em um unico sistema
- Permitir ajustes operacionais sem intervencao direta no codigo
- Oferecer base confiavel para visualizacao e uso continuo dos dados

## Stack

| Camada     | Tecnologia          | Hospedagem        |
|------------|---------------------|-------------------|
| Frontend   | React               | Cloudflare Pages  |
| Backend    | Django (API)        | Render            |
| Banco      | PostgreSQL 16       | Render PostgreSQL |
| Pipeline   | Python (ML/Dados)   | Mesmo backend     |

## Restricoes

- Evitar complexidade operacional excessiva
- Sistema administravel por equipe pequena
- Pipeline pode exigir processamento pesado, mas sera isolado logicamente dentro do mesmo projeto na fase inicial
- Volume reduzido de usuarios (~500 max), priorizando simplicidade sobre arquitetura distribuida

## Principios

- **TDD obrigatorio** — toda funcionalidade nova deve ter testes escritos antes da implementacao. Testes definem o comportamento esperado e guiam o desenvolvimento
- Componentes pequenos, modulares e de responsabilidade clara
- Contratos simples entre modulos antes de aprofundar implementacao
- Evitar acoplamento prematuro a detalhes de infraestrutura
- Entregas incrementais e revisaveis
- Registrar decisoes tecnicas progressivamente
- Primeira versao com foco em clareza estrutural, nao sofisticacao maxima

## Riscos

- Acoplamento excessivo entre camada web e pipeline se a organizacao modular nao for respeitada
- Falhas silenciosas no cron job sem monitoramento minimo
- Crescimento do pipeline exigir extracao para servico separado
- Configuracoes admin mal geridas afetarem qualidade dos resultados

## Criterios de Sucesso

- Usuarios autenticados consultam resultados com estabilidade
- Admins ajustam parametros sem alterar codigo
- Pipeline mensal atualiza banco corretamente
- Rastreabilidade minima das execucoes mantida
- Solucao mantida sem complexidade desproporcional ao porte
