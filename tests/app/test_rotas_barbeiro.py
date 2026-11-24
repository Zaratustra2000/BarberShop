from tests.app.conftest import cadastrar_e_entrar


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

    barbearia_id = extrair(r'name="barbearia_id" value="(\w+)"', pagina)
    horario_id = extrair(r'name="horario_ocioso_id" value="(\w+)"', pagina)
    pagina = client.post("/barbeiro/blocos", data=dict(
        barbearia_id=barbearia_id, horario_ocioso_id=horario_id,
        inicio="2030-01-07T14:00", fim="2030-01-07T16:00"),
        follow_redirects=True).get_data(as_text=True)
    assert "Barbearia Exemplo" in pagina
    assert "R$ 60,00" in pagina
