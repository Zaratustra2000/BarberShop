from dataclasses import dataclass
from typing import List, Optional

from domain.agendamento import Agendamento
from domain.avaliacao import Avaliacao
from domain.barbearia import Barbearia
from use_cases.portas import (RepositorioDeAgendamentos,
                              RepositorioDeAvaliacoes,
                              RepositorioDeBarbearias, RepositorioDeUsuarios,
                              Relogio)


@dataclass
class AgendamentoDoCliente:
    agendamento: Agendamento
    barbeiro_nome: str
    barbearia: Optional[Barbearia]
    avaliacao: Optional[Avaliacao] = None
    pode_avaliar: bool = False


class ConsultarAgendamentosDoCliente:
    """US5: o cliente vê seus agendamentos com barbeiro e endereço."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias,
                 agendamentos: RepositorioDeAgendamentos,
                 avaliacoes: RepositorioDeAvaliacoes, relogio: Relogio):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._agendamentos = agendamentos
        self._avaliacoes = avaliacoes
        self._relogio = relogio

    def executar(self, cliente_id: str) -> List[AgendamentoDoCliente]:
        agora = self._relogio.agora()
        resultado = []
        for agendamento in self._agendamentos.do_cliente(cliente_id):
            barbeiro = self._usuarios.por_id(agendamento.barbeiro_id)
            resultado.append(AgendamentoDoCliente(
                agendamento, barbeiro.nome if barbeiro else "",
                self._barbearias.por_id(agendamento.barbearia_id),
                self._avaliacoes.do_agendamento(agendamento.id),
                agendamento.avaliavel_em(agora)))
        return resultado
