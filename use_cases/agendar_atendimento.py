from datetime import datetime

from domain.agendamento import Agendamento
from domain.erros import DadosInvalidos, NaoEncontrado
from domain.usuario import Papel
from use_cases.acesso import exigir_usuario
from use_cases.consultar_agenda_do_barbeiro import montar_agenda
from use_cases.portas import (RepositorioDeAgendamentos,
                              RepositorioDeBarbearias, RepositorioDeServicos,
                              RepositorioDeUsuarios, Relogio)


class AgendarAtendimento:
    """US5: o cliente marca um serviço dentro de um bloco do barbeiro."""

    def __init__(self, usuarios: RepositorioDeUsuarios,
                 barbearias: RepositorioDeBarbearias,
                 servicos: RepositorioDeServicos,
                 agendamentos: RepositorioDeAgendamentos, relogio: Relogio):
        self._usuarios = usuarios
        self._barbearias = barbearias
        self._servicos = servicos
        self._agendamentos = agendamentos
        self._relogio = relogio

    def executar(self, cliente_id: str, servico_id: str,
                 inicio: datetime) -> Agendamento:
        exigir_usuario(self._usuarios, cliente_id, Papel.CLIENTE)
        if inicio < self._relogio.agora():
            raise DadosInvalidos("Escolha um horário no futuro.")
        servico = self._servicos.por_id(servico_id)
        if servico is None:
            raise NaoEncontrado("Serviço não encontrado.")
        agenda = montar_agenda(self._barbearias, self._agendamentos,
                               servico.barbeiro_id)
        agendamento = agenda.agendar(cliente_id, servico, inicio)
        self._agendamentos.salvar(agendamento)
        return agendamento
