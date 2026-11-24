# 04: Editando e excluindo Horários ociosos

**What to build:** O Dono corrige um Horário ocioso ou o remove quando ainda não há Bloco de horário associado, sem quebrar ofertas ou compromissos.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] Somente o Dono da Barbearia pode editar ou excluir seus Horários ociosos.
- [x] A edição permite corrigir período, Cadeira e preço, respeitando a validade do período, preço positivo e pertencimento da Cadeira à Barbearia.
- [x] A edição não cria sobreposição com outro Horário ocioso da mesma Cadeira.
- [x] Quando há Blocos de horário, a edição mantém cada Bloco dentro do Horário ocioso e preserva o valor já combinado de cada Bloco.
- [x] A exclusão é recusada quando existe qualquer Bloco de horário associado.
- [x] Horários ociosos sem Blocos podem ser excluídos e deixam de aparecer nas ofertas.
- [x] Falhas e permissões são verificadas no domínio/caso de uso e no fluxo de rota, sem mocks de classes do projeto.
