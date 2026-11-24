from domain.avaliacao import Avaliacao
from domain.erros import AcessoNegado, DadosInvalidos, NaoEncontrado
from use_cases.portas import (
    RepositorioDeAgendamentos,
    RepositorioDeAvaliacoes,
    RepositorioDeUsuarios,
    Relogio,
)


class AvaliarAgendamento:
    def __init__(self, usuarios: RepositorioDeUsuarios,
                 agendamentos: RepositorioDeAgendamentos,
                 avaliacoes: RepositorioDeAvaliacoes,
                 relogio: Relogio):
        self._usuarios = usuarios
        self._agendamentos = agendamentos
        self._avaliacoes = avaliacoes
        self._relogio = relogio

    def executar(self, cliente_id: str, agendamento_id: str,
                 nota: int) -> Avaliacao:
        if (isinstance(nota, bool) or not isinstance(nota, int)
                or not 1 <= nota <= 5):
            raise DadosInvalidos("A nota deve ser um número inteiro de 1 a 5.")
        if self._usuarios.por_id(cliente_id) is None:
            raise NaoEncontrado("Cliente não encontrado.")
        agendamento = self._agendamentos.por_id(agendamento_id)
        if agendamento is None:
            raise NaoEncontrado("Agendamento não encontrado.")
        if agendamento.cliente_id != cliente_id:
            raise AcessoNegado(
                "Somente o Cliente dono do Agendamento pode avaliá-lo.")
        if not agendamento.avaliavel_em(self._relogio.agora()):
            raise DadosInvalidos(
                "Só é possível avaliar Agendamento não cancelado, "
                "depois do horário previsto de término.")

        existente = self._avaliacoes.do_agendamento(agendamento_id)
        if existente:
            existente.nota = nota
            avaliacao = existente
        else:
            avaliacao = Avaliacao(
                agendamento_id=agendamento.id,
                cliente_id=cliente_id,
                barbeiro_id=agendamento.barbeiro_id,
                nota=nota)
        self._avaliacoes.salvar(avaliacao)
        return avaliacao
