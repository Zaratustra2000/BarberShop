# 02: Editando o perfil da Barbearia e suas Cadeiras

**What to build:** O Dono edita os dados do perfil da Barbearia e a quantidade de Cadeiras; Clientes e Barbeiros autenticados podem consultar o perfil.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] O Dono responsável pode editar nome, endereço, bairro, localização e regras da casa da Barbearia.
- [x] O perfil atualizado é persistido e aparece quando a Barbearia é consultada.
- [x] O Dono pode adicionar Cadeiras e remover uma Cadeira somente quando nenhum Horário ocioso ou Bloco de horário a referencia.
- [x] Cliente e Barbeiro autenticados podem consultar o perfil, sem permissão para editá-lo.
- [x] Outro Dono não pode editar a Barbearia; acesso não autorizado apresenta o comportamento de erro já adotado pelo projeto.
- [x] A alteração funciona com o adapter em memória e com SQLite, preservando registros existentes.
