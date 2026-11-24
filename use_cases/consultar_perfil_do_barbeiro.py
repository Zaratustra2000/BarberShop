from dataclasses import dataclass, field
from typing import List, Optional

from domain.agenda import AgendaDoBarbeiro, HorarioDisponivel, ItemDaAgenda
from domain.erros import NaoEncontrado
from domain.servico import Servico
from domain.usuario import Papel, Usuario
from use_cases.acesso import exigir_usuario
from use_cases.consultar_agenda_do_barbeiro import montar_agenda
from use_cases.portas import (RepositorioDeAgendamentos,
                              RepositorioDeBarbearias, RepositorioDeServicos,
                              RepositorioDeUsuarios, Relogio)


@dataclass
class PerfilDoBarbeiro:
    barbeiro: Usuario
    servicos: List[Servico]
    agenda: AgendaDoBarbeiro
    proximos_locais: List[ItemDaAgenda]
    servico_escolhido: Optional[Servico] = None
    horarios: List[HorarioDisponivel] = field(default_factory=list)


class ConsultarPerfilDoBarbeiro:
    """US5: serviços, onde o barbeiro vai atender e horários livres."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias,
                 servicos: RepositorioDeServicos,
                 agendamentos: RepositorioDeAgendamentos, relogio: Relogio):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._servicos = servicos
        self._agendamentos = agendamentos
        self._relogio = relogio

    def executar(self, barbeiro_id: str,
                 servico_id: Optional[str] = None) -> PerfilDoBarbeiro:
        barbeiro = exigir_usuario(self._usuarios, barbeiro_id,
                                  Papel.BARBEIRO)
        agora = self._relogio.agora()
        agenda = montar_agenda(self._barbearias, self._agendamentos,
                               barbeiro_id)
        perfil = PerfilDoBarbeiro(
            barbeiro=barbeiro,
            servicos=self._servicos.do_barbeiro(barbeiro_id),
            agenda=agenda, proximos_locais=agenda.a_partir_de(agora))
        if servico_id:
            servico = self._servicos.por_id(servico_id)
            if servico is None or servico.barbeiro_id != barbeiro_id:
                raise NaoEncontrado("Serviço não encontrado.")
            perfil.servico_escolhido = servico
            perfil.horarios = agenda.horarios_disponiveis(servico, agora)
        return perfil
