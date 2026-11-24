from dataclasses import dataclass, field
from typing import Iterable, Optional

from domain.identidade import novo_id


@dataclass
class Avaliacao:
    agendamento_id: str
    cliente_id: str
    barbeiro_id: str
    nota: int
    id: str = field(default_factory=novo_id)


@dataclass(frozen=True)
class ResumoDeAvaliacoes:
    """Média e quantidade das Avaliações; sem Avaliações, não há média."""
    quantidade: int = 0
    media: Optional[float] = None

    @classmethod
    def de(cls, avaliacoes: Iterable[Avaliacao]) -> "ResumoDeAvaliacoes":
        notas = [a.nota for a in avaliacoes]
        if not notas:
            return cls()
        return cls(quantidade=len(notas), media=sum(notas) / len(notas))
