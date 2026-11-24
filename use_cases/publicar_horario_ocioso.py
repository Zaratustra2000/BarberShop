from datetime import datetime

from domain.barbearia import HorarioOcioso
from domain.erros import DadosInvalidos
from domain.periodo import Periodo
from use_cases.consultar_barbearias_do_dono import barbearia_do_dono
from use_cases.portas import RepositorioDeBarbearias, Relogio


class PublicarHorarioOcioso:
    """US2: o dono oferece uma cadeira para aluguel num período."""

    def __init__(self, barbearias: RepositorioDeBarbearias, relogio: Relogio):
        self._barbearias = barbearias
        self._relogio = relogio

    def executar(self, dono_id: str, barbearia_id: str, cadeira_id: str,
                 inicio: datetime, fim: datetime,
                 preco_por_hora_centavos: int) -> HorarioOcioso:
        barbearia = barbearia_do_dono(self._barbearias, dono_id,
                                      barbearia_id)
        periodo = Periodo(inicio, fim)
        if periodo.inicio < self._relogio.agora():
            raise DadosInvalidos("O horário ocioso precisa ser no futuro.")
        horario = barbearia.publicar_horario_ocioso(
            cadeira_id, periodo, preco_por_hora_centavos)
        self._barbearias.salvar(barbearia)
        return horario
