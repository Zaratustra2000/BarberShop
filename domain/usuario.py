from dataclasses import dataclass, field
from enum import Enum

from domain.erros import AcessoNegado, DadosInvalidos
from domain.identidade import novo_id


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
    apresentacao: str = ""
    foto_perfil: str = ""
    breve_apresentacao: str = ""
    foto: str = ""

    def __post_init__(self):
        self.nome = (self.nome or "").strip()
        self.email = (self.email or "").strip().lower()
        self.apresentacao = (self.apresentacao or "").strip()
        if not self.apresentacao:
            self.apresentacao = (self.breve_apresentacao or "").strip()
        self.breve_apresentacao = self.apresentacao
        if not self.nome:
            raise DadosInvalidos("Informe o nome.")
        if "@" not in self.email or self.email.startswith("@"):
            raise DadosInvalidos("Informe um e-mail válido.")
        if len(self.apresentacao) > 500:
            raise DadosInvalidos(
                "A apresentação deve ter no máximo 500 caracteres.")
        self.foto_perfil = self.foto_perfil or ""
        if not self.foto_perfil:
            self.foto_perfil = self.foto or ""
        self.foto = self.foto_perfil

    def editar_perfil_do_barbeiro(self, nome: str,
                                  apresentacao: str) -> None:
        nome = (nome or "").strip()
        apresentacao = (apresentacao or "").strip()
        if not nome:
            raise DadosInvalidos("Informe o nome.")
        if len(apresentacao) > 500:
            raise DadosInvalidos(
                "A apresentação deve ter no máximo 500 caracteres.")
        self.nome = nome
        self.apresentacao = apresentacao
        self.breve_apresentacao = apresentacao

    def definir_foto_perfil(self, nome_do_arquivo: str) -> None:
        self.foto_perfil = nome_do_arquivo or ""
        self.foto = self.foto_perfil

    def exigir_papel(self, papel: Papel) -> None:
        if self.papel != papel:
            raise AcessoNegado(
                "Esta ação é exclusiva de {}.".format(papel.value))
