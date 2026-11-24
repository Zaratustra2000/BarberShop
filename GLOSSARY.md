# BarberShop

Marketplace que conecta barbearias com cadeiras ociosas a barbeiros autônomos e
conecta os clientes desses barbeiros ao ecossistema. Vocabulário validado no
Lean Inception e refinado durante a modelagem.

## Pessoas

**Dono**:
Pessoa responsável por uma ou mais barbearias, que publica horários ociosos das
suas cadeiras.
_Avoid_: proprietário, administrador, lojista

**Barbeiro**:
Profissional autônomo que reserva blocos de horário em cadeiras de barbearias e
atende seus próprios clientes nelas.
_Avoid_: profissional, prestador, funcionário

**Cliente**:
Pessoa que agenda atendimentos com um barbeiro.
_Avoid_: usuário final, consumidor

**Barbeiro de confiança**:
Barbeiro que o cliente segue, seja qual for a barbearia onde ele atende.

## Lugar e tempo

**Barbearia**:
Estabelecimento físico, com endereço e localização no mapa, que tem cadeiras e
regras da casa.
_Avoid_: loja, salão, estabelecimento

**Cadeira**:
Estação de corte de uma barbearia; é a unidade que se aluga.
_Avoid_: estação, posto, bancada

**Regras da casa**:
Condições que a barbearia impõe a quem atende nela.

**Horário ocioso**:
Período em que uma cadeira está sem barbeiro e o dono a oferece para aluguel,
com um preço por hora.
_Avoid_: vaga, disponibilidade, slot

**Cadeira ociosa**:
Cadeira que tem um horário ocioso em determinado momento.

**Bloco de horário**:
Parte de um horário ocioso que um barbeiro reservou para atender naquela
cadeira.
_Avoid_: reserva de cadeira, locação, aluguel

**Agendamento**:
Atendimento de um serviço, marcado por um cliente com um barbeiro, dentro de um
bloco de horário desse barbeiro.
_Avoid_: reserva, booking, horário marcado

**Serviço**:
Trabalho oferecido por um barbeiro (corte, barba etc.), com preço e duração
definidos por ele.
_Avoid_: procedimento, produto

**Avaliação**:
Nota inteira de 1 a 5, sem comentário, que o cliente dá a um agendamento seu
não cancelado, depois do fim do horário previsto. Há no máximo uma por
agendamento e o cliente pode alterá-la. A média e a quantidade das avaliações
de um barbeiro aparecem na lista e no perfil dele. A avaliação não verifica
que o cliente compareceu ao atendimento.
_Avoid_: review, comentário, estrelas

**Agenda do barbeiro**:
Conjunto dos blocos de horário e dos agendamentos de um barbeiro.

## Fora do MVP

**Credenciamento**:
Aprovação de um barbeiro por uma barbearia para que ele possa atender lá.

**Add-on**:
Extra vendido pela barbearia durante o atendimento (lavagem, máquinas, café,
cerveja).
_Avoid_: adicional, extra

**Barbearia premium**:
Barbearia com estrutura superior, que cobra um preço adicional.
