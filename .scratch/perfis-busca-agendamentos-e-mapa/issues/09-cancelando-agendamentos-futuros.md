# 09: Cancelando Agendamentos futuros

**What to build:** O Barbeiro cancela um Agendamento futuro próprio, preservando o histórico e liberando aquele horário para outro Cliente dentro do mesmo Bloco de horário.

**Blocked by:** None (can start immediately).

**Status:** ready-for-agent

- [ ] Somente o Barbeiro responsável pode cancelar seu Agendamento futuro.
- [ ] Agendamentos passados ou de outro Barbeiro não podem ser cancelados por essa operação.
- [ ] O cancelamento preserva o Agendamento e registra seu estado; não apaga o histórico.
- [ ] O horário cancelado deixa de bloquear outro Agendamento dentro do mesmo Bloco de horário.
- [ ] Cliente e Barbeiro veem o estado cancelado em seus históricos.
- [ ] Não é enviada notificação por e-mail ou serviço externo.
- [ ] Permissões, conflito de horário e persistência são cobertos por testes de caso de uso, contrato e rota.
