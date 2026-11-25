# 01: Preparar o pacote municipal offline

**What to build:** Preparar um basemap local utilizável do município do Rio de
Janeiro, derivado de dados OpenStreetMap/ODbL, nos zooms 10–16. O pacote deve
ficar pronto para a aplicação servir sem realizar requisições cartográficas
externas.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] O pacote cobre a área municipal acordada nos zooms 10 a 16.
- [x] Os tiles estão organizados para consumo por uma camada de basemap local
  do Leaflet.
- [x] Há metadados simples sobre fonte, data de preparação e licença.
- [x] Há indicação clara da atribuição exigida pelo OpenStreetMap e pela ODbL.
- [x] Não existe requisição necessária a um tile server externo para usar o
  pacote.

## Answer

Preparado o pacote estático municipal do Rio de Janeiro em
`app/static/basemap/rio-de-janeiro/`, com metadados JSON, atribuição OSM/ODbL,
URL relativa compatível com Leaflet e limites/zooms definidos. O pacote contém
11.630 tiles PNG cobrindo os níveis 10–16. Os tiles foram derivados do extrato
OSM regional e renderizados localmente; o gerador usa o servidor de tiles
apenas em `127.0.0.1` durante a preparação.

O gerador manual `scripts/preparar_basemap_rio.py` reproduz os tiles da área
municipal nos zooms 10–16. A aplicação não contém fallback ou sincronização
externa. A cobertura e a validade PNG de todos os tiles foram verificadas pelos
testes do pacote.
