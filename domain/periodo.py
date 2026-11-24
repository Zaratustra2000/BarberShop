from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List

from domain.erros import DadosInvalidos


@dataclass(frozen=True)
class Periodo:
    """Intervalo de tempo semiaberto [inicio, fim)."""

    inicio: datetime
    fim: datetime

    def __post_init__(self):
        if self.fim <= self.inicio:
            raise DadosInvalidos("O fim precisa ser depois do início.")

    @property
    def minutos(self) -> int:
        return int((self.fim - self.inicio).total_seconds() // 60)

    def sobrepoe(self, outro: "Periodo") -> bool:
        return self.inicio < outro.fim and outro.inicio < self.fim

    def contem(self, outro: "Periodo") -> bool:
        return self.inicio <= outro.inicio and outro.fim <= self.fim

    def subtrair(self, ocupados: Iterable["Periodo"]) -> List["Periodo"]:
        """Devolve os trechos deste período que não estão ocupados."""
        livres = []
        cursor = self.inicio
        for ocupado in sorted(ocupados, key=lambda o: o.inicio):
            if not self.sobrepoe(ocupado):
                continue
            if ocupado.inicio > cursor:
                livres.append(Periodo(cursor, ocupado.inicio))
            cursor = max(cursor, ocupado.fim)
        if cursor < self.fim:
            livres.append(Periodo(cursor, self.fim))
        return livres
