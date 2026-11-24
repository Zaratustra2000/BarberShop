from typing import List

from domain.usuario import Usuario
from use_cases.portas import RepositorioDeUsuarios


class BuscarBarbeiros:
    """US5: o cliente procura o barbeiro de confiança pelo nome."""

    def __init__(self, usuarios: RepositorioDeUsuarios):
        self._usuarios = usuarios

    def executar(self, nome: str) -> List[Usuario]:
        return self._usuarios.barbeiros_por_nome((nome or "").strip())
