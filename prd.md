# PRD — Plataforma Web de Monitoramento e Curadoria de Resultados com Pipeline de Dados/ML

## 1. Visão geral do produto

Este documento define os requisitos do produto para uma plataforma web voltada à consulta, administração e atualização periódica de resultados gerados por um pipeline de dados e aprendizado de máquina. O sistema terá uma interface web consumindo uma aplicação backend responsável tanto pela camada de negócio quanto pela administração das configurações que controlam o pipeline periódico de atualização.

O produto não é orientado a grande escala de usuários, mas sim a um grupo restrito de usuários autenticados, incluindo perfis administrativos com permissão para ajustar parâmetros do fluxo de coleta e processamento. O foco principal está na confiabilidade do processo, na rastreabilidade das atualizações e na boa experiência de consulta dos resultados finais.

Neste estágio inicial, o PRD prioriza requisitos funcionais, responsabilidades dos módulos e fluxos principais do sistema, evitando detalhar excessivamente escolhas de implementação. A intenção é permitir que o desenvolvimento evolua de forma incremental, com refinamento técnico progressivo ao longo da construção.

## 2. Contexto e problema

Atualmente, o fluxo de obtenção dos dados envolve múltiplas etapas: busca em repositórios, intersecção entre resultados, aplicação de modelos de machine learning, processamento posterior e persistência em banco de dados. Embora esse fluxo produza dados valiosos, ele exige uma forma organizada de:

- disponibilizar os resultados em uma aplicação web;
- controlar quem pode acessar e administrar o sistema;
- permitir ajustes nos parâmetros do pipeline sem depender de alterações manuais no código;
- atualizar periodicamente os dados por meio de execução agendada;
- manter histórico e controle sobre quais resultados são exibidos ao usuário final.

Sem uma plataforma estruturada, o processo tende a ficar excessivamente manual, pouco auditável e dependente de intervenções técnicas para ajustes operacionais simples.

## 3. Objetivo do produto

Construir uma plataforma web que permita:

1. autenticação e autorização de usuários;
2. consulta de resultados processados pelo pipeline;
3. administração de parâmetros que influenciam a coleta e o processamento dos dados;
4. atualização periódica e rastreável do conjunto de dados por meio de um cron job mensal;
5. controle administrativo sobre a visibilidade e manutenção dos resultados apresentados na aplicação.

## 4. Objetivos de negócio

- Reduzir o esforço manual para atualização dos dados da plataforma.
- Centralizar em um único sistema a administração do pipeline e a consulta dos resultados.
- Garantir que usuários administrativos consigam ajustar parâmetros operacionais sem intervenção direta no código.
- Oferecer uma base confiável para visualização e uso contínuo dos dados produzidos.

## 5. Objetivos do usuário

### 5.1 Usuário comum

- Entrar no sistema com segurança.
- Visualizar resultados atualizados.
- Filtrar, pesquisar e consultar os dados disponíveis.

### 5.2 Usuário administrador

- Gerenciar usuários e permissões.
- Ajustar parâmetros do pipeline, como termos de busca e regras operacionais.
- Ocultar, remover ou revisar resultados exibidos.
- Acompanhar o status das execuções periódicas.

## 6. Escopo do produto

## 6.1 Em escopo

- Frontend React hospedado no Cloudflare Pages.
- Backend Django exposto como API para consumo do frontend.
- PostgreSQL como banco principal.
- Autenticação de usuários.
- Controle de autorização por perfis e permissões.
- Painel administrativo para configuração do pipeline.
- Persistência de resultados processados.
- Execução mensal do pipeline de dados/ML.
- Registro de execuções do pipeline.
- Consulta e filtragem dos resultados no frontend.
- Controle administrativo de visibilidade dos resultados.

## 6.2 Fora de escopo nesta fase

- Arquitetura distribuída em múltiplos microserviços.
- Escalabilidade para grandes volumes de usuários.
- Processamento em tempo real.
- Edição colaborativa simultânea complexa.
- Aplicativo mobile nativo.

