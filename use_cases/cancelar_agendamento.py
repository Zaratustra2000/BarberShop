from domain.agendamento import Agendamento
from domain.erros import AcessoNegado, DadosInvalidos, NaoEncontrado
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.portas import (RepositorioDeAgendamentos,
                              RepositorioDeUsuarios, Relogio)


class CancelarAgendamento:
    """O barbeiro responsável cancela um agendamento futuro."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 agendamentos: RepositorioDeAgendamentos,
                 relogio: Relogio):
        self._usuarios = usuarios
        self._agendamentos = agendamentos
        self._relogio = relogio

    def executar(self, barbeiro_id: str,
                 agendamento_id: str) -> Agendamento:
        exigir_usuario(self._usuarios, barbeiro_id, Papel.BARBEIRO)
        agendamento = self._agendamentos.por_id(agendamento_id)
        if agendamento is None:
            raise NaoEncontrado("Agendamento não encontrado.")
        if agendamento.cancelado:
            raise DadosInvalidos("Este agendamento já está cancelado.")
        if agendamento.barbeiro_id != barbeiro_id:
            raise AcessoNegado(
                "Somente o barbeiro responsável pode cancelar.")
        if agendamento.periodo.inicio <= self._relogio.agora():
            raise DadosInvalidos(
                "Somente agendamentos futuros podem ser cancelados.")
        agendamento.cancelar()
        self._agendamentos.salvar(agendamento)
        return agendamento
