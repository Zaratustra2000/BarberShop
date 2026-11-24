# 03: Verificar e documentar o mapa offline

**What to build:** Garantir que o basemap local permaneça protegido por testes
determinísticos e documentar como regenerar periodicamente o pacote municipal
sem atualizar dados da aplicação nem dependências externas.

**Blocked by:** 02: Integrar o basemap nas telas Leaflet

**Status:** ready-for-agent

- [x] Os testes HTTP e estáticos verificam a URL local, a ausência de tile server
  externo e a atribuição obrigatória.
- [x] Os testes preservam a presença dos elementos de seleção e marcadores.
- [x] Os testes não fazem requisições reais a tiles ou serviços externos.
- [ ] Existe uma verificação manual registrada em navegador, incluindo pan, zoom,
  seleção e marcadores.
- [x] A documentação explica como regenerar manualmente o pacote, registrar a
  data/fonte e substituir apenas o basemap.
