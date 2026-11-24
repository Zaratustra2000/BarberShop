# 02: Integrar o basemap nas telas Leaflet

**What to build:** Fazer as telas que mostram ou selecionam localidades usar o
basemap municipal offline. A seleção de ponto da Barbearia, os marcadores de
busca e perfil e o ajuste automático aos pontos continuam demonstráveis nas
mesmas telas, agora sem tile server externo.

**Blocked by:** 01: Preparar o pacote municipal offline

**Status:** resolved

- [x] Todas as telas de mapa usam a fonte local em vez de um servidor remoto.
- [x] O pan fica limitado ao município e o zoom máximo é 16.
- [x] O clique continua preenchendo latitude e longitude e pode mover o marcador
  selecionado.
- [x] Os marcadores continuam exibindo título e detalhe em popup.
- [x] A visualização continua ajustada aos marcadores existentes.
- [x] A atribuição visível inclui links para créditos do OpenStreetMap e
  licença ODbL.
- [x] Nenhuma chave externa ou credencial é adicionada.
