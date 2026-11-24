from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.barbearia import (Barbearia, Cadeira, HorarioOcioso,
                              normalizar_bairro)
from domain.periodo import Periodo
from use_cases.portas import RepositorioDeBarbearias, Relogio


@dataclass
class OfertaDeCadeira:
    """Um horário ocioso com os trechos que ainda dá para reservar."""

    barbearia: Barbearia
    cadeira: Cadeira
    horario: HorarioOcioso
    periodos_livres: List[Periodo]


class BuscarCadeirasOciosas:
    """US4: o barbeiro procura cadeiras ociosas num bairro."""

    def __init__(self, barbearias: RepositorioDeBarbearias, relogio: Relogio):
        self._barbearias = barbearias
        self._relogio = relogio

    def executar(self, bairro: str) -> List[OfertaDeCadeira]:
        agora = self._relogio.agora()
        ofertas = []
        for barbearia in self._barbearias.no_bairro(
                normalizar_bairro(bairro)):
            for horario in barbearia.horarios_ociosos:
                livres = _a_partir_de(
                    agora, barbearia.periodos_livres(horario.id))
                if livres:
                    ofertas.append(OfertaDeCadeira(
                        barbearia, barbearia.cadeira(horario.cadeira_id),
                        horario, livres))
        return sorted(ofertas, key=lambda o: o.periodos_livres[0].inicio)


def _a_partir_de(agora: datetime, periodos: List[Periodo]) -> List[Periodo]:
    futuros = []
    for periodo in periodos:
        if periodo.fim <= agora:
            continue
        futuros.append(Periodo(max(periodo.inicio, agora), periodo.fim))
    return futuros
