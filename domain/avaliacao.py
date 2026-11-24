from dataclasses import dataclass, field

from domain.identidade import novo_id


@dataclass
class Avaliacao:
    agendamento_id: str
    cliente_id: str
    barbeiro_id: str
    nota: int
    id: str = field(default_factory=novo_id)

