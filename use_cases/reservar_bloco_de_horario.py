from datetime import datetime

from domain.barbearia import BlocoDeHorario
from domain.erros import ConflitoDeHorario, DadosInvalidos, NaoEncontrado
from domain.periodo import Periodo
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.portas import (RepositorioDeBarbearias, RepositorioDeUsuarios,
                              Relogio)


class ReservarBlocoDeHorario:
    """US4: o barbeiro reserva parte de um horário ocioso.

    As regras dentro da barbearia ficam no agregado; aqui fica a regra que
    atravessa barbearias: o barbeiro não pode estar em dois lugares ao mesmo
    tempo (ADR 0001).
    """

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias, relogio: Relogio):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._relogio = relogio

    def executar(self, barbeiro_id: str, barbearia_id: str,
                 horario_ocioso_id: str, inicio: datetime,
                 fim: datetime) -> BlocoDeHorario:
        exigir_usuario(self._usuarios, barbeiro_id, Papel.BARBEIRO)
        periodo = Periodo(inicio, fim)
        if periodo.inicio < self._relogio.agora():
            raise DadosInvalidos("O bloco precisa começar no futuro.")
        self._exigir_barbeiro_livre(barbeiro_id, periodo)
        barbearia = self._barbearias.por_id(barbearia_id)
        if barbearia is None:
            raise NaoEncontrado("Barbearia não encontrada.")
        bloco = barbearia.reservar_bloco(horario_ocioso_id, barbeiro_id,
                                         periodo)
        self._barbearias.salvar(barbearia)
        return bloco

    def _exigir_barbeiro_livre(self, barbeiro_id, periodo):
        for barbearia in self._barbearias.com_blocos_do_barbeiro(barbeiro_id):
            for bloco in barbearia.blocos_do_barbeiro(barbeiro_id):
                if bloco.periodo.sobrepoe(periodo):
                    raise ConflitoDeHorario(
                        "Você já tem um bloco nesse horário em {}.".format(
                            barbearia.nome))