## 7. Perfis de usuário

### 7.1 Visitante não autenticado

Não terá acesso ao sistema, salvo decisão futura de liberar alguma área pública.

### 7.2 Usuário autenticado padrão

Pode acessar a plataforma, visualizar e consultar os dados disponibilizados conforme sua permissão.

### 7.3 Usuário administrador

Possui acesso ampliado ao sistema para gerenciar parâmetros, usuários, execuções do pipeline e visibilidade dos resultados.

## 8. Proposta de solução

A solução será composta por uma interface web e uma aplicação backend unificada.

O backend concentrará:

- autenticação e autorização;
- regras de negócio da aplicação;
- API consumida pelo frontend;
- administração de usuários, permissões e parâmetros operacionais;
- armazenamento e leitura dos resultados processados;
- lógica de configuração do pipeline;
- execução do fluxo agendado de atualização.

Embora seja um sistema unificado, o projeto deverá ser organizado em módulos distintos, separando claramente a camada de aplicação da camada de pipeline de dados, de forma a permitir futura extração caso isso se torne necessário.

As escolhas específicas de framework, bibliotecas auxiliares, estratégia de autenticação, orquestração de jobs e organização detalhada de infraestrutura poderão ser refinadas durante o desenvolvimento, desde que respeitem os requisitos e responsabilidades definidos neste documento.

## 9. Fluxo de alto nível

1. Usuários acessam o frontend React.
2. O frontend consome a API do backend Django.
3. O backend autentica o usuário e aplica regras de autorização.
4. O usuário consulta resultados previamente persistidos no PostgreSQL.
5. Usuários administradores ajustam parâmetros do pipeline por meio do painel administrativo.
6. Em uma frequência mensal, um cron job executa o pipeline.
7. O pipeline busca novos dados, processa os resultados e atualiza o banco.
8. O frontend passa a consumir a nova versão dos dados processados.

## 10. Requisitos funcionais

### RF-01 — Autenticação

O sistema deve permitir autenticação segura de usuários.

### RF-02 — Autorização

O sistema deve distinguir permissões entre usuários padrão e administradores.

### RF-03 — Gestão de usuários

Administradores devem conseguir gerenciar usuários e seus papéis.

### RF-04 — Consulta de resultados

Usuários autenticados devem conseguir visualizar os resultados armazenados no banco.

### RF-05 — Busca e filtros

A aplicação deve oferecer mecanismos de busca e filtragem sobre os resultados.

### RF-06 — Visualização controlada

Administradores devem conseguir ocultar, remover ou marcar resultados para não exibição.

### RF-07 — Configuração do pipeline

Administradores devem conseguir editar parâmetros operacionais do fluxo periódico de atualização de dados, respeitando o nível de configuração definido para a fase inicial do produto.

### RF-08 — Execução agendada

O sistema deve executar mensalmente o pipeline de atualização dos dados.

### RF-09 — Registro de execuções

Cada execução do fluxo periódico de atualização deve gerar um registro com data, status, duração e observações de erro ou sucesso.

### RF-10 — Persistência dos resultados

Os resultados processados pelo pipeline devem ser persistidos no PostgreSQL e disponibilizados para consulta.

### RF-11 — Separação lógica interna

O sistema deve manter separação lógica entre módulos de autenticação, administração, consulta e pipeline.

### RF-12 — Histórico mínimo operacional

O sistema deve manter histórico mínimo das configurações aplicadas e das execuções realizadas, para fins de rastreabilidade operacional.

## 11. Requisitos não funcionais

### RNF-01 — Simplicidade arquitetural

A arquitetura deve priorizar simplicidade de manutenção, evitando complexidade desnecessária para o volume estimado de usuários.

### RNF-02 — Segurança

O sistema deve proteger autenticação, sessões, permissões e acesso aos endpoints administrativos.

