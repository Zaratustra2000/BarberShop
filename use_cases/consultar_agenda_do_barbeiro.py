from dataclasses import dataclass
from typing import Dict

from domain.agenda import AgendaDoBarbeiro
from use_cases.portas import (RepositorioDeAgendamentos,
                              RepositorioDeBarbearias, RepositorioDeUsuarios)


def montar_agenda(barbearias: RepositorioDeBarbearias,
                  agendamentos: RepositorioDeAgendamentos,
                  barbeiro_id: str) -> AgendaDoBarbeiro:
    return AgendaDoBarbeiro(barbeiro_id,
                            barbearias.com_blocos_do_barbeiro(barbeiro_id),
                            agendamentos.do_barbeiro(barbeiro_id))


@dataclass
class VisaoDaAgenda:
    agenda: AgendaDoBarbeiro
    nomes_dos_clientes: Dict[str, str]


class ConsultarAgendaDoBarbeiro:
    """US5: o barbeiro vê onde atende e quem vai atender."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias,
                 agendamentos: RepositorioDeAgendamentos):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._agendamentos = agendamentos

    def executar(self, barbeiro_id: str) -> VisaoDaAgenda:
        agenda = montar_agenda(self._barbearias, self._agendamentos,
                               barbeiro_id)
        nomes = {}
        for item in agenda.itens:
            for agendamento in item.agendamentos:
                cliente = self._usuarios.por_id(agendamento.cliente_id)
                nomes[agendamento.cliente_id] = cliente.nome if cliente else ""
        return VisaoDaAgenda(agenda, nomes)
