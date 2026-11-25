from datetime import datetime
from dataclasses import dataclass, field

from domain.identidade import novo_id
from domain.periodo import Periodo


@dataclass
class Agendamento:
    """Atendimento marcado por um cliente dentro de um bloco do barbeiro.

    Nome e preço do serviço são copiados no momento do agendamento: se o
    barbeiro mudar o preço depois, o combinado com o cliente não muda.
    """

    cliente_id: str
    barbeiro_id: str
    servico_id: str
    servico_nome: str
    barbearia_id: str
    bloco_id: str
    periodo: Periodo
    preco_centavos: int
    id: str = field(default_factory=novo_id)
    cancelado: bool = False

    def cancelar(self) -> None:
        self.cancelado = True

    def avaliavel_em(self, agora: datetime) -> bool:
        """Só se avalia o que não foi cancelado, depois do fim previsto.

        O horário passado não prova que o atendimento aconteceu.
        """
        return not self.cancelado and agora > self.periodo.fim
