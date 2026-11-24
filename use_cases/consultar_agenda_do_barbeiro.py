from dataclasses import dataclass
from typing import List

from domain.barbearia import Barbearia, BlocoDeHorario
from use_cases.portas import RepositorioDeBarbearias


@dataclass
class ItemDaAgenda:
    """Um bloco de horário do barbeiro e a barbearia onde ele acontece."""

    barbearia: Barbearia
    bloco: BlocoDeHorario


class ConsultarAgendaDoBarbeiro:
    """Agenda do barbeiro: onde e quando ele vai atender."""

    def __init__(self, barbearias: RepositorioDeBarbearias):
        self._barbearias = barbearias

    def executar(self, barbeiro_id: str) -> List[ItemDaAgenda]:
        itens = [ItemDaAgenda(barbearia, bloco)
                 for barbearia in self._barbearias.com_blocos_do_barbeiro(
                     barbeiro_id)
                 for bloco in barbearia.blocos_do_barbeiro(barbeiro_id)]
        return sorted(itens, key=lambda i: i.bloco.periodo.inicio)
