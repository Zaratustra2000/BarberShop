from tests.app.conftest import cadastrar_e_entrar


def test_pagina_inicial_abre(client):
    assert client.get("/").status_code == 200


def test_cadastro_e_login_levam_ao_painel_da_persona(client):
    resposta = cadastrar_e_entrar(client, "dono", nome="Carlos Menezes")
    assert resposta.status_code == 200
    assert "Minhas barbearias" in resposta.get_data(as_text=True)


def test_login_errado_mostra_mensagem_generica(client):
    resposta = client.post("/login", data=dict(email="x@exemplo.com",
                                               senha="errada99"),
                           follow_redirects=True)
    assert "E-mail ou senha inválidos" in resposta.get_data(as_text=True)


def test_persona_nao_acessa_painel_de_outra(client):
    cadastrar_e_entrar(client, "cliente")
    assert client.get("/dono").status_code == 403
