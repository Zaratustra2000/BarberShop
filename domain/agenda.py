"""Agenda do barbeiro: onde e quando ele atende e o que já está marcado.

Módulo profundo: três operações (`itens`, `horarios_disponiveis`,
`agendar`) escondem o cruzamento entre blocos de várias barbearias,
agendamentos existentes, encaixe de serviços e sobreposição.
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Iterable, List

from domain.agendamento import Agendamento
from domain.barbearia import Barbearia, BlocoDeHorario
from domain.erros import ConflitoDeHorario, DadosInvalidos
from domain.periodo import Periodo
from domain.servico import Servico

PASSO = timedelta(minutes=30)


@dataclass
class ItemDaAgenda:
    barbearia: Barbearia
    bloco: BlocoDeHorario
    agendamentos: List[Agendamento] = field(default_factory=list)


@dataclass(frozen=True)
class HorarioDisponivel:
    inicio: datetime
    barbearia: Barbearia


class AgendaDoBarbeiro:
    def __init__(self, barbeiro_id: str, barbearias: Iterable[Barbearia],
                 agendamentos: Iterable[Agendamento]):
        self.barbeiro_id = barbeiro_id
        self._agendamentos = list(agendamentos)
        self._blocos = sorted(
            ((b, bloco) for b in barbearias
             for bloco in b.blocos_do_barbeiro(barbeiro_id)),
            key=lambda par: par[1].periodo.inicio)

    @property
    def itens(self) -> List[ItemDaAgenda]:
        return [ItemDaAgenda(barbearia, bloco, self._no_bloco(bloco))
                for barbearia, bloco in self._blocos]

    def a_partir_de(self, momento: datetime) -> List[ItemDaAgenda]:
        return [i for i in self.itens if i.bloco.periodo.fim > momento]

    def horarios_disponiveis(self, servico: Servico,
                             a_partir_de: datetime
                             ) -> List[HorarioDisponivel]:
        """Inícios possíveis para o serviço.

        Em cada trecho livre, oferece inícios a cada 30 minutos e também o
        último início possível, para que o fim do bloco não fique ocioso.
        """
        duracao = timedelta(minutes=servico.duracao_minutos)
        horarios = []
        for barbearia, bloco in self._blocos:
            ocupados = [a.periodo for a in self._no_bloco(bloco)]
            for livre in bloco.periodo.subtrair(ocupados):
                for inicio in _inicios(livre, duracao):
                    if inicio >= a_partir_de:
                        horarios.append(HorarioDisponivel(inicio, barbearia))
        return horarios

    def agendar(self, cliente_id: str, servico: Servico,
                inicio: datetime) -> Agendamento:
        if servico.barbeiro_id != self.barbeiro_id:
            raise DadosInvalidos("Este serviço é de outro barbeiro.")
        periodo = Periodo(inicio,
                          inicio + timedelta(minutes=servico.duracao_minutos))
        barbearia, bloco = self._bloco_que_contem(periodo)
        if any(a.periodo.sobrepoe(periodo) for a in self._agendamentos):
            raise ConflitoDeHorario("O barbeiro já tem um agendamento "
                                    "nesse horário.")
        agendamento = Agendamento(
            cliente_id=cliente_id, barbeiro_id=self.barbeiro_id,
            servico_id=servico.id, servico_nome=servico.nome,
            barbearia_id=barbearia.id, bloco_id=bloco.id, periodo=periodo,
            preco_centavos=servico.preco_centavos)
        self._agendamentos.append(agendamento)
        return agendamento

    def _bloco_que_contem(self, periodo):
        for barbearia, bloco in self._blocos:
            if bloco.periodo.contem(periodo):
                return barbearia, bloco
        raise DadosInvalidos("O barbeiro não atende nesse horário.")

    def _no_bloco(self, bloco):
        return sorted((a for a in self._agendamentos
                       if a.bloco_id == bloco.id),
                      key=lambda a: a.periodo.inicio)


def _inicios(livre: Periodo, duracao: timedelta) -> List[datetime]:
    ultimo = livre.fim - duracao
    inicios = []
    momento = livre.inicio
    while momento <= ultimo:
        inicios.append(momento)
        momento += PASSO
    if inicios and inicios[-1] != ultimo:
        inicios.append(ultimo)
    return inicios
