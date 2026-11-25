Status: ready-for-agent

# Perfis, descoberta, Agendamentos e mapa

## Problem Statement

Donos não conseguem corrigir ou administrar adequadamente suas Barbearias e
Horários ociosos depois do cadastro. Barbeiros e Clientes precisam conhecer as
opções disponíveis sem informar um bairro ou nome exato. Os perfis não oferecem
as informações de apresentação necessárias, Clientes não conseguem comparar
Barbeiros por nota e Barbeiros não conseguem cancelar Agendamentos futuros. Em
algumas telas, o mapa exibe uma mensagem de bloqueio do servidor de tiles do
OpenStreetMap.

## Solution

Permitir que Donos editem perfis de Barbearias, adicionem uma foto principal,
ajustem Cadeiras com segurança e corrijam ou removam Horários ociosos. Barbearias
com histórico de Blocos de horário poderão ser desativadas sem perder os
compromissos existentes.

Permitir que Barbeiros mantenham um perfil com apresentação e foto, naveguem por
todas as Barbearias ativas e cancelem seus Agendamentos futuros. Permitir que
Clientes naveguem por todos os Barbeiros, vejam a nota agregada e avaliem
Agendamentos passados não cancelados. Corrigir a integração existente do mapa
com o serviço padrão de tiles do OpenStreetMap, sem chave externa.

## User Stories

1. As a Dono, I want to view each of my Barbearias and its profile, so that I
   can manage my establishments from one place.
2. As a Dono, I want to edit a Barbearia's name, address, bairro, map location,
   and house rules, so that its public profile stays accurate.
3. As a Dono, I want to adjust the number of Cadeiras, so that the profile
   reflects the current establishment.
4. As a Dono, I want to remove a Cadeira only when it has no Horários ociosos or
   Blocos de horário, so that existing offers and commitments remain valid.
5. As a Dono, I want to add one optional main photo to a Barbearia, so that
   Clients and Barbeiros can recognize it.
6. As a Dono, I want to replace the Barbearia's photo, so that I can correct or
   update its presentation.
7. As an authenticated Cliente or Barbeiro, I want to view a Barbearia's
   profile, so that I can decide whether to book or work there.
8. As a Dono, I want to edit a Horário ocioso's period, Cadeira, and hourly
   price, so that I can correct data-entry mistakes.
9. As a Dono, I want an edited Horário ocioso to avoid overlapping another
   Horário ocioso for the same Cadeira, so that conflicting offers cannot be
   created.
10. As a Dono, I want an edited Horário ocioso to continue containing every
    existing Bloco de horário, so that an edit cannot invalidate a Barbeiro's
    commitment.
11. As a Dono, I want a price change to leave the price of an existing Bloco de
    horário unchanged, so that the agreed rental value is preserved.
12. As a Dono, I want to delete a Horário ocioso only when it has no associated
    Bloco de horário, so that reserved time is not erased.
13. As a Dono, I want to permanently delete a Barbearia that has never had a
    Bloco de horário, so that I can remove an unused registration.
14. As a Dono, I want a Barbearia with Blocos de horário to be deactivated
    rather than erased, so that its history remains intact.
15. As a Dono, I want a deactivated Barbearia hidden from new discovery and
    unable to accept new Blocos de horário, so that it no longer offers new
    rental periods.
16. As a Barbeiro, I want existing Blocos de horário at a deactivated
    Barbearia to remain valid, so that my commitments are not canceled.
17. As a Cliente, I want to continue booking within an existing Bloco de horário
    at a deactivated Barbearia, so that deactivation does not invalidate
    commitments already made by the Barbeiro.
18. As a Barbeiro, I want to edit my display name, a short presentation, and one
    optional profile photo, so that Clients can learn who I am.
19. As a Barbeiro, I want my account email to remain private on my public
    profile, so that profile discovery does not expose a login identifier.
20. As a Barbeiro, I want to browse all active Barbearias without first entering
    an exact bairro, so that I can discover places to work.
