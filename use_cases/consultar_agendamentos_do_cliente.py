from dataclasses import dataclass
from typing import List, Optional

from domain.agendamento import Agendamento
from domain.barbearia import Barbearia
from use_cases.portas import (RepositorioDeAgendamentos,
                              RepositorioDeBarbearias, RepositorioDeUsuarios)


@dataclass
class AgendamentoDoCliente:
    agendamento: Agendamento
    barbeiro_nome: str
    barbearia: Optional[Barbearia]


class ConsultarAgendamentosDoCliente:
    """US5: o cliente vê seus agendamentos com barbeiro e endereço."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias,
                 agendamentos: RepositorioDeAgendamentos):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._agendamentos = agendamentos

    def executar(self, cliente_id: str) -> List[AgendamentoDoCliente]:
        resultado = []
        for agendamento in self._agendamentos.do_cliente(cliente_id):
            barbeiro = self._usuarios.por_id(agendamento.barbeiro_id)
            resultado.append(AgendamentoDoCliente(
                agendamento, barbeiro.nome if barbeiro else "",
                self._barbearias.por_id(agendamento.barbearia_id)))
        return resultado
