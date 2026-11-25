Status: ready-for-agent

# Mapa básico offline do Rio de Janeiro

## Problem Statement

As telas de localização da Barbearia exibem o Leaflet, a seleção de ponto e os
marcadores, mas o basemap depende de solicitações a um servidor externo de
tiles. Quando esse servidor é bloqueado ou indisponível, o mapa fica sem
representação visual. Isso impede que Donos visualizem a área ao cadastrar uma
Barbearia e que Barbeiros e Clientes reconheçam os locais em um contexto
geográfico confiável.

## Solution

Entregar um basemap local do município do Rio de Janeiro com a mesma interação
existente do Leaflet. O usuário poderá arrastar o mapa, aproximar e afastar,
selecionar uma localização e visualizar marcadores, sem solicitar tiles a
provedores externos.

O pacote será limitado ao município, cobrirá os zooms 10 a 16 e será mantido
localmente pela aplicação. Fora dessa cobertura ou nesse limite de zoom, a
aplicação não fará requisições externas.

## User Stories

1. Como Dono, quero ver um mapa visual ao cadastrar uma Barbearia, para localizar
   o estabelecimento sem depender de um tile server externo.
2. Como Dono, quero clicar no mapa municipal, para selecionar latitude e
   longitude da Barbearia.
3. Como Dono, quero mover o marcador já selecionado, para corrigir a
   localização antes de cadastrar a Barbearia.
4. Como Dono, quero aproximar o mapa até o nível das ruas, para escolher um ponto
   com precisão nas proximidades da Barbearia.
5. Como Barbeiro, quero ver um mapa ao buscar cadeiras ociosas, para relacionar
   os resultados aos locais do Rio de Janeiro.
6. Como Barbeiro, quero ver os marcadores das Barbearias encontradas no mesmo
   mapa, para comparar visualmente as opções.
7. Como Barbeiro, quero que o mapa ajuste a visualização aos marcadores, para
   encontrar rapidamente as localidades retornadas pela busca.
8. Como Cliente, quero ver a localização dos próximos atendimentos do Barbeiro
   no mapa municipal, para entender onde ele vai atender.
9. Como Cliente, quero ver o título e os detalhes de cada local em um marcador,
   para relacionar o ponto com a Barbearia e o horário.
10. Como pessoa usando o mapa, quero arrastar e ampliar dentro da área municipal,
    para navegar pelos bairros sem trocar de fonte de basemap.
11. Como pessoa usando o mapa, quero que o basemap não seja solicitado de um
    servidor externo, para que bloqueios de rede não removam toda a
    representação visual.
12. Como pessoa usando o mapa, quero ver a atribuição completa do OpenStreetMap
    e da ODbL, para conhecer a fonte e a licença dos dados visualizados.
13. Como pessoa responsável pelo produto, quero que a data e a origem de
    regeneração do basemap estejam registradas, para saber quando os dados
    foram preparados.
14. Como pessoa responsável pelo produto, quero regenerar manualmente o pacote
    municipal a cada revisão planejada, para corrigir mudanças cartográficas
    sem depender de atualização automática externa.
15. Como pessoa responsável pelo produto, quero substituir apenas o pacote
    local do Rio, para preservar os dados de Barbearias e a lógica de
    marcadores.
16. Como pessoa responsável pela implantação, quero que o servidor entregue os
    tiles locais como arquivos estáticos da aplicação, para não exigir banco,
    serviço ou chave adicional.
17. Como pessoa responsável pela implantação, quero que o pacote cubra todo o
    município do Rio de Janeiro nos zooms acordados, para que cadastros não
    fiquem fora da cobertura em princípio.
18. Como pessoa responsável pela implantação, quero que o pan seja limitado ao
    município e o zoom máximo seja 16, para impedir carga externa e uso de área
    fora do pacote.
19. Como mantenedora da aplicação, quero que os testes existentes validem a
    configuração do mapa sem fazer requisições reais, para manter o build
    determinístico e offline.