21. As a Barbeiro, I want to optionally filter Barbearias by a flexible bairro
    match, so that I can narrow the list without knowing the exact spelling.
22. As a Barbeiro, I want the Barbearia list to indicate whether it has future
    Horários ociosos that can still be reserved, so that I can distinguish
    available places from places without an offer.
23. As a Cliente, I want to browse all registered Barbeiros without first
    entering an exact name, so that I can discover whom to choose.
24. As a Cliente, I want the Barbeiro list to indicate when a Barbeiro has no
    Serviço or available time, so that I understand why I cannot book yet.
25. As a Cliente, I want to optionally filter Barbeiros by a flexible name
    match, so that I can find a particular Barbeiro without exact spelling.
26. As a Cliente, I want to see a Barbeiro's average rating and number of
    ratings in the selection list and profile, so that I can compare
    experiences.
27. As a Cliente, I want to rate a non-canceled Agendamento after its scheduled
    end time, so that I can share feedback after the expected service time.
28. As a Cliente, I want each Agendamento to have at most one rating from its
    own Cliente, so that the same experience is not counted multiple times.
29. As a Cliente, I want to edit my own rating for an eligible Agendamento, so
    that I can correct a mistake without creating a duplicate.
30. As a Cliente, I want future and canceled Agendamentos to be ineligible for
    ratings, so that ratings follow the agreed timing and cancellation rules.
31. As a Barbeiro, I want to cancel my own future Agendamento, so that I can
    handle a change in my availability.
32. As a Barbeiro, I want cancellation to preserve the Agendamento and its
    canceled state, so that both parties retain a history of what happened.
33. As a Cliente, I want a canceled Agendamento to remain visible in my
    history, so that I know it will no longer take place.
34. As a Barbeiro, I want canceled Agendamentos to remain visible in my
    history, so that I can review changes to my schedule.
35. As a Cliente, I want the time of a canceled Agendamento to become available
    again within the Barbeiro's existing Bloco de horário, so that another
    Cliente can book it.
36. As a Cliente or Barbeiro, I want the map to load on pages that show or
    select locations, so that I can use the location features.
37. As a map user, I want the tile requests to use the official OSM tile URL and
    visible linked attribution, so that the map follows the stated tile usage
    requirements.

## Implementation Decisions

- Preserve the Clean Architecture direction: domain rules stay in the domain;
  use cases orchestrate through repository ports; infrastructure adapters
  implement those ports; Flask routes translate requests and responses.
- Preserve the existing `Barbearia` aggregate boundary from ADR 0001: Cadeiras,
  Horários ociosos, and Blocos de horário are validated and persisted as one
  aggregate.
- Extend the Barbearia profile with an active/deactivated state and an optional
  main-photo reference. Allow physical deletion only when there are no Blocos
  de horário; otherwise deactivate and preserve the aggregate and its history.
- Allow removal of a Cadeira only when no Horário ocioso or Bloco de horário
  refers to it. When a Barbearia is deactivated, hide it from new discovery and
  prevent new Blocos, but keep existing Blocos and Agendamentos usable.
- Editing a Horário ocioso must preserve its validity, avoid same-Cadeira
  overlaps, and contain every associated Bloco. Deletion is rejected if a
  Bloco exists. A changed hourly price does not recalculate existing
  `BlocoDeHorario.valor_centavos`.
- Extend the Barbeiro profile with editable presentation text and an optional
  photo. The existing display name remains editable; account email is not part
  of the profile response.
- Store one optional image per Barbearia and Barbeiro in local, configurable
  application storage. Accept JPG, PNG, or WebP up to 5 MB; generate server-side
  filenames, validate uploads, and allow replacement. No cloud image service or
  gallery is included.
- Add a canceled state to Agendamento without deleting the record. Only the
  Barbeiro responsible for a future Agendamento can cancel it. A canceled
  Agendamento is excluded from schedule-conflict calculations so its time can
  be booked again within the same Bloco; cancellation does not delete or
  release the Bloco itself. Show the canceled state to both Cliente and
  Barbeiro. Do not send email or external notifications.
