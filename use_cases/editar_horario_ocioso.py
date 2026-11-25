from datetime import datetime

from domain.barbearia import HorarioOcioso
from domain.erros import DadosInvalidos
from domain.periodo import Periodo
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.consultar_barbearias_do_dono import barbearia_do_dono
from use_cases.portas import (Relogio, RepositorioDeBarbearias,
                              RepositorioDeUsuarios)


class EditarHorarioOcioso:
    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias, relogio: Relogio):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._relogio = relogio

    def executar(self, dono_id: str, barbearia_id: str,
                 horario_ocioso_id: str, cadeira_id: str,
                 inicio: datetime, fim: datetime,
                 preco_por_hora_centavos: int) -> HorarioOcioso:
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        periodo = Periodo(inicio, fim)
        if periodo.inicio < self._relogio.agora():
            raise DadosInvalidos("O horário ocioso precisa ser no futuro.")
        horario = barbearia.editar_horario_ocioso(
            horario_ocioso_id, cadeira_id, periodo,
            preco_por_hora_centavos)
        self._barbearias.salvar(barbearia)
        return horario

    def excluir(self, dono_id: str, barbearia_id: str,
                horario_ocioso_id: str) -> None:
        exigir_usuario(self._usuarios, dono_id, Papel.DONO)
        barbearia = barbearia_do_dono(
            self._barbearias, dono_id, barbearia_id)
        barbearia.excluir_horario_ocioso(horario_ocioso_id)
        self._barbearias.salvar(barbearia)
