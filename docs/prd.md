# PRD: BarberShop (MVP acadêmico)

## Origem

Este PRD resume o **Lean Inception** feito pelo grupo (Visão do Produto, É/Não
É/Faz/Não Faz, Objetivos, Personas, Jornadas, Brainstorming de Features,
Revisão Técnica/Negócio/UX, Sequenciador e Canvas MVP). O vocabulário está em
[GLOSSARY.md](../GLOSSARY.md).

### Visão do produto

> Para **donos de barbearias** que têm cadeiras ociosas, **barbeiros**
> que pagam taxas altas por corte e **clientes** que querem agendar com
> facilidade com o barbeiro de confiança, o **BarberShop** é um **website**
> que gerencia o calendário de reservas de barbearias, conectando-as a
> barbeiros autônomos e conectando o cliente final a esse ecossistema.
> Diferente da **barbearia tradicional, com taxas altas para barbeiros**,
> nós disponibilizamos uma ferramenta de gestão para aluguel de cadeiras
> com taxas menores para barbeiros autônomos e flexibilidade de local para o
> cliente.

### Objetivos de produto

1. Transformar cadeiras ociosas em faturamento.
2. Mais renda e autonomia para o barbeiro.
3. Agendamento fácil com o barbeiro de confiança.

### Personas

| Persona | Quem | Necessidade principal |
|---|---|---|
| Dono | Carlos, 45, dono de barbearia em Botafogo (6 cadeiras, 2 barbeiros fixos) | Ocupar as cadeiras ociosas |
| Barbeiro | Rafa, 27, barbeiro autônomo, ~25 clientes fiéis por semana | Pagar menos taxa e escolher onde e quando atender |
| Cliente | Lucas, 31, corta a cada 15 dias, fiel ao barbeiro | Horário com o barbeiro de confiança perto de onde está |

## Escopo deste trabalho

O Sequenciador definiu o MVP nas ondas 1 a 7. Para a disciplina, o grupo
escolheu um **recorte mínimo de 5 histórias**, que percorre a hipótese central
do Canvas MVP de ponta a ponta: *barbearias alugam cadeiras ociosas por hora a
barbeiros autônomos, e clientes agendam com seu barbeiro nessas barbearias*.

| Feature do Sequenciador | Onda | Neste trabalho |
|---|---|---|
| Cadastro da barbearia, cadastrar cadeiras | 1 | US2 |
| Horários ociosos e preço por hora | 1 | US2 |
| Cadastro do barbeiro, serviços e preços | 2 | US1, US3 |
| Buscar barbearias no mapa | 3 | US4 |
| Cadastro do cliente | 4 | US1 |
| Reservar bloco de horário | 5 | US4 |
| Agendar horário com o barbeiro, perfil do barbeiro | 6 | US5 |
| Agenda do barbeiro, meu barbeiro no mapa | 7 | US5 |
| Regras da casa | 2 | campo texto em US2 |
| Credenciamento, aprovar/recusar, add-ons, bloquear horários, link da agenda | 2–6 | **fora** (próximo incremento) |

Segue também a decisão do Canvas MVP: **pagamento presencial**, sem pagamento
online ([ADR 0003](adr/0003-pagamento-presencial-no-mvp.md)).

## Histórias de usuário

### US1: Cadastro e login

**Como** dono, barbeiro ou cliente, **quero** criar uma conta e entrar com
e-mail e senha **para** usar as funções da minha persona.

- E-mail é único; senha tem ao menos 6 caracteres.
- A senha nunca é armazenada em texto puro.
- Login com e-mail ou senha errados mostra a mesma mensagem genérica.
- Cada persona só acessa as próprias telas.

### US2: Dono publica cadeiras ociosas

**Como** dono, **quero** cadastrar minha barbearia (endereço, bairro, ponto no
mapa, regras da casa e quantidade de cadeiras) e publicar horários ociosos de
uma cadeira com preço por hora **para** transformar cadeiras ociosas em
faturamento.

- Só um dono cadastra barbearia, e só o dono dela publica horários ociosos.
- Horário ocioso: fim depois do início, no futuro, preço por hora > 0.
- Dois horários ociosos da mesma cadeira não podem se sobrepor.

### US3: Barbeiro cadastra serviços

**Como** barbeiro, **quero** cadastrar meus serviços com preço e duração **para**
que meus clientes saibam o que ofereço e quanto custa.

- Preço > 0 e duração entre 5 e 240 minutos.
- Só barbeiros cadastram serviços.

### US4: Barbeiro reserva bloco de horário

**Como** barbeiro, **quero** buscar cadeiras ociosas por bairro (lista e mapa) e
reservar um bloco de horário **para** atender meus clientes onde e quando eu
quiser.

- A busca mostra só os períodos ainda livres e futuros de cada horário ocioso.
- O bloco precisa caber inteiro dentro de um horário ocioso.
- Um bloco não pode se sobrepor a outro bloco na mesma cadeira.
- Um barbeiro não pode ter dois blocos sobrepostos (em qualquer barbearia).
- Valor do bloco = preço por hora × duração (arredondado ao centavo).

### US5: Cliente agenda com o barbeiro de confiança

**Como** cliente, **quero** encontrar meu barbeiro, ver no mapa onde ele vai
atender e agendar um serviço **para** cortar com quem confio, onde e quando ele
estiver.

- O agendamento cabe inteiro dentro de um bloco de horário do barbeiro.
- Dois agendamentos do mesmo barbeiro não se sobrepõem.
- Agendamento no passado é recusado.
- O barbeiro vê os agendamentos na agenda dele; o cliente vê os seus.

## Métricas (do Canvas MVP)

- Taxa de ocupação das cadeiras antes ociosas (%).
- Reservas de cadeira por barbearia por semana.
- Nº de agendamentos e % de clientes que voltam.
