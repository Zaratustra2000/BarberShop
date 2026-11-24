import pytest

from domain.erros import DadosInvalidos
from domain.servico import Servico


@pytest.mark.parametrize("nome,preco,duracao", [
    ("", 4500, 40),
    ("Corte", 0, 40),
    ("Corte", 4500, 4),
    ("Corte", 4500, 241),
])
def test_servico_invalido(nome, preco, duracao):
    with pytest.raises(DadosInvalidos):
        Servico(barbeiro_id="b1", nome=nome, preco_centavos=preco,
                duracao_minutos=duracao)


def test_servico_valido():
    servico = Servico(barbeiro_id="b1", nome=" Corte + barba ",
                      preco_centavos=7000, duracao_minutos=60)
    assert servico.nome == "Corte + barba"
