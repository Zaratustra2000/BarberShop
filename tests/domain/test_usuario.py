import pytest

from domain.erros import AcessoNegado, DadosInvalidos
from domain.usuario import Papel, Usuario


def novo(**kw):
    dados = dict(nome="Rafa Souza", email="rafa@exemplo.com",
                 senha_hash="h", papel=Papel.BARBEIRO)
    dados.update(kw)
    return Usuario(**dados)


def test_email_e_normalizado():
    assert novo(email="  Rafa@Exemplo.COM ").email == "rafa@exemplo.com"


def test_email_sem_arroba_e_invalido():
    with pytest.raises(DadosInvalidos):
        novo(email="rafa.exemplo.com")


def test_nome_obrigatorio():
    with pytest.raises(DadosInvalidos):
        novo(nome="   ")


def test_exigir_papel_de_outra_persona_nega_acesso():
    with pytest.raises(AcessoNegado):
        novo(papel=Papel.CLIENTE).exigir_papel(Papel.BARBEIRO)