- Introduce the domain concept `Avaliação` for a 1–5 star rating associated with
  an Agendamento. Only that Agendamento's Cliente may create or update it, only
  after the scheduled end time and if the Agendamento is not canceled. Enforce
  one rating per Agendamento and calculate the Barbeiro's average and count
  from stored ratings. Do not accept written comments. A passed scheduled time
  is not proof that the service was attended.
- Add repository-port operations and matching in-memory and SQLite adapters for
  directories, profile changes, deactivation, cancellation, and ratings.
  Update the SQLite schema compatibly so existing local databases retain their
  data.
- Discovery lists include all active Barbearias and all registered Barbeiros,
  including those without a reservable Horário or bookable Serviço/time. Make
  bairro and name filters optional and flexible rather than exact-only. Indicate
  availability and provide a clear empty/unavailable state.
- Keep profile pages accessible to authenticated product personas. A
  deactivated Barbearia is omitted from new discovery while existing records
  remain available in the relevant histories.
- Correct the map layer to request
  `https://tile.openstreetmap.org/{z}/{x}/{y}.png` without subdomains, and show
  visible linked attribution for OpenStreetMap contributors. Keep Leaflet and
  the current interactive map behavior; do not add a tile-provider key. If the
  compliant configuration remains blocked, choosing another provider is a
  separate follow-up decision.
- Update the product documentation to include the new profile, discovery,
  cancellation, rating, and map behavior. Add `Avaliação` to the domain
  glossary.

## Testing Decisions

- Tests should assert externally observable business behavior, permissions,
  persistence, rendered results, and errors; avoid asserting internal call
  sequences or implementation details.
- Domain tests cover editing/deleting Horários ociosos, Cadeira removal,
  same-Cadeira overlap, containment of existing Blocos, price snapshots,
  Barbearia deactivation, rating eligibility, and canceled Agendamento
  availability.
- Use-case tests use the in-memory repository adapters and fixed clock to cover
  ownership, role restrictions, browse-all behavior, profile updates,
  cancellation, and rating create/update rules. Do not mock project classes.
- Repository contract tests run against both in-memory and SQLite adapters to
  verify profiles, active Barbearias, canceled Agendamentos, and Avaliações
  survive save/load consistently.
- Route smoke tests cover authenticated access, profile editing, validated
  photo upload/replacement, list and profile rendering, cancellation visibility,
  and rating submission/update. Use synthetic image data.
- Do not call external tile servers from automated tests. Verify the configured
  tile URL and visible attribution in the page, then manually check map display
  in a browser.
- Follow the repository's existing vertical-slice test seams: domain,
  use-case, repository-contract, and route smoke tests. Similar prior art exists
  for Barbearia invariants, use-case permissions, repository parity, and
  end-to-end route flows.

## Out of Scope

- Canceling an Agendamento as a Cliente.
- Email, SMS, push, or other notifications.
- Written reviews, moderation, appeals, or verification that the service was
  actually attended.
- Barber or Client profile photos beyond the single optional Barbeiro profile
  photo and Barbearia main photo.
- Image galleries, remote image hosting, or image transformation services.
- Editing or canceling a Bloco de horário, or removing a Cadeira that still has
  a Horário ocioso or Bloco de horário.
- Replacing OSM with a different provider, self-hosting tiles, adding a key, or
  guaranteeing production availability. Revisit only if the compliant OSM
  configuration remains blocked.
- Broad refactoring or unrelated product changes.

## Further Notes

- The existing PRD lists ratings outside the original MVP. This spec explicitly
  adds a minimal rating capability based on the user's decision; the PRD and
  glossary should be updated consistently.
- The rating rule is time-based, not attendance-verified: a past,
  non-canceled Agendamento can be rated even if the system cannot establish
  whether the parties met.
- The current SQLite setup creates tables but must also support existing local
  database files when profile fields, deactivation, cancellation, and ratings
  are introduced.
- Browser verification of map tiles depends on network access and the
  third-party OSM tile service; successful local tests do not guarantee tile
  availability.
