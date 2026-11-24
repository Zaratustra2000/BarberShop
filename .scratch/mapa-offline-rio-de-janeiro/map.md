# Mapa offline do Rio de Janeiro

## Notes

- Basemap municipal offline com tiles locais nos zooms 10–16.
- Origem derivada do OpenStreetMap sob licença ODbL.
- Preservar seleção de ponto, marcadores, popups e ajuste automático.
- Atualização manual periódica; sem fallback externo.

## Decisions-so-far

- Cobertura: município do Rio de Janeiro.
- Zoom: 10–16.
- Armazenamento: arquivos estáticos da aplicação.
- Licença: atribuição completa a OpenStreetMap e ODbL.
- Pan limitado ao município e zoom máximo em 16.

## Fog

- Nenhuma decisão pendente na especificação aprovada.

## Tickets

- [01: Preparar o pacote municipal offline](./issues/01-preparar-pacote-municipal-offline.md)
- [02: Integrar o basemap nas telas Leaflet](./issues/02-integrar-basemap-nas-telas.md)
- [03: Verificar e documentar o mapa offline](./issues/03-verificar-e-documentar-mapa-offline.md)
