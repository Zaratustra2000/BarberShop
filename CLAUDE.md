# BarberShop: instruções para agentes

- Leia `GLOSSARY.md` antes de nomear qualquer coisa. Classes, métodos, testes e
  telas usam os termos de lá, em português (ex.: `HorarioOcioso`, nunca
  `Slot`).
- Respeite as ADRs em `docs/adr/`.
- Camadas (Clean Architecture); a dependência só aponta para dentro:
  `app/` → `use_cases/` → `domain/`; `infra/` implementa `use_cases/portas.py`.
  `domain/` e `use_cases/` nunca importam Flask, sqlite3 ou werkzeug.
- Trabalhe em fatias verticais com TDD (veja `docs/fatias.md`): um teste
  vermelho, o mínimo para ficar verde, e repita. Teste apenas nas seams
  combinadas. Nunca use mock de classes do próprio projeto; use os adapters em
  memória.
- Use dados sintéticos em testes e seeds. Nunca coloque segredos no código: a
  `SECRET_KEY` vem de variável de ambiente.
- Antes de concluir: `.venv/bin/pytest` e `.venv/bin/flake8` precisam passar.
