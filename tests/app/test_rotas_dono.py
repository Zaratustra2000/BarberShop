from io import BytesIO
import struct
import zlib

from tests.app.conftest import cadastrar_e_entrar, extrair


def chunk_png(tipo, dados):
    corpo = tipo + dados
    return (struct.pack(">I", len(dados)) + corpo
            + struct.pack(">I", zlib.crc32(corpo) & 0xffffffff))


def png_sintetico(tamanho=None):
    assinaturas = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    idat = zlib.compress(b"\x00\x00\x00\x00\xff")
    prefixo = assinaturas + chunk_png(b"IHDR", ihdr)
    prefixo += chunk_png(b"IDAT", idat)
    iend = chunk_png(b"IEND", b"")
    if tamanho is None:
        return prefixo + iend
    tamanho_padding = tamanho - len(prefixo) - len(iend) - 12
    if tamanho_padding < 1:
        raise ValueError("Tamanho de PNG sintético muito pequeno")
    return prefixo + chunk_png(b"tEXt", b"x" * tamanho_padding) + iend


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


def test_dono_edita_perfil_e_adiciona_cadeiras(client):
    cadastrar_e_entrar(client, "dono")
    criar_barbearia(client)
    pagina = client.get("/dono").get_data(as_text=True)
    barbearia_id = extrair(r'/dono/barbearias/(\w+)', pagina)
    pagina = client.post(
        "/dono/barbearias/{}/perfil".format(barbearia_id),
        data=dict(nome="Nova Barbershop", endereco="Rua Nova, 20",
                  bairro="Copacabana", latitude="-22.967",
                  longitude="-43.178", regras="Sem atrasos.",
                  quantidade_de_cadeiras="3"),
        follow_redirects=True).get_data(as_text=True)
    assert "Nova Barbershop" in pagina
    assert "Cadeira 3" in pagina


def test_dono_envia_e_substitui_foto_principal(client):
    cadastrar_e_entrar(client, "dono")
    criar_barbearia(client)
    pagina = client.get("/dono").get_data(as_text=True)
    barbearia_id = extrair(r'/dono/barbearias/(\w+)', pagina)

    pagina = client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(png_sintetico()), "barbearia.png")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)
    assert "/fotos/" in pagina


def test_foto_invalida_nao_altera_a_foto_existente(client):
    cadastrar_e_entrar(client, "dono")
    criar_barbearia(client)
    pagina = client.get("/dono").get_data(as_text=True)
    barbearia_id = extrair(r'/dono/barbearias/(\w+)', pagina)
    client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(png_sintetico()), "original.png")},
        content_type="multipart/form-data",
        follow_redirects=True)

    pagina = client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(b"texto-invalido"), "arquivo.txt")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)
    assert "JPG, PNG ou WebP" in pagina
    assert "/fotos/" in pagina
    assert "arquivo.txt" not in pagina

    pagina = client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(b"\xff\xd8dados-falsos\xff\xd9"),
                       "arquivo-falso.jpg")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)
    assert "Formato inválido. Envie uma imagem JPG, PNG ou WebP." in pagina
    assert "/fotos/" in pagina
    assert "arquivo-falso.jpg" not in pagina

    pagina = client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(
            b"RIFF\x10\x00\x00\x00WEBPVP8 " + b"12345678"),
                       "outra-foto.webp")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)
    assert "/fotos/" in pagina


def test_foto_acima_de_cinco_mb_nao_substitui_a_foto_existente(client):
    cadastrar_e_entrar(client, "dono")
    criar_barbearia(client)
    pagina = client.get("/dono").get_data(as_text=True)
    barbearia_id = extrair(r'/dono/barbearias/(\w+)', pagina)

    tamanho_limite = 5 * 1024 * 1024
    foto_no_limite = png_sintetico(tamanho=tamanho_limite)
    pagina = client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(foto_no_limite), "barbearia.png")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)
    foto_existente = extrair(r'/fotos/([^"]+)', pagina)

    foto_acima_do_limite = foto_no_limite + b"\0"
    pagina = client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(foto_acima_do_limite),
                       "barbearia-grande.png")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)

    assert "A imagem deve ter no máximo 5 MB." in pagina
    assert "/fotos/{}".format(foto_existente) in pagina
