# Fatias verticais (tracer bullets)

Cada fatia atravessa **todas as camadas** (entidade → caso de uso → porta →
adapter em memória e SQLite → rota Flask → template) e é feita com TDD:
primeiro um commit `test:` (vermelho) e depois um commit `feat:` (verde).

| # | Fatia | História | Seams testadas |
|---|---|---|---|
| 0 | `Periodo`: intervalo de tempo, sobreposição, contenção e subtração | base | domínio |
| 1 | Cadastro e login | US1 | domínio, caso de uso, contrato de repositório, rota |
| 2 | Barbearia, cadeiras e horários ociosos | US2 | domínio, caso de uso, contrato de repositório, rota |
| 3 | Serviços do barbeiro | US3 | domínio, caso de uso, contrato de repositório, rota |
| 4 | Busca por bairro e reserva de bloco | US4 | domínio, caso de uso, contrato de repositório, rota |
| 5 | Agenda do barbeiro e agendamento do cliente | US5 | domínio, caso de uso, contrato de repositório, rota |

## Seams combinadas

| Seam | O que pega | O que não pega |
|---|---|---|
| Entidades de domínio (`tests/domain`) | invariantes e regras de sobreposição | orquestração e persistência |
| Casos de uso + adapters em memória (`tests/use_cases`) | regras de negócio e permissões por persona | SQL e HTTP |
| Contrato de repositório (`tests/infra`) | mapeamento SQL ↔ entidade, igual ao adapter em memória | regras de negócio |
| Rotas Flask, smoke (`tests/app`) | formulários, sessão e renderização de ponta a ponta | casos de borda (já cobertos abaixo) |
