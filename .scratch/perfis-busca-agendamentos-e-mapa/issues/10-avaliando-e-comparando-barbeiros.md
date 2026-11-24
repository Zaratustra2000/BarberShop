# 10: Avaliando e comparando Barbeiros

**What to build:** O Cliente avalia seu Agendamento elegível e compara Barbeiros pela média e quantidade de avaliações na lista e no perfil.

**Blocked by:** 08: Descobrindo todos os Barbeiros; 09: Cancelando Agendamentos futuros.

**Status:** done

- [x] O Cliente só pode avaliar um Agendamento seu, não cancelado, depois do fim do horário previsto.
- [x] A nota aceita valores inteiros de 1 a 5; não há comentário escrito.
- [x] Existe no máximo uma Avaliação por Agendamento; o Cliente pode alterar a própria nota sem criar uma segunda Avaliação.
- [x] Outro Cliente, Barbeiro ou Dono não pode criar nem alterar a Avaliação de outra pessoa.
- [x] A média e a quantidade refletem as Avaliações válidas do Barbeiro e aparecem na lista e no perfil.
- [x] Barbeiros sem Avaliações são apresentados com um estado vazio claro, sem nota inventada.
- [x] Avaliações persistem de forma consistente nos adapters em memória e SQLite.
- [x] Testes cobrem limites da nota, elegibilidade temporal, cancelamento, propriedade, atualização e agregação.
- [x] O vocabulário de domínio é atualizado para registrar `Avaliação`; não se afirma que a presença no atendimento foi verificada.
