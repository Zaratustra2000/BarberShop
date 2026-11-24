import re

import pytest

from app.main import create_app
from tests.dubles import RelogioFixo


@pytest.fixture
def client(tmp_path):
    app = create_app(caminho_do_banco=str(tmp_path / "app.sqlite3"),
                     relogio=RelogioFixo(), secret_key="chave-de-teste")
    app.config["TESTING"] = True
    return app.test_client()


def cadastrar_e_entrar(client, papel, nome="Pessoa Teste", email=None):
    email = email or "{}@exemplo.com".format(papel)
    client.post("/cadastro", data=dict(nome=nome, email=email,
                                       senha="segredo1", papel=papel))
    return client.post("/login", data=dict(email=email, senha="segredo1"),
                       follow_redirects=True)


def extrair(padrao, html):
    """Pega o primeiro grupo de um padrão no HTML (ex.: ids em formulários)."""
    achado = re.search(padrao, html)
    assert achado, "padrão não encontrado: " + padrao
    return achado.group(1)
