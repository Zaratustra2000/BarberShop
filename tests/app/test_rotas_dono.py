from tests.app.conftest import cadastrar_e_entrar, extrair


def criar_barbearia(client):
    return client.post("/dono/barbearias", data=dict(
        nome="Barbearia Exemplo", endereco="Rua Exemplo, 100",
        bairro="Botafogo", latitude="-22.951", longitude="-43.184",
        regras="Sem som alto.", quantidade_de_cadeiras="2"),
        follow_redirects=True)


def test_dono_cadastra_barbearia_e_publica_horario_ocioso(client):
    cadastrar_e_entrar(client, "dono")
    pagina = criar_barbearia(client).get_data(as_text=True)
    assert "Cadeira 2" in pagina

    barbearia_id = extrair(r'/dono/barbearias/(\w+)/horarios', pagina)
    cadeira_id = extrair(r'<option value="(\w+)">Cadeira 1', pagina)
    pagina = client.post(
        "/dono/barbearias/{}/horarios".format(barbearia_id),
        data=dict(cadeira_id=cadeira_id, inicio="2030-01-07T13:00",
                  fim="2030-01-07T18:00", preco_por_hora="30,00"),
        follow_redirects=True).get_data(as_text=True)
    assert "R$ 30,00" in pagina
    assert "07/01/2030 13:00" in pagina


def test_regra_violada_volta_com_mensagem(client):
    cadastrar_e_entrar(client, "dono")
    pagina = client.post("/dono/barbearias", data=dict(
        nome="", endereco="Rua Exemplo", bairro="Botafogo",
        latitude="-22.9", longitude="-43.1", quantidade_de_cadeiras="1"),
        headers={"Referer": "/dono/barbearias/nova"},
        follow_redirects=True).get_data(as_text=True)
    assert "Informe o nome" in pagina


def test_mapa_da_nova_barbearia_usa_mapa_municipal_offline(client):
    cadastrar_e_entrar(client, "dono")

    pagina = client.get("/dono/barbearias/nova").get_data(as_text=True)
    script = client.get("/static/mapa.js").get_data(as_text=True)

    assert 'data-mapa-seletor' in pagina
    assert 'data-lat="#latitude"' in pagina
    assert 'data-lng="#longitude"' in pagina
    assert '/static/basemap/rio-de-janeiro/{z}/{x}/{y}.png' in script
    assert 'tile.openstreetmap.org' not in script
    assert 'https://www.openstreetmap.org/copyright' in script
    assert 'https://opendatacommons.org/licenses/odbl/' in script
    assert 'maxBounds' in script
    assert 'maxZoom: 16' in script
    assert 'marcador.setLatLng' in script
    assert 'L.marker' in script
    assert 'minZoom: 10' in script
    assert 'fitBounds(limites' in script
    assert 'lat.value = e.latlng.lat.toFixed(6)' in script
    assert 'lng.value = e.latlng.lng.toFixed(6)' in script
    assert 'marcador.setLatLng(e.latlng)' in script
    assert 'm.bindPopup(caixa)' in script
    assert 'chave' not in script.lower()
