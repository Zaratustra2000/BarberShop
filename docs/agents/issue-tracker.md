# Issue tracker: Local Markdown

Issues e specs deste repositório vivem em `.scratch/`.

## Convenções

- Um esforço por diretório: `.scratch/<feature-slug>/`.
- O spec é `.scratch/<feature-slug>/spec.md`.
- Tickets de implementação ficam em `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numerados a partir de `01`, um arquivo por ticket.
- Specs publicados por `/to-spec` recebem `Status: ready-for-agent`.
- Comentários e histórico ficam no fim do arquivo sob `## Comments`.

## Publicar no tracker

Ao publicar um spec, criar o arquivo em `.scratch/<feature-slug>/spec.md`, criando o diretório se necessário.

## Operações Wayfinder

- Mapa: `.scratch/<effort>/map.md`, com Notes / Decisions-so-far / Fog.
- Cada ticket fica em `.scratch/<effort>/issues/`, com `Type: research|prototype|grilling|task` e `Status: claimed|resolved`.
- `Blocked by: NN, NN` indica dependências; tickets ficam desbloqueados quando todos os arquivos listados têm `Status: resolved`.
- Para reivindicar, gravar `Status: claimed` antes do trabalho. Para resolver, adicionar `## Answer`, gravar `Status: resolved` e registrar um resumo/link em Decisions-so-far do mapa.