### RNF-03 — Confiabilidade do pipeline

A execução mensal deve ocorrer de forma previsível, com registro de falhas e possibilidade de reprocessamento manual.

### RNF-04 — Manutenibilidade

O código deve ser organizado por módulos claros, facilitando evolução futura.

### RNF-05 — Desempenho adequado

A aplicação deve responder adequadamente para uma base esperada de até aproximadamente 500 usuários.

### RNF-06 — Observabilidade básica

O sistema deve ter logs e registros suficientes para diagnóstico de falhas em autenticação, API e pipeline.

## 12. Módulos do sistema

### 12.1 Módulo de autenticação e autorização

Responsável por login, sessões ou tokens, perfis de usuário e controle de acesso.

### 12.2 Módulo de administração

Responsável por gerenciamento de usuários, permissões, parâmetros de busca, regras operacionais e manutenção dos resultados.

### 12.3 Módulo de consulta

Responsável por servir ao frontend os resultados já processados e persistidos.

### 12.4 Módulo de pipeline

Responsável por executar o fluxo de atualização dos dados utilizados pela aplicação. Neste estágio do PRD, esse módulo deve ser entendido de forma genérica como a camada encarregada de coletar, processar, transformar e disponibilizar dados persistidos para consumo posterior pela aplicação.

Os detalhes de implementação desse fluxo, incluindo etapas específicas, algoritmos utilizados, integrações externas, estratégias de processamento, critérios de validação e forma de orquestração, deverão ser discutidos e definidos mais detalhadamente durante a etapa de implementação.

## 12.5 Módulo de agendamento e execução

Responsável por disparar e registrar o cron job mensal e eventuais execuções manuais administrativas.

## 13. Entidades principais

As entidades abaixo representam uma visão inicial do domínio e poderão ser refinadas na etapa de modelagem.

- Usuário
- Papel ou perfil
- Permissão
- Configuração de pipeline
- Execução de pipeline
- Resultado processado
- Status de visibilidade do resultado
- Log operacional

## 14. Fluxo do pipeline de dados

O pipeline de dados deverá ser tratado, nesta fase, como um fluxo periódico e modular de atualização das informações consumidas pela aplicação.

De forma geral, espera-se que esse fluxo contemple atividades de obtenção, preparação, processamento e persistência de dados. No entanto, a decomposição detalhada dessas etapas, bem como suas regras específicas de execução, será definida posteriormente durante a implementação.

O ponto principal, para fins deste PRD, é que o sistema disponha de um mecanismo controlado e rastreável para atualizar os dados da aplicação em periodicidade definida, garantindo que os resultados apresentados ao usuário sejam derivados da última execução válida desse fluxo.

## 15. Requisitos administrativos específicos

- O administrador deve conseguir ajustar parâmetros configuráveis do fluxo periódico de atualização, conforme o escopo definido para cada fase do projeto.
- O administrador deve conseguir revisar resultados antes ou depois da publicação, conforme a regra adotada.
- O administrador deve conseguir remover ou ocultar itens da interface.
- O administrador deve visualizar histórico de execuções do fluxo periódico.
- O administrador deve conseguir disparar execução manual, caso essa função seja habilitada na primeira versão.

## 16. Premissas

- O sistema terá uma interface web para usuários autenticados.
- Haverá uma aplicação backend responsável pela lógica de negócio e exposição de dados.
- O pipeline de dados/ML permanecerá no ecossistema Python.
- Os dados processados serão persistidos em banco relacional.
- A atualização dos dados ocorrerá, em princípio, mensalmente.
- O volume de usuários é reduzido, priorizando simplicidade sobre arquitetura distribuída.
- O sistema deverá ser construído de forma incremental, permitindo que detalhes de implementação sejam definidos e refinados ao longo do desenvolvimento.

## 17. Restrições

