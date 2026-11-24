# 05: Excluindo ou desativando Barbearias com segurança

**What to build:** O Dono remove uma Barbearia sem histórico de Blocos de horário ou desativa uma Barbearia usada, preservando compromissos existentes.

**Blocked by:** None (can start immediately).

**Status:** done

- [x] O Dono responsável pode excluir definitivamente uma Barbearia que não tem Blocos de horário.
- [x] Uma Barbearia com histórico de Blocos de horário não é apagada; pode ser desativada pelo Dono.
- [x] A Barbearia desativada deixa de aparecer em novas buscas e não aceita novos Blocos de horário.
- [x] Blocos existentes permanecem válidos e Clientes ainda podem agendar dentro deles.
- [x] Agendamentos e dados históricos continuam consultáveis depois da desativação.
- [x] Um Dono não pode excluir nem desativar a Barbearia de outro Dono.
- [x] A operação funciona nos adapters em memória e SQLite sem apagar referências históricas.