20. Como mantenedora da aplicação, quero conservar o comportamento atual de
    seleção de ponto, marcadores e ajuste por limites, para não repetir ou
    quebrar funcionalidades já implementadas.

## Implementation Decisions

- Substituir o tile server remoto por um basemap municipal local compatível com
  o comportamento atual do Leaflet.
- Gerar o pacote a partir de dados derivados do OpenStreetMap sob licença ODbL,
  com atribuição permanente visível no mapa.
- Cobrir o município do Rio de Janeiro nos níveis de zoom 10 a 16. O zoom 10
  oferece visão municipal ampla e o zoom 16 oferece detalhe próximo de rua.
- Armazenar os tiles em arquivos estáticos da aplicação, organizados pelo
  município e pelos níveis de zoom e coordenadas esperados pelo Leaflet.
- Limitar o pan aos limites do município e configurar zoom máximo em 16.
- Não oferecer fallback externo para tiles não presentes no pacote.
- Preservar a configuração e o comportamento dos seletores de latitude e
  longitude, dos marcadores e do ajuste automático aos limites dos pontos.
- Não alterar entidades de domínio, casos de uso, repositórios, banco de dados
  ou regras de cadastro; esta mudança pertence à camada de apresentação
  estática.
- Não adicionar chave de provedor, credencial ou variável secreta.
- Atualizar o basemap somente por regeneração manual e periódica. Não incluir
  sincronização automática na aplicação.
- Incluir, junto ao pacote, metadados simples da fonte, da data de preparação
  e da licença, além da atribuição apresentada pela interface.
- Manter o tamanho e a quantidade de arquivos do pacote dentro da aplicação
  como um compromisso de entrega do MVP; migrar para CDN ou armazenamento
  externo fica fora desta especificação.

## Testing Decisions

- O seam principal continuará sendo o teste HTTP da rota que renderiza a página
  e o arquivo estático do mapa. Isso já é usado no teste de cadastro da
  Barbearia e verifica a integração mais próxima da interação no navegador sem
  abrir um domínio externo.
- Um bom teste deve carregar a página renderizada e o JavaScript do mapa, afirmar
  que o tile URL aponta para o basemap local, afirmar que não contém um servidor
  remoto de tiles e afirmar que a atribuição OSM/ODbL permanece visível.
- Também deve verificar que os elementos existentes de seleção e marcadores
  continuam presentes na página e que o código continua inicializando esses
  comportamentos.
- Não serão usados mocks de classes do próprio projeto. Os testes não farão
  requisição real a tiles, apenas validarão a configuração estática entregue
  pela aplicação.
- Testes de domínio, casos de uso, repositórios e banco não precisam ser
  alterados, pois a decisão não muda entidades nem portas.
- Pode haver uma verificação manual em navegador registrando que o basemap
  aparece localmente, que pan e zoom respeitam os limites e que os marcadores
  permanecem utilizáveis.

## Out of Scope

- Dados detalhados além dos níveis de zoom acordados.
- Cobertura fora do município do Rio de Janeiro.
- Atualização automática do basemap a partir da internet.
- Busca de endereço, geocodificação ou endereços reversos.
- Navegação por rotas, cálculo de distâncias ou limites administrativos
  interativos.
- Integração com um novo provedor comercial de tiles.
- Acompanhamento de tráfego ou dados cartográficos em tempo real.
- Migração do pacote para CDN, bucket de objetos ou armazenamento externo.
- Mudança das regras de cadastro, busca ou agendamento.
- Execução de serviços externos durante testes automatizados.

## Further Notes

O basemap será uma instantânea cartográfica, não um feed dinâmico. A precisão
visual pode diferir da fonte original devido à data em que o pacote foi gerado
e aos níveis de zoom distribuídos.

Dados de Barbearias, coordenadas e marcadores continuarão sendo dados locais da
aplicação. Somente o desenho do basemap municipal é fornecido pelo pacote
derivado do OSM/ODbL.
