from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from domain.erros import AcessoNegado, DadosInvalidos


def novo_id() -> str:
    return uuid4().hex


class Papel(Enum):
    """Persona com que a pessoa usa o produto."""

    DONO = "dono"
    BARBEIRO = "barbeiro"
    CLIENTE = "cliente"

    @classmethod
    def de_texto(cls, valor: str) -> "Papel":
        try:
            return cls(valor)
        except ValueError:
            raise DadosInvalidos("Persona desconhecida: {}".format(valor))


@dataclass
class Usuario:
    nome: str
    email: str
    senha_hash: str
    papel: Papel
    id: str = field(default_factory=novo_id)

    def __post_init__(self):
        self.nome = (self.nome or "").strip()
        self.email = (self.email or "").strip().lower()
        if not self.nome:
            raise DadosInvalidos("Informe o nome.")
        if "@" not in self.email or self.email.startswith("@"):
            raise DadosInvalidos("Informe um e-mail válido.")

    def exigir_papel(self, papel: Papel) -> None:
        if self.papel != papel:
            raise AcessoNegado(
                "Esta ação é exclusiva de {}.".format(papel.value))
