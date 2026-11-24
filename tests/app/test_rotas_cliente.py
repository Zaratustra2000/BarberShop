import base64
from io import BytesIO

from tests.app.conftest import cadastrar_e_entrar, extrair
from tests.app.fluxo import dono_publica_horario, sair


def barbeiro_pronto_para_atender(client):
    dono_publica_horario(client)
    cadastrar_e_entrar(client, "barbeiro", nome="Rafa Souza")
    client.post("/barbeiro/servicos", data=dict(
        nome="Corte", preco="45,00", duracao_minutos="40"))
    pagina = client.get("/barbeiro/busca?bairro=Botafogo").get_data(
        as_text=True)
    client.post("/barbeiro/blocos", data=dict(
        barbearia_id=extrair(r'name="barbearia_id" value="(\w+)"', pagina),
        horario_ocioso_id=extrair(r'name="horario_ocioso_id" value="(\w+)"',
                                  pagina),
        inicio="2030-01-07T14:00", fim="2030-01-07T16:00"))
    sair(client)


def test_cliente_acha_o_barbeiro_e_agenda(client):
    barbeiro_pronto_para_atender(client)
    cadastrar_e_entrar(client, "cliente", nome="Lucas Andrade")

    pagina = client.get("/cliente?nome=rafa").get_data(as_text=True)
    perfil = extrair(r'href="(/cliente/barbeiros/\w+)"', pagina)
    pagina = client.get(perfil).get_data(as_text=True)
    assert "Barbearia Exemplo" in pagina
    assert 'data-mapa-marcadores=' in pagina

    servico_id = extrair(r'servico_id=(\w+)"', pagina)
    pagina = client.get(perfil + "?servico_id=" + servico_id).get_data(
        as_text=True)
    assert "14:30" in pagina

    pagina = client.post("/cliente/agendamentos", data=dict(
        servico_id=servico_id, inicio="2030-01-07T14:30"),
        follow_redirects=True).get_data(as_text=True)
    assert "07/01/2030 14:30" in pagina
    assert "Rafa Souza" in pagina

    sair(client)
    client.post("/login", data=dict(email="barbeiro@exemplo.com",
                                    senha="segredo1"))
    assert "Lucas Andrade" in client.get("/barbeiro").get_data(as_text=True)


def test_cliente_consulta_perfil_da_barbearia(client):
    from tests.app.fluxo import dono_publica_horario

    dono_publica_horario(client)
    with client.application.app_context():
        container = client.application.extensions["barbershop"]
        dono = container.usuarios.por_email("dono@exemplo.com")
        barbearia_id = container.consultar_barbearias_do_dono.executar(
            dono.id)[0].id
    cadastrar_e_entrar(client, "dono")
    client.post(
        "/dono/barbearias/{}/foto".format(barbearia_id),
        data={"foto": (BytesIO(
            base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lE"
                "QVR42mP8/x8AAusB9Wl/4nQAAAAASUVORK5CYII=")),
                 "barbearia.png")},
        content_type="multipart/form-data",
        follow_redirects=True)
    cadastrar_e_entrar(client, "cliente")
    perfil = client.get(
        "/cliente/barbearias/{}".format(barbearia_id)).get_data(
            as_text=True)
    assert "Barbearia Exemplo" in perfil
    assert "/fotos/" in perfil
