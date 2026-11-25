from io import BytesIO

from tests.app.conftest import cadastrar_e_entrar, extrair


def test_barbeiro_cadastra_servico_e_ve_no_painel(client):
    cadastrar_e_entrar(client, "barbeiro")
    pagina = client.post("/barbeiro/servicos", data=dict(
        nome="Corte degradê", preco="45,00", duracao_minutos="40"),
        follow_redirects=True).get_data(as_text=True)
    assert "Corte degradê" in pagina
    assert "R$ 45,00" in pagina
    assert "40 min" in pagina


def test_barbeiro_busca_por_bairro_e_reserva_bloco(client):
    from tests.app.conftest import extrair
    from tests.app.fluxo import dono_publica_horario

    dono_publica_horario(client)
    cadastrar_e_entrar(client, "barbeiro")
    pagina = client.get("/barbeiro/busca?bairro=botafogo").get_data(
        as_text=True)
    assert "Barbearia Exemplo" in pagina
    assert "13:00 às 18:00" in pagina
    assert 'data-mapa-marcadores=' in pagina

    barbearia_id = extrair(r'name="barbearia_id" value="(\w+)"', pagina)
    horario_id = extrair(r'name="horario_ocioso_id" value="(\w+)"', pagina)
    pagina = client.post("/barbeiro/blocos", data=dict(
        barbearia_id=barbearia_id, horario_ocioso_id=horario_id,
        inicio="2030-01-07T14:00", fim="2030-01-07T16:00"),
        follow_redirects=True).get_data(as_text=True)
    assert "Barbearia Exemplo" in pagina
    assert "R$ 60,00" in pagina


def test_barbeiro_ve_barbearias_ativas_sem_informar_bairro(client):
    from tests.app.fluxo import dono_publica_horario

    dono_publica_horario(client)
    cadastrar_e_entrar(client, "barbeiro")
    pagina = client.get("/barbeiro/busca").get_data(as_text=True)

    assert "Barbearia Exemplo" in pagina
    assert "Reservar bloco" in pagina
    assert 'data-mapa-marcadores=' in pagina


def test_barbeiro_ve_barbearia_sem_horarios_como_indisponivel(client):
    from tests.app.test_rotas_dono import criar_barbearia

    cadastrar_e_entrar(client, "dono")
    criar_barbearia(client)
    client.post("/logout")
    cadastrar_e_entrar(client, "barbeiro")

    pagina = client.get("/barbeiro/busca").get_data(as_text=True)

    assert "Barbearia Exemplo" in pagina
    assert "Indisponível para nova reserva" in pagina
    assert "períodos livres" in pagina


def test_barbeiro_ve_estado_vazio_quando_sem_barbearia_ativa(client):
    cadastrar_e_entrar(client, "barbeiro")

    pagina = client.get("/barbeiro/busca?bairro=Copacabana").get_data(
        as_text=True)

    assert "Nenhuma barbearia ativa" in pagina


def test_barbeiro_consulta_perfil_da_barbearia(client):
    from tests.app.fluxo import dono_publica_horario

    dono_publica_horario(client)
    cadastrar_e_entrar(client, "barbeiro")
    pagina = client.get("/barbeiro/busca?bairro=Botafogo").get_data(
        as_text=True)
    barbearia_id = extrair(r'name="barbearia_id" value="(\w+)"', pagina)
    perfil = client.get(
        "/barbeiro/barbearias/{}".format(barbearia_id)).get_data(
            as_text=True)
    assert "Barbearia Exemplo" in perfil
    assert "Sem som alto." in perfil


def test_barbeiro_edita_seu_nome_e_apresentacao(client):
    cadastrar_e_entrar(client, "barbeiro", nome="Rafa")

    pagina = client.post("/barbeiro/perfil", data=dict(
        nome="Rafael Souza",
        apresentacao="Especialista em cortes clássicos."),
        follow_redirects=True).get_data(as_text=True)

    assert "Rafael Souza" in pagina
    assert "Especialista em cortes clássicos." in pagina


def test_barbeiro_envia_foto_do_perfil(client):
    from tests.app.test_rotas_cliente import png_sintetico

    cadastrar_e_entrar(client, "barbeiro", nome="Rafa")
    pagina = client.post(
        "/barbeiro/perfil/foto",
        data={"foto": (BytesIO(png_sintetico()), "rafa.png")},
        content_type="multipart/form-data",
        follow_redirects=True).get_data(as_text=True)

    assert "/fotos/" in pagina


def test_barbeiro_cancela_agendamento_e_cliente_ve_estado(client):
    from tests.app.test_rotas_cliente import barbeiro_pronto_para_atender
    from tests.app.conftest import cadastrar_e_entrar
    from tests.app.fluxo import sair

    barbeiro_pronto_para_atender(client)
    cadastrar_e_entrar(client, "cliente", nome="Lucas Andrade")
    pagina = client.get("/cliente").get_data(as_text=True)
    perfil = extrair(r'href="(/cliente/barbeiros/\w+)"', pagina)
    pagina = client.get(perfil).get_data(as_text=True)
    servico_id = extrair(r'servico_id=(\w+)"', pagina)
    client.post("/cliente/agendamentos", data=dict(
        servico_id=servico_id, inicio="2030-01-07T14:30"))

    with client.application.app_context():
        container = client.application.extensions["barbershop"]
        cliente = container.usuarios.por_email("cliente@exemplo.com")
        agendamento = container.consultar_agendamentos_do_cliente.executar(
            cliente.id)[0].agendamento
        agendamento_id = agendamento.id

    sair(client)
    client.post("/login", data=dict(email="barbeiro@exemplo.com",
                                    senha="segredo1"))
    pagina = client.post(
        "/barbeiro/agendamentos/{}/cancelar".format(agendamento_id),
        follow_redirects=True).get_data(as_text=True)
    assert "Cancelado" in pagina

    sair(client)
    cadastrar_e_entrar(client, "cliente", nome="Lucas Andrade")
    pagina = client.get("/cliente").get_data(as_text=True)
    assert "Cancelado" in pagina


def test_barbeiro_nao_ve_acao_de_cancelar_agendamento_passado(client):
    from datetime import datetime

    from tests.app.test_rotas_cliente import barbeiro_pronto_para_atender
    from tests.app.fluxo import sair

    barbeiro_pronto_para_atender(client)
    cadastrar_e_entrar(client, "cliente", nome="Lucas Andrade")
    pagina = client.get("/cliente").get_data(as_text=True)
    perfil = extrair(r'href="(/cliente/barbeiros/\w+)"', pagina)
    pagina = client.get(perfil).get_data(as_text=True)
    servico_id = extrair(r'servico_id=(\w+)"', pagina)
    client.post("/cliente/agendamentos", data=dict(
        servico_id=servico_id, inicio="2030-01-07T14:30"))

    with client.application.app_context():
        container = client.application.extensions["barbershop"]
        container.relogio.ajustar(datetime(2030, 1, 8, 8))

    sair(client)
    client.post("/login", data=dict(email="barbeiro@exemplo.com",
                                    senha="segredo1"))
    pagina = client.get("/barbeiro").get_data(as_text=True)
    assert "/cancelar" not in pagina
