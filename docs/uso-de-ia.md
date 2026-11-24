# Uso de IA no desenvolvimento

**Ferramenta:** Claude Code (modelo Claude Opus 5.5), com o conjunto de skills
de engenharia de **Matt Pocock** (`domain-modeling`, `tdd`, `codebase-design`).
Todos os commits feitos com IA têm a linha `Co-Authored-By: Claude`, então dá
para auditar no `git log` o que a IA produziu.

## Por que uma estratégia, e não só "pedir o código"

Pedir "faça um sistema de barbearia em Flask" a um modelo costuma dar três
problemas:

1. **Vocabulário inventado**: a IA chama de `Slot`, `Booking` ou `Reservation`
   o que o time chamou de *horário ocioso*, *bloco de horário* e *agendamento*.
2. **Fatiamento horizontal**: todas as entidades, depois todos os repositórios,
   depois todas as rotas. Nada funciona de ponta a ponta até o final, e os
   testes escritos em lote verificam a *forma* do código, não o comportamento.
3. **Testes acoplados à implementação**: mocks de classes internas, que passam
   mesmo quando a regra de negócio está errada.

A estratégia de Matt Pocock ataca cada um desses problemas:

| Problema | Técnica | Artefato |
|---|---|---|
| Vocabulário inventado | **Linguagem ubíqua**: o glossário do Lean Inception vira um `GLOSSARY.md` que a IA é obrigada a ler | [GLOSSARY.md](../GLOSSARY.md), [CLAUDE.md](../CLAUDE.md) |
| Decisões que se perdem | **ADRs curtas**, só para decisões difíceis de reverter, surpreendentes e com trade-off real | [docs/adr/](adr/) |
| Fatiamento horizontal | **Fatias verticais (tracer bullets)**: cada história atravessa domínio → caso de uso → repositório → rota → tela | [docs/fatias.md](fatias.md) |
| Testes inúteis | **TDD red → green em seams combinadas antes**, sem mock de classes do projeto | `tests/`, histórico `test:` → `feat:` |
| Código raso | **Módulos profundos**: interface pequena e muita lógica escondida (ex.: `AgendaDoBarbeiro`) | [domain/agenda.py](../domain/agenda.py) |

## O fluxo, passo a passo

1. **Entrada humana.** O Lean Inception (visão, personas, jornadas,
   sequenciador, Canvas MVP) foi feito pelo grupo e é a fonte da verdade. A IA
   não inventou produto: ela leu o board exportado.
2. **Alinhamento antes de codar.** A IA fez perguntas ao grupo, e as respostas
   viraram decisões:
   - escopo: recorte de 5 histórias em vez das 17 features do MVP;
   - seams de teste: entidades, casos de uso com repositórios em memória,
     contrato de repositório e smoke das rotas;
   - login com senha (hash) em vez de "entrar como".
3. **Modelagem de domínio.** O glossário do Inception foi refinado ("cadeira
   ociosa" virou **horário ocioso**, que é o que o dono de fato publica) e
   registrado *antes* do código. Foram escritas três ADRs.
4. **PRD e fatias.** As histórias receberam critérios de aceite testáveis
   ([prd.md](prd.md)) e foram ordenadas em 6 fatias.
5. **TDD por fatia.** Para cada fatia: um commit `test:` (vermelho, comprovado
   rodando o pytest) e depois um commit `feat:` (verde). Basta rodar
   `git log --oneline` para ver o ritmo.
6. **Revisão.** Ao final: checagem automática da regra de dependência (o
   domínio e os casos de uso não importam Flask, sqlite3 nem werkzeug),
   cobertura (97%), `flake8` sem avisos e execução real do servidor com dados
   sintéticos.

## O que os testes pegaram (evidência de que a estratégia funciona)

- **Hash de senha quebrado no macOS.** O teste de rota (seam de smoke) falhou
  porque o `scrypt`, padrão do Werkzeug 3, não existe no Python da Apple
  (LibreSSL). Um teste com mock do hash nunca teria pegado isso. A correção
  ficou registrada em [infra/seguranca.py](../infra/seguranca.py).
- **Divergência entre adapters.** A suíte de contrato, rodando contra SQLite,
  falhou por e-mail duplicado num dado de teste. Isso mostrou que o SQLite
  garante unicidade e o adapter em memória não. A regra de negócio "e-mail
  único" fica no caso de uso, por isso o comportamento visível é o mesmo nos
  dois adapters.

## Limites e responsabilidade do grupo

- A IA **não substitui a revisão**: o grupo deve ler cada caso de uso e cada
  teste e conseguir explicar as regras na apresentação.
- Regras que a IA propôs e que o grupo deve validar como regra de negócio: a
  oferta de horários de 30 em 30 minutos mais o "último início possível", o
  limite de 30 cadeiras por barbearia e a duração de serviço entre 5 e 240
  minutos.
- Só dados **sintéticos** (nomes e e-mails `@exemplo.com`) foram usados em
  testes e no seed. Nenhum segredo está no código: a `SECRET_KEY` vem de
  variável de ambiente.
