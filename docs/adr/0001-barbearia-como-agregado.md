# Barbearia é o agregado que guarda cadeiras, horários ociosos e blocos

As regras de sobreposição ("dois horários ociosos da mesma cadeira não se
sobrepõem", "dois blocos na mesma cadeira não se sobrepõem", "o bloco cabe
dentro do horário ocioso") envolvem cadeira, horário ocioso e bloco ao mesmo
tempo. Por isso, os três vivem dentro do agregado `Barbearia`, que é lido e
salvo inteiro pelo repositório: as invariantes ficam num só lugar, testáveis sem
banco. A regra que atravessa barbearias ("um barbeiro não tem dois blocos
sobrepostos") fica no caso de uso `ReservarBlocoDeHorario`, que consulta as
outras barbearias pelo repositório.

## Consequências

- Uma barbearia com muitos horários antigos fica pesada de carregar. Para o MVP
  isso é aceitável; arquivar horários passados resolve no futuro.
