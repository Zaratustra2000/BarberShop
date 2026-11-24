# Mapa municipal offline

O basemap do município do Rio de Janeiro é entregue por arquivos estáticos em
`app/static/basemap/rio-de-janeiro/`. A aplicação usa apenas a URL relativa
`/static/basemap/rio-de-janeiro/{z}/{x}/{y}.png`, nos zooms 10 a 16. Não há
fallback para tiles ou serviços externos.

## Regeneração manual

A regeneração é periódica e executada somente por uma pessoa mantenedora.

1. Instale Docker e certifique-se de que o daemon está disponível.
2. Execute:

   ```bash
   .venv/bin/python scripts/preparar_basemap_rio.py
   ```

   Para reproduzir a partir de um extrato local, use:

   ```bash
   .venv/bin/python scripts/preparar_basemap_rio.py \
     --extrato caminho/rio.osm.pbf \
     --data-extrato 2026-11-20 \
     --fonte-extrato "Recorte municipal fornecido" \
     --url-extrato "https://fonte.exemplo/rio.osm.pbf"
   ```

3. Aguarde o script gerar todos os tiles previstos para a área municipal.
4. Confirme a presença de `metadata.json`, `ATRIBUICAO.txt` e dos tiles nos
   diretórios dos zooms 10 a 16.
5. Execute a verificação automatizada:

   ```bash
   .venv/bin/pytest tests/app/test_pacote_mapa_municipal.py \
     tests/app/test_rotas_barbeiro.py \
     tests/app/test_rotas_cliente.py \
     tests/app/test_rotas_dono.py
   ```

O script baixa o extrato regional do Geofabrik, recorta o município e renderiza
os tiles por Docker. Ele não atualiza dados de Barbearias, cadastros,
marcadores, banco de dados ou dependências Python.

## Registrar origem e data

Após a regeneração, registre a revisão cartográfica em `metadata.json`:

- `fonte` e `fonte_url`: origem OpenStreetMap;
- `extrato`, `extrato_url` e `data_extrato`: extrato usado;
- `licenca` e `licenca_url`: licença ODbL;
- `data_preparacao`: data da geração;
- `zoom_minimo`, `zoom_maximo` e `limites`: cobertura reproduzida.

Não altere esses dados manualmente para afirmar uma revisão que não foi
gerada. Preserve a atribuição em `ATRIBUICAO.txt` e no JavaScript Leaflet.

## Substituir somente o basemap

Substitua apenas a pasta `app/static/basemap/rio-de-janeiro/` e revise o
JavaScript ou os metadados somente quando o formato acordado mudar. Não altere
dados de Barbearias, coordenadas de marcadores, repositórios, banco de dados,
casos de uso ou dependências da aplicação ao renovar os tiles.

## Verificação manual

Execute em um navegador com acesso à rede bloqueado para tiles externos.

- [x] Abra o cadastro de uma Barbearia e confirme a seleção por clique.
- [x] Clique uma segunda vez e confirme que o mesmo marcador é movido.
- [x] Aproxime e afaste o mapa; confirme zoom mínimo 10 e máximo 16.
- [x] Arraste o mapa para os limites municipais; confirme que o pan não sai da
  cobertura municipal.
- [x] Abra a busca do Barbeiro e o perfil do Cliente; confirme marcadores,
  popups e ajuste automático aos limites.
- [x] Confirme os links visíveis de atribuição OpenStreetMap e ODbL.
- [x] No DevTools Network, confirme que não há requisições a tile servers
  externos.

**Status da verificação:** concluída em navegador em 2026-11-24. Foram
confirmados pan, zoom, seleção, movimento do marcador, marcadores, popups,
atribuição e ausência de requisições a tile servers externos.
