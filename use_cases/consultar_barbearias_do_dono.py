from typing import List

from domain.barbearia import Barbearia
from domain.erros import AcessoNegado, NaoEncontrado
from use_cases.portas import RepositorioDeBarbearias


class ConsultarBarbeariasDoDono:
    """US2: painel do dono, só com as barbearias dele."""

    def __init__(self, barbearias: RepositorioDeBarbearias):
        self._barbearias = barbearias

    def executar(self, dono_id: str) -> List[Barbearia]:
        return self._barbearias.do_dono(dono_id)

    def uma(self, dono_id: str, barbearia_id: str) -> Barbearia:
        return barbearia_do_dono(self._barbearias, dono_id, barbearia_id)


def barbearia_do_dono(barbearias: RepositorioDeBarbearias, dono_id: str,
                      barbearia_id: str) -> Barbearia:
    barbearia = barbearias.por_id(barbearia_id)
    if barbearia is None:
        raise NaoEncontrado("Barbearia não encontrada.")
    if not barbearia.pertence_a(dono_id):
        raise AcessoNegado("Esta barbearia é de outro dono.")
    return barbearia