- O projeto deve evitar complexidade operacional excessiva.
- O sistema deve ser compreensível e administrável por uma equipe pequena.
- O pipeline pode exigir processamento mais pesado do que a camada web, mas isso será tratado de forma isolada dentro do mesmo projeto em uma primeira fase.

## 18. Riscos

- Acoplamento excessivo entre camada web e pipeline se a organização modular não for respeitada.
- Falhas silenciosas no cron job caso não haja monitoramento mínimo.
- Crescimento futuro da complexidade do pipeline exigir extração para um serviço separado.
- Configurações administrativas mal geridas afetarem a qualidade dos resultados.

## 19. Critérios de sucesso

O produto será considerado bem-sucedido quando:

- usuários autenticados conseguirem consultar os resultados com estabilidade;
- administradores conseguirem ajustar parâmetros sem alteração direta no código;
- o pipeline mensal atualizar corretamente o banco;
- o sistema mantiver rastreabilidade mínima das execuções;
- a solução puder ser mantida sem complexidade desproporcional ao porte da aplicação.

## 20. Roadmap inicial sugerido

### Fase 1 — Estrutura base

- Definição da estrutura inicial do projeto
- Modelagem inicial do domínio
- Implementação da base de autenticação e autorização
- Estruturação dos módulos principais do sistema

### Fase 2 — Consulta e administração

- Endpoints ou serviços de leitura dos resultados
- Gestão de usuários e permissões
- Configuração administrativa do pipeline
- Controle de visibilidade dos resultados

### Fase 3 — Integração do pipeline

- Integração do fluxo de dados/ML ao projeto
- Persistência estruturada no banco
- Registro de execuções
- Agendamento periódico

### Fase 4 — Refinamento operacional

- Logs e observabilidade básica
- Melhorias na experiência administrativa
- Ajustes de performance
- Refinamento técnico das decisões de implementação

## 21. Questões em aberto

- Qual framework backend será adotado na implementação final?
- Qual estratégia de autenticação será usada na primeira versão?
- A primeira versão permitirá reexecução manual do pipeline pelo admin?
- Haverá fluxo de aprovação manual antes da publicação de novos resultados?
- Qual será o conjunto mínimo de filtros na interface de consulta?
- Qual será a política de atualização: sobrescrita completa, versionamento ou atualização incremental?
- Quais componentes devem ser tratados inicialmente apenas como interfaces genéricas, para posterior especialização?

## 22. Diretriz de implementação incremental

Durante o desenvolvimento inicial, os componentes do sistema devem ser tratados de forma relativamente genérica, com foco em responsabilidades, contratos de entrada e saída e fluxo entre módulos, evitando detalhamento excessivo prematuro.

Isso significa que, na fase inicial, é aceitável trabalhar com:

- modelos simplificados de domínio;
- interfaces administrativas com escopo reduzido;
- versões iniciais do pipeline com pontos de extensão claros;
- contratos de API estáveis, mesmo que a lógica interna ainda evolua;
- parametrizações genéricas que possam ser refinadas futuramente.

No caso específico do pipeline, o PRD estabelece apenas seu papel no produto, sua relação com os dados exibidos na aplicação e a necessidade de execução rastreável e periódica. O detalhamento técnico dessa implementação deverá ser conduzido em etapa própria, com definição progressiva de componentes, regras e estratégias operacionais.

A especialização de cada componente deverá ocorrer progressivamente, à medida que o projeto amadurecer e que novas decisões de produto e implementação forem consolidadas.

## 23. Princípios para desenvolvimento com agentes

- Priorizar componentes pequenos, modulares e de responsabilidade clara.
- Definir contratos simples entre módulos antes de aprofundar a implementação.
- Evitar acoplamento prematuro a detalhes específicos de infraestrutura.
- Favorecer entregas incrementais e facilmente revisáveis.
- Registrar decisões técnicas à medida que forem sendo fechadas, sem antecipar complexidade desnecessária.
- Construir a primeira versão com foco em clareza estrutural, e não em sofisticação máxima.
