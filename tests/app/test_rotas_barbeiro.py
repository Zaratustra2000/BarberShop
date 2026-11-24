from tests.app.conftest import cadastrar_e_entrar


def test_barbeiro_cadastra_servico_e_ve_no_painel(client):
    cadastrar_e_entrar(client, "barbeiro")
    pagina = client.post("/barbeiro/servicos", data=dict(
        nome="Corte degradê", preco="45,00", duracao_minutos="40"),
        follow_redirects=True).get_data(as_text=True)
    assert "Corte degradê" in pagina
    assert "R$ 45,00" in pagina
    assert "40 min" in pagina
