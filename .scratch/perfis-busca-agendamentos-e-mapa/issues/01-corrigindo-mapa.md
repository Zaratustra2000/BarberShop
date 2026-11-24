# 01: Corrigindo a exibição do mapa

**What to build:** O mapa volta a exibir tiles nas telas de localização, mantendo a seleção de ponto e os marcadores que já existem.

**Blocked by:** None (can start immediately).

**Status:** resolved

- [x] As requisições usam a URL oficial dos tiles OSM, sem subdomínios.
- [x] A atribuição visível inclui links para os créditos do OpenStreetMap exigidos pela política.
- [x] Selecionar a localização da Barbearia e visualizar marcadores continua funcionando.
- [x] A aplicação não adiciona chave externa nem faz requisições aos tiles em testes automatizados.
- [x] A exibição é verificada manualmente no navegador, registrando que a disponibilidade depende do serviço externo.

## Answer

As telas que usam Leaflet continuam preservando seleção e marcadores. O mapa
agora usa `https://tile.openstreetmap.org/{z}/{x}/{y}.png`, sem subdomínios, e
exibe atribuição visível com link para os créditos do OpenStreetMap.

Os testes automatizados verificam a configuração e não fazem requisições aos
tiles. A disponibilidade visual em navegador deve ser registrada manualmente,
pois depende do serviço externo.
