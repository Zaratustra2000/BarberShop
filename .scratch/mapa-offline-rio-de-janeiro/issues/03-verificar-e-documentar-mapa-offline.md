# 03: Verificar e documentar o mapa offline

**What to build:** Garantir que o basemap local permaneça protegido por testes
determinísticos e documentar como regenerar periodicamente o pacote municipal
sem atualizar dados da aplicação nem dependências externas.

**Blocked by:** 02: Integrar o basemap nas telas Leaflet

**Status:** resolved

- [x] Os testes HTTP e estáticos verificam a URL local, a ausência de tile server
  externo e a atribuição obrigatória.
- [x] Os testes preservam a presença dos elementos de seleção e marcadores.
- [x] Os testes não fazem requisições reais a tiles ou serviços externos.
- [x] Existe uma verificação manual registrada em navegador, incluindo pan, zoom,
  seleção e marcadores.
- [x] A documentação explica como regenerar manualmente o pacote, registrar a
  data/fonte e substituir apenas o basemap.

## Answer

A verificação manual foi realizada em navegador em 2026-11-24 e confirmou pan,
zoom, seleção de ponto, movimento do marcador, marcadores, popups e atribuição.
Os testes automatizados continuam cobrindo o basemap local sem requisições
externas. Commit da implementação: `92b29da`.
