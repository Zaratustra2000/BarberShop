# 💈 BarberShop

Marketplace web que transforma **cadeiras ociosas de barbearias** em faturamento.
O dono publica horários ociosos com preço por hora, o **barbeiro autônomo**
reserva blocos de horário onde e quando quiser, e o **cliente** agenda com o seu
barbeiro de confiança na barbearia em que ele estiver.

Trabalho 2 de Engenharia de Software: Flask + Clean Architecture + SOLID +
Pytest.

- Produto definido num **Lean Inception**: resumo em [docs/prd.md](docs/prd.md)
- Linguagem do domínio: [GLOSSARY.md](GLOSSARY.md)
- Decisões de arquitetura: [docs/adr/](docs/adr/)
- Uso de IA (bônus): [docs/uso-de-ia.md](docs/uso-de-ia.md)

## Como rodar

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# (opcional) dados sintéticos de demonstração; a senha das contas é demo123
.venv/bin/python -m scripts.popular_demo

export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
.venv/bin/flask --app app.main:create_app run
# abra http://127.0.0.1:5000
```

Contas de demonstração: `carlos@exemplo.com` (dono), `rafa@exemplo.com`
(barbeiro) e `lucas@exemplo.com` (cliente).

## Mapa municipal offline

A aplicação entrega os tiles locais do Rio de Janeiro nos zooms 10–16. Não usa
tile server externo para o basemap. A manutenção manual, os metadados
obrigatórios e a verificação de navegador estão documentados em
[docs/mapa-municipal-offline.md](docs/mapa-municipal-offline.md).

## Testes e estilo

```bash
.venv/bin/pytest                                    # 108 testes
.venv/bin/pytest --cov=domain --cov=use_cases       # cobertura
.venv/bin/flake8                                    # PEP-8 (0 avisos)
```

Cobertura total: **97%** (domínio e casos de uso entre 89% e 100%).

## Histórias de usuário implementadas

O Sequenciador do Inception colocou 17 features no MVP. Para este trabalho, o
grupo implementou um recorte de **5 histórias** que percorre a hipótese central
do Canvas MVP de ponta a ponta (detalhes e critérios de aceite em
[docs/prd.md](docs/prd.md)).

| História | Casos de uso | Testes dos casos de uso |
|---|---|---|
| **US1** Cadastro e login (as 3 personas) | `CadastrarUsuario`, `AutenticarUsuario` | [test_cadastro_e_login.py](tests/use_cases/test_cadastro_e_login.py) |
| **US2** Dono cadastra barbearia e publica horários ociosos | `CadastrarBarbearia`, `PublicarHorarioOcioso`, `ConsultarBarbeariasDoDono` | [test_dono_publica_cadeiras_ociosas.py](tests/use_cases/test_dono_publica_cadeiras_ociosas.py) |
| **US3** Barbeiro cadastra serviços | `CadastrarServico`, `ConsultarServicosDoBarbeiro` | [test_barbeiro_cadastra_servicos.py](tests/use_cases/test_barbeiro_cadastra_servicos.py) |
| **US4** Barbeiro busca cadeiras por bairro (lista e mapa) e reserva bloco | `BuscarCadeirasOciosas`, `ReservarBlocoDeHorario` | [test_barbeiro_reserva_bloco.py](tests/use_cases/test_barbeiro_reserva_bloco.py) |
| **US5** Cliente acha o barbeiro, vê no mapa onde ele atende e agenda | `BuscarBarbeiros`, `ConsultarPerfilDoBarbeiro`, `AgendarAtendimento`, `ConsultarAgendamentosDoCliente`, `ConsultarAgendaDoBarbeiro` | [test_cliente_agenda_com_barbeiro.py](tests/use_cases/test_cliente_agenda_com_barbeiro.py) |

### Entidades

| Entidade | Arquivo | Regras principais |
|---|---|---|
| `Usuario` (+ `Papel`) | [domain/usuario.py](domain/usuario.py) | e-mail válido e normalizado; ação restrita por persona |
| `Barbearia` (agregado: `Cadeira`, `HorarioOcioso`, `BlocoDeHorario`) | [domain/barbearia.py](domain/barbearia.py) | horários e blocos não se sobrepõem na cadeira; bloco cabe no horário ocioso; valor do bloco proporcional |
| `Servico` | [domain/servico.py](domain/servico.py) | preço > 0; duração entre 5 e 240 min |
| `Agendamento` | [domain/agendamento.py](domain/agendamento.py) | guarda o preço e o nome combinados na hora do agendamento |
| `AgendaDoBarbeiro` | [domain/agenda.py](domain/agenda.py) | agendamento cabe num bloco; sem sobreposição; calcula horários livres |
| `Periodo` (objeto de valor) | [domain/periodo.py](domain/periodo.py) | fim > início; sobreposição, contenção e subtração |

## Clean Architecture

```
            ┌───────────────────────────────────────────────┐
            │  Frameworks & Drivers                         │
            │  app/main.py (Flask) · infra/db (SQLite)      │
            │  ┌─────────────────────────────────────────┐  │
            │  │  Interface Adapters                     │  │
            │  │  app/routes (controllers) · formatos.py │  │
            │  │  infra/repositories (adapters)          │  │
            │  │  ┌───────────────────────────────────┐  │  │
            │  │  │  Use Cases                        │  │  │
            │  │  │  use_cases/*.py · portas.py       │  │  │
            │  │  │  ┌─────────────────────────────┐  │  │  │
            │  │  │  │  Entities  ·  domain/        │  │  │  │
            │  │  │  └─────────────────────────────┘  │  │  │
            │  │  └───────────────────────────────────┘  │  │
            │  └─────────────────────────────────────────┘  │
            └───────────────────────────────────────────────┘
                    as dependências só apontam para dentro
```

| Camada | Pastas | Pode importar |
|---|---|---|
| Entities | `domain/` | nada do projeto além de `domain/` |
| Use Cases | `use_cases/` (casos de uso + **portas** abstratas) | `domain/` |
| Interface Adapters | `app/routes/`, `app/formatos.py`, `infra/repositories/`, `infra/seguranca.py` | camadas internas |
| Frameworks & Drivers | `app/main.py`, `app/container.py`, `app/templates/`, `infra/db/` | tudo |

- **Regra de dependência verificável:** `grep -rE "^(from|import) (flask|sqlite3|werkzeug|app|infra)" domain use_cases` não retorna nada.
- Os **controllers** só traduzem formulário em chamada de caso de uso e
  resultado em HTML. Erros de domínio viram mensagens num único
  `errorhandler` ([app/main.py](app/main.py)).
- O **composition root** ([app/container.py](app/container.py)) é o único lugar
  que conhece as classes concretas.

## SOLID no código

| Princípio | Onde aparece |
|---|---|
| **S**: Responsabilidade Única | Cada caso de uso é uma classe com um único `executar` ([use_cases/](use_cases/)). Validação de entrada da tela fica em [app/formatos.py](app/formatos.py), regras ficam no domínio e persistência fica em [infra/repositories/](infra/repositories/). |
| **O**: Aberto/Fechado | Para trocar o banco basta escrever um novo adapter de `RepositorioDe...`; nenhum caso de uso muda. Foi assim que entraram os adapters em memória e SQLite. |
| **L**: Substituição de Liskov | `RepositorioDeUsuariosEmMemoria` e `RepositorioDeUsuariosSQLite` (e os demais pares) são intercambiáveis, e isso é **provado** pela mesma suíte de contrato que roda nos dois ([tests/infra/conftest.py](tests/infra/conftest.py)). |
| **I**: Segregação de Interfaces | As portas são pequenas e específicas ([use_cases/portas.py](use_cases/portas.py)): `Relogio` só tem `agora()`, `GeradorDeHashDeSenha` só tem `gerar` e `conferir`, e cada repositório expõe só as consultas que os casos de uso usam. |
| **D**: Inversão de Dependência | Os casos de uso recebem as portas abstratas no construtor. Quem decide a implementação é o [container](app/container.py); os testes injetam adapters em memória, um hash falso e um relógio fixo ([tests/dubles.py](tests/dubles.py)). |

## Estratégia de testes

Testes nas **seams** combinadas antes de começar ([docs/fatias.md](docs/fatias.md)):

| Seam | Pasta | O que garante |
|---|---|---|
| Entidades | `tests/domain/` | invariantes e regras de sobreposição, sem I/O |
| Casos de uso | `tests/use_cases/` | regras de negócio e permissões, **isolados da infraestrutura** (adapters em memória) |
| Contrato de repositório | `tests/infra/` | SQLite e memória se comportam igual |
| Rotas (smoke) | `tests/app/` | fluxo completo pelas telas, com SQLite temporário |

Não há mock de classes do próprio projeto. Os únicos dublês são os de fronteira:
relógio e hash de senha.

## Estrutura

```
barbershop/
├── app/                 # Flask: main, container, rotas, templates, estáticos
├── domain/              # entidades e objetos de valor
├── use_cases/           # casos de uso + portas (interfaces)
├── infra/
│   ├── db/              # conexão e esquema SQLite
│   └── repositories/    # adapters: memória e SQLite
├── tests/               # domain/, use_cases/, infra/, app/
├── docs/                # PRD, ADRs, fatias, uso de IA
├── scripts/             # dados sintéticos de demonstração
├── GLOSSARY.md
└── CLAUDE.md            # instruções para agentes de IA
```

## Fora do escopo (próximos incrementos do Sequenciador)

Credenciamento e aprovação de barbeiros, add-ons, bloqueio manual de horários,
link da agenda, pagamento online e split, avaliações, chat e notificações.
O pagamento é presencial no MVP ([ADR 0003](docs/adr/0003-pagamento-presencial-no-mvp.md)).
